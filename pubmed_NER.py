import os
import pandas as pd
import streamlit as st
from Bio import Entrez, Medline
from io import BytesIO
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import spacy
from bionlp.processors import DiseaseProcessor, ChemicalProcessor, GeneProcessor, Entities

# Google Analytics tracking code
GA_JS = """..."""
components.html(GA_JS, height=0)

# PubMed article types
article_types = { ... }

# Load the NER models
try:
    print('Loading NER services...')
    disease_service = DiseaseProcessor('alvaroalon2/biobert_diseases_ner')
    chemical_service = ChemicalProcessor('alvaroalon2/biobert_chemical_ner')
    genetic_service = GeneProcessor('alvaroalon2/biobert_genetic_ner')
    nlp = spacy.load("en_core_web_sm", exclude=["tok2vec", "lemmatizer"])
    print('NER services loaded!')
except Exception as e:
    st.write(f"Error loading NER models: {e}")

# Function to construct query
def construct_query(search_term, mesh_term, choice):
    # Same as in the provided code
    ...

# Function to fetch abstracts from PubMed
def fetch_abstracts(query, num_articles, email):
    # Same as in the provided code
    ...

# Function to generate Excel file
def save_to_excel(articles):
    # Same as in the provided code
    ...

# Function to count articles by year
def count_articles_by_year(articles):
    # Same as in the provided code
    ...

# NER Processing function
def perform_ner_on_abstracts(df):
    extracted_entities = {
        "diseases": [],
        "chemicals": [],
        "genes": []
    }
    
    for idx, row in df.iterrows():
        abstract = row['Abstract']
        if abstract != 'No abstract available':
            doc = nlp(abstract)
            
            # Process the text through the NER pipeline
            entities = Entities(doc)
            for ent in doc.ents:
                if ent.label_ == "DISEASE":
                    extracted_entities["diseases"].append(ent.text)
                elif ent.label_ == "CHEMICAL":
                    extracted_entities["chemicals"].append(ent.text)
                elif ent.label_ == "GENE":
                    extracted_entities["genes"].append(ent.text)
    
    return extracted_entities

# Function to visualize entities with bar charts
def plot_entities_bar_chart(entities):
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Diseases", "Chemicals", "Genes"))

    # Diseases Bar Chart
    disease_counts = pd.Series(entities['diseases']).value_counts()
    fig.add_trace(go.Bar(x=disease_counts.index, y=disease_counts.values, name="Diseases"), row=1, col=1)

    # Chemicals Bar Chart
    chemical_counts = pd.Series(entities['chemicals']).value_counts()
    fig.add_trace(go.Bar(x=chemical_counts.index, y=chemical_counts.values, name="Chemicals"), row=2, col=1)

    # Genes Bar Chart
    gene_counts = pd.Series(entities['genes']).value_counts()
    fig.add_trace(go.Bar(x=gene_counts.index, y=gene_counts.values, name="Genes"), row=3, col=1)

    fig.update_layout(height=800, title="Entity Distribution in Abstracts", showlegend=False)
    st.plotly_chart(fig)

# Streamlit UI
st.title("PubMed Research Navigator with NER")
email = st.text_input("Enter your email (for PubMed access):")
search_term = st.text_input("Enter the general search term:")
mesh_term = st.text_input("Enter an optional MeSH term (leave blank if not needed):")
article_choice = st.selectbox("Select article type:", list(article_types.keys()))
num_articles = st.number_input("Enter the number of articles to fetch:", min_value=1, max_value=1000, value=10)

if st.button("Fetch Articles"):
    if email and search_term:
        query = construct_query(search_term, mesh_term, article_choice)
        articles = fetch_abstracts(query, num_articles, email)

        if articles:
            excel_data = save_to_excel(articles)
            st.download_button(
                label="Download Abstracts",
                data=excel_data,
                file_name="pubmed_articles.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Load the abstracts into a DataFrame
            df = pd.read_excel(excel_data)

            # Perform NER on the abstracts
            extracted_entities = perform_ner_on_abstracts(df)

            # Plot the extracted entities in bar charts
            plot_entities_bar_chart(extracted_entities)
        else:
            st.write("No articles fetched.")
    else:
        st.write("Please fill in all the required fields.")

st.write("Copyright Information...")
