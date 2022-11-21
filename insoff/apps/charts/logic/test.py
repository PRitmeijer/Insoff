import datetime


def find_weeks(start,end):
    l = []
    for i in range((end-start).days + 1):
        d = (start+datetime.timedelta(days=i)).isocalendar()[:2] # e.g. (2011, 52)
        yearweek = '{}{:02}'.format(*d) # e.g. "201152"
        l.append(yearweek)
    return sorted(set(l))

start = datetime.date(2011, 12, 25) 
end = datetime.date(2012, 1, 21)
print(find_weeks(start, end))
