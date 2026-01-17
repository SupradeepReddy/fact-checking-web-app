from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Local LLM (no API key needed)
llm = Ollama(model="llama3")

prompt = PromptTemplate.from_template(
    """
Extract factual claims from the text below.

Only include:
- Dates
- Statistics
- Financial numbers
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
