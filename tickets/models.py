from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
#to create signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    hall = models.CharField(max_length=12)
    movie = models.CharField(max_length=30)
    def __str__(self):
        return self.movie

class Guest(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=13)

    def __str__(self):
        return f'{self.name}'

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservation')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reservation')
    def __str__(self):
        return f'{self.guest} & {self.movie}'

#If you want every user to have an automatically generated Token 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
# #If you've already created some users, you can generate tokens for all existing users like this:
# from django.contrib.auth.models import User

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)