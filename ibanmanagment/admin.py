from django.contrib import admin
from ibanmanagment.models import IbanDetails
from .forms import *
# Register your models here.


@admin.register(IbanDetails)
class IbanDetailsAdmin(admin.ModelAdmin):
    form = IbanDetailsForm
    fields = (('first_name','last_name'),('iban_number','status'),('creator',))
    list_display = ('first_name','last_name','iban_number','creator','status')
    search_fields = ('first_name','last_name','iban_number','status')