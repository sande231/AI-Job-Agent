import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

_client = None


def _get_client():
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. Check your .env file."
        )

    _client = OpenAI(api_key=api_key)
    return _client


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

    response = _get_client().responses.create(
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


def generate_application_materials(
    resume_text: str,
    job_title: str,
    company: str,
    job_description: str,
):
    prompt = f"""
You are an AI job application assistant.

Create application materials using ONLY information supported by
the candidate's resume and the job description.

STRICT RULES:
- Never invent skills.
- Never invent work experience.
- Never invent projects.
- Never invent education.
- Never invent achievements, metrics, dates, certifications,
  publications, or leadership experience.
- Do not claim experience with a technology unless the resume
  clearly supports it.
- If the job requires something missing from the resume, mention
  it only as a gap or learning area.
- Keep the tone professional and appropriate for a student or
  internship applicant.
- The cover letter must be a draft for the user to review.
- Do not claim that an application was submitted.

CANDIDATE RESUME:
{resume_text}

JOB TITLE:
{job_title}

COMPANY:
{company}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON using exactly this structure:

{{
  "cover_letter": "",
  "resume_suggestions": [],
  "skills_to_emphasize": []
}}
"""

    response = _get_client().responses.create(
        model="gpt-5",
        input=prompt,
        store=False,
    )

    ai_text = response.output_text

    try:
        return json.loads(ai_text)

    except json.JSONDecodeError:
        return {
            "cover_letter": "",
            "resume_suggestions": [],
            "skills_to_emphasize": [],
            "error": "AI returned an invalid JSON response.",
            "raw_response": ai_text,
        }


def generate_interview_preparation(
    resume_text: str,
    job_title: str,
    company: str,
    job_description: str,
):
    prompt = f"""
You are an AI interview preparation assistant.

Prepare the candidate for an interview using ONLY information
supported by the resume and the job description.

STRICT RULES:
- Never invent candidate experience.
- Never invent candidate skills.
- Never invent projects.
- Never invent education.
- Do not claim the candidate knows a technology unless the
  resume supports it.
- Questions should be realistic for a student/internship role.
- Use the candidate's real projects when suggesting talking points.
- Clearly identify technical areas that should be reviewed.
- Do not create fake interview history or achievements.

RESUME:
{resume_text}

JOB TITLE:
{job_title}

COMPANY:
{company}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON using exactly this structure:

{{
  "likely_interview_questions": [],
  "technical_topics_to_review": [],
  "project_talking_points": [],
  "questions_to_ask_interviewer": [],
  "preparation_advice": []
}}
"""

    response = _get_client().responses.create(
        model="gpt-5",
        input=prompt,
        store=False,
    )

    ai_text = response.output_text

    try:
        return json.loads(ai_text)

    except json.JSONDecodeError:
        return {
            "likely_interview_questions": [],
            "technical_topics_to_review": [],
            "project_talking_points": [],
            "questions_to_ask_interviewer": [],
            "preparation_advice": [],
            "error": "AI returned an invalid JSON response.",
            "raw_response": ai_text,
        }


def generate_application_form_answers(
    resume_text: str,
    job_title: str,
    company: str,
    job_description: str,
):
    prompt = f"""
You are an AI job application assistant.

Create draft answers for common job application questions using
ONLY information supported by the candidate's resume and the
job description.

STRICT RULES:
- Never invent skills.
- Never invent work experience.
- Never invent projects.
- Never invent education.
- Never invent achievements, metrics, certifications, dates,
  publications, or leadership experience.
- Do not answer legal or sensitive personal questions.
- Work authorization, visa sponsorship, demographic information,
  disability status, veteran status, criminal-history questions,
  legal attestations, and similar fields MUST be marked:
  "USER INPUT REQUIRED".
- Do not claim the application has been submitted.
- Keep answers concise, professional, and suitable for an internship
  or student application.
- Tailor normal answers to the specific role and company.

RESUME:
{resume_text}

JOB TITLE:
{job_title}

COMPANY:
{company}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON using exactly this structure:

{{
  "why_this_role": "",
  "why_this_company": "",
  "relevant_experience": "",
  "projects_to_highlight": [],
  "skills_to_highlight": [],
  "short_professional_summary": "",
  "work_authorization": "USER INPUT REQUIRED",
  "visa_sponsorship": "USER INPUT REQUIRED",
  "demographic_questions": "USER INPUT REQUIRED",
  "legal_attestations": "USER INPUT REQUIRED"
}}
"""

    response = _get_client().responses.create(
        model="gpt-5",
        input=prompt,
        store=False,
    )

    ai_text = response.output_text

    try:
        return json.loads(ai_text)

    except json.JSONDecodeError:
        return {
            "why_this_role": "",
            "why_this_company": "",
            "relevant_experience": "",
            "projects_to_highlight": [],
            "skills_to_highlight": [],
            "short_professional_summary": "",
            "work_authorization": "USER INPUT REQUIRED",
            "visa_sponsorship": "USER INPUT REQUIRED",
            "demographic_questions": "USER INPUT REQUIRED",
            "legal_attestations": "USER INPUT REQUIRED",
            "error": "AI returned an invalid JSON response.",
            "raw_response": ai_text,
        }
