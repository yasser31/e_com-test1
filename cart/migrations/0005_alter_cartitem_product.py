# Generated by Django 4.1.4 on 2023-01-01 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_image'),
        ('cart', '0004_cartitem_product_alter_cartitem_product_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.product'),
        ),
    ]
