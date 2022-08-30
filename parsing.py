import pandas as pd


def parsing_file(filename):
    # filename = "./shedule/ikts-1K-.xls"
    xl = pd.ExcelFile(filename)
    sheets = xl.sheet_names
    subj_records = []
    for sheet in sheets:
        df = xl.parse(sheet)
        # group1 = df.iloc[0, 5]
        # print(group1)
        # group2 = df.iloc[0, 10]
        # print(group2)
        # even_week_lines = range(2, 2, 72)
        # odd_week_lines = range(3, 2, 73)

        for num_day in range(6):
            for num_subj in range(6):
                for week in range(2):
                    for group_col_num in range(0, 6, 5):
                        line = num_day * 6 + num_subj + 2
                        # print(line)
                        group = df.iloc[0, 5 + group_col_num]
                        subj_name = df.iloc[line, 5 + group_col_num]
                        subj_type = df.iloc[line, 6 + group_col_num]
                        teach_name = df.iloc[line, 7 + group_col_num]
                        aud_name = df.iloc[line, 8 + group_col_num]
                        subj_record = []
                        subj_record.append(group)
                        subj_record.append(num_day)
                        subj_record.append(num_subj)
                        subj_record.append(week)
                        subj_record.append(subj_name)
                        subj_record.append(subj_type)
                        subj_record.append(teach_name)
                        subj_record.append(aud_name)
                        subj_records.append(subj_record)
    # print(subj_records)
    return subj_records


def parsing_all_files(filenames):
    subj_records = []
    for filename in filenames:
        subj_record = parsing_file("./shedule/" + filename)
        for item in subj_record:
            subj_records.append(item)
    # save to file
    list_of_colums = ["group", "num_day", "num_subj", "week", " subj_name", "subj_type", "teach_name", "aud_name"]
    df = pd.DataFrame(subj_records, columns=list_of_colums)
    # print(df)
    df.to_excel("output.xlsx")


if __name__ == '__main__':
    filenames = [
        "ikts-1K-.xls",
        "IKTST-2k.xls",
        "IKTST-3-k.xls",
        "IKTST-4-k.xls",
        "IKTST-5-k.xls"
    ]
    parsing_all_files(filenames)
