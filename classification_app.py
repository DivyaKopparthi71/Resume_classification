import streamlit as st
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the trained model
model_file = "resume_classification.pkl"
with open(model_file, 'rb') as file:
    model_rfc = pickle.load(file)

# Load the dataset to obtain feature names for input
# Assuming you have a DataFrame to extract feature names (replace with your actual dataset)
data = pd.read_csv("Resumes-Dataset-with-Labels.csv")  # Load your dataset
feature_names = data.columns[2:].tolist()  # Assuming the first two columns are Label and Cleaned_Tokens

# Streamlit app
st.title("Resume Classification")

# Input features
st.header("Input Features")
inputs = {}
for feature in feature_names:
    inputs[feature] = st.number_input(f"{feature}", min_value=0)

# Create a DataFrame for the input features
input_data = pd.DataFrame([inputs])

# Make predictions
if st.button("Classify"):
    prediction = model_rfc.predict(input_data)
    st.write("Prediction:", prediction[0])

# Optionally show model accuracy
accuracy_train_rfc = accuracy_score(data['Label'], model_rfc.predict(data[feature_names]))  # Train accuracy on the dataset
st.subheader("Model Accuracy")
st.write("The model's accuracy on the training set is:", accuracy_train_rfc)

