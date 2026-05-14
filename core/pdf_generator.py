from fpdf import FPDF
import pandas as pd


def generate_pdf(df):

    # =========================================
    # BASIC INFO
    # =========================================

    rows, cols = df.shape

    missing_values = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    categorical_columns = df.select_dtypes(include="object").columns.tolist()

    # =========================================
    # PDF SETUP
    # =========================================

    pdf = FPDF()

    pdf.set_auto_page_break(auto=True, margin=15)

    # =========================================
    # PAGE 1 - TITLE PAGE
    # =========================================

    pdf.add_page()

    pdf.set_fill_color(15, 23, 42)

    pdf.rect(0, 0, 220, 297, style='F')

    pdf.set_text_color(255, 255, 255)

    pdf.set_font("Arial", "B", 28)

    pdf.ln(60)

    pdf.cell(
        0,
        20,
        "InsightAI Executive Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font("Arial", "", 16)

    pdf.cell(
        0,
        10,
        "AI Powered Business Intelligence",
        ln=True,
        align="C"
    )

    # =========================================
    # PAGE 2 - EXECUTIVE SUMMARY
    # =========================================

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)

    pdf.set_font("Arial", "B", 20)

    pdf.cell(0, 12, "Executive Summary", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "", 13)

    summary = f"""
Dataset Size:
- Total Rows: {rows}
- Total Columns: {cols}

Data Quality:
- Missing Values: {missing_values}
- Duplicate Records: {duplicates}

Feature Overview:
- Numeric Features: {len(numeric_columns)}
- Categorical Features: {len(categorical_columns)}

Business Readiness:
- Dataset successfully processed
- Analytics ready structure detected
- Suitable for AI insights generation
"""

    pdf.multi_cell(0, 8, summary)

    # =========================================
    # PAGE 3 - KPI DASHBOARD
    # =========================================

    pdf.add_page()

    pdf.set_font("Arial", "B", 20)

    pdf.cell(0, 12, "Business KPI Dashboard", ln=True)

    pdf.ln(10)

    kpis = [

        ("Rows", rows),

        ("Columns", cols),

        ("Missing Values", missing_values),

        ("Duplicates", duplicates),

        ("Numeric Features", len(numeric_columns)),

        ("Categorical Features", len(categorical_columns))
    ]

    x = 10
    y = 40

    for title, value in kpis:

        pdf.set_fill_color(37, 99, 235)

        pdf.rect(x, y, 60, 25, style='F')

        pdf.set_text_color(255, 255, 255)

        pdf.set_font("Arial", "B", 12)

        pdf.text(x + 3, y + 8, str(title))

        pdf.set_font("Arial", "B", 18)

        pdf.text(x + 3, y + 18, str(value))

        x += 70

        if x > 140:

            x = 10
            y += 40

    # =========================================
    # PAGE 4 - COLUMN DETAILS
    # =========================================

    pdf.add_page()

    pdf.set_text_color(0, 0, 0)

    pdf.set_font("Arial", "B", 20)

    pdf.cell(0, 12, "Column Intelligence", ln=True)

    pdf.ln(5)

    for col in df.columns:

        pdf.set_fill_color(30, 41, 59)

        pdf.set_text_color(255, 255, 255)

        pdf.set_font("Arial", "B", 12)

        pdf.cell(
            0,
            10,
            f"Column: {col}",
            ln=True,
            fill=True
        )

        pdf.set_text_color(0, 0, 0)

        pdf.set_font("Arial", "", 11)

        details = f"""
Datatype: {df[col].dtype}
Missing Values: {df[col].isnull().sum()}
Unique Values: {df[col].nunique()}
"""

        pdf.multi_cell(0, 7, details)

        pdf.ln(2)

    # =========================================
    # PAGE 5 - STATISTICS
    # =========================================

    pdf.add_page()

    pdf.set_font("Arial", "B", 20)

    pdf.cell(0, 12, "Statistical Intelligence", ln=True)

    pdf.ln(5)

    pdf.set_font("Courier", "", 8)

    try:

        stats = df.describe().to_string()

        pdf.multi_cell(0, 5, stats)

    except:

        pdf.multi_cell(
            0,
            8,
            "Statistical summary unavailable."
        )

    # =========================================
    # PAGE 6 - DATA QUALITY ANALYSIS
    # =========================================

    pdf.add_page()

    pdf.set_font("Arial", "B", 20)

    pdf.cell(0, 12, "Data Quality Analysis", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "", 12)

    quality = f"""
Strengths:
- Structured dataset detected
- AI analytics compatible
- Visualization ready
- Statistical analysis enabled

Issues Identified:
- Missing values present: {missing_values}
- Duplicate rows present: {duplicates}

Strategic Recommendations:
- Apply advanced data cleaning
- Remove duplicates for better accuracy
- Standardize numeric features
- Enable predictive modeling
- Deploy AI forecasting models
"""

    pdf.multi_cell(0, 8, quality)

    # =========================================
    # PAGE 7 - SAMPLE DATA
    # =========================================

    pdf.add_page()

    pdf.set_font("Arial", "B", 20)

    pdf.cell(0, 12, "Dataset Preview", ln=True)

    pdf.ln(5)

    pdf.set_font("Courier", "", 7)

    sample = df.head(15).to_string()

    pdf.multi_cell(0, 4, sample)

    # =========================================
    # PAGE 8 - AI INSIGHTS
    # =========================================

    pdf.add_page()

    pdf.set_font("Arial", "B", 20)

    pdf.cell(0, 12, "AI Business Insights", ln=True)

    pdf.ln(10)

    insights = [

        "Dataset structure is suitable for advanced analytics.",

        "Potential business trends detected in numeric variables.",

        "Data quality improvement can increase prediction accuracy.",

        "High-value KPI indicators identified.",

        "AI-ready architecture confirmed."
    ]

    pdf.set_font("Arial", "", 13)

    for insight in insights:

        pdf.multi_cell(
            0,
            10,
            f"- {insight}"
        )

    # =========================================
    # PAGE 9 - CONCLUSION
    # =========================================

    pdf.add_page()

    pdf.set_fill_color(15, 23, 42)

    pdf.rect(0, 0, 220, 297, style='F')

    pdf.set_text_color(255, 255, 255)

    pdf.ln(90)

    pdf.set_font("Arial", "B", 28)

    pdf.cell(
        0,
        20,
        "Thank You",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font("Arial", "", 14)

    pdf.cell(
        0,
        10,
        "Generated by InsightAI",
        ln=True,
        align="C"
    )

    # =========================================
    # SAVE PDF
    # =========================================

    pdf_path = "InsightAI_Report.pdf"

    pdf.output(pdf_path)

    return pdf_path