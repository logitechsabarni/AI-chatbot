# chromadb_manager.py

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Set embedding model (you can customize with specific models)
embedding = HuggingFaceEmbeddings()

# Use persistent local directory for Chroma DB
PERSIST_DIR = "db"

# Create or load Chroma vector store
def get_vectorstore():
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding)
