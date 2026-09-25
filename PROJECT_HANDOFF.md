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

The project should remain **human-controlled**.

The AI should assist, prepare, organize, and draft.

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