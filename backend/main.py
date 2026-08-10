from fastapi import FastAPI, UploadFile, File
from services.resume_parser import extract_text_from_pdf

from models.job import Job
from models.profile import Profile
from models.match_request import MatchRequest
from models.application import Application
from models.status_update import StatusUpdate



from services.job_matcher import analyze_job

from database.database import (
    create_database,
    save_application_to_db,
    get_applications_from_db,
    update_application_status,
    delete_application_from_db
)


app = FastAPI()

create_database()


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Job Agent"
    }


@app.get("/about")
def about():
    return {
        "project": "AI Job Application Agent",
        "version": "1.0",
        "purpose": "Help users find and manage job applications"
    }


@app.get("/profile")
def profile():
    return {
        "name": "Sandeep",
        "education": "Bachelor's in Computer Science",
        "career_goal": "Software Engineering, AI, Machine Learning, or GenAI Internship",
        "skills": [
            "Python",
            "FastAPI",
            "JavaScript",
            "React",
            "Vite",
            "Tailwind CSS",
            "REST APIs",
            "Machine Learning",
            "Generative AI",
            "AI Agents",
            "RAG",
            "Google Gemini",
            "Google ADK",
            "Vertex AI Search",
            "MySQL",
            "Redis",
            "Docker",
            "Google Cloud Run",
            "Git",
            "GitHub"
        ]
    }


@app.post("/profile")
def create_profile(profile: Profile):
    return {
        "message": "Profile received successfully",
        "profile": profile
    }


@app.post("/match-job")
def match_job(request: MatchRequest):

    analysis = analyze_job(
        request.job.description,
        request.profile.skills
    )

    return {
        "message": "Job matched successfully",
        "candidate": request.profile.name,
        "title": request.job.title,
        "company": request.job.company,
        **analysis
    }


@app.post("/applications")
def save_application(application: Application):

    save_application_to_db(
        application.title,
        application.company,
        application.description,
        application.status
    )

    return {
        "message": "Application saved to database",
        "application": application
    }


@app.get("/applications")
def get_applications():

    saved_applications = get_applications_from_db()

    return {
        "total_applications": len(saved_applications),
        "applications": saved_applications
    }


@app.put("/applications/{application_id}/status")
def change_application_status(
    application_id: int,
    update: StatusUpdate
):

    updated_rows = update_application_status(
        application_id,
        update.status
    )

    if updated_rows == 0:
        return {
            "message": "Application not found"
        }

    return {
        "message": "Application status updated",
        "application_id": application_id,
        "new_status": update.status
    }


@app.delete("/applications/{application_id}")
def delete_application(application_id: int):

    deleted_rows = delete_application_from_db(application_id)

    if deleted_rows == 0:
        return {
            "message": "Application not found"
        }

    return {
        "message": "Application deleted",
        "application_id": application_id
    }


@app.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):

    resume_text = extract_text_from_pdf(file.file)

    return {
        "filename": file.filename,
        "message": "Resume uploaded successfully",
        "resume_text": resume_text
    }