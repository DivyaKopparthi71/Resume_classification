import streamlit as st
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the trained model
model_file = "resume_classification.pkl"
with open(model_file, 'rb') as file:
    model_rfc = pickle.load(file)

# Load the dataset to obtain feature names and labels
data = pd.read_csv("Resumes-Dataset-with-Labels.xls")  # Load your dataset
feature_names = data.columns[2:].tolist()  # Assuming the first two columns are Label and Cleaned_Tokens

# Create a mapping of numerical labels to string labels
label_mapping = {0: "Developer", 1: "Admin", 2: "Manager", 3: "Other"}
# Ensure that you map according to the actual numerical encoding used in your dataset.

# Streamlit app
st.title("Resume Classification")

# Input features
st.header("Input Features")
inputs = {}
for feature in feature_names:
    inputs[feature] = st.number_input(f"{feature}", min_value=0)

# Create a DataFrame for the input features
input_data = pd.DataFrame([inputs], columns=feature_names)

# Make predictions
if st.button("Classify"):
    try:
        prediction = model_rfc.predict(input_data)
        predicted_label = label_mapping[prediction[0]]  # Map the numerical prediction to the string label
        st.write("Prediction:", predicted_label)
    except ValueError as e:
        st.error(f"Error in prediction: {e}")

# Optionally show model accuracy
accuracy_train_rfc = accuracy_score(data['Label'], model_rfc.predict(data[feature_names]))  # Train accuracy on the dataset
st.subheader("Model Accuracy")
st.write("The model's accuracy on the training set is:", accuracy_train_rfc)

