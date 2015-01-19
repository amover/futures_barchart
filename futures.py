#!/usr/bin/python

import urllib2
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import argparse
import os

import __main__ as main



class barChart():
	def __init__(self,filename='data.csv'):

		url = "http://www.barchart.com/commodityfutures/Crude_Oil_WTI_Futures/CL"
		req = urllib2.Request(url)
		req.add_header('User-Agent' , 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0')
		html = urllib2.urlopen(req).read()
		
		df=pd.read_html(html, attrs={'id':'dt1'})[0]
		numcols = [u'Last', u'Change', u'Open', u'High', u'Low', u'Previous', u'Volume']
		for x in numcols:
			if df[x].dtype==object:
				df[x]=df[x].str.replace('s|,','').astype(float)
			pass
		df.Time = pd.to_datetime(df.Time)
		df.index.names=['Strike']
		df.reset_index(inplace=True)
		df.set_index(['Time','Contract','Strike'],inplace=True)
		
		self.df = df
		self.filename=filename
		try:
			print "Loaded %i records" % self.load()
			#~ self.all.append(self.df)
		except IOError:
			print "File load failed", filename
			self.all = df
		self.html = html

		
	def save(self):
		self.all.to_csv(self.filename)
		return len(self.df)
		
	def load(self):
		self.all=pd.read_csv(self.filename)
		self.all.set_index(['Time','Contract','Strike'],inplace=True)
		return len(self.all)

if __name__ == "__main__":
	dirname = os.path.dirname(os.path.realpath(__file__))
	parser = argparse.ArgumentParser()
	parser.add_argument('--filename', default=dirname+"/wti_contracts.csv", type=unicode, help='CSV filed where data is stored')
	parser.add_argument('--update', help='Download and save data',action="store_true")
	parser.add_argument('--chart', help='Show pyplot chart',action="store_true")
	args = parser.parse_args()

	bc = barChart(args.filename)
	if hasattr(main, '__file__') or "__IPYTHON__" in dir() or args.chart:
		f=plt.figure()
		ax=f.gca()
		dfp = bc.df.reset_index()
		dfp.Last.plot(ax=ax)
		ax.xaxis.set_major_locator(MultipleLocator(2))
		locs, labels = plt.xticks()
		plt.xticks(locs, list(dfp.Contract[::2]))
		plt.setp(labels, rotation=90)
		plt.fill_between(dfp.index.values,dfp.Low.values,dfp.High.values,alpha=0.3,color='r')
		plt.ion()
	if args.update:
		print "Saved %i records" % bc.save()




