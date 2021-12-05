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
fig, ax = plt.subplots(figsize=(14,10))
ha = ['right', 'center', 'left']
merge_points_2["Total Courses"] = 1
course_categories = merge_points_2.groupby(["Course Category"])["Total Courses"].count()
course_df = pd.DataFrame(course_categories, columns = ["Total Courses"])
sorted_courses = course_df.sort_values(by = ["Total Courses"], ascending = False)
top_10_courses = sorted_courses.head(n = 10).plot(ax = ax, kind = "bar")
xlabels = ax.get_xticklabels()
ax.set_xticklabels(xlabels, rotation=45, ha='right', rotation_mode='anchor')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()
plt.show()