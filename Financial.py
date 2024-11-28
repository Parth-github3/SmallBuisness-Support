from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from googletrans import Translator  # Multilingual support
import matplotlib.pyplot as plt
import numpy as np

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

##################################### Financial Advisor Chains ###########################################
# Custom Financial Advice Chain
financial_chain = (
    ChatPromptTemplate.from_template("""
You are a financial advisor for small businesses. The business owner provided the following details:
Revenue: {revenue}
Expenses: {expenses}
Savings Goal: {savings_goal}
Investment Plan: {investment_plan}
Debt: {debt}

Provide a detailed financial recommendation with the following:
1. Ways to optimize expenses.
2. Strategies to achieve the savings goal.
3. Insights on the investment plan.
4. Debt reduction strategies.
5. Suggestions for reinvestment into the business.

Respond in a professional tone with actionable insights.
""")
    | llama
    | StrOutputParser()
)

##################################### Streamlit Financial Advisor Page ###########################################
st.title("Financial Advisor for Small Businesses")

# Form for user input
with st.form("financial_advisor_form"):
    st.header("Enter Business Financial Details:")
    revenue = st.number_input("Monthly Revenue ($)", min_value=0, step=100, value=10000)
    expenses = st.number_input("Monthly Expenses ($)", min_value=0, step=100, value=5000)
    savings_goal = st.number_input("Savings Goal ($)", min_value=0, step=100, value=2000)
    investment_plan = st.text_area(
        "Describe Your Investment Plan (e.g., expand operations, invest in marketing, etc.)", 
        placeholder="Briefly describe your investment plan"
    )
    debt = st.number_input("Outstanding Debt ($)", min_value=0, step=100, value=5000)

    # Submit button
    submit_financials = st.form_submit_button("Get Financial Advice")

if submit_financials:
    if revenue > 0 and expenses > 0:
        # Generate Financial Advice
        response = financial_chain.invoke({
            "revenue": revenue,
            "expenses": expenses,
            "savings_goal": savings_goal,
            "investment_plan": investment_plan,
            "debt": debt
        })

        # Display Financial Advice
        st.subheader("Customized Financial Recommendations:")
        st.write(response)

        # Financial Distribution Visualization
        st.subheader("Financial Distribution:")
        financial_data = {
            "Revenue": revenue,
            "Expenses": expenses,
            "Savings Goal": savings_goal,
            "Debt": debt,
            "Remaining Funds": max(revenue - expenses - savings_goal - debt, 0)
        }

        fig, ax = plt.subplots(figsize=(6, 6))
        labels = financial_data.keys()
        sizes = financial_data.values()
        explode = (0.1, 0, 0, 0, 0)  # Emphasize 'Revenue'
        colors = ['#2E91E5', '#E15F99', '#1CA71C', '#FB0D0D', '#FFC300']

        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

        st.pyplot(fig)

        # Break-Even Analysis
        st.subheader("Break-Even Analysis:")
        fixed_costs = st.number_input("Fixed Costs ($)", min_value=0, step=100, value=3000)
        variable_costs_per_unit = st.number_input("Variable Costs per Unit ($)", min_value=0.0, step=0.1, value=20.0)
        price_per_unit = st.number_input("Price per Unit ($)", min_value=0.0, step=0.1, value=50.0)

        if st.button("Calculate Break-Even Point"):
            if price_per_unit > variable_costs_per_unit:
                break_even_units = fixed_costs / (price_per_unit - variable_costs_per_unit)
                st.write(f"Break-Even Point: **{int(break_even_units)} units**")
            else:
                st.warning("Price per unit must be greater than variable costs per unit.")

    else:
        st.warning("Please enter valid financial details to proceed.")
