# AI Job Agent

AI Job Agent is a full-stack project I am building to make the internship and job-search process more organized and intelligent.

The idea started from a simple problem: searching for internships, comparing job descriptions with a resume, keeping track of applications, and remembering interviews can become difficult when everything is handled manually.

This project brings those tasks together in one system. The backend can analyze a resume, discover live internship opportunities, calculate job-match scores using AI, track applications, process job-related emails, and manage interview reminders.

The project is currently under active development.

---

## What the Project Does

AI Job Agent currently supports several parts of the job-search workflow:

- Resume parsing and candidate profile creation
- AI-powered resume and job-description comparison
- Live internship discovery
- Job-match scoring
- Duplicate job detection
- Application tracking
- Application status management
- Gmail-based job email processing
- Interview date tracking
- Interview reminders
- Application notes
- Dashboard data for a future frontend

The goal is not to automatically apply to every job. Instead, the system helps identify relevant opportunities and keeps the user in control of the application process.

---

## How It Works

The basic workflow is:

```text
Resume
   ↓
Candidate Profile
   ↓
Live Job Discovery
   ↓
AI Job Analysis
   ↓
Match Score
   ↓
Discovered / Review / Skip
   ↓
Application Tracker
   ↓
Applied
   ↓
Assessment
   ↓
Interview
   ↓
Offer / Rejected
```

---

## Resume Processing

A user can upload a PDF resume to the backend.

The system extracts information such as:

- Name
- Education
- Skills
- Experience
- Projects
- Career information

The extracted information is converted into a structured candidate profile and stored so that it can later be used during job analysis.

---

## AI-Powered Job Matching

One of the main features of the project is comparing a candidate's resume with a job description.

The backend uses the OpenAI API to analyze the two and return information such as:

- Match score
- Matching skills
- Missing skills
- Strengths
- Areas for improvement
- Recommendation

For example:

```text
Job: AI Engineering Intern
Match Score: 78%

Matching Skills:
- Python
- APIs
- Machine Learning
- AI

Missing Skills:
- Some job-specific technologies
```

The match score is meant to help prioritize opportunities. It is not intended to guarantee whether someone will receive an interview or job offer.

---

## Live Job Discovery

The project integrates with the Adzuna Jobs API to retrieve real internship and job listings.

The current search focuses mainly on technical internships such as:

- Software Engineering Intern
- AI Intern
- Machine Learning Intern
- Generative AI Intern

Additional categories can easily be added later.

After jobs are retrieved, the system compares them against the stored resume profile.

---

## Job Classification

Jobs are organized according to their AI match score.

| Match Score | Status |
|---|---|
| 70–100 | Discovered |
| 55–69 | Review |
| Below 55 | Skip |

High-scoring jobs are saved as opportunities, while medium-scoring jobs are kept for manual review.

Low-scoring jobs are skipped so that the user can focus on more relevant positions.

---

## Duplicate Job Detection

Job APIs can sometimes return the same opportunity multiple times or provide different tracking URLs for the same posting.

To reduce duplicate records, the backend checks information such as:

- Job title
- Company
- Location

before saving a discovered opportunity.

This also prevents unnecessary AI analysis of jobs that have already been processed.

---

## Application Tracking

Jobs can be moved from the discovered-jobs list into the application tracker.

An application can move through the following statuses:

```text
Saved
Applied
Assessment
Interview
Offer
Rejected
```

Each application can contain:

- Job title
- Company
- Description
- Location
- Job URL
- Match score
- Application status
- Date applied
- Interview date
- Deadline
- Notes

This creates one place to keep track of the entire application process.

---

## Moving a Job to Applications

A discovered opportunity can be moved into the application tracker through:

```text
POST /discovered-jobs/{job_id}/apply
```

When this happens, the backend:

1. Retrieves the discovered job
2. Creates an application record
3. Changes the application status to `Applied`
4. Stores the application date
5. Preserves the original job information
6. Updates the discovered-job status

The system also prevents the same discovered job from being moved multiple times.

---

## Application Status Updates

Application status can be updated through:

```text
PUT /applications/{application_id}/status
```

Supported statuses currently include:

```text
Saved
Applied
Assessment
Interview
Offer
Rejected
```

This makes it possible to track an application as it moves through the hiring process.

---

## Interview Management

Interview information can also be stored for an application.

```text
PUT /applications/{application_id}/interview
```

When an interview is scheduled, the system can:

- Store the interview date and time
- Update the application status
- Include the interview in upcoming-interview checks
- Use the date for reminder processing

---

## Interview Reminders

The project includes an interview reminder system.

The backend checks scheduled interviews and determines whether an interview is approaching.

It can:

- Find upcoming interviews
- Check whether an interview is within the reminder window
- Send an email reminder
- Record that the reminder was sent
- Prevent duplicate reminders

APScheduler is used to support scheduled background checks.

---

## Gmail Integration

The backend also includes Gmail integration for processing job-related messages.

The email workflow can:

- Retrieve recent emails
- Detect whether an email is related to a job application
- Ignore unrelated messages
- Classify recruiter or application emails
- Match an email with an existing application
- Extract useful dates
- Prevent the same email from being processed repeatedly

This allows application information to be updated from real email activity instead of relying completely on manual updates.

---

## Application Notes

Notes can be attached to an application using:

```text
PUT /applications/{application_id}/notes
```

For example, notes can be used for:

- Interview preparation
- Recruiter information
- Follow-up reminders
- Questions to ask during an interview
- Technical topics to review

---

## Dashboard API

The backend provides a dashboard endpoint:

