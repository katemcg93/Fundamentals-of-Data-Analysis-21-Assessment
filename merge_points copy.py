import re
import pandas as pd
from pandas.core.reshape import merge
import numpy as np
from numpy import random
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from scipy import stats

plt.style.use('seaborn-pastel')

np.set_printoptions(precision = 2)

timenow = dt.datetime.now()
nowstrng = timenow.strftime('%Y%m%d_%H%M%S')

currentpath = os.getcwd()

#Constructing filepath
csvfilepath = currentpath + '\\' + 'Points_Data' + '\\' +'Combined' + nowstrng + '.csv'

from caopoints2021 import pointsData21
from caopoints2020 import points2020
from caopoints2019 import points2019

fig, ax = plt.subplots()
sns.kdeplot(points2019["R1_Points19"], ax = ax,  color = "#987284", label = "2019")
ax2 = ax.twinx()
ax2.get_yaxis().set_ticks([])
sns.kdeplot(points2020["R1_Points20"], ax = ax2, color = "#9DBF9E", label = "2020")
ax3 = ax.twinx()
ax3.get_yaxis().set_ticks([])
sns.kdeplot(pointsData21["R1_Points21"], ax = ax3, color = "#F9B5AC", label = "2021")

lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax2.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc=0)

plt.show()
plt.close()

def descriptiveStats (x, yr, r):
    np.set_printoptions(precision = 2)
    mean = np.mean(x)
    std = np.std(x)
    median = x.median()
    mode = x.mode().values[0].tolist()
    output = """
    Year: {0}
    Points Round: {1}
    Mean Points Value :  {2}
    Standard Deviation : {3}
    Median : {4}
    Mode : {5}
    """.format(yr, r, round(mean,2), round(std, 2), median, mode)
    print(output)

descriptiveStats(x = points2019["R1_Points19"], yr = "2019", r = "1")
descriptiveStats(x = points2020["R1_Points20"], yr = "2020", r = "1")
descriptiveStats(x = pointsData21["R1_Points21"], yr = "2021", r = "1")

descriptiveStats(x = points2019["R2_Points19"], yr = "2019", r = "2")
descriptiveStats(x = points2020["R2_Points20"], yr = "2020", r = "2")
descriptiveStats(x = pointsData21["R2_Points21"], yr = "2021", r = "2")

merge_points_1 = pd.merge(points2019, points2020, on = 'Course_Code')
merge_points_2 = pd.merge(merge_points_1, pointsData21, on = 'Course_Code')
merge_points_2 = merge_points_2.rename(columns = {"CATEGORY (i.e.ISCED description)" : "Course Category"})
merge_points_2 = merge_points_2.drop(columns = ["Course Name_x", "Course Name_y"])
print(merge_points_2.columns)

university_df = merge_points_2[merge_points_2["HEI"].isin(["Dublin City University", "Maynooth University", "Trinity College Dublin", "University College Cork (NUI)", "University College Dublin (NUI)", "University of Limerick", 'National University of Ireland, Galway'])]
university_melt = university_df.melt(id_vars = "HEI", value_vars= ["R1_Points19", "R1_Points20", "R1_Points21"])

fig, ax = plt.subplots()
sns.barplot(data = university_melt, x = "HEI", y = "value", hue = "variable", palette = "coolwarm")
xlabels = ["UCC", "DCU", "TCD", "UCD", "NUIG", "UL", "NUIM"]
ax.set_xticklabels(labels = xlabels, rotation=45, ha='right', rotation_mode='anchor')
plt.tight_layout()
plt.show()
plt.close()

it_df = merge_points_2[merge_points_2["HEI"].isin(["Athlone Institute of Technology", "Cork Institute of Technology", "Galway-Mayo Institute of Technology", "Institute of Technology, Sligo", "Institute of Technology, Tralee", "Waterford Institute of Technology"])]
it_melt = it_df.melt(id_vars = "HEI", value_vars= ["R1_Points19", "R1_Points20", "R1_Points21"])

fig, ax = plt.subplots()
sns.barplot(data = it_melt, x = "HEI", y = "value", hue = "variable", palette = "muted")
xlabels = ["Athlone IT", "CIT", "GMIT", "IT Sligo", "IT Tralee", "WIT"]
ax.set_xticklabels (labels = xlabels, rotation=45, ha='right', rotation_mode='anchor')
plt.tight_layout()
plt.show()
plt.close()


r1pointsonly = merge_points_2[["R1_Points19", "R1_Points20", "R1_Points21"]]
r2pointsonly = merge_points_2[["R2_Points19", "R2_Points20", "R2_Points21"]]

fig, (ax1, ax2) = plt.subplots(ncols = 2)
sns.boxplot(ax = ax1, data = r1pointsonly, palette = "fireice")
sns.boxplot(ax = ax2, data = r1pointsonly, palette = "fireice")
plt.show()

#Make plot bigger
fig, ax = plt.subplots(figsize=(14,10))

