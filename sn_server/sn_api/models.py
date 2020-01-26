from django.db import models
from django.contrib.auth.models import AbstractUser

def user_path(instance, filename):
    return f'media/users/{instance.id}/avatar.{filename.split(".")[-1]}'

class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True) # use e-mail as login?
    password = models.CharField(max_length=100) # TODO Encrypt this!
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    info = models.CharField(max_length=1500, blank=True)
    avatar = models.FileField(upload_to=user_path, blank=True)
    friends = models.ManyToManyField('self', blank=True, related_name='friends')
    groups = models.ManyToManyField('Group', related_name='members', blank=True)

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    avatar = models.FileField(upload_to='media/img', blank=True)
    administrator = models.ForeignKey('User', on_delete=models.CASCADE)