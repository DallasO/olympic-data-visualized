from django.core.management.base import BaseCommand, CommandError
# from django.db import DoesNotExist
import csv, sys, os

from django.conf import settings

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from visualData.models import *

class Command(BaseCommand):
    """Import data"""
    def handle(self, *args, **options):
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Process noc_regions.csv
        # BUG: Try to make os.path.join work?
        # with open(os.path.join(BASE_DIR,'visualData/data/noc_regions.csv')) as csvfile:
        with open('visualData/data/noc_regions.csv') as csvfile:
            regionreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            titlerow = next(regionreader)
            for row in regionreader:
                try:
                    currentRegion = Regions.objects.get(country_code= row[0])
                except Regions.DoesNotExist as e:
                    print('DoesNotExist')
                    # regionImport = Regions.objects.create(country_code= row[0],region= row[1],notes= row[2])
                else:
                    print('DoesExist')
                    # print(currentRegion)
                    # regionImport.save() # Save changes to the DB



        # Process athlete_events.csv
        # with open('visualData/data/athlete_events.csv') as csvfile:
        #     regionreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        #     titlerow = next(regionreader)
        #     for row in regionreader:
        #         print(', '.join(row))
