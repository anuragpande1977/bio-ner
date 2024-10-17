import streamlit as st
import spacy
import subprocess

# Ensure the SpaCy model is installed if not already
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

from spacy import displacy

# Custom colors for visualization (if needed)
colors = {
    "DISEASE": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
    "CHEMICAL": "linear-gradient(90deg, #ffa17f, #3575ad)",
    "GENETIC": "linear-gradient(90deg, #c21500, #ffc500)"
}

# Title of the Streamlit app
st.title("Bio-NER using SpaCy NER Model")

# Instructions for the user
st.write("Enter text below for Named Entity Recognition (NER) processing.")

# Text input area for the user to enter PubMed abstracts or other text
text_input = st.text_area("Enter text for NER analysis:", height=200)

# Button to trigger the NER process
if st.button("Analyze with NER"):
    if text_input:
        # Process the text with Spacy NER
        doc = nlp(text_input)

        # Render entities using displacy
        entities_html = displacy.render(doc, style="ent", options={"colors": colors})

        # Display the rendered HTML in Streamlit
        st.markdown(entities_html, unsafe_allow_html=True)

        # Optionally, list the entities in text form
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        st.write("### Extracted Entities:")
        st.write(entities)
    else:
        st.warning("Please enter text to analyze.")
