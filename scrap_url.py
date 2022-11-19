import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_url_from_user_input(user_input):
    url = "https://szukaj.ipn.gov.pl/search?q="+user_input+"&site=&btnG=Szukaj&client=default_frontend&output=xml_no_dtd&proxystylesheet=default_frontend&sort=date%3AD%3AL%3Ad1&wc=200&wc_mc=1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&tlen=200&size=50"
    soup = BeautifulSoup(urlopen(url),'html.parser')
    # items = soup.find_all("div",{"class":["res-item"]}).find('href')
    url_and_type_table = []
    for a in soup.select(".res-item a")[:10]:
        get_extension = re.search("(pdf|docx|html)",a['href'])
        url_and_type_table.append([a['href'],get_extension.group(1)])
    for i in url_and_type_table:
        print(i)

if __name__ == '__main__':
    what_you_are_looking_for = input("What you are looking for: ")
    get_url_from_user_input(what_you_are_looking_for)
