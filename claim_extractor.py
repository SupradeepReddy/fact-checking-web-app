import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Get OpenAI key
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in Streamlit secrets")

llm = ChatOpenAI(
    model="gpt-4o-mini",
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
