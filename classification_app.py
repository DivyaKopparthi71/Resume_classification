import streamlit as st
import pandas as pd
import pickle
import re

# Load the trained model and TF-IDF vectorizer
model_rfc = joblib.load('resume_classification.pkl')  # Update with the path to your model file
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')  # Update with the path to your vectorizer file

def preprocess_resume(resume_text):
    # Example preprocessing steps
    resume_text = resume_text.lower()  # Lowercase
    resume_text = re.sub(r'[^\w\s]', '', resume_text)  # Remove punctuation
    return tfidf_vectorizer.transform([resume_text])  # Transform to match training data format

def predict_resume_category(processed_resume):
    prediction = model_rfc.predict(processed_resume)
    return prediction[0]  # Return the predicted class

def main():
    st.title("Resume Classifier")
    st.write("Upload a resume to classify its category.")

    # File uploader for resume
    uploaded_file = st.file_uploader("Choose a resume file", type=["txt", "pdf"])

    if uploaded_file is not None:
        # Read and process the uploaded file
        if uploaded_file.type == "text/plain":
            resume_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
        
        # Debugging output
        st.write("Original Resume:")
        st.write(resume_text)
        
        # Preprocess the resume
        processed_resume = preprocess_resume(resume_text)

        # Check shape and type of processed resume
        st.write("Processed Resume Shape:", processed_resume.shape)
        st.write("Expected Features:", model_rfc.n_features_in_)

        # Predict the category of the resume
        if processed_resume.shape[1] == model_rfc.n_features_in_:
            prediction = predict_resume_category(processed_resume)
            st.write(f"The predicted category is: {prediction}")
        else:
            st.error(f"Mismatch in feature dimensions. Expected {model_rfc.n_features_in_} features but got {processed_resume.shape[1]}.")

if __name__ == "__main__":
    main()
