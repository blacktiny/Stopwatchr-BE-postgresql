# Generated by Django 3.2.3 on 2021-05-24 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatchr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(default='', max_length=70),
        ),
    ]
