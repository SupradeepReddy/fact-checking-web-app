import streamlit as st
from pdf_loader import extract_text_from_pdf
from claim_extractor import extract_claims
from fact_checker import verify_claim

st.set_page_config(page_title="Fact Checker", layout="wide")

st.title("📄 Fact-Checking Web App")
st.write("Upload a PDF to verify factual claims using live web data.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    try:
        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)

        with st.spinner("Extracting factual claims..."):
            claims = extract_claims(text)

        if not claims:
            st.warning("No factual claims detected.")
        else:
            st.subheader("Verification Results")

            for claim in claims:
                st.markdown(f"### 🔍 {claim}")
                with st.spinner("Checking live web data..."):
                    verdict = verify_claim(claim)
                st.write(verdict)
                st.divider()

    except Exception as e:
        st.error(f"Error occurred: {e}")
