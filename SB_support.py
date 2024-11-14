#Requirements
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

#LLM Model
llama = ChatGroq(
    model="LLaMA3-70B-8192",
    groq_api_key='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',
    temperature=0.0
)

#chatbot chains 
base_chain = ChatPromptTemplate.from_template("""
You are a customer support chatbot for a small business. You assist customers with their queries about products, manage bookings, and provide other necessary information. 

Customer Query: {query}

Respond clearly and concisely.
""") | llama | StrOutputParser()

# Streamlit UI
st.title("AI-Based Customer Support Chatbot")

# Sidebar Information
st.sidebar.header("Chatbot Information")
st.sidebar.write("""
This chatbot is designed to:
- Handle customer queries about products.
- Manage booking requests.
- Provide business information.
- Respond in multiple languages.
""")


