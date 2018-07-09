from .. import db
from sqlalchemy import Column, Integer, String

class Votes(db.Model):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    vote = Column(String)

    def __init__(self, vote=None):
        self.vote = vote

    def __repr__(self):
        return '<Vote %s>' % (self.vote)
