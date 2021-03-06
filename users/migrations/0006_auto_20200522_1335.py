# Generated by Django 3.0.3 on 2020-05-22 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200521_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(default='', help_text='Ex: 123 Broad St, Newark, NJ, 07102', max_length=3000, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(help_text='Contact Phone Number', max_length=12, verbose_name='Phone Number'),
        ),
    ]
