import re
from numpy import rint
import requests as rq
import csv
import datetime as dt
import os
import pandas as pd

timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')

#Get current file path to construct backup file destination paths
currentpath = os.getcwd()

#Constructing filepath
filepath  = currentpath + '\\' + 'Points_Data' + '\\' +'cao2020'+ nowstrng + '.html'
csvfilepath = currentpath + '\\' + 'Points_Data' + '\\' +'cao2020' + nowstrng + '.csv'
pandasfilepath = currentpath + '\\' + 'Points_Data' + '\\' +'cao2020_Pandasdf' + nowstrng + '.csv'


df2020 = pd.read_excel('http://www2.cao.ie/points/CAOPointsCharts2020.xlsx', header = 10, dtype = str)
df2020.to_csv(csvfilepath, encoding = 'utf-8', index = False)
print(len(df2020.index))

#Only interested in L8 courses so filtering out other levels
points2020 = df2020[df2020["LEVEL"] == "8"]

#Creating a new version of the dataframe with only the columns I'll use for analysis
points2020 = df2020.filter(['COURSE TITLE', 'COURSE CODE2', 'R1 POINTS', 'R2 POINTS', 'CATEGORY (i.e.ISCED description)', "HEI"])
points2020.to_csv(pandasfilepath, encoding = 'utf-8', index = False )


# Keeping a version of the dataframe with non-numeric characters to do further analysis on those courses
points2020_with_chars = points2020


#Removing all non-numeric chars to get descriptive stats on points
points2020['R1 POINTS'] = points2020['R1 POINTS'].str.replace(r'[^0-9]+', '', regex = True)
points2020['R2 POINTS'] = points2020['R2 POINTS'].str.replace(r'[^0-9]+','', regex = True)

points2020['R1 POINTS'] = points2020['R1 POINTS'].str.replace(r'[a-zA-Z]+', '', regex = True)
points2020['R2 POINTS'] = points2020['R2 POINTS'].str.replace(r'[a-zA-Z]+', '', regex = True)


#Changing some of the names to match the other two years and converting points columns to numeric
points2020 = points2020.rename(columns = {"COURSE TITLE": "Course Name", "COURSE CODE2": "Course_Code", "R1 POINTS": "R1_Points20", "R2 POINTS": "R2_Points20"})
points2020[["R1_Points20"]] = points2020[["R1_Points20"]].apply(pd.to_numeric)
points2020[["R2_Points20"]] = points2020[["R2_Points20"]].apply(pd.to_numeric)

with pd.option_context('expand_frame_repr', False):
    print(points2020.head(n = 10))



