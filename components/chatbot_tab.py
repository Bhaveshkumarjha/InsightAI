import streamlit as st

from core.ai_chat import ask_ai

from auth.auth_utils import save_chat_history

# =========================================
# INSIGHTGPT COPILOT
# =========================================

def show_chatbot(df):

    # =====================================
    # HEADER
    # =====================================

    st.subheader(" InsightGPT")

    st.caption(
        "Chat with your dataset using AI-powered analytics"
    )

    st.divider()

    # =====================================
    # EMPTY CHAT
    # =====================================

    if len(st.session_state.messages) == 0:

        st.info(
            """
            👋 Welcome to Insight GPT
            
            You can ask:
            
            • What are the sales trends?
            • Show top performing categories
            • Detect missing values
            • Give business insights
            • Predict important patterns
            """
        )

    # =====================================
    # SHOW CHAT HISTORY
    # =====================================

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(
                msg["content"]
            )

    # =====================================
    # CHAT INPUT
    # =====================================

    prompt = st.chat_input(
        "Ask anything about your dataset..."
    )

    # =====================================
    # USER MESSAGE
    # =====================================

    if prompt:

        # SAVE USER MESSAGE
        st.session_state.messages.append({

            "role": "user",

            "content": prompt

        })

        # SHOW USER MESSAGE
        with st.chat_message("user"):

            st.write(prompt)

        # =================================
        # AI RESPONSE
        # =================================

        with st.chat_message("assistant"):

            with st.spinner(
                "Insight GPT is analyzing your data..."
            ):

                try:

                    response = ask_ai(
                        df,
                        prompt
                    )

                except Exception as e:

                    response = (
                        f"❌ AI Error: {e}"
                    )

                st.write(response)

        # =================================
        # SAVE ASSISTANT MESSAGE
        # =================================

        st.session_state.messages.append({

            "role": "assistant",

            "content": response

        })

        # =================================
        # SAVE DATABASE HISTORY
        # =================================

        try:

            save_chat_history(

                st.session_state.user_email,

                st.session_state.current_file,

                prompt,

                response

            )

        except:

            pass

        st.rerun()
