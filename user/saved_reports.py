import sqlite3
import streamlit as st


# =========================================
# SAVE REPORT
# =========================================

def save_report_history(
    user_email,
    report_name
):

    conn = sqlite3.connect(
        "auth/database.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO reports (
        user_email,
        report_name
    )

    VALUES (?, ?)

    """, (
        user_email,
        report_name
    ))

    conn.commit()

    conn.close()


# =========================================
# SHOW REPORTS
# =========================================

def show_saved_reports():

    st.subheader("📄 Saved Reports")

    conn = sqlite3.connect(
        "auth/database.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

    SELECT report_name, created_at

    FROM reports

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
                f"📊 {row[0]} | ⏰ {row[1]}"
            )

    else:

        st.info("No reports generated yet.")