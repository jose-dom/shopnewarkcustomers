# Generated by Django 3.0.7 on 2020-06-15 04:41

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20200614_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='approved',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3, verbose_name='Application Approved'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='banner',
            field=models.CharField(choices=[('Please create my banners. I understand there is a cost of $25', 'Please create my banners. I understand there is a cost of $25'), ('No, thank you. I will email you my banners (No Cost). If I do not email you my banners within 5 business days, I authorize you to create the banners for us at the above cost of $25 for both banners.', 'No, thank you. I will email you my banners (No Cost). If I do not email you my banners within 5 business days, I authorize you to create the banners for us at the above cost of $25 for both banners.')], max_length=1000, verbose_name='Options'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='business_structure',
            field=models.CharField(choices=[('Sole Proprietorship', 'Sole Proprietorship'), ('Limited Liability Corporation', 'Limited Liability Corporation'), ('S Corp', 'S Corp'), ('Other', 'Other')], max_length=1000, verbose_name='Business Structure'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='location_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Physical Location', 'Physical Location'), ('Home-based', 'Home-based'), ('Online', 'Online')], max_length=35, verbose_name='Does your business have a physical location? (Check all that apply)'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='rate',
            field=models.CharField(choices=[('Cost to me: 10%, Net Reward to Customer: 7.0%', 'Cost to me: 10%, Net Reward to Customer: 7.0%'), ('Cost to me: 14.3%, Net Reward to Customer: 10%', 'Cost to me: 14.3%, Net Reward to Customer: 10%'), ('Cost to me: 17.1%, Net Reward to Customer: 12%', 'Cost to me: 17.1%, Net Reward to Customer: 12%'), ('Other', 'Other')], default='', max_length=50, verbose_name='Percentage'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='special_business',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Minority Owned', 'Minority Owned'), ('Woman Owned', 'Woman Owned'), ('MWBE Certified', 'MWBE Certified'), ('DBE Certified', 'DBE Certified'), ('VOSBE Certified', 'VOSBE Certified'), ('None', 'None')], max_length=76, verbose_name='Is your business: (Check all that apply)'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='tax_credits',
            field=models.CharField(choices=[('On line, manually (Free)', 'On line, manually (Free)'), ('Downloading the application onto my own Android (Free)', 'Downloading the application onto my own Android (Free)'), ('Fincredit’s Dedicated Device and Stand ($90)', 'Fincredit’s Dedicated Device and Stand ($90)')], max_length=1000, verbose_name='Tax Credits'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='terms_conditions',
            field=models.CharField(choices=[('Agree', 'Agree'), ('Disagree', 'Disagree')], default='Agree', max_length=8, verbose_name='Terms & Coniditons'),
        ),
    ]
