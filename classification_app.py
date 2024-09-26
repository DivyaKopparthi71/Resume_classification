import streamlit as st
import pandas as pd
import pickle

# Load pre-trained model
with open('resume_classification.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define function to classify resumes
def classify_resume(selected_resumes, experience, skills, resumes_df):
    # Ensure columns exist in the dataset
    if 'experience' not in resumes_df.columns or 'skills' not in resumes_df.columns:
        st.error("The dataset does not contain 'experience' or 'skills' columns.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Filter selected resumes based on experience and skills
    filtered_resumes = selected_resumes[
        (selected_resumes['experience'] >= experience) & 
        (selected_resumes['skills'].apply(lambda x: all(skill.strip().lower() in x.lower() for skill in skills if skill)))
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

# Check if 'name' column exists; if not, modify accordingly
identifier_column = 'name'  # Replace 'name' with the actual column that identifies resumes

if identifier_column in resumes_df.columns:
    # Step 1: Display all resumes and allow user to select multiple resumes
    selected_indices = st.multiselect('Select Resumes:', resumes_df.index, format_func=lambda x: resumes_df.iloc[x][identifier_column])
else:
    st.error(f"The dataset does not contain a '{identifier_column}' column for identifying resumes.")

# Proceed if resumes are selected
if selected_indices:
    selected_resumes = resumes_df.iloc[selected_indices]

    # Step 2: Input form for user to enter criteria after selecting resumes
    st.write("Selected Resumes:")
    st.dataframe(selected_resumes)

    experience = st.number_input('Minimum Experience (Years)', min_value=0, max_value=50, value=1)
    skills_input = st.text_input('Required Skills (Comma Separated)').split(',')

    # Step 3: Button to trigger the prediction
    if st.button('Filter Selected Resumes'):
        result = classify_resume(selected_resumes, experience, skills_input, resumes_df)

        # Step 4: Display the result
        if not result.empty:
            st.write('Resumes matching the criteria:')
            st.dataframe(result)
        else:
            st.write('No resumes match the criteria.')

        # Optionally: Allow users to download the selected resumes
        csv_data = result.to_csv(index=False)
        st.download_button(label='Download Filtered Resumes', data=csv_data, file_name='filtered_resumes.csv', mime='text/csv')
else:
    st.write("Please select resumes to proceed.")
