from bs4 import BeautifulSoup
import requests
url = 'https://www.mirea.ru/schedule/'
page = requests.get(url)
#Проверим подключение:
if page.status_code==200:
    print(url + " 200")

#Самое время воспользоваться BeautifulSoup4 и скормить ему наш page,
#указав в кавычках как он нам поможет 'html.parcer':
soup = BeautifulSoup(page.text, "html.parser")
#Если попросить его показать, что он там сохранил:
#print(soup)

# #Теперь воспользуемся функцией поиска в BeautifulSoup4:
# news = soup.findAll('a', class_='lenta')
insts=[]
# print(soup)
insts = soup.findAll('a', class_='uk-text-bold')
# insts = soup.findAll('a.uk-text-bold')
# print(insts)
for inst in insts:
    inst_name = inst.renderContents().decode("utf-8")
    # print(inst_name)
    if inst_name == "Институт кибербезопасности и цифровых технологий":
        print("fd")
        print(inst)
# for news_item in news:
#     if news_item.find('span', class_='time2 time3') is not None:
#         new_news.append(news_item.text)
#
# print(f"{news_item =}")