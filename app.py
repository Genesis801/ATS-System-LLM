import streamlit as st
import PyPDF2
from transformers import pipeline, AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
import numpy as np

# Load pre-trained model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to compute embeddings
def compute_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings

# Function to calculate similarity score
def calculate_similarity(resume_text, job_description):
    resume_embedding = compute_embeddings(resume_text)
    job_embedding = compute_embeddings(job_description)
    similarity = cosine_similarity(resume_embedding.numpy(), job_embedding.numpy())
    return similarity[0][0]

# Streamlit UI
st.title("ATS System: Resume Matcher")
st.write("Upload your resume and paste the job description to get a match score.")

# File upload and job description input
uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here")

if uploaded_file and job_description:
    try:
        # Extract resume text
        resume_text = extract_text_from_pdf(uploaded_file)

        # Calculate similarity score
        similarity_score = calculate_similarity(resume_text, job_description)

        # Display results
        st.subheader("Results")
        st.write(f"**Match Score:** {round(similarity_score * 100, 2)}%")

        # Recommendation
        if similarity_score > 0.8:
            st.success("Recommendation: Likely to be selected")
        elif similarity_score > 0.6:
            st.warning("Recommendation: Moderate chance")
        else:
            st.error("Recommendation: Unlikely to be selected")

    except Exception as e:
        st.error(f"An error occurred: {e}")
