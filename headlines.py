#!/usr/bin/python3

import datetime
import feedparser
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import json
import urllib
from urllib.request import urlopen

app = Flask(__name__)

RSS_FEEDS={'baidu':'http://news.baidu.com/ns?word=shanghai&tn=newsrss&sr=0&cl=2&rn=20&ct=0',
	'iol':'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS={"publication":'baidu',
	"city":'Shanghai, CN'}


def get_weather(query):
	api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
	query=urllib.parse.quote(query)  # escape the input string
	url=api_url.format(query)
	data = urlopen(url).read()
	data = data.decode('utf-8')
	parsed=json.loads(data)
	weather = None
	if parsed.get("weather"):
		weather={"description": parsed["weather"][0]["description"],
			"temperature":parsed["main"]["temp"],
			"city":parsed["name"],
			"country":parsed["sys"]["country"]
		}

	return weather

def get_value_with_fallback(key):
	if request.args.get(key):
		return  request.args.get(key)
	if request.cookies.get(key):
		return  request.cookies.get(key)
	return DEFAULTS[key]
	

@app.route("/")
def home():
	publication = request.args.get("publication")
	if not publication or publication.lower() not in RSS_FEEDS:
		publication = request.cookies.get("publication")
		if not publication or publication.lower() not in RSS_FEEDS:
			publication = DEFAULTS['publication']
	else:
		publication = publication.lower()

	articles = get_news(publication)

	city = get_value_with_fallback("city")
	weather = get_weather(city)

	response=make_response(  render_template("home.html",
		arts=articles,
		weather=weather ) )

	expires = datetime.datetime.now() + datetime.timedelta(days=30)
	response.set_cookie("publication", publication, expires=expires)
	response.set_cookie("city", city, expires=expires)

	return response



def get_news(publication):

	feed = feedparser.parse(RSS_FEEDS[publication])
	return feed.entries
	

if __name__ == '__main__':
	app.run(port=5000, debug = True)


