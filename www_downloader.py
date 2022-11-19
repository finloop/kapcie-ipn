import requests
from readabilipy import simple_json_from_html_string
import re

def download(URL: str) -> dict:
    req = requests.get(URL)
    article = simple_json_from_html_string(req.text, use_readability=False)
    del (article["content"])
    del (article["plain_content"])
    del (article["byline"])
    del (article["date"])

    stringg = ''

    for dictionary in article['plain_text']:
        stringg =  stringg  + dictionary['text'] 

    stringg = re.sub(r'["*„”@#$%^&|\\/\=;<>\']', '', stringg)
    stringg = re.sub(r'[.]{2,}', '', stringg)
    stringg = re.sub(r'\[\d{1,}\]', '.', stringg)
    stringg = re.sub(r'–-', '', stringg)
    stringg = re.sub(r'\n', ' ', stringg)
    stringg = re.sub(r'\[…\]', ' ', stringg)
    stringg = stringg + '.'
    stringg = re.sub(r'- ', '', stringg)
    stringg = re.sub(r'\s\s+', ' ', stringg)
    
    return stringg


# print(download("https://zbrodniawolynska.pl/zw1/sledztwa/157,Sledztwo-OKSZpNP-w-Krakowie-w-sprawie-zbrodni-w-Hucie-Pieniackiej.html"))
print(download('https://ipn.gov.pl/pl/upamietnianie/oddzialowe-komitety-opw/komitet-opwim-przy-oddz-2/73888,X-posiedzenie-Komitetu-Ochrony-Pamieci-Walk-i-Meczenstwa-w-Katowicach-27-czerwca.html'))