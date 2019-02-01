'''
    Author: X. Xiang

    The buying alarm sends reminder when at least one stock
    on my watchlist reaches my pre-defined thresholds
'''


import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances

#You won't see my api key :D
with open ('private_info/alphavantage_api_key.txt', "r") as f:
    for line in f:
        for word in line.split():
            my_key = word
av_api_key = my_key
ti = TechIndicators(key=av_api_key, output_format='pandas') #Techical Indicator
ts = TimeSeries(key=av_api_key, output_format='pandas', indexing_type='date') #Time Series

# Read my watch list saved in a txt file
to_buy_list=[]
with open ('private_info/watchlist_buy.txt', "r") as f:
    for line in f:
        for word in line.split():
            to_buy_list.append(word)
to_sell_list=[]
with open ('private_info/watchlist_sell.txt', "r") as f:
    for line in f:
        for word in line.split():
            to_sell_list.append(word)


import datetime
start_date = '2018-11-01'
import time

#----------------------------
# buy
def BuyAlarm():

    for aTicker in to_buy_list:
        # ts_d, ts_meta_d = ts.get_daily_adjusted(symbol=aTicker)
        macd_d, macd_meta_d = ti.get_macd(symbol=aTicker, interval='daily', fastperiod=12, slowperiod=26, signalperiod=9)
        macd_w, macd_meta_w = ti.get_macd(symbol=aTicker, interval='weekly', fastperiod=12, slowperiod=26, signalperiod=9)
        mask_d = (macd_d.index >= start_date)
        mask_w = (macd_w.index >= start_date)
        macd_d = macd_d.loc[mask_d]
        macd_w = macd_w.loc[mask_w]
        slope_d = macd_d['MACD_Hist'][-1]-macd_d['MACD_Hist'][-2]
        slope_w = macd_w['MACD_Hist'][-1]-macd_w['MACD_Hist'][-2]

        # thresholds
        # Todo: incoorpate RIS
        flags = [False, False]
        buy_flag = slope_w>0 and slope_d>0 and macd_d['MACD_Hist'][-1]>0 and macd_d['MACD_Hist'][-2]<=0
        if (buy_flag):
            flags[0] = True
        if (buy_flag and macd_w['MACD'][-1]<0 and macd_d['MACD'][-1]<0):
            flags[1] = True

        if (flags[1]):
            print ("Strong Buy Signal according MACD! Don't orget your checklist!")
        elif (flags[0]):
            print ("Buy Signal accoring to MACD! Don't forget your checklist!");
        else:
            print("Nothing")

#-----------------------------------


#--------------------------------
# sell
def SellAlarm(aTicker):
    macd_d, macd_meta_d = ti.get_macd(symbol=aTicker, interval='daily', fastperiod=12, slowperiod=26, signalperiod=9)
    macd_w, macd_meta_w = ti.get_macd(symbol=aTicker, interval='weekly', fastperiod=12, slowperiod=26, signalperiod=9)
    rsi_d, rsi_meta_d = ti.get_rsi(symbol=aTicker, interval='daily')
    rsi_w, rsi_meta_w = ti.get_rsi(symbol=aTicker, interval='weekly')
    #time.sleep(60) #alpha_ventage basic only allows 5 calls per minute, 500 per day

    mask_d = (macd_d.index >= start_date)
    mask_w = (macd_w.index >= start_date)
    macd_d = macd_d.loc[mask_d]
    macd_w = macd_w.loc[mask_w]
    slope_d = macd_d['MACD_Hist'][-1]-macd_d['MACD_Hist'][-2]
    slope_w = macd_w['MACD_Hist'][-1]-macd_w['MACD_Hist'][-2]
    mask_d = (rsi_d.index >= start_date)
    mask_w = (rsi_w.index >= start_date)
    rsi_d = rsi_d.loc[mask_d]
    rsi_w = rsi_w.loc[mask_w]

    # Sell alarm needs to be prompt
    # perhaps change it to macd_hour??
    sell_flag = ( macd_w['MACD_Hist'][-1]<macd_w['MACD_Hist'][-2] and macd_w['MACD_Hist'][-2]>macd_w['MACD_Hist'][-3] and (macd_w['MACD_Hist'][-1]>0 or macd_w['MACD_Hist'][-2] >0) )
    sell_flag = sell_flag or (rsi_w['RSI'][-1]>threshold_overbought and rsi_w['RSI'][-2]<threshold_overbought )
    if sell_flag:
        print(aTicker, ": shit is about to go down")

#open question: how to automatically determine proper RSI threshold
threshold_overbought=70
for aTicker in to_sell_list:
    SellAlarm(aTicker)
