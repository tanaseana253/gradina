# Ca sa rulezi scriptul de imagini, baga comanda in terminal
# python manage.py upload_photos store/management/commands/photos


import os

# de aici am inceput sa bag pt imagini
import sys

import django as django

sys.stdout.reconfigure(encoding='utf-8')
# pana aici pt imagini


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradinaCraciun.settings')
django.setup()

from django.core.management.base import BaseCommand
from store.models import Product
from django.core.files import File


class Command(BaseCommand):
    help = 'Upload images from a specified directory to the database'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Directory containing images to upload')

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']

        # Check if the directory exists
        if not os.path.exists(directory):
            self.stdout.write(self.style.ERROR('Directory does not exist'))
            return

        # Get all product objects
        products = Product.objects.all()

        # Iterate over files in the directory and products
        for product, filename in zip(products, os.listdir(directory)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'rb') as img_file:
                    # Update the product's image field
                    product.image = File(img_file, name=filename)
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated {product.name} with {filename}'))

        # Notify if there are more images than products
        if len(os.listdir(directory)) > products.count():
            self.stdout.write(self.style.WARNING('More images than products. Some images were not used.'))

        # Notify if there are more products than images
        if products.count() > len(os.listdir(directory)):
            self.stdout.write(self.style.WARNING('More products than images. Some products were not updated.'))
