# rag_pipeline.py

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load documents from a file
loader = TextLoader("docs/sample.txt")  # Replace with your document path
documents = loader.load()

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Generate embeddings
embedding = HuggingFaceEmbeddings()

# Store vectors in ChromaDB
vectorstore = Chroma.from_documents(chunks, embedding=embedding)
retriever = vectorstore.as_retriever()

# Initialize language model
llm = OpenAI()  # Ensure OPENAI_API_KEY is set in your environment

# Create RAG QA chain
qa_chain = RetrievalQA(llm=llm, retriever=retriever)

# Function to handle user queries
def get_response(query: str) -> str:
    response = qa_chain.run(query)
    return response
