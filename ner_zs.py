import string
import streamlit as st
from transformers import pipeline

def preprocess_text(text):
    # Remove unnecessary characters
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.replace("\n", " ").replace("\r", "")

    # Convert to lowercase
    text = text.lower()

    return text

def main():
    st.title("Historical Text Named Entity Recognition for Project Gutenberg")

    # Enter URL or upload file
    option = st.radio("Select Input Option", ("Enter URL", "Upload Text File"))

    if option == "Enter URL":
        url = st.text_input("Enter URL")
        if url:
            text = get_text_from_url(url)
        else:
            st.warning("Please enter a valid URL")
            return
    else:
        file = st.file_uploader("Upload Text File")
        if file is not None:
            text = file.read().decode("utf-8")
        else:
            st.warning("Please upload a text file")
            return

    # Preprocess text
    text = preprocess_text(text)

    # Load zero-shot NER model
    nlp = pipeline("ner", model="cross-encoder/nli-distilroberta-base", tokenizer="distilroberta-base")

    # Label named entities using zero-shot NER model
    entities = nlp(text)

    # Display named entities
    st.write("Named Entities:")
    for entity in entities:
        st.write(f"{entity['entity']} : {entity['word']} (Score: {entity['score']:.2f})")
