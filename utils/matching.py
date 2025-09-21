# utils/matching.py
from sentence_transformers import SentenceTransformer, util

def extract_skills(text):
    """Extract skills from text using a simple keyword-based approach."""
    # Placeholder: Replace with your actual skill extraction logic
    model = SentenceTransformer('all-MiniLM-L6-v2')
    skill_keywords = ['python', 'java', 'sql', 'machine learning', 'communication', 'teamwork']
    skills = [skill for skill in skill_keywords if skill.lower() in text.lower()]
    return skills

def match_skills(resume_skills, jd_skills):
    """Match resume skills with JD skills."""
    matched = [skill for skill in resume_skills if skill in jd_skills]
    missing = [skill for skill in jd_skills if skill not in resume_skills]
    return matched, missing
