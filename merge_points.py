import pandas as pd

from caopoints2021 import pointsData21
from caopoints2020 import points2020
from caopoints2019 import points2019


merge_points_1 = pd.merge(points2019, points2020, on = 'Course_Code')
print(merge_points_1)