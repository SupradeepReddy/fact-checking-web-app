import streamlit as st
from serpapi import GoogleSearch
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
SERPAPI_API_KEY = st.secrets.get("SERPAPI_API_KEY")

if not GROQ_API_KEY or not SERPAPI_API_KEY:
    raise ValueError("Missing GROQ_API_KEY or SERPAPI_API_KEY in Streamlit secrets")

llm = ChatGroq(
    model="llama3-70b-8192",
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
