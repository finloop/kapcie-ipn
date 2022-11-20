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

        answers = np.random.choice(np.append(random_correct[0], json_data[key_idx]['False_answers'][:3]),
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

    for key_idx in json_data.keys():
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt=pdf.normalize_text(json_data[key_idx]['Question']).encode('latin-1', 'ignore').decode('latin-1'),
                 ln=2, align='L')

        random_correct = [np.random.choice(json_data[key_idx]['Correct_answers'])]

        answers = np.random.choice(np.append(random_correct[0], json_data[key_idx]['False_answers'][:3]),
                                   np.clip(len(json_data[key_idx]['False_answers']) + 1, 2, 4), replace=False)

        pdf.set_font("Arial", size=10)
        for i, answer in enumerate(answers):
            if answer == random_correct[0] and highlight_correct:
                pdf.set_text_color(0, 255, 0)
                pdf.cell(40, 7, txt=pdf.normalize_text(f"\n{ans_idxes[i]}) {answer.encode('latin-1', 'ignore').decode('latin-1')}"),
                         ln=2, align='L')
                pdf.set_text_color(0, 0, 0)
            else:
                pdf.cell(40, 7, txt=pdf.normalize_text(f"\n{ans_idxes[i]}) {answer.encode('latin-1', 'ignore').decode('latin-1')}"),
                         ln=2, align='L')
    pdf_fname = output_filename + '.pdf'

    pdf.output(pdf_fname, 'F')
