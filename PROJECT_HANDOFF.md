# AI Job Agent — Project Handoff

## 1. Project Overview

This project is an AI-powered internship and job application assistant.

The main goal is to help a student:

- Upload and analyze a resume
- Discover relevant internships/jobs
- Compare resume skills with job descriptions
- Rank job matches with AI
- Save discovered jobs
- Move selected jobs into an application tracker
- Track application status
- Monitor recruiting emails
- Detect interview / assessment / offer / rejection updates
- Extract interview dates
- Send interview reminders
- Generate tailored application materials
- Generate AI interview preparation
- Assist with application form answers
- Keep sensitive/legal application questions for user review
- Eventually assist with job application forms while keeping the user in control

The project should remain **human-controlled**.

The AI should assist, prepare, organize, draft, and prefill safe fields.

It should NOT blindly submit applications or guess sensitive/legal answers.

---

# 2. Development Style

The developer is a Computer Science student and prefers:

- Simple explanations
- One small step at a time
- Beginner-friendly language
- Exact terminal commands
- Test each feature before moving on
- Finish core functionality before spending time on UI polish
- Avoid rebuilding features that already exist
- Inspect current code before adding new functionality

Important rule:

> The GitHub repository is the source of truth.

Before changing code, inspect the current repository because older conversation notes may not perfectly match the latest files.

---

# 3. Main Architecture

```text
Resume
  ↓
Resume Parser
  ↓
Candidate Profile
  ↓
Live Job Discovery
  ↓
AI Job Matching
  ↓
Discovered Jobs
  ↓
User Selects Job
  ↓
Applications Tracker
  ↓
AI Application Materials
  ↓
Application Form Assistance
  ↓
Recruiting Email Monitoring
  ↓
Status Updates
  ↓
Interview Date Extraction
  ↓
Interview Reminders
  ↓
AI Interview Preparation
  ↓
Offer / Rejection
```

Frontend:

```text
React / Vite
```

Backend:

```text
FastAPI
```

Database:

```text
SQLite
```

AI:

```text
OpenAI API
```

Job discovery:

```text
Adzuna API
```

Email:

```text
Gmail OAuth / Gmail API
```

Scheduling:

```text
APScheduler
```

---

# 4. Project Structure

Approximate repository structure:

```text
AI-Job-Agent/
│
├── README.md
├── PROJECT_HANDOFF.md
├── .gitignore
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── applications.db
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── application.py
│   │   ├── discovered_job.py
│   │   ├── interview_update.py
│   │   ├── job.py
│   │   ├── match_request.py
│   │   ├── notes_update.py
│   │   ├── profile.py
│   │   ├── resume_profile.py
│   │   └── status_update.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── application_matcher.py
│   │   ├── ats_detector.py
│   │   ├── contact_extractor.py
│   │   ├── date_extractor.py
│   │   ├── email_classifier.py
│   │   ├── email_service.py
│   │   ├── experience_extractor.py
│   │   ├── job_discovery_service.py
│   │   ├── job_matcher.py
│   │   ├── profile_extractor.py
│   │   ├── profile_store.py
│   │   ├── project_extractor.py
│   │   ├── reminder_service.py
│   │   ├── resume_parser.py
│   │   ├── scheduler_service.py
│   │   ├── skill_extractor.py
│   │   │
│   │   └── apply_adapters/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── greenhouse.py
│   │       └── lever.py
│   │
│   └── tests...
│
└── frontend/
    └── src/
        ├── App.jsx
        ├── App.css
        │
        ├── components/
        │
        └── pages/
            ├── ApplicationsPage.jsx
            ├── DashboardPage.jsx
            ├── DiscoverJobsPage.jsx
            ├── InterviewsPage.jsx
            ├── JobDetailsPage.jsx
            └── ProfilePage.jsx
```

Always inspect the actual repository because this structure may have changed.

---

# 5. Environment

Typical local project location:

```text
~/AI-Job-Agent
```

Backend:

```text
~/AI-Job-Agent/backend
```

Frontend:

```text
~/AI-Job-Agent/frontend
```

Backend virtual environment:

```text
~/AI-Job-Agent/backend/venv
```

Typical backend startup:

