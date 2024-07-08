from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class CustomManager(BaseUserManager):
    
    
    def create_user(self,username,email,password=None,**extra_fields):
        
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        if not password:
            raise ValueError('password is required')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields,username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None,**extra_fields):
        
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        return self.create_user(username=username,email=email,password=password,**extra_fields)
    

class BlogUsers(AbstractUser):
    
    email = models.EmailField(unique=True,blank=False)
    username=models.CharField(max_length=100,unique=True,blank=False)
    DOB = models.DateField(blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    profession = models.CharField(max_length=60,blank=True,null=True)
    objects = CustomManager()
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    
