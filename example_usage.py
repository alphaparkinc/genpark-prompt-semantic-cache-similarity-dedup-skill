"""
Demonstration of genpark-prompt-semantic-cache-similarity-dedup-skill
"""

from client import SemanticPromptCacheClient

def main():
    cache = SemanticPromptCacheClient(similarity_threshold=0.80)

    # 1. Store baseline query
    p1 = "Explain the difference between TCP and UDP networking protocols"
    r1 = "TCP is connection-oriented and reliable, whereas UDP is connectionless and low-latency."
    cache.store(p1, r1, model="gpt-4o")
    print("Stored baseline prompt in semantic cache.")

    # 2. Query with near-identical wording
    p2 = "Explain the difference between UDP and TCP networking protocols"
    match = cache.lookup(p2, model="gpt-4o")

    print("\n=== CACHE LOOKUP RESULT ===")
    if match:
        print(f"CACHE HIT! Similarity: {match['similarity']}")
        print(f"Cached Response: {match['response']}")
    else:
        print("CACHE MISS")

    print("\nCache Metrics:", cache.get_metrics())

if __name__ == "__main__":
    main()
