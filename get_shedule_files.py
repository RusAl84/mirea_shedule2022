import urllib

def load_file(url, filename):
    import urllib.request
    urllib.request.urlretrieve(url, filename)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_file("https://webservices.mirea.ru/upload/iblock/b9f/1ffqlzsrdlfigrfuhwddaux81kffig22/ikts-1K-.xls","./shedule/ikts-1K-.xls")



