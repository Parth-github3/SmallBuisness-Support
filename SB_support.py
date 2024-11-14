#Requirements
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
#from googletrans import Translator  # Multilingual support

#LLM Model
llama = ChatGroq(
    model="LLaMA3-70B-8192",
    groq_api_key='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',
    temperature=0.0
)

#translator = Translator()  # Translator for multilingual support

##################################### Multilingual Chain ###########################################
def translate_input(user_input):
    """Auto-detect and translate the user input to English"""
    detected_lang = translator.detect(user_input).lang
    if detected_lang != 'en':
        user_input = translator.translate(user_input, src=detected_lang, dest='en').text
    return user_input, detected_lang

def translate_output(response, target_lang):
    """Translate response back to the user's language"""
    if target_lang != 'en':
        response = translator.translate(response, src='en', dest=target_lang).text
    return response

##################################### Query Handling ###########################################
query_chain = (
    ChatPromptTemplate.from_template("""
You are a customer support assistant. The user has the query: "{query}". 
Respond with a clear and concise answer. If you don't know the answer, ask for more details or suggest contacting support.
""")
    | llama
    | StrOutputParser()
)

##################################### Booking Management ###########################################
booking_chain = (
    ChatPromptTemplate.from_template("""
You are a virtual assistant that manages bookings for a business. The user wants to {action} for a service: "{service}". 
If they provide a time or date, confirm the booking; if not, ask for more details.
""")
    | llama
    | StrOutputParser()
)

##################################### Product Information ###########################################
product_info_chain = (
    ChatPromptTemplate.from_template("""
You are a knowledgeable sales assistant. The user is asking about: "{product}". 
Provide detailed information including features, pricing, and availability.
""")
    | llama
    | StrOutputParser()
)

##################################### Customization Chain ###########################################
custom_chain = (
    ChatPromptTemplate.from_template("""
You are assisting a small business that specializes in {business_type}. Tailor your response to reflect the company's services and brand tone.
The user query is: "{query}".
""")
    | llama
    | StrOutputParser()
)

##################################### Contextual Query Chain ###########################################
context_chain = (
    ChatPromptTemplate.from_template("""
You are a follow-up assistant. Based on the previous interaction: "{previous_interaction}", suggest a related query or provide further assistance.
""")
    | llama
    | StrOutputParser()
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

if user_input:
    # Translate input
    translated_input, user_lang = translate_input(user_input)
    
    # Select chain based on option
    if option == "General Query":
        response = query_chain.invoke({"query": translated_input})
    elif option == "Booking Management":
        service = st.text_input("Service Type (e.g., Haircut, Meeting, etc.):")
        action = st.text_input("Action (e.g., Book, Cancel, Reschedule):")
        if service and action:
            response = booking_chain.invoke({"action": action, "service": service})
        else:
            response = "Please provide both service and action details."
    elif option == "Product Information":
        product = st.text_input("Product Name:")
        if product:
            response = product_info_chain.invoke({"product": translated_input})
        else:
            response = "Please provide the product name."
    elif option == "Customized Responses":
        business_type = st.text_input("Business Type (e.g., Restaurant, Salon, etc.):")
        if business_type:
            response = custom_chain.invoke({"business_type": business_type, "query": translated_input})
        else:
            response = "Please specify the business type."
    
    # Translate output back to user language
    response = translate_output(response, user_lang)
    st.write("Response:", response)

    # Contextual Suggestions
    if st.checkbox("Need more help? Get suggestions."):
        contextual_response = context_chain.invoke({"previous_interaction": translated_input})
        st.write("Suggestions:", contextual_response)


