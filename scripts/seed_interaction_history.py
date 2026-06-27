import os
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
    
    chroma_db_path = os.path.join(workspace_root, "chroma_store")
        
    print(f"Initializing Chroma PersistentClient pointing at: {chroma_db_path}")
    client = chromadb.PersistentClient(path=chroma_db_path)
    
    print("Getting or creating collection 'interaction_history'...")
    collection = client.get_or_create_collection(name="interaction_history")
    
    # Verify count and print confirmation
    count = collection.count()
    print(f"Confirmation: 'interaction_history' collection exists. Current document count: {count}")

if __name__ == "__main__":
    main()
