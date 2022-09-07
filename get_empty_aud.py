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
                s=1

def get_empty_aud(subj_records):
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
                s=1
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = pd.read_excel("output.xlsx")
    auds=df["aud_name"]
    all_auds=set(auds)
    l_all_auds= set()
    for item in all_auds:
        if "(С-20)" in str(item):
            l_all_auds.add(item)
    # sets.remove((1, 2))
    tmpset = l_all_auds
    for item in tmpset:

    print(l_all_auds)
    # df.loc[df['Customer'] == 'Bart']