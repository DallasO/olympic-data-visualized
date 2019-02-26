from django.db import models

class Sources(models.Model):
    title             = models.CharField(max_length=120)
    url               = models.URLField()
    last_updated_date = models.DateTimeField()

    def __str__(self):
        return self.title



class Regions(models.Model):
    country_code = models.CharField(primary_key=True, max_length=3)
    region       = models.CharField(max_length=120)
    notes        = models.TextField(null=True)

    def __str__(self):
        return self.region



class Sports(models.Model):
    event = models.CharField(max_length=400, primary_key=True)
    sport = models.CharField(max_length=200)

    def __str__(self):
        return self.event



class Games(models.Model):
    year     = models.CharField(max_length=4)
    season   = models.CharField(max_length=6)
    city     = models.CharField(max_length=120)

    class Meta:
        unique_together = ('year', 'season', 'city')
        # BUG: Will have to update for 2.2
        # constraints = [
        #     models.UniqueConstraint(fields=['year', 'season', 'city'], name='unique_games'),
        # ]

    def __str__(self):
        return f"{self.year} {self.season}"



class Athletes(models.Model):
    id     = models.PositiveSmallIntegerField(primary_key=True)
    name   = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, default='X')
    sport  = models.ManyToManyField(Sports, through='Athlete_Event')
    game   = models.ManyToManyField(Games, through='Athlete_Event')

    def __str__(self):
        return self.name



class Athlete_Event(models.Model):
    athlete = models.ForeignKey(Athletes, on_delete=models.CASCADE)
    sport   = models.ForeignKey(Sports, on_delete=models.CASCADE)
    game    = models.ForeignKey(Games, on_delete=models.CASCADE)
    age     = models.PositiveSmallIntegerField(null=True)
    height  = models.FloatField(null=True)
    weight  = models.FloatField(null=True)
    team    = models.ForeignKey(Regions, max_length=120, null=True, on_delete=models.CASCADE)
    medal   = models.CharField(max_length=6, null=True)

    def __str__(self):
        return f"{self.athlete.name} - {self.sport.event}"
