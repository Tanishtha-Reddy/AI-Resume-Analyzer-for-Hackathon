# utils/scoring.py
from sentence_transformers import SentenceTransformer, util
from utils.matching import extract_skills  # Import only extract_skills

def calculate_relevance_score(resume_text, jd_text):
    """Calculate relevance score between resume and JD."""
    # Placeholder: Replace with your actual scoring logic
    model = SentenceTransformer('all-MiniLM-L6-v2')
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    similarity = util.cos_sim(resume_embedding, jd_embedding)[0][0]
    score = similarity.item() * 100
    return score
