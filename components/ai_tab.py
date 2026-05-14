import streamlit as st
from core.ai_analysis import generate_ai_summary

def show_ai_tab(df):

    st.subheader("🤖 AI Insights")

    if st.button("Generate AI Summary"):

        summary = generate_ai_summary(df)

        st.success(summary)