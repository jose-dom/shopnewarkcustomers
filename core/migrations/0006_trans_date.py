# Generated by Django 3.0.7 on 2020-06-15 00:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200614_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='trans',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
