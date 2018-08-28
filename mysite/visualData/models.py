from django.db import models

# Create your models here.
class Sources(models.Model):
    title             = models.CharField(max_length=120)
    url               = models.URLField()
    last_updated_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Regions(models.Model):
    country_code = models.CharField(unique=True, max_length=3)
    region       = models.CharField(max_length=120)
    notes        = models.TextField()

    def __str__(self):
        return self.region


class Games(models.Model):
    year   = models.CharField(max_length=4)
    season = models.CharField(max_length=6)
    city   = models.CharField(max_length=120)

    def __str__(self):
        return "%s %s" % (self.year, self.season)


class Athletes(models.Model):
    region = models.CharField(max_length=120)
    name   = models.CharField(max_length=200)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return self.name


class Sports(models.Model):
    sport = models.CharField(max_length=200)
    event = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Athlete_Event(models.Model):
    athlete = models.ForeignKey(Athletes, on_delete=models.CASCADE)
    sport   = models.ForeignKey(Sports, on_delete=models.CASCADE)
    age     = models.SmallIntegerField()
    height  = models.SmallIntegerField()
    weight  = models.SmallIntegerField()
    team    = models.CharField(max_length=200)
    region  = models.ForeignKey(Regions, on_delete=models.CASCADE)
    game    = models.ForeignKey(Games, on_delete=models.CASCADE)
    sport   = models.ForeignKey(Sports, on_delete=models.CASCADE)
    medal   = models.CharField(max_length=6)

    def __str__(self):
        return self.name
