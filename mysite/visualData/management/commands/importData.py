# --------------------------------------------------------------------------- #
# This file can be run as a script using the command  #
# ::  $ python3 /path/to/app/manage.py importData  :: #
# --------------------------------------------------------------------------- #

import csv, sys, os
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.conf import settings
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
                            currentRegion, created = Regions.objects.update_or_create(country_code= row[0],region= row[1],notes= row[2])
                            # currentRegion.save()
                        except IntegrityError:
                            print("Region:", currentRegion)

            except FileNotFoundError:
                print(f"File not found: {noc_regions}")



        # Process athlete_events.csv
        if importAll or options['events']:
            athlete_events = os.path.join(settings.BASE_DIR,'visualData/data/athlete_events.csv')
            try:
                athleteTest = None

                with open(athlete_events) as csvfile:
                    eventReader = csv.reader(csvfile, delimiter=delim, quotechar=quote)
                    titlerow = next(eventReader)

                    for row in eventReader:

                        row = dict(zip(titlerow,row))

                        # Clean up NA values
                        if row['Age'] == 'NA':
                            row['Age'] = 0

                        if row['Height'] == 'NA':
                            row['Height'] = 0

                        if row['Weight'] == 'NA':
                            row['Weight'] = 0

                        if row['Medal'] == 'NA':
                            row['Medal'] = None
                        # Clean up NA values

                        goodData = True

                        # Athletes
                        athleteID     = row['ID']
                        athleteName   = row['Name']
                        athleteGender = row['Sex']

                        try:
                            athlete, created = Athletes.objects.get_or_create(id= athleteID, name= athleteName, gender= athleteGender)
                            # if not created:
                            #     athlete.id = athleteID
                            #     athlete.save()
                        except IntegrityError:
                            print("Name:", athleteName)
                            goodData = False

                        # Games
                        gamesYear   = row['Year']
                        gamesSeason = row['Season']
                        gamesCity   = row['City']

                        try:
                            games, created = Games.objects.get_or_create(year= gamesYear, season= gamesSeason, city= gamesCity)
                            # games.save()
                        except IntegrityError:
                            print("year", gamesYear)
                            print("season", gamesSeason)
                            goodData = False

                        # Sports
                        sportSport = row['Sport']
                        sportEvent = row['Event']

                        try:
                            sport, created = Sports.objects.get_or_create(sport= sportSport, event= sportEvent)
                            # sport.save()
                        except IntegrityError:
                            print("sport", sportSport)
                            print("event", sportEvent)
                            goodData = False

                        # Athlete_Event
                        aeAge    = row['Age']
                        aeHeight = row['Height']
                        aeWeight = row['Weight']
                        aeMedal  = row['Medal']

                        try:
                            region = Regions.objects.get(country_code=row['NOC'])
                        except Regions.DoesNotExist:
                            print("NOC", row['NOC'])
                            print("Team", row['Team'])
                            goodData = False

                        if goodData:
                            # Shoud this be get_or_create()?
                            ae, created = Athlete_Event.objects.update_or_create(athlete= athlete, sport= sport, game= games, age= aeAge, height= aeHeight, weight= aeWeight, team= region, medal= aeMedal)
                            # ae.save()

            except FileNotFoundError:
                print(f"File not found: {athlete_events}")
