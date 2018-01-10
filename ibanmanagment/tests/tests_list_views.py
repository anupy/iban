from django.test import TestCase
from django.contrib.auth.models import User, Group
from ibanmanagment.models import IbanDetails
from django.core.management import call_command
from django.core.urlresolvers import reverse
# Create your tests here.
class IbanViewTestCase(TestCase):

    #Dashboard should redirect if anonymous user tries to login to system.
    def dashboard_negative_test(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/?next=/dashboard/')
        self.assertEqual(response.status_code, 302)

    #Dashboard should work for logged in user. And should return 3 object of list of IbanDetails.
    def dashboard_list_test(self):
        """
        List View / Dashboard unittest.
        Should retrive list of objects of IbanDetails.
        """
        user = User.objects.create_user(username='flyuser',email='flyuser@gmail.com',password='flyuser')
        fixtures = 'iban_details.json'
        call_command('loaddata', fixtures, verbosity=0)
        login = self.client.login(username='flyuser', password='flyuser')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('ibandetails_list')),3)
        
    def dashboard_no_list_test(self):
        """
        List View / Dashboard unittest.
        Should retrive zero objects of IbanDetails, but message should get matched.
        """
        user = User.objects.create_user(username='flyuser',email='flyuser@gmail.com',password='flyuser')
        login = self.client.login(username='flyuser', password='flyuser')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"No IBAN Numbers are added yet.")