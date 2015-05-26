from __future__ import unicode_literals
import urllib2
from bs4 import BeautifulSoup as soup

works = ('ot', 'nt', 'bofm', 'dc-testament', 'pgp')

class Scriptures:
	def __init__(self,works):
		self.works = works

class Work:
	def __init__(self,name):
		self.links = []
		self.name = name
		self.url = baseurl.format(name)
		self.getBooks(self.url)
		for name,url in self.books.iteritems():
			self.addBook(name,url)

	def getBooks(self,url):
		page = urllib2.urlopen(url)
		parse = soup(page)
		booktags = parse.html.body.div(class_='table-of-contents')[0].findAll('a')
		self.booknames = [book.string.replace('\xa0',' ').replace('\u2014','-') for book in booktags]
		self.bookrefs = [book.get('href') for book in booktags]
		self.books = dict(zip(self.booknames,self.bookrefs))

	def addBook(self,name,url):
		book = Book(name,url)
		setattr(self,name,book)

class Book:
	def __init__(self,name,url):
		self.name = name
		self.url = url
		self.getChapters(self.url)
		for name,url in self.chapters.iteritems():
			pass
			self.addChapter(name,url)

	def getChapters(self,url):
		page = urllib2.urlopen(url)
		parse = soup(page)
		chapters = parse.html.body.div(class_='chapters')
		if len(chapters):
			self.chaptertags = chapters[0].findAll('dt')
			self.chapternames = [chapter.text for chapter in self.chaptertags]
			self.chapterrefs = [chapter.a.get('href') for chapter in self.chaptertags]
		else:
			self.chapternames = [self.name]
			self.chapterrefs = [self.url]
		self.chapters = dict(zip(self.chapternames,self.chapterrefs))

	def addChapter(self,name,url):
		chapter = Chapter(name,url)
		setattr(self,name,chapter)

class Chapter:
	def __init__(self,name,url):
		self.name = name
		self.url = url
		self.getVerses(url)

	def getVerses(self,url):
		page = urllib2.urlopen(url)
		parse = soup(page)
		verses = parse.html.body.div(id='primary')[0].findAll('p')
		for verse in verses:
			if verse.span:
				setattr(self,verse.span.text.strip(),Verse(verse))
		

class Verse:
	def __init__(self,verse):
		self.name = verse.span.text
		self.id = verse.get('uri')
		self.xrefs = [ref.get('rel')[0] for ref in verse.findAll('a',class_='footnote')]
		

baseurl = 'https://www.lds.org/scriptures/{0}?lang=eng'

standardWorks = ['Old Testament', 'New Testament', 'Book of Mormon',\
				 'Doctrine and Covenants']
#DC = Work('dc-testament')
BOM = Work('bofm')
#OT = Work('ot')
#NT = Work('nt')
#PGP = Work('pgp')
