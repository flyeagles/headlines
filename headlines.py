#!/usr/bin/python3

import feedparser
from flask import Flask
from flask import render_template


app = Flask(__name__)

RSS_FEEDS={'baidu':'http://news.baidu.com/ns?word=shanghai&tn=newsrss&sr=0&cl=2&rn=20&ct=0',
	'iol':'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
@app.route('/<publication>')
def get_news(publication='baidu'):
	feed=feedparser.parse(RSS_FEEDS[publication])
	return render_template("home.html",
		arts=feed.entries )

	

if __name__ == '__main__':
	app.run(port=5000, debug = True)


