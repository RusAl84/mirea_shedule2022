import urllib


def load_file(url, filename):
    import urllib.request
    import requests
    r = requests.head(url)
    if r.status_code == 200:
        urllib.request.urlretrieve(url, filename)


def load_all_files(urls):
    for item_url in urls:
        print(item_url[0])
        load_file(item_url[0], "./shedule/" + item_url[1])   


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_all_files()
