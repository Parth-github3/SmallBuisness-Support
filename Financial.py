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

Provide detailed financial recommendations with the following:
1. Ways to optimize expenses.
2. Strategies to achieve the savings goal.
3. Insights on the investment plan, including feasibility and potential risks.
4. Debt reduction strategies tailored to the user's financial condition.
5. Suggestions for reinvestment into the business.

Respond in a professional tone with actionable insights.
""")
    | llama
    | StrOutputParser()
)

##################################### Streamlit Financial Advisor Page ###########################################

# Form for user input
with st.form("financial_advisor_form"):
    st.header("Enter Business Financial Details:")
    
    # Financial inputs
    revenue = st.number_input("Monthly Revenue ($)", min_value=0, step=1)
    expenses = st.number_input("Monthly Expenses ($)", min_value=0, step=1, value=5000)
    savings_goal = st.number_input("Savings Goal ($)", min_value=0, step=1, value=2000)
    
    # Debt information
    debt = st.number_input("Outstanding Debt ($)", min_value=0, step=1, value=5000)
    debt_interest = st.number_input(
        "Debt Interest Rate (%)", min_value=0.0, step=0.1, value=5.0,
        help="Enter the annual interest rate on your outstanding debt."
    )
    monthly_payment = st.number_input(
        "Monthly Debt Payment ($)", min_value=0, step=100, value=200,
        help="Enter the amount you pay monthly to service the debt."
    )
    
    # Investment plan section (before the button)
    st.subheader("Describe Your Investment Plan:")
    investment_plan = st.text_area(
        "Investment Plan (e.g., expand operations, invest in marketing, etc.)",
        placeholder="Briefly describe your investment plan"
    )

    # Submit button
    submit_financials = st.form_submit_button("Get Financial Advice")

    if submit_financials:
        if investment_plan and revenue > 0 and expenses > 0:
            # Generate Financial Advice
            response = financial_chain.invoke({
                "revenue": revenue,
                "expenses": expenses,
                "savings_goal": savings_goal,
                "investment_plan": investment_plan,
                "debt": f"{debt} at {debt_interest}% interest with ${monthly_payment}/month payment"
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
                "Debt Payment": monthly_payment * 12,
                "Remaining Funds": max(revenue - expenses - savings_goal - (monthly_payment * 12), 0)
            }

            fig, ax = plt.subplots(figsize=(6, 6))
            labels = financial_data.keys()
            sizes = financial_data.values()
            explode = (0.1, 0, 0, 0, 0)  # Emphasize 'Revenue'
            colors = ['#2E91E5', '#E15F99', '#1CA71C', '#FB0D0D', '#FFC300']

            ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
            ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

            st.pyplot(fig)

            # Debt Analysis
            st.subheader("Debt Analysis:")
            total_debt_payment = monthly_payment * 12
            remaining_debt = debt - total_debt_payment if debt > total_debt_payment else 0
            interest_paid = debt * (debt_interest / 100)

            st.write(f"Total Debt Paid This Year: **${total_debt_payment:,.2f}**")
            st.write(f"Remaining Debt After a Year: **${remaining_debt:,.2f}**")
            st.write(f"Estimated Interest Paid This Year: **${interest_paid:,.2f}**")

            if remaining_debt > 0:
                st.write(
                    "Consider increasing your monthly debt payments or restructuring the debt to reduce interest payments."
                )
            else:
                st.write("Congratulations! You are on track to clear your debt.")
        else:
            st.warning("Please enter a valid investment plan to proceed.")
