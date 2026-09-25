from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from services.email_service import (
    build_application_report,
    build_interview_reminder,
    send_email,
    get_recent_emails,
)

from services.reminder_service import (
    is_within_24_hours,
    get_hours_until_interview,
)

from services.scheduler_service import (
    start_scheduler,
    stop_scheduler,
    scheduler,
)

from services.date_extractor import (
    extract_interview_date,
    normalize_interview_date,
)

from services.job_discovery_service import (
    get_sample_internships,
    search_internships,
    search_multiple_internship_categories,
)
from services.resume_parser import extract_text_from_pdf
from services.skill_extractor import extract_skills
from services.experience_extractor import extract_experience
from services.profile_extractor import extract_basic_profile
from services.project_extractor import extract_projects
from services.job_matcher import analyze_job
from services.application_matcher import match_email_to_application
from services.ai_service import (
    analyze_resume_and_job,
    generate_application_materials,
)
from services.contact_extractor import extract_contact_info
from services.ats_detector import detect_ats_platform
from services.apply_adapters import get_adapter_for_url

from services.profile_store import (
    save_resume_profile,
    get_resume_profile,
    get_resume_text,
)

from services.email_classifier import (
    is_job_related_email,
    classify_job_email,
)
from models.discovered_job import DiscoveredJob
from models.job import Job
from models.profile import Profile
from models.match_request import MatchRequest
from models.application import Application
from models.status_update import StatusUpdate
from models.interview_update import InterviewUpdate
from models.resume_profile import ResumeProfile
from models.notes_update import NotesUpdate

from database.database import (
    create_database,
    save_application_to_db,
    get_applications_from_db,
    get_application_by_id,
    update_application_status,
    delete_application_from_db,
    create_resume_profile_table,
    save_resume_profile_to_db,
    get_resume_profile_from_db,
    get_application_summary,
    get_upcoming_events,
    create_processed_emails_table,
    is_email_processed,
    mark_email_as_processed,
    update_application_interview_date,
    get_upcoming_interviews,
    create_interview_reminders_table,
    is_interview_reminder_sent,
    mark_interview_reminder_sent,
    create_discovered_jobs_table,
    save_discovered_job_to_db,
    get_discovered_jobs_from_db,
    discovered_job_exists,
    get_discovered_job_by_id,
    update_discovered_job_status,
    update_application_notes,
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    start_scheduler()


@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()


create_database()
create_resume_profile_table()
create_processed_emails_table()
create_interview_reminders_table()
create_discovered_jobs_table()
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
        "purpose": "Help users find and manage job applications",
    }


@app.get("/profile")
def profile():
    # First try the profile currently stored in memory
    saved_profile = get_resume_profile()

    if saved_profile is not None:
        return {
            "name": saved_profile.name,
            "education": saved_profile.education,
            "career_goal": saved_profile.career_goal,
            "skills": saved_profile.skills,
            "experience": saved_profile.experience,
            "projects": saved_profile.projects,
            "email": saved_profile.email,
            "phone": saved_profile.phone,
            "linkedin_url": saved_profile.linkedin_url,
        }

    # If the server restarted, load the latest profile
    # from SQLite instead
    db_profile = get_resume_profile_from_db()

    if db_profile is not None:
        return {
            "name": db_profile["name"],
            "education": db_profile["education"],
            "career_goal": db_profile["career_goal"],
            "skills": db_profile["skills"],
            "experience": db_profile["experience"],
            "projects": db_profile["projects"],
            "email": db_profile["email"],
            "phone": db_profile["phone"],
            "linkedin_url": db_profile["linkedin_url"],
        }

    return {
        "message": (
            "No resume profile found. "
            "Please upload a resume first."
        ),
        "name": "",
        "education": "",
        "career_goal": "",
        "skills": [],
        "experience": [],
        "projects": [],
        "email": "",
        "phone": "",
        "linkedin_url": "",
    }


