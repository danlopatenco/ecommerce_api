from django.core.management.base import BaseCommand
from core.models import Product


class Command(BaseCommand):
    help = 'Loads a list of test products into the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to generate test products...'))

        for i in range(1, 21):
            product = Product(name=f'Test Product {i}', price=i * 10, description=f'This is test product {i}')
            product.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated test products. - 20'))
