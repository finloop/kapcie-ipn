from PyPDF2 import PdfReader
import requests
import os
# from scrap_url import get_url_from_user_input
import re

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

    text = text[0: character_limit-1]
    last_occurence_of_dot = text.rfind('.')
    text = text[0: last_occurence_of_dot+1]

    os.remove("myfile.pdf")

    return text

# print(get_content_of_pdf('https://przystanekhistoria.pl/pa2/tematy/adolf-hitler/43381,Hitler-i-Stalin-zywoty-rownolegle.pdf'))
# print(len(get_content_of_pdf('https://przystanekhistoria.pl/pa2/tematy/adolf-hitler/43381,Hitler-i-Stalin-zywoty-rownolegle.pdf').split()))
# print(get_content_of_pdf('https://martyrologiawsipolskich.pl/download/151/170815/Kielecczyzna19391945stratyBROSZURA.doc'))
