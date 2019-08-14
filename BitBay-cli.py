#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from bitbay import BitBay
from sys import argv
import time

def showCurrencies(BB):
	for currency in sorted(list(BB.tickerPairs.keys())):
		print(currency)

def showPairs(BB,currency):
	l=len(currency)
	for pair in sorted(BB.tickerPairs[currency]):
		print(currency,"/",pair)

def showPair(BB,curr1,curr2,force):
	fields=["bid", "last", "ask", "volume", "average", "max", "min", "vwap"]
	print('Current time:',time.asctime())
	print('Last ticker time:',time.ctime(BB.lastTicker(curr1,curr2)))
	print("Pair: %s/%s" % (curr1,curr2))
	ticker=BB.getTicker(curr1,curr2,force)
	for key in fields:
		print(key,':\t',ticker[key])

os.chdir('/home/moneetor/bitcoin')
if argv[0][-3:] == '.py':
	argv=argv[1:]
force=False
currencies=[]

while argv:
	if argv[0][0] == '-':
		if argv[0] == "-h":
			print("""
Usage:
BitBay-cli.py currency1 currency2 [-f]
BitBay-cli.py currency1
BitBay-cli.py [-h]

When you do not using second currency in pair, you can view list of secod currencies available for measure first currency.
When you don not set first currency, ciy show all pairs of cryoptocurrencies available for using
Options are:
  -h	this screen
  -f	using force update
""")
			exit()
		elif argv[0] == "-f":
			force=True
	else:
		currencies.append(argv[0])
	argv=argv[1:]

bb=BitBay()
lc=len(currencies)
if lc >= 2:
	showPair(bb,currencies[0],currencies[1],force)
elif lc == 1:
	showPairs(bb,currencies[0])
else:
	showCurrencies(bb)
