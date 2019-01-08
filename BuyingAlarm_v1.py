'''
  The buying alarm sends reminder when at least one stock 
  on my watchlist reaches my pre-defined thresholds
'''


import pandas as pd
import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances

#You won't see my api key :D
with open ('private_info/alphavantage_api_key.txt', "r") as f:
    for line in f:
        for word in line.split():
            my_key = word 
av_api_key = my_key


# Read my watch list saved in a txt file       
my_list=[]
with open ('private_info/watchlist_buy.txt', "r") as f:
    for line in f:
        for word in line.split():
            my_list.append(word)
print(my_list)


start_date = '2018-09-01'

ti = TechIndicators(key=av_api_key, output_format='pandas')
for aTick in my_list:
    ti_d, ti_meta_d = ti.get_macd(symbol=aTick, interval='daily', fastperiod=12, slowperiod=26, signalperiod=9)
    ti_w, ti_meta_w = ti.get_macd(symbol=aTick, interval='weekly', fastperiod=12, slowperiod=26, signalperiod=9)
    mask_d = (ti_d.index >= start_date)
    mask_w = (ti_w.index >= start_date)
    ti_d = ti_d.loc[mask_d]
    ti_w = ti_w.loc[mask_w]
    slope_d = ti_d['MACD_Hist'][-1]-ti_d['MACD_Hist'][-2]
    slope_w = ti_w['MACD_Hist'][-1]-ti_w['MACD_Hist'][-2]
    
    #thresholds
    flags = [False, False]
    if (slope_w>0 and slope_d>0 and ti_d['MACD_Hist'][-1]>0):
        flags[0]=True
    if (slope_w>0 and slope_d>0 and ti_d['MACD_Hist'][-1]>0 and ti_w['MACD'][-1]<0 and ti_d['MACD'][-1]<0):
        flags[1] = True

        if (flags[1]):
            print ("Strong Buy Signal according MACD! Don't orget your checklist!")
        elif (flags[0]):
            print ("Buy Signal accoring to MACD! Don't forget your checklist!");



    
