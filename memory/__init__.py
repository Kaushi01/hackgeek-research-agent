from memory.store import store_preference, store_research, store_fact
from memory.retrieve import retrieve

def store(user_id: str, query: str, result: dict):
    """Called by Person 1 after every agent response"""
    store_research(user_id, query, result.get("summary", ""), result.get("mode", "quick"))
    if result.get("preference"):
        store_preference(user_id, result["preference"])
    if result.get("fact"):
        store_fact(user_id, result["fact"], result.get("topic", "general"))

def clear(user_id: str):
    """Called by Person 4's forget button — coming soon"""
    pass