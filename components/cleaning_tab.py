import streamlit as st
from core.data_cleaning import clean_dataset


def show_cleaning(df):

    # Always latest dataframe
    df = st.session_state.df

    st.subheader("🧹 Data Cleaning Center")

    # ---------------- STATUS CARDS ----------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "❌ Missing Values",
            int(df.isnull().sum().sum())
        )

    with c2:
        st.metric(
            "🔁 Duplicate Rows",
            int(df.duplicated().sum())
        )

    with c3:
        st.metric(
            "📊 Total Rows",
            int(df.shape[0])
        )

    st.divider()

    # ---------------- CLEANING METHOD ----------------
    method = st.selectbox(
        "Select Cleaning Method",
        [
            "Mean",
            "Median",
            "Mode",
            "Drop Rows"
        ]
    )

    # ---------------- CLEAN BUTTON ----------------
    if st.button("🚀 Clean Dataset"):

        cleaned_df = clean_dataset(df, method)

        # Update dataframe
        st.session_state.df = cleaned_df

        # Success flag
        st.session_state.clean_success = True

        # Refresh app
        st.rerun()

    # ---------------- SUCCESS MESSAGE ----------------
    if st.session_state.get("clean_success", False):

        st.success("✅ Dataset Cleaned Successfully")

        # Live Updated Metrics
        updated_df = st.session_state.df

        st.info(
            f"""
            📉 Missing Values After Cleaning: {updated_df.isnull().sum().sum()}
            
            🔁 Duplicates After Cleaning: {updated_df.duplicated().sum()}
            """
        )

        del st.session_state.clean_success

    st.divider()

    # ---------------- REMOVE DUPLICATES ----------------
    if st.button("🗑 Remove Duplicate Rows"):

        st.session_state.df = df.drop_duplicates()

        st.success("✅ Duplicate Rows Removed")

        st.rerun()

    st.divider()

    # ---------------- DROP COLUMNS ----------------
    drop_cols = st.multiselect(
        "Select Columns to Drop",
        df.columns
    )

    if st.button("❌ Drop Selected Columns"):

        st.session_state.df = df.drop(columns=drop_cols)

        st.success("✅ Columns Dropped Successfully")

        st.rerun()