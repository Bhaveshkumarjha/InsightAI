import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

from core.file_handler import load_file
from core.ppt_generator import generate_ppt

from components.overview_tab import show_overview
from components.visualization_tab import show_visualization
from components.cleaning_tab import show_cleaning
from components.ai_tab import show_ai_tab
from components.reports_tab import show_reports
from components.chatbot_tab import show_chatbot
from components.metrics import show_metrics

from auth.google_login import google_login
from styles.theme import apply_theme

# =========================================
# AUTH IMPORTS
# =========================================

from auth.auth_utils import (
    create_users_table,
    save_chat_history,
    get_dataset_history,
    get_chat_by_dataset,
    save_upload_history,
    save_report_history
)

from auth.login import login_page
from auth.register import register_page
from auth.forgot_password import forgot_password_page
from auth.reset_password import reset_password_page

# =========================================
# CREATE DATABASE
# =========================================

create_users_table()

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="InsightAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Sidebar width */
section[data-testid="stSidebar"] {
    min-width: 320px !important;
    max-width: 320px !important;
}

/* Keep sidebar visible on desktop */
@media (min-width: 768px) {
    section[data-testid="stSidebar"] {
        transform: translateX(0px) !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================
# SESSION STATE DEFAULTS
# =========================================

defaults = {
    "df": None,
    "messages": [],
    "saved_chats": [],
    "dark_mode": False,
    "logged_in": False,
    "current_file": None,
    "user_email": None,
    "login_time": None,
    "selected_dataset": None,
    "active_tab": "📊 Overview"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================
# SESSION TIMEOUT
# =========================================

SESSION_TIMEOUT = 3600

if st.session_state.logged_in:

    if st.session_state.login_time:

        elapsed = time.time() - st.session_state.login_time

        if elapsed > SESSION_TIMEOUT:

            st.session_state.logged_in = False
            st.session_state.user_email = None

            st.warning("⚠️ Session Expired")

            st.rerun()


# =========================================
# LOGIN / REGISTER
# =========================================

if not st.session_state.logged_in:

    st.sidebar.title("🔐 Authentication")

    menu = st.sidebar.selectbox(
        "Select Option",
        [
            "Login",
            "Register",
            "Forgot Password",
            "Reset Password"
        ]
    )

    if menu == "Login":

        login_page()

        st.divider()

    elif menu == "Register":

        register_page()

    elif menu == "Forgot Password":

        forgot_password_page()

    elif menu == "Reset Password":

        reset_password_page()

    st.stop()


# =========================================
# APPLY THEME
# =========================================

apply_theme(st.session_state.dark_mode)


# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.sidebar.markdown("## ☰ Navigation")
    st.title("⚙️ InsightAI")

    st.success(
        f"✅ Logged in as:\n{st.session_state.user_email}"
    )

    st.divider()

    # USER PROFILE
    st.subheader("👤 User Profile")

    st.write(
        f"📧 {st.session_state.user_email}"
    )

    if st.session_state.login_time:

        login_time = datetime.fromtimestamp(
            st.session_state.login_time
        ).strftime("%d %b %Y %I:%M %p")

        st.caption(f"🕒 {login_time}")

    st.divider()

    # DATASET HISTORY
    st.subheader("📂 Dataset History")

    dataset_history = get_dataset_history(
        st.session_state.user_email
    )

    if len(dataset_history) > 0:

        for i, dataset in enumerate(dataset_history):

            dataset_name = dataset[0]

            unique_key = f"dataset_{dataset_name}_{i}"

            if st.button(
                f"📊 {dataset_name}",
                key=unique_key
            ):

                st.session_state.selected_dataset = (
                    dataset_name
                )

    else:

        st.caption("No dataset history")

    st.divider()

    # CHAT HISTORY
    st.subheader("💬 Dataset Chats")

    if st.session_state.selected_dataset:

        st.info(
            f"Selected Dataset:\n{st.session_state.selected_dataset}"
        )

        chats = get_chat_by_dataset(

            st.session_state.user_email,

            st.session_state.selected_dataset

        )

        if len(chats) > 0:

            for chat in chats:

                question = chat[0]
                answer = chat[1]
                created_at = chat[2]

                with st.expander(
                    f"❓ {question[:40]}..."
                ):

                    st.markdown(
                        f"**Question:** {question}"
                    )

                    st.markdown(
                        f"**Answer:** {answer}"
                    )

                    st.caption(created_at)

        else:

            st.caption(
                "No chats found for this dataset"
            )

    else:

        st.caption(
            "Select dataset to view chats"
        )

    st.divider()

    # THEME TOGGLE

    if st.button("🌓 Toggle Theme"):

        st.session_state.dark_mode = (
            not st.session_state.dark_mode
        )

        st.rerun()

    # RESET APP

    if st.button("🔄 Reset App"):

        st.session_state.df = None
        st.session_state.messages = []
        st.session_state.current_file = None
        st.session_state.selected_dataset = None
        st.session_state.active_tab = "📊 Overview"

        st.success("✅ App Reset Complete")

        st.rerun()

    # LOGOUT

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.df = None
        st.session_state.messages = []
        st.session_state.current_file = None
        st.session_state.user_email = None
        st.session_state.login_time = None
        st.session_state.selected_dataset = None
        st.session_state.active_tab = "📊 Overview"

        st.success("✅ Logged Out Successfully")

        st.rerun()


# =========================================
# HEADER
# =========================================

st.title("🧠 InsightAI - Smart Data Analytics")

st.caption(
    "AI Powered Analytics • Executive Dashboards • Smart Insights"
)


# =========================================
# FILE UPLOAD
# =========================================

uploaded_file = st.file_uploader(
    "📂 Upload CSV or Excel File",
    type=["csv", "xlsx"]
)


# =========================================
# LOAD FILE
# =========================================

if uploaded_file is not None:

    if st.session_state.current_file != uploaded_file.name:

        try:

            with st.spinner("Loading dataset..."):

                # LOAD DATA
                st.session_state.df = load_file(
                    uploaded_file
                )

                # SAVE FILE NAME
                st.session_state.current_file = (
                    uploaded_file.name
                )

                # SAVE HISTORY
                save_upload_history(

                    st.session_state.user_email,

                    uploaded_file.name,

                    uploaded_file.type,

                    st.session_state.df.shape[0],

                    st.session_state.df.shape[1]

                )

                # CLEAR CHAT
                st.session_state.messages = []

                st.success(
                    f"✅ File Loaded Successfully: {uploaded_file.name}"
                )

        except Exception as e:

            st.error(f"❌ File Load Error: {e}")


# =========================================
# MAIN APP
# =========================================

if st.session_state.df is not None:

    df = st.session_state.df.copy()

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns.tolist()

    # LIVE METRICS
    show_metrics(df, numeric_columns)

    # TABS
    tabs = [

        "📊 Overview",
        "📈 Visualization",
        "🧹 Cleaning",
        "🤖 AI Insights",
        "📄 Reports",
        "💬 InsightGPT"

    ]

    selected_tab = st.radio(
        "",
        tabs,
        horizontal=True,
        index=tabs.index(st.session_state.active_tab)
    )

    st.session_state.active_tab = selected_tab

    st.divider()

    # OVERVIEW
    if selected_tab == "📊 Overview":
        show_overview(df)

    # VISUALIZATION
    elif selected_tab == "📈 Visualization":
        show_visualization(
            df,
            numeric_columns,
            categorical_columns
        )

    # CLEANING
    elif selected_tab == "🧹 Cleaning":
        show_cleaning(df)

    # AI INSIGHTS
    elif selected_tab == "🤖 AI Insights":
        show_ai_tab(df)

    # REPORTS
    elif selected_tab == "📄 Reports":

        show_reports(df, numeric_columns)

        if st.button("📥 Save Report History"):

            report_name = (

                f"Executive_Report_"

                f"{datetime.now().strftime('%H%M%S')}"

            )

            save_report_history(

                st.session_state.user_email,

                report_name,

                "PPT"

            )

            st.success(
                "✅ Report Saved Successfully"
            )

    # CHATBOT
    elif selected_tab == "💬 InsightGPT":

        show_chatbot(df)

        # SAVE CHAT
        if len(st.session_state.messages) >= 2:

            last_user = st.session_state.messages[-2]
            last_ai = st.session_state.messages[-1]

            if (

                isinstance(last_user, dict)

                and isinstance(last_ai, dict)

            ):

                if (

                    last_user.get("role") == "user"

                    and last_ai.get("role") == "assistant"

                ):

                    question = last_user.get("content", "")
                    answer = last_ai.get("content", "")

                    if question and answer:

                        chat_key = f"{question}_{answer}"

                        if "saved_chats" not in st.session_state:

                            st.session_state.saved_chats = []

                        if chat_key not in st.session_state.saved_chats:

                            save_chat_history(
                                st.session_state.user_email,
                                question,
                                answer,
                                st.session_state.current_file
                            )

                            st.session_state.saved_chats.append(
                                chat_key
                            )

# =========================================
# NO FILE
# =========================================

else:

    st.info(
        "👆 Please upload a dataset to start analysis"
    )
