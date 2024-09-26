import streamlit as st
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer

# Load the model
with open('resume_classification.pkl', 'rb') as file:
    model_rfc = pickle.load(file)

# Load your dataset (replace 'Resumes-Dataset-with-Labels.xls' with your actual file path)
data = pd.read_excel('Resumes-Dataset-with-Labels.xls')  # Use read_excel for .xls files

# Initialize your vectorizer (use the same parameters as in training)
vectorizer = CountVectorizer()  # Replace with your actual vectorizer if applicable

# Streamlit application
st.title("Resume Classification")

# User inputs
st.header("Input Skills and Experiences")
skills = st.text_input("Enter Skills (comma-separated)")
experience = st.text_area("Enter Experience Details")

# Multi-select for resumes
st.header("Select Resumes for Comparison")
resume_options = data['File Name'].tolist()  # Extract the resume file names for selection
selected_resumes = st.multiselect("Select Resumes", resume_options)

if st.button("Predict"):
    # Preprocess the input
    user_input = f"{skills} {experience}"
    
    # Here, you should preprocess the input to match your model's expectations
    # For example, if you used CountVectorizer for training:
    cleaned_input = vectorizer.transform([user_input])  # Transform the input text to the feature matrix
    
    # Make prediction
    prediction = model_rfc.predict(cleaned_input)  # Use the cleaned input for prediction

    # Display the prediction result
    st.write("Predicted Resume Category: ", prediction[0])

    # Show relevant resumes based on the prediction
    relevant_resumes = data[data['Label'] == prediction[0]]
    st.write("Relevant Resumes Based on Prediction:")
    st.dataframe(relevant_resumes[['File Name', 'Label']])
    
    # Show the selected resumes by the user
    st.write("Selected Resumes:")
    if selected_resumes:
        selected_data = data[data['File Name'].isin(selected_resumes)]
        st.dataframe(selected_data[['File Name', 'Label']])
    else:
        st.write("No resumes selected.")
