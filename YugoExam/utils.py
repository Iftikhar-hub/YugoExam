#utils.py

import spacy
import difflib
from spacy.cli import download as spacy_download

# Mapping topics to links
topic_links = {
    "osi model": "https://www.youtube.com/watch?v=vv4y_uOneC0",
    "switch": "https://www.geeksforgeeks.org/network-switch/",
    "router": "https://www.geeksforgeeks.org/router-in-computer-network/",
    "ip address": "https://www.geeksforgeeks.org/introduction-of-ip-address/",
    # Add more mappings as needed
}

stop_keywords = {
    "what", "why", "how", "is", "an", "are", "the", "in", "and", "a", "to", "of", "between", "on", "with", "for", "be"
}

# ✅ Lazy load the spaCy model only when needed
def get_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        spacy_download("en_core_web_sm")  # Download using spaCy's built-in method
        return spacy.load("en_core_web_sm")


def extract_topic_from_question(question_text):
    """Extract keywords from the question using spaCy and remove stop-like words."""
    nlp = get_nlp()  # Load model here
    doc = nlp(question_text)
    keywords = set()

    for token in doc:
        if token.pos_ in ("NOUN", "PROPN") and token.text.lower() not in stop_keywords:
            keywords.add(token.text.lower())

    return " and ".join(sorted(keywords)) if keywords else "General Technology"

def get_similarity(a, b):
    return difflib.SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()