```bash
cd ~/AI-Job-Agent/backend
source venv/bin/activate
uvicorn main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Frontend:

```bash
cd ~/AI-Job-Agent/frontend
npm run dev
```

Frontend production test:

```bash
npm run build
```

---

# 6. Resume Processing

The user can upload a resume.

The backend extracts text from the PDF and builds a candidate profile.

Resume-related services include:

```text
resume_parser.py
skill_extractor.py
profile_extractor.py
experience_extractor.py
project_extractor.py
profile_store.py
contact_extractor.py
```

Candidate information includes things like:

- name
- education
- career goal
- skills
- experience
- projects
- email
- phone
- LinkedIn URL

The resume text/profile can be saved and later reused by AI features.

Important AI rule:

> Never invent candidate experience, education, skills, projects, achievements, or certifications.

---

# 7. AI Job Matching

The project compares the saved resume with a job description using AI.

Main function:

```text
analyze_resume_and_job(...)
```

The scoring system has used categories similar to:

```text
Technical skills: 0–40
Experience/projects: 0–25
Education: 0–15
Role relevance: 0–10
Preferred qualifications: 0–10
```

The backend recalculates the final match score from the score breakdown instead of blindly trusting an AI-provided total.

Typical AI output includes:

- match_score
- score_breakdown
- matching_skills
- missing_skills
- strengths
- gaps
- recommendation

---

# 8. Live Job Discovery

Live internships/jobs are retrieved using Adzuna.

The project searches categories such as:

```text
software engineering intern
AI intern
machine learning intern
generative AI intern
```

The project tries to avoid duplicate jobs.

Discovered jobs can be classified approximately as:

```text
70+ → Discovered
55–69 → Review
Below 55 → skipped
```

These thresholds may change, so inspect the current implementation.

---

# 9. Discovered Jobs

Discovered jobs are stored in SQLite.

Fields may include:

```text
id
title
company
description
location
job_url
source
match_score
status
score_breakdown
matching_skills
missing_skills
strengths
gaps
recommendation
```

Features include:

- viewing discovered jobs
- AI analysis
- reanalyzing a job
- moving a discovered job to applications
- duplicate prevention

The frontend includes:

```text
DiscoverJobsPage.jsx
JobDetailsPage.jsx
```

---

# 10. Applications Tracker

Selected jobs can be moved into the applications table.

Application data can include:

```text
id
title
company
description
status
job_url
match_score
location
date_applied
interview_date
deadline
notes
```

Known application statuses:

```text
Saved
Applied
Assessment
Interview
Offer
Rejected
```

Features include:

- view applications
- change status
- add notes
- schedule interview
- delete application
- generate AI application materials

---

# 11. AI Application Materials

The project contains AI logic for application materials.

Main function:

```text
generate_application_materials(...)
```

Typical output:

- tailored cover letter
- resume suggestions
- skills to emphasize

The AI must use only information supported by the resume and job description.

It must not invent experience or skills.

**Important current-repo note:**

The frontend may call:

```text
POST /applications/{id}/generate-materials
```

but the current GitHub backend may not yet expose that route.

Inspect `main.py` before assuming it exists.

---

# 12. Recruiting Email Monitoring

The project integrates Gmail.

The application can inspect recent emails and determine whether they are recruiting/job-related.

The email classifier can detect statuses such as:

```text
Applied
Assessment
Interview
Offer
Rejected
```

Examples of recognized phrases:

```text
thank you for applying
application received
coding challenge
online assessment
interview invitation
offer letter
unfortunately
not moving forward
```

Job emails are matched to tracked applications.

Processed email IDs are stored to prevent duplicate processing.

A dashboard button exists for:

```text
Check Recruiting Emails
```

Backend route:

```text
POST /emails/process
```

This can update the application status automatically when a clear recruiting email is found.

---

# 13. Interview Date Extraction

When an interview email is detected, the project attempts to extract a date/time.

The normalized interview date is stored in the application.

The project has a service similar to:

```text
date_extractor.py
```

---

# 14. Interview Reminders

The project uses APScheduler.

Scheduled tasks include:

```text
Hourly interview reminder checks
Daily application report
```

The scheduler only runs while the backend process is running locally.

Deployment will eventually be needed for 24/7 scheduling.

---

# 15. AI Interview Preparation

AI interview preparation logic exists.

Main function:

```text
generate_interview_preparation(...)
```

Typical output:

```text
likely_interview_questions
technical_topics_to_review
project_talking_points
questions_to_ask_interviewer
preparation_advice
```

The frontend may call:

```text
POST /applications/{application_id}/interview-prep
```

**Important current-repo note:**

The current GitHub backend may not yet expose this route even though the frontend expects it.

Inspect `main.py` first.

---

# 16. Application Form Assistance

This is the current major feature area.

A function exists in:

```text
backend/services/ai_service.py
```

Named:

```text
generate_application_form_answers(...)
```

Its purpose is to create draft answers for common application questions.

Expected output includes things such as:

```json
{
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
}
```

Sensitive questions must NOT be guessed.

Examples:

```text
work authorization
visa sponsorship
citizenship
race/ethnicity
gender
disability
veteran status
criminal-history questions
legal attestations
```

Those fields should require the user to answer them personally.

The project should remain a human-reviewed application assistant.

**Important current-repo note:**

The AI function exists, but the backend route that calls it may still be missing.

A likely route is:

```text
POST /applications/{application_id}/form-assistance
```

or:

```text
POST /applications/{application_id}/form-answers
```

Use one clear route name and keep it consistent in frontend and backend.

---

# 17. Application Submission / ATS Groundwork

The repository contains early groundwork for application-system adapters.

Files include:

```text
backend/services/ats_detector.py
backend/services/contact_extractor.py

