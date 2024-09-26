import pickle
import streamlit as st
import pandas as pd

# Load the trained model
with open("resume_classification.pkl", 'rb') as file:
    model = pickle.load(file)

# Load your resumes dataset
# Assume the dataset has columns: 'Label', 'Resume'
resumes_df = pd.read_csv("resumes_dataset.csv")  # Update with your actual file path

# Define your labels based on the model training
labels = ["Developer", "Admin", "Manager", "Others"]

# Title of the web app
st.title("Resume Classification")

# Input fields for label, experience, year of passing, education, and technical skills
label = st.selectbox("Select Label", labels)
experience = st.selectbox("Select Experience Range", ["0-2 years", "2-5 years", "5-10 years", "10+ years"])
year_of_passing = st.selectbox("Select Year of Passing", [2010, 2012, 2015, 2018, 2020, 2022])
education = st.selectbox("Select Education Level", ["Bachelor's", "Master's", "PhD"])

# Input for technical skills
skills = st.text_input("Enter Technical Skills (comma-separated)", "Python, Machine Learning, Data Analysis")

# Button to make predictions
if st.button('Predict'):
    # Process the inputs to match model expectations
    skills_list = [skill.strip() for skill in skills.split(',')]
    
    # Prepare the input data for the model
    input_data = [label, experience, year_of_passing, education] + skills_list
    
    # Make prediction
    prediction = model.predict([input_data])
    
    # Show prediction result
    predicted_class = prediction[0]
    st.write(f"Predicted Class: {predicted_class}")
    
    # Filter resumes that match the predicted class from the DataFrame
    matching_resumes = resumes_df[resumes_df['Label'] == predicted_class]
    
    # Display matching resumes
    if not matching_resumes.empty:
        st.write(f"Matching Resumes for {predicted_class}:")
        for index, row in matching_resumes.iterrows():
            st.write(f"Resume {index + 1}: {row['Resume']}")
    else:
        st.write("No resumes found for the predicted class.")
