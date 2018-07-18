from __future__ import division
from flask import Flask, render_template, make_response, request
from datetime import datetime
from app import db
from . import main
from models import Votes
import sys
sys.path.append('../')
from app.util_funcs import market_closed, percent_up, vote_count

@main.route('/') # HOME
def home():
    vote_count_up=vote_count('up')
    vote_count_down=vote_count('down')
    p_up=percent_up()
    if 'vote' in request.cookies: #if the user has voted, return poll html
        return make_response( render_template('poll.html', percent_up=p_up, vote_count_up=vote_count_up,
            vote_count_down=vote_count_down, vote=request.cookies.get('vote')))

    return render_template ('home.html', market_closed=market_closed(datetime.utcnow()), percent_up=p_up,
        vote_count_up=vote_count_up, vote_count_down=vote_count_down) # if the above if does not run, render home


@main.route('/poll/<vote>') # VOTE
def handle_vote(vote):
    vote_count_up=vote_count('up')
    vote_count_down=vote_count('down')
    p_up=percent_up()
    if not 'vote' in request.cookies: # if the user has not voted, add their vote
        if market_closed(datetime.utcnow()): # market is closed and its a weekday
            v = Votes(vote)
            db.session.add(v)
            db.session.commit()
            response = make_response( render_template('poll.html', percent_up=percent_up(),
                vote_count_up=vote_count('up'), vote_count_down=vote_count('down'), vote=vote))
            response.set_cookie('vote', vote)
            return response
        else: # user has not voted, but the window is closed
            return render_template("home.html", percent_up=p_up,
                vote_count_up=vote_count_up, vote_count_down=vote_count_down)

    else: # if the user has voted, then display the poll html without adding to db
        response = make_response( render_template('poll.html', percent_up=p_up,
            vote_count_up=vote_count_up, vote_count_down=vote_count_down, vote=vote))
        return response
