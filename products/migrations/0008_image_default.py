# Generated by Django 4.1.4 on 2023-01-03 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_image_product_alter_image_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
