import urllib
import pandas as pd
import warnings
import regex as re
from pandas import Series
import itertools

warnings.filterwarnings("ignore", 'This pattern is interpreted as a regular expression, and has match groups')
warnings.filterwarnings("ignore", 'The default value of regex will change from True to False in a future version.')
day_of_week = {0: '1ПН', 1: '2ВТ', 2: '3СР', 3: '4ЧТ', 4: '5ПТ', 5: '6СБ'}
week_types = {0: "не четная", 1: "четная"}
lines = []


def get_all_aud():
    df = pd.read_excel("output.xlsx")
    all_auds = beautify_auds(df)
    # print(*all_auds, sep='\n')
    for num_day in range(6):
        for num_subj in range(1, 7):
            for week in range(0, 2):
                empty_auds = get_empty_auds(df, all_auds, num_day, num_subj, week)
                empty_auds = split_auds_in_floors(empty_auds)
                line = [day_of_week[num_day], num_subj, week_types[week], ''.join(empty_auds['1']),
                        ''.join(empty_auds['2']), ''.join(empty_auds['3']), ''.join(empty_auds['4']),
                        ''.join(empty_auds['комп1']), ''.join(empty_auds['комп2']), ''.join(empty_auds['комп3']),
                        ''.join(empty_auds['комп4']), ''.join(empty_auds['ФОК']), ''.join(empty_auds['Другие'])]
                line.extend(())
                lines.append(line)

    df = pd.DataFrame(lines, columns=["num_day", "num_subj", "week", "empty_1_floor", "empty_2_floor",
                                      "empty_3_floor", "empty_4_floor", "empty_komp_1_floor",
                                      "empty_komp_2_floor", "empty_komp_3_floor", "empty_komp_4_floor",
                                      "empty_FOC", "other_empty"])
    df.to_excel("empty_aud.xlsx")


def get_empty_auds(df, all_auds, num_day, num_subj, week):
    df_num_day = df[df['num_day'] == day_of_week[num_day]]
    df_num_subj = df_num_day[df_num_day['num_subj'] == num_subj]
    df_week = df_num_subj[df_num_subj['week'] == week_types[week]]

    auds_busy_this_day = beautify_auds(df_week)
    empty_auds = [" " + aud for aud in all_auds if aud not in auds_busy_this_day]
    empty_auds.sort()
    return empty_auds


def beautify_auds(df):
    # Причесали - забрали все аудитории стромынки, оставили только колонку названий аудиторий,
    # убрали переносы строки по бокам (strip) и все лишние пробелы (replace), оставили уникальные аудитории
    all_auds = sorted(list(set(df[df["aud_name"].str.contains('С-20', na=False)]["aud_name"]
        .map(lambda x: x.strip('\n'))
        .replace(r'[^\S\r\n]+', ' ', regex=True).unique())))
    # Причесали - по регулярке отобрали именно аудитории, убрали None после регулярки,
    # схлопнули список списков в список (itertools.chain), оставили уникальные аудитории, отсортировали
    return sorted(list(set((itertools.chain(*list(filter
               (None, [re.findall('[ауд|комп|физ].{1,12}\(С\-20\)', aud) for aud in all_auds])))))))


def split_auds_in_floors(empty_auds):
    floor_auds = {'1': [], '2': [], '3': [], '4': [], 'комп1': [], 'комп2': [],
                  'комп3': [], 'комп4': [], 'ФОК': [], 'Другие': []}
    for aud in empty_auds:
        if re.search(r'\d{1,}(?![^\(]*\))', aud):
            aud_number = re.search(r'\d{1,}(?![^\(]*\))', aud)
            if 'физ' in aud:
                floor_auds['ФОК'].append(aud)
                continue
            floor = str(aud_number[0][0]) if len(aud_number[0]) > 2 else '1'
            if 'комп' in aud:
                floor_auds["комп" + floor].append(aud)
            floor_auds[floor].append(aud)
        else:
            floor_auds['Другие'].append(aud)
    return floor_auds


if __name__ == '__main__':
    get_all_aud()
