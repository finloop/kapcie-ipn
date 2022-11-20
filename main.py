"""
# My first app
Here's our first attempt at using data to create a table:
"""


import streamlit as st
from gpt import *
import streamlit_authenticator as stauth
import yaml
from urllib.parse import urlparse
from www_downloader import download

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def download_summarized_article(text: str) -> str:
    article = ""
    with st.spinner("Skracanie tekstu..."):
        article = summarize_article(text=text)
    return article

def get_questions_single(text: str):
    # Wygeneruj pytania
    with st.spinner("Generuję pytania. Proszę czekać 🤔"):
        questions = generate_questions(text=text)
        st.write("Mam! 😋 Oto one: ")
        #for i, question in enumerate(questions):
        #    st.write(f"**{i+1}. {question.strip()}**")
        return questions


with open(".streamlit/config.yaml") as file:
    config = yaml.load(file, Loader=stauth.SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)
name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status:
    authenticator.logout("Logout", "main")
    st.write("# QuickQuiz")
    st.write(f"Zalogowano jako: *{name}*")

    user_input = st.text_area(
        "Tekst",
        placeholder="Wpisz hasło, temat, link lub fragment tekstu",
        label_visibility="hidden",
    )
    generate_new_questions = st.button("Wygeneruj pytania", type="primary")

    user_input = user_input.strip()
    if generate_new_questions:
        if len(user_input) > 200:
            st.session_state.input_type = "text"
            st.session_state.text = user_input
            questions = get_questions_single(user_input)

            if "questions" not in st.session_state:
                st.session_state.questions = []
            st.session_state.questions += questions
        elif len(user_input) > 0:
            # Check if it is a URL
            if is_url(user_input):
                st.session_state.text  = download(URL=user_input)
                st.write(f"**Taki tekst odnalazłem na podanej stronie**: {st.session_state.text}")
                questions = get_questions_single(text=str(st.session_state.text))

                if "questions" not in st.session_state:
                    st.session_state.questions = []
                st.session_state.questions += questions
            else:
                # Handle search
                st.session_state.text  = user_input
    

    if "questions" in st.session_state:
        questions_area = st.text_area(label="Zredaguj pytania lub dodaj własne. Możesz też wygenerować dodatkowe pytania. Każde pytanie pisz w nowej linii.", value="\n".join(st.session_state.questions), height=200)
        st.session_state.questions = questions_area.split("\n")
        st.write("Gdy już skończysz, kliknij \"Wygeneruj odpowiedzi\"")

        if st.button("Wygeneruj odpowiedzi", type="primary"):
             # Wygeneruj odpowiedzi
            correct_answers: dict[int, list[str]] = dict()
            wrong_answers: dict[int, list[str]] = dict()
            with st.spinner("Generuję odpowiedzi 🏃🏼‍♂️🏃🏼‍♂️🏃🏼‍♂️"):
                for i, question in enumerate(st.session_state.questions):
                    correct_answers[i] = generate_correct_answers(
                        text=st.session_state.text , question=question
                    )
                    wrong_answers[i] = generate_wrong_answers(text=st.session_state.text , question=question)

            # Wypisz wyniki
            st.write("Skończyłem 🥳🎉 oto wyniki. Możesz je zapisać jako PDF lub DOCX.")
            
            # TODO: Download buttons

            st.write("# Pytania i odpowiedzi")
            for i, question in enumerate(st.session_state.questions):
                st.write(f"### {i+1}. {question}")
                st.write(f"**Poprawne odpowiedzi:**")
                for j, ans in enumerate(correct_answers[i]):
                    st.write(f"\t{j+1}. {ans}")
                st.write(f"**Błędne odpowiedzi:**")
                for j, ans in enumerate(wrong_answers[i]):
                    st.write(f"\t{j+1}. {ans}")

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
