from django.contrib.gis.db import models

import datetime

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=50, unique=True, primary_key=True, db_index=True)

    objects = models.GeoManager()


PROGRESS_CHOICES = (
    ('running', 'running'),
    ('complete', 'Complete'),
    ('failed', 'Failed'),
)

class RenderBlock(models.Model):
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    identifier = models.CharField(max_length=20)
    state = models.CharField(max_length=20, choices=PROGRESS_CHOICES, blank=True, null=True)
    source = models.CharField(max_length=200)
    bounds = models.PolygonField(blank=True, null=True)
    dataset = models.ForeignKey(Dataset, related_name="blocks", db_index=True)

    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(RenderBlock, self).save(*args, **kwargs)
