# Generated by Django 4.2.5 on 2025-01-25 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_save_info_paymentinfo_payment_save_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingaddress',
            old_name='save_info',
            new_name='is_saved_billing_address_info',
        ),
        migrations.RenameField(
            model_name='paymentinfo',
            old_name='payment_save_info',
            new_name='is_saved_payment_info',
        ),
    ]
