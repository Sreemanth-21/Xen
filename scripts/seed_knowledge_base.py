import os
import json
import sys

# Try importing chromadb to give a friendly error if not installed
try:
    import chromadb
except ImportError:
    print("Error: 'chromadb' package is not installed. Please install it or run 'pip install -r requirements.txt'.", file=sys.stderr)
    sys.exit(1)

def main():
    # Resolve paths relative to workspace root (parent of the scripts directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    
    docs_path = os.path.join(workspace_root, "data", "scenarios", "knowledge_base_docs.json")
    chroma_db_path = os.path.join(workspace_root, "chroma_store")
    
    # Verify that the JSON file exists
    if not os.path.exists(docs_path):
        print(f"Error: knowledge_base_docs.json not found at {docs_path}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Loading playbooks from: {docs_path}")
    with open(docs_path, "r", encoding="utf-8") as f:
        docs = json.load(f)
        
    print(f"Initializing Chroma PersistentClient pointing at: {chroma_db_path}")
    client = chromadb.PersistentClient(path=chroma_db_path)
    
    print("Getting or creating collection 'knowledge_base'...")
    collection = client.get_or_create_collection(name="knowledge_base")
    
    # Prepare batch arrays for upsert
    ids = []
    documents = []
    metadatas = []
    
    for doc in docs:
        ids.append(doc["doc_id"])
        documents.append(doc["text"])
        # Store category and timestamp as metadata
        metadatas.append({
            "category": doc["category"],
            "timestamp": doc["timestamp"]
        })
        
    print(f"Upserting {len(docs)} documents into Chroma...")
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    # Verify count and print confirmation
    count = collection.count()
    print(f"Confirmation: Successfully upserted playbooks. Total document count in 'knowledge_base': {count}")

if __name__ == "__main__":
    main()
