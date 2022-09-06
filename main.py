import get_shedule_files
import parsing
import get_urls

if __name__ == '__main__':
    urls = get_urls.get_urls()
    print(urls)
    get_shedule_files.load_all_files(urls)

    parsing.parsing_all_files(urls)

