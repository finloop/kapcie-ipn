"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
from gpt import *

def download_summarized_article(text: str) -> str:
    article = ""
    with st.spinner('Skracanie tekstu...'):
        article = summarize_article(text=text)
    return article

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
