from duckduckgo_search import DDGS

def verify_claim(claim):
    with DDGS() as ddgs:
        results = list(ddgs.text(claim, max_results=5))

    if not results:
        return "❌ Unverified", "No reliable sources found."

    evidence = " ".join(r["body"] for r in results)

    if any(word in evidence.lower() for word in ["confirmed", "according to", "reported"]):
        return "✅ Verified", "Multiple sources support this claim."

    return "⚠️ Inconclusive", "Some mentions found, but not clearly verified."
