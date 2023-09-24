from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from helpers import utils


from .manager import MyAccountManager

class Organization(models.Model):
    uid = models.CharField(max_length=255, unique= True, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    address_line = models.JSONField(default = dict, null= True, blank= True)

    def save(self, *args, **kwargs):
            
        if not self.uid:
            self.uid = utils.generate_unique_id(5)
            
        super().save(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE=(
        ('manager','manager'),
        ('user','user')
    )
    
    password = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True,unique=True)
    contact = models.CharField(max_length=255, null= True, blank= True, unique= True)

    org = models.ForeignKey(Organization, on_delete= models.CASCADE, null= True, blank=True)
    token= models.TextField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    access = models.JSONField(default = dict, null= True, blank= True)
    USERNAME_FIELD = "email"	
    REQUIRED_FIELDS = ["password"]

    objects = MyAccountManager()


    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name if full_name else self.email

    @property
    def full_name(self):
        return self.get_full_name()
    
    @property
    def full_contact_number(self):
        if self.contact_number:
            contact_number = '+91' + self.contact_number
        else:
            contact_number='no contact present'

        return contact_number

    def __str__(self):
        return self.email