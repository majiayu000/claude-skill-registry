---
name: knowledge-base-cache
description: Create and manage a layered knowledge base with hot/cold/warm cache tiers. Provides component-based architecture with Working Memory layer, automatic caching, semantic retrieval, and intelligent context assembly. Reduces API costs and supports unlimited knowledge scale.
version: 1.0
---

# Knowledge Base Cache Skill

Create a structured knowledge repository with **layered architecture** (hot/cold/warm) and intelligent context management.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     应用层 (Application)                     │
│                    Agent 核心                               │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              工作记忆层 (Working Memory)                     │
│  • 上下文组装              • Token预算管理                   │
│  • 多源协调                • LRU缓存                         │
└─────────────┬───────────────────────────────────────────────┘
              │ 标准接口 KnowledgeSource
    ┌─────────┼─────────┐
    ▼         ▼         ▼ (预留)
┌───────┐ ┌───────┐ ┌───────┐
│  Hot  │ │  Cold │ │ Warm  │
│ Cache │ │Storage│ │Vector │
│ Layer │ │ Layer │ │ Layer │
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
Context   Repository  Vector DB
 Cache     Files     (Future)
```

### Three-Tier Architecture

| Tier | Technology | Use Case | Status |
|------|------------|----------|--------|
| **🔥 Hot** | Context Cache (API) | Full document retrieval, 90% cost savings | ✅ Available |
| **❄️ Cold** | Repository Files | Keyword search, browsing, discovery | ✅ Available |
| **🌡️ Warm** | Vector DB | Semantic search, precise Q&A | 🔮 Planned |

## What This Skill Does

1. **Layered Knowledge Storage**
   ```
   repository/
   ├── core/                    # Core components
   │   ├── __init__.py          # Standard interfaces
   │   └── working_memory.py    # Working Memory layer
   ├── adapters/                # Layer adapters
   │   ├── __init__.py
   │   ├── hot_cache_adapter.py
   │   ├── cold_storage_adapter.py
   │   └── warm_cache_adapter.py (reserved)
   ├── index.json               # Knowledge index
   ├── cache-state.json         # Cache status
   ├── skills/                  # Skill knowledge
   ├── docs/                    # Document knowledge
   └── scripts/
       ├── cache_manager.py     # Cache management
       └── cache_helper.py      # Helper utilities
   ```

2. **Working Memory Layer**
   - Unified interface for all knowledge sources
   - Automatic context assembly with token budgeting
   - LRU cache for repeated queries
   - Cross-tier result ranking

3. **Context Caching (Hot Layer)**
   - Full document caching via API
   - 90% cost reduction
   - 83% latency improvement

4. **File-Based Storage (Cold Layer)**
   - Keyword-based retrieval
   - Excerpt generation
   - No API costs

5. **Auto-Refresh**
   - Configures cron job for daily refresh
   - Keeps caches fresh without manual intervention

## Quick Start

### Step 1: Initialize Repository

```bash
# The repository structure is already created
# If not, run:
python scripts/init_knowledge_base.py
```

### Step 2: Add Knowledge

Add markdown files to appropriate directories:
- `repository/skills/` - Skill documentation
- `repository/docs/` - General documentation  
- `repository/projects/` - Project-specific knowledge

### Step 3: Build Cache

```bash
cd repository

# Initialize index
python scripts/cache_manager.py init

# Build hot cache (Context Caching)
python scripts/cache_manager.py build

# Test the system
python test_phase1.py
```

### Step 4: Use in Your Agent

**Modern Approach (Recommended):**
```python
from repository.core.working_memory import WorkingMemoryManager

# Initialize once
wm = WorkingMemoryManager({
    'max_tokens': 6000,
    'allocation': {
        'system_prompt': 0.15,      # 15%
        'conversation': 0.25,        # 25%
        'retrieved_knowledge': 0.60  # 60%
    }
})

# Use in conversations
context = wm.query(
    user_query="How do I deploy?",
    system_prompt="You are an assistant...",
    conversation=history_messages
)
```

**Legacy Approach:**
```python
from scripts.cache_helper import get_cache_headers, load_knowledge_context

# Get cache headers for API calls
headers = get_cache_headers()

# Load knowledge context
context = load_knowledge_context()
```

### Step 5: Configure Auto-Refresh

```bash
# Add cron job for daily refresh
# Configure in your agent's cron system
```

## Layer Details

### 🔥 Hot Cache Layer

**Purpose**: Store frequently accessed complete documents

**When to Use**:
- Reading full skill documentation
- API reference lookup
- Deployment guides

**Implementation**: `adapters/hot_cache_adapter.py`

```python
from adapters.hot_cache_adapter import HotCacheAdapter
from core import RetrievalQuery

