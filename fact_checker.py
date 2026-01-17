import streamlit as st
from serpapi import GoogleSearch
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

SERPAPI_API_KEY = st.secrets.get("SERPAPI_API_KEY")
if not SERPAPI_API_KEY:
    raise ValueError("SERPAPI_API_KEY not found in Streamlit secrets.")

llm = Ollama(model="llama3")

verification_prompt = PromptTemplate.from_template(
    """
Claim:
{claim}

Web Search Evidence:
{evidence}

Classify the claim as:
- Verified
- Inaccurate
- False

Give a short explanation.
"""
)

def verify_claim(claim: str):
    search = GoogleSearch({
        "q": claim,
        "api_key": SERPAPI_API_KEY,
        "num": 5
    })

    results = search.get_dict()

    evidence = ""
    for r in results.get("organic_results", []):
        evidence += r.get("snippet", "") + "\n"

    chain = verification_prompt | llm
    return chain.invoke({
        "claim": claim,
        "evidence": evidence
    })
