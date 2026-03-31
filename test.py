import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Initialize SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded!")

# Initialize ChromaDB

import chromadb
from chromadb.config import Settings

import chromadb

# This replaces the old Settings(persist_directory=...) approach
chroma_client = chromadb.PersistentClient(path="./chroma_db")
print("ChromaDB client initialized!")