import sqlite3


DATABASE_NAME = "applications.db"


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

    connection.commit()
    connection.close()


def save_application_to_db(title, company, description, status):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO applications (
            title,
            company,
            description,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        title,
        company,
        description,
        status
    ))

    connection.commit()
    connection.close()


def get_applications_from_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, company, description, status
        FROM applications
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
            "status": row[4]
        })

    return applications


def update_application_status(application_id, new_status):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE applications
        SET status = ?
        WHERE id = ?
    """, (
        new_status,
        application_id
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows


def delete_application_from_db(application_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM applications
        WHERE id = ?
    """, (application_id,))

    connection.commit()

    deleted_rows = cursor.rowcount

    connection.close()

    return deleted_rows