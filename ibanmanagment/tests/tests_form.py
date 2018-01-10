from django.test import TestCase
from ibanmanagment.models import IbanDetails
from django.core.management import call_command
from ibanmanagment.forms import IbanDetailsForm
# Create your tests here.
class IbanFormTestCase(TestCase):

    def test_form_success(self):
        """
            To check Form is valid or not.
        """
        form_data = {
            "first_name":"anup",
            "last_name":"yadav",
            "iban_number":"DE89 3704 0044 0532 0130 00",
        }
        form = IbanDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())

    #Iban number exception.
    def test_form_error(self):
        """
            To check Form is testing to perfect Iban number or not.
        """
        form_data = {
            "first_name":"anup",
            "last_name":"yadav",
            "iban_number":"123456789",
        }
        form = IbanDetailsForm(data=form_data)
        #for error in form.errors:print(error) This should raise exception to IBAN number.
        self.assertFalse(form.is_valid())