from tabnanny import check
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from charts.models import *
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
import calendar
import statistics
from itertools import chain

from charts.logic.week import get_week_data

def get_bsdex(asset, from_date, to_date, scope, pricedata):
    pricedata = transform_pricedata(pricedata)
    if scope == 2:
        start, end, labels, data_dict = get_week_data(asset, from_date, to_date, pricedata)
        bsdex_dict = create_bsdex_json(labels, data_dict)
        L = list(chain(*data_dict))
        raw_data = dict()
        for _dict in L:
            raw_data[_dict['date']] = _dict['value']
        data = {
            "start":start,
            "end":end,
            "results": [
                {
                    "date":key,
                    "amount":value
                } for key, value in bsdex_dict.items()
            ],
            "raw_data": [
                {
                    "date":key,
                    "amount":value
                } for key, value in raw_data.items()
            ]
        }
        return data
    
def create_bsdex_json(labels, data_dict):
    bsdex_dict = {}
    for datalist in data_dict:
        average = float(sum(d['value'] for d in datalist)) / len(datalist)
        for index, data in enumerate(datalist):
            bsdex = float(data['value']) / average
            if index not in bsdex_dict:
                bsdex_dict[index] = bsdex
            else:
                bsdex_dict[index] += bsdex
    for index in range(len(data_dict[0])):
        bsdex_dict[labels[index]] = bsdex_dict.pop(index)
    result = {key: value / len(data_dict) for key, value in bsdex_dict.items()}
    return result

def best_date(stats):
    return

def transform_pricedata(pricedata):
    return 'low' if pricedata == 'L' else 'high' if pricedata == 'H' else 'vwap'