import spacy
import re

nlp = spacy.load("es_core_news_sm")
STOPWORDS = set(nlp.Defaults.stop_words)

def normalize_prompt(text):
    text = text.lower()
    text = re.sub(r'[^ -\w\s]', '', text)  # quitar puntuación, mantener tildes
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.text not in STOPWORDS and not token.is_space]
    return ' '.join(tokens) 