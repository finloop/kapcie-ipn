import os
import openai
import logging
import re

logging.getLogger()

openai.api_key = 'api-key'

def summarize_article(text: str) -> str:
    try:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"""Podsumuj poniższy tekst w języku polskim.

{text}

""",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response["choices"][0]["text"].strip()
    except Exception:
        print("Błąd!")
        logging.exception("Błąd")
        return ""


def select_not_empty(data: list[str]) -> list[str]:
    data = list(set(data))
    if "" in data:
        data.remove("")
    return data


def trim_answer(answer: str) -> str:
    reg = r"\d[.)]\s"
    if re.match(reg, answer):
        answer = answer[3:]
    return answer


def generate_questions(text: str) -> list[str]:
    try:
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=f"""Dla podanego tekstu napisz 6 pytań.
Tekst: {text}

""",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        questions = [
            trim_answer(question)
            for question in response["choices"][0]["text"].split("\n")
        ]
        return select_not_empty(questions)
    except Exception:
        logging.exception("Błąd")
        return []


def generate_correct_answers(text: str, question: str) -> list[str]:
    try:
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=f"""Tekst: {text}
Pytanie: {question}

Podaj 3 poprawne odpowiedzi na powyższe pytanie.

    """,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        correct_answers = [
            trim_answer(ans) for ans in response["choices"][0]["text"].split("\n")
        ]
        return select_not_empty(correct_answers)
    except Exception:
        return []


def generate_wrong_answers(text: str, question: str) -> list[str]:
    try:
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=f"""Tekst: {text}
Pytanie: {question}

Podaj trzy niepoprawne odpowiedzi.

    """,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        correct_answers = [
            trim_answer(ans) for ans in response["choices"][0]["text"].split("\n")
        ]
        return select_not_empty(correct_answers)
    except Exception:
        return []


if __name__ == "__main__":
    text = input("Podaj tekst: ")
    print(text)

    # Wygeneruj pytania
    print("Generuję pytania. Proszę czekać 🤔")
    questions = generate_questions(text=text)
    print("Mam! 😋 Oto one: ")
    for i, question in enumerate(questions):
        print(f"{i+1}. {question}")

    # Wygeneruj odpowiedzi
    correct_answers: dict[int, list[str]] = dict()
    wrong_answers: dict[int, list[str]] = dict()
    print("Generuję odpowiedzi 🏃🏼‍♂️🏃🏼‍♂️🏃🏼‍♂️")
    for i, question in enumerate(questions):
        correct_answers[i] = generate_correct_answers(text=text, question=question)
        wrong_answers[i] = generate_wrong_answers(text=text, question=question)

    # Wypisz wyniki
    print("Skończyłem 🥳🎉 oto wyniki:")
    for i, question in enumerate(questions):
        print(f"{i+1}. {question}")
        print(f"\tPoprawne odpowiedzi:")
        for j, ans in enumerate(correct_answers[i]):
            print(f"\t{j+1}. {ans}")
        print(f"\tBłędne odpowiedzi:")
        for j, ans in enumerate(wrong_answers[i]):
            print(f"\t{j+1}. {ans}")