```text
GET /dashboard
```

It combines information from different parts of the system and currently returns:

- Total applications
- Application status summary
- Upcoming interviews
- Top job matches
- Recent applications
- Jobs waiting for review
- Number of offers

Jobs that have already been moved into the application tracker are excluded from the available top-job recommendations.

The dashboard endpoint will be used by the frontend in the next phase of development.

---

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### Artificial Intelligence

- OpenAI API

### Database

- SQLite

### Job Discovery

- Adzuna Jobs API

### Email

- Gmail API
- Email/SMTP services

### Automation

- APScheduler

### Development Tools

- Git
- GitHub
- Docker
- VS Code

---

## System Architecture

```text
                    React Frontend
                    (Next Phase)
                          │
                          ▼
                   FastAPI Backend
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
     SQLite            OpenAI            Adzuna
     Database            API             Jobs API
        │
        ▼
      Gmail
       API
```

FastAPI acts as the main backend layer and connects the different services together.

SQLite stores application, job, resume, and reminder information.

OpenAI is used for intelligent resume/job analysis, while Adzuna provides live job listings and Gmail provides email-related automation.

---

## Project Structure

```text
AI-Job-Agent/
│
├── README.md
├── .gitignore
│
└── backend/
    │
    ├── main.py
    ├── requirements.txt
    │
    ├── database/
    │   └── database.py
    │
    ├── models/
    │   ├── application.py
    │   ├── discovered_job.py
    │   ├── interview_update.py
    │   ├── notes_update.py
    │   ├── resume_profile.py
    │   └── status_update.py
    │
    ├── services/
    │   ├── ai_service.py
    │   ├── application_matcher.py
    │   ├── date_extractor.py
    │   ├── email_classifier.py
    │   ├── email_service.py
    │   ├── experience_extractor.py
    │   ├── job_discovery_service.py
    │   ├── profile_extractor.py
    │   ├── profile_store.py
    │   ├── project_extractor.py
    │   ├── reminder_service.py
    │   ├── scheduler_service.py
    │   └── skill_extractor.py
    │
    └── test_*.py
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sande231/AI-Job-Agent.git
cd AI-Job-Agent
```

### 2. Go to the backend

```bash
cd backend
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the `backend` directory.

For example:

```env
OPENAI_API_KEY=your_openai_api_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
```

Additional Gmail/email credentials may be required when using the email features.

**Never commit API keys, passwords, OAuth tokens, or other credentials to GitHub.**

---

## Running the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Main API Endpoints

Some of the main endpoints currently include:

```text
GET    /applications
POST   /applications

PUT    /applications/{application_id}/status
PUT    /applications/{application_id}/interview
PUT    /applications/{application_id}/notes

GET    /discovered-jobs
POST   /discovered-jobs/{job_id}/apply

GET    /jobs/live-preview
POST   /jobs/live-discover-and-save

POST   /upload-resume

GET    /dashboard
```

FastAPI's Swagger interface can be used to view and test the available endpoints.

---

## Responsible Use of AI

The AI component is designed to assist with job analysis rather than make hiring decisions.

A few principles I am following while developing the project are:

- Do not invent skills that are not present in the resume
- Do not invent education or work experience
- Base job analysis on available resume information
- Clearly identify missing skills
- Keep the user involved in application decisions
- Treat match scores as guidance rather than guarantees

---

## Security

Sensitive and local development files are excluded through `.gitignore`.

Examples include:

```text
.env
*.db
backend/venv/
*.backup
```

Files containing the following information should never be committed:

- OpenAI API keys
- Adzuna credentials
- Gmail credentials
- OAuth tokens
- Passwords
- Local SQLite databases
- Virtual environments

---

## Development Progress

### Completed

- [x] FastAPI backend
- [x] SQLite database
- [x] PDF resume parsing
- [x] Candidate profile extraction
- [x] Skill extraction
- [x] Experience extraction
- [x] Project extraction
- [x] Resume profile persistence
- [x] OpenAI resume/job analysis
- [x] AI match scoring
- [x] Live internship discovery with Adzuna
- [x] Multiple internship search categories
- [x] Duplicate job prevention
- [x] Discovered-job storage
- [x] Application tracking
- [x] Discovered-job to application workflow
- [x] Application status management
- [x] Automatic application dates
- [x] Application notes
- [x] Interview scheduling
- [x] Job-related email classification
- [x] Application/email matching
- [x] Interview date extraction
- [x] Interview reminders
- [x] Background scheduling
- [x] Dashboard API

### Currently Working On

- [ ] React frontend dashboard
- [ ] Improving job-search performance
- [ ] Improving job filtering
- [ ] Organizing automated tests

### Future Improvements

- [ ] User authentication
- [ ] PostgreSQL database
- [ ] Cloud deployment
- [ ] Analytics and visualizations
- [ ] Calendar integration
- [ ] Resume tailoring
- [ ] Cover-letter assistance
- [ ] Additional job providers

---

## Why I Built This Project

Searching for internships involves more than finding job postings. A student may need to compare many job descriptions, determine which positions fit their skills, keep track of application statuses, monitor emails, prepare for interviews, and remember important dates.

I wanted to explore how AI and backend automation could make that process easier while still keeping the final decisions with the user.

This project has also given me practical experience working with APIs, databases, AI integration, backend development, automation, email processing, and application architecture.

---

## Author

**Sandeep Shah**

Computer Science Student

GitHub: [@sande231](https://github.com/sande231)

---

> This project is under active development. The backend is functional, and the next major phase is building the React frontend.