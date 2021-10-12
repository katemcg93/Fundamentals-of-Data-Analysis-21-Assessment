from bs4 import BeautifulSoup
import csv as csv
import pandas as pd
import numpy as np

with open ("l8.php.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

print ("Sanity")

outputfile = []

for tag in soup.find_all('pre'):
    line = soup.get_text(separator="\n")
    with open ('caodata.csv', 'w') as f:
        f.write(line)

caodata = pd.read_csv("caodata.csv", sep = '\t', names = ["Course Code", "Course Name", "R1", "R2"])
#print(caodata)

caodf = pd.DataFrame(caodata)
pd.set_option("display.max_rows", None, "display.max_columns", None)

print(caodf)