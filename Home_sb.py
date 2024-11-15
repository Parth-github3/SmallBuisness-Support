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
st.title("Contact Us")

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