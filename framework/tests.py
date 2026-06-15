from django.test import TestCase
from django_currentuser.middleware import _set_current_user


class BaseTestCase(TestCase):
    def tearDown(self):
        _set_current_user(None)