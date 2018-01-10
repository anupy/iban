from django.test import TestCase
from django.contrib.auth.models import User, Group
from ibanmanagment.models import IbanDetails
from django.core.management import call_command
from django.core.urlresolvers import reverse

# Create your tests here.
class IbanCreateUpdateDeleteViewTestCase(TestCase):
    
    def iban_create_update_delete_test_permission(self):
        """
        Iban create and update view.
        Should not reach to the page of create and update of IbanDetails, should display error of permission denied.
        """
        #Create View UnitTest
        user = User.objects.create_user(username='flyuser',email='flyuser@gmail.com',password='flyuser')
        login = self.client.login(username='flyuser', password='flyuser')
        response = self.client.get(reverse('createiban'))
        self.assertTrue('Permission Denied - Error 403' in str(response.content)) #Expected output is Permission Denied.

        #Update View UnitTest
        url = reverse('updateiban', args=[1])
        self.assertEqual(url, '/updateiban/1/')
        response = self.client.get(url)
        self.assertTrue('Permission Denied - Error 403' in str(response.content)) #Expected output is Permission Denied.

        #Delete View UnitTest
        url = reverse('deleteiban', args=[1])
        self.assertEqual(url, '/deleteiban/1/')
        response = self.client.get(url)
        self.assertTrue('Permission Denied - Error 403' in str(response.content)) #Expected output is Permission Denied.

    def iban_create_update_delete_test_valid(self):
        """
        Iban create view.
        Should be create objects of IbanDetails.
        """
        #This is to enter Permissions, Group and their mapping.
        fixtures = 'permission_group.json'
        call_command('loaddata', fixtures, verbosity=0)
        user = User.objects.create_user(username='flyuser',email='flyuser@gmail.com',password='flyuser')
        group = Group.objects.get(pk=1)
        user.groups.add(group)
        login = self.client.login(username='flyuser', password='flyuser')
        response = self.client.get(reverse('createiban'))
        self.assertEqual(response.status_code, 200) #Should display add page
        self.assertTrue('Add New IBAN Detail' in str(response.content)) #Expected output is to display form page.
        ibanformdata = {"first_name":"anup",
            "last_name":"yadav",
            "iban_number":"123456789",
            "status":True,
            "creator":user.id,
            "created_at":"2017-12-26 12:33:52.94701+05:30",
            "updated_at":"2017-12-26 12:33:52.94701+05:30"
        }
        response = self.client.post("/createiban/", ibanformdata)
        ########## Checking for Valid IBAN message. #################
        self.assertTrue('This Iban is not valid. Please correct and try again.' in str(response.content)) #Should verify iban through schwifty

        ##########  Checking for perfect insertion / posititve test. ############
        ibanformdata['iban_number'] = "EE38 2200 2210 2014 5685"
        response = self.client.post("/createiban/", ibanformdata)
        iban = IbanDetails.objects.last()
        self.assertEqual(iban.iban_number, "EE38 2200 2210 2014 5685") #Just to verify.

        ##### Should not allow duplicate IBAN, this won't but still added in unittest for future reference. ######
        response = self.client.post("/createiban/", ibanformdata)
        self.assertTrue('Iban Details with this Iban number already exists.' in str(response.content))

        self.client.logout() #Logging out one user to login another user, which is hacker.
        dummyuser = User.objects.create_user(username='dummyuser',email='dummyuser@gmail.com',password='dummyuser')
        group = Group.objects.get(pk=1)
        dummyuser.groups.add(group)
        #Login through hacking user / administrator, and trying to access update page of another Iban creator.
        login = self.client.login(username='dummyuser', password='dummyuser')

        ########## Update view should not allow ###########
        url = reverse('updateiban', args=[1])
        self.assertEqual(url, '/updateiban/1/')
        response = self.client.get(url)
        self.assertTrue('Permission Denied - Error 403' in str(response.content)) # Expected output is Permission Denied.

        ############# Checking the permission / ownership for delete view as well.#############
        deleteurl = reverse('deleteiban', args=[1])
        self.assertEqual(deleteurl, '/deleteiban/1/')
        response = self.client.get(deleteurl)
        self.assertTrue('Permission Denied - Error 403' in str(response.content)) #Expected output is Permission Denied.

        #Now trying to post values using dummy user, so changing creator and it must return Permission debied error.
        #Ownership permission has to be tested in post as well.
        ibanformdata['creator'] = dummyuser.id
        response = self.client.post(url, ibanformdata)
        self.assertTrue('Permission Denied - Error 403' in str(response.content)) #Expected output is Permission Denied.

        ## Delete should not allow.
        response = self.client.post(deleteurl, {"id":1})
        self.assertTrue('Permission Denied - Error 403' in str(response.content)) #Expected output is Permission Denied.

        self.client.logout() #Loging out hacker.
        #Allow update and delete test. Positive test for update and deletion of records.
        login = self.client.login(username='flyuser', password='flyuser')
        url = reverse('updateiban', args=[1])
        self.assertEqual(url, '/updateiban/1/')
        response = self.client.get(url)
        self.assertTrue('Add New IBAN Detail' in str(response.content)) #Expected output is to display form page.

        ####### Allow valid user to update record. #######
        ibanformdata['first_name'] = "update"
        response = self.client.post(url, ibanformdata)
        iban = IbanDetails.objects.get(pk=1)
        self.assertEqual(iban.first_name, "update")

        ####### Allow valid user to delete record. #######
        response = self.client.post(deleteurl, {"id":1})
        self.assertRedirects(response, '/dashboard/') #Should redirect to list page after delete.
        self.assertEqual(response.status_code, 302) #Should match the 302, redirection.
        iban = IbanDetails.objects.filter(id=1)
        self.assertFalse(iban.count()) #Expect 0 records.
