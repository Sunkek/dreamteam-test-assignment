from django.db import models
from django.contrib.auth.models import AbstractUser

def user_path(instance, filename):
    """Dynamically create path to the user avatar i.e.
    `media/users/123/avatar.PNG`
    """
    return f'media/users/{instance.id}/avatar.{filename.split(".")[-1]}'

def group_path(instance, filename):
    """Dynamically create path to the group avatar"""
    return f'media/groups/{instance.id}/avatar.{filename.split(".")[-1]}'

class User(AbstractUser):
    """User model with all the fields we need, inherited from 
    the Django AbstractUser for easier auth
    """
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    info = models.CharField(max_length=1500, blank=True)
    avatar = models.FileField(upload_to=user_path, blank=True)
    # Friends and groups are foreign key fields with many-to-many relations
    friends = models.ManyToManyField('self', blank=True, related_name='friends')
    # We can access group members by calling `group.members`
    groups = models.ManyToManyField(
        'Group', 
        related_name='members', 
        blank=True,
        on_delete=models.CASCADE
    )

class Group(models.Model):
    """Group model with all the requred fields"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    avatar = models.FileField(upload_to=group_path, blank=True)
    # If admin was deleted - the group dies too
    administrator = models.ForeignKey('User', on_delete=models.CASCADE)