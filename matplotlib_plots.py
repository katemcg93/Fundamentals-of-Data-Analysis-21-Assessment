import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import matplotlib.cm as cmap

pd.set_option("display.precision", 2)

fh_dataframe = pd.read_csv('C:\\Users\\Owner\\Desktop\\Fundamentals-of-Data-Analysis-21-Assessment\\Framingham.csv')

description = fh_dataframe.describe()
print(description)


fh_dataframe = fh_dataframe.replace({'male':1}, value = 'Male')
fh_dataframe = fh_dataframe.replace({'male':0}, value = 'Female')
fh_dataframe = fh_dataframe.rename(columns= {'male':'gender'})

eduLevel1 = fh_dataframe[fh_dataframe["education"] == 1]
eduLevel2 = fh_dataframe[fh_dataframe["education"] == 2]
eduLevel3 = fh_dataframe[fh_dataframe["education"] == 3]
eduLevel4 = fh_dataframe[fh_dataframe["education"] == 4]

plt.hist(eduLevel1["BMI"], stacked = True, label = 'Education Level 1', color = '#DD7373')
plt.hist(eduLevel2["BMI"], stacked = True, label = 'Education Level 2', color = '#3B3561')
plt.hist(eduLevel3["BMI"], stacked = True, label = 'Education Level 3', color = '#EAD94C')
plt.hist(eduLevel4["BMI"], stacked = True, label = 'Education Level 4', color = '#51A3A3')
legend = plt.legend()
plt.show()
plt.close()


corr_coeff_fh = fh_dataframe.corr()
print(corr_coeff_fh)
fig = plt.figure(figsize = (20,20))
ax = fig.add_subplot(111)
corrmat = ax.matshow(corr_coeff_fh,cmap = 'coolwarm', vmin = -1, vmax = 1)
fig.colorbar(corrmat)
ticks = np.arange(0, len(corr_coeff_fh.columns), 1)
print(ticks)
ax.set_xticks(ticks)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(corr_coeff_fh.columns)
ax.set_yticklabels(corr_coeff_fh.columns)
plt.show()