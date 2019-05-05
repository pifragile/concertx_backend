from django.db import models
from django.contrib.auth.models import User


class Concert(models.Model):
    location = models.CharField(max_length=60, blank=True)
    date = models.DateTimeField()
    confirmed = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='concert_owner')
    accepted_by = models.ManyToManyField(User, related_name='concert_accepted_by', blank=True)
    canceled_by = models.ManyToManyField(User, related_name='concert_canceled_by', blank=True)