@app.post("/profile")
def create_profile(profile: Profile):
    return {
        "message": "Profile received successfully",
        "profile": profile,
    }


@app.post("/match-job")
def match_job(request: MatchRequest):
    analysis = analyze_job(
        request.job.description,
        request.profile.skills,
    )

    return {
        "message": "Job matched successfully",
        "candidate": request.profile.name,
        "title": request.job.title,
        "company": request.job.company,
        **analysis,
    }


@app.post("/applications")
def save_application(application: Application):
    save_application_to_db(
        application.title,
        application.company,
        application.description,
        application.status,
        application.job_url,
        application.match_score,
        application.location,
        application.date_applied,
        application.interview_date,
        application.deadline,
        application.notes,
    )

    return {
        "message": "Application saved to database",
        "application": application,
    }


@app.get("/applications")
def get_applications():
    saved_applications = get_applications_from_db()

    return {
        "total_applications": len(saved_applications),
        "applications": saved_applications,
    }



@app.post("/applications/{application_id}/generate-materials")
def generate_application_materials_endpoint(application_id: int):
    application = get_application_by_id(application_id)

    if application is None:
        return {
            "message": "Application not found",
            "application_id": application_id,
        }

    saved_resume_text = get_resume_text()

    if saved_resume_text is None:
        db_profile = get_resume_profile_from_db()

        if db_profile is None:
            return {
                "message": "Please upload your resume first."
            }

        saved_resume_text = db_profile["resume_text"]

    materials = generate_application_materials(
        resume_text=saved_resume_text,
        job_title=application["title"],
        company=application["company"],
        job_description=application["description"],
    )

    return {
        "message": "Application materials generated successfully",
        "application_id": application_id,
        "title": application["title"],
        "company": application["company"],
        "materials": materials,
    }


@app.put("/applications/{application_id}/status")
def change_application_status(
    application_id: int,
    update: StatusUpdate,
):
    allowed_statuses = {
        "Saved",
        "Applied",
        "Assessment",
        "Interview",
        "Offer",
        "Rejected",
    }

    new_status = update.status.strip()

    if new_status not in allowed_statuses:
        return {
            "message": "Invalid application status",
            "allowed_statuses": sorted(allowed_statuses),
        }

    updated_rows = update_application_status(
        application_id,
        new_status,
    )

    if updated_rows == 0:
        return {
            "message": "Application not found",
            "application_id": application_id,
        }

    return {
        "message": "Application status updated successfully",
        "application_id": application_id,
        "new_status": new_status,
    }

@app.put("/applications/{application_id}/notes")
def update_application_notes_endpoint(
    application_id: int,
    update: NotesUpdate,
):
    updated_rows = update_application_notes(
        application_id,
        update.notes,
    )

    if updated_rows == 0:
        return {
            "message": "Application not found",
            "application_id": application_id,
        }

    return {
        "message": "Application notes updated successfully",
        "application_id": application_id,
        "notes": update.notes,
    }

@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    deleted_rows = delete_application_from_db(
        application_id
    )

    if deleted_rows == 0:
        return {
            "message": "Application not found"
        }

    return {
        "message": "Application deleted",
        "application_id": application_id,
    }

@app.post("/discovered-jobs")
def save_discovered_job(job: DiscoveredJob):
    save_discovered_job_to_db(
        job.title,
        job.company,
        job.description,
        job.location,
        job.job_url,
        job.source,
        job.match_score,
        job.status,
    )

    return {
        "message": "Discovered job saved successfully",
        "job": job,
    }


@app.get("/discovered-jobs")
def get_discovered_jobs():
    jobs = get_discovered_jobs_from_db()

    return {
        "message": "Discovered jobs retrieved successfully",
        "total_jobs": len(jobs),
        "jobs": jobs,
    }


