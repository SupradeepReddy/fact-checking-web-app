import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

HF_API_TOKEN = st.secrets.get("HF_API_TOKEN")
if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN not found in Streamlit secrets")

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=HF_API_TOKEN,
    temperature=0
)

prompt = PromptTemplate.from_template(
    """
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
"""
)

def extract_claims(text: str):
    chain = prompt | llm
    response = chain.invoke({"text": text})
    return [line for line in response.split("\n") if line.strip()]
