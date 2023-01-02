# Generated by Django 4.1.4 on 2023-01-02 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/img'),
        ),
        migrations.AlterField(
            model_name='image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_images', to='products.product'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='media/thumbnails'),
        ),
        migrations.AlterField(
            model_name='image',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='variant_images', to='products.productvariation'),
        ),
    ]
