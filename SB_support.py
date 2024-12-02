import streamlit as st

# Title
st.title("AI Customer Support Assistant")

pages = {
    "Home": [
        st.Page("Home_sb.py", title="Welcome!"),
    ],
    "General Query": [
        st.Page("Query.py", title="Query"),
    ],
    "Booking Management": [
        st.Page("Booking.py", title="Booking."),
    ],
    "Product Information": [
        st.Page("Product_info.py", title="Product Information"),
    ],
    "Customized Responses": [
        st.Page("Customization.py", title="Customized Responses"),
    ],
    "Chat Bot": [
        st.Page("Chatbot.py", title="Chat Bot"),
    ],
    "Financial Advisor": [
        st.Page("Financial.py", title="Financial Advisor"),
    ]
}

# Navigation page execution
pg = st.navigation(pages)
pg.run()