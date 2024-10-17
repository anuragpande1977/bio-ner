import streamlit as st
from transformers import pipeline

# Load the NER pipeline using a locally stored BioBERT model
ner_pipeline = pipeline("ner", model="./biobert-model", grouped_entities=True)

# Title of the app
st.title("Bio-NER using BioBERT for Biomedical Entities")

# Input for PubMed abstracts or other text
text_input = st.text_area("Enter text for NER analysis:", height=200)

# Button to trigger the NER process
if st.button("Analyze with NER"):
    if text_input:
        # Show the input text
        st.write(f"Input text: {text_input}")
        
        # Run NER using the BioBERT pipeline
        results = ner_pipeline(text_input)

        # Show raw NER results
        st.write("Raw NER Results:")
        st.write(results)

        # Display the processed NER results
        if results:
            st.write("### NER Results:")
            for entity in results:
                st.write(f"- {entity['word']}: {entity['entity_group']} (score: {entity['score']:.4f})")
        else:
            st.write("No entities detected.")
    else:
        st.warning("Please enter text to analyze.")
