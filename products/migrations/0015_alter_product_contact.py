# Generated by Django 4.1.4 on 2023-01-15 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='contact',
            field=models.CharField(default='Non disponible', max_length=100),
        ),
    ]
