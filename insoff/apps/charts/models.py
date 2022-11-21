from tkinter import CASCADE
from django.db import models

# Create your models here.
# CHOICES
class Provider(models.IntegerChoices):
        KRAKEN = 0, 'KRAKEN'

class PriceInterval(models.IntegerChoices):
        YEAR = 0, 'YEAR'
        MONTH = 1, 'MONTH'
        WEEK = 2, 'WEEK'
        DAY = 3, 'DAY'


class Asset(models.Model):
        name = models.CharField(max_length=50, unique=True)
        ticker_name = models.CharField(max_length=10, unique=True)
        symbol = models.CharField(max_length=10)
        symbol_unicode = models.CharField(max_length=10)
        api_name = models.CharField(max_length=30, unique=True)
        provider = models.IntegerField(default=Provider.KRAKEN, choices=Provider.choices)


class PriceStat(models.Model):   
    date = models.DateField()
    interval = models.IntegerField(default=PriceInterval.DAY, choices=PriceInterval.choices)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    open = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True)
    high = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True)
    low = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True)
    close = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True)
    vwap = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True)
    volume = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True) #Number of trades

    