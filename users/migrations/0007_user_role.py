# Generated by Django 3.0.7 on 2020-06-14 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200522_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('1', 'customer'), ('2', 'vendor')], default='1', max_length=1000, verbose_name='ROLE'),
        ),
    ]
