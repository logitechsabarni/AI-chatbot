# app.py

import streamlit as st
from backend.rag_pipeline import get_response
from backend.prompt_engineering import create_prompt
from backend.evaluate import log_response

st.set_page_config(page_title="🧠 AI Clone Chatbot", layout="centered")

st.title("🤖 Build Your Own AI Clone")
st.markdown("Ask anything and get intelligent answers using RAG + LLM!")

# User query input
query = st.text_input("💬 Enter your question:", placeholder="What is Retrieval-Augmented Generation?")

if st.button("Submit"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating response..."):
            # Prompt engineering
            final_prompt = create_prompt(query)
            # Get response from RAG pipeline
            response = get_response(final_prompt)
            # Log interaction for evaluation
            log_response(query, response)
        
        st.subheader("📢 Response:")
        st.success(response)

# Optional: Sidebar credits
st.sidebar.markdown("Made with 💜 using LangChain, OpenAI, ChromaDB, and Streamlit.")
