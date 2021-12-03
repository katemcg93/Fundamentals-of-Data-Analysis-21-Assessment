import re
import pandas as pd
from pandas.core.reshape import merge
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

from matplotlib import rcParams

timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')

currentpath = os.getcwd()

#Constructing filepath
csvfilepath = currentpath + '\\' + 'Points_Data' + '\\' +'Combined' + nowstrng + '.csv'

from caopoints2021 import pointsData21
from caopoints2020 import points2020
from caopoints2019 import points2019


merge_points_1 = pd.merge(points2019, points2020, on = 'Course_Code')
merge_points_2 = pd.merge(merge_points_1, pointsData21, on = 'Course_Code')
merge_points_2 = merge_points_2.rename(columns = {"CATEGORY (i.e.ISCED description)" : "Course Category"})
merge_points_2 = merge_points_2.drop(columns = ["Course Name_x", "Course Name_y"])

print(merge_points_2.describe())

merge_points_2.to_csv(csvfilepath, encoding = 'utf-8', index = False)

artsCourses = merge_points_2[merge_points_2['Course Category'] == "Arts"]

courseMelt = merge_points_2.melt(id_vars = ["Course_Code", "Course Category", "Course_Name"], value_vars = ["R1_Points20", "R1_Points19", "R1_Points21"], var_name = "Year")


points_19 = courseMelt[courseMelt["Year"] == "R1_Points19"]
points_20 = courseMelt[courseMelt["Year"] == "R1_Points20"]
points_21 = courseMelt[courseMelt["Year"] == "R1_Points21"]


courses_grouped = points2020[["Course_Code","CATEGORY (i.e.ISCED description)" ]].groupby("CATEGORY (i.e.ISCED description)").agg({"CATEGORY (i.e.ISCED description)": "size"})
popular_categories = courses_grouped.nlargest(5, "CATEGORY (i.e.ISCED description)").plot(kind = "bar")
plt.xticks(fontsize = 8, rotation = 360)
plt.tight_layout()
L = plt.legend()
L.get_texts()[0].set_text('Total Courses')
plt.show()

