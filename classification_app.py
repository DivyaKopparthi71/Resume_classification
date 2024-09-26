import streamlit as st
import pandas as pd
import pickle

# Load the model
with open('resume_classification.pkl', 'rb') as file:
    model_rfc = pickle.load(file)

# Load your dataset (replace 'your_dataset.csv' with your actual file path)
data = pd.read_csv('your_dataset.csv')  # Update this line if your data is in a different format

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
    
    # Here you would typically preprocess the input in the same way as you did for your training data
    # Example: Clean and tokenize the input as needed
    # cleaned_input = your_preprocessing_function(user_input)
    
    # Make prediction
    prediction = model_rfc.predict([user_input])  # Ensure this matches your model's input requirements

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
