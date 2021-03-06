# Generated by Django 3.0.7 on 2020-06-14 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_user_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='users.Vendor'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
