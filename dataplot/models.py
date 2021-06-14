from django.db import models


class Asset(models.Model):
    asset = models.CharField(max_length=100, blank=False)


class Column(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    column = models.CharField(max_length=100, blank=True, default='')
