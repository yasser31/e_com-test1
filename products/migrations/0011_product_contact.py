# Generated by Django 4.1.4 on 2023-01-13 14:45

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_user_productvariation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='contact',
            field=phonenumber_field.modelfields.PhoneNumberField(default=0, max_length=128, region=None),
        ),
    ]
