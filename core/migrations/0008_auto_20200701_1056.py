# Generated by Django 3.0.7 on 2020-07-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200618_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trans',
            name='sale_type',
            field=models.CharField(choices=[('Sale', 'Sale'), ('Return', 'Return'), ('Other', 'Other')], default='Sale', max_length=7),
        ),
    ]