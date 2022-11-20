# pip install fpdf
# pip install docx
# pip install numpy

from fpdf import FPDF
from docx import Document
import numpy as np
from docx.shared import RGBColor
import fpdf


def write_docx(json_data, output_filename, highlight_correct=False):

    document = Document()
    ans_idxes = ['a', 'b', 'c', 'd']

    for key_idx in json_data.keys():

        p = document.add_paragraph(json_data[key_idx]['Question'])

        random_correct = json_data[key_idx]['Correct_answers']

        answers = np.random.choice(np.append(random_correct, json_data[key_idx]['False_answers'][:(4 - len(random_correct))]),
                                   np.clip(len(json_data[key_idx]['False_answers']) + 1, 2, 4), replace=False)

        for i, answer in enumerate(answers):
            if np.isin(answer, random_correct) and highlight_correct:
                run = p.add_run(f'\n\t{ans_idxes[i]}) {answer}')
                run.font.color.rgb = RGBColor(0x00, 0xFF, 0x00)
            else:
                run = p.add_run(f'\n\t{ans_idxes[i]}) {answer}')
                run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    document.add_page_break()

    docx_fname = output_filename + '.docx'

    document.save(docx_fname)


def write_pdf(json_data, output_filename, highlight_correct=False):

    pdf = FPDF()

    ans_idxes = ['a', 'b', 'c', 'd']

    pdf.add_page()

    pdf.set_font("Arial", size=15)

    for key_idx in json_data.keys():
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt=pdf.normalize_text(json_data[key_idx]['Question']),
                 ln=2, align='L')

        random_correct = json_data[key_idx]['Correct_answers']

        answers = np.random.choice(np.append(random_correct, json_data[key_idx]['False_answers'][:(4 - len(random_correct))]),
                                   np.clip(len(json_data[key_idx]['False_answers']) + 1, 2, 4), replace=False)

        pdf.set_font("Arial", size=10)
        for i, answer in enumerate(answers):
            if np.isin(answer, random_correct) and highlight_correct:
                pdf.set_text_color(0, 255, 0)
                pdf.cell(40, 7, txt=pdf.normalize_text(f"\n{ans_idxes[i]}) {answer}"),
                         ln=2, align='L')
                pdf.set_text_color(0, 0, 0)
            else:
                pdf.cell(40, 7, txt=pdf.normalize_text(f"\n{ans_idxes[i]}) {answer}"),
                         ln=2, align='L')
    pdf_fname = output_filename + '.pdf'

    pdf.output(pdf_fname)


if __name__ == '__main__':

    """
    sample_dict = {'1': {'Question': "Testowe pytanie?",
                         'Correct_answers': ["Poprawna :)"],
                         'False_answers': ["Nie poprawna 1", "Nie poprawna 2", "Nie poprawna 3"]},
                   '2': {'Question': "Testowe pytanie 2?",
                         'Correct_answers': ["Poprawna :)"],
                         'False_answers': ["Nie poprawna 1", "Nie poprawna 2", "Nie poprawna 3"]},
                   '3': {'Question': "Testowe pytanie 3?",
                         'Correct_answers': ["Tak"],
                         'False_answers': ["Nie"]}

                   }
    """

    sample_dict = {1: {'Question': 'W jakim czasie zakończyła się II wojna światowa? ',
                       'Correct_answers': ['1949, 1955, 1979.'],
                       'False_answers': ['2 września 1945 roku – kapitulacja Japonii.', '9 maja 1945 roku – wejście w życie aktu bezwarunkowej kapitulacji III Rzeszy.', '8 maja 1945 roku – podpisanie aktu bezwarunkowej kapitulacji III Rzeszy.']},
                   2: {'Question': 'Czy była to jedna wielka wojna?', 'Correct_answers': ['Wojna była wielką, ale nie jedną wielką wojną.', 'Wojna była wielką, ale nie jedną wielką wojną ojczyźnianą.', 'Wojna była wielką, ale nie jedną wielką wojną światową.'],
                       'False_answers': ['      ', 'była to jedna wielka wojna, ale liczba stron miała inną skalę.', 'była to jedna wielka wojna, ale różnice w liczebnościach żołnierzy i ofiar były duże;', 'była to jedna wielka wojna, choć podział na strony miał inną skalę;']},
                   3: {'Question': 'Jaką liczbę ludzi zginęło w II wojnie światowej? ', 'Correct_answers': [' 1,7 mln ludzi zginęło w II wojnie światowej.', '2,0 mln ludzi zginęło w II wojnie światowej.', '3,0 mln ludzi zginęło w II wojnie światowej.'],
                       'False_answers': ['Odpowiedź 2:', '  Wszystkie szacunki na ten temat są nieprawdziwe.', 'Odpowiedź 3:', 'Według szacunków zginęło w niej od 50 do 78 milionów ludzi.', 'Odpowiedź 1:']},
                   4: {'Question': 'Czy wojna była trwała dwukrotnie w Europie? ', 'Correct_answers': ['Tak, wojna trwała dwukrotnie w Europie.', 'Tak, wojna była trwała dwukrotnie w Europie.'],
                       'False_answers': ['     ', 'Według różnych szacunków zginęło w niej od 50[2] do 78[3] milionów ludzi.']},
                   5: {'Question': 'Jaką rolę wojennej w II wojnie światowej odgrywała Europa? ',
                       'Correct_answers': [' Europa była głównym obszarem działań wojennych w II wojnie światowej. Wojna objęła prawie całą Europę, wschodnią i południowo-wschodnią Azję, północną Afrykę, część Bliskiego Wschodu, wyspy Oceanii i wszystkie oceany. Do walki przystąpiło 1,7 mld ludzi.'],
                       'False_answers': ['Europa była głównym częścią obszaru działań wojennych wojny.', '  1. Europa była jednym z głównych obszarów działań wojennych wojny.', 'Europa była głównym stroną konfliktu.']},
                   6: {'Question': 'Czy zginęło w niej wszystkich, czy tylko część ludzi? ',
                       'Correct_answers': ['Wszystkich zginęło.', 'Część ludzi zginęła, ale wszystkich nie zabiła. ', ' Część ludzi zginęła, ale wszystkich nie zabiła. '],
                       'False_answers': [' 1. Według różnych szacunków zginęło w niej od 50[2] do 78[3] milionów ludzi.', 'Według różnych szacunków zginęło w niej od 50[2] do 78[3] milionów ludzi.']}}


    write_docx(sample_dict, '2', highlight_correct=True)
    write_pdf(sample_dict, '2', highlight_correct=True)
