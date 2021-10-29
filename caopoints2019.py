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

pdffilepath = currentpath + '\\' + 'cao2019' + nowstrng + '.pdf'

def main():
    download_file('http://www2.cao.ie/points/lvl8_19.pdf')

def download_file(download_url):
    response = urllib.request.urlopen(download_url)
    file = open(pdffilepath, 'wb')
    file.write(response.read())
    file.close()
    print("Completed")

    pointsdf = tabula.read_pdf(pdffilepath, pages = 'all')
    count = 0

    colnames = ["Course Code", "Course Name", "R1 Points", "R2 Points"]


    list = []

    for item in pointsdf:
        for info in item.values: 
            list.append(info) 
        
        points2019 = pd.DataFrame (list, columns=colnames)
        points2019.to_excel('outfile.xlsx', sheet_name='Sheet1', index=True)



   

if __name__ == "__main__":
    main()
