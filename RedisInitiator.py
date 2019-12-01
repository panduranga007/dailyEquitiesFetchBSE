# -*- coding: utf-8 -*-

"""
Created on Sat Dec 01 13:51:50 2019

@author: pandu ranga
"""

import os
import requests
import zipfile
import redis as rd
import pandas as pd
import datetime

#REDIS URL AND PORT
hostUrl = u'localhost'
portNo = 6379

##########################

#CONNECT TO REDIS
#THIS FUNCTION CLEARS ALL THE PREVIOUS KEYS WHILE CREATING NEW CONNECTION
def makeFreshConnection():
    conn = rd.Redis(host=hostUrl, port=portNo)
    if conn.dbsize() != 0:
        conn.flushall(asynchronous=False)
    return conn

#JUST CONNECTS TO REDIS
def makeConnection():
    conn = rd.Redis(host=hostUrl, port=portNo)
    return conn

###########################    

#GET DATE AS INPUT
year = input('Year').strip()
month = input('Month').strip()
day = input('Date').strip()

try :
    queryDate = datetime.date(int(year),int(month),int(day))
    nowDate = datetime.date.today()
    
    if nowDate <= queryDate:
        raise Exception('Current and Future dates not allowed')
except ValueError :
    raise Exception('Invalid date entered')

if len(day) != 2:
    day = '0'+day
if len(month) != 2:
    month = '0'+month    

#FILE NAMES
fileSpecifier = day+month+year[2:4]

zipName = 'EQ'+fileSpecifier+'_CSV.ZIP'
csvName = 'EQ'+fileSpecifier+'.csv'

# ZIP FILE DOWNLOAD AND EXTRACT CSV

#url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ191119_CSV.ZIP'
url = 'https://www.bseindia.com/download/BhavCopy/Equity/'+zipName
myfile = requests.get(url)
#open('EQ191119_CSV.ZIP', 'wb').write(myfile.content)
z = open(zipName, 'wb')

z.write(myfile.content)

#CLOSE FILES
z.close()

#zip = zipfile.ZipFile('EQ191119_CSV.ZIP')
zip = zipfile.ZipFile(zipName)
zip.extractall()

#CONVERT TO DATAFRAME
#equities = pd.read_csv('EQ191119.csv')
equities = pd.read_csv(csvName)
equities.head()



# FINAL DATAFRAME TO INSERT INTO REDIS
eq = equities.loc[:,['SC_CODE','SC_NAME','OPEN','HIGH','LOW','CLOSE']]

#CONVERT TO ARRAY OF DICTS
equityRecords = eq.to_dict(orient='records')

# REDIS CONNECTION
#conn = makeConnection()
conn = makeFreshConnection()

#PUSH EACH DICT INTO REDIS WITH SC_NAME AS KEY
for eachDict in equityRecords:
    code = eachDict['SC_NAME'].strip()
    eachDict.pop('SC_NAME', None)
    conn.hmset(code,eachDict)

