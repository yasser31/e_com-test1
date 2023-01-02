# Generated by Django 4.1.4 on 2023-01-02 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/static/products/img')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='products/thumbnails/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.productvariation')),
            ],
        ),
    ]
