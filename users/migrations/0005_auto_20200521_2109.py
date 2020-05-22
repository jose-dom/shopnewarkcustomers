# Generated by Django 3.0.3 on 2020-05-22 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics', verbose_name='Profile Image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(default='', help_text='Ex: 123 Broad St, Newark, NJ, 07102', max_length=3000, verbose_name='<strong>Address</strong>&nbsp;'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='<strong>First Name</strong>&nbsp;'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='<strong>Last Name</strong>&nbsp;'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(help_text='Contact Phone Number', max_length=12, verbose_name='<strong>Phone Number</strong>&nbsp;'),
        ),
    ]