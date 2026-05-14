import streamlit as st
import sqlite3
import bcrypt


# =========================================
# RESET PASSWORD
# =========================================

def reset_password(token, new_password):

    conn = sqlite3.connect("auth/database.db")

    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    )

    cursor.execute(

        """

        UPDATE users

        SET password=?,
            reset_token=NULL

        WHERE reset_token=?

        """,

        (hashed_password, token)

    )

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated > 0


# =========================================
# PAGE
# =========================================

def reset_password_page():

    st.title("Reset Password")

    token = st.text_input("Reset Token")

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    if st.button("Reset Password"):

        success = reset_password(
            token,
            new_password
        )

        if success:

            st.success("Password Updated")

        else:

            st.error("Invalid Token")