import streamlit as st
import pickle
import pandas as pd

# Load the trained model from the pickle file
model_file = "resume_classification.pkl"

with open(model_file, 'rb') as file:
    model_rfc = pickle.load(file)

# Define a function to preprocess the input data
def preprocess_resume(resume_text):
    # Add your preprocessing steps here (e.g., text cleaning, vectorization)
    # For demonstration, we'll just return the input text
    return resume_text

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
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()

        st.write("Resume Content:")
        st.write(resume_text)

        # Preprocess the resume
        processed_resume = preprocess_resume(resume_text)

        # Make predictions
        prediction = model_rfc.predict([processed_resume])

        # Display the prediction
        st.write("Classification Result:")
        st.write(prediction[0])

if __name__ == "__main__":
    main()
