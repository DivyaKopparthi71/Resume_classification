import streamlit as st
import pandas as pd
import pickle  # Assuming you're using a pre-trained model saved as a pickle

# Load pre-trained model
# Ensure you have saved your trained model as 'resume_model.pkl'
with open('resume_classification.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the function to predict resumes based on experience and skills
def classify_resume(experience, skills, resumes_df):
    # Use your pre-trained model to make predictions
    # Here, you need to adjust based on how your model works
    # Assuming the model takes 'experience' and 'skills' as input features
    # resumes_df contains the resumes data

    filtered_resumes = resumes_df[
        (resumes_df['experience'] >= experience) & 
        (resumes_df['skills'].apply(lambda x: all(skill in x for skill in skills)))
    ]
    
    # Here 'filtered_resumes' is a DataFrame of selected resumes based on criteria
    return filtered_resumes

# Load your resumes dataset (you might need to modify this part)
resumes_df = pd.read_csv('Resumes-Dataset-with-Labels.xls')  # Replace with your actual resumes data

# Streamlit app layout
st.title('Resume Classification App')

# Input form for user to enter criteria
experience = st.number_input('Minimum Experience (Years)', min_value=0, max_value=50, value=1)
skills_input = st.text_input('Required Skills (Comma Separated)').split(',')

# Button to trigger the prediction
if st.button('Classify Resumes'):
    # Perform classification
    result = classify_resume(experience, skills_input, resumes_df)
    
    # Display the result
    if not result.empty:
        st.write('Selected Resumes:')
        st.dataframe(result)
    else:
        st.write('No resumes match the criteria.')

# Optionally: Allow users to download the selected resumes
if not result.empty:
    result.to_csv('selected_resumes.csv', index=False)
    st.download_button(label='Download Selected Resumes', data='selected_resumes.csv', file_name='selected_resumes.csv')
