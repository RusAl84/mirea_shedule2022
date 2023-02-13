import urllib
import ssl

def load_file(url, filename):
    import urllib.request
    import requests
    r = requests.head(url)
    if r.status_code == 200:
        urllib.request.urlretrieve(url, filename)


def load_all_files(urls):
    ssl._create_default_https_context = ssl._create_unverified_context
    for item_url in urls:
        load_file(item_url[0], "./shedule/" + item_url[1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_all_files()
