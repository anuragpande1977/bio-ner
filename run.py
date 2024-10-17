import streamlit as st
import spacy
from pubmed_NER import fetch_abstracts  # Assuming this is your previous code for fetching abstracts

# Load the NER model (you can change to a different model if needed)
nlp = spacy.load("en_core_web_sm")

# Title of the Streamlit app
st.title("Bio-NER for PubMed Articles")

# Text input area for PubMed query
query = st.text_input("Enter PubMed query:")

# Button to fetch abstracts and run NER
if st.button("Fetch and Analyze Abstracts"):
    if query:
        # Fetch the abstracts using your existing function
        abstracts = fetch_abstracts(query)

        # If abstracts are returned, process with NER
        if abstracts:
            st.write(f"Fetched {len(abstracts)} abstracts. Running NER analysis...")

            # Process each abstract through the NER model
            for abstract in abstracts:
                doc = nlp(abstract)
                st.write(f"### Abstract: {abstract}")
                # Display named entities
                for ent in doc.ents:
                    st.write(f"- {ent.text} ({ent.label_})")
        else:
            st.warning("No abstracts found for the given query.")
    else:
        st.warning("Please enter a query.")

