import pandas as pd
from regex import regex
from itertools import groupby

days_of_week = ["MONDAY", "TUESDAY", "WEDNESDAY",
                "THURSDAY", "FRIDAY", "SATURDAY"]
dweek = ["нечетная", "четная"]
week_nums = [str(i) for i in range(1, 18)]


def test():
    filename = "./shedule/ikts-1K-.xls"
    xl = pd.ExcelFile(filename)
    sheets = xl.sheet_names
    subj_records = []
    df = xl.parse(sheets[0])
    for num_day in range(6):
        for num_subj in range(0, 12, 2):
            for week in range(1, 2):
                line = 2 + num_day * 6 * 2 + num_subj + week
                znach = df.iloc[line, 5]
                print("line: {0} group: {1} num_day: {2} num_subj: {3}".format(
                    line, znach, num_day, num_subj))


def parsing_file(filename, inst):
    if not is_xls_xlsx_format(filename):
        return []
    xl = pd.ExcelFile(filename)
    sheets = xl.sheet_names
    subj_records = []
    for sheet in sheets:
        df = xl.parse(sheet)
        if not df.empty:
            pari = df.iloc[2:15, 1].values.tolist()
            pari = [int(pair) for pair in pari if str(
                pair) != 'nan' and len(str(pair)) == 1]

            if len(pari) == 0:
                continue
            reps = max(pari)
            for num_day in range(6):
                for num_subj in range(0, 12, 2):
                    for week in range(0, 2):
                        rows, cols = len(df.axes[0]), len(df.axes[1])
                        for group_col_num in range(0, cols - 8, 5):
                            line = 2 + num_day * reps * 2 + num_subj + week
                            group = str(df.iloc[0, 5 + group_col_num])
                            if len(group) > 2 and rows >= 97:
                                subj_name = df.iloc[line, 5 + group_col_num]
                                subj_type = df.iloc[line, 6 + group_col_num]
                                teach_name = df.iloc[line, 7 + group_col_num]
                                aud_name = df.iloc[line, 8 + group_col_num]
                                if is_line_legit(subj_name, group):
                                    group = prepare_group(group)
                                    subj_type = prepare_subj_type(subj_type)
                                    subj_name = prepare_subj(subj_name)
                                    subj_record = split_subjects(inst, group, days_of_week[num_day],
                                                                 round(
                                                                     (num_subj + 1.1) / 2), dweek[week],
                                                                 subj_name, subj_type, teach_name, aud_name)
                                    for record in subj_record:
                                        if record not in subj_records:
                                            subj_records.append(record)
    subj_records = concat_groups_records(subj_records)
    return subj_records


def is_xls_xlsx_format(filename):
    import codecs
    xlsx_sig = b'\x50\x4B\x05\06'
    xls_sig = b'\x09\x08\x10\x00\x00\x06\x05\x00'
    types = [
        (0, 512, 8),  # 'spreadsheet.xls',
        (2, -22, 4)]  # 'spreadsheet.xlsx'
    result = False
    for whence, offset, size in types:
        with open(filename, 'rb') as f:
            f.seek(offset, whence)  # Seek to the offset.
            bytes = f.read(size)   # Capture the specified number of bytes.
            # print codecs.getencoder('hex')(bytes)
            if bytes == xls_sig or bytes == xlsx_sig:
                result = True
    return result


def parsing_all_files(urls):
    subj_records = []
    for item in urls:
        print(f"{item[1]} {item[2]}")
        subj_record = parsing_file("./shedule/" + item[1], item[2])
        for it in subj_record:
            subj_records.append(it)
    return subj_records


def is_line_legit(subj_name, group):
    if is_subj_name_legit(subj_name) and is_group_legit(group):
        return True
    return False


def is_subj_name_legit(subj_name):
    return (len(str(subj_name)) >= 3) and (not pd.isna(subj_name)) and (str(subj_name) not in days_of_week)


def is_group_legit(group):
    return regex.match('^[а-яА-Я]{4}-\d{2}-\d{2}', group)


def prepare_group(group):
    return group[:10]


def prepare_subj_type(s_type):
    s_type = str(s_type).upper()
    s_type = ''.join(ch for ch in s_type if ch.isalnum())
    s_type = regex.sub(r"ЛАБ|ЛБ", "лаб,", s_type)
    s_type = regex.sub(r"ЛЕК|ЛК|Л", "лек,", s_type)
    s_type = regex.sub(r"ПР|П", "пр,", s_type)
    s_type = regex.sub(r"СР", "ср,", s_type)
    s_type = s_type.rstrip(", ")
    return s_type


def prepare_subj(subj_name):
    for i in range(20):
        match = regex.search(r"\d\s*п(?:/|\\|//|\\\\)?г", subj_name)
        if match is not None:
            subj_name = regex.sub(r"\d\s*п(?:/|\\|//|\\\\)?г", "", subj_name)
        else:
            break
    for i in range(20):
        match = regex.search(r"\s*п\/г", subj_name)
        if match is not None:
            subj_name = regex.sub(r"\s*п\/г", "", subj_name)
        else:
            break
    subjs = subj_name.split("\n")
    # subjs = regex.findall(r"(?:кр\.?)?\s*(?:\d\,?\s*)+н\.?[^\d]*", subj_name)
    subjes = [subj for subj in subjs if subj != '' and subj != ',']
    if subjes[0] in ["Военная", "Коммуникативные технологии в профессиональной "]:
        subjes[0] = subjes[0] + " " + subjes[1]
        subjes = [subjes[0]]
    subjes = [regex.sub(r'\s+', ' ', subj) for subj in subjes]
    subset = set()
    subjes[:] = [x for x in subjes if x not in subset and not subset.add(x)]
    return subjes


