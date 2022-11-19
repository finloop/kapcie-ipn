from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

def get_url_from_user_input(user_input):
    url = "https://szukaj.ipn.gov.pl/search?q=" + user_input + "&site=&btnG=Szukaj&client=default_frontend&output=xml_no_dtd&proxystylesheet=default_frontend&sort=date%3AD%3AL%3Ad1&wc=200&wc_mc=1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&tlen=200&size=50"
    req = requests.get(url)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')
    url_and_type_table = []
    for a in soup.select(".res-item a")[:10]:
        reg = a['href'].split(".")
        if reg[-1]=="html" or reg[-1]=="pdf" or reg[-1]=="docx":
            url_and_type_table.append([a['href'], reg[-1]])
    return url_and_type_table


# if __name__ == '__main__':
#     what_you_are_looking_for = input("What you are looking for:")
#     print(get_url_from_user_input(what_you_are_looking_for))
# print(get_url_from_user_input('gierek'))
