import get_shedule_files
import parsing

if __name__ == '__main__':
    # print_hi('PyCharm')
    # for group_col_num in range(0, 6, 5):
    #     print(group_col_num)
    urls = [["https://webservices.mirea.ru/upload/iblock/173/ahnk7937c2lon8u8m48s1a97uaqye7vm/1-kurs-IKB-pyatnitsa-nechet.xls",
             "1K.xls"],
            ["https://webservices.mirea.ru/upload/iblock/499/9uhqf0wm1na1v020a0gn5zar6856b7vf/2_kurs_IKB_pyatnitsa_nechet.xls",
             "2k.xls"],
            ["https://webservices.mirea.ru/upload/iblock/7a3/5mj5kxlbmtx5tehfk4gk9c9muwk220db/3-kurs-IKB-pyatnitsa-nechet.xls",
            "3k.xls"],
            ["https://webservices.mirea.ru/upload/iblock/a44/23et1pvdcwn4zonu57qudt63m9tbcqjf/4_kurs_IKB_pyatnitsa_nechet.xls",
             "4k.xls"],
            ["https://webservices.mirea.ru/upload/iblock/553/8941gvzxzh0wnoyijohdv3f5nyka9izn/5-kurs-IKB-pyatnitsa-nechet.xls",
             "5k.xls"]
            ]
    get_shedule_files.load_all_files(urls)
    filenames = []
    for item_urls in urls:
        filenames.append(item_urls[1])

    parsing.parsing_all_files(filenames)

