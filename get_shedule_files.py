import urllib

def load_file(url, filename):
    import urllib.request
    urllib.request.urlretrieve(url, filename)


def load_all_files(urls):
    for item_url in urls:
        load_file(item_url[0], "./shedule/" + item_url[1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_all_files()
