from django.test import TestCase
from ibanmanagment.models import IbanDetails
from django.core.management import call_command
# Create your tests here.
class IbanModelTestCase(TestCase):

    def setUp(self):
        fixtures = 'group_admin.json'
        call_command('loaddata', fixtures, verbosity=0)

    def test_iban_details_model(self):
        """
        Model specific unittest.
        Should check create object of IbanDetails.
        """
        detail = IbanDetails.objects.create(first_name = "anup",
            last_name = "yadav",iban_number = "123456789012",status = True,
            creator_id = "1",created_at = "2017-12-29 12:33:52.94701+05:30",
            updated_at = "2017-12-29 12:33:52.94701+05:30")
        self.assertIsInstance(detail,IbanDetails)

    def test_str_is_equal_to_iban_number(self):
        """
        Model specific unittest.
        Method `__str__` should be equal to field `title`
        """
        iban = IbanDetails.objects.get(pk=1)
        self.assertEqual(str(iban), iban.iban_number)
