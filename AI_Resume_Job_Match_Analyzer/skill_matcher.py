import re


SKILLS = [
    "python",
    "java",
    "javascript",
    "react",
    "react.js",
    "html",
    "css",
    "sql",
    "git",
    "github",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "generative ai",
    "natural language processing",
    "nlp",
    "computer vision",

    "pandas",
    "numpy",
    "scikit-learn",
    "sklearn",
    "tensorflow",
    "pytorch",
    "keras",

    "matplotlib",
    "seaborn",

    "flask",
    "fastapi",
    "streamlit",

    "aws",
    "azure",
    "google cloud",
    "gcp",

    "docker",
    "kubernetes"
]


def normalize_text(text):
    """
    Convert text to lowercase and normalize whitespace.
    """

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):
    """
    Detect known technical skills from text.
    """

    normalized_text = normalize_text(text)

    detected_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, normalized_text):
            detected_skills.append(skill)

    return sorted(set(detected_skills))


def calculate_match(resume_skills, job_skills):
    """
    Compare resume skills with skills detected in the JD.

    Returns:
        match_percentage
        matched_skills
        missing_skills
    """

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    if not job_set:
        return 0, [], []

    matched_skills = sorted(resume_set.intersection(job_set))
    missing_skills = sorted(job_set - resume_set)

    match_percentage = round(
        (len(matched_skills) / len(job_set)) * 100
    )

    return match_percentage, matched_skills, missing_skills