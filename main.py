import get_shedule_files
import parsing
import get_urls

if __name__ == '__main__':
    urls = get_urls.get_urls()
    print(urls)
    # urls2=[]
    # for ur in urls:
    #     if "mag" not in ur[0]:
    #         urls2.append(ur)
    # get_shedule_files.load_all_files(urls2)
    get_shedule_files.load_all_files(urls)

    filenames = []
    for item_urls in urls:
        filenames.append(item_urls[1])

    parsing.parsing_all_files(filenames)

