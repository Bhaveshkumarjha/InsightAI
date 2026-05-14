import sqlite3
import bcrypt
import streamlit as st
import os

# =========================================
# DATABASE PATH
# =========================================

DB_PATH = "auth/database.db"

# CREATE AUTH FOLDER
os.makedirs("auth", exist_ok=True)

# =========================================
# DATABASE CONNECTION
# =========================================

def get_connection():

    return sqlite3.connect(DB_PATH)

# =========================================
# CREATE ALL TABLES
# =========================================

def create_users_table():

    conn = get_connection()

    cursor = conn.cursor()

    # =====================================
    # USERS TABLE
    # =====================================

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password BLOB NOT NULL,

            reset_token TEXT,

            profile_image TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    # =====================================
    # UPLOAD HISTORY
    # =====================================

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS uploads (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_email TEXT,

            filename TEXT,

            file_type TEXT,

            rows_count INTEGER,

            cols_count INTEGER,

            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    # =====================================
    # REPORT HISTORY
    # =====================================

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS reports (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_email TEXT,

            report_name TEXT,

            report_type TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    # =====================================
    # CHAT HISTORY
    # =====================================

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS chats (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_email TEXT,

            dataset_name TEXT,

            question TEXT,

            answer TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)
    # =====================================
    # CHECK dataset_name COLUMN
    # =====================================

    cursor.execute(
        "PRAGMA table_info(chats)"
    )

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "dataset_name" not in columns:

        cursor.execute(
            "ALTER TABLE chats ADD COLUMN dataset_name TEXT"
        )

        conn.commit()

    # =====================================
    # USER ACTIVITY
    # =====================================

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS activity_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_email TEXT,

            activity TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    conn.commit()

    conn.close()

# =========================================
# REGISTER USER
# =========================================

def register_user(

    username,
    email,
    password

):

    conn = get_connection()

    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(

        password.encode('utf-8'),

        bcrypt.gensalt()

    )

    try:

        cursor.execute("""

            INSERT INTO users (

                username,
                email,
                password

            )

            VALUES (?, ?, ?)

        """, (

            username,
            email,
            hashed_password

        ))

        conn.commit()

        save_activity(
            email,
            "New account created"
        )

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()

# =========================================
# LOGIN USER
# =========================================

def login_user(

    email,
    password

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )

    user = cursor.fetchone()

    conn.close()

    if user:

        stored_password = user[3]

        if isinstance(stored_password, str):

            stored_password = stored_password.encode(
                'utf-8'
            )

        if bcrypt.checkpw(

            password.encode('utf-8'),

            stored_password

        ):

            save_activity(
                email,
                "User logged in"
            )

            return True

    return False

# =========================================
# SAVE ACTIVITY
# =========================================

def save_activity(

    user_email,
    activity

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO activity_logs (

            user_email,
            activity

        )

        VALUES (?, ?)

    """, (

        user_email,
        activity

    ))

    conn.commit()

    conn.close()

# =========================================
# GET ACTIVITY HISTORY
# =========================================

def get_activity_history(user_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT activity,
               created_at

        FROM activity_logs

        WHERE user_email=?

        ORDER BY id DESC

    """, (user_email,))

    data = cursor.fetchall()

    conn.close()

    return data

# =========================================
# SAVE UPLOAD HISTORY
# =========================================

def save_upload_history(

    user_email,
    filename,
    file_type="CSV",
    rows_count=0,
    cols_count=0

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO uploads (

            user_email,
            filename,
            file_type,
            rows_count,
            cols_count

        )

        VALUES (?, ?, ?, ?, ?)

    """, (

        user_email,
        filename,
        file_type,
        rows_count,
        cols_count

    ))

    conn.commit()

    conn.close()

    save_activity(
        user_email,
        f"Uploaded dataset: {filename}"
    )

# =========================================
# GET UPLOAD HISTORY
# =========================================

def get_upload_history(user_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT filename,
               file_type,
               rows_count,
               cols_count,
               upload_time

        FROM uploads

        WHERE user_email=?

        ORDER BY id DESC

    """, (user_email,))

    data = cursor.fetchall()

    conn.close()

    return data

# =========================================
# SAVE REPORT HISTORY
# =========================================

def save_report_history(

    user_email,
    report_name,
    report_type="PPT"

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO reports (

            user_email,
            report_name,
            report_type

        )

        VALUES (?, ?, ?)

    """, (

        user_email,
        report_name,
        report_type

    ))

    conn.commit()

    conn.close()

    save_activity(
        user_email,
        f"Generated report: {report_name}"
    )

# =========================================
# GET REPORT HISTORY
# =========================================

def get_report_history(user_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT report_name,
               report_type,
               created_at

        FROM reports

        WHERE user_email=?

        ORDER BY id DESC

    """, (user_email,))

    data = cursor.fetchall()

    conn.close()

    return data

# =========================================
# SAVE CHAT HISTORY
# =========================================

def save_chat_history(

    user_email,
    dataset_name,
    question,
    answer

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO chats (

            user_email,
            dataset_name,
            question,
            answer

        )

        VALUES (?, ?, ?, ?)

    """, (

        user_email,
        dataset_name,
        question,
        answer

    ))

    conn.commit()

    conn.close()

# =========================================
# GET FULL CHAT HISTORY
# =========================================

def get_chat_history(user_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT dataset_name,
               question,
               answer,
               created_at

        FROM chats

        WHERE user_email=?

        ORDER BY id DESC

    """, (user_email,))

    data = cursor.fetchall()

    conn.close()

    return data

# =========================================
# GET DATASET HISTORY
# =========================================

def get_dataset_history(user_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT DISTINCT dataset_name

        FROM chats

        WHERE user_email=?

        ORDER BY id DESC

    """, (user_email,))

    data = cursor.fetchall()

    conn.close()

    return [x[0] for x in data]

# =========================================
# GET CHAT BY DATASET
# =========================================

def get_chat_by_dataset(

    user_email,
    dataset_name

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT question,
               answer,
               created_at

        FROM chats

        WHERE user_email=?
        AND dataset_name=?

        ORDER BY id ASC

    """, (

        user_email,
        dataset_name

    ))

    data = cursor.fetchall()

    conn.close()

    return data

# =========================================
# GET USER PROFILE
# =========================================

def get_user_profile(user_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT username,
               email,
               created_at

        FROM users

        WHERE email=?

    """, (user_email,))

    user = cursor.fetchone()

    conn.close()

    return user

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    create_users_table()

    print("✅ Advanced InsightAI Database Ready")