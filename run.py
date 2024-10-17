import streamlit as st
import requests
import json

# Title of the Streamlit app
st.title("Bio-NER using Flask API")

# Instructions for the user
st.write("Enter text below for Named Entity Recognition (NER) and processing using the Flask backend.")

# Text input area for the user to enter PubMed abstracts or other text
text_input = st.text_area("Enter text for NER analysis:", height=200)

# Button to trigger the NER process
if st.button("Analyze with NER"):
    if text_input:  # Check if there is text in the input field
        # Prepare data to send to Flask API
        data = {"text": text_input}

        try:
            # Send the POST request to Flask API for NER
            response = requests.post("http://localhost:5000/bio-ner/entities", json=data)

            if response.status_code == 200:
                result = response.json()

                # Display entities and HTML rendering in Streamlit
                st.write("### NER Results:")
                st.write(result['entities'])  # The processed entities

                # Render HTML (You can use st.markdown if you're getting HTML content from displaCy)
                st.markdown(result['html'], unsafe_allow_html=True)
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter text to analyze.")
