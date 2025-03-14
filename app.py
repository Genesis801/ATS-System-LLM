# import streamlit as st
# import PyPDF2
# from llama_index import VectorStoreIndex, SimpleKeywordTableIndex, Document

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# # Function to create Llama index and calculate similarity
# def calculate_similarity_with_llama(resume_text, job_description):
#     # Create documents for resume and job description
#     resume_doc = Document(text=resume_text)
#     job_doc = Document(text=job_description)

#     # Create an index with the documents
#     index = VectorStoreIndex.from_documents([resume_doc, job_doc])

#     # Perform a similarity query
#     query_engine = index.as_query_engine()
#     response = query_engine.query(job_description)

#     return response

# # Streamlit UI
# st.title("ATS System: Resume Matcher with LLaMA")
# st.write("Upload your resume and paste the job description to get a match score.")

# # File upload and job description input
# uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
# job_description = st.text_area("Paste the Job Description here")

# if uploaded_file and job_description:
#     try:
#         # Extract resume text
#         resume_text = extract_text_from_pdf(uploaded_file)

#         # Calculate similarity using LLaMA index
#         response = calculate_similarity_with_llama(resume_text, job_description)

#         # Display results
#         st.subheader("Results")
#         st.write(f"**Match Response:** {response.response}")

#     except Exception as e:
#         st.error(f"An error occurred: {e}")
