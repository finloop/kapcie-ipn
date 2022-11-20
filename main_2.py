"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
from gpt import *
from export_functions import write_docx, write_pdf
from pdf_www_for import *
def download_summarized_article(text: str) -> str:
    article = ""
    with st.spinner('Skracanie tekstu...'):
        article = summarize_article(text=text)
    return article


# streamlit_app.py

import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
                st.session_state["username"] in st.secrets["passwords"]
                and st.session_state["password"]
                == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():

    st.write("# QuickQuiz")
    user_input_pre = st.text_area("Tekst_2", placeholder="Wpisz słowa kluczowe/zdanie/fakt", label_visibility="hidden")
    url_ki = get_url_from_user_input(user_input_pre)
    for i in url_ki:
        if i[1] == 'pdf':
            pdff = get_content_of_pdf(i[0])
            user_input = pdff

        else:
            wwww = download(i[0])
            user_input = wwww

        if len(user_input) > 10:
            text = user_input
            # Wygeneruj pytania
            with st.spinner("Generuję pytania. Proszę czekać 🤔"):
                questions = generate_questions(text=text)
                st.write("Mam! 😋 Oto one: ")
                for i, question in enumerate(questions):
                    st.write(f"**{i + 1}. {question.strip()}**")

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
                    st.write(f"## {i + 1}. {question}")
                    st.write(f"**Poprawne odpowiedzi:**")
                    for j, ans in enumerate(correct_answers[i]):
                        st.write(f"\t{j + 1}. {ans}")
                    st.write(f"**Błędne odpowiedzi:**")
                    for j, ans in enumerate(wrong_answers[i]):
                        st.write(f"\t{j + 1}. {ans}")

    if st.button('Eksport pytań do pliku pdf.'):
        st.write('Tworzenie pliku pdf.')
        # write_pdf(sample_dict, '2', highlight_correct=True)

    if st.button('Eksport pytań do pliku docx.'):
        st.write('Tworzenie pliku docx.')
        # write_docx(sample_dict, '2', highlight_correct=True)