import sqlite3
import streamlit as st


# =========================================
# SAVE UPLOAD
# =========================================

def save_upload_history(
    user_email,
    filename
):

    conn = sqlite3.connect(
        "auth/database.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO uploads (
        user_email,
        filename
    )

    VALUES (?, ?)

    """, (user_email, filename))

    conn.commit()

    conn.close()


# =========================================
# SHOW HISTORY
# =========================================

def show_upload_history():

    st.subheader("📂 Upload History")

    conn = sqlite3.connect(
        "auth/database.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

    SELECT filename, upload_time

    FROM uploads

    WHERE user_email=?

    ORDER BY id DESC

    """, (
        st.session_state.user_email,
    ))

    data = cursor.fetchall()

    conn.close()

    if data:

        for row in data:

            st.write(
                f"📄 {row[0]} | ⏰ {row[1]}"
            )

    else:

        st.info("No uploads yet.")