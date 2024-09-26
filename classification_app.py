import streamlit as st
import pandas as pd
import pickle

# Load the saved model
file_name = "resume_classification.pkl"
with open(file_name, 'rb') as file:
    model_rfc = pickle.load(file)

# Load your dataset
data = pd.read_csv("Resumes-Dataset-with-Labels.xls")  # Replace with your actual dataset file

# Map numerical labels to more descriptive names
label_mapping = {
    0: 'developer',
    1: 'admin',
    2: 'manager',
    3: 'others'
}

# Create a new column in the dataframe with the mapped labels
data['Label_Mapped'] = data['Label'].map(label_mapping)

# Streamlit app
st.title("Resume Classification")

# Input for the label (dropdown showing descriptive labels instead of 0, 1, etc.)
selected_label = st.selectbox('Select Role:', data['Label_Mapped'].unique())

# Map the selected label back to its numeric form
numeric_label = {v: k for k, v in label_mapping.items()}[selected_label]

# Filter the dataset based on the selected label
filtered_data = data[data['Label'] == numeric_label]

# Display the count of resumes
st.write(f"Number of resumes for {selected_label}: {len(filtered_data)}")

# Display the file names of resumes with the selected label
st.write(f"Resumes with the selected role ({selected_label}):")
st.dataframe(filtered_data[['File Name']])

# Optional: If you want to run predictions
# Assuming the necessary input features are in the dataset
X_test = filtered_data[['count_developer', 'count_admin', 'count_manager', 'count_other']]  # Modify columns as per your dataset
predictions = model_rfc.predict(X_test)

st.write("Predictions for selected role:")
st.write(predictions)

