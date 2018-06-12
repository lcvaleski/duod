from __future__ import division
from flask import Flask, render_template, make_response, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_bootstrap import Bootstrap
import os

################################################################################################################################################################
################################################################################################################################################################

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

################################################################################################################################################################
################################################################################################################################################################

class Votes(db.Model):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    vote = Column(String)

    def __init__(self, vote=None):
        self.vote = vote

    def __repr__(self):
        return '<Vote %s>' % (self.vote)

################################################################################################################################################################
################################################################################################################################################################

@app.route('/') # HOME
def home():

    if 'vote' in request.cookies: #if the user has voted, return poll html
        percent_up = int((Votes.query.filter_by(vote='up').count() / Votes.query.count()) * 100)
        response = make_response( render_template('poll.html', percent_up=percent_up, vote=request.cookies.get('vote')))
        return response

    return render_template ('home.html') # if the above if does not run, render home

def weekday(day):
    if day.weekday < 5:
       return False
    return True


def market_closed(cur_time):
    if (cur_time.weekday() < 5 and
                ((cur_time.hour == 14 and cur_time.minute >= 30)
                or
                (cur_time.hour > 14 and cur_time.hour < 21))):
       return False
    return True

def test_market_closed():

    err_message = "ERROR: market_closed not working - "
    tests_passed = True

    # test some known open and closed time windows
    closed_time_1 = datetime.strptime("12/06/18 14:05", "%d/%m/%y %H:%M")
    open_time_1 = datetime.strptime("12/06/18 14:35", "%d/%m/%y %H:%M")
    closed_time_2 = datetime.strptime("12/06/18 23:05", "%d/%m/%y %H:%M")
    open_time_2 = datetime.strptime("12/06/18 18:00", "%d/%m/%y %H:%M")
    closed_weekend = datetime.strptime("17/06/18 18:00", "%d/%m/%y %H:%M")

    if not market_closed(closed_time_1):
        tests_passed = False
        print err_message + "closed_time_1"

    if market_closed(open_time_1):
        tests_passed = False
        print err_message + "open_time_1"

    if not market_closed(closed_time_2):
        tests_passed = False
        print err_message + "closed_time_2"

    if market_closed(open_time_2):
        tests_passed = False
        print err_message + "open_time_2"

    if not market_closed(closed_weekend):
        tests_passed = False
        print err_message + "closed_weekend"

    if tests_passed:
        print "market_closed() works! all tests_passed"

    return

@app.route('/poll/<vote>') # VOTE
def handle_vote(vote):

    if not 'vote' in request.cookies: # if the user has not voted, add their vote
        if market_closed(datetime.utcnow()) and weekday(): # market is closed and its a weekday
            v = Votes(vote)
            db.session.add(v)
            db.session.commit()
            percent_up = int((Votes.query.filter_by(vote='up').count() / Votes.query.count()) * 100)
            response = make_response( render_template('poll.html', percent_up=percent_up, vote=vote))

            response.set_cookie('vote', vote)
            return response
        else: # user has not voted, but the window is closed
            percent_up = int((Votes.query.filter_by(vote='up').count() / Votes.query.count()) * 100)
            return render_template("poll_market_open.html", percent_up=percent_up)

    else: # if the user has voted, then display the poll html without adding to db
        percent_up = int((Votes.query.filter_by(vote='up').count() / Votes.query.count()) * 100)
        response = make_response( render_template('poll.html', percent_up=percent_up, vote=vote))
        return response

################################################################################################################################################################
################################################################################################################################################################

if __name__ == "__main__":
    app.run()
