# Generated by Django 4.1.4 on 2023-01-02 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_image_image_alter_image_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails'),
        ),
    ]
