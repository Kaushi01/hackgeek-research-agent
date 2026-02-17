from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Connect to Qdrant using your .env values
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# The 3 collections we need
COLLECTIONS = {
    "user_preferences": 384,
    "research_history": 384,
    "key_facts": 384
}

def create_collections():
    """Create all 3 collections if they don't exist"""
    existing = [c.name for c in client.get_collections().collections]
    
    for name, size in COLLECTIONS.items():
        if name not in existing:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE)
            )
            print(f"[CREATED] {name}")
        else:
            print(f"[EXISTS] {name}")

if __name__ == "__main__":
    create_collections()
    print("Qdrant is connected and ready!")