import streamlit as st
from streamlit_oauth import OAuth2Component

# =====================================
# GOOGLE OAUTH CONFIG
# =====================================

CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]

CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"

TOKEN_URL = "https://oauth2.googleapis.com/token"

REDIRECT_URI = "http://localhost:8501"

# =====================================
# OAUTH COMPONENT
# =====================================

oauth2 = OAuth2Component(

    CLIENT_ID,

    CLIENT_SECRET,

    AUTHORIZE_URL,

    TOKEN_URL

)

# =====================================
# GOOGLE BUTTON CSS
# =====================================

def load_google_css():

    st.markdown(
        """
        <style>

        /* ===================================== */
        /* CONTAINER */
        /* ===================================== */

        .google-container {

            display: flex;

            justify-content: center;

            align-items: center;

            margin-top: 12px;

            margin-bottom: 12px;
        }

        /* ===================================== */
        /* BUTTON */
        /* ===================================== */

        .google-container button {

            width: auto !important;

            min-width: 260px !important;

            max-width: 300px !important;

            height: 25px !important;

            padding: 0 18px !important;

            border-radius: 12px !important;

            border: 1px solid #d1d5db !important;

            background: white !important;

            color: #111827 !important;

            font-size: 7px !important;

            font-weight: 200 !important;

            transition: all 0.2s ease !important;

            box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
        }

        /* ===================================== */
        /* HOVER */
        /* ===================================== */

        .google-container button:hover {

            background: #f9fafb !important;

            border: 1px solid #9ca3af !important;

            color: #111827 !important;
        }

        /* ===================================== */
        /* ACTIVE / FOCUS */
        /* ===================================== */

        .google-container button:focus,
        .google-container button:active {

            outline: none !important;

            box-shadow: none !important;

            border: 1px solid #6b7280 !important;
        }

        /* ===================================== */
        /* REMOVE EXTRA WHITE SPACE */
        /* ===================================== */

        iframe {

            width: 260px !important;

            margin: auto !important;

            display: block !important;

            overflow: hidden !important;
        }

        </style>
        """,

        unsafe_allow_html=True
    )

# =====================================
# GOOGLE LOGIN
# =====================================

def google_login():

    load_google_css()

    st.markdown(

        '<div class="google-container">',

        unsafe_allow_html=True
    )

    result = oauth2.authorize_button(

        name="Continue with Google",

        icon="https://developers.google.com/identity/images/g-logo.png",

        redirect_uri=REDIRECT_URI,

        scope="openid email profile",

        key="google"

    )

    st.markdown(

        '</div>',

        unsafe_allow_html=True
    )

    # =================================
    # LOGIN SUCCESS
    # =================================

    if result and "token" in result:

        st.session_state.logged_in = True

        st.session_state.user_email = (
            "Google User"
        )

        st.success(
            "✅ Google Login Successful"
        )

        st.rerun()
