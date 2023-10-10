from bs4 import BeautifulSoup
import requests
import urllib.parse


def get_urls(url):
    page = requests.get(url)
    # if page.status_code == 200:
    #     print(url + " 200")

    soup = BeautifulSoup(page.text, "html.parser")
    insts = []
    
    # /html/body/div[2]/div[2]/div/div/div[2]/div[4]/div[1]/div/ul[2]/li[1]/div/div[4]/div
    #tab-content > li.uk-active > div > div:nth-child(4) > div
    # <div class="uk-card slider_ads uk-card-body uk-card-small">
    blocks = soup.findAll(True, {"class": ["uk-card", "slider_ads", "uk-card-body", "uk-card-small"]})

    urls = []
    num_inst = 0
    for block in blocks:
        soup_inst = BeautifulSoup(str(block), "html.parser")
        inst = soup_inst.find_all("a", {"class": "uk-text-bold"})
        if len(inst) > 0:
            # print(inst[0].text)  # список институтов

            # if inst[0].text == 'Институт кибербезопасности и цифровых технологий' \
            #         or inst[0].text == 'Институт перспективных технологий и индустриального программирования' \
            #         or inst[0].text == 'Институт технологий управления':
            if inst[0].text == 'Институт перспективных технологий и индустриального программирования':
                num_inst += 1
                num = 1
                for link in soup_inst.find_all('a', href=True):
                    # print(link['href'])
                    if "javascript:void(0)" not in link['href']:
                        # print(link['href'])
                        url = []
                        url.append(link['href'])
                        url.append(str(num_inst) + "_" + str(num) + "_k_osen_22_23.xls")
                        url.append(inst[0].text)
                        num += 1
                        if "pdf" not in link['href']:
                            urls.append(url)
                            # print(url)
    return urls


if __name__ == '__main__':
    url="https://www.mirea.ru/schedule/"
    print(get_urls(url))
