import numpy as np
import pandas as pd

df = pd.read_excel('./test.xlsx', index_col=0)


# Вариант 5: Найти список всех групп для которых проводят занятия
all_groups=[]
count_rows = len(df.axes[1])

payload={}
for i in range(4, count_rows, 15):
    ind_1=i
    ind_2=i+5
    for num_day in range(6):
        for num_subj in range(0, 14, 2):
            for week in range(0, 2):
                line=2+num_day*14+num_subj+week
                set_days= {0:"ПН", 1:"ВТ", 2:"СР", 3:"ЧТ", 4:"ПТ", 5:"СБ"}
                set_week= {0:"(ЧЕТ)", 1:"(НЕ_ЧЕТ)"}
                str1=f"{set_days[num_day]}_{set_week[week]}_{int(num_subj/2+1)}"
                if len(str(df.iloc[line,ind_1]))>4 :
                    if str1 in payload:
                        payload[str1]+=1
                    else:
                        payload[str1]=1
                if len(str(df.iloc[line,ind_2]))>4 :
                    if str1 in payload:
                        payload[str1]+=1
                    else:
                        payload[str1]=1
                print()
    all_groups.append(df.iloc[0,i])
    all_groups.append(df.iloc[0,i+5])
payload=dict(sorted(payload.items(), key=lambda item: item[1]))
# {k: v for k, v in sorted(payload.items(), key=lambda item: item[1])}
print(payload)    
# print(all_groups)



