# Generated by Django 3.0.7 on 2020-06-15 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200614_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trans',
            name='trans_id',
            field=models.CharField(max_length=50, verbose_name='Transaction ID'),
        ),
    ]