@app.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...)
):
    resume_text = extract_text_from_pdf(
        file.file
    )

    detected_skills = extract_skills(
        resume_text
    )

    basic_profile = extract_basic_profile(
        resume_text
    )

    detected_experience = extract_experience(
        resume_text
    )

    detected_projects = extract_projects(
        resume_text
    )

    contact_info = extract_contact_info(
        resume_text
    )

    auto_profile = ResumeProfile(
        name=basic_profile["name"],
        education=basic_profile["education"],
        career_goal=(
            "Software Engineering, AI, Machine Learning, "
            "or GenAI Internship"
        ),
        skills=detected_skills,
        experience=detected_experience,
        projects=detected_projects,
        email=contact_info["email"],
        phone=contact_info["phone"],
        linkedin_url=contact_info["linkedin_url"],
    )

    save_resume_profile(
        auto_profile,
        resume_text,
    )

    save_resume_profile_to_db(
        auto_profile,
        resume_text,
    )

    return {
        "filename": file.filename,
        "message": (
            "Resume uploaded and profile "
            "created successfully"
        ),
        "resume_text": resume_text,
        "profile": auto_profile,
    }


@app.post("/ai-match")
def ai_match(job: Job):
    saved_profile = get_resume_profile()
    saved_resume_text = get_resume_text()

    if (
        saved_profile is None
        or saved_resume_text is None
    ):
        db_profile = get_resume_profile_from_db()

        if db_profile is None:
            return {
                "message": "Please upload your resume first."
            }

        saved_profile = ResumeProfile(
            name=db_profile["name"],
            education=db_profile["education"],
            career_goal=db_profile["career_goal"],
            skills=db_profile["skills"],
            experience=db_profile["experience"],
            projects=db_profile["projects"],
        )

        saved_resume_text = db_profile[
            "resume_text"
        ]

        save_resume_profile(
            saved_profile,
            saved_resume_text,
        )

    ai_analysis = analyze_resume_and_job(
        saved_resume_text,
        job.description,
    )

    return {
        "message": (
            "AI job analysis completed successfully"
        ),
        "candidate": saved_profile.name,
        "job_title": job.title,
        "company": job.company,
        "profile": saved_profile,
        "ai_analysis": ai_analysis,
    }


@app.get("/applications/summary")
def application_summary():
    summary = get_application_summary()

    return {
        "message": (
            "Application summary retrieved successfully"
        ),
        "summary": summary,
    }


@app.get("/applications/upcoming")
def upcoming_applications():
    events = get_upcoming_events()

    return {
        "message": (
            "Upcoming application events "
            "retrieved successfully"
        ),
        "total_events": len(events),
        "events": events,
    }


@app.get("/reports/daily")
def daily_report():
    summary = get_application_summary()
    events = get_upcoming_events()

    report = build_application_report(
        summary,
        events,
    )

    return {
        "message": (
            "Daily application report "
            "generated successfully"
        ),
        "report": report,
    }


@app.post("/reports/send")
def send_daily_report():
    summary = get_application_summary()
    events = get_upcoming_events()

    report = build_application_report(
        summary,
        events,
    )

    result = send_email(
        to_email="Sandeepshah2054@gmail.com",
        subject=(
            "AI Job Agent - "
            "Internship Application Report"
        ),
        body=report,
    )

    return {
        "message": (
            "Daily application report "
            "sent successfully"
        ),
        "email_result": result,
    }


@app.get("/emails/recent")
def recent_emails():
    emails = get_recent_emails(
        max_results=10
    )

    return {
        "message": (
            "Recent emails retrieved successfully"
        ),
        "total_emails": len(emails),
        "emails": emails,
    }


@app.get("/emails/job-related")
def job_related_emails():
    emails = get_recent_emails(
        max_results=50
    )

    job_emails = []

    for email in emails:
        if is_job_related_email(email):
            job_emails.append({
                **email,
                "detected_status":
                    classify_job_email(email),
            })

    return {
        "message": (
            "Job-related emails retrieved successfully"
        ),
        "total_job_emails": len(job_emails),
        "emails": job_emails,
    }


