from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    name = models.TextField()
    year = models.TextField()
    company = models.TextField()
    position = models.TextField()
    email = models.TextField()
    phone = models.TextField()


    def __str__(self):
        return self.name


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    year =  models.CharField(max_length=100)
    company =  models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length= 10)


    def __str__(self):
        return self.name

    def create_profile(sender, **kwargs ):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])
        post_save.connect(create_profile, sender=User)

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})
