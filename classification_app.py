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

# Year of Passing selection (custom range)
year_of_passing_input = st.text_input("Enter Year of Passing (e.g., 2019-2023 or 2010):")
year_of_passing = []

if year_of_passing_input:
    if '-' in year_of_passing_input:  # If a range is given
        start_year, end_year = map(int, year_of_passing_input.split('-'))
        year_of_passing = list(range(start_year, end_year + 1))
    else:  # If a single year is given
        year_of_passing = [int(year_of_passing_input)]

# Professional Role selection
professional_roles = [
    "PeopleSoft Admin", "Developer", "Software Engineer", "PeopleSoft Consultant",
    "Senior Software Engineer", "SQL Developer", "React Developer", "UI Developer",
    "Front End Developer", "Web Developer", "Not Specified", "Techno Functional Consultant",
    "Workday Consultant", "Workday Integration Consultant",
    "Data Scientist", "Data Analyst", "Business Analyst", "Machine Learning Engineer",
    "DevOps Engineer", "System Architect", "Database Administrator", "Cloud Engineer",
    "Mobile Application Developer", "Full Stack Developer", "Scrum Master",
    "Network Engineer", "Project Manager", "Product Manager", "IT Support Specialist",
    "Cybersecurity Analyst", "QA Engineer", "Game Developer", "Salesforce Developer",
    "Digital Marketing Specialist", "Content Strategist", "Technical Writer",
    "UI/UX Designer", "Software Tester", "Embedded Systems Engineer", 
    "Infrastructure Engineer", "Blockchain Developer", "AI Researcher"
]
selected_role = st.selectbox("Select Professional Role:", professional_roles)

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

if 'preview_states' not in st.session_state:
    st.session_state['preview_states'] = {}  # Dictionary to track preview states for each resume

# Process the uploaded files
if uploaded_files and skills:
    resumes_data = []
    processed_file_names = set()  # Set to keep track of processed file names

    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        # Check for duplicates
        if uploaded_file.name in processed_file_names:
            st.warning(f"Duplicate file detected: {uploaded_file.name}. This file will be skipped.")
            continue

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
            processed_file_names.add(uploaded_file.name)  # Add file name to processed set
    
    # Store in session state to retain data
    st.session_state['resumes_data'] = resumes_data

# Button to classify resumes
if st.button('Classify'):
    if st.session_state['resumes_data']:
        # Filter resumes based only on matched skills
        filtered_resumes = [
            resume for resume in st.session_state['resumes_data']
            if any(skill.lower() in resume['resume_text'].lower() for skill in skills)
        ]

        # Further filtering based on experience level if selected
        if selected_experience:
            experience_filters = {
                "Fresher (0-1 years)": ["fresher", "0 years", "1 year"],
                "2 years": ["2 years"],
                ">2 years": [f"{i} years" for i in range(3, 11)],
                "2-5 years": ["2 years", "3 years", "4 years", "5 years"],
                "5-10 years": ["5 years", "6 years", "7 years", "8 years", "9 years", "10 years"],
                "<10 years": ["fresher", "1 year", "2 years", "3 years", "4 years", "5 years", "6 years", "7 years", "8 years", "9 years"]
            }

            filtered_resumes = [
                resume for resume in filtered_resumes
                if any(exp in resume['resume_text'].lower() for exp in experience_filters[selected_experience])
            ]

        # Check for year of passing matches the specified range
        if year_of_passing:
            filtered_resumes = [
                resume for resume in filtered_resumes
                if any(str(year) in resume['resume_text'] for year in year_of_passing)
            ]

        if filtered_resumes:
            st.write(f"### Resumes matching selected skills:")
            # Display resumes with a button to toggle preview text
            for resume in filtered_resumes:
                col1, col2 = st.columns([9, 1])  # Layout with a preview area and download symbol

                with col1:
                    # Display file name and a button to toggle resume preview
                    st.write(f"**{resume['file_name']}**")

                    # Initialize preview state if not set
                    if resume['file_name'] not in st.session_state['preview_states']:
                        st.session_state['preview_states'][resume['file_name']] = False

                    # Button to toggle preview
                    if st.button(f"{'Hide' if st.session_state['preview_states'][resume['file_name']] else 'Show'} {resume['file_name']}", key=f"preview_{resume['file_name']}"):
                        st.session_state['preview_states'][resume['file_name']] = not st.session_state['preview_states'][resume['file_name']]

                    # Show or hide the preview based on the state
                    if st.session_state['preview_states'][resume['file_name']]:
                        st.text_area(label="Resume Preview", value=resume['resume_text'], height=300, key=f"textarea_{resume['file_name']}", disabled=True)

                with col2:
                    # Add download button with a unique key
                    st.download_button("☁️", data=resume['resume_data'], file_name=resume['file_name'], key=f"download_{resume['file_name']}")

        else:
            st.write("No resumes matched your criteria.")
    else:
        st.write("No resumes uploaded.")