@app.get("/emails/match-preview")
def email_match_preview():
    emails = get_recent_emails(
        max_results=50
    )

    applications = get_applications_from_db()

    results = []

    for email in emails:
        if not is_job_related_email(email):
            continue

        detected_status = classify_job_email(
            email
        )

        match = match_email_to_application(
            email,
            applications,
        )

        results.append({
            "email_subject":
                email.get("subject"),
            "email_from":
                email.get("from"),
            "detected_status":
                detected_status,
            "matched_application": (
                match["application"]
                if match
                else None
            ),
            "match_score": (
                match["match_score"]
                if match
                else 0
            ),
        })

    return {
        "message": (
            "Email/application matching "
            "preview completed"
        ),
        "total_matches": len(results),
        "results": results,
    }


@app.post("/emails/process")
def process_job_emails():
    emails = get_recent_emails(
        max_results=50
    )

    applications = get_applications_from_db()

    processed = []
    skipped = []

    for email in emails:
        gmail_message_id = email.get("id")

        # Ignore emails already processed
        if is_email_processed(
            gmail_message_id
        ):
            skipped.append({
                "email_id": gmail_message_id,
                "reason": "Already processed",
            })

            continue

        # Ignore non-job emails
        if not is_job_related_email(email):
            continue

        detected_status = classify_job_email(
            email
        )

        match = match_email_to_application(
            email,
            applications,
        )

        # No application match
        if not match:
            skipped.append({
                "email_id": gmail_message_id,
                "subject": email.get("subject"),
                "reason": (
                    "No matching application"
                ),
            })

            continue

        match_score = match["match_score"]
        application = match["application"]

        # Require strong match
        if match_score < 5:
            skipped.append({
                "email_id": gmail_message_id,
                "subject": email.get("subject"),
                "reason": (
                    "Match confidence too low"
                ),
                "match_score": match_score,
            })

            continue

        # Ignore unclear email status
        if detected_status == "Other":
            skipped.append({
                "email_id": gmail_message_id,
                "subject": email.get("subject"),
                "reason": (
                    "No clear application "
                    "status detected"
                ),
            })

            continue

        updated_rows = update_application_status(
            application["id"],
            detected_status,
        )

        interview_date = None

        # Extract interview date if applicable
        if detected_status == "Interview":
            raw_interview_date = extract_interview_date(
                email
            )

            interview_date = normalize_interview_date(
                raw_interview_date
                )

            if interview_date:
                update_application_interview_date(
                    application["id"],
                    interview_date,
                )

        if updated_rows > 0:
            mark_email_as_processed(
                gmail_message_id
            )

            processed.append({
                "email_id":
                    gmail_message_id,
                "subject":
                    email.get("subject"),
                "application_id":
                    application["id"],
                "company":
                    application["company"],
                "title":
                    application["title"],
                "old_status":
                    application["status"],
                "new_status":
                    detected_status,
                "interview_date":
                    interview_date,
                "match_score":
                    match_score,
            })

    return {
        "message": (
            "Job emails processed successfully"
        ),
        "updated_applications":
            len(processed),
        "processed":
            processed,
        "skipped":
            skipped,
    }


@app.get("/interviews/upcoming")
def upcoming_interviews():
    interviews = get_upcoming_interviews()

    return {
        "message": "Upcoming interviews retrieved successfully",
        "total_interviews": len(interviews),
        "interviews": interviews,
    }



