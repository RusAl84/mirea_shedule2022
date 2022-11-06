import itertools
import json
import pickle
import pandas as pd
from numpy import nan
import datetime as dt

days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
week_regex = "((?<=^)( *{week})(?=,?)|(?<=,)( *{week})(?=,|$))"


def generate_df_day(df, day):
    df = df.loc[df['num_day'] == day]
    df = df.drop(columns=['num_day'])
    df = df.set_index("num_subj")
    df = df.sort_index()
    try:
        df = df.to_dict('index')
    except ValueError:
        print(df.head())
    return df


def define_week():
    today = dt.date.today()
    semester = 1 if today.month >= 9 else 2
    week_now = 1
    start_date = dt.date(today.year, 9, 1) if semester == 1 else dt.date(today.year, 2, 9)
    while today > start_date:
        today -= dt.timedelta(days=7)
        week_now += 1
    return week_now


class DataManager:
    def __init__(self):
        with open('df.pickle', 'rb') as handle:
            self.df = pickle.load(handle)
        with open('empty_auds.pickle', 'rb') as handle:
            self.eaud_df = pickle.load(handle)

    def get_teachers(self):
        df = self.df[(self.df["teach_name"].str.contains("nan") == False)
                     & (self.df["teach_name"].replace('', nan).notna())]
        df = df["teach_name"].drop_duplicates()
        df = df.sort_values().to_frame()
        df.reset_index(inplace=True, drop=True)
        df = df.to_dict('list')
        return json.dumps(df)

    def get_week(self, teacher: str, week: str):
        df = self.df.loc[self.df['teach_name'] == teacher]
        df = df.loc[df['weeks_available'].str.contains(week_regex.format(week=int(week)), regex=True)]
        df = df.drop(columns=['teach_name', 'inst', 'week', 'weeks_available'])
        df_days = [generate_df_day(df, day) for day in days]
        res = json.dumps(dict(zip(days, df_days)))
        return res


    def get_empty_auds(self, num_subj: int, need_komp: bool):
        week_now, day_now = define_week(), days[dt.datetime.today().weekday()]
        df = self.eaud_df.loc[self.eaud_df["num_day"] == day_now]
        df = df.loc[df["num_subj"] == num_subj]
        df = df.loc[df["week"] == week_now]
        df = df.drop(columns=["num_day", "num_subj", "week"])
        df = df.set_index("floor")
        df_base = df.drop(columns=["comp"]).to_dict('index')
        df_comp = df.drop(columns=["basic"]).to_dict('index')
        for k in df_base:
            df_base[k] = df_base[k]["basic"]
            df_comp[k] = df_comp[k]["comp"]
        ret_dict = {"basic": df_base, "all": df_comp}
        return json.dumps(ret_dict)

if __name__ == "__main__":
    manager = DataManager()
    manager.get_empty_auds(2, False)
