from django.http import JsonResponse
from datetime import datetime, timedelta
from charts.models import *

def same_week_as_current(date):
    '''returns true if a date is part of the current week'''
    d1 = date
    d2 = datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year  

def validate_date_range(start, end):
    if same_week_as_current(start):
        start = start - timedelta(weeks=1)
    if start.weekday() != 0:
        start = start - timedelta(days=start.weekday())
    if same_week_as_current(end):
        end = end - timedelta(weeks=1)
    if end.weekday() != 0:
        end = end - timedelta(days=end.weekday())
    return start, end


def find_week_starts(start,end):
    week_l = []
    weekly = start
    while weekly <= end:
        week_l.append(weekly)
        weekly += timedelta(days=7)
    return week_l

def get_average_week(asset, from_date, to_date):
    start, end = validate_date_range(from_date, to_date)
    weeks = find_week_starts(start, end)
    week_d = {'Monday':0, 'Tuesday':0, 'Wednesday':0, 'Thursday':0, 'Friday':0, 'Saturday':0, 'Sunday':0}
    all_stats = PriceStat.objects.filter(
            asset = asset,
            date__gte = from_date,
            date__lte = to_date,
            interval = 3
    )
    for index in range(len(weeks) -1):
        week1, week2 = weeks[index], weeks[index+1]
        lowest_day_average = all_stats.filter(
            date__gte = weeks[index],
            date__lte = weeks[index+1],
        ).order_by('vwap').first()
        if lowest_day_average:
            day = lowest_day_average.date.strftime("%A")
            if day not in week_d:
                week_d[day] = 1
            else:
                week_d[day] += 1
    
    return start, end, week_d