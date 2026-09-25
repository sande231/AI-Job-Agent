import json
import sqlite3

from datetime import datetime


DATABASE_NAME = "applications.db"


# =========================================================
# APPLICATIONS
# =========================================================

def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Add newer columns safely if they do not already exist
    new_columns = [
        ("job_url", "TEXT"),
        ("match_score", "INTEGER"),
        ("location", "TEXT"),
        ("date_applied", "TEXT"),
        ("interview_date", "TEXT"),
        ("deadline", "TEXT"),
        ("notes", "TEXT"),
        ("applied_via", "TEXT"),
        ("ats_platform", "TEXT"),
        ("submission_status", "TEXT"),
    ]

    for column_name, column_type in new_columns:
        try:
            cursor.execute(
                f"""
                ALTER TABLE applications
                ADD COLUMN {column_name} {column_type}
                """
            )
        except sqlite3.OperationalError:
            # Column already exists
            pass

    connection.commit()
    connection.close()


def save_application_to_db(
    title,
    company,
    description,
    status,
    job_url=None,
    match_score=None,
    location=None,
    date_applied=None,
    interview_date=None,
    deadline=None,
    notes=None,
    applied_via="manual",
    ats_platform=None,
    submission_status=None,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO applications (
            title,
            company,
            description,
            status,
            job_url,
            match_score,
            location,
            date_applied,
            interview_date,
            deadline,
            notes,
            applied_via,
            ats_platform,
            submission_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        company,
        description,
        status,
        job_url,
        match_score,
        location,
        date_applied,
        interview_date,
        deadline,
        notes,
        applied_via,
        ats_platform,
        submission_status,
    ))

    connection.commit()

    application_id = cursor.lastrowid

    connection.close()

    return application_id


def get_applications_from_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            description,
            status,
            job_url,
            match_score,
            location,
            date_applied,
            interview_date,
            deadline,
            notes,
            applied_via,
            ats_platform,
            submission_status
        FROM applications
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    applications = []

    for row in rows:
        applications.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "description": row[3],
            "status": row[4],
            "job_url": row[5],
            "match_score": row[6],
            "location": row[7],
            "date_applied": row[8],
            "interview_date": row[9],
            "deadline": row[10],
            "notes": row[11],
            "applied_via": row[12],
            "ats_platform": row[13],
            "submission_status": row[14],
        })

    return applications



def get_application_by_id(application_id):
    """
    Return one application as a dictionary, or None if no
    application has this id.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            description,
            status,
            job_url,
            match_score,
            location,
            date_applied,
            interview_date,
            deadline,
            notes,
            applied_via,
            ats_platform,
            submission_status
        FROM applications
        WHERE id = ?
        LIMIT 1
    """, (application_id,))

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "company": row[2],
        "description": row[3],
        "status": row[4],
        "job_url": row[5],
        "match_score": row[6],
        "location": row[7],
        "date_applied": row[8],
        "interview_date": row[9],
        "deadline": row[10],
        "notes": row[11],
        "applied_via": row[12],
        "ats_platform": row[13],
        "submission_status": row[14],
    }

def update_application_status(
    application_id,
    new_status,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE applications
        SET status = ?
        WHERE id = ?
    """, (
        new_status,
        application_id,
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows


def update_application_interview_date(
    application_id,
    interview_date,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE applications
        SET interview_date = ?
        WHERE id = ?
    """, (
        interview_date,
        application_id,
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows


def update_application_notes(
    application_id,
    notes,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE applications
        SET notes = ?
        WHERE id = ?
    """, (
        notes,
        application_id,
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows



def delete_application_from_db(
    application_id,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM applications
        WHERE id = ?
    """, (
        application_id,
    ))

    connection.commit()

    deleted_rows = cursor.rowcount

    connection.close()

    return deleted_rows


# =========================================================
# RESUME PROFILE
# =========================================================

def create_resume_profile_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            education TEXT NOT NULL,
            career_goal TEXT NOT NULL,
            skills TEXT NOT NULL,
            experience TEXT NOT NULL,
            projects TEXT NOT NULL,
            resume_text TEXT NOT NULL
        )
    """)

    # Add newer columns safely if they do not already exist
    new_columns = [
        ("email", "TEXT"),
        ("phone", "TEXT"),
        ("linkedin_url", "TEXT"),
    ]

    for column_name, column_type in new_columns:
        try:
            cursor.execute(
                f"""
                ALTER TABLE resume_profiles
                ADD COLUMN {column_name} {column_type}
                """
            )
        except sqlite3.OperationalError:
            # Column already exists
            pass

    connection.commit()
    connection.close()


def save_resume_profile_to_db(
    profile,
    resume_text,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Keep only the latest/current resume profile
    cursor.execute("""
        DELETE FROM resume_profiles
    """)

    cursor.execute("""
        INSERT INTO resume_profiles (
            name,
            education,
            career_goal,
            skills,
            experience,
            projects,
            resume_text,
            email,
            phone,
            linkedin_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile.name,
        profile.education,
        profile.career_goal,
        json.dumps(profile.skills),
        json.dumps(profile.experience),
        json.dumps(profile.projects),
        resume_text,
        profile.email,
        profile.phone,
        profile.linkedin_url,
    ))

    connection.commit()
    connection.close()


def get_resume_profile_from_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            name,
            education,
            career_goal,
            skills,
            experience,
            projects,
            resume_text,
            email,
            phone,
            linkedin_url
        FROM resume_profiles
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "name": row[0],
        "education": row[1],
        "career_goal": row[2],
        "skills": json.loads(row[3]),
        "experience": json.loads(row[4]),
        "projects": json.loads(row[5]),
        "resume_text": row[6],
        "email": row[7],
        "phone": row[8],
        "linkedin_url": row[9],
    }


