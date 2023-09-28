import numpy as np
import pandas as pd

df = pd.read_excel('./test.xlsx', index_col=0)


# Вариант 5: Найти список всех групп для которых проводят занятия
all_groups=[]
count_rows = len(df.axes[1])
for i in range(4, count_rows, 15):
    all_groups.append(df.iloc[0,i])
    all_groups.append(df.iloc[0,i+5])
print(all_groups)

