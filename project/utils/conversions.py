import datetime


def todate_time(date_):
    if date_ == None:
        return
    elif len(str(date_)) < 20:
        print('>{}'.format(date_))
        val = datetime.datetime(int(date_.split('-')[0]), int(date_.split('-')[1]),
                                int(date_.split('-')[2]))
        print(datetime.datetime.strftime(val, '%a, %d %b %Y %X %Z'))
        return datetime.datetime.strftime(val, '%a, %d %b %Y %X %Z')
    else:
        return datetime.datetime.strptime(date_, '%a, %d %b %Y %X %Z')


def to_date(str):
    # print('>{}'.format(datetime.date(str)))
    y, m, d = str.split('-')
    return datetime.datetime(int(y), int(m), int(d))
def with_utf(date_):
    return datetime.datetime.strptime(datetime.datetime.strftime(date_, '%a, %d %b %Y %X'), '%a, %d %b %Y %X')
