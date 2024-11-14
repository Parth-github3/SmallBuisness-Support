#Requirements
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from googletrans import Translator  # Multilingual support


#LLM Model
llama = ChatGroq(
    model="LLaMA3-70B-8192",
    groq_api_key='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',
    temperature=0.0
)

translator = Translator()  # Translator for multilingual support

##################################### Base Chains ###########################################
# 1. Input Translation Chain
def translate_input(user_input):
    """Auto-detect and translate the user input to English."""
    try:
        detected_lang = translator.detect_language(user_input).result
        if detected_lang != "English":
            user_input = translator.translate(user_input, destination_language="English").result
        return user_input, detected_lang
    except Exception as e:
        #st.error(f"Error in language detection or translation: {e}")
        return user_input, "English"  # Default to English if detection fails

# 2. Output Translation Chain
def translate_output(response, target_lang):
    """Translate response back to the user's language."""
    try:
        if target_lang != "English":
            response = translator.translate(response, destination_language=target_lang).result
        return response
    except Exception as e:
        #st.error(f"Error in translating response: {e}")
        return response  # Return the original response if translation fails

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
# 4. Customization Chain
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

user_input = st.text_input("Ask your question here:")

if user_input:
    # Base Chain: Translate input to English
    translated_input, user_lang = translate_input(user_input)
    business_type = st.text_input("Business Type (e.g., Restaurant, Salon, etc.):")
    if business_type:
        response = custom_chain.invoke({"business_type": business_type, "query": translated_input})
    else:
        response = fallback_chain.invoke({"query": "Missing business type."})
    # Base Chain: Translate output back to user language
    if response:
        translated_response = translate_output(response, user_lang)
        st.write("Response:", translated_response)

    # Contextual Suggestions
    if st.checkbox("Need more help? Get suggestions."):
        contextual_response = context_chain.invoke({"previous_interaction": translated_input})
        st.write("Suggestions:", contextual_response)