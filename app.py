import streamlit as st
import os
import pandas as pd
import json
from utils.parsing import extract_text_from_pdf, extract_text_from_docx
from utils.matching import extract_skills, match_skills
from utils.scoring import calculate_relevance_score
from utils.visualization import create_gauge_chart

# File paths relative to repo root
RESUME_DIR = "sample_data/resumes/Resumes"
JD_DIR = "sample_data/jds/JD"
HISTORY_FILE = "analysis_history.json"

# Streamlit page configuration
st.set_page_config(page_title="AI Resume Relevance Checker", layout="wide")

# Initialize session state for analysis history
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Sidebar for navigation
st.sidebar.title("Resume Checker")
page = st.sidebar.radio("Select Page", ["Analysis", "Dashboard"])

# Analysis Tab
if page == "Analysis":
    st.header("Resume Analysis")
    
    # Resume selection
    resume_files = [f for f in os.listdir(RESUME_DIR) if f.endswith(('.pdf', '.docx'))]
    resume = st.selectbox("Select Resume", ["Upload a file"] + resume_files)
    
    if resume == "Upload a file":
        resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    else:
        resume_path = os.path.join(RESUME_DIR, resume)
        resume_file = None
    
    # JD selection
    jd_option = st.radio("JD Input", ["Select Sample JD", "Paste JD Text", "Upload JD PDF"])
    if jd_option == "Select Sample JD":
        jd_files = [f for f in os.listdir(JD_DIR) if f.endswith('.pdf')]
        jd_file = st.selectbox("Select JD", jd_files)
        jd_path = os.path.join(JD_DIR, jd_file)
    elif jd_option == "Paste JD Text":
        jd_text = st.text_area("Paste Job Description")
    else:
        jd_upload = st.file_uploader("Upload JD (PDF)", type=["pdf"])
    
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            # Simulate progress
            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)
            
            # Extract resume text
            if resume_file:
                if resume_file.name.endswith('.pdf'):
                    resume_text = extract_text_from_pdf(resume_file)
                else:
                    resume_text = extract_text_from_docx(resume_file)
            else:
                if resume.endswith('.pdf'):
                    resume_text = extract_text_from_pdf(resume_path)
                else:
                    resume_text = extract_text_from_docx(resume_path)
            
            # Extract JD text
            if jd_option == "Select Sample JD":
                jd_text = extract_text_from_pdf(jd_path)
            elif jd_option == "Paste JD Text":
                jd_text = jd_text
            else:
                jd_text = extract_text_from_pdf(jd_upload)
            
            # Process analysis
            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text)
            matched_skills, missing_skills = match_skills(resume_skills, jd_skills)
            score = calculate_relevance_score(resume_text, jd_text)
            
            # Display results
            st.write(f"**Relevance Score**: {score:.2f}%")
            verdict = "Strong" if score >= 75 else "Moderate" if score >= 50 else "Weak"
            st.write(f"**Verdict**: {verdict}")
            st.write("**Matched Skills**:")
            st.write(", ".join(matched_skills) if matched_skills else "None")
            st.write("**Missing Skills**:")
            st.write(", ".join(missing_skills) if missing_skills else "None")
            
            # Suggestions (placeholder)
            suggestions = ["Add missing skills to resume", "Highlight relevant experience"]
            st.write("**Suggestions**:")
            for s in suggestions:
                st.write(f"- {s}")
            
            # Gauge chart
            fig = create_gauge_chart(score)
            st.plotly_chart(fig)
            
            # Save to history
            analysis = {
                "resume": resume_file.name if resume_file else resume,
                "jd_source": jd_file if jd_option == "Select Sample JD" else "Uploaded/Pasted",
                "score": score,
                "verdict": verdict,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.analysis_history.append(analysis)
            
            # Save to JSON
            with open(HISTORY_FILE, 'w') as f:
                json.dump(st.session_state.analysis_history, f)
            
            # Download JSON
            st.download_button(
                label="Download Analysis",
                data=json.dumps(analysis, indent=2),
                file_name="analysis_result.json",
                mime="application/json"
            )

# Dashboard Tab
if page == "Dashboard":
    st.header("Analysis History Dashboard")
    
    if st.session_state.analysis_history:
        df = pd.DataFrame(st.session_state.analysis_history)
        st.dataframe(df)
        
        # Download all analyses
        st.download_button(
            label="Download All Analyses",
            data=json.dumps(st.session_state.analysis_history, indent=2),
            file_name="all_analyses.json",
            mime="application/json"
        )
    else:
        st.write("No analyses yet. Run an analysis in the Analysis tab.")
