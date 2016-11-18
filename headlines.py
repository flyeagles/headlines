#!/usr/bin/python3

import feedparser
from flask import Flask


app = Flask(__name__)

RSS_FEEDS={'baidu':'http://news.baidu.com/ns?word=shanghai&tn=newsrss&sr=0&cl=2&rn=20&ct=0',
	'iol':'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
@app.route('/<publication>')
def get_news(publication='baidu'):
	print(publication + "-----")
	feed=feedparser.parse(RSS_FEEDS[publication])
	first_art = feed.entries[0]
	return """<html>
		<body>
		<h1>BBC Headlines</h1>
		<b>{0}</b> <br/>
		<i>{1}</i> <br/>
		<p>{2}</p> <br/>
		</body>
	</html>""".format(first_art.get('title'), first_art.get('published'),
		first_art.get('summary'))

	

if __name__ == '__main__':
	app.run(port=5000, debug = True)


