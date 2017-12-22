# -*- coding: utf-8 -*-
import sys
import time
import urllib.request
import json
import os

class BitBay(object):
	def __init__(self):
		self.baseLink='https://bitbay.net/API/Public/'
		self.interval=60
		self.tickerPairs=dict(BTC=['PLN','USD','EUR'])
		self.tickerPairs['LTC']=list(self.tickerPairs['BTC'])+['BTC']
		cryptos=('BTC','LTC','ETH','LSK','GAME','DASH','BCC')
		for cr in cryptos[2:]:
			self.tickerPairs[cr]=list(self.tickerPairs['LTC'])
		try:
			f=open('BitBay-tickers.json') 
			self.ticker = json.loads(f.read())
			f.close()
		except:
			self.ticker = dict()
			self.updateTicker()

	def getPairs(self,currency=None):
		if currency == None:
			#trzeba uzyć wszystkich par
			pairs=[]
			for key in sorted(list(self.tickerPairs.keys())):
				for k2 in self.tickerPairs[key]:
					pairs.append("%s/%s" % (key,k2))
		else:
			if currency not in tickerPairs.keys:
				return pairs
			for k2 in self.tickerPairs[currency]:
				pairs.append("%s/%s" % (currency,k2))
		return pairs

	def updateTicker(self):
		f=open('BitBay-tickers.json','w')
		f.write(json.dumps(self.ticker))
		f.close()

	def testUpToDate(self,curr1,curr2):
		tname=curr1+curr2
		if tname in self.ticker.keys():
			#1 or more tickers
			lt = float(sorted(list(self.ticker[tname]))[-1])
			if time.time()-lt < self.interval:
				return True
			return False
		else:
			return False

	def lastTicker(self,curr1,curr2):
		tname=curr1+curr2
		if tname not in self.ticker.keys():
			return float(0)
		tt = sorted(list(self.ticker[tname].keys()))[-1]
		return float(tt)

	def getTicker(self,curr1,curr2,force=False):
		tname=curr1+curr2
		url=self.baseLink + tname + "/ticker.json"
		if force | self.testUpToDate(curr1,curr2) == False:
			try:
				with urllib.request.urlopen(url) as f:
					bhtml=f.read()
					html=bhtml.decode()
					f.close()
			except:
				print('*')
			tt=str(time.time())
			if not (tname in self.ticker.keys()):
				self.ticker[tname]=dict()
			self.ticker[tname][tt]=json.loads(html)
			self.updateTicker()
		tt = sorted(list(self.ticker[tname].keys()))[-1]
		return 	self.ticker[tname][tt]

