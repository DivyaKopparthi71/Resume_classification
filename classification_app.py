import streamlit as st
import pandas as pd
import pickle

# Load pre-trained model
with open('resume_classification.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define function to classify resumes
def classify_resume(experience, skills, resumes_df):
    # Ensure columns exist in the dataset
    if 'experience' not in resumes_df.columns or 'skills' not in resumes_df.columns:
        st.error("The dataset does not contain 'experience' or 'skills' columns.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Filter resumes based on experience and skills
    filtered_resumes = resumes_df[
        (resumes_df['experience'] >= experience) & 
        (resumes_df['skills'].apply(lambda x: all(skill.strip().lower() in x.lower() for skill in skills if skill)))
    ]
    
    return filtered_resumes

# Load resumes dataset (ensure the file exists and path is correct)
try:
    resumes_df = pd.read_csv('Resumes-Dataset-with-Labels.xls')  # Replace with the actual file path
    st.write("Resumes dataset loaded successfully.")
except Exception as e:
    st.error(f"Error loading dataset: {e}")

# Display the dataset columns for debugging
if resumes_df is not None:
    st.write("Available columns in the dataset:", resumes_df.columns)

# Streamlit app layout
st.title('Resume Classification App')

# Input form for user to enter criteria
experience = st.number_input('Minimum Experience (Years)', min_value=0, max_value=50, value=1)
skills_input = st.text_input('Required Skills (Comma Separated)').split(',')

# Button to trigger the prediction
if st.button('Classify Resumes'):
    if resumes_df is not None:
        result = classify_resume(experience, skills_input, resumes_df)

        # Display the result
        if not result.empty:
            st.write('Selected Resumes:')
            st.dataframe(result)
        else:
            st.write('No resumes match the criteria.')
    else:
        st.error("No dataset found.")

# Optionally: Allow users to download the selected resumes
if 'result' in locals() and not result.empty:
    csv_data = result.to_csv(index=False)
    st.download_button(label='Download Selected Resumes', data=csv_data, file_name='selected_resumes.csv', mime='text/csv')
