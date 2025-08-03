from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        titles = ['Cozy Cottage', 'Beach House', 'Mountain Cabin', 'Urban Apartment', 'Luxury Villa']
        locations = ['Addis Ababa', 'Bahir Dar', 'Lalibela', 'Hawassa', 'Gondar']

        for i in range(10):
            Listing.objects.create(
                title=random.choice(titles),
                description="This is a sample listing description.",
                price_per_night=random.uniform(50, 300),
                location=random.choice(locations),
            )

        self.stdout.write(self.style.SUCCESS('✅ Seeded the database with sample listings!'))