@app.post("/interviews/send-reminders")
def send_interview_reminders():
    interviews = get_upcoming_interviews()

    sent_reminders = []
    skipped = []

    for interview in interviews:
        interview_date = interview["interview_date"]

        if not is_within_24_hours(interview_date):
            skipped.append({
                "company": interview["company"],
                "title": interview["title"],
                "interview_date": interview_date,
                "reason": "Interview is not within 24 hours",
            })
            continue

        already_sent = is_interview_reminder_sent(
            interview["id"],
            interview_date,
            "24_hour",
        )

        if already_sent:
            skipped.append({
                "company": interview["company"],
                "title": interview["title"],
                "interview_date": interview_date,
                "reason": "24-hour reminder already sent",
            })
            continue

        hours_remaining = get_hours_until_interview(
            interview_date
        )

        reminder = build_interview_reminder(
            interview
        )

        result = send_email(
            to_email="Sandeepshah2054@gmail.com",
            subject=(
                f"Interview Reminder - "
                f"{interview['company']} "
                f"{interview['title']}"
            ),
            body=reminder,
        )

        mark_interview_reminder_sent(
            interview["id"],
            interview_date,
            "24_hour",
        )

        sent_reminders.append({
            "company": interview["company"],
            "title": interview["title"],
            "interview_date": interview_date,
            "hours_remaining": hours_remaining,
            "email_result": result,
        })

    return {
        "message": "Interview reminder check completed",
        "total_sent": len(sent_reminders),
        "sent_reminders": sent_reminders,
        "skipped": skipped,
    }


@app.get("/scheduler/status")
def scheduler_status():
    jobs = scheduler.get_jobs()

    return {
        "running": scheduler.running,
        "total_jobs": len(jobs),
        "jobs": [
            {
                "id": job.id,
                "next_run_time": (
                    str(job.next_run_time)
                    if job.next_run_time
                    else None
                ),
            }
            for job in jobs
        ],
    }

@app.get("/jobs/discover-preview")
def discover_jobs_preview():
    jobs = get_sample_internships()

    return {
        "message": "Internship discovery preview completed",
        "total_jobs": len(jobs),
        "jobs": jobs,
    }


@app.post("/jobs/discover-and-save")
def discover_and_save_jobs():
    saved_profile = get_resume_profile()
    saved_resume_text = get_resume_text()

    if saved_profile is None or saved_resume_text is None:
        db_profile = get_resume_profile_from_db()

        if db_profile is None:
            return {
                "message": "Please upload your resume first."
            }

        saved_profile = ResumeProfile(
            name=db_profile["name"],
            education=db_profile["education"],
            career_goal=db_profile["career_goal"],
            skills=db_profile["skills"],
            experience=db_profile["experience"],
            projects=db_profile["projects"],
        )

        saved_resume_text = db_profile["resume_text"]

        save_resume_profile(
            saved_profile,
            saved_resume_text,
        )

    jobs = get_sample_internships()

    saved_jobs = []
    skipped_jobs = []

    for job in jobs:
        analysis = analyze_resume_and_job(
            saved_resume_text,
            job["description"],
        )

        match_score = analysis.get(
            "match_score",
            0,
        )

        if match_score >= 70:

            if discovered_job_exists(
                job["title"],
                job["company"],
                job["location"],
            ):
                skipped_jobs.append({
                    **job,
                    "match_score": match_score,
                    "reason": "Job already discovered",
                })

                continue

            save_discovered_job_to_db(
                title=job["title"],
                company=job["company"],
                description=job["description"],
                location=job["location"],
                job_url=job["job_url"],
                source=job["source"],
                match_score=match_score,
                status="Discovered",
            )

            saved_jobs.append({
                **job,
                "match_score": match_score,
            })

        else:
            skipped_jobs.append({
                **job,
                "match_score": match_score,
                "reason": "Match score below 70",
            })

    return {
        "message": "Job discovery and saving completed",
        "candidate": saved_profile.name,
        "saved_count": len(saved_jobs),
        "skipped_count": len(skipped_jobs),
        "saved_jobs": saved_jobs,
        "skipped_jobs": skipped_jobs,
    }

