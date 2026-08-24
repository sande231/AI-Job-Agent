import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Check your .env file."
    )

client = OpenAI(api_key=api_key)


def analyze_resume_and_job(
    resume_text: str,
    job_description: str
):
    prompt = f"""
You are an AI job matching assistant.

Analyze the candidate resume against the job description.

Rules:
- Never invent candidate skills.
- Never invent work experience.
- Never invent education.
- Only use information supported by the resume.
- Clearly identify strengths and gaps.
- Give a match score from 0 to 100.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON using exactly this structure:

{{
  "match_score": 0,
  "matching_skills": [],
  "missing_skills": [],
  "strengths": [],
  "gaps": [],
  "recommendation": ""
}}
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt,
        store=False
    )

    ai_text = response.output_text

    try:
        return json.loads(ai_text)

    except json.JSONDecodeError:
        return {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "gaps": [],
            "recommendation": "AI returned an invalid JSON response.",
            "raw_response": ai_text
        }