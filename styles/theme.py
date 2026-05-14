import streamlit as st

def apply_theme(dark_mode: bool):

    base = """
    <style>
    * { font-family: 'Inter', sans-serif; }
    </style>
    """

    light_theme = base + """
    <style>
    .stApp {
        background: linear-gradient(145deg, #f0f4ff, #ffffff);
    }
    </style>
    """

    dark_theme = base + """
    <style>
    .stApp {
        background: linear-gradient(145deg, #0b0f19, #131a2e);
        color: white;
    }
    </style>
    """

    if dark_mode:
        st.markdown(dark_theme, unsafe_allow_html=True)
    else:
        st.markdown(light_theme, unsafe_allow_html=True)