#Alignment parameters, will need this to rotate tick labels
ha = ['right', 'center', 'left']
#Initializing total column to store counts
merge_points_2["Total Courses"] = 1
#Group DF by course category then cound number of unique entries
course_categories = merge_points_2.groupby(["Course Category"])["Total Courses"].count()
#Convert the groupby object back to a df to make it easier to sort and plot
course_df = pd.DataFrame(course_categories, columns = ["Total Courses"])
#Sort in descending order by course category to get top 10
sorted_courses = course_df.sort_values(by = ["Total Courses"], ascending = False)
top_10_courses = sorted_courses.head(n = 10).plot(ax = ax, kind = "bar")
#Fix labels so they're not overlapping
xlabels = ax.get_xticklabels()
ax.set_xticklabels(xlabels, rotation=45, ha='right', rotation_mode='anchor')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.suptitle("Top 10 Areas of Study")
plt.title("Based on Count of Courses Offered")
plt.savefig("Top_10_courses.png", bbox_inches='tight')
plt.tight_layout()
plt.close()

top_5_courses = sorted_courses.head(n = 5)
top_5_list = top_5_courses.index.tolist()
top_5_filter = merge_points_2["Course Category"].isin(top_5_list)
top_5_df = merge_points_2[top_5_filter]

fig, ax = plt.subplots()
top_5_melt = top_5_df.melt(id_vars = ["Course Category"], value_vars= ["R1_Points19", "R1_Points20", "R1_Points21"])
sns.violinplot(data = top_5_melt, y = "value", x = "Course Category", hue = "variable", palette = "dark")
xlabels =["ICT", "Health", "Business", "Arts", "Engineering"]
ax.set_xticklabels(xlabels, rotation=45, ha='right', rotation_mode='anchor')
plt.tight_layout()
plt.show()
plt.close()

fig, ax = plt.subplots()
top_5_melt = top_5_df.melt(id_vars = ["Course Category"], value_vars= ["R2_Points19", "R2_Points20", "R2_Points21"])
sns.violinplot(data = top_5_melt, y = "value", x = "Course Category", hue = "variable", palette = "bright")
xlabels =["ICT", "Health", "Business", "Arts", "Engineering"]
ax.set_xticklabels(xlabels, rotation=45, ha='right', rotation_mode='anchor')
plt.tight_layout()
plt.show()
plt.close()


def course_trends2(df, col, yr, highlow):

    pd.set_option('display.max_columns', 500)

    points_df =  df.sort_values(col, ascending = highlow).head(10)
    with pd.option_context('expand_frame_repr', False):
        print("\n")
        print("Top Courses : {}".format(yr))
        print("\n")
        print(points_df[["Course_Code", "Course_Name", col]])
    
    return points_df


course_trends2(df = merge_points_2, col = "R1_Points19", yr = "2019", highlow = False)
course_trends2(df = merge_points_2, col = "R1_Points20", yr = "2020", highlow = False)
course_trends2(df = merge_points_2, col = "R1_Points21", yr = "2021", highlow = False)

exclude_arts = merge_points_2[merge_points_2["Course Category"]!= "Arts"]
exclude_arts_portfolio = exclude_arts[exclude_arts["R1_Points19"] <=625]


course_trends2(df = exclude_arts, col = "R1_Points19", yr = "2019", highlow = False)
course_trends2(df = exclude_arts, col = "R1_Points20", yr = "2020", highlow = False)
course_trends2(df = exclude_arts, col = "R1_Points21", yr = "2021", highlow = False)


top_10_2019 = course_trends2(df = exclude_arts_portfolio, col = "R1_Points19", yr = "2019", highlow = False)
top_10_2020 = course_trends2(df = exclude_arts_portfolio, col = "R1_Points20", yr = "2020", highlow = False)
top_10_2021 = course_trends2(df = exclude_arts_portfolio, col = "R1_Points21", yr = "2021", highlow = False)

exclude_med = merge_points_2[~merge_points_2["Course_Name"].str.contains("Medicine")]

bottom_10_2019 = course_trends2(df = exclude_med, col = "R1_Points19", yr = "2019", highlow = True)
bottom_10_2020 = course_trends2(df = exclude_med, col = "R1_Points20", yr = "2020", highlow = True)
bottom_10_2021 = course_trends2(df = exclude_med, col = "R1_Points21", yr = "2021", highlow = True)


def course_plot(df, x):
    top_2019_melt = df.melt(id_vars = "Course_Name", value_vars= ["R1_Points19", "R1_Points20", "R1_Points21"])
    sns.set_style("whitegrid")
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    sns.lineplot(data = top_2019_melt, x= "variable", y = "value", hue = "Course_Name", style="Course_Name", palette = "deep", linewidth = 3)
    plt.legend(fontsize = "small")
    plt.savefig("{}.png".format(x), dpi = 100)
    plt.show()
    plt.close()

course_plot(df = top_10_2019, x = "top10points")
course_plot(df = bottom_10_2019, x = "bottom10points")