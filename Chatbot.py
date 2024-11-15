#Requirements
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from googletrans import Translator  # Multilingual support
from langchain_core.messages import SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

#LLM Model
llama = ChatGroq(
    model="LLaMA3-70B-8192",
    groq_api_key='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',
    temperature=0.0
)

translator = Translator()  # Translator for multilingual support
##################################### Base Chains ###########################################

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""You are an ai chatbot fine tuned for buisness and sales.
You are made for assistance for Small buisnesses to grow them. The customer will chat {userinput} with you and you will service them.
Here is the following services you will provide:
                                     resolve the customer queries; 
                                     provide product information; 
                                     book, cancel, or re-schedule any product or service; 
                                     provide customized solutions for queries; 
                                     Help customer to choose the best product or service according to their needs or requirements.
"""
        ),  # The persistent system prompt
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # Where the memory will be stored.
        HumanMessagePromptTemplate.from_template(
            "{userinput}"
        ),  # Where the human input will injected
    ]
)
prompt = ChatPromptTemplate.format_prompt(prompt)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
Chat_chain= LLMChain(
    llm=llama,
    prompt=prompt,
    verbose=True,
    memory=memory,
)
# 1. Chat chain
# Chat_chain = (
    
# #     ChatPromptTemplate.from_template("""
# # You are an ai chatbot fine tuned for buisness and sales.
# # You are made for assistance for Small buisnesses to grow them. The customer will chat {userinput} with you and you will service them.
# # Here is the following services you will provide:
# #                                      resolve the customer queries; 
# #                                      provide product information; 
# #                                      book, cancel, or re-schedule any product or service; 
# #                                      provide customized solutions for queries; 
# #                                      Help customer to choose the best product or service according to their needs or requirements.
# # """)
#     | llama
#     | StrOutputParser()
# )


# 1. Input Translation Chain
def translate_input(userinput):
    """Auto-detect and translate the user input to English."""
    try:
        detected_lang = translator.detect_language(userinput).result
        if detected_lang != "English":
            userinput = translator.translate(userinput, destination_language="English").result
        return userinput, detected_lang
    except Exception as e:
        #st.error(f"Error in language detection or translation: {e}")
        return userinput, "English"  # Default to English if detection fails

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


if "messages" not in st.session_state:
    st.session_state.messages = []

# getting User input
userinput = st.chat_input("How can I help you?")
with st.chat_message("user"):
        st.write(userinput)


if userinput:
    message = st.chat_message("assistant")
    #message.write(cbt_chain.invoke(user_input))
    # Base Chain: Translate input to English
    translated_input, user_lang = translate_input(userinput)
    st.session_state.messages.append({"role": "user", "content": userinput})
    response = Chat_chain.invoke(userinput)
    # Base Chain: Translate output back to user language
    if response:
        translated_response = translate_output(response, user_lang)
        st.write("Response:", translated_response)     
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    
    
# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    else:
        st.write(f"Bot: {message['content']}")