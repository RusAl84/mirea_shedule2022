import multiprocessing
import pickle
import urllib
import pandas as pd
import warnings
import regex as re
from pandas import Series
import itertools


day_of_week = {0: 'MONDAY', 1: 'TUESDAY', 2: 'WEDNESDAY', 3: 'THURSDAY', 4: 'FRIDAY', 5: 'SATURDAY'}
week_types = {0: "нечетная", 1: "четная"}
columns = ["week", "num_day", "num_subj", "floor",  "basic", "comp"]

lines = []
week_regex = "((?<=^)( *{week})(?=,?)|(?<=,)( *{week})(?=,|$))"


def get_all_aud():
    with open('df.pickle', 'rb') as handle:
        df = pickle.load(handle)
    all_auds = beautify_auds(df)
    for week in range(1, 17):
        for num_day in range(6):
            for num_subj in range(1, 7):
                for floor in range(1, 5):
                    empty_auds = get_empty_auds(df, all_auds, num_day, num_subj, week, floor)
                    empty_auds = split_auds_by_type(empty_auds).copy()
                    line = [week, day_of_week[num_day], num_subj, floor, empty_auds['basic'], empty_auds['comp']]
                    lines.append(line)
                    empty_auds.clear()
    df = pd.DataFrame(lines, columns=columns)
    load_to_excel(df)
    with open('empty_auds.pickle', 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_empty_auds(df, all_auds, num_day, num_subj, week, floor):
    df_num_day = df[df['num_day'] == day_of_week[num_day]]
    df_num_subj = df_num_day[df_num_day['num_subj'] == num_subj]
    df_week = df_num_subj.loc[df_num_subj['weeks_available'].str.contains(week_regex.format(week=int(week)), regex=True)]
    auds_busy_this_day = beautify_auds(df_week)
    all_auds_by_floor = get_auds_by_floor(floor, all_auds)
    empty_auds = [aud for aud in all_auds_by_floor if aud not in auds_busy_this_day]
    empty_auds.sort()
    return empty_auds


def beautify_auds(df):
    all_auds = sorted(list(set(df[df["aud_name"].str.contains('С-20', na=False)]["aud_name"]
                               .map(lambda x: x.strip('\n'))
                               .replace(r'[^\S\r\n]+', ' ', regex=True)
                               .replace(r'ауд(?!\.)', 'ауд.', regex=True)
                               .replace(r'комп(?!\.)', 'комп.', regex=True)
                               .replace(r'физ(?!\.)', 'физ.', regex=True)
                               .replace(r'ауд\.(?!\s)', 'ауд. ', regex=True)
                               .replace(r'комп\.(?!\s)', 'комп. ', regex=True)
                               .replace(r'физ\.(?!\s)', 'физ. ', regex=True).unique())))
    return sorted(list(set((itertools.chain(*list(filter
                                                  (None, [re.findall('[ауд|комп|физ].{1,12}\(С\-20\)', aud) for aud in
                                                          all_auds])))))))


def get_auds_by_floor(floor, auds):
    return_data = []
    for aud in auds:
        if re.search(r'\d{1,}(?![^\(]*\))', aud):
            aud_number = re.search(r'\d{1,}(?![^\(]*\))', aud)
            aud_floor = int(aud_number[0][0]) if len(aud_number[0]) > 2 else 1
            if aud_floor == floor:
                return_data.append(aud)
    return return_data




def split_auds_by_type(empty_auds):
    floor_auds = {'basic': [], 'comp': []}
    for aud in empty_auds:
        if 'комп' in aud:
            floor_auds["comp"].append(aud)
        else:
            if 'физ' not in aud and 'ФОК' not in aud:
                floor_auds["basic"].append(aud)
    return floor_auds


def load_to_excel(df):
    writer = pd.ExcelWriter('empty_aud.xlsx')
    df.to_excel(writer, sheet_name='sheetName', index=False, na_rep='NaN')
    workbook = writer.book
    for column in df:
        column_length = max(df[column].astype(str).map(len).max() * 0.1, len(column) * 2)
        col_idx = df.columns.get_loc(column)
        form = workbook.add_format({'text_wrap': True})
        writer.sheets['sheetName'].set_column(col_idx, col_idx, column_length, cell_format=form)
    writer.save()
    with open('empty_auds.pickle', 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)



if __name__ == '__main__':
    get_all_aud()
