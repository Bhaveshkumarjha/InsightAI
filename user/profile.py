import streamlit as st


# =========================================
# USER PROFILE
# =========================================

def show_profile():

    st.subheader("👤 User Profile")

    email = st.session_state.get(
        "user_email",
        "Unknown"
    )

    st.info(f"📧 Logged in as: {email}")

    st.success("✅ Account Active")

    st.write("Plan: Free Tier")