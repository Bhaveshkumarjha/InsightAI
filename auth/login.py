import streamlit as st
import sqlite3
import bcrypt
import time

from auth.google_login import google_login

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="InsightAI · Secure Login",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================
# PROFESSIONAL MINIMAL CSS
# =========================================

def load_css():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ===================================== */
    /* GLOBAL */
    /* ===================================== */

    html, body, [class*="css"], .stApp {

        font-family: 'Inter', sans-serif;

        background: #f5f7fb;

        color: #111827;
    }

    /* ===================================== */
    /* MAIN CONTAINER */
    /* ===================================== */

    .block-container {

        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* ===================================== */
    /* LOGIN CARD */
    /* ===================================== */

    .main-card {

        background: white;

        padding: 40px;

        border-radius: 22px;

        border: 1px solid #e5e7eb;

        box-shadow:
            0 4px 20px rgba(0,0,0,0.05);

        margin-top: 10px;
    }

    /* ===================================== */
    /* TITLE */
    /* ===================================== */

    .main-title {

        text-align: center;

        font-size: 2.2rem;

        font-weight: 700;

        color: #111827;

        margin-bottom: 10px;
    }

    /* ===================================== */
    /* SUBTITLE */
    /* ===================================== */

    .login-description {

        text-align: center;

        color: #6b7280;

        font-size: 15px;

        margin-bottom: 28px;
    }

    /* ===================================== */
    /* FEATURE BOX */
    /* ===================================== */

    .feature-card {

        background: #f9fafb;

        border: 1px solid #e5e7eb;

        border-radius: 14px;

        padding: 12px 6px;

        text-align: center;

        font-size: 12px;

        font-weight: 600;

        color: #374151;

        min-height: 75px;
    }

    /* ===================================== */
    /* INPUT */
    /* ===================================== */

    .stTextInput input {

        border-radius: 12px !important;

        border: 1px solid #d1d5db !important;

        padding: 12px !important;

        background: white !important;

        color: #111827 !important;

        font-size: 15px !important;
    }

    .stTextInput input:focus {

        border: 1px solid #111827 !important;

        box-shadow: none !important;
    }

    /* ===================================== */
    /* PRIMARY BUTTON */
    /* ===================================== */

    div.stButton > button {

        width: 100%;

        border-radius: 12px;

        background: #111827;

        color: white;

        border: none;

        padding: 12px;

        font-size: 15px;

        font-weight: 600;

        transition: 0.2s ease;
    }

    div.stButton > button:hover {

        background: #1f2937;

        color: white;
    }

    div.stButton > button:focus:not(:active) {

        background: #111827 !important;

        color: white !important;

        border: none !important;

        box-shadow: none !important;
    }

    /* ===================================== */
    /* SECONDARY BUTTONS */
    /* ===================================== */

    .secondary-btn div.stButton > button {

        background: white !important;

        color: #111827 !important;

        border: 1px solid #d1d5db !important;

        box-shadow: none !important;
    }

    .secondary-btn div.stButton > button:hover {

        background: #f9fafb !important;

        color: #111827 !important;
    }

    /* ===================================== */
    /* CHECKBOX */
    /* ===================================== */

    .stCheckbox label {

        color: #4b5563 !important;

        font-size: 14px !important;
    }

    /* ===================================== */
    /* GOOGLE TEXT */
    /* ===================================== */

    .google-text {

        text-align: center;

        color: #6b7280;

        font-size: 13px;

        margin-top: 18px;

        margin-bottom: 10px;

        font-weight: 500;
    }

    /* ===================================== */
    /* FOOTER */
    /* ===================================== */

    .brand-tagline {

        text-align: center;

        color: #9ca3af;

        margin-top: 28px;

        font-size: 13px;

        font-weight: 500;
    }

    /* ===================================== */
    /* HIDE STREAMLIT */
    /* ===================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    </style>
    """, unsafe_allow_html=True)

# LOAD CSS EVERY RERUN
load_css()

# =========================================
# LOGIN USER
# =========================================

def login_user(email, password):

    conn = sqlite3.connect("auth/database.db")

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

            stored_password = stored_password.encode("utf-8")

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        ):

            return user

    return None

# =========================================
# LOGIN PAGE
# =========================================

def login_page():

    # IMPORTANT
    # CSS reload on every rerun

    load_css()

    left, center, right = st.columns([1, 1.8, 1])

    with center:

        st.markdown(
            '<div class="main-card">',
            unsafe_allow_html=True
        )

        # =====================================
        # TITLE
        # =====================================

        st.markdown(
            """
            <div class="main-title">
                InsightAI
            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================
        # SUBTITLE
        # =====================================

        st.markdown(
            """
            <div class="login-description">
                Enterprise AI Analytics Platform
            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================
        # FEATURE ROW
        # =====================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.markdown(
                """
                <div class="feature-card">
                    📊<br>
                    Analytics
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                """
                <div class="feature-card">
                    📈<br>
                    Dashboards
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                """
                <div class="feature-card">
                    📄<br>
                    Reports
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:

            st.markdown(
                """
                <div class="feature-card">
                    🤖<br>
                    AI Insights
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================
        # INPUTS
        # =====================================

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        remember_me = st.checkbox(
            "Remember Me"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================
        # LOGIN BUTTON
        # =====================================

        if st.button(
            "Login to InsightAI",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "⚠️ Please fill all fields"
                )

                return

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.user_email = user[2]

                st.session_state.username = user[1]

                st.session_state.login_time = time.time()

                if remember_me:

                    st.session_state.remember_me = True

                st.success(
                    f"Welcome {user[1]}"
                )

                time.sleep(1)

                st.rerun()

            else:

                st.error(
                    "Invalid Email or Password"
                )

        # =====================================
        # GOOGLE SECTION
        # =====================================

        st.markdown(
            """
            
            """,
            unsafe_allow_html=True
        )

        google_login()

        # =====================================
        # EXTRA OPTIONS
        # =====================================

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                '<div class="secondary-btn">',
                unsafe_allow_html=True
            )

            if st.button(
                "Forgot Password"
            ):

                st.info(
                    "Go to sidebar → Forgot Password"
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                '<div class="secondary-btn">',
                unsafe_allow_html=True
            )

            if st.button(
                "Create Account"
            ):

                st.info(
                    "Go to sidebar → Register"
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        # =====================================
        # FOOTER
        # =====================================

        st.markdown(
            """
            <div class="brand-tagline">
                Designed & Developed by 
                <a href="https://www.linkedin.com/in/bhavesh-jha-51ab48246" target="_blank" style="color:#2563eb;
              text-decoration:none;
              font-weight:600;">
                Bhavesh Jha
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    login_page()
