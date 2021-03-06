# Generated by Django 2.2.1 on 2019-05-01 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=60)),
                ('date', models.DateTimeField()),
                ('confirmed', models.BooleanField()),
                ('accepted_by', models.ManyToManyField(blank=True, related_name='concert_accepted_by', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concert_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
