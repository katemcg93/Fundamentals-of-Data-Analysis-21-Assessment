import re
import requests as rq
import datetime as dt
import os
import pandas as pd
import urllib
import urllib.request
import tabula
import seaborn as sns
import matplotlib.pyplot as plt

currentpath = os.getcwd()
print(currentpath)
timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')

#Constructing filepaths to backup PDF file and dataframe
pdffilepath = currentpath + '\\' + 'Points_Data' + '\\' +  'cao2019' + nowstrng + '.pdf'
csvfilepath = currentpath  + '\\' + 'Points_Data' + '\\' + 'cao2019' + nowstrng + '.csv'
wcharsfilepath = currentpath  + '\\' + 'Points_Data' + '\\' + 'cao2019_wchars' + nowstrng + '.csv'


#Function that takes a web address as a parameter
#Purpose is to download the data and save it as a PDF file locally
#Then can use Tabula to convert to DF
def download_file(download_url):
    response = urllib.request.urlopen(download_url)
    file = open(pdffilepath, 'wb')
    file.write(response.read())
    file.close()

    #Reading the PDF data and converting it to a dataframe
    #Count is to keep track of rows in dataframe - should have 948
    pointsdf = tabula.read_pdf(pdffilepath, pages = 'all')
    count = 0

    #Extracting only the columns that I'm interested in for further analysis
    colnames = ["Course_Code", "Course Name", "R1_Points19", "R2_Points19"]


    list = []

    for item in pointsdf:
        for info in item.values: 
            list.append(info) 
            count = count + 1
        
        points2019 = pd.DataFrame (list, columns=colnames)
        points2019.to_csv(csvfilepath, encoding = 'utf-8', index = False)
    
    print("Total Lines Processed: {}".format(count))

    return points2019
    

points2019 = download_file(download_url= 'http://www2.cao.ie/points/lvl8_19.pdf')

#Removing any rows that don't have a course code in them - these are the college names only
points2019.dropna(subset = ["Course_Code"], inplace=True)

#Want to preserve version of dataset with chars like # and * so these can be analysed separately
points2019_with_chars = points2019

#Issue with a few of the rows where # + matric was split over the R1 and R2 points columns, fixing this using find and replace
points2019_with_chars ['R1_Points19']  = points2019['R1_Points19'].str.replace("# +mat", "# +matric", regex = False)
points2019_with_chars ['R2_Points19'] = points2019['R2_Points19'].str.replace("ic ", "", regex = False)

points2019_with_chars.to_csv(wcharsfilepath, encoding = 'utf-8', index = False)

#Removing all non-numeric chars so cols can be converted to dataframe format
points2019['R1_Points19'] = points2019['R1_Points19'].str.replace(r'[^0-9]+', '', regex = True)
points2019['R2_Points19'] = points2019['R2_Points19'].str.replace(r'[^0-9]+','', regex = True)

points2019['R1_Points19'] = points2019['R1_Points19'].str.replace(r'[a-zA-Z]+', '', regex = True)
points2019['R2_Points19'] = points2019['R2_Points19'].str.replace(r'[a-zA-Z]+', '', regex = True)


points2019[["R1_Points19"]] = points2019[["R1_Points19"]].apply(pd.to_numeric)
points2019[["R2_Points19"]] = points2019[["R2_Points19"]].apply(pd.to_numeric)


def download_student_data(download_url, yr):
    response = urllib.request.urlopen(download_url)
    file = open(pdffilepath, 'wb')
    file.write(response.read())
    file.close()

    #Reading the PDF data and converting it to a dataframe
    #Count is to keep track of rows in dataframe - should have 948
    pointsdf = tabula.read_pdf(pdffilepath, pages = 'all',pandas_options= {'header': None})
    colnames = ["Points_Range", "Total_{}".format(yr), "Percentage", "Cumulative Total", "Cumulative Percentage"]
    list = []

    for item in pointsdf:
        for info in item.values: 
            list.append(info) 

    studentpoints = pd.DataFrame (list, columns=colnames)
    print("Points Breakdown : {}".format(yr))
    print(studentpoints.head(n = 6))
    return studentpoints.head(n = 6)

students_points_2021 = download_student_data("http://www2.cao.ie/app_scoring/points_stats/lc21pts.pdf", yr = "2021")
students_points_2020 = download_student_data("http://www2.cao.ie/app_scoring/points_stats/lc20pts.pdf", yr = "2020")
students_points_2019 = download_student_data("http://www2.cao.ie/app_scoring/points_stats/lc19pts.pdf", yr = "2019")

merge_1 = pd.merge(students_points_2021, students_points_2020, on = "Points_Range")
merge_2= pd.merge(merge_1, students_points_2019, on = "Points_Range")

fig, ax = plt.subplots()
student_points_melt = pd.melt(merge_2, id_vars=["Points_Range"], value_vars = ["Total_2019", "Total_2020", "Total_2021"])
student_points_melt['value']  = student_points_melt['value'].str.replace(",", "", regex = False)
student_points_melt["value"] = pd.to_numeric(student_points_melt["value"], downcast = "integer")
yr_order = ["Total_2019", "Total_2020", "Total_2021"]
sns.barplot(data = student_points_melt, x = "variable", y= "value", hue = "Points_Range", order = yr_order, palette = "pastel")
plt.show()
plt.close()

