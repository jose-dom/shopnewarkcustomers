# Generated by Django 3.0.7 on 2020-06-14 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20200614_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
