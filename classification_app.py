import streamlit as st
import pandas as pd
import pickle
import PyPDF2
import docx2txt
import os

# Streamlit UI
st.title('Resume Classification and Skill Matching')

# Load the pre-trained SVC model and DataFrame
svc_model = pickle.load(open("resume_classification_svc.pkl", 'rb'))
df = pickle.load(open("dataset_svc.pkl", 'rb'))

# Input files (resumes)
uploaded_files = st.file_uploader("Upload your resumes", type=['pdf', 'doc', 'docx'], accept_multiple_files=True)

# Skill selection
skills = st.multiselect("Select your skills:", [
    "Benefits", "Integration", "PeopleSoft", "Update Management", "PeopleTools", "Reporting",
    "Oracle 12c", "Studio", "Windows Server", "Application Designer", "PeopleSoft HCM",
    "PeopleSoft FSCM", "Crystal Reports", "SQL", "Java", "R", "Communication", "Leadership",
    "Power BI", "CSS", "JavaScript", "HTML", "MySQL", "Go", "Typescript", "React", "Node.js",
    "SOAP", "MongoDB", "Problem Solving", "SSIS", "MS SQL Server", "T-SQL", "Performance Tuning",
    "Data Analysis", "Stakeholder Management", "Calculated Fields", "Business Objects",
    "EIB Inbound", "Workday HCM", "Compensation", "Python", "C++", "C", "Embedded C",
    "Machine Learning", "Data Visualization", "Agile Methodologies", "Cloud Computing",
    "API Development", "DevOps", "Docker", "Kubernetes", "Git", "Scrum Master", 
    "NoSQL Databases", "Data Warehousing", "ETL Processes", "User Interface Design", 
    "Software Testing"
])

# Experience level selection
experience_options = [
    "Fresher (0-1 years)",
    "2 years",
    ">2 years",
    "2-5 years",
    "5-10 years",
    "<10 years"
]
selected_experience = st.selectbox("Select your experience level:", experience_options)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text() or ""  # Handle cases where text extraction may fail
    return text

# Function to extract text from a .docx file
def extract_text_from_docx(docx_file):
    text = docx2txt.process(docx_file)
    return text

# Initialize a list to store resumes with their details
resumes_data = []

# Process the uploaded files
if uploaded_files and skills:
    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split('.')[-1]

        # Extract text based on file type
        if file_extension == 'pdf':
            resume_text = extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            resume_text = extract_text_from_docx(uploaded_file)
        elif file_extension == 'doc':
            # For .doc files, handle them here if needed or skip
            st.write(f"Unsupported file format: {file_extension}")
            continue
        else:
            st.write(f"Unsupported file format: {file_extension}")
            continue

        # Display the file name
        st.write(f"### Resume: {uploaded_file.name}")

        # Find matching skills
        matched_skills = [skill for skill in skills if skill.lower() in resume_text.lower()]
        if matched_skills:
            st.write(f"**Matched Skills:** {', '.join(matched_skills)}")
            resumes_data.append({
                'file_name': uploaded_file.name,
                'matched_skills': matched_skills,
                'resume_text': resume_text
            })
        else:
            st.write("No skills matched.")

# Filter resumes based on experience level
if resumes_data:
    experience_filters = {
        "Fresher (0-1 years)": ["fresher", "1 year"],
        "2 years": ["2 years"],
        ">2 years": [f"{i} years" for i in range(3, 11)],
        "2-5 years": ["2 years", "3 years", "4 years"],
        "5-10 years": ["5 years", "6 years", "7 years", "8 years", "9 years", "10 years"],
        "<10 years": ["fresher", "1 year", "2 years", "3 years", "4 years", "5 years", "6 years", "7 years", "8 years", "9 years"]
    }

    st.write(f"### Resumes for {selected_experience}:")
    for resume in resumes_data:
        if any(exp in resume['resume_text'].lower() for exp in experience_filters[selected_experience]):
            st.write(f"**Resume:** {resume['file_name']}")
            st.write(f"**Matched Skills:** {', '.join(resume['matched_skills'])}")
