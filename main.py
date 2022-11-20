"""
# My first app
Here's our first attempt at using data to create a table:
"""
import streamlit as st
from gpt import *
import streamlit_authenticator as stauth
import yaml
from export_functions import write_pdf, write_docx
import streamlit_ext as ste


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

        sample_dict = {}
        for i, question in enumerate(questions):
            sample_dict[i+1] = {'Question': question,
                            'Correct_answers': correct_answers[i],
                            'False_answers': wrong_answers[i]}
        # print(sample_dict)
        write_docx(sample_dict, 'pytania', highlight_correct=True)
        write_pdf(sample_dict, 'pytania1', highlight_correct=True)

        with open('pytania1.pdf', "rb") as f:
            ste.download_button('Eksport pytań do pliku pdf.', data=f, file_name='pytania1.pdf')

        with open('pytania.docx', "rb") as f:
            ste.download_button('Eksport pytań do pliku docx.', data=f, file_name='pytania.docx')

#    st.download_button('Download CSV', f)
#         ste.download_button('Eksport pytań do pliku pdf.', data=write_pdf(sample_dict, '2', highlight_correct=True), file_name='pytania.pdf')

#         ste.download_button('Eksport pytań do pliku docx.', data=write_docx(sample_dict, '2', highlight_correct=True), file_name='pytania.docx')    

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
