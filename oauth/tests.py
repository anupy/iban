"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".
Replace these with more appropriate tests for your application.
"""

from django.test import TestCase, RequestFactory, Client
from oauth.views import AuthView
from django.core.management import call_command
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse


class OauthTestCase(TestCase):
    def setUp(self):
        # If only response is required.
        self.client = Client()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # sample json, google like data.
        self.google_profile = {
            'gender': 'male',
            'profile': 'https://plus.google.com/116778214376484098997',
            'family_name': 'yadav',
            'locale': 'en-GB',
            'sub': '116778214376484098997',
            'picture': 'https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg',
            'email_verified': True,
            'given_name': 'anup',
            'email': 'anupyadav1234@gmail.com',
            'name': 'anup yadav'
        }
        self.request = self.factory.get('auth/complete/google-oauth2/')
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)

        fixtures = 'group_admin.json'
        call_command('loaddata', fixtures, verbosity=0)

    def run_all_test(self):
        self.check_account_exist_or_create_test()
        self.check_account_exist_or_create_test_new_user()
        self.check_account_exist_or_create_test_is_active()
        self.check_account_exist_or_create_test_is_superadmin()
        self.check_account_exist_or_create_test_is_admin()        

    def check_account_exist_or_create_test(self):
        user = AuthView.check_account_exist_or_create(self.request,self.google_profile)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.google_profile['email'])

    def check_account_exist_or_create_test_new_user(self):
        self.google_profile['email'] = "newadmin@gmail.com"
        user = AuthView.check_account_exist_or_create(self.request,self.google_profile)
        self.assertIsInstance(user, User)
        self.assertIsInstance(user.groups.all()[0], Group)
        self.assertFalse(user.is_active)

    # Exceptional in case is_active is false
    def check_account_exist_or_create_test_is_active(self):
        self.google_profile['email'] = "inactive@gmail.com"
        user = AuthView.check_account_exist_or_create(self.request,self.google_profile)
        self.assertFalse(user)

    # Exceptional in case is_superadmin is true
    def check_account_exist_or_create_test_is_superadmin(self):
        # with self.assertRaisesMessage(Exception, 'User is non admin.'):
        self.google_profile['email'] = "anupy27@gmail.com"
        user = AuthView.check_account_exist_or_create(self.request,self.google_profile)
        self.assertTrue(user)

    # Exceptional in case is_admin is true
    def check_account_exist_or_create_test_is_admin(self):
        self.google_profile['email'] = "noadmin@gmail.com"
        user = AuthView.check_account_exist_or_create(self.request,self.google_profile)
        self.assertFalse(user)
