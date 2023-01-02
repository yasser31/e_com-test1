from django.db import models
from io import BytesIO
from PIL import Image as Img
from django.core.files import File


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


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    variations = models.ManyToManyField(VariationOption)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductVariation(models.Model):

    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ManyToManyField(VariationOption, blank=True)
    value = models.ManyToManyField(VariationValue, blank=True)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="product_images", null=True, blank=True)
    variant = models.ForeignKey(
        ProductVariation, on_delete=models.DO_NOTHING, related_name="variant_images", null=True, blank=True)
    image = models.ImageField(
        upload_to='img', null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails', null=True, blank=True)

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

    def make_thumbnail(self, image, size=(300, 200)):
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