backend/services/apply_adapters/
    base.py
    greenhouse.py
    lever.py
```

The ATS detector recognizes multiple platforms.

The current groundwork may recognize:

- Greenhouse
- Lever
- Workday
- iCIMS
- SmartRecruiters
- Ashby
- Workable
- LinkedIn
- Indeed

Only Greenhouse and Lever currently have dedicated adapters.

These adapters prepare/prefill known application fields.

They should NOT perform blind final submission.

There is also a backend route similar to:

```text
POST /discovered-jobs/{job_id}/prepare-application
```

This can detect the ATS and return a preview of fields that could be filled.

Before extending this functionality:

1. Read the current implementation.
2. Determine what is already supported.
3. Do not assume these files are complete.
4. Do not build blind autonomous application submission.
5. Keep the user in control before final submission.
6. Never auto-answer sensitive/legal fields.

---

# 18. Dashboard

The React dashboard shows information such as:

- total applications
- applied applications
- interviews
- offers
- top job matches
- recent applications

The dashboard also has:

```text
Check Recruiting Emails
Refresh
```

Backend endpoint:

```text
GET /dashboard
```

---

# 19. Important Security Rules

The following files are local only and MUST NOT be committed or shared:

```text
backend/.env
backend/credentials.json
backend/token.json
backend/applications.db
```

`.gitignore` protects them.

Never ask the user to paste:

- OpenAI API keys
- Adzuna credentials
- Gmail OAuth token
- Gmail credentials
- passwords
- private tokens

The repository was checked before the latest commit.

Secrets were ignored properly.

---

# 20. Git / GitHub

The repository is synchronized with GitHub.

Latest known status:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

The GitHub repository should be treated as the source of truth.

Before implementing changes:

```bash
git status
```

After a meaningful feature:

```bash
git add ...
git commit -m "..."
git push origin main
```

Do not commit:

```text
.env
credentials.json
token.json
applications.db
backend 2/
*.backup
*.zip
__pycache__/
*.pyc
```

---

# 21. Known Local Backup / Temporary Files

The local machine contains some old or temporary items such as:

```text
backend 2/
ai-job-agent-phase2-autoapply-groundwork.zip
*.backup
```

These are intentionally ignored.

Do not treat them as the main source code.

Use:

```text
backend/
frontend/
```

as the active project.

---

# 22. Important Development Lessons

Before adding a feature, `grep` the repository to check whether similar functionality already exists.

Avoid duplicate endpoints.

Keep:

```text
FastAPI routes → main.py
Database helpers → database/database.py
AI functions → services/ai_service.py
```

Avoid naming an endpoint function the same as an imported helper because this can cause recursion/name conflicts.

After backend edits:

```bash
python -m py_compile ...
```

No output usually means syntax passed.

But also test the endpoint because syntax success does not guarantee runtime success.

Typical endpoint testing:

```bash
curl -s -X POST http://127.0.0.1:8000/... | python -m json.tool
```

After frontend changes:

```bash
npm run build
```

Expected success:

```text
✓ built
```

---

# 23. Common Local Development Issues Already Encountered

## Port already in use

If Uvicorn reports:

```text
Address already in use
```

check:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

and if necessary:

```bash
pkill -f uvicorn
```

Note: Uvicorn `--reload` can create two processes. That is normal.

## Terminal vs JavaScript

Do not paste JavaScript code directly into zsh.

React code belongs inside `.jsx` files.

Terminal commands belong in Terminal.

## Python compile check

If:

```bash
python -m py_compile file.py
```

shows no output, syntax passed.

---

# 24. Current Repository Gaps Found During Review

The current GitHub repository appears to have some frontend/backend mismatches.

The frontend expects routes such as:

```text
POST /applications/{id}/generate-materials
POST /applications/{id}/interview-prep
POST /discovered-jobs/{id}/reanalyze
```

but the current `main.py` may not expose them.

Also:

```text
get_application_by_id(...)
```

may be missing from:

```text
backend/database/database.py
```

This is important because multiple application-specific AI routes need to fetch a single application by ID.

Before coding, verify these gaps against the actual latest GitHub files.

Do not rely only on this handoff.

---

# 25. Current Priority

Do NOT spend significant time polishing styling yet.

The priority is:

```text
Complete core functionality
↓
Reconnect missing backend routes
↓
Test workflows
↓
Improve safety/reliability
↓
Clean sample/test data
↓
Deployment
↓
UI polish
```

---

# 26. Current Recommended Repair Order

Based on the current GitHub review, the safest next order is:

## Step 1

Add and test:

```text
get_application_by_id(application_id)
```

in:

```text
backend/database/database.py
```

## Step 2

Reconnect AI application materials route:

```text
POST /applications/{id}/generate-materials
```

## Step 3

Reconnect interview preparation route:

```text
POST /applications/{id}/interview-prep
```

## Step 4

Reconnect discovered-job reanalysis route:

```text
POST /discovered-jobs/{id}/reanalyze
```

## Step 5

Add Application Form Assistance backend route:

```text
POST /applications/{id}/form-assistance
```

This should call:

```text
generate_application_form_answers(...)
```

## Step 6

Test all routes individually with curl or Swagger.

## Step 7

Connect Application Form Assistance to the frontend.

## Step 8

Then improve ATS adapter integration and controlled form prefill.

---

# 27. Application Form Assistance Safety Rules

For normal application questions, AI may draft:

- Why this role?
- Why this company?
- Relevant experience
- Skills summary
- Project highlights
- Short professional summary

For sensitive or legal fields, AI must not guess.

Return:

```text
USER INPUT REQUIRED
```

for fields such as:

- work authorization
- sponsorship
- citizenship
- race/ethnicity
- gender
- disability
- veteran status
- criminal-history questions
- legal attestations
- salary expectations unless explicitly provided by the user
- relocation willingness unless explicitly provided by the user

The user should review everything before any application is submitted.

---

# 28. Instructions for the Next AI Assistant

You are continuing an existing project.

Do NOT rebuild it from scratch.

First:

1. Inspect the repository.
2. Read this `PROJECT_HANDOFF.md`.
3. Compare this handoff with current code.
4. Treat current code as the source of truth.
5. Identify exactly what is already implemented.
6. Continue from the next missing core feature.

Work with the developer one small step at a time.

Give exact commands when appropriate.

After each step, explain how to verify that it worked.

Do not make large unrequested refactors.

Do not spend time on UI polish until the core system is complete.

Never invent resume facts.

Never guess sensitive job-application answers.

Always keep final application submission under user control.

---

# 29. Immediate Next Task

Before changing anything, inspect these files:

```text
backend/database/database.py
backend/main.py
backend/services/ai_service.py
backend/services/ats_detector.py
backend/services/apply_adapters/
frontend/src/pages/ApplicationsPage.jsx
frontend/src/pages/InterviewsPage.jsx
frontend/src/pages/JobDetailsPage.jsx
```

Confirm whether the following exist:

```text
get_application_by_id
generate_application_materials
generate_interview_preparation
generate_application_form_answers
/applications/{id}/generate-materials
/applications/{id}/interview-prep
/discovered-jobs/{id}/reanalyze
/applications/{id}/form-assistance
```

Then report:

1. What exists
2. What is missing
3. The single safest next implementation step

Do not modify code until that review is complete.