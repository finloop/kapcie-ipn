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

        random_correct = [np.random.choice(json_data[key_idx]['Correct_answers'])]

        answers = np.random.choice(np.append(random_correct, json_data[key_idx]['False_answers']),
                                   np.clip(len(json_data[key_idx]['False_answers']) + 1, 2, 4), replace=False)

        for i, answer in enumerate(answers):
            if highlight_correct and (answer == random_correct[0]):
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

    help(pdf.set_font)
    help(fpdf.fpdf.FPDF)

    for key_idx in json_data.keys():
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt=json_data[key_idx]['Question'],
                 ln=2, align='L')

        random_correct = [np.random.choice(json_data[key_idx]['Correct_answers'])]

        answers = np.random.choice(np.append(random_correct, json_data[key_idx]['False_answers']),
                                   np.clip(len(json_data[key_idx]['False_answers']) + 1, 2, 4), replace=False)

        pdf.set_font("Arial", size=10)
        for i, answer in enumerate(answers):
            if answer == random_correct[0] and highlight_correct:
                pdf.set_text_color(0, 255, 0)
                pdf.cell(40, 7, txt=f'\n{ans_idxes[i]}) {answer}',
                         ln=2, align='L')
                pdf.set_text_color(0, 0, 0)
            else:
                pdf.cell(40, 7, txt=f'\n{ans_idxes[i]}) {answer}',
                         ln=2, align='L')
    pdf_fname = output_filename + '.pdf'

    pdf.output(pdf_fname)


if __name__ == '__main__':

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

    # write_docx(sample_dict, '2', highlight_correct=True)
    # write_pdf(sample_dict, '2', highlight_correct=True)