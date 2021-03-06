from fperms import enums
from fperms.models import Perm

from .base import ArticleTestCase, ArticleUserPermTestCase, ArticleGroupPermTestCase


class ModelPermTestCaseMixin:

    def _create_perm(self):
        return self._create_add_perm()

    def _create_add_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_MODEL,
            codename='add',
            content_type=self._get_content_type()
        )

    def _create_delete_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_MODEL,
            codename='delete',
            content_type=self._get_content_type()
        )

    def _create_wildcard_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_MODEL,
            codename=enums.PERM_CODENAME_WILDCARD,
            content_type=self._get_content_type()
        )


class ModelPermTestCase(ModelPermTestCaseMixin, ArticleTestCase):

    def test_perm_has_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_model_perm())


class ArticleUserModelPermPermTestCase(ModelPermTestCaseMixin, ArticleUserPermTestCase):

    def test_add_model_perm_by_perm(self):
        perm = self._create_perm()

        self.user.fperms.add_perm(perm)

        self.assertTrue(self.user.fperms.has_perm(perm))

    def test_add_model_perm_by_str(self):
        add_perm = self._create_add_perm()

        self.user.fperms.add_perm('model.articles.Article.add')

        self.assertTrue(self.user.fperms.has_perm(add_perm))

    def test_fail_add_model_perm_by_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.fperms.add_perm('model.articles.Article.delete')

    def test_fail_add_model_perm_by_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(LookupError):
            self.user.fperms.add_perm('model.articles.Bar.fap')

    def test_has_model_perm_from_wildcard(self):
        self._create_wildcard_perm()

        self.user.fperms.add_perm('model.articles.Article.*')

        self.assertTrue(self.user.fperms.has_perm('model.articles.Article.whatever'))


class ArticleGroupModelPermPermTestCase(ModelPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_model_perm_by_perm(self):
        perm = self._create_perm()

        self.group.fperms.add_perm(perm)

        self.assertTrue(self.group.fperms.has_perm(perm))

    def test_add_model_perm_by_str(self):
        add_perm = self._create_add_perm()

        self.group.fperms.add_perm('model.articles.Article.add')

        self.assertTrue(self.group.fperms.has_perm(add_perm))

        # test perm is correctly available to the user as well
        self.assertFalse(self.user.fperms.has_perm(add_perm))

        self.user.fgroups.add(self.group)

        self.assertTrue(self.user.fperms.has_perm(add_perm))

    def test_fail_add_model_perm_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.fperms.add_perm('model.articles.Article.delete')

    def test_fail_add_model_perm_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(LookupError):
            self.group.fperms.add_perm('model.articles.Bar.fap')
