from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class IbanDetails(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    iban_number = models.CharField(max_length=200,unique=True)
    status = models.BooleanField(default=True)
    creator = models.ForeignKey(User, models.DO_NOTHING, related_name='created_by_admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.iban_number

    #Checking ownership of record / row.
    def is_owner(self,user):
        return self.creator == user

    class Meta:
        #managed = False
        db_table = 'iban_details'
        verbose_name = "Iban Details"
        verbose_name_plural = "Iban Details"