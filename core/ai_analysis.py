import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def generate_ai_summary(df):

    dataset_info = f"""
    Dataset Shape: {df.shape}
    Columns: {list(df.columns)}
    Missing Values: {df.isnull().sum().sum()}
    Sample Data: {df.head(5).to_string()}
    """

    prompt = f"""
    Analyze this dataset professionally.

    Dataset:
    {dataset_info}

    Give:
    1. Data Quality
    2. Patterns
    3. Recommendations
    4. Business Insights
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile"
    )

    return response.choices[0].message.content
