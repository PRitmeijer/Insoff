from datetime import datetime, timedelta
from charts.models import *
from django.db.models import F


def same_week_as_current(date):
    '''returns true if a date is part of the current week'''
    d1 = date
    d2 = datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year  

def validate_date_range(start, end):
    if end > datetime.now():
        end = datetime.now().replace(hour=0, minute=0)
    
    if start > end - timedelta(weeks=1):
        start = end - timedelta(weeks=1)

    if start.weekday() != end.weekday():
        start = start.replace(hour=0, minute=0) - timedelta(days=(start.weekday() - end.weekday()))
    # if same_week_as_current(end):
    #     end = end - timedelta(weeks=1)
    # if same_week_as_current(start):
    #     start = start - timedelta(weeks=1)
    # startweekday = start.weekday()
    # if startweekday != 0:
    #     start = start - timedelta(days=startweekday)
    # if same_week_as_current(end):
    #     end = end - timedelta(weeks=1)
    # endweekday = end.weekday()
    # if end.weekday() != 0:
    #     end = end - timedelta(days=endweekday)
    return start, end


def find_week_starts(start,end):
    week_l = []
    weekly = start
    while weekly <= end:
        week_l.append(weekly)
        weekly += timedelta(days=7)
    return week_l

def get_week_labels(start):
    labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if start.weekday() == 0:
        return labels
    else:
        index = start.weekday() - 1
        return labels[index + 1:] + labels[:index + 1]

def  get_week_data(asset, from_date, to_date, pricedata):
    start, end = validate_date_range(from_date, to_date)
    all_stats = PriceStat.objects.filter(
            asset = asset,
            date__gte = start,
            date__lt = end,
            interval = 3
    )

    weeks = find_week_starts(start, end)

    labels = get_week_labels(start)
    data = []
    for index in range(len(weeks) -1):
        week_start, week_end = weeks[index], weeks[index+1]
        week_stats = all_stats.filter(
            date__gte = week_start,
            date__lt = week_end,
        ).order_by('date').values('date', value=F(f'{pricedata}'))
        data.append(list(week_stats))
    
    return start, end, labels, data