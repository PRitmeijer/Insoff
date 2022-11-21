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

from charts.logic.avarage.week import get_average_week

def get_average(asset, from_date, to_date, scope):
    if scope == 2:
        start, end, week_d = get_average_week(asset, from_date, to_date)
        data = {
            "start":start,
            "end":end,
            "results": [
                {
                    "date":d,
                    "amount":week_d[d]
                } for d in week_d
            ]
        }
        return data
    

def best_date(stats):
    return

