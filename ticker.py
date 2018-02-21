import sys
import time
import types
import urllib
import json
import sl4a
import os
try:  
  import gdata.docs.service
except ImportError:
  gdata = None

droid = sl4a.Android()
from bitbay import BitBay
from sys import argv

def event_loop():
  for i in range(10):
    time.sleep(1)
    droid.eventClearBuffer()
    time.sleep(1)
    e = droid.eventPoll(1)
    if e.result is not None:
      return True
  return False


def showCurrencies(BitBayObject):
  items = BitBayObject.getPairs()
  title = "Wybierz ticker"

  droid.dialogCreateAlert(title)
  droid.dialogSetSingleChoiceItems(items)
  droid.dialogSetPositiveButtonText('Obadaj!')
  droid.dialogShow()
  response = droid.dialogGetResponse().result
  item = droid.dialogGetSelectedItems()
  return item

def showTicker(text,pair):
  title = ("Ticker: %s" % (pair))
  droid.dialogCreateAlert(title,text)
  droid.dialogSetPositiveButtonText('OK!')
  droid.dialogShow()
  response = droid.dialogGetResponse().result
  return response['which'] == 'positive'

if __name__ == '__main__':
  os.chdir(os.path.dirname(argv[0]))
  bb=BitBay()

  r = showCurrencies(bb)[1][0]
  pair = bb.getPairs()[r]
  sys.stdout.flush()

  (curr1,curr2)=pair.split('/')
  ticker=bb.getTicker(curr1,curr2,False)
  fields=["bid", "last", "ask", "volume", "average", "max", "min", "vwap"]
  tickerText = 'Last ticker time:'+ time.ctime(bb.lastTicker(curr1,curr2))+ "\n"+ ("Pair: %s/%s" % (curr1,curr2))+ "\n"
  for key in fields:
    tickerText = tickerText + key + ":\t" + str(ticker[key]) + "\n"
  showTicker(tickerText,pair)
  
  sys.stdout.flush()
