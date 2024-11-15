#Requirements
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from googletrans import Translator  # Multilingual support
import matplotlib.pyplot as plt  # For visualization
import random  # For generating dummy demand data

# LLM Model
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
        return user_input, "English"  # Default to English if detection fails

# 2. Output Translation Chain
def translate_output(response, target_lang):
    """Translate response back to the user's language."""
    try:
        if target_lang != "English":
            response = translator.translate(response, destination_language=target_lang).result
        return response
    except Exception as e:
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
# 4. General Query Chain
# 6. Product Information Chain
product_info_chain = (
    ChatPromptTemplate.from_template("""
You are a knowledgeable sales assistant. The user is asking about: "{product}". 
Provide detailed information including features, pricing, and availability.
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

##################################### Upselling Chain ###########################################
# 9. Upselling Chain
upselling_chain = (
    ChatPromptTemplate.from_template("""
You are an AI sales assistant. The user is interested in "{product}". 
Suggest related or higher-tier products/services and their potential benefits.
""")
    | llama
    | StrOutputParser()
)

##################################### Streamlit Application ###########################################
product = st.text_input("Product Name:")
if product:
    # Base Chain: Translate input to English
    translated_input, user_lang = translate_input(product)

    # Product Info Chain
    if product:
        response = product_info_chain.invoke({"product": product})
    else:
        response = fallback_chain.invoke({"query": "Missing product details."})
    
    # Base Chain: Translate output back to user language
    if response:
        translated_response = translate_output(response, user_lang)
        st.write("Response:", translated_response)

    # Contextual Suggestions
    if st.checkbox("Need more help? Get suggestions."):
        contextual_response = context_chain.invoke({"previous_interaction": translated_input})
        st.write("Suggestions:", contextual_response)

    # Upselling Recommendations
    st.subheader("Upselling Recommendations")
    upselling_response = upselling_chain.invoke({"product": product})
    st.write("Upselling Suggestions:", upselling_response)

    # Visualize Upselling Suggestions
    upsell_products = [f"{product} Pro", f"{product} Premium", f"{product} Bundle"]
    upsell_demand = [random.randint(20, 100) for _ in upsell_products]

    st.write("**Demand for Upselling Options:**")
    fig, ax = plt.subplots()
    ax.bar(upsell_products, upsell_demand, color="lightblue")
    ax.set_title("Upselling Demand Visualization")
    ax.set_xlabel("Products")
    ax.set_ylabel("Demand Score")
    st.pyplot(fig)
