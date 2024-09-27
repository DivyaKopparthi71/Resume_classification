import streamlit as st
import pandas as pd
import pickle
import PyPDF2
import docx2txt

# Streamlit UI
st.title('Resume Classification and Skill Matching')

# Load the pre-trained SVC model and DataFrame (assuming these are required later in the code)
svc_model = pickle.load(open("resume_classification_svc.pkl", 'rb'))
df = pickle.load(open("dataset_svc.pkl", 'rb'))

# Input files (resumes)
uploaded_files = st.file_uploader("Upload your resumes", type=['pdf', 'docx'], accept_multiple_files=True)

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
    "Fresher (0-1 years)", "2 years", ">2 years", "2-5 years", "5-10 years", "<10 years"
]
selected_experience = st.selectbox("Select your experience level:", experience_options)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text() or ""
    return text

# Function to extract text from a .docx file
def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

# Initialize session state to store resumes data and results
if 'resumes_data' not in st.session_state:
    st.session_state['resumes_data'] = []

# Process the uploaded files
if uploaded_files and skills:
    resumes_data = []
    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        # Extract text based on file type
        if file_extension == 'pdf':
            resume_text = extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            st.write(f"Unsupported file format: {file_extension}")
            continue

        # Find matching skills
        matched_skills = [skill for skill in skills if skill.lower() in resume_text.lower()]
        
        # Add resume details if skills matched
        if matched_skills:
            resumes_data.append({
                'file_name': uploaded_file.name,
                'matched_skills': matched_skills,
                'resume_text': resume_text,
                'resume_data': uploaded_file.read()  # Store resume file for later download
            })
    
    # Store in session state to retain data
    st.session_state['resumes_data'] = resumes_data

# Filter resumes based on experience level and match them with selected skills
if st.button('Classify') or st.session_state.get('classified', False):
    st.session_state['classified'] = True  # Mark as classified

    if st.session_state['resumes_data']:
        experience_filters = {
            "Fresher (0-1 years)": ["fresher", "0 years", "1 year"],
            "2 years": ["2 years"],
            ">2 years": [f"{i} years" for i in range(3, 11)],
            "2-5 years": ["2 years", "3 years", "4 years", "5 years"],
            "5-10 years": ["5 years", "6 years", "7 years", "8 years", "9 years", "10 years"],
            "<10 years": ["fresher", "1 year", "2 years", "3 years", "4 years", "5 years", "6 years", "7 years", "8 years", "9 years"]
        }

        # Display resumes that meet both skills and experience criteria
        filtered_resumes = []
        for resume in st.session_state['resumes_data']:
            if any(exp in resume['resume_text'].lower() for exp in experience_filters[selected_experience]):
                filtered_resumes.append(resume)

        if filtered_resumes:
            st.write(f"### Resumes matching {selected_experience} and selected skills:")
            for resume in filtered_resumes:
                st.write(f"**Resume:** {resume['file_name']}")
                st.write(f"**Matched Skills:** {', '.join(resume['matched_skills'])}")

                # Add a preview expander to show resume text
                with st.expander(f"Preview {resume['file_name']}"):
                    st.write(resume['resume_text'])

                # Add a download button for each resume
                st.download_button(
                    label=f"Download {resume['file_name']}",
                    data=resume['resume_data'],
                    file_name=resume['file_name']
                )
        else:
            st.write(f"No resumes match the selected experience level ({selected_experience}) and skills.")
    else:
        st.write("Please upload resumes and select skills.")
