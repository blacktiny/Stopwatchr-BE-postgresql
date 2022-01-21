from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class users(AbstractBaseUser):
    DAILY = 'Daily'
    HOURLY = 'Hourly'
    NONE = 'None'
    DAILY_OPTIONS_CHOICES = [
        (DAILY, 'Daily'),
        (HOURLY, 'Hourly'),
        (NONE, 'None'),
    ]

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('id', 'useremail', 'password',)

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, blank=False, default='', unique=True)
    useremail = models.CharField(max_length=200, blank=False, default='')
    password = models.CharField(max_length=70, blank=False, default='')
    last_login = models.DateTimeField(auto_now=True)
    alert_options = models.CharField(
        max_length=10,
        choices=DAILY_OPTIONS_CHOICES,
        default=DAILY,
    )
    # todo: add new fields for subscription

class stocks(models.Model):
    id = models.AutoField(primary_key=True)
    stockId = models.CharField(max_length=200, blank=False, default='')
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    type = models.CharField(max_length=70, blank=False, default='Manual')
    name = models.CharField(max_length=200, blank=True, default='')
    entry = models.FloatField(blank=False, default=0.00)
    stop = models.FloatField(blank=False, default=0)
    current = models.FloatField(blank=False, default=0.00)
    last_updated = models.DateTimeField(blank=False)

class alerts(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(stocks, on_delete=models.CASCADE)
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
    created = models.DateTimeField(blank=False)
