import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the model
with open('resume_classification.pkl', 'rb') as f:
    model_rfc = pickle.load(f)

# Load the label mapping
with open('label_mapping.pkl', 'rb') as f:
    label_mapping = pickle.load(f)

# Streamlit app
st.title('Resume Classification')

# Input field for cleaned tokens
cleaned_tokens = st.text_input("Enter your cleaned tokens:")

if st.button("Classify"):
    # Assuming you have the same TF-IDF vectorizer
    input_tfidf = tfidf_vectorizer.transform([cleaned_tokens])
    
    # Make prediction
    prediction = model_rfc.predict(input_tfidf)

    # Get the human-readable label from the mapping
    predicted_label = label_mapping[prediction[0]]

    # Display the predicted label
    st.write(f"The predicted label is: **{predicted_label}**")
