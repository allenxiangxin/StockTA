'''
    Author: X. Xiang

    Stock buy/sell trading alarm (work in progress)

'''

import json
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
import datetime
import time



'''
    API Mainager:
    Unless you pay for premium, alpha_ventage only allows 5 calls per minute,
    and 500 per day. The solution goes around by using multiple api_key.
    If not avoidable, force 1 min delay

    Always use the first
    (work in progress)
'''
class APIManager:

    last_api_key='';
    api_keychain=[];
    ti_list=[];
    ts_list=[];
    ti='';
    ts='';

    def __init__(self, aFile='private_info/alphavantage_api_key.json'):
        try:
            myf = open(aFile, "r")
        except IOError:
            print ("Could not open the api file:", aFile)
        self.api_file = aFile
        self.counter = 0;
        with open (self.api_file, "r") as f: #You won't see my api key :D
            for line in f:
                for word in line.split():
                    self.api_keychain.append(word)
        n_keys = len(self.api_keychain)
        self.last_api_key = self.api_keychain[n_keys-1]


    def init_av_protocol(self):
        for i in range(len(self.api_keychain)):
            aKey = self.api_keychain[i]
            self.ti_list.append(TechIndicators(key=aKey, output_format='pandas')) #Techical Indicator
            self.ts_list.append(TimeSeries(key=aKey, output_format='pandas', indexing_type='date')) #Time Series
        self.ts = self.ts_list[0]
        self.ti = self.ti_list[0]

    def permute_list(self):
        self.api_keychain.append(self.api_keychain.pop(0))
        self.ti_list.append(self.ti_list.pop(0))
        self.ts_list.append(self.ts_list.pop(0))
        self.ts = self.ts_list[0]
        self.ti = self.ti_list[0]

    def check(self):
        self.counter+=1
        if (self.counter>5):
            if (self.api_keychain[0]==self.last_api_key):
                print('The api key is used 5 times, delay for 60s ...')
                time.sleep(60) #TODO: switch to next api key
                self.permute_list()
                self.counter=1
            else:
                self.permute_list()
                self.counter=1
# ------------------------------------


'''
    buy alarm
'''
def BuyAlarm(aTicker):

    # default: fastperiod=12, slowperiod=26, signalperiod=9
    aMan.check(); ti = aMan.ti;
    macd_d, macd_meta_d = ti.get_macd(symbol=aTicker, interval='daily' )
    aMan.check(); ti = aMan.ti;
    macd_w, macd_meta_w = ti.get_macd(symbol=aTicker, interval='weekly')
    mask_d = (macd_d.index >= start_date)
    mask_w = (macd_w.index >= start_date)
    macd_d = macd_d.loc[mask_d]
    macd_w = macd_w.loc[mask_w]
    slope_d = macd_d['MACD_Hist'][-1]-macd_d['MACD_Hist'][-2]
    slope_w = macd_w['MACD_Hist'][-1]-macd_w['MACD_Hist'][-2]

    # thresholds
    # Todo: incoorpate RIS
    flags = [False, False]
    buy_flag = slope_w>0 and slope_d>0 \
                and macd_d['MACD_Hist'][-1]>0 \
                and macd_d['MACD_Hist'][-2]<=0
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


'''
    sell alarm
'''
def SellAlarm(aTicker):

    #default: fastperiod=12, slowperiod=26, signalperiod=9
    aMan.check(); ti = aMan.ti_list[0];
    macd_d, macd_meta_d = ti.get_macd(symbol=aTicker, interval='daily');
    aMan.check(); ti = aMan.ti_list[0];
    macd_w, macd_meta_w = ti.get_macd(symbol=aTicker, interval='weekly');
    aMan.check(); ti = aMan.ti_list[0];
    rsi_d, rsi_meta_d = ti.get_rsi(symbol=aTicker, interval='daily');
    aMan.check(); ti = aMan.ti_list[0];
    rsi_w, rsi_meta_w = ti.get_rsi(symbol=aTicker, interval='weekly');

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
    sell_flag = ( macd_w['MACD_Hist'][-1]<macd_w['MACD_Hist'][-2] \
                and macd_w['MACD_Hist'][-2]>macd_w['MACD_Hist'][-3] \
                and (macd_w['MACD_Hist'][-1]>0 or macd_w['MACD_Hist'][-2] >0) )\
                or (rsi_w['RSI'][-1]>rsi_overbought \
                and rsi_w['RSI'][-2]<rsi_overbought )
    if sell_flag:
        print(aTicker, ": shit is about to go down")
        return True
    else:
        print(aTicker, ": nothing!")
        return False



def send_whatsapp_alarm(main_text):
    from twilio.rest import Client
    from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse


    account_sid = 'ACc249fe284543fcf71c91d9897dbe5ccc'
    with open ('private_info/twilio_token.txt', "r") as f:
        for line in f:
            for word in line.split():
                my_token= word
    auth_token = my_token
    client = Client(account_sid, auth_token)


    main_text = "Hello whatsapp!"
    ruoyan = 'whatsapp:+16467172736'
    xin = 'whatsapp:+18052524078'
    message = client.messages.create(
                                     from_='whatsapp:+14155238886',
                                     body=main_text,
                                     to=xin)



# ------------------------
# Main
def main():

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

    #global variables
    global aMan
    aMan = APIManager()
    aMan.init_av_protocol()

    global start_date;
    start_date = datetime.datetime.today() - datetime.timedelta(days=100)
    start_date = start_date.strftime("%Y-%m-%d")
    global rsi_overbought;
    rsi_overbought=70 # how to auto determine the proper thresholds
    print('start_date:',start_date)

    sell_list = []
    for aTicker in to_sell_list:
        aFlag = SellAlarm(aTicker)
        sell_list.append(aTicker) if aFlag == True

    if len(sell_list>=1):
        main_text = 'Potential Sell Stocks are:'
        for aTicker in sell_list:
            main_text += aTicker + '; '
        tw = twilioManager.twilioManager()
        tw.send_text_alarm(main_text)


if __name__== "__main__":
    main()
