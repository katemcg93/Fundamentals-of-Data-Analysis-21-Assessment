import re
import requests as rq
import csv
import datetime as dt
import os
import pandas as pd

timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')

pd.set_option('display.max_rows', 1000)

currentpath = os.getcwd()
print(currentpath)

#Constructing filepath
filepath  = currentpath + '\\' + 'cao2020'+ nowstrng + '.html'
csvfilepath = currentpath + '\\' + 'cao2020' + nowstrng + '.csv'

print(filepath)

df2020 = pd.read_excel('http://www2.cao.ie/points/CAOPointsCharts2020.xlsx')
df2020.to_csv(csvfilepath, encoding = 'utf-8', index = False)

df2020 = df2020.iloc[9:,]
print(df2020)

df2020.columns = df2020.iloc[0]


df2020points = df2020[['COURSE TITLE', 'COURSE CODE2', 'R1 POINTS', 'R2 POINTS']]
print(df2020points['COURSE TITLE'])

