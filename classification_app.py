import streamlit as st
import pandas as pd
import pickle

# Load the model
with open('resume_classification.pkl', 'rb') as file:
    model_rfc = pickle.load(file)

# Load your dataset (replace 'your_dataset.csv' with your actual file path)
data = pd.read_csv('Resumes-Dataset-with-Labels.xls')  # Update this line if your data is in a different format

# Streamlit application
st.title("Resume Classification")

# User inputs
st.header("Input Skills and Experiences")
skills = st.text_input("Enter Skills (comma-separated)")
experience = st.text_area("Enter Experience Details")

if st.button("Predict"):
    # Preprocess the input
    user_input = f"{skills} {experience}"
    # Here you would typically preprocess the input in the same way as you did for your training data
    # Example: Clean and tokenize the input as needed
    # cleaned_input = your_preprocessing_function(user_input)

    # Make prediction
    prediction = model_rfc.predict([user_input])  # Update if your model requires a different input format
    
    # Display the prediction result
    st.write("Predicted Resume Category: ", prediction[0])

    # Show relevant resumes based on the prediction
    relevant_resumes = data[data['Label'] == prediction[0]]
    st.write("Relevant Resumes:")
    st.dataframe(relevant_resumes[['File Name', 'Label']])


        
