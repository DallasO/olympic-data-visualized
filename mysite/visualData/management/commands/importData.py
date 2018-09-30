# --------------------------------------------------------------------------- #
# This file can be run as a script using the command  #
# ::  $ python3 /path/to/app/manage.py importData  :: #
# --------------------------------------------------------------------------- #

from django.core.management.base import BaseCommand, CommandError
import csv, sys, os

from django.conf import settings

# BUG: Do I need this?
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from visualData.models import *

class Command(BaseCommand):
    """Import data"""
    help = "Imports new data into the database"

    # Allow importing one file at a time with command line argument
    # FIXME: Add ability to specify each file as well, in case they are not in default location
    def add_arguments(self, parser):
        parser.add_argument(
            '--regions',
            action='store_true', # make flag
            dest='regions', # set options[] value
            help='Import only the regions csv',
        )
        parser.add_argument(
            '--events',
            action='store_true',
            dest='events',
            help='Import only the events csv',
        )

    def handle(self, *args, **options):
        delim = ','
        quote = '"'

        importAll = not(options['regions'] or options['events'])

        # Process noc_regions.csv
        if importAll or options['regions']:
            noc_regions = os.path.join(settings.BASE_DIR,'visualData/data/noc_regions.csv')
            try:

                with open(noc_regions) as csvfile:
                    regionReader = csv.reader(csvfile, delimiter=delim, quotechar=quote)
                    titlerow = next(regionReader)

                    for row in regionReader:

                        try:
                            currentRegion = Regions.objects.filter(country_code= row[0])
                        except Regions.DoesNotExist as e:
                            regionImport = Regions.objects.create(country_code= row[0],region= row[1],notes= row[2])
                        else:

                            if (
                                currentRegion.values()[0]['region'] != row[1] or
                                currentRegion.values()[0]['notes'] != row[2]
                                ):
                                currentRegion.update(region= row[1], notes= row[2])

            except FileNotFoundError as e:
                print(f"File not found: {noc_regions}")



        # Process athlete_events.csv
        # if importAll or options['events']:
        #     athlete_events = os.path.join(settings.BASE_DIR,'visualData/data/athlete_events.csv')
        #     try:
        #
        #         with open(athlete_events) as csvfile:
        #             eventReader = csv.reader(csvfile, delimiter=delim, quotechar=quote)
        #             titlerow = next(eventReader)
        #
        #             for row in eventReader:
        #
        #                 try:
        #                     currentEvent = Regions.objects.filter(country_code= row[0])
        #                 except Regions.DoesNotExist as e:
        #                     regionImport = Regions.objects.create(country_code= row[0],region= row[1],notes= row[2])
        #                 else:
        #
        #                     if (
        #                         currentEvent.values()[0]['region'] != row[1] or
        #                         currentEvent.values()[0]['notes'] != row[2]
        #                         ):
        #                         currentEvent.update(region= row[1], notes= row[2])
        #
        #     except FileNotFoundError as e:
        #         print(f"File not found: {athlete_events}")
