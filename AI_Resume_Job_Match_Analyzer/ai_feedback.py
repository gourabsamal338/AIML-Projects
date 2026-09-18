import os

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env
load_dotenv()


def generate_ai_feedback(
    resume_text,
    job_description,
    match_percentage,
    matched_skills,
    missing_skills
):
    """
    Generate personalized resume/job feedback using OpenAI.

    Args:
        resume_text (str): Extracted resume text
        job_description (str): Job description provided by user
        match_percentage (int): Deterministic skill match score
        matched_skills (list): Skills found in both resume and JD
        missing_skills (list): Skills found in JD but not resume

    Returns:
        str: AI-generated career feedback
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "OpenAI API key not found. "
            "Please configure OPENAI_API_KEY in your .env file."
        )

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an AI career assistant helping a student understand how their
resume aligns with a job description.

IMPORTANT RULES:

1. Use only the resume and job description provided.
2. Do not invent qualifications, projects, skills, or experience.
3. Do not claim that the candidate will or will not get the job.
4. The match percentage below was calculated separately using
   deterministic technical-skill overlap.
5. Do not modify, recalculate, or reinterpret the match score.
6. Give practical and concise recommendations.
7. If a skill is missing, recommend learning or demonstrating it
   through a project. Never suggest falsely adding it to the resume.
8. Base strengths only on evidence present in the resume.

MATCH ANALYSIS

Technical Skill Match:
{match_percentage}%

Matched Skills:
{", ".join(matched_skills) if matched_skills else "None detected"}

Missing Skills:
{", ".join(missing_skills) if missing_skills else "None detected"}

--------------------
RESUME
--------------------

{resume_text}

--------------------
JOB DESCRIPTION
--------------------

{job_description}

Return your response using exactly these sections:

## Overall Analysis
Give a concise 2-3 sentence assessment.

## Strengths
Identify 3-5 relevant strengths supported by the resume.

## Gaps
Identify the most important gaps relative to the job description.

## Recommended Next Steps
Give 4 specific actions the candidate can take.

## Suggested Project
Recommend one small practical project that could help demonstrate
one or more missing skills.

## Interview Questions
Generate 5 interview questions relevant to this candidate and
the job description.
"""

    try:

        response = client.responses.create(
            model="gpt-5.5",
            input=prompt
        )

        return response.output_text

    except Exception as e:

        return (
            "Unable to generate AI feedback.\n\n"
            f"Error: {str(e)}"
        )