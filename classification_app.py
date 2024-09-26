import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import PyPDF2

# Load the trained model from the pickle file
model_file = "resume_classification.pkl"

with open(model_file, 'rb') as file:
    model_rfc = pickle.load(file)

# Load the TF-IDF vectorizer
vectorizer_file = "tfidf_vectorizer.pkl"
with open(vectorizer_file, 'rb') as file:
    tfidf_vectorizer = pickle.load(file)

# Define a function to preprocess the input data
def preprocess_resume(resume_text):
    # Vectorize the input text using the loaded vectorizer
    return tfidf_vectorizer.transform([resume_text])  # Transform to match training data format

# Define the Streamlit app
def main():
    st.title("Resume Classification App")

    st.write("Upload your resume (in text format) for classification:")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf'])

    if uploaded_file is not None:
        # Read the file content
        if uploaded_file.type == 'text/plain':
            resume_text = uploaded_file.read().decode('utf-8')
        elif uploaded_file.type == 'application/pdf':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()

        st.write("Resume Content:")
        st.write(resume_text)

        # Preprocess the resume
        processed_resume = preprocess_resume(resume_text)

        # Check shape and type of processed resume
        st.write("Processed Resume Shape:", processed_resume.shape)
        
        if processed_resume.shape[1] == model_rfc.n_features_in_:
            # Make prediction using the loaded model
            prediction = model_rfc.predict(processed_resume)
            prediction_proba = model_rfc.predict_proba(processed_resume)

            st.write("Predicted Class:", prediction[0])
            st.write("Prediction Probabilities:", prediction_proba)

        else:
            st.error(f"Mismatch in feature dimensions. Expected {model_rfc.n_features_in_} features but got {processed_resume.shape[1]}.")

# Run the app
if __name__ == "__main__":
    main()
