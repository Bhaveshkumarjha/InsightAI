
import streamlit as st

from core.pdf_generator import generate_pdf
from core.ppt_generator import generate_ppt


def show_reports(df, numeric_columns):

    st.markdown("## 📄 Reports & Downloads")

    # =========================================
    # DOWNLOAD CSV
    # =========================================

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv,
        file_name="InsightAI_Dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    # =========================================
    # PDF + PPT COLUMNS
    # =========================================

    col1, col2 = st.columns(2)

    # =========================================
    # PDF REPORT
    # =========================================

    with col1:

        if st.button(
            "📄 Generate Advanced PDF Report",
            use_container_width=True
        ):

            with st.spinner("Generating Professional PDF Report..."):

                try:

                    # GENERATE PDF
                    pdf_file = generate_pdf(df)

                    st.success("✅ PDF Report Generated Successfully")

                    # DOWNLOAD PDF
                    with open(pdf_file, "rb") as file:

                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=file,
                            file_name=pdf_file,
                            mime="application/pdf",
                            use_container_width=True
                        )

                except Exception as e:

                    st.error(f"PDF Error: {e}")

    # =========================================
    # PPT REPORT
    # =========================================

    with col2:

        if st.button(
            "📊 Generate Executive PowerPoint",
            use_container_width=True
        ):

            with st.spinner("📊 Generating Boardroom Presentation...."):

                try:

                    # GENERATE PPT
                    ppt_file = generate_ppt(df)

                    st.success("✅ Executive PPT Generated Successfully")

                    # DOWNLOAD PPT
                    with open(ppt_file, "rb") as file:

                        st.download_button(
                            label="⬇️ Download Executive PPT",
                            data=file,
                            file_name=ppt_file,
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True
                        )

                except Exception as e:

                    st.error(f"PPT Error: {e}")

    st.divider()

    # =========================================
    # DATASET SUMMARY
    # =========================================

    rows, cols = df.shape

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    st.markdown("### 📌 Current Dataset Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Rows", rows)

    with c2:
        st.metric("Columns", cols)

    with c3:
        st.metric("Missing Values", missing)

    with c4:
        st.metric("Duplicates", duplicates)

    st.divider()

    # =========================================
    # COLUMN DETAILS
    # =========================================

    st.markdown("### 📋 Dataset Columns Information")

    column_info = {
        "Column Name": df.columns,
        "Datatype": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    }

    st.dataframe(
        column_info,
        use_container_width=True
    )
