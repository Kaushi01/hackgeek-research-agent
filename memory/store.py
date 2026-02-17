from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct
from dotenv import load_dotenv
from datetime import datetime
import uuid
import os

from memory.qdrant_db import client

load_dotenv()

# Load the embedding model (converts text to vectors)
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(text: str):
    """Convert text into a vector (list of numbers)"""
    return model.encode(text).tolist()


def store_preference(user_id: str, preference: str):
    """
    Save a user preference
    Example: store_preference("user123", "I prefer code examples")
    """
    client.upsert(
        collection_name="user_preferences",
        points=[PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(preference),
            payload={
                "user_id": user_id,
                "preference": preference,
                "timestamp": datetime.now().isoformat()
            }
        )]
    )
    print(f"[STORED] Preference for {user_id}: {preference}")


def store_research(user_id: str, query: str, summary: str, mode: str):
    """
    Save a research session
    Example: store_research("user123", "what is RAG?", "RAG is...", "quick")
    """
    client.upsert(
        collection_name="research_history",
        points=[PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(query),
            payload={
                "user_id": user_id,
                "query": query,
                "summary": summary,
                "mode": mode,
                "timestamp": datetime.now().isoformat()
            }
        )]
    )
    print(f"[STORED] Research for {user_id}: {query}")


def store_fact(user_id: str, fact: str, topic: str):
    """
    Save a key fact extracted from research
    Example: store_fact("user123", "LoRA reduces params by 90%", "LoRA")
    """
    client.upsert(
        collection_name="key_facts",
        points=[PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(fact),
            payload={
                "user_id": user_id,
                "fact": fact,
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            }
        )]
    )
    print(f"[STORED] Fact for {user_id}: {fact}")