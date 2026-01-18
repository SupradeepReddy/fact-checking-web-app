import re

def extract_claims(text):
    claims = []

    patterns = [
        r"\b\d{4}\b",                           # years
        r"\$\d+(\.\d+)?\s?(billion|million)?", # money
        r"\b\d+(\.\d+)?%\b",                    # percentages
        r"\b(released|launched|announced)\b.*",# releases
    ]

    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        for pattern in patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                claims.append(sentence.strip())
                break

    return claims[:15]  # limit for performance
