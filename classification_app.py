import streamlit as st
import pandas as pd
import pickle

# Load pre-trained model (if needed)
with open('resume_classification.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define function to classify resumes based on 'Label' and 'Cleaned_Tokens'
def classify_resume(selected_resumes, role, skills, resumes_df):
    # Ensure 'Cleaned_Tokens' and 'Label' exist in the dataset
    if 'Cleaned_Tokens' not in resumes_df.columns or 'Label' not in resumes_df.columns:
        st.error("The dataset does not contain 'Cleaned_Tokens' or 'Label' columns.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Filter selected resumes based on the role and skills
    filtered_resumes = selected_resumes[
        (selected_resumes['Label'] == role) & 
        (selected_resumes['Cleaned_Tokens'].apply(lambda x: all(skill.strip().lower() in x.lower() for skill in skills if skill)))
    ]
    
    return filtered_resumes

# Load resumes dataset
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

# Use 'File Name' as the identifier for resumes
identifier_column = 'File Name'

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

    # Input for role selection (Admin, Developer, etc.)
    role = st.selectbox('Select Role:', resumes_df['Label'].unique())

    # Input for required skills
    skills_input = st.text_input('Required Skills (Comma Separated)').split(',')

    # Step 3: Button to trigger the filtering
    if st.button('Filter Selected Resumes'):
        result = classify_resume(selected_resumes, role, skills_input, resumes_df)

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
