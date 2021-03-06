import re
import requests as rq
import csv
import datetime as dt
import os
import pandas as pd
import urllib
from urllib.request import urlretrieve

#Getting current date and time so unique, up to date version of site is saved each time code is run
#Note that underscores are being used instead of slashes, as slashes will cause issues when generating the file path

timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')


#Getting current directory to pass to filepath variable

currentpath = os.getcwd()



#Getting data from CAO site
resp = rq.get('http://www2.cao.ie/points/l8.php')


#Constructing filepath
filepath  = currentpath + '\\' + 'Points_Data'+ '\\' + 'cao2021'+ nowstrng + '.html'
csvfilepath = currentpath + '\\' +'Points_Data'+ '\\'+ 'cao2021' + nowstrng + '.csv'



#Changing encoding from iso-8859-1 to cp1252, one line uses an x96 character (-) which is not supported in iso-8859-1. 
#If encoding is not changed the file won't be decoded
original_encoding = resp.encoding
resp.encoding = 'cp1252'


#Writing html text to file so original format is stored on repository
with open(filepath, "w") as f:
    f.write(resp.text)

#r character means that text will be treated as raw string, and / or * characters will be interpreted as part of string
# Brackets are dividing the text into the sections we're looking for - 
    # course code (2 letters + 3 digits)
    # course name (string of undefined length)
    # R1 points (3 digits)
    # R2 points if present
    # The * at end allows for whitespace
coursematch = re.compile(r'([A-Z]{2}[0-9]{3})  (.*)([0-9]{3})(\*?) *')

total_lines  = 0

with open (csvfilepath,"w") as f:
    for line in  resp.iter_lines ():
        dline = line.decode('cp1252')
        re.sub(' +', " ", dline)
        re.sub(",", " ", dline)
        if coursematch.fullmatch(dline):
            total_lines = total_lines + 1
            linesplit = re.split('  +', dline)
            f.write(','.join(linesplit) + '\n')


headers = ["Course_Code", "Course_Name", "R1_Points21", "R2_Points21"]

pointsData21 = pd.read_csv (csvfilepath, sep = ',', names = headers, encoding = 'cp1252')


#Replacing all alphanumeric chars and words with nothing, so I can convert these columns to numeric
pointsData21['R1_Points21'] = pointsData21['R1_Points21'].str.replace(r'[^0-9]+', '', regex = True)
pointsData21['R2_Points21'] = pointsData21['R2_Points21'].str.replace(r'[^0-9]+','', regex = True)

pointsData21['R1_Points21'] = pointsData21['R1_Points21'].str.replace(r'[a-zA-Z]+', '', regex = True)
pointsData21['R2_Points21'] = pointsData21['R2_Points21'].str.replace(r'[a-zA-Z]+', '', regex = True)


pointsData21[["R1_Points21"]] = pointsData21[["R1_Points21"]].apply(pd.to_numeric, downcast = 'integer')
pointsData21[["R2_Points21"]] = pointsData21[["R2_Points21"]].apply(pd.to_numeric, downcast = 'integer')

pointsData21.to_csv(csvfilepath)