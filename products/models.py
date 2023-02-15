from django.db import models
from io import BytesIO
from PIL import Image as Img
from django.core.files import File
from django.contrib.auth.models import User
from django.utils import timezone



class VariationOption(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class VariationValue(models.Model):
    option = models.ForeignKey(VariationOption, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    dependency = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        'Product', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.value


class Category(models.Model):
    name = models.CharField('Nom', max_length=100, default="")
    parent = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, related_name="childs", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_products", null=True, blank=True)
    name = models.CharField('Nom', max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="products", null=True, blank=True)
    description = models.TextField('Description')
    variations = models.ManyToManyField(VariationOption, null=True, blank=True)
    price = models.DecimalField('Prix',
        max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    contact = models.CharField('Contact', default="ND", max_length=100)
    created_date = models.DateTimeField('date created', default=timezone.now, null=True, blank=True)

    
    def __str__(self):
        return self.name


class ProductVariation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_variants", null=True, blank=True)
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    option = models.ManyToManyField(VariationOption, blank=True)
    value = models.ManyToManyField(VariationValue, blank=True)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images", null=True, blank=True)
    variant = models.ForeignKey(
        ProductVariation, on_delete=models.DO_NOTHING, related_name="variant_images", null=True, blank=True)
    image = models.ImageField(
        upload_to='img', null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails', null=True, blank=True)
    default = models.BooleanField('Image pricipale', default=False)

    def get_image(self):
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return "http://127.0.0.1:8000" + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return "http://127.0.0.1:8000" + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(225, 225)):
        img = Img.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def save(self):
        thumbnail = self.make_thumbnail(self.image)
        self.thumbnail = thumbnail
        super().save()
