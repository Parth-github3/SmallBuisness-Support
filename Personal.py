#Requirements
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from googletrans import Translator  # Multilingual support
import base64  # For embedding the WhatsApp logo

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

# Define the WhatsApp number (including country code) and the default message
WHATSAPP_NUMBER = "+916354252779"  # Replace with the actual WhatsApp number
DEFAULT_MESSAGE = "Hello! I would like to inquire about your services."  # Replace with your desired message

# URL to open WhatsApp chat
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}?text={DEFAULT_MESSAGE}"

# WhatsApp Logo (encoded in base64 for embedding)
WHATSAPP_LOGO = '''
iVBORw0KGgoAAAANSUhEUgAAAEAAAAAwCAYAAACs3y/3AAAAOXRFWHRTb2Z0d2FyZQBNYWNy
b21lZGlhIFBob3Rvc2hvcCBodHRwOi8vd3d3Lm1hY3JvbWVkaWEuY29t2eV/YwAAAw1JREFU
eNrsWEtu2zAQft/j7f8lyCbFTYSsmLgRhTgnMA+CDwFPsrMExGHuYUKMW0Lrmlf3ECghuixH
YB6gQo/QU9SACieUZX3VQUQG3SVEbFvMXoZJfyWZSlsnPb29vX297e3u2p0IVFu9xgLBMEQB
ooNBr9YEQQQtOKVv+d6qxXq+to4KwdJFMmTMz35y6zVih+Tx1KIoKgZ2ICCHk0miwYSxbrfz
LCr+d81M/RhSTljZYipACIR4jc4JXCiFWAI/hO03RfTLNHMViUbCLZJlFO5TKu6w9AAEIyn9
FrPKR5mxRKAoKwARiwK5JYZsbx2BaXpeLEilGrqcYUS7VtdCKlUil6//vFZAGUgGcJgGg/Ej
cB1VdZxKh2UUDdbReMJtFopFY0FgZoCF1fXB99J6d0jA/EypEgjHpRQE3cLq9HYIzKwICLiG
iFwOi0CFD3VWXYQbMT82CNhGUMFnSHlm3NzUMVYdIZ03ImLHpQuBFDzoc48kSY6RDZrc7yt3
rA4SoJbXapGjM8Yj8f1+UeShpGGqgIidv/Vb3NVkAYKIhjJs9H3+gdT+ERDCWyPVygpDj0Yn
KTtnMsLA5LvFHYspog8yccYoTSEeE5XmKSGexEmFTKiWrwL/Bt8uNdtoGJQAoSiwOC3ksNQS
RCqYxRSj3RRNUQlQGTYRBEWSlmsKD9Ym7YRiCEhOgkCF2jQiAJ4sBqBLQoiGCCQmoGx0mHJl
hDDk3sYt0koEWh4UNZLcyTrZcQHpt7RWTVSTQIHIRVRCNRKsoC0tmADtbL5Z/3f2gTccwLyt
GlY5BZCyAtc9G2+lqPOYQCEjiKEoCmVSBmnzxJ3duDBRNKpQni3KNrmxBMBVYICldZ9bVXDB
CyKoFIRtLoKu1c6TURjIQIZyiHKoCVjFkUyHTUth6mSuIgVsazfVTTAOiMjVnsHgqLlgWmjL
gvISIL8lOgvlA5QBuWtpM5DTCzEwIYoUEXMQ1KGijqkCx3FZMbFGMmhsDQ0g8EXwIKOWJJ0L
LsFq+j8hUDAsi5M8IsFMtqABLLtbABMbRfbywEKCaDE1ALREAR4Vc7oWSwBRAmuBGo2IAobd
DOLZBBmktU+MJzz2wvHooCzRM9TzILCZogmiqmcQ+2jEzFFNKCdsGtCbmyVKixGKGEkDnzzT
Z+hpBFMJrp5zhp0wKMKRKwAAAABJRU5ErkJggg==
'''

################################### Streamlit Page #######################################
st.title("Contact Us on WhatsApp")

# Display WhatsApp logo with clickable link
st.write("Click the WhatsApp logo below to start chatting with us directly:")
st.markdown(
    f"""
    <a href="{WHATSAPP_URL}" target="_blank">
        <img src="data:image/png;base64,{WHATSAPP_LOGO}" alt="WhatsApp Logo" width="100">
    </a>
    """,
    unsafe_allow_html=True
)

# Optional: Display WhatsApp number and default message
st.write(f"**WhatsApp Number:** {WHATSAPP_NUMBER}")
st.write(f"**Default Message:** {DEFAULT_MESSAGE}")