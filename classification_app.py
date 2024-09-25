import streamlit as st
import pickle
import pandas as pd

# Load the model (ensure this file exists)
with open('resume_classification.pkl', 'rb') as f:
    model_rfc = pickle.load(f)

# Load the sample DataFrame (replace with actual data loading)
data = {
    'Label': ['Developer', 'Developer', 'Admin', 'Developer', 'Admin'],
    'Cleaned_Tokens': [
        'anubhavkumarsinghtoworkinagloballycompetitiveenvironment',
        'profilesummary7yearsofexperienceinimplementing',
        'peoplesoftdatabaseadministrator',
        'muraliexperiencesummaryihave6yearsofexperience',
        'workdayfunctionalconsultantexpertisewith6years'
    ]
}
df = pd.DataFrame(data)

# Streamlit app
st.title('Resume Classification and Search')

# Dropdown for label selection
selected_label = st.selectbox("Select a label to view resumes:", df['Label'].unique())

if st.button("Show Resumes"):
    # Filter resumes based on the selected label
    matched_resumes = df[df['Label'] == selected_label]

    # Display matched resumes
    if not matched_resumes.empty:
        st.write("### Resumes with Label:", selected_label)
        for index, row in matched_resumes.iterrows():
            st.write(f"**Resume Content**: {row['Cleaned_Tokens']}")
            st.write("---")
    else:
        st.write("No resumes found for this label.")
