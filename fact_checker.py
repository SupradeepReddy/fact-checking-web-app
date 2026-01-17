import streamlit as st
from serpapi import GoogleSearch
from langchain_huggingface import ChatHuggingFace
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

SERPAPI_API_KEY = st.secrets.get("SERPAPI_API_KEY")
HF_API_TOKEN = st.secrets.get("HF_API_TOKEN")

if not SERPAPI_API_KEY or not HF_API_TOKEN:
    raise ValueError("Missing API keys in Streamlit secrets")

llm = ChatHuggingFace(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=HF_API_TOKEN,
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a fact-checking assistant."),
    ("human", """
Claim:
{claim}

Web Evidence:
{evidence}

Classify the claim as ONE of:
- Verified
- Inaccurate
- False

Then give a short explanation.
""")
])

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

    messages = prompt.format_messages(
        claim=claim,
        evidence=evidence
    )

    response = llm.invoke(messages)
    return response.content
