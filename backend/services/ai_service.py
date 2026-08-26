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

Analyze the candidate's resume against the job description.

IMPORTANT RULES:
- Never invent candidate skills.
- Never invent work experience.
- Never invent education.
- Only credit information clearly supported by the resume.
- Related technologies may receive partial credit when reasonable.
- Do not require an exact keyword match when the resume shows an
  equivalent or closely related skill.
- Evaluate internships at a student/internship level, not as senior
  engineering positions.
- Coursework, academic projects, personal projects, research,
  hackathons, and internships may count as relevant experience.
- Preferred qualifications should have less weight than required
  qualifications.

Calculate the score using this EXACT rubric:

1. Technical Skills: 0-40 points
   Compare required technical skills with the resume.
   Give reasonable partial credit for related technologies.

2. Experience and Projects: 0-25 points
   Evaluate relevant work, projects, coursework, research,
   internships, and hackathons.

3. Education: 0-15 points
   Evaluate degree and field-of-study alignment.

4. Role Relevance: 0-10 points
   Evaluate overall alignment with the type of position.

5. Preferred Qualifications: 0-10 points
   Treat preferred qualifications as bonuses.
   Missing preferred qualifications must not heavily reduce
   the candidate's score.

The match_score MUST equal:

technical_skills
+ experience_projects
+ education
+ role_relevance
+ preferred_qualifications

Score interpretation:

85-100 = Excellent Match
70-84 = Strong Match
55-69 = Possible Match
40-54 = Stretch Match
0-39 = Weak Match

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON using exactly this structure:

{{
  "match_score": 0,
  "score_breakdown": {{
    "technical_skills": 0,
    "experience_projects": 0,
    "education": 0,
    "role_relevance": 0,
    "preferred_qualifications": 0
  }},
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
        result = json.loads(ai_text)

        breakdown = result.get(
            "score_breakdown",
            {}
        )

        calculated_score = sum([
            breakdown.get("technical_skills", 0),
            breakdown.get("experience_projects", 0),
            breakdown.get("education", 0),
            breakdown.get("role_relevance", 0),
            breakdown.get("preferred_qualifications", 0),
        ])

        # Do not trust a conflicting total returned by the model.
        result["match_score"] = min(
            100,
            max(0, calculated_score)
        )

        return result

    except (json.JSONDecodeError, TypeError, ValueError):
        return {
            "match_score": 0,
            "score_breakdown": {
                "technical_skills": 0,
                "experience_projects": 0,
                "education": 0,
                "role_relevance": 0,
                "preferred_qualifications": 0,
            },
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "gaps": [],
            "recommendation": (
                "AI returned an invalid analysis response."
            ),
            "raw_response": ai_text,
        }
