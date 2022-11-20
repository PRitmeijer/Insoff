from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from unicodedata import decimal
from wsgiref.handlers import format_date_time
from charts.models import Asset, PriceInterval, Provider, PriceStat
from decimal import Decimal
from django.db import models

import kraken.api.public as kraken_api

# Create your views here.
def sync_kraken_assets(request):
    kraken_assets = Asset.objects.filter(provider=Provider.KRAKEN)
    epoch = datetime.timestamp(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(weeks=12))
    for asset in kraken_assets:
        data = kraken_api.get_ohlc_data(asset.api_name, 1440, epoch)[asset.api_name]
        for timestamp in data:
            date_t = datetime.fromtimestamp(timestamp[0])
            PriceStat.objects.update_or_create(
                asset=asset, date=date_t,
                defaults={
                    'date': date_t,
                    'asset':asset,
                    'interval':PriceInterval.DAY,
                    'open':Decimal(timestamp[1]),
                    'high':Decimal(timestamp[2]),
                    'low':Decimal(timestamp[3]),
                    'close':Decimal(timestamp[4]),
                    'vwap':Decimal(timestamp[5]),
                    'volume':Decimal(timestamp[6]),
                    'count':int(timestamp[7])
                },
            )
        
    
    return JsonResponse('success', safe=False)


# btcdata = kraken.get_ohlc_data(settings.PAIR, 1440, epoch)['XXBTZUSD']
# stat_day = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
# temp = [0, 0.0]
# for tick in btcdata:
#     day = datetime.fromtimestamp(tick[0])
#     number = int(day.strftime('%w'))
#     average = Decimal(tick[4])
#     if average > temp[1]:
#         temp = [number, average]
#     if number == 6:
#         stat_day[temp[0]] += 1
#         temp = [0,0.0]

# print(stat_day)