from django.forms.models import model_to_dict

def products_to_dict(products):
    filtered_products = []
    for product in products:
        product_images = []
        product_dict = model_to_dict(product)
        for image in product.product_images.all():
            image_dict = {}
            image_dict["url"] = image.image.url
            image_dict["default"] = image.default
            product_images.append(image_dict)
        product_dict["images"] = product_images
        filtered_products.append(product_dict)
    return filtered_products