from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from ...models import User, Organization



class Command(BaseCommand):
    help = 'Creating Superuser'

    def handle(self, *args, **kwargs):
        organization_name = input("Name of the organization: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        
        org = Organization.objects.create(
            name=organization_name
        )
        User.objects.create(
            email=email,
            password=make_password(password),
            org = org,
            is_staff = True,
            is_superuser= True,
            is_active= True,
        )

        print(f'user is created. UserName/Email: {email} , password: {password}')