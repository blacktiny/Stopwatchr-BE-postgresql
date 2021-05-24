from django.db import models


class users(models.Model):
    username = models.CharField(max_length=200, blank=False, default='')
    useremail = models.CharField(max_length=200, blank=False, default='')
    password = models.CharField(max_length=70, blank=False, default='')
