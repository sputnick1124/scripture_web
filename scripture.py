import urllib2
from bs4 import BeautifulSoup as BS

page = urllib2.urlopen('https://www.lds.org/scriptures/nt/matt/13?lang=eng')
soup = BS(page)
verses = soup.html.body.div(id='primary')[0].findAll('p')

'''for verse in verses:
	if verse.marker:
		for mark in verse.findAll('sup'):
			mark.replaceWith('')
	if verse.a:
		for a in verse.findAll('a'):
			a.replaceWith(a.text)
	if verse.span:
		for span in verse.findAll('span'):
			span.replaceWith('')'''

