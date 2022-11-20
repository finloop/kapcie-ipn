from urllib.request import urlopen
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import os
import re
import requests
from readabilipy import simple_json_from_html_string

def get_url_from_user_input(user_input):
    url = "https://szukaj.ipn.gov.pl/search?q=" + user_input + "&site=&btnG=Szukaj&client=default_frontend&output=xml_no_dtd&proxystylesheet=default_frontend&sort=date%3AD%3AL%3Ad1&wc=200&wc_mc=1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&tlen=200&size=50"
    req = requests.get(url)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')
    url_and_type_table = []
    for a in soup.select(".res-item a")[:20]:
        reg = a['href'].split(".")
        if reg[-1]=="html" or reg[-1]=="pdf" or reg[-1]=="docx":
            url_and_type_table.append([a['href'], reg[-1]])
    return url_and_type_table

# if __name__ == '__main__':
#     what_you_are_looking_for = input("What you are looking for:")
#     print(get_url_from_user_input(what_you_are_looking_for))

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
        text = text + dictionary['text']

    text = re.sub(r'["*„”@#$%^&|\\/\=;<>\']', '', text)
    text = re.sub(r'[.]{2,}', '', text)
    text = re.sub(r'\[\d{1,}\]', '.', text)
    text = re.sub(r'–-', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\[…\]', ' ', text)
    text = text + '.'
    text = re.sub(r'- ', '', text)
    text = re.sub(r'\s\s+', ' ', text)

    text = text[0: character_limit - 1]
    last_occurence_of_dot = text.rfind('.')
    text = text[0: last_occurence_of_dot + 1]

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

url_ki = get_url_from_user_input('Protesty górników')
for i in url_ki:
    if i[1] == 'pdf':
        print(get_content_of_pdf(i[0]))
        print("\n")
    else:
        print(download(i[0]))
        print("\n")

print(len(url_ki))