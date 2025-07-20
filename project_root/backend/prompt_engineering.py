# prompt_engineering.py

from langchain.prompts import PromptTemplate

# Creates a structured prompt for the chatbot
def create_prompt(user_input: str) -> str:
    prompt = PromptTemplate(
        input_variables=["query"],
        template="""
You are a helpful, intelligent AI assistant.

Answer the user's question below clearly, concisely, and helpfully.

Question: {query}

Answer:"""
    )
    return prompt.format(query=user_input)
