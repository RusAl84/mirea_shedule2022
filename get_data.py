import urllib.request

import get_shedule_files
import parsing
import get_urls
import get_empty_aud
import pandas as pd
import pickle

import urllib.parse

if __name__ == '__main__':
    urls = get_urls.get_urls('https://www.mirea.ru/schedule/')
    print(urls)
    get_shedule_files.load_all_files(urls)
    subj_records = parsing.parsing_all_files(urls)
    # save to file
    list_of_colums = ["inst", "group", "num_day", "num_subj", "week", "subj_name", "subj_type", "teach_name",
                    "aud_name", "weeks_available"]
    df = pd.DataFrame(subj_records, columns=list_of_colums)
    df.to_excel("output.xlsx")
    with open('df.pickle', 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
    get_empty_aud.get_all_aud()


