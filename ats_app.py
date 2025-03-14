import streamlit as st
from langchain import LLMChain, PromptTemplate
from langchain.llms import Ollama
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Load environment variables (if needed)
load_dotenv()

# Initialize Ollama (local)
ollama = Ollama(base_url="http://localhost:11434", model="deepseek-r1:1.5b")  # Replace "llama2" with your preferred model

# Define a prompt template for matching JD and CV
prompt_template = PromptTemplate(
    input_variables=["job_description", "resume_text"],
    template="Compare the following job description and resume text, and provide: "
             "1. A match score between 0 and 100. "
             "2. Areas of improvement for the resume to better match the job description. "
             "Do not include any additional explanations or thinking process. "
             "Format your response as follows:\n\n"
             "Match Score: [score]/100\n"
             "Areas of Improvement: [bullet points]\n\n"
             "Job Description:\n{job_description}\n\n"
             "Resume:\n{resume_text}\n\n"
)

# Create a LangChain with Ollama
llm_chain = LLMChain(llm=ollama, prompt=prompt_template)

# Streamlit App
st.title("ATS Application")
st.write("Upload your Job Description and Resume (PDF) to get a match score and analysis.")

# Input field for Job Description
job_description = st.text_area("Paste the Job Description here:", height=200)

# File upload for Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

# Extract text from the uploaded PDF
resume_text = ""
if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text()
    except Exception as e:
        st.error(f"Error processing PDF: {e}")

# Match button
if st.button("Get Match Score"):
    if job_description and resume_text:
        # Get the match score and analysis using LangChain and Ollama
        with st.spinner("Analyzing..."):
            result = llm_chain.run(job_description=job_description, resume_text=resume_text)
        
        # Display the result
        st.subheader("Match Score and Analysis:")
        st.write(result)
    else:
        st.error("Please provide both the Job Description and Resume PDF.")