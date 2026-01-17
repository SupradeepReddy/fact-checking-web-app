import streamlit as st
from serpapi import GoogleSearch
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

SERPAPI_API_KEY = st.secrets.get("SERPAPI_API_KEY")
HF_API_TOKEN = st.secrets.get("HF_API_TOKEN")

if not SERPAPI_API_KEY or not HF_API_TOKEN:
    raise ValueError("Missing API keys in Streamlit secrets")

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=HF_API_TOKEN,
    temperature=0
)

verification_prompt = PromptTemplate.from_template(
    """
Claim:
{claim}

Web Evidence:
{evidence}

Based on the evidence, classify the claim as ONE of:
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
