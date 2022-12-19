from asyncio.windows_events import NULL
from dateutil import rrule
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from assets.models import *
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
import calendar
import statistics
from itertools import chain
from django.db.models import F

from charts.logic.transform import transform_pricedata


def get_investmentgraph(asset, from_date, to_date, purchase_amount, interval, pricedata):
    pricedata = transform_pricedata(pricedata)
    raw_data = get_raw_data(asset, from_date, to_date, interval, pricedata)
    data = get_investment_data(raw_data, purchase_amount)
    data = {
            "start":from_date,
            "end":to_date,
            "results": [
                {
                    "date":instance['date'],
                    "amount":round(instance['portfolio_value'], 3)
                } for instance in data
            ],
            "raw_data": [
                {
                    "date":instance['date'],
                    "amount":round(instance['value'], 3)
                } for instance in data
            ]
        }
    return data

#def get_
def get_investment_data(raw_data, purchase_amount):
    accumulated_amount = 0
    for instance in raw_data:
        value = instance['value']
        amount = purchase_amount / value
        portfolio_value = (amount + accumulated_amount) * value
        instance['portfolio_value'] = portfolio_value
        accumulated_amount += amount
    return raw_data


def get_raw_data(asset, from_date, to_date, interval, pricedata):
    date_array = get_interval_data(from_date, to_date, interval)
    data = []
    for date in date_array:
        stat = PriceStat.objects.filter(
            asset = asset,
            date = date.date(),
            interval = 3
        ).values('date', value=F(f'{pricedata}')).first()
        data.append(stat)

    return data

def get_interval_data(from_date, to_date, interval):
    match interval:
        #Daily
        case 0:
            return list(rrule.rrule(rrule.DAILY, dtstart=from_date, until=to_date))
        #Weekly    
        case 1:
            return list(rrule.rrule(rrule.WEEKLY, dtstart=from_date, until=to_date))
        #Bi-weekly    TODO
        case 2:
            return list(rrule.rrule(rrule.WEEKLY, dtstart=from_date, until=to_date))
        #Montly    
        case 3:
            return list(rrule.rrule(rrule.MONTHLY, dtstart=from_date, until=to_date))
        #Error
        case _:
            return NULL