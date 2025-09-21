
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.parsing import clean_text

def extract_skills(text, skills_list):
    """Extract skills from text"""
    found_skills = []
    text_lower = text.lower()

    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills

def calculate_relevance_score(resume_text, jd_text, model=None):
    """Calculate relevance score"""
    try:
        if model:
            # AI-powered scoring
            resume_clean = clean_text(resume_text)
            jd_clean = clean_text(jd_text)

            # TF-IDF similarity
            vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
            tfidf_matrix = vectorizer.fit_transform([jd_clean, resume_clean])
            keyword_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

            # Semantic similarity
            embeddings = model.encode([resume_clean, jd_clean])
            semantic_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

            # Combined score
            final_score = (keyword_score * 0.4 + semantic_score * 0.6) * 100

        else:
            # Basic word overlap scoring
            resume_words = set(clean_text(resume_text).split())
            jd_words = set(clean_text(jd_text).split())

            if not jd_words:
                final_score = 0
            else:
                common_words = resume_words.intersection(jd_words)
                final_score = (len(common_words) / len(jd_words)) * 100

        return min(final_score, 100)

    except Exception as e:
        return 0
