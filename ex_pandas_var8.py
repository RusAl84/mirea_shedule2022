import numpy as np
import pandas as pd

df = pd.read_excel('./test.xlsx', index_col=0)


# Вариант 5: Найти список всех групп для которых проводят занятия
all_groups=[]
count_rows = len(df.axes[1])
# for i in range(4, count_rows, 15):
#     all_groups.append(df.iloc[0,i])
#     all_groups.append(df.iloc[0,i+5])
# print(all_groups)


for num_day in range(6):
    for num_subj in range(0, 12, 2):
        for week in range(0, 2):
            rows, cols = len(df.axes[0]), len(df.axes[1])
            for group_col_num in range(0, cols - 8, 5):
                line = 2 + num_day  * 2 + num_subj + week
                group = str(df.iloc[0, 5 + group_col_num])
                subj_name=""
                if len(group) > 2 and rows >= 97:
                    subj_name = df.iloc[line, 5 + group_col_num]
                print(subj_name)
