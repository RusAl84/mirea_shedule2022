import urllib


def load_file(url, filename):
    import urllib.request
    urllib.request.urlretrieve(url, filename)

def load_all_files():
    urls = [["https://webservices.mirea.ru/upload/iblock/b9f/1ffqlzsrdlfigrfuhwddaux81kffig22/ikts-1K-.xls",
             "ikts-1K-.xls"],
            ["https://webservices.mirea.ru/upload/iblock/7d1/rfruyo6rz2sljq9qz9k2fcco248jaw8s/IKTST-2k.xls",
             "IKTST-2k.xls"],
            [
                "https://webservices.mirea.ru/upload/iblock/1e9/5q85fces7rll3lb131dwv03ln5kqjr7v/IKTST-3-k.xls",
                "IKTST-3-k.xls"],
            ["https://webservices.mirea.ru/upload/iblock/b8f/qvb2m42wqi7zu4h6cdg7k3m7uveip7o5/IKTST-4-k.xls",
             "IKTST-4-k.xls"],
            ["https://webservices.mirea.ru/upload/iblock/14c/kkk53zx3zxk37b9ivuowt2qgalkkrr8r/IKTST-5-k.xls",
             "IKTST-5-k.xls"]
            ]
    for item_url in urls:
        load_file(item_url[0], "./shedule/"+item_url[1])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_all_files()
