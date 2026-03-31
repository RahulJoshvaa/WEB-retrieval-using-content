import os
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions

# 1. Setup Embedding Function (Uses sentence-transformers locally)
# This replaces manual encoding in a loop for better performance
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 2. Initialize Persistent ChromaDB Client (Modern API)
# This saves data to the 'chroma_data' folder in your directory
chroma_client = chromadb.PersistentClient(path="./chroma_data")

# 3. Create or get collection
# We pass the embedding function here so it's automatic
collection = chroma_client.get_or_create_collection(
    name="pdf_files", 
    embedding_function=ef
)

# ------------------------------
# 4. Extract PDF text
# ------------------------------
def extract_pdf_text(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found.")
        return None
    
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    return full_text

# ------------------------------
# 5. Chunk text
# ------------------------------
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ------------------------------
# 6. Add PDF to ChromaDB
# ------------------------------
def add_pdf_to_chroma(pdf_path, description=""):
    file_name = os.path.basename(pdf_path)
    text = extract_pdf_text(pdf_path)
    
    if not text:
        return

    chunks = chunk_text(text)

    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({
            "file_name": file_name,
            "description": description
        })
        ids.append(f"{file_name}_chunk{i+1}")

    # Note: We no longer need to pass 'embeddings' manually!
    # The 'ef' we defined in Step 3 handles it automatically.
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"[+] Added {len(chunks)} chunks for {file_name}.")

# ------------------------------
# 7. Search function
# ------------------------------
def search_pdf(query, top_k=1):
    # Just pass the text string; Chroma encodes it using 'ef' automatically
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    output = []
    seen = set()
    # Results are returned in lists of lists
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        if meta['file_name'] not in seen:
            output.append({
                "file_name": meta['file_name'],
                "description": meta.get('description', ''),
                "snippet": doc
            })
            seen.add(meta['file_name'])
    return output

# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    # Ensure you have a file named 'example.pdf' in the same folder
    pdf_to_load1 = "example_1.pdf"
    pdf_to_load2 = "example_2.pdf"

    
    if os.path.exists(pdf_to_load1):
        add_pdf_to_chroma(pdf_to_load1, description="AI in healthcare report")
        add_pdf_to_chroma(pdf_to_load2, description="NASA")

        
        # Search
        query = "NASA"
        print(f"\nSearching for: '{query}'\n" + "="*50)
        
        search_results = search_pdf(query)
        for r in search_results:
            print(f"Source: {r['file_name']} ({r['description']})")
            print(f"Snippet: {r['snippet'][:200]}...") # Print first 200 chars
            print("-" * 50)
    else:
        print(f"Please place a file named '{pdf_to_load1}' in the directory to test.")