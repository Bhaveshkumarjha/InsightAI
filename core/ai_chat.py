import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)
def ask_ai(df, prompt):

    dataset_context = f"""
    Dataset Shape: {df.shape}
    Columns: {list(df.columns)}
    Missing Values: {df.isnull().sum().sum()}
    Sample Data:
    {df.head(5).to_string()}
    """

    full_prompt = f"""
    You are a professional data analyst.

    Dataset:
    {dataset_context}

    User Question:
    {prompt}
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        model="llama-3.3-70b-versatile"
    )

    return response.choices[0].message.content
