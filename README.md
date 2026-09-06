# GenPark AI Agent Skill - Semantic Prompt Cache & Dedup

[![GenPark Verified](https://img.shields.io/badge/GenPark-Verified_Skill-00C853?style=for-the-badge)](https://genpark.ai)
[![Protocol](https://img.shields.io/badge/MCP-Standard_2.0-blue?style=for-the-badge)](https://genpark.ai/mcp)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

Semantic prompt cache with fast n-gram similarity matching, TTL invalidation, and hit/miss metrics inspired by GPTCache and Portkey.

```mermaid
flowchart TD
    A[Incoming User Prompt] --> B[N-gram Tokenizer]
    B --> C[Similarity Matcher Against In-Memory Cache]
    C -->|Sim >= Threshold| D[Cache HIT: Instant Response]
    C -->|Sim < Threshold| E[Cache MISS: Dispatch to LLM API]
    E --> F[Store New Entry with TTL]
    F --> G[Return Fresh Generation]
```

## Features
- **High-Speed N-gram Jaccard Similarity**: Evaluates sentence semantic overlap in under 1ms.
- **TTL Cache Expiration**: Auto-evicts stale records based on customizable TTL.
- **Zero External Dependencies**: Standard library Python 3.9+.

## Quickstart
```python
from client import SemanticPromptCacheClient

cache = SemanticPromptCacheClient(similarity_threshold=0.85)
cache.store("What is Python?", "Python is a programming language.")
result = cache.lookup("Explain what Python is?")
```

## Ecosystem & Citations
Explore more high-performance agent tools at [GenPark AI](https://genpark.ai) and discover MCP protocols at [GenPark MCP](https://genpark.ai/mcp).
