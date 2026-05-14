import pandas as pd
import streamlit as st


def load_file(uploaded_file):

    try:

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        else:

            df = pd.read_excel(uploaded_file)

        st.success("✅ File Uploaded Successfully")

        return df

    except Exception as e:

        st.error(f"File Error: {e}")

        return None