# =========================================================
# APPLICATION SUMMARY / EVENTS
# =========================================================

def get_application_summary():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM applications
        GROUP BY status
    """)

    rows = cursor.fetchall()

    connection.close()

    summary = {
        "total": 0,
        "Saved": 0,
        "Applied": 0,
        "Assessment": 0,
        "Interview": 0,
        "Rejected": 0,
        "Offer": 0,
    }

    for status, count in rows:
        summary["total"] += count

        if status in summary:
            summary[status] = count

    return summary


def get_upcoming_events():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            status,
            interview_date,
            deadline
        FROM applications
        WHERE interview_date IS NOT NULL
           OR deadline IS NOT NULL
        ORDER BY
            CASE
                WHEN interview_date IS NOT NULL
                THEN interview_date
                ELSE deadline
            END
    """)

    rows = cursor.fetchall()

    connection.close()

    events = []

    for row in rows:
        events.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "status": row[3],
            "interview_date": row[4],
            "deadline": row[5],
        })

    return events





def get_upcoming_interviews():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            status,
            interview_date
        FROM applications
        WHERE interview_date IS NOT NULL
          AND status = 'Interview'
        ORDER BY interview_date
    """)

    rows = cursor.fetchall()

    connection.close()

    interviews = []
    now = datetime.now()

    for row in rows:
        interview_date_text = row[4]

        try:
            interview_datetime = datetime.strptime(
                interview_date_text,
                "%Y-%m-%d %H:%M:%S",
            )
        except (ValueError, TypeError):
            continue

        if interview_datetime <= now:
            continue

        interviews.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "status": row[3],
            "interview_date": row[4],
        })

    return interviews


# =========================================================
# PROCESSED EMAILS
# =========================================================

def create_processed_emails_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gmail_message_id TEXT UNIQUE NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def is_email_processed(
    gmail_message_id,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM processed_emails
        WHERE gmail_message_id = ?
        LIMIT 1
    """, (
        gmail_message_id,
    ))

    row = cursor.fetchone()

    connection.close()

    return row is not None


def mark_email_as_processed(
    gmail_message_id,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO processed_emails (
            gmail_message_id
        )
        VALUES (?)
    """, (
        gmail_message_id,
    ))

    connection.commit()
    connection.close()


# =========================================================
# INTERVIEW REMINDERS
# =========================================================

def create_interview_reminders_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            interview_date TEXT NOT NULL,
            reminder_type TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (
                application_id,
                interview_date,
                reminder_type
            )
        )
    """)

    connection.commit()
    connection.close()


def is_interview_reminder_sent(
    application_id,
    interview_date,
    reminder_type="24_hour",
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM interview_reminders
        WHERE application_id = ?
          AND interview_date = ?
          AND reminder_type = ?
        LIMIT 1
    """, (
        application_id,
        interview_date,
        reminder_type,
    ))

    row = cursor.fetchone()

    connection.close()

    return row is not None


def mark_interview_reminder_sent(
    application_id,
    interview_date,
    reminder_type="24_hour",
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO interview_reminders (
            application_id,
            interview_date,
            reminder_type
        )
        VALUES (?, ?, ?)
    """, (
        application_id,
        interview_date,
        reminder_type,
    ))

    connection.commit()
    connection.close()


# =========================================================
# DISCOVERED JOBS
# =========================================================

def create_discovered_jobs_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discovered_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT,
            job_url TEXT,
            source TEXT,
            match_score INTEGER,
            status TEXT NOT NULL DEFAULT 'Discovered'
        )
    """)

    connection.commit()
    connection.close()


def save_discovered_job_to_db(
    title,
    company,
    description,
    location=None,
    job_url=None,
    source=None,
    match_score=None,
    status="Discovered",
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO discovered_jobs (
            title,
            company,
            description,
            location,
            job_url,
            source,
            match_score,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        company,
        description,
        location,
        job_url,
        source,
        match_score,
        status,
    ))

    connection.commit()

    discovered_job_id = cursor.lastrowid

    connection.close()

    return discovered_job_id


def get_discovered_jobs_from_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            description,
            location,
            job_url,
            source,
            match_score,
            status
        FROM discovered_jobs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    jobs = []

    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "description": row[3],
            "location": row[4],
            "job_url": row[5],
            "source": row[6],
            "match_score": row[7],
            "status": row[8],
        })

    return jobs


# =========================================================
# NEW HELPER: GET ONE DISCOVERED JOB
# =========================================================

def get_discovered_job_by_id(job_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            description,
            location,
            job_url,
            source,
            match_score,
            status
        FROM discovered_jobs
        WHERE id = ?
        LIMIT 1
    """, (
        job_id,
    ))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "company": row[2],
        "description": row[3],
        "location": row[4],
        "job_url": row[5],
        "source": row[6],
        "match_score": row[7],
        "status": row[8],
    }


# =========================================================
# NEW HELPER: UPDATE DISCOVERED JOB STATUS
# =========================================================

def update_discovered_job_status(
    job_id,
    new_status,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE discovered_jobs
        SET status = ?
        WHERE id = ?
    """, (
        new_status,
        job_id,
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows


# =========================================================
# DUPLICATE JOB CHECK
# =========================================================

def discovered_job_exists(
    title,
    company,
    location=None,
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM discovered_jobs
        WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))
          AND LOWER(TRIM(company)) = LOWER(TRIM(?))
          AND LOWER(TRIM(COALESCE(location, '')))
              = LOWER(TRIM(COALESCE(?, '')))
        LIMIT 1
    """, (
        title,
        company,
        location,
    ))

    row = cursor.fetchone()

    connection.close()

    return row is not None