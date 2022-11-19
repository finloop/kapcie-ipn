import requests
from readabilipy import simple_json_from_html_string
import re
def download(URL):
    req = requests.get(URL)
    article = simple_json_from_html_string(req.text, use_readability=False)
    del (article["content"])
    del (article["plain_content"])
    del (article["byline"])
    del (article["date"])
    return article

slownik = download("https://zbrodniawolynska.pl/zw1/sledztwa/157,Sledztwo-OKSZpNP-w-Krakowie-w-sprawie-zbrodni-w-Hucie-Pieniackiej.html")
#print(slownik["plain_text"])
#print(slownik["title"])
#print(slownik)
stringg = ""
list_of_char = ['-', '*','"',"''"]
pattern = '['+''.join(list_of_char)+']'
print(stringg)
for i in slownik["plain_text"]:
    print(i["text"])
    strr = i["text"]
    strr += ". "
    stringg += strr
mod_string = re.sub(pattern, '', stringg)
print(mod_string)
#print(download('https://kop.ipn.gov.pl/kop/multimed/materialy-audio/relacje-i-wspomnienia/8533,Stanislaw-Ratajski.html'))

'''from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_url_from_user_input(user_input):
    url = "https://szukaj.ipn.gov.pl/search?q="+user_input+"&site=&btnG=Szukaj&client=default_frontend&output=xml_no_dtd&proxystylesheet=default_frontend&sort=date%3AD%3AL%3Ad1&wc=200&wc_mc=1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&tlen=200&size=50"
    soup = BeautifulSoup(urlopen(url),'html.parser')
    url_and_type_table = []
    for a in soup.select(".res-item a")[:10]:
        reg = a['href'].split(".")
        if reg[-1]=="html" or reg[-1]=="pdf" or reg[-1]=="docx":
            url_and_type_table.append([a['href'], reg[-1]])
    return url_and_type_table


what_you_are_looking_for = input("What you are looking for:")
get = get_url_from_user_input(what_you_are_looking_for)
for i in get:
    print(i)'''