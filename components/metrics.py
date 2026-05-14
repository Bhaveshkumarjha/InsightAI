import streamlit as st

def show_metrics(df, numeric_columns):

    # 🔥 ALWAYS take fresh data from session state
    df = st.session_state.df

    rows, cols = df.shape
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    numeric_count = len(numeric_columns)

    st.markdown("### 📊 Dataset Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg,#1e3c72,#2a5298);
                padding:15px;
                border-radius:15px;
                color:white;
                text-align:center;
                box-shadow:0px 4px 15px rgba(0,0,0,0.2);
            ">
                <h3 style="margin:0">{rows}</h3>
                <p style="margin:0">📋 Rows</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg,#4e73df,#6f86d6);
                padding:15px;
                border-radius:15px;
                color:white;
                text-align:center;
                box-shadow:0px 4px 15px rgba(0,0,0,0.2);
            ">
                <h3 style="margin:0">{cols}</h3>
                <p style="margin:0">📊 Columns</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg,#ff6b6b,#ff8787);
                padding:15px;
                border-radius:15px;
                color:white;
                text-align:center;
                box-shadow:0px 4px 15px rgba(0,0,0,0.2);
            ">
                <h3 style="margin:0">{missing}</h3>
                <p style="margin:0">❌ Missing</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg,#f6c23e,#f39c12);
                padding:15px;
                border-radius:15px;
                color:white;
                text-align:center;
                box-shadow:0px 4px 15px rgba(0,0,0,0.2);
            ">
                <h3 style="margin:0">{duplicates}</h3>
                <p style="margin:0">🔁 Duplicates</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg,#2ecc71,#27ae60);
                padding:15px;
                border-radius:15px;
                color:white;
                text-align:center;
                box-shadow:0px 4px 15px rgba(0,0,0,0.2);
            ">
                <h3 style="margin:0">{numeric_count}</h3>
                <p style="margin:0">🔢 Numeric</p>
            </div>
            """,
            unsafe_allow_html=True
        )