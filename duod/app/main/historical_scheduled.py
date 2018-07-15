import requests
from datetime import date
from bs4 import BeautifulSoup
from models import Historical, Votes

#SOUP
quote_page = requests.get('http://markets.businessinsider.com/index/dow_jones')
soup = BeautifulSoup(quote_page.text, 'html.parser')

today_close = soup.find(class_='push-data ')
yest_close = soup.find(class_='price-row-price')

today = today_close.contents[0]
yest = yest_close.contents[0]

#DATETIME
date = date.today()

#COOKIES DELETION
s = requests.session()
if 'vote' in request.cookies:
    >>> s.cookies.clear()

#CLEAR VOTE DB
models.Votes.query.delete()
db.session.commit()

#DB VARS
dbdate = date(date)
up = value('up')
down = value('Down')
             

if yest < today:
    print "The DJIA closed down up."
    models.Historical.add(dbdate)
    models.Historical.add(up)
    db.session.commit()
else:
    print "The DJIA closed down today."
    models.Historical.add(dbdate)
    models.Historical.add(down)
    db.session.commit()

