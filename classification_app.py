import streamlit as st
import pandas as pd
import pickle

# Load pre-trained model (if needed)
with open('resume_classification.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define function to classify resumes based on experience and skills
def classify_resume(selected_resumes, experience, skills, resumes_df):
    if 'experience' not in resumes_df.columns or 'File Name' not in resumes_df.columns:
        st.error("The dataset does not contain 'experience' or 'File Name' columns.")
        return pd.DataFrame()

    # Check if all required skills are present in the resume text
    def filter_skills_in_text(resume_text, skills):
        return all(skill.strip().lower() in resume_text.lower() for skill in skills if skill)

    filtered_resumes = selected_resumes[
        (selected_resumes['experience'] >= experience) &
        (selected_resumes['File Name'].apply(lambda filename: filter_skills_in_text(read_resume_text(filename), skills)))
    ]

    return filtered_resumes

# Function to read resume text from a file
def read_resume_text(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except Exception as e:
        st.error(f"Error reading file {filename}: {e}")
        return ""

# Load resumes dataset
try:
    resumes_df = pd.read_excel('Resumes-Dataset-with-Labels.xls')  # Ensure correct file type
    st.write("Resumes dataset loaded successfully.")
except Exception as e:
    st.error(f"Error loading dataset: {e}")

# Display the dataset columns for debugging
if resumes_df is not None:
    st.write("Available columns in the dataset:", resumes_df.columns)

# Streamlit app layout
st.title('Resume Classification App')

# Use 'File Name' as the identifier for resumes
identifier_column = 'File Name'

if identifier_column in resumes_df.columns:
    selected_indices = st.multiselect('Select Resumes:', resumes_df.index, format_func=lambda x: resumes_df.iloc[x][identifier_column])
else:
    st.error(f"The dataset does not contain a '{identifier_column}' column for identifying resumes.")

# Proceed if resumes are selected
if selected_indices:
    selected_resumes = resumes_df.iloc[selected_indices]

    st.write("Selected Resumes:")
    st.dataframe(selected_resumes)

    experience = st.number_input('Minimum Experience (Years)', min_value=0, max_value=50, value=1)
    skills_input = st.text_input('Required Skills (Comma Separated)').split(',')

    if st.button('Filter Selected Resumes'):
        result = classify_resume(selected_resumes, experience, skills_input, resumes_df)

        if not result.empty:
            st.write('Resumes matching the criteria:')
            st.dataframe(result)
        else:
            st.write('No resumes match the criteria.')

        # Allow users to download the selected resumes
        csv_data = result.to_csv(index=False)
        st.download_button(label='Download Filtered Resumes', data=csv_data, file_name='filtered_resumes.csv', mime='text/csv')
else:
    st.write("Please select resumes to proceed.")
