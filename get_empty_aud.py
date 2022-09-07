import urllib
import pandas as pd


def get_all_aud(subj_records):
    dweek = {}
    dweek[0] = "не четная"
    dweek[1] = "четная"
    dnum_day = {}
    dnum_day[0] = "1ПН"
    dnum_day[1] = "2ВТ"
    dnum_day[2] = "3СР"
    dnum_day[3] = "4ЧТ"
    dnum_day[4] = "5ПТ"
    dnum_day[5] = "6СБ"
    for num_day in range(6):
        for num_subj in range(1, 7):
            for week in range(0, 2):
                s = 1


def get_empty_auds(df, all_auds, num_day, num_subj, week):
    dweek = {}
    dweek[0] = "не четная"
    dweek[1] = "четная"
    dnum_day = {}
    dnum_day[0] = "1ПН"
    dnum_day[1] = "2ВТ"
    dnum_day[2] = "3СР"
    dnum_day[3] = "4ЧТ"
    dnum_day[4] = "5ПТ"
    dnum_day[5] = "6СБ"
    list_of_colums = ["inst", "group", "num_day", "num_subj", "week", "subj_name", "subj_type", "teach_name",
                      "aud_name"]
    df_num_day = df.loc[df['num_day'] == dnum_day[num_day]]
    df_num_subj = df_num_day.loc[df_num_day['subj_name']] == str(num_subj)
    df_week = df_num_subj.loc[df_num_subj['week']] == dweek[week]
    c_auds = df["aud_name"]
    empty_auds = []
    for aud in c_auds:
        if aud in all_auds:
            empty_auds.append(aud)
    return(empty_auds)


def get_all_auds(auds):
    all_auds = set(auds)
    l_all_auds = set()
    for item in all_auds:
        if "(С-20)" in str(item):
            l_all_auds.add(item)
    all_auds = list(l_all_auds)
    # print(all_auds)
    l_auds = all_auds.copy()
    tmp_list = []
    for aud1 in all_auds:
        line = []
        for aud2 in l_auds:
            if aud2 in aud1:
                line.append(aud2)
        tmp_list.append(line)
    # print(tmp_list)
    all_auds = []
    for item in tmp_list:
        if len(item) == 1:
            all_auds.append(item[0])
        else:
            l = 10 ** 8
            el = ""
            for item1 in item:
                if len(item1) < l:
                    l = len(item1)
                    el = item1
            all_auds.append(el)
    return all_auds


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = pd.read_excel("output.xlsx")
    auds = df["aud_name"]
    all_auds = get_all_auds(auds)
    dweek = {}
    dweek[0] = "не четная"
    dweek[1] = "четная"
    dnum_day = {}
    dnum_day[0] = "1ПН"
    dnum_day[1] = "2ВТ"
    dnum_day[2] = "3СР"
    dnum_day[3] = "4ЧТ"
    dnum_day[4] = "5ПТ"
    dnum_day[5] = "6СБ"
    empty_auds = get_empty_auds(df, all_auds, 3, 1, 1)
    print(all_auds)
    print(empty_auds)
