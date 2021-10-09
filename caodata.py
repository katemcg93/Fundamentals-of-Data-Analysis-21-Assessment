from bs4 import BeautifulSoup
import csv as csv

with open ("l8.php.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

print ("Sanity")

outputfile = []

for tag in soup.find_all('pre'):
    line = soup.get_text(separator="\n")
    print(line)
    with open ('caodata.csv', 'w') as f:
        f.write(line)

