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
""")

# How to use section
# st.markdown("**How to use?**")

# with st.expander("Instructions to follow..."):
#     st.markdown("""
# Open the **Question** page -> Upload pyq papers (only in pdf format) -> Download the ***Question_response*** text file.\n 
# You can you this file for both Answer page and Concept-Learning Plan for getting responses.\n
#                 """)
    

# Description
st.markdown("**Description about app's functions**")

with st.expander("About Query..."):
    st.markdown("""
    **Question** is a place where you upload your Past Year Question papers and get your imp questions in seconds.\n
    Input: Question papers(one or more) **Format:** PDF\n
    Task: It will generate you a list of questions which are repeated and catagorize it on concept base.\n
    Output: List of imp questions. Also, you can download it as a file.
    """)

with st.expander("About Booking..."):
    st.markdown("""
In **Answer** page, you will get brief and informative answer for any questions provided. \n
Input: The ***Question_response*** text file from the **Question** page.\n
Task: Generation of answers with conceptual understanding.\n
Output: Answer text file to download.                          
""")
    
with st.expander("About Product Info..."):
    st.markdown("""
In **Concept-Learning Plan** page, you will get a guided study plan to kickstart your studying.\n
Input: The ***Question_response*** text file from the **Question** page.\n
Task: Generation of a Study plan according to your imp concepts covered in the exam with a flow chart to visualize it better.\n
Output: Plan text file to download.                                               
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