hot = HotCacheAdapter()
result = hot.retrieve(RetrievalQuery(
    query="Docker deployment",
    context_budget=2000,
    top_k=3
))
```

### ❄️ Cold Storage Layer

**Purpose**: Keyword-based file retrieval with excerpt generation

**When to Use**:
- Browsing knowledge base
- Finding relevant files
- Low-cost retrieval

**Implementation**: `adapters/cold_storage_adapter.py`

```python
from adapters.cold_storage_adapter import ColdStorageAdapter
from core import RetrievalQuery

cold = ColdStorageAdapter()
result = cold.retrieve(RetrievalQuery(
    query="Docker deployment",
    context_budget=2000,
    top_k=5
))
```

### 🌡️ Warm Cache Layer (Planned)

**Purpose**: Semantic search with vector embeddings

**When to Use**:
- Precise Q&A
- Semantic similarity matching
- Large knowledge bases

**Implementation**: Reserved interface in `adapters/warm_cache_adapter.py`

## Working Memory Configuration

### Token Budget Allocation

Default allocation (customizable):

| Component | Percentage | Tokens (6K total) |
|-----------|------------|-------------------|
| System Prompt | 15% | 900 |
| Conversation | 25% | 1,500 |
| Retrieved Knowledge | 60% | 3,600 |

### Configuration Options

```python
from repository.core.working_memory import WorkingMemoryManager
from repository.core import MemoryAllocation

wm = WorkingMemoryManager({
    'max_tokens': 8000,                    # Total context window
    'lru_cache_size': 10,                  # LRU cache size
    'allocation': {
        'system_prompt': 0.20,             # 20%
        'conversation': 0.20,              # 20%
        'retrieved_knowledge': 0.60        # 60%
    },
    'repo_path': 'repository'              # Repository path
})
```

## Cache Management Commands

| Command | Description |
|---------|-------------|
| `cache_manager.py init` | Scan repository and update index |
| `cache_manager.py build` | Create/update hot caches |
| `cache_manager.py status` | Show cache status |
| `cache_manager.py refresh` | Refresh expired caches |
| `cache_manager.py stats` | Show statistics |

### Testing Commands

```bash
# Run Phase 1 integration tests
cd repository
python test_phase1.py

# Test individual layers
python -c "from adapters.hot_cache_adapter import HotCacheAdapter; print(HotCacheAdapter().get_stats())"
python -c "from adapters.cold_storage_adapter import ColdStorageAdapter; print(ColdStorageAdapter().get_stats())"
```

## Cost Benefits

### Hot Layer (Context Cache)

| Metric | Without Cache | With Cache | Savings |
|--------|--------------|------------|---------|
| Cost per 1000 queries | ~¥150 | ~¥15 | **90%** |
| First token latency | ~30s | ~5s | **83%** |
| Monthly cost (daily 50 queries) | ~¥450 | ~¥45 | **¥405** |

### Cold Layer (File Storage)

| Metric | Value |
|--------|-------|
| API Cost | ¥0 (no API calls) |
| Latency | ~10-50ms (local files) |
| Best For | Browsing, discovery, keyword search |

### Working Memory Layer

| Metric | Value |
|--------|-------|
| Context Assembly | Automatic |
| Token Budget | Enforced |
| Multi-Source | Hot + Cold (+ Warm in future) |
| LRU Cache | Reduces repeated queries |

## Troubleshooting

### Cache Not Working

```bash
# Check if caches are active
python scripts/cache_manager.py status

# Rebuild if needed
python scripts/cache_manager.py build

# Verify hot layer
python -c "from adapters.hot_cache_adapter import HotCacheAdapter; print(HotCacheAdapter().is_available())"
```

### Working Memory Not Finding Knowledge

```python
# Debug: Check registered sources
from repository.core.working_memory import WorkingMemoryManager

wm = WorkingMemoryManager()
print(wm.get_stats())

# Debug: Test individual layers
from adapters.hot_cache_adapter import HotCacheAdapter
from adapters.cold_storage_adapter import ColdStorageAdapter
from core import RetrievalQuery

hot = HotCacheAdapter()
cold = ColdStorageAdapter()

query = RetrievalQuery(query="test", context_budget=2000)
print("Hot:", hot.retrieve(query))
print("Cold:", cold.retrieve(query))
```

### API Key Issues

Ensure API key is set in environment or config for hot layer.
Cold layer works without API keys.

### Path Issues

All paths in generated files are relative (workspace-relative) for portability.

## Migration from v1

If you were using the old cache system:

1. **Old way still works**: `cache_helper.py` functions unchanged
2. **New way recommended**: Use `WorkingMemoryManager` for better control
3. **Same repository structure**: No migration needed

## References

- Context Caching documentation
- Component architecture design