def split_subjects(inst, group, dow, num_subj, dweek, subjects, subj_type, teach_name, aud_name):
    # if teach_name == "Ермакова А.Ю." and dow == "TUESDAY":
    #     print([group, dow, num_subj, dweek, subjects, aud_name])
    string_count = len(subjects)
    teach_name = str(teach_name)
    aud_name = str(aud_name)
    weeks = []
    # if string_count == 1:
    #     subjects, weeks = define_weeks(subjects, weeks, dweek)
    #     return [[inst, group, dow, num_subj, dweek, *subjects, subj_type, teach_name, aud_name, *weeks]]
    teachers = teach_name.split('\n')
    teachers = [regex.sub(r'\s+', ' ', teacher) for teacher in teachers]
    teachers = [''.join(regex.findall(r'^[А-Яа-я]{1,20}\s?[А-Яа-я]{1}\.?\s?[А-Яа-я]{1}\.?\s?$', teacher))
                for teacher in teachers]
    print(teachers)
    for i, teacher in enumerate(teachers):
        teachers_re = regex.findall(
            r"^[А-Яа-я]{1,20}\s?[А-Яа-я]{1}\.?\s?[А-Яа-я]{1}\.?\s?$", teacher)
        if len(teachers_re) == 0:
            break
        teachers[i] = ', '.join(teachers_re)
    while len(teachers) < len(subjects):
        try:
            teachers.append(teachers[0])
        except IndexError:
            teachers.append('')
    auds = aud_name.split(',')
    auds = [aud for aud in auds if aud not in ['', ',', '\n']]
    auds = [regex.sub(r'\s+', ' ', aud) for aud in auds]
    while len(auds) < len(subjects):
        auds.append(auds[0])
    if string_count == 1:
        subjects, weeks = define_weeks(subjects, weeks, dweek)
        return [[inst, group, dow, num_subj, dweek, *subjects, subj_type, teachers[0], auds[0], *weeks]]
    # print(subjects, teachers, auds)
    # Начинаем делить пары
    subj_type = subj_type.split(',')
    while len(subj_type) < len(subjects):
        try:
            subj_type.append(subj_type[0])
        except IndexError:
            subj_type.append('')
    subjects, weeks = define_weeks(subjects, weeks, dweek)
    subj_recs = []
    for i in range(len(subjects)):
        subj_recs.append([inst, group, dow, num_subj, dweek,
                         subjects[i], subj_type[i], teachers[i], auds[i], weeks[i]])
    return subj_recs


def define_week_when(subj_name):
    while 'п/г' in subj_name:
        subj_name = regex.sub(r"\d п\/г", "", subj_name)
        subj_name = regex.sub(r"п\/г", "", subj_name)
    subjs = subj_name.split("\n")
    # subjs = regex.findall(r"(?:кр\.?)?\s*(?:\d\,?\s*)+н\.?[^\d]*", subj_name)
    subjes = [subj for subj in subjs if subj != '' and subj != ',']
    if subjes[0] in ["Военная", "Коммуникативные технологии в профессиональной "]:
        subjes[0] = subjes[0] + subjes[1]
        subjes = [subjes[0]]
    subjes = [regex.sub(r'\s+', ' ', subj) for subj in subjes]
    subjes = list(set(subjes))
    return ' '.join(subjes)


def define_weeks(subjects, weeks, dweek):
    for i, subj in enumerate(subjects):
        match = regex.match(r"(?:кр\.?)?\s*(?:\d\,?\s*)+н\.?[^\d]*", subj)
        if match is not None:
            weeks_raw = regex.search(r"[^н]+н\.?", subj)[0]
            weeks_found = regex.findall(r"[0-9]+", weeks_raw)
            if 'кр' in weeks_raw:
                weeks_available = [
                    week_num for week_num in week_nums if week_num not in weeks_found]
            else:
                weeks_available = weeks_found
            if dweek == 'нечетная':
                weeks_available = [
                    week for week in weeks_available if int(week) % 2 == 1]
            else:
                weeks_available = [
                    week for week in weeks_available if int(week) % 2 == 0]
            subj_name_new = subj.lstrip(weeks_raw)
            subjects[i] = subj_name_new
            weeks.append(','.join(weeks_available))
        else:
            weeks_available = []
            if dweek == 'нечетная':
                weeks_available = [
                    week for week in week_nums if int(week) % 2 == 1]
            else:
                weeks_available = [
                    week for week in week_nums if int(week) % 2 == 0]
            weeks.append(','.join(weeks_available))
    return subjects, weeks


def concat_groups_records(recs):
    i = 0
    rec_len = len(recs)
    while i < rec_len - 1:
        recs_banned = []
        j = i
        while j < rec_len:
            if recs[i][2] == recs[j][2] and recs[i][3] == recs[j][3] and recs[i][4] == recs[j][4] \
                    and recs[i][5] == recs[j][5] and recs[i][6] == recs[j][6] and recs[i][7] == recs[j][7] \
                    and recs[i][9] == recs[j][9] and recs[i][1] != recs[j][1]:
                recs[i][1] += f", {recs[j][1]}"
                recs_banned.append(j)
            j += 1
        ban_counter = 0
        for ban in recs_banned:
            ban -= ban_counter
            recs.pop(ban)
            ban_counter += 1
            rec_len = len(recs)
        i += 1
    return recs


if __name__ == '__main__':
    test()
