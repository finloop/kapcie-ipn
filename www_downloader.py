import requests
from readabilipy import simple_json_from_html_string
import re
from PyPDF2 import PdfReader
import requests
import os
# from scrap_url import get_url_from_user_input


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

# links_to_pdfs = get_url_from_user_input('piłsudzki')
# print(links_to_pdfs)
character_limit = 2000


def get_content_of_pdf(pdf_path: str) -> list:
    # download pdf
    response = requests.get(pdf_path)

    # make temp pdf file
    file = open("myfile.pdf", "wb")
    file.write(response.content)
    file.close()

    # take content of pdf
    reader = PdfReader("myfile.pdf")
    number_of_pages = len(reader.pages)

    text = ''

    for i in range(number_of_pages):
        page = reader.pages[i]
        new_text = page.extract_text()
        text = text + new_text

    text = re.sub(r'["*„”@#$%^&|\\/-\=;<>\']', '', text)
    text = re.sub(r'[.]{2,}', '', text)
    text = re.sub(r'–', '', text)
    text = re.sub(r'\[\d{1,}\]', '.', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\[…\]', ' ', text)
    text = text + '.'
    text = re.sub(r'\s\s+', ' ', text)

    text = text[0: character_limit - 1]
    last_occurence_of_dot = text.rfind('.')
    text = text[0: last_occurence_of_dot + 1]

    os.remove("myfile.pdf")

    return text


# print(download("https://zbrodniawolynska.pl/zw1/sledztwa/157,Sledztwo-OKSZpNP-w-Krakowie-w-sprawie-zbrodni-w-Hucie-Pieniackiej.html"))
print(download('https://zbrodniawolynska.pl/zw1/sledztwa/157,Sledztwo-OKSZpNP-w-Krakowie-w-sprawie-zbrodni-w-Hucie-Pieniackiej.html'))