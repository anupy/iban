from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Need to make email as unique field.
User._meta.get_field('email')._unique = True


def is_admin(self):
    """Function check user access and permissions.

    Args:
        user : object of class User

    Returns:
        Object - Return object of found else None from Exception.

    """
    return self.groups.filter(name='admin').exists()

User.add_to_class("is_admin",is_admin)