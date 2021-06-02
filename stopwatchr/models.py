from django.db import models


class users(models.Model):
    username = models.CharField(max_length=200, blank=False, default='')
    useremail = models.CharField(max_length=200, blank=False, default='')
    password = models.CharField(max_length=70, blank=False, default='')

class stocks(models.Model):
    stockId = models.CharField(max_length=200, blank=False, default='')
    userId = models.ForeignKey(users, on_delete=models.CASCADE)
    type = models.CharField(max_length=70, blank=False, default='Manual')
    name = models.CharField(max_length=200, blank=True, default='')
    entry = models.FloatField(max_length=70, blank=True, default='')
    stop = models.FloatField(max_length=70, blank=True, default='')
