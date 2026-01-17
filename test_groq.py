from langchain_groq import ChatGroq

llm = ChatGroq(api_key="gsk_your_real_key_here")
print(llm.invoke("Say hello in one word"))
