import streamlit as st
from transformers import pipeline

# Load the NER pipeline from Hugging Face
ner_pipeline = pipeline("ner", grouped_entities=True)

# Title of the app
st.title("Bio-NER using Hugging Face Transformers")

# Input for PubMed abstracts or other text
text_input = st.text_area("Enter text for NER analysis:", height=200)

# Button to trigger the NER process
if st.button("Analyze with NER"):
    if text_input:
        # Run NER using Hugging Face pipeline
        results = ner_pipeline(text_input)

        # Display the results
        st.write("### NER Results:")
        for entity in results:
            st.write(f"- {entity['word']}: {entity['entity_group']} (score: {entity['score']:.4f})")
    else:
        st.warning("Please enter text to analyze.")