@app.get("/jobs/live-preview")
def live_jobs_preview():
    try:
        jobs = search_internships(
            keyword="software engineering intern",
            results_per_page=10,
        )

        return {
            "message": "Live internships retrieved successfully",
            "total_jobs": len(jobs),
            "jobs": jobs,
        }

    except Exception as error:
        return {
            "message": "Unable to retrieve live internships",
            "error": str(error),
        }



@app.post("/jobs/live-discover-and-save")
def live_discover_and_save_jobs():
    saved_profile = get_resume_profile()
    saved_resume_text = get_resume_text()

    # Load resume from database if it is not in memory
    if saved_profile is None or saved_resume_text is None:
        db_profile = get_resume_profile_from_db()

        if db_profile is None:
            return {
                "message": "Please upload your resume first."
            }

        saved_profile = ResumeProfile(
            name=db_profile["name"],
            education=db_profile["education"],
            career_goal=db_profile["career_goal"],
            skills=db_profile["skills"],
            experience=db_profile["experience"],
            projects=db_profile["projects"],
        )

        saved_resume_text = db_profile["resume_text"]

        save_resume_profile(
            saved_profile,
            saved_resume_text,
        )

    # Get real internships from Adzuna
    jobs = search_multiple_internship_categories(
        results_per_category=1,
    )

    saved_jobs = []
    skipped_jobs = []

    for job in jobs:

        # Check duplicate BEFORE calling OpenAI
        if discovered_job_exists(
            job["title"],
            job["company"],
            job.get("location"),
        ):
            skipped_jobs.append({
                **job,
                "reason": "Job already discovered",
            })
            continue

        # AI resume/job analysis
        analysis = analyze_resume_and_job(
            saved_resume_text,
            job["description"],
        )

        match_score = analysis.get(
            "match_score",
            0,
        )

        # 70-100 = Strong match
        if match_score >= 70:
            status = "Discovered"

        # 55-69 = Worth reviewing
        elif match_score >= 55:
            status = "Review"

        # Below 55 = Skip
        else:
            skipped_jobs.append({
                **job,
                "match_score": match_score,
                "reason": "Match score below review threshold",
            })
            continue

        # Save strong/review jobs
        discovered_job_id = save_discovered_job_to_db(
            title=job["title"],
            company=job["company"],
            description=job["description"],
            location=job["location"],
            job_url=job["job_url"],
            source=job["source"],
            match_score=match_score,
            status=status,
        )

        saved_jobs.append({
            "id": discovered_job_id,
            **job,
            "match_score": match_score,
            "status": status,
            "score_breakdown": analysis.get(
                "score_breakdown",
                {},
            ),
            "matching_skills": analysis.get(
                "matching_skills",
                [],
            ),
            "missing_skills": analysis.get(
                "missing_skills",
                [],
            ),
            "recommendation": analysis.get(
                "recommendation",
                "",
            ),
        })

    return {
        "message": "Live internship discovery completed",
        "candidate": saved_profile.name,
        "jobs_checked": len(jobs),
        "saved_count": len(saved_jobs),
        "skipped_count": len(skipped_jobs),
        "saved_jobs": saved_jobs,
        "skipped_jobs": skipped_jobs,
    }

@app.post("/discovered-jobs/{job_id}/apply")
def apply_to_discovered_job(job_id: int):
    job = get_discovered_job_by_id(job_id)

    if job is None:
        return {
            "message": "Discovered job not found"
        }

    # Prevent moving the same job twice
    if job["status"] == "Applied":
        return {
            "message": "This discovered job has already been moved to applications",
            "job_id": job_id,
        }

    application_id = save_application_to_db(
        title=job["title"],
        company=job["company"],
        description=job["description"],
        status="Applied",
        job_url=job["job_url"],
        match_score=job["match_score"],
        location=job["location"],
        date_applied=datetime.now().strftime("%Y-%m-%d"),
        interview_date=None,
        deadline=None,
        notes=(
            "Moved from discovered jobs. "
            f"Source: {job['source']}"
        ),
    )

    update_discovered_job_status(
        job_id,
        "Applied",
    )

    return {
        "message": "Job moved to applications successfully",
        "discovered_job_id": job_id,
        "application_id": application_id,
        "company": job["company"],
        "title": job["title"],
        "match_score": job["match_score"],
        "status": "Applied",
    }


