from PyPDF2 import PdfReader
import requests

response = requests.get("https://przystanekhistoria.pl/pa2/tematy/adolf-hitler/43381,Hitler-i-Stalin-zywoty-rownolegle.pdf")
file = open("myfile.pdf", "wb")
file.write(response.content)
file.close()

def get_content_of_pdf(pdf_path: str) -> list:

    response = requests.get(
        "https://przystanekhistoria.pl/pa2/tematy/adolf-hitler/43381,Hitler-i-Stalin-zywoty-rownolegle.pdf")

    file = open("myfile.pdf", "wb")
    file.write(response.content)
    file.close()

    reader = PdfReader("myfile.pdf")
    number_of_pages = len(reader.pages)

    text = []

    for i in range(number_of_pages):
        page = reader.pages[i]
        new_text = page.extract_text()
        text.append(new_text)
    text = "".join(text)


    return text

print(get_content_of_pdf('https://przystanekhistoria.pl/pa2/tematy/adolf-hitler/43381,Hitler-i-Stalin-zywoty-rownolegle.pdf'))

