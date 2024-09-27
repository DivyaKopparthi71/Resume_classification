import streamlit as st
import pandas as pd
import pickle
import PyPDF2
import docx2txt
import pythoncom
from win32com import client
import os

# Streamlit UI
st.title('Resume Classification and Skill Matching')

# Load the pre-trained SVC model and DataFrame
svc_model = pickle.load(open("model_svc.pkl", 'rb'))
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
        text += page.extract_text()
    return text

# Function to extract text from a .docx file
def extract_text_from_docx(docx_file):
    text = docx2txt.process(docx_file)
    return text

# Function to extract text from a .doc file using win32com
def extract_text_from_doc(doc_file):
    # Save the uploaded file temporarily
    with open("temp_doc_file.doc", "wb") as f:
        f.write(doc_file.getbuffer())

    pythoncom.CoInitialize()  # Initialize the COM library
    word = client.Dispatch("Word.Application")

    # Open the temporarily saved file using win32com
    doc = word.Documents.Open(os.path.abspath("temp_doc_file.doc"))
    doc_text = doc.Range().Text
    doc.Close()
    word.Quit()

    # Remove the temporary file after processing
    os.remove("temp_doc_file.doc")

    return doc_text

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
            resume_text = extract_text_from_doc(uploaded_file)
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
    if selected_experience == "Fresher (0-1 years)":
        st.write("### Resumes for Freshers (0-1 years):")
        for resume in resumes_data:
            if "fresher" in resume['resume_text'].lower() or "1 year" in resume['resume_text'].lower():
                st.write(f"**Resume:** {resume['file_name']}")
                st.write(f"**Matched Skills:** {', '.join(resume['matched_skills'])}")

    elif selected_experience == "2 years":
        st.write("### Resumes for 2 years Experience:")
        for resume in resumes_data:
            if "2 years" in resume['resume_text'].lower():
                st.write(f"**Resume:** {resume['file_name']}")
                st.write(f"**Matched Skills:** {', '.join(resume['matched_skills'])}")

    elif selected_experience == ">2 years":
        st.write("### Resumes for Experience > 2 years:")
        for resume in resumes_data:
            # Match resumes with experience greater than 2 years
            for i in range(3, 11):  # Checking from 3 to 10 years
                if f"{i} years" in resume['resume_text'].lower():
                    st.write(f"**Resume:** {resume['file_name']}")
                    st.write(f"**Matched Skills:** {', '.join(resume['matched_skills'])}")
                    break

    elif selected_experience == "2-5 years":
        st.write("### Resumes for Experience 2-5 years:")
        for resume in resumes_data:
            if "2 years" in resume['resume_text'].lower() or "3 years" in resume['resume_text'].lower() or "4 years" in resume['resume_text'].lower():
                st.write(f"**Resume:** {resume['file_name']}")
                st.write(f"**Matched Skills:** {', '.join(resume['matched_skills'])}")

    elif selected_experience == "5-10 years":
        st.write("### Resumes for Experience 5-10 years:")
        for resume in resumes_data:
            if "5 years" in resume['resume_text'].lower() or "6 years" in resume['resume_text'].lower() or "7 years" in resume['resume_text'].lower() or "8 years" in resume['resume_text'].lower() or "9 years" in resume['resume_text'].lower() or "10 years" in resume['resume_text'].lower():
                st.write(f"**Resume:** {resume['file_name']}")
                st.write(f"**Matched Skills:** {', '.join(resume['matched_skills'])}")

    elif selected_experience == "<10 years":
        st.write("### Resumes for Experience < 10 years:")
        for resume in resumes_data:
            if "fresher" in resume['resume_text'].lower() or "1 year" in resume['resume_text'].lower() or "2 years" in resume['resume_text'].lower() or "3 years" in resume['resume_text'].lower() or "4 years" in resume['resume_text'].lower() or "5 years" in resume['resume_text'].lower() or "6 years" in resume['resume_text'].lower() or "7 years" in resume['resume_text'].lower() or "8 years" in resume['resume_text'].lower() or "9 years" in resume['resume_text'].lower():
                st.write(f"**Resume:** {resume['file_name']}")
                st.write(f"**Matched Skills:** {', '.join(resume['matched_skills'])}")

