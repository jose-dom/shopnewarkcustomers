# Generated by Django 3.0.7 on 2020-06-14 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('1', 'customer'), ('2', 'vendor')], default='', max_length=1000, verbose_name='ROLE'),
        ),
    ]