@app.post("/discovered-jobs/{job_id}/prepare-application")
def prepare_application_for_discovered_job(job_id: int):
    """
    Preview what an auto-filled application would contain for this
    job, using whichever ATS adapter matches its job_url. This does
    NOT submit anything anywhere - it only shows what would be
    sent, and flags anything missing, so submission stays an
    explicit, separate, human-reviewed step.
    """
    job = get_discovered_job_by_id(job_id)

    if job is None:
        return {
            "message": "Discovered job not found"
        }

    job_url = job["job_url"]
    platform = detect_ats_platform(job_url)
    adapter = get_adapter_for_url(job_url)

    if adapter is None:
        return {
            "job_id": job_id,
            "job_url": job_url,
            "ats_platform": platform,
            "supported": False,
            "message": (
                f"No auto-apply adapter for '{platform}' yet - "
                "this one needs a manual application."
            ),
        }

    saved_profile = get_resume_profile()

    if saved_profile is not None:
        profile = saved_profile.dict()
        profile["resume_text"] = get_resume_text()
    else:
        profile = get_resume_profile_from_db()

    if profile is None:
        return {
            "job_id": job_id,
            "job_url": job_url,
            "ats_platform": platform,
            "supported": True,
            "message": (
                "No resume profile found - upload a resume before "
                "preparing an application."
            ),
        }

    prepared = adapter.prepare_application(job_url, profile)

    return {
        "job_id": job_id,
        "job_url": job_url,
        "supported": True,
        **prepared.to_dict(),
    }


@app.put("/applications/{application_id}/interview")
def set_application_interview(
    application_id: int,
    update: InterviewUpdate,
):
    applications = get_applications_from_db()

    application = next(
        (
            app
            for app in applications
            if app["id"] == application_id
        ),
        None,
    )

    if application is None:
        return {
            "message": "Application not found",
            "application_id": application_id,
        }

    update_application_status(
        application_id,
        "Interview",
    )

    updated_rows = update_application_interview_date(
        application_id,
        update.interview_date,
    )

    if updated_rows == 0:
        return {
            "message": "Unable to update interview date",
            "application_id": application_id,
        }

    return {
        "message": "Interview scheduled successfully",
        "application_id": application_id,
        "company": application["company"],
        "title": application["title"],
        "status": "Interview",
        "interview_date": update.interview_date,
    }


@app.get("/dashboard")
def get_dashboard():
    summary = get_application_summary()
    upcoming_interviews = get_upcoming_interviews()
    discovered_jobs = get_discovered_jobs_from_db()
    applications = get_applications_from_db()

    available_jobs = [
        job
        for job in discovered_jobs
        if job["status"] in {
            "Discovered",
            "Review",
        }
    ]

    top_discovered_jobs = sorted(
        available_jobs,
        key=lambda job: (
            job["match_score"]
            if job["match_score"] is not None
            else 0
        ),
        reverse=True,
    )[:5]

    recent_applications = applications[:5]

    review_jobs = [
        job
        for job in discovered_jobs
        if job["status"] == "Review"
    ]

    offers = [
        application
        for application in applications
        if application["status"] == "Offer"
    ]

    return {
        "message": "Dashboard retrieved successfully",
        "application_summary": summary,
        "upcoming_interviews": upcoming_interviews,
        "top_discovered_jobs": top_discovered_jobs,
        "recent_applications": recent_applications,
        "review_jobs_count": len(review_jobs),
        "offers_count": len(offers),
    }