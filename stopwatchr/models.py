from django.db import models

class users(models.Model):
    DAILY = 'Daily'
    HOURLY = 'Hourly'
    NONE = 'None'
    DAILY_OPTIONS_CHOICES = [
        (DAILY, 'Daily'),
        (HOURLY, 'Hourly'),
        (NONE, 'None'),
    ]
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, blank=False, default='')
    useremail = models.CharField(max_length=200, blank=False, default='')
    password = models.CharField(max_length=70, blank=False, default='')
    alert_options = models.CharField(
        max_length=10,
        choices=DAILY_OPTIONS_CHOICES,
        default=DAILY,
    )

class stocks(models.Model):
    id = models.AutoField(primary_key=True)
    stockId = models.CharField(max_length=200, blank=False, default='')
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    type = models.CharField(max_length=70, blank=False, default='Manual')
    name = models.CharField(max_length=200, blank=True, default='')
    entry = models.FloatField(max_length=70, blank=True, default='')
    stop = models.FloatField(max_length=70, blank=True, default='')
    last_updated = models.DateTimeField(blank=True)

class alerts(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(stocks, on_delete=models.CASCADE)
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
    created = models.DateTimeField(blank=False)
