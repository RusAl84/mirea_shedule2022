import get_shedule_files
import parsing
import get_urls
import get_empty_aud

if __name__ == '__main__':
    urls = get_urls.get_urls()
    print(urls)
    get_shedule_files.load_all_files(urls)

    subj_records = parsing.parsing_all_files(urls)
    get_empty_aud.get_all_aud()

