import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

pd.set_option("display.precision", 2)

fh_dataframe = pd.read_csv('C:\\Users\\Owner\\Desktop\\Fundamentals-of-Data-Analysis-21-Assessment\\Framingham.csv')

description = fh_dataframe.describe()
print(description)

for col in fh_dataframe.columns:
    print(col)

fh_dataframe = fh_dataframe.replace({'male':1}, value = 'Male')
fh_dataframe = fh_dataframe.replace({'male':0}, value = 'Female')
fh_dataframe = fh_dataframe.rename(columns= {'male':'gender'})

print(fh_dataframe['gender'])