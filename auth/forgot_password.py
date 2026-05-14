import streamlit as st
import sqlite3
import secrets


# =========================================
# GENERATE RESET TOKEN
# =========================================

def generate_token():

    return secrets.token_hex(16)


# =========================================
# SAVE RESET TOKEN
# =========================================

def save_reset_token(email):

    conn = sqlite3.connect("auth/database.db")

    cursor = conn.cursor()

    token = generate_token()

    cursor.execute(

        "UPDATE users SET reset_token=? WHERE email=?",

        (token, email)

    )

    conn.commit()

    conn.close()

    return token


# =========================================
# FORGOT PASSWORD PAGE
# =========================================

def forgot_password_page():

    st.title("Forgot Password")

    email = st.text_input("Enter Your Email")

    if st.button("Generate Reset Token"):

        token = save_reset_token(email)

        st.success("Reset Token Generated")

        st.code(token)