from bs4 import BeautifulSoup
import requests

def get_urls(url = 'https://www.mirea.ru/schedule/'):
    page = requests.get(url)
    # if page.status_code == 200:
    #     print(url + " 200")

    soup = BeautifulSoup(page.text, "html.parser")
    insts = []

    blocks = soup.findAll(True, {"class": ["uk-card", "slider_ads", "uk-card-body", "uk-card-small"]})

    urls = []
    for block in blocks:
        soup_inst = BeautifulSoup(str(block), "html.parser")
        inst = soup_inst.find_all("a", {"class": "uk-text-bold"})
        if len(inst) > 0:
            # print(inst[0].text)  # список институтов
            if inst[0].text == 'Институт кибербезопасности и цифровых технологий':
                # print(inst[0].text)
                # print(block)
                num = 1
                for link in soup_inst.find_all('a', href=True):
                    # print(link['href'])
                    if "javascript:void(0)" not in link['href']:
                        # print(link['href'])
                        url = []
                        url.append(link['href'])
                        url.append(str(num) + "-k.xls")
                        urls.append(url)
    return urls

if __name__ == '__main__':
    get_urls()