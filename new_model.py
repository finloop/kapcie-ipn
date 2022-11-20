# !pip install --upgrade git+https://github.com/ramsrigouthamg/Questgen.ai
# !pip install --quiet git+https://github.com/boudinfl/pke.git@69337af9f9e72a25af6d7991eaa9869f1322dd72
# !python -m nltk.downloader universal_tagset
# !python -m spacy download en
# !wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
# !tar -xvf  s2v_reddit_2015_md.tar.gz

import nltk
nltk.download('stopwords')
from Questgen import main
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

en_pl_tokenizer = AutoTokenizer.from_pretrained("gsarti/opus-mt-tc-en-pl")
pl_en_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-pl-en")

en_pl_model = AutoModelForSeq2SeqLM.from_pretrained("gsarti/opus-mt-tc-en-pl")
pl_en_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-pl-en")

en_pl_pipe = pipeline('translation', model=en_pl_model, tokenizer=en_pl_tokenizer)
pl_en_pipe = pipeline('translation', model=pl_en_model, tokenizer=pl_en_tokenizer)


class MCQModel:

    def __init__(self):
        self.en_pl_tokenizer = AutoTokenizer.from_pretrained("gsarti/opus-mt-tc-en-pl")
        self.pl_en_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-pl-en")

        self.en_pl_model = AutoModelForSeq2SeqLM.from_pretrained("gsarti/opus-mt-tc-en-pl")
        self.pl_en_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-pl-en")

        self.en_pl_pipe = pipeline('translation', model=en_pl_model, tokenizer=en_pl_tokenizer)
        self.pl_en_pipe = pipeline('translation', model=pl_en_model, tokenizer=pl_en_tokenizer)

        self.qg = main.QGen()

    def pl_translate_en(self, text):
        return self.pl_en_pipe(text)[0]['translation_text']

    def en_translate_pl(self, text):
        return self.en_pl_pipe(text)[0]['translation_text']

    def predict(self, text):

        return_dict = {}
        c_idx = 1

        text_splited = text.split('.')[:-1]

        for single_text in text_splited:

            payload = {
                "input_text": self.pl_translate_en(single_text)
            }
            output = self.qg.predict_mcq(payload)

            for question in output['questions']:
                question_stetment = self.en_translate_pl(question['question_statement'])

                answer = [self.en_translate_pl(question['answer'])]

                options = [self.en_translate_pl(i) for i in question['options']]

                return_dict[str(c_idx)] = {
                    'Question': question_stetment,
                    'Correct_answers': answer,
                    'False_answers': options}

                c_idx += 1

            return return_dict
