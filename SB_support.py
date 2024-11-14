#Requirements
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from translatepy import Translator  # Multilingual support

#LLM Model
llama = ChatGroq(
    model="LLaMA3-70B-8192",
    groq_api_key='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',
    temperature=0.0
)

# Translator instance
translator = Translator()

##################################### Translation Functions ###########################################
def translate_input(user_input):
    """Auto-detect and translate the user input to English."""
    try:
        detected_lang = translator.detect_language(user_input).result
        if detected_lang != "English":
            user_input = translator.translate(user_input, destination_language="English").result
        return user_input, detected_lang
    except Exception as e:
        st.error(f"Error in language detection or translation: {e}")
        return user_input, "English"  # Default to English if detection fails

def translate_output(response, target_lang):
    """Translate response back to the user's language."""
    try:
        if target_lang != "English":
            response = translator.translate(response, destination_language=target_lang).result
        return response
    except Exception as e:
        st.error(f"Error in translating response: {e}")
        return response  # Return the original response if translation fails

##################################### Chat Chains ###########################################
# General Query Chain
query_chain = (
    ChatPromptTemplate.from_template("""
You are a customer support assistant. The user has the query: "{query}". 
Respond with a clear and concise answer. If you don't know the answer, ask for more details or suggest contacting support.
""")
    | llama
    | StrOutputParser()
)

# Booking Management Chain
booking_chain = (
    ChatPromptTemplate.from_template("""
You are a virtual assistant that manages bookings for a business. The user wants to {action} for a service: "{service}". 
If they provide a time or date, confirm the booking; if not, ask for more details.
""")
    | llama
    | StrOutputParser()
)

# Product Information Chain
product_info_chain = (
    ChatPromptTemplate.from_template("""
You are a knowledgeable sales assistant. The user is asking about: "{product}". 
Provide detailed information including features, pricing, and availability.
""")
    | llama
    | StrOutputParser()
)

# Customized Response Chain
custom_chain = (
    ChatPromptTemplate.from_template("""
You are assisting a small business that specializes in {business_type}. Tailor your response to reflect the company's services and brand tone.
The user query is: "{query}".
""")
    | llama
    | StrOutputParser()
)

# Contextual Query Chain
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

# Sidebar module selection
option = st.selectbox(
    "Choose a support module:",
    ("General Query", "Booking Management", "Product Information", "Customized Responses"),
    index=0
)

# User input
user_input = st.text_input("Ask your question here:")

if user_input:
    # Translate input
    translated_input, user_lang = translate_input(user_input)

    # Select the appropriate chain
    response = ""
    if option == "General Query":
        response = query_chain.invoke({"query": translated_input})
    elif option == "Booking Management":
        service = st.text_input("Service Type (e.g., Haircut, Meeting, etc.):")
        action = st.text_input("Action (e.g., Book, Cancel, Reschedule):")
        if service and action:
            response = booking_chain.invoke({"action": action, "service": service})
        else:
            st.warning("Please provide both service and action details.")
    elif option == "Product Information":
        product = st.text_input("Product Name:")
        if product:
            response = product_info_chain.invoke({"product": product})
        else:
            st.warning("Please provide the product name.")
    elif option == "Customized Responses":
        business_type = st.text_input("Business Type (e.g., Restaurant, Salon, etc.):")
        if business_type:
            response = custom_chain.invoke({"business_type": business_type, "query": translated_input})
        else:
            st.warning("Please specify the business type.")

    # Translate output back to the user's language
    if response:
        translated_response = translate_output(response, user_lang)
        st.write("Response:", translated_response)

    # Contextual suggestions
    if st.checkbox("Need more help? Get suggestions."):
        contextual_response = context_chain.invoke({"previous_interaction": translated_input})
        st.write("Suggestions:", contextual_response)


