from flask import Flask, render_template, url_for
import re
import os
from bs4 import BeautifulSoup
from bookapp import app

cwd = os.path.dirname(os.path.realpath(__file__))
BOOK = open(cwd+"/static/data/senseandsensibility.html").read()

def parse_htmlbook(page):
	links = get_chap_links(page)
	sections = {}
	for ind in range(len(links)):
		section = {}
		start = links[ind]
		print ind, len(links)-1
		if ind < len(links)-1:
			end = links[ind+1]
			patt = ('<A NAME="' + start +
			'"></A>(?P<sectionbody>.*)<A NAME="' +
			end + '">' )
			match = re.search(patt,page,re.MULTILINE|re.DOTALL)
			if match == None:
				raise Exception('patt: '+patt+'\n\n')
		else:
			patt = ('<A NAME="' + start + '"></A>(?P<sectionbody>.*)<pre>')
			match = re.search(patt,page,re.MULTILINE|re.DOTALL)
		if match:
			soup = BeautifulSoup(match.group("sectionbody"), 'html.parser')
			plist = [p.contents[0] for p in soup.find_all('p')]
			section['title']= (soup.find('h3').contents)[0]
			section['plist']= plist
			sections[start] = section
	return links, sections

def get_chap_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [str(link.get('href'))[1:]
	         for link in soup.find_all('a') if link.get('href')]
	return links

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/<chap>')
def chapter(chap):
	(chapters, text) = parse_htmlbook(BOOK)
	key = 'chap' + ('0'+chap if len(chap)==1 else chap)
	return render_template("section.html", chapters=chapters, text=text[key])