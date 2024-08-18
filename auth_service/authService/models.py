from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from .manager import AccountManagement
import random


# Create your models here.
class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True,max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, blank=True, unique=True)
    phone_number = models.CharField(max_length=30, unique=True)
    country = models.CharField(max_length=10, default="NG")
    pin = models.CharField(blank=True, default="", max_length=256)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['first_name', 'last_name', 'phone_number']
    
    objects = AccountManagement()
    
    
    
    @property
    def fullname(self):
        return self.first_name + " " + self.last_name
    
    def __str__(self):
        return self.username
    def generate_username(self):
        
        username = self.first_name + str(random.randint(5, 10000))
        
        if Account.objects.filter(username=username).exists():
            return self.generate_username()
        return username
    def save(self, *args, **kwargs) -> None:
        if not self.username:
            self.username = self.generate_username()
        return super().save(*args, **kwargs)
    