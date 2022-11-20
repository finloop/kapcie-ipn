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
from scrap_url import get_url_from_user_input
from export_functions import *
import streamlit_ext as sxt

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
                st.session_state.input_type = "url"
            else:
                # Handle search
                if "input_type" in st.session_state and st.session_state.input_type == "search":
                    # Process checkboxes
                    st.write("Processing checkboxes.")
                st.session_state.input_type = "search"

    
    if "input_type" in st.session_state and st.session_state.input_type == "search":
        st.write("Przeszukujemy bazę danych szukaj.ipn.gov.pl. Wybierz linki, z których mamy pobrać tekst:")
        urls = [u[0] for u in get_url_from_user_input(user_input)]
        urls = list(set(urls))
        st.write("Po wybraniu artykułów skopiuj link do wyszukiwarki.")
        for url in urls:
            st.write(url)


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

            sample_dict = {}
            for i, question in enumerate(st.session_state.questions):
                sample_dict[i+1] = {'Question': question,
                                'Correct_answers': correct_answers[i],
                                'False_answers': wrong_answers[i]}
            # print(sample_dict)
            write_docx(sample_dict, 'pytania', highlight_correct=True)
            write_pdf(sample_dict, 'pytania1', highlight_correct=True)

            with open('pytania1.pdf', "rb") as f:
                sxt.download_button('Eksport pytań do pliku pdf.', data=f, file_name='pytania1.pdf')

            with open('pytania.docx', "rb") as f:
                sxt.download_button('Eksport pytań do pliku docx.', data=f, file_name='pytania.docx')


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
