import streamlit as st
import base64  # For embedding the WhatsApp logo

# Introduction Text
st.markdown("""
### Hello mate!\n
This app will make your buisness go with a boom!\n
        This app is a customizable AI-powered customer support chatbot. Features include:\n
            - Multilingual support
            - Booking management
            - Product information retrieval
            - Contextual query handling
            - Customizable responses for businesses
            - Financial Adivisor with Dept Analysis
""")

# Description
st.markdown("**Description about app's functions**")

with st.expander("About Query..."):
    st.markdown("""
    In **Query**, you can resolve any general queries or questions related to the buisness you have.\n
    """)

with st.expander("About Booking..."):
    st.markdown("""
In **Booking** page, you can book, cancel or reschedule any product or service you want directly.\n                          
""")
    
with st.expander("About Product Information..."):
    st.markdown("""
In **Product Information** page, you can get product information you want to search for.\n                                               
""")

with st.expander("About Customized Responses..."):
    st.markdown("""
In **Customized Responses** page, you can get all the detailed description of a product or service.\n                          
""")
    
with st.expander("About Chat Bot..."):
    st.markdown("""
In **Chat Bot** page, you can chat with our chatbot and access all the features mentioned above with chatting.\n
Like you can ask for a haircut, choose the right haircut offered by the salon, and book an appointment with it.\n                                               
""") 

with st.expander("About Financial Advisor..."):
    st.markdown("""
In **Financial Advisor** page, generates customized financial recommendations and visualizes financial distribution using graphs.\n
 The inputs include revenue, expenses, savings goals, and investment plans.\n                          
""")  

# Define the WhatsApp number (including country code) and the default message
WHATSAPP_NUMBER = "+916354252779"  # Replace with the actual WhatsApp number
DEFAULT_MESSAGE = "Hello! I would like to inquire about your services."  # Replace with your desired message

# URL to open WhatsApp chat
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}?text={DEFAULT_MESSAGE}"

################################### Streamlit Page #######################################
st.title("Contact Us")

# Try using the full file path to avoid issues
logo_path = "whatsapp_logo.png"  # Path to the logo file (use full path if needed)

try:
    st.markdown(
        f"""
        <a href="{WHATSAPP_URL}" target="_blank">
            <img src="{logo_path}" alt="WhatsApp Logo" width="100">
        </a>
        """,
        unsafe_allow_html=True
    )
except Exception as e:
    st.error("WhatsApp logo could not be loaded. Please ensure the image file exists.")
    st.write(f"Error: {e}")