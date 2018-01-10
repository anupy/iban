from django import forms
from ibanmanagment.models import IbanDetails
from django.forms import widgets
from schwifty import IBAN
class IbanDetailsForm(forms.ModelForm):
    #@TODO :: We might need to implement live API to verify.
    # We need to purchase this service.
    # https://www.iban.com/validation-api.html Need to discuss.
    def clean_iban_number(self):
        """ Default clean method of iban_number to check valid iban
            using schwifty Python library.
            schwifty need to pass iban number strinf format.
            Library returns excpetion if not validated.
            else return same number.
        """
        try:
            iban = IBAN(self.cleaned_data.get("iban_number"))
            if iban:
                return self.cleaned_data.get("iban_number")
        except Exception as e:
            raise forms.ValidationError('This Iban is not valid. Please correct and try again.')
        return self.cleaned_data.get("iban_number")

    class Meta:
        model = IbanDetails
        fields = ['first_name','last_name','iban_number']
        exclude = ('created_at','updated_at')
        CHOICES = ((True, 'Active',), (False, 'Inactive',))
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'iban_number':forms.TextInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'first_name':{
                'required':'Please Enter First Name.'
            },
            'last_name':{
                'required':'Please Enter Last Name.'
            },
            'iban_number':{
                'required':'Please Enter Iban Number.'
            }
        }
    class Media:
        js = (('js/iban.js','js/iban_details.js',))