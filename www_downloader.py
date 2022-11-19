import requests
from readabilipy import simple_json_from_html_string
import re

character_limit = 2000

def download(URL: str) -> dict:
    req = requests.get(URL)
    article = simple_json_from_html_string(req.text, use_readability=False)
    del (article["content"])
    del (article["plain_content"])
    del (article["byline"])
    del (article["date"])

    text = ''

    for dictionary in article['plain_text']:
        text =  text  + dictionary['text'] 

    text = re.sub(r'["*„”@#$%^&|\\/\=;<>\']', '', text)
    text = re.sub(r'[.]{2,}', '', text)
    text = re.sub(r'\[\d{1,}\]', '.', text)
    text = re.sub(r'–-', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\[…\]', ' ', text)
    text = text + '.'
    text = re.sub(r'- ', '', text)
    text = re.sub(r'\s\s+', ' ', text)
    
    text = text[0: character_limit-1]
    last_occurence_of_dot = text.rfind('.')
    text = text[0: last_occurence_of_dot+1]

    return text


# print(download("https://zbrodniawolynska.pl/zw1/sledztwa/157,Sledztwo-OKSZpNP-w-Krakowie-w-sprawie-zbrodni-w-Hucie-Pieniackiej.html"))
# print(download('https://ipn.gov.pl/pl/upamietnianie/oddzialowe-komitety-opw/komitet-opwim-przy-oddz-2/73888,X-posiedzenie-Komitetu-Ochrony-Pamieci-Walk-i-Meczenstwa-w-Katowicach-27-czerwca.html'))
