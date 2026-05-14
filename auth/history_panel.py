import streamlit as st

from auth.auth_utils import (
    get_upload_history,
    get_report_history,
    get_chat_history
)

# =========================================
# HISTORY PANEL
# =========================================

def show_history_panel(user_email):

    st.sidebar.divider()

    st.sidebar.markdown("## 📜 History")

    # =====================================
    # UPLOAD HISTORY
    # =====================================

    with st.sidebar.expander(
        "📂 Upload History",
        expanded=False
    ):

        uploads = get_upload_history(
            user_email
        )

        if uploads:

            for file, time in uploads:

                st.write(f"📄 {file}")

                st.caption(time)

        else:

            st.info("No uploads found")

    # =====================================
    # REPORT HISTORY
    # =====================================

    with st.sidebar.expander(
        "📄 Report History",
        expanded=False
    ):

        reports = get_report_history(
            user_email
        )

        if reports:

            for report, time in reports:

                st.write(f"📊 {report}")

                st.caption(time)

        else:

            st.info("No reports found")

    # =====================================
    # CHAT HISTORY
    # =====================================

    with st.sidebar.expander(
        "💬 Chat History",
        expanded=False
    ):

        chats = get_chat_history(
            user_email
        )

        if chats:

            for question, answer, time in chats:

                with st.container():

                    st.markdown(
                        f"### ❓ {question}"
                    )

                    st.write(answer)

                    st.caption(time)

                    st.divider()

        else:

            st.info("No chats found")