from langchain_groq import ChatGroq
import streamlit as st

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama3-70b-8192",
    temperature=0
)

def verify_claim(claim: str):
    # 🚫 SERPAPI DISABLED
    response = llm.invoke(
        f"Classify this claim as Verified, Inaccurate, or False:\n{claim}"
    )
    return response.content
