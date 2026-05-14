import streamlit as st
import pandas as pd

# =========================================
# OVERVIEW TAB
# =========================================

def show_overview(df):

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.subheader("📊 Column Information")

    info_df = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing Values": df.isnull().sum(),

        "Unique Values": df.nunique()

    })

    st.dataframe(
        info_df,
        use_container_width=True
    )

    st.subheader("❗ Missing Values Summary")

    missing_df = pd.DataFrame({

        "Column": df.columns,

        "Missing Values": df.isnull().sum()

    })

    st.dataframe(
        missing_df,
        use_container_width=True
    )

    # =====================================
    # FOOTER
    # =====================================

    st.markdown(
        """

        <div style="text-align:center; margin-top:20px;" class="brand-tagline">
                Designed & Developed by
                <a href="https://www.linkedin.com/in/bhavesh-jha-51ab48246" target="_blank" style="color:#2563eb;
              text-decoration:none;
              font-weight:600;">
                Bhavesh Jha
            </div>
        """,
        unsafe_allow_html=True
    )