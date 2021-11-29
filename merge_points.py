import re
import pandas as pd
from pandas.core.reshape import merge

import matplotlib.pyplot as plt
import seaborn as sns

from caopoints2021 import pointsData21
from caopoints2020 import points2020
from caopoints2019 import points2019


merge_points_1 = pd.merge(points2019, points2020, on = 'Course_Code')
merge_points_2 = pd.merge(merge_points_1, pointsData21, on = 'Course_Code')
merge_points_2 = merge_points_2.rename(columns = {"CATEGORY (i.e.ISCED description)" : "Course Category"})

print(merge_points_2.describe())