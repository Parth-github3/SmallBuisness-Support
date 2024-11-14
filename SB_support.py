#Requirements
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from googletrans import Translator  # Multilingual support
import pdfplumber

#LLM Model
llama = ChatGroq(
    model="LLaMA3-70B-8192",
    groq_api_key='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',
    temperature=0.0
)

translator = Translator()  # Translator for multilingual support

##################################### Base Chains ###########################################
# 1. Input Translation Chain
translate_input_chain = (
    ChatPromptTemplate.from_template("""
You are a language translator. Detect the input language and translate it into English. 
Input: "{input_text}"
""")
    | llama
    | StrOutputParser()
)

# 2. Output Translation Chain
translate_output_chain = (
    ChatPromptTemplate.from_template("""
You are a language translator. Translate the following text into the target language: "{target_language}".
Input Text: "{response_text}"
""")
    | llama
    | StrOutputParser()
)

# 3. Fallback Error Handling Chain
fallback_chain = (
    ChatPromptTemplate.from_template("""
You are a fallback assistant. If the system cannot handle the query, respond politely and suggest contacting support.
Input Query: "{query}"
""")
    | llama
    | StrOutputParser()
)

##################################### Advanced Chains ###########################################
# 4. General Query Chain
query_chain = (
    ChatPromptTemplate.from_template("""
You are a customer support assistant. The user has the query: "{query}". 
Respond with a clear and concise answer. If you don't know the answer, ask for more details or suggest contacting support.
""")
    | llama
    | StrOutputParser()
)

# 5. Booking Management Chain
booking_chain = (
    ChatPromptTemplate.from_template("""
You are a virtual assistant that manages bookings for a business. The user wants to {action} for a service: "{service}". 
If they provide a time or date, confirm the booking; if not, ask for more details.
""")
    | llama
    | StrOutputParser()
)

# 6. Product Information Chain
product_info_chain = (
    ChatPromptTemplate.from_template("""
You are a knowledgeable sales assistant. The user is asking about: "{product}". 
Provide detailed information including features, pricing, and availability.
""")
    | llama
    | StrOutputParser()
)

# 7. Customization Chain
custom_chain = (
    ChatPromptTemplate.from_template("""
You are assisting a small business that specializes in {business_type}. Tailor your response to reflect the company's services and brand tone.
The user query is: "{query}".
""")
    | llama
    | StrOutputParser()
)

# 8. Contextual Query Chain
context_chain = (
    ChatPromptTemplate.from_template("""
You are a follow-up assistant. Based on the previous interaction: "{previous_interaction}", suggest a related query or provide further assistance.
""")
    | llama
    | StrOutputParser()
)
# 9. Buisness Understanding Chain
buisness_chain = (
    ChatPromptTemplate.from_template("""
You are a data analyist. Based on the given text: "{buisness}", 
Identify the buisness, the products and services offered in the buisness, the product information, 
    customer reviews and any other neccessary information regarding the buisness.
""")
    | llama
    | StrOutputParser()
    #| RunnablePassthrough
)

##################################### Streamlit UI ###########################################
st.title("AI Customer Support Assistant")
st.sidebar.header("About")
st.sidebar.write("""
This app is a customizable AI-powered customer support chatbot. Features include:
- Multilingual support
- Booking management
- Product information retrieval
- Contextual query handling
- Customizable responses for businesses
""")

# Sidebar selection
option = st.selectbox(
    "Choose a support module:",
    ("General Query", "Booking Management", "Product Information", "Customized Responses"),
    index=0
)

# User Interaction
user_input = st.text_input("Ask your question here:")

uploaded_files = st.file_uploader(
        "Upload your PYQ papers below. (Only .pdf is allowed)", accept_multiple_files=True
    )
def extract():
    
        extracted_text = []
        for file in uploaded_files:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    extracted_text.append(page.extract_text())
                   
        return extracted_text
buisness= extract()


if user_input:
    # Base Chain: Translate input to English
    translated_input, user_lang = translate_input_chain.invoke({"input_text": user_input}), 'en'
    
    # Select chain based on option
    if option == "General Query":
        response = query_chain.invoke({"query": translated_input})
    elif option == "Booking Management":
        service = st.text_input("Service Type (e.g., Haircut, Meeting, etc.):")
        action = st.text_input("Action (e.g., Book, Cancel, Reschedule):")
        if service and action:
            response = booking_chain.invoke({"action": action, "service": service})
        else:
            response = fallback_chain.invoke({"query": "Missing service or action details."})
    elif option == "Product Information":
        product = st.text_input("Product Name:")
        if product:
            response = product_info_chain.invoke({"product": product})
        else:
            response = fallback_chain.invoke({"query": "Missing product details."})
    elif option == "Customized Responses":
        business_type = st.text_input("Business Type (e.g., Restaurant, Salon, etc.):")
        if business_type:
            response = custom_chain.invoke({"business_type": business_type, "query": translated_input})
        else:
            response = fallback_chain.invoke({"query": "Missing business type."})
    
    # Base Chain: Translate output back to user language
    translated_response = translate_output_chain.invoke({"response_text": response, "target_language": user_lang})
    st.write("Response:", translated_response)

    # Contextual Suggestions
    if st.checkbox("Need more help? Get suggestions."):
        contextual_response = context_chain.invoke({"previous_interaction": translated_input})
        st.write("Suggestions:", contextual_response)

if st.button("Submit"):
     message = st.chat_message("assistant")
     bot_response = buisness_chain.invoke(buisness)
     st.write("RES:", bot_response)