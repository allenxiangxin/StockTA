'''
# Earnings: Company Earnings Calendar 
Generate quarterly earnings alarms based on Yahoo Finance. The earnings normally have impacts on stock price.

The python package `yahoo_earnings_calendar` comes from:
https://github.com/wenboyu2/yahoo-earnings-calendar

SMS message is send via www.twilio.com API
'''

import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar

# Get the calendar in one week
yec = YahooEarningsCalendar()
date_from = datetime.datetime.now()
date_to = date_from + datetime.timedelta(days=7) 
print(date_from, ' to ', date_to)
aList = yec.earnings_between(date_from, date_to)


# Read my watch list saved in a txt file
my_list=[]
with open ('private_info/watchlist.txt', "r") as f:
    for line in f:
        for word in line.split():
            my_list.append(word)
print(my_list)

# Setup twilio API
from twilio.rest import Client 
with open ('private_info/twilio_token.txt', "r") as f:
    for line in f:
        for word in line.split():
            my_token= word
account_sid = 'ACc249fe284543fcf71c91d9897dbe5ccc' 
auth_token = my_token
client = Client(account_sid, auth_token) 


# Send SMS message once 
main_text="Company Earnings Alarm: \n"
counter=0
for i in range(len(aList)):
    aCompany = aList[i]
    if aCompany['ticker'] in my_list:
        counter+=1
        main_text += aCompany['companyshortname'] \
        +' (' \
        +aCompany['ticker']  +') ' \
        + aCompany['startdatetime'] \
        +' exp EPS='\
        + str(aCompany['epsestimate']) \
        +'\n'

if (counter!=0):
    print(main_text)
    message = client.messages.create( from_='+18056170294', to='+18052524078', body=main_text)
else:
    print("None in next week !")
