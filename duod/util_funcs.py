from datetime import datetime

from app.main.models import Votes

def percent_up():
    if Votes.query.count():
        return int((Votes.query.filter_by(vote='up').count() / Votes.query.count()) * 100)
    return 0

def vote_count(vote_type):
    return int(Votes.query.filter_by(vote=vote_type).count())

def market_closed(cur_time):
    if (cur_time.weekday() < 5 and
                ((cur_time.hour == 14 and cur_time.minute >= 30)
                or
                (cur_time.hour > 14 and cur_time.hour < 21))):
       return False
    return True
