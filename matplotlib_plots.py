import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import matplotlib.cm as cmap
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

pd.set_option("display.precision", 2)

fh_dataframe = pd.read_csv('C:\\Users\\Owner\\Desktop\\Fundamentals-of-Data-Analysis-21-Assessment\\Framingham.csv')

description = fh_dataframe.describe()


fh_dataframe = fh_dataframe.replace({'male':1}, value = 'Male')
fh_dataframe = fh_dataframe.replace({'male':0}, value = 'Female')
fh_dataframe = fh_dataframe.rename(columns= {'male':'gender'})

eduLevel1 = fh_dataframe[fh_dataframe["education"] == 1]
eduLevel2 = fh_dataframe[fh_dataframe["education"] == 2]
eduLevel3 = fh_dataframe[fh_dataframe["education"] == 3]
eduLevel4 = fh_dataframe[fh_dataframe["education"] == 4]

plt.hist(eduLevel1["BMI"], stacked = True, label = 'Some Second Level Education', color = '#DD7373', bins = 15)
plt.hist(eduLevel2["BMI"], stacked = True, label = 'Completed Second Level Education', color = '#3B3561',  bins = 15)
plt.hist(eduLevel3["BMI"], stacked = True, label = 'Some Third Level Education', color = '#EAD94C',  bins = 15)
plt.hist(eduLevel4["BMI"], stacked = True, label = 'Completed Third Level Education', color = '#51A3A3',  bins = 15)
legend = plt.legend()
plt.show()
plt.close()


corr_coeff_fh = fh_dataframe.corr()
print(corr_coeff_fh)
fig = plt.figure(figsize = (20,20))
ax = fig.add_subplot(111)
corrmat = ax.matshow(corr_coeff_fh,cmap = 'rainbow', vmin = -1, vmax = 1)
fig.colorbar(corrmat)
ticks = np.arange(0, len(corr_coeff_fh.columns), 1)
ax.set_xticks(ticks)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(corr_coeff_fh.columns)
ax.set_yticklabels(corr_coeff_fh.columns)
plt.show()
plt.close()

#Reading csv containing data from Eurostat on Weekly Covid Cases
covid_df = pd.read_csv("Covid Case Data Eurostat.csv")

#File has cases and deaths, isolating data on cases to plot
covid_df = covid_df.loc[covid_df["indicator"] == "cases"]

#Creating new column with numeric form of year - week to filter on last 4 weeks
covid_df["Year_Week_int"] = covid_df["year_week"].str.replace("-", "")
covid_df["Year_Week_int"] = pd.to_numeric(covid_df["Year_Week_int"])
covid_4_wks = covid_df.loc[covid_df["Year_Week_int"] > 202145]

#Isolating the total weekly case numbers for each continent into its own dataframe to plot later
covid_africa = covid_4_wks.loc[covid_4_wks["country"] == "Africa (total)"]
covid_europe = covid_4_wks.loc[covid_4_wks["country"] == "Europe (total)"]
covid_america = covid_4_wks.loc[covid_4_wks["country"] == "America (total)"]
covid_asia = covid_4_wks.loc[covid_4_wks["country"] == "Asia (total)"]
covid_oceania= covid_4_wks.loc[covid_4_wks["country"] == "Oceania (total)"]

#Retrieving weekly count figures for each continent
y1 = covid_africa["weekly_count"]
y2 = covid_europe ["weekly_count"]
y3 = covid_america ["weekly_count"]
y4 = covid_asia ["weekly_count"]
y5 = covid_oceania["weekly_count"]

#Setting up x axis - bins and tick labels
x = [0,1,2,3]
tick_labels = ["Wk 46", "Wk 47", "Wk 48", "Wk 49"]

#Labels for legent
labels = ["Africa", "Europe", "America", "Asia", "Oceania"]

#Converting the pandas columns with weekly case numbers to numpy arrays
array1 = y1.to_numpy()
array2 = y2.to_numpy()
array3 = y3.to_numpy()
array4 = y4.to_numpy()
array5 = y5.to_numpy()


fig, ax = plt.subplots()
ax.stackplot(x, array1, array2, array3, array4, array5, labels = labels)
ax.locator_params(tight=True, nbins=4)
ax.set_xticks(range(len(tick_labels)))
ax.set_xticklabels(labels = tick_labels)

ax.set_xlabel("Week Number")
ax.set_ylabel("Weekly Covid Cases in Millions")

#Adding a tick label at each 1m interval
ax.set_yticks(np.arange(0, 5000000, 1000000))
plt.legend()
plt.show()