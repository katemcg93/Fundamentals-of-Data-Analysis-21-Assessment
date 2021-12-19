import re
import requests as rq
import csv
import datetime as dt
import os
import pandas as pd
import urllib
import urllib.request
import tabula

currentpath = os.getcwd()
print(currentpath)
timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')

pdffilepath = currentpath + '\\' + 'Points_Data' + '\\' +  'cao2019' + nowstrng + '.pdf'
excelfilepath = currentpath  + '\\' + 'Points_Data' + '\\' + 'cao2019' + nowstrng + '.xlsx'


def download_file(download_url):
    response = urllib.request.urlopen(download_url)
    file = open(pdffilepath, 'wb')
    file.write(response.read())
    file.close()

    pointsdf = tabula.read_pdf(pdffilepath, pages = 'all')
    count = 0

    colnames = ["Course_Code", "Course Name", "R1_Points19", "R2_Points19"]


    list = []

    for item in pointsdf:
        for info in item.values: 
            list.append(info) 
        
        points2019 = pd.DataFrame (list, columns=colnames)
        points2019.to_excel(excelfilepath, sheet_name='Sheet1', index=True)
    
    return points2019
    

points2019 = download_file(download_url= 'http://www2.cao.ie/points/lvl8_19.pdf')

points2019['R1_Points19'] = points2019['R1_Points19'].str.replace(r'[^0-9]+', '', regex = True)
points2019['R2_Points19'] = points2019['R2_Points19'].str.replace(r'[^0-9]+','', regex = True)

points2019['R1_Points19'] = points2019['R1_Points19'].str.replace(r'[a-zA-Z]+', '', regex = True)
points2019['R2_Points19'] = points2019['R2_Points19'].str.replace(r'[a-zA-Z]+', '', regex = True)


points2019[["R1_Points19"]] = points2019[["R1_Points19"]].apply(pd.to_numeric, downcast = 'integer')
points2019[["R2_Points19"]] = points2019[["R2_Points19"]].apply(pd.to_numeric, downcast = 'integer')


