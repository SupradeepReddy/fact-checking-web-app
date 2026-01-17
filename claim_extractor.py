import streamlit as st
from langchain_huggingface import ChatHuggingFace
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

HF_API_TOKEN = st.secrets.get("HF_API_TOKEN")
if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN not found in Streamlit secrets")

llm = ChatHuggingFace(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=HF_API_TOKEN,
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
