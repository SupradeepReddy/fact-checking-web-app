import streamlit as st
from pdf_loader import extract_text_from_pdf
from claim_extractor import extract_claims
from fact_checker import verify_claim

st.set_page_config(page_title="Fact Checker", layout="wide")

st.title("📄 Fact-Checking Web App (Free & Deployed)")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with st.spinner("Reading PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    claims = extract_claims(text)

    if not claims:
        st.warning("No factual claims detected.")
    else:
        st.subheader("Verification Results")

        for i, claim in enumerate(claims, 1):
            verdict, explanation = verify_claim(claim)

            st.markdown(f"### Claim {i}")
            st.write(claim)
            st.write(verdict)
            st.caption(explanation)
