
from utils.matching import extract_skills, calculate_relevance_score

def analyze_resume(resume_text, jd_text, model=None):
    """Complete resume analysis"""

    # Skills database
    skills_database = [
        'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Node.js',
        'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'AWS', 'Azure',
        'Machine Learning', 'Data Science', 'AI', 'Deep Learning',
        'Docker', 'Kubernetes', 'Git', 'Linux', 'HTML', 'CSS',
        'C++', 'C#', 'Django', 'Flask', 'TensorFlow', 'PyTorch',
        'Pandas', 'NumPy', 'Scikit-learn', 'REST API', 'GraphQL'
    ]

    # Calculate relevance score
    score = calculate_relevance_score(resume_text, jd_text, model)

    # Determine verdict
    if score >= 70:
        verdict = "High Suitability"
        color = "green"
    elif score >= 40:
        verdict = "Medium Suitability"
        color = "orange"
    else:
        verdict = "Low Suitability"
        color = "red"

    # Extract skills
    resume_skills = extract_skills(resume_text, skills_database)
    jd_skills = extract_skills(jd_text, skills_database)
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

    # Generate suggestions
    suggestions = []
    if missing_skills:
        suggestions.append(f"Consider adding these skills: {', '.join(missing_skills[:5])}")
    if score < 40:
        suggestions.append("Add more relevant projects and experience")
        suggestions.append("Include more technical keywords from the job description")
    elif score < 70:
        suggestions.append("Highlight relevant projects more prominently")
        suggestions.append("Add certifications related to the role")
    else:
        suggestions.append("Great match! Consider adding recent projects")

    return {
        'score': score,
        'verdict': verdict,
        'verdict_color': color,
        'found_skills': resume_skills,
        'missing_skills': missing_skills,
        'suggestions': suggestions
    }
