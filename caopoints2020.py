import re
from numpy import rint
import requests as rq
import csv
import datetime as dt
import os
import pandas as pd

timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')

pd.set_option('display.max_rows', 1000)

currentpath = os.getcwd()

#Constructing filepath
filepath  = currentpath + '\\' + 'Points_Data' + '\\' +'cao2020'+ nowstrng + '.html'
csvfilepath = currentpath + '\\' + 'Points_Data' + '\\' +'cao2020' + nowstrng + '.csv'


df2020 = pd.read_excel('http://www2.cao.ie/points/CAOPointsCharts2020.xlsx', header = 10, dtype = str)
df2020.to_csv(csvfilepath, encoding = 'utf-8', index = False)


points2020 = df2020[df2020["LEVEL"] == "8"]
points2020 = df2020.filter(['COURSE TITLE', 'COURSE CODE2', 'R1 POINTS', 'R2 POINTS', 'CATEGORY (i.e.ISCED description)'])


points2020['R1 POINTS'] = points2020['R1 POINTS'].str.replace(r'[^0-9]+', '', regex = True)
points2020['R2 POINTS'] = points2020['R2 POINTS'].str.replace(r'[^0-9]+','', regex = True)

points2020['R1 POINTS'] = points2020['R1 POINTS'].str.replace(r'[a-zA-Z]+', '', regex = True)
points2020['R2 POINTS'] = points2020['R2 POINTS'].str.replace(r'[a-zA-Z]+', '', regex = True)


points2020 = points2020.rename(columns = {"COURSE TITLE": "Course Name", "COURSE CODE2": "Course_Code", "R1 POINTS": "R1_Points20", "R2 POINTS": "R2_Points20"})
points2020[["R1_Points20"]] = points2020[["R1_Points20"]].apply(pd.to_numeric, downcast = 'integer')
points2020[["R2_Points20"]] = points2020[["R2_Points20"]].apply(pd.to_numeric, downcast = 'integer')

