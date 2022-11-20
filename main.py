"""
# My first app
Here's our first attempt at using data to create a table:
"""

from fpdf import FPDF
from docx import Document
import numpy as np
from docx.shared import RGBColor
import fpdf
import streamlit as st
from gpt import *
import streamlit_authenticator as stauth
import yaml

# from export_functions import write_docx, write_pdf

### to delete!
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
### to delete!!!

def download_summarized_article(text: str) -> str:
    article = ""
    with st.spinner('Skracanie tekstu...'):
        article = summarize_article(text=text)
    return article

# streamlit_app.py

with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=stauth.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    
    st.write("# QuickQuiz")
    user_input = st.text_area("Tekst",placeholder="Wpisz tekst do wygenerowania quizu", label_visibility="hidden")

    if len(user_input) > 10:
        text = user_input
        # Wygeneruj pytania
        with st.spinner("Generuję pytania. Proszę czekać 🤔"):
            questions = generate_questions(text=text)
            st.write("Mam! 😋 Oto one: ")
            for i, question in enumerate(questions):
                st.write(f"**{i+1}. {question.strip()}**")

        # Wygeneruj odpowiedzi
        correct_answers: dict[int, list[str]] = dict()
        wrong_answers: dict[int, list[str]] = dict()
        with st.spinner("Generuję odpowiedzi 🏃🏼‍♂️🏃🏼‍♂️🏃🏼‍♂️"):
            for i, question in enumerate(questions):
                correct_answers[i] = generate_correct_answers(text=text, question=question)
                wrong_answers[i] = generate_wrong_answers(text=text, question=question)

        # Wypisz wyniki
        with st.spinner("Skończyłem 🥳🎉 oto wyniki:"):
            for i, question in enumerate(questions):
                st.write(f"## {i+1}. {question}")
                st.write(f"**Poprawne odpowiedzi:**")
                for j, ans in enumerate(correct_answers[i]):
                    st.write(f"\t{j+1}. {ans}")
                st.write(f"**Błędne odpowiedzi:**")
                for j, ans in enumerate(wrong_answers[i]):
                    st.write(f"\t{j+1}. {ans}")

    if st.button('Eksport pytań do pliku pdf.'):
        # write_pdf(sample_dict, '2', highlight_correct=True)
        st.write('Wygenerowano plik pdf.')

    if st.button('Eksport pytań do pliku docx.'):
        # write_docx(sample_dict, '2', highlight_correct=True)
        st.write('Wygenerowano plik docx.')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


    

