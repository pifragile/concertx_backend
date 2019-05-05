# Generated by Django 2.2.1 on 2019-05-05 14:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('concertx_backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='canceled_by',
            field=models.ManyToManyField(blank=True, related_name='concert_canceled_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
