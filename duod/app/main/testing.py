from __future__ import division
from flask import Flask, render_template, make_response, request
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

@app.route('/')
def home():

    if 'vote' in request.cookies:
        percent_up = int((Votes.query.filter_by(vote='up').count() / Votes.query.count()) * 100)
        response = make_response( render_template('poll.html', percent_up=percent_up, vote=request.cookies.get('vote')))
        return response

    return render_template ('home.html')


@app.route('/poll/<vote>')
def handle_vote(vote):

    if not 'vote' in request.cookies:
        v = Votes(vote)
        db.session.add(v)
        db.session.commit()
        percent_up = int((Votes.query.filter_by(vote='up').count() / Votes.query.count()) * 100)
        response = make_response( render_template('poll.html', percent_up=percent_up, vote=vote))

        response.set_cookie('vote', vote)
        return response
    else:
        percent_up = int((Votes.query.filter_by(vote='up').count() / Votes.query.count()) * 100)
        response = make_response( render_template('poll.html', percent_up=percent_up, vote=vote))
        return response

################################################################################################################################################################
################################################################################################################################################################

if __name__ == "__main__":
    app.run()
