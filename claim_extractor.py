import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in Streamlit secrets")

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You extract factual claims from documents."),
    ("human", """
Extract factual claims from the text below.

Only include:
- Dates
- Statistics
- Financial figures
- Model releases
- Technology or policy claims

Return a numbered list.
Do NOT add explanations.

TEXT:
{text}
""")
])

def extract_claims(text: str):
    messages = prompt.format_messages(text=text)
    response = llm.invoke(messages)
    return [line for line in response.content.split("\n") if line.strip()]
