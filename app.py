
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import json
import os
import time
#from google.colab import drive

# Mount Google Drive (optional)
#try:
    #drive.mount('/content/Resumes.zip')
#except:
   # pass

# File paths relative to repo root
RESUME_DIR = "sample_data/resumes/Resumes"
JD_DIR = "sample_data/jds/JD"
HISTORY_FILE = "analysis_history.json"

# Rest of your app code (e.g., dropdowns, analysis, dashboard)
st.set_page_config(page_title="AI Resume Relevance Checker", layout="wide")

# Imports
import PyPDF2
import docx
import re
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
import plotly.express as px

# Imports from utils
from utils.parsing import extract_text_from_pdf, extract_text_from_docx, clean_text
from utils.matching import extract_skills, calculate_relevance_score
from utils.scoring import analyze_resume
from utils.visualization import create_score_gauge

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stDownloadButton>button {
        background-color: #008CBA;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stDownloadButton>button:hover {
        background-color: #006d87;
    }
    .stSelectbox { margin-bottom: 20px; }
    .stDataFrame { margin-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Load AI model
@st.cache_resource
def load_ai_model():
    """Load sentence transformer model"""
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return model
    except Exception as e:
        st.error(f"Could not load AI model: {e}")
        return None

# Load or initialize analysis history
def load_analysis_history():
    history_file = '/content/analysis_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

# Save analysis history
def save_analysis_history(history):
    with open('/content/analysis_history.json', 'w') as f:
        json.dump(history, f, indent=2)

def main():
    # Page setup
    st.set_page_config(
        page_title="Resume Relevance Checker",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if 'sample_jd' not in st.session_state:
        st.session_state.sample_jd = False
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = load_analysis_history()

    # Sidebar
    with st.sidebar:
        st.header("Resume Checker Settings")
        page = st.radio("Select View:", ["Analysis", "Dashboard"])
        st.markdown("---")
        if page == "Analysis":
            st.markdown("Select sample data or configure options.")
            sample_data_path = '/content/sample_data/'

            # Sample resume selector
            resume_dir = os.path.join(sample_data_path, 'resumes/Resumes/')
            resume_samples = [f for f in os.listdir(resume_dir) if f.endswith(('.pdf', '.docx'))] if os.path.exists(resume_dir) else []
            selected_resume = st.selectbox('Load Sample Resume:', ['None'] + resume_samples)

            # Sample JD selector
            jd_dir = os.path.join(sample_data_path, 'jds/JD/')
            jd_samples = [f for f in os.listdir(jd_dir) if f.endswith('.pdf')] if os.path.exists(jd_dir) else []
            selected_jd = st.selectbox('Load Sample JD:', ['None'] + jd_samples)

    # Main content
    if page == "Analysis":
        st.title("🎯 Resume Relevance Checker")
        st.markdown("### AI-Powered Job Matching for Hackathon 2025", unsafe_allow_html=True)

        # Load AI model
        with st.spinner("Loading AI model..."):
            model = load_ai_model()

        if model:
            st.success("✅ AI model loaded successfully!")
        else:
            st.warning("⚠️ Using basic scoring (AI model not available)")

        # Main interface
        col1, col2 = st.columns([1, 1])

        with col1:
            st.header("📄 Upload Resume")
            resume_file = None
            resume_text = ""
            resume_filename = "Unknown"

            # File uploader
            uploaded_file = st.file_uploader(
                "Choose your resume file",
                type=['pdf', 'docx'],
                help="Upload PDF or DOCX files"
            )

            if uploaded_file:
                resume_file = uploaded_file
                resume_filename = uploaded_file.name
                try:
                    if resume_file.type == "application/pdf":
                        resume_text = extract_text_from_pdf(resume_file)
                    elif resume_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                        resume_text = extract_text_from_docx(resume_file)

                    if resume_text and not resume_text.startswith("Error"):
                        st.success(f"✅ {resume_filename} uploaded successfully!")
                        with st.expander("Preview Resume Text"):
                            st.text_area("Content Preview", resume_text[:1000] + "...", height=200, disabled=True)
                    else:
                        st.error("Could not extract text from file")

                except Exception as e:
                    st.error(f"Error processing file: {e}")

            # Handle sample resume
            if selected_resume != 'None':
                sample_path = os.path.join(resume_dir, selected_resume)
                with open(sample_path, 'rb') as f:
                    resume_file = io.BytesIO(f.read())
                    resume_filename = selected_resume
                    resume_text = extract_text_from_pdf(resume_file) if selected_resume.endswith('.pdf') else extract_text_from_docx(resume_file)
                    st.success(f'Loaded sample: {selected_resume}')

        with col2:
            st.header("💼 Job Description")

            # Sample JD button
            if st.button("📝 Use Sample Job Description"):
                st.session_state.sample_jd = True

            if st.session_state.get('sample_jd', False):
                default_jd = """Job Title: Software Developer

Required Skills:
• Python programming (3+ years experience)
• JavaScript and React framework
• SQL database management
• REST API development
• Git version control
• Problem-solving skills

Preferred Skills:
• Machine Learning experience
• AWS cloud platform
• Docker containerization
• Agile development methodology

Qualifications:
• Bachelor's degree in Computer Science or related field
• 2+ years of software development experience
• Strong analytical and communication skills
• Experience with team collaboration tools"""
            else:
                default_jd = ""

            jd_text = st.text_area(
                "Paste job description here:",
                value=default_jd,
                height=400,
                placeholder="Include required skills, qualifications, responsibilities..."
            )

            # Handle sample JD
            if selected_jd != 'None':
                sample_jd_path = os.path.join(jd_dir, selected_jd)
                with open(sample_jd_path, 'rb') as f:
                    jd_text = extract_text_from_pdf(io.BytesIO(f.read()))

        # Analysis section
        st.markdown("---")

        if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
            if resume_file and jd_text.strip() and resume_text:
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)  # Simulate analysis
                    progress_bar.progress(i + 1)
                with st.spinner("Analyzing resume..."):
                    results = analyze_resume(resume_text, jd_text, model)

                # Save results to history
                history_entry = {
                    'resume_filename': resume_filename,
                    'jd_source': selected_jd if selected_jd != 'None' else ('Sample JD' if st.session_state.get('sample_jd', False) else 'Custom JD'),
                    'relevance_score': results['score'],
                    'verdict': results['verdict'],
                    'skills_found': ', '.join(results['found_skills']),
                    'missing_skills': ', '.join(results['missing_skills']),
                    'analysis_date': datetime.now().isoformat()
                }
                st.session_state.analysis_history.append(history_entry)
                save_analysis_history(st.session_state.analysis_history)

                # Display results
                st.header("📊 Analysis Results")

                # Main metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🎯 Relevance Score", f"{results['score']:.1f}%")
                with col2:
                    st.metric("✅ Skills Found", len(results['found_skills']))
                with col3:
                    st.metric("❌ Skills Missing", len(results['missing_skills']))

                # Verdict
                if results['verdict_color'] == 'green':
                    st.success(f"🏆 **{results['verdict']}**")
                elif results['verdict_color'] == 'orange':
                    st.warning(f"⚖️ **{results['verdict']}**")
                else:
                    st.error(f"📉 **{results['verdict']}**")

                # Score visualization
                fig = create_score_gauge(results['score'], results['verdict_color'])
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

                # Skills analysis
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Skills Found in Resume")
                    if results['found_skills']:
                        for skill in results['found_skills']:
                            st.write(f"• {skill}")
                    else:
                        st.write("No matching skills detected")

                with col2:
                    st.subheader("❌ Missing Skills")
                    if results['missing_skills']:
                        for skill in results['missing_skills']:
                            st.write(f"• {skill}")
                    else:
                        st.write("All required skills found!")

                # Suggestions
                st.subheader("💡 Improvement Suggestions")
                for i, suggestion in enumerate(results['suggestions'], 1):
                    st.write(f"**{i}.** {suggestion}")

                # Download results
                results_json = {
                    'filename': resume_filename,
                    'analysis_date': datetime.now().isoformat(),
                    'relevance_score': results['score'],
                    'verdict': results['verdict'],
                    'skills_found': results['found_skills'],
                    'missing_skills': results['missing_skills'],
                    'suggestions': results['suggestions']
                }

                st.download_button(
                    label="📥 Download Analysis Results",
                    data=json.dumps(results_json, indent=2),
                    file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

            else:
                st.error("⚠️ Please upload a resume file AND provide a job description!")

    elif page == "Dashboard":
        st.title("📊 Analysis Dashboard")
        st.markdown("### View Past Resume Analyses for Placement Team", unsafe_allow_html=True)

        if st.session_state.analysis_history:
            df = pd.DataFrame(st.session_state.analysis_history)
            df['analysis_date'] = pd.to_datetime(df['analysis_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(
                df[['resume_filename', 'jd_source', 'relevance_score', 'verdict', 'skills_found', 'missing_skills', 'analysis_date']],
                use_container_width=True,
                column_config={
                    "resume_filename": "Resume",
                    "jd_source": "JD Source",
                    "relevance_score": "Score (%)",
                    "verdict": "Verdict",
                    "skills_found": "Skills Found",
                    "missing_skills": "Missing Skills",
                    "analysis_date": "Date"
                }
            )
            # Download all results
            st.download_button(
                label="📥 Download All Analyses",
                data=json.dumps(st.session_state.analysis_history, indent=2),
                file_name=f"all_resume_analyses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("No analyses performed yet. Run an analysis to populate the dashboard.")

    # Footer
    st.markdown("---")
    st.markdown("**Submitted by Team Insight Squad | Resume Relevance Check System**", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
