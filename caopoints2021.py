import re
import urllib
import requests as rq
import datetime as dt
import os
import pandas as pd
import urllib3
import urllib
from urllib.request import urlopen


#Getting current date and time so unique, up to date version of site is saved each time code is run
#Note that underscores are being used instead of slashes, as slashes will cause issues when generating the file path

timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')


#Getting current directory to pass to filepath variable

currentpath = os.getcwd()



#Getting data from CAO site
resp = rq.get('http://www2.cao.ie/points/l8.php')

response = urlopen('http://www2.cao.ie/points/l8.php')
charset = response.headers.get_content_charset()
print(charset)


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


#Regex Statement to identify lines containing course data
#First section finds corse code - 1 letter and three numbers
#Next section retrieves all other info - course name, points etc
coursematch = re.compile(r'([A-Z]{2}[0-9]{3})(.*)')

#Check to ensure all lines are processed
total_lines  = 0

with open (csvfilepath,"w") as f:
    for line in  resp.iter_lines ():
        dline = line.decode('cp1252')
        if coursematch.fullmatch(dline):
            # Add one to the lines counter.
            total_lines = total_lines + 1
            # The course code.
            course_code = dline[:5]
            # The course title - char 7 is the start of the title section, char 57 is where the longest title ends
            # strip is to remove white space at the beginning and end of each line
            course_title = dline[7:57].strip()
            # Round one points.
            course_points = re.split(' +', dline[60:])

            #Splitting points into round one and two, where r2 points exist
            if len(course_points) != 2:
                course_points = course_points[:2]
            # Join the fields using a comma.
            linesplit = [course_code, course_title, course_points[0], course_points[1]]
            # Rejoin the substrings with commas in between.
            f.write(','.join(linesplit) + '\n')

# Print the total number of processed lines.
print(f"Total number of lines is {total_lines}.")

headers = ["Course_Code", "Course_Name", "R1_Points21", "R2_Points21"]

pointsData21 = pd.read_csv (csvfilepath, sep = ',', names = headers, encoding = 'cp1252')


#Replacing all alphanumeric chars and words with nothing, so I can convert these columns to numeric
pointsData21['R1_Points21'] = pointsData21['R1_Points21'].str.replace(r'[^0-9]+', '', regex = True)
pointsData21['R2_Points21'] = pointsData21['R2_Points21'].str.replace(r'[^0-9]+','', regex = True)

pointsData21['R1_Points21'] = pointsData21['R1_Points21'].str.replace(r'[a-zA-Z]+', '', regex = True)
pointsData21['R2_Points21'] = pointsData21['R2_Points21'].str.replace(r'[a-zA-Z]+', '', regex = True)


#Changing points columns to numeric
pointsData21[["R1_Points21"]] = pointsData21[["R1_Points21"]].apply(pd.to_numeric, downcast = 'integer')
pointsData21[["R2_Points21"]] = pointsData21[["R2_Points21"]].apply(pd.to_numeric, downcast = 'integer')

pointsData21.to_csv(csvfilepath)