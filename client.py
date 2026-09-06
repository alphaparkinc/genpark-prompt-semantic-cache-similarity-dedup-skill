"""
Semantic Prompt Cache with Character N-gram Jaccard Similarity and TTL.
Zero external dependencies, standard library only.
"""

import time
import math
from typing import Dict, List, Any, Optional, Tuple

class SemanticPromptCacheClient:
    """
    Semantic prompt cache using character/word n-gram similarity to avoid redundant
    LLM API calls. Tracks hit/miss ratios and supports time-to-live (TTL) invalidation.
    """

    def __init__(self, similarity_threshold: float = 0.82, default_ttl_seconds: int = 3600):
        self.threshold = similarity_threshold
        self.default_ttl = default_ttl_seconds
        self.cache = [] # List of dicts: {prompt, vector, response, model, expires_at}
        self.stats = {"hits": 0, "misses": 0, "stores": 0}

    def _extract_ngrams(self, text: str, n: int = 3) -> set:
        """Extracts character n-grams for fast zero-dependency similarity."""
        normalized = "".join(c.lower() for c in text if c.isalnum() or c.isspace()).strip()
        if len(normalized) < n:
            return {normalized}
        return {normalized[i : i + n] for i in range(len(normalized) - n + 1)}

    def compute_jaccard_similarity(self, s1: str, s2: str) -> float:
        """Computes Jaccard similarity across n-gram sets."""
        ng1 = self._extract_ngrams(s1)
        ng2 = self._extract_ngrams(s2)
        union = ng1.union(ng2)
        if not union:
            return 1.0 if s1 == s2 else 0.0
        return len(ng1.intersection(ng2)) / len(union)

    def lookup(self, prompt: str, model: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Searches cache for semantically similar previous prompt above threshold.
        Returns cached response or None.
        """
        now = time.time()
        best_match = None
        highest_sim = 0.0

        # Purge expired entries while searching
        valid_entries = []
        for entry in self.cache:
            if entry["expires_at"] < now:
                continue
            valid_entries.append(entry)

            if model and entry["model"] != model:
                continue

            sim = self.compute_jaccard_similarity(prompt, entry["prompt"])
            if sim >= self.threshold and sim > highest_sim:
                highest_sim = sim
                best_match = entry

        self.cache = valid_entries

        if best_match:
            self.stats["hits"] += 1
            return {
                "cache_hit": True,
                "similarity": round(highest_sim, 4),
                "matched_prompt": best_match["prompt"],
                "response": best_match["response"],
                "cached_model": best_match["model"]
            }
        else:
            self.stats["misses"] += 1
            return None

    def store(self, prompt: str, response: str, model: str = "default", ttl_seconds: Optional[int] = None):
        """Stores a new prompt-response pair in the semantic cache."""
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        entry = {
            "prompt": prompt,
            "response": response,
            "model": model,
            "created_at": time.time(),
            "expires_at": time.time() + ttl
        }
        self.cache.append(entry)
        self.stats["stores"] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Returns hit rate, miss rate, and active cache size."""
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = round((self.stats["hits"] / total) * 100.0, 2) if total > 0 else 0.0
        return {
            "active_entries": len(self.cache),
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "hit_rate_pct": hit_rate,
            "total_requests": total
        }
