from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import random
from django.utils.translation import gettext_lazy as _

class AccountManagement(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            return ValueError(_("Please enter a valid email address"))
        
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            # self.email_validator(email)
        else:
            raise ValueError(_("An email address is required"))
        if not first_name:
            raise ValueError(_("First name is required"))
        if not last_name:
            raise ValueError(_("Last name is required"))

        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        # user.username = self.generate_username(first_name=first_name)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Is staff must be true for admin user"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Is Superuser must be true for admin user"))

        return self.create_user(email, first_name, last_name, password, **extra_fields)