import streamlit as st
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the model
with open('resume_classification.pkl', 'rb') as file:
    model_rfc = pickle.load(file)

# Load your dataset (ensure the path is correct)
data = pd.read_csv('Resumes-Dataset-with-Labels.csv')


# Define text cleaning function
def text_clean_nltk(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    cleaned_text = ' '.join(tokens)
    return cleaned_text

# Clean the resume text
data['Cleaned_Tokens'] = data['Resume Text'].apply(text_clean_nltk)

# List of keywords to count
keywords = ['developer', 'admin', 'manager', 'other']

# Create keyword count features
for keyword in keywords:
    data[f'count_{keyword}'] = data['Cleaned_Tokens'].str.lower().str.count(keyword)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
X_tfidf = tfidf_vectorizer.fit_transform(data['Cleaned_Tokens'])

# Convert TF-IDF matrix to DataFrame and combine with keyword counts
tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
X = pd.concat([data.reset_index(drop=True), tfidf_df], axis=1)

# Prepare your labels
Y = data['Label']

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
    
    # Clean the user input
    cleaned_input = text_clean_nltk(user_input)

    # Vectorize the user input
    user_input_vectorized = tfidf_vectorizer.transform([cleaned_input])

    # Prepare features for prediction
    user_feature_vector = pd.DataFrame(user_input_vectorized.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
    
    # Ensure the keyword counts are also included
    for keyword in keywords:
        user_feature_vector[f'count_{keyword}'] = cleaned_input.lower().count(keyword)

    # Make prediction
    prediction = model_rfc.predict(user_feature_vector)  # Use the cleaned input for prediction

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
