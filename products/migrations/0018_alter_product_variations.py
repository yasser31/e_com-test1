# Generated by Django 4.1.4 on 2023-01-31 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_productvariation_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='variations',
            field=models.ManyToManyField(blank=True, null=True, to='products.variationoption'),
        ),
    ]
