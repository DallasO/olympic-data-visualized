import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import mysite.visualData.models

# Process noc_regions.csv
with open(os.path.join(BASE_DIR,'visualData/data/noc_regions.csv')) as csvfile:
    regionreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    titlerow = next(regionreader)
    for row in regionreader:
        print(', '.join(row))






# Process athlete_events.csv
