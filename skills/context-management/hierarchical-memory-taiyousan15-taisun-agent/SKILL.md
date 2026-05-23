---
name: hierarchical-memory
description: Hierarchical memory architecture combining short-term, long-term, and episodic memory layers. Based on Mem0 research showing 26% accuracy improvement. Use for persistent knowledge, context management, and RAG optimization.
---

# Hierarchical Memory System

TAISUN's hierarchical memory architecture based on Mem0 research, providing 26% accuracy improvement through structured memory layers.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    HIERARCHICAL MEMORY                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   SHORT-TERM    │  │    LONG-TERM    │  │    EPISODIC     │ │
│  │   (Session)     │  │   (Persistent)  │  │   (Events)      │ │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤ │
│  │ taisun-proxy    │  │ Qdrant Vector   │  │ claude-mem      │ │
│  │ InMemoryStore   │  │ Database        │  │ Observations    │ │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤ │
│  │ TTL: Session    │  │ TTL: Permanent  │  │ TTL: 30 days    │ │
│  │ Size: 100 items │  │ Size: Unlimited │  │ Size: 50/day    │ │
│  │ Search: Token   │  │ Search: Vector  │  │ Search: ID/Time │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                   │                    │            │
│           └───────────────────┼────────────────────┘            │
│                               ▼                                 │
│                    ┌─────────────────┐                         │
│                    │  MEMORY ROUTER  │                         │
│                    │  (Consolidation)│                         │
│                    └─────────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Memory Layers

### 1. Short-Term Memory (Working Memory)
**System**: taisun-proxy InMemoryStore
**Purpose**: Current session context

| Property | Value |
|----------|-------|
| Storage | In-memory |
| TTL | Session duration |
| Max Items | 100 |
| Search | Token-based |
| Use Cases | Current task context, recent commands, temp data |

```
# Store in short-term
memory_add type="short-term" content="現在のタスク: API実装"

# Retrieve
memory_search query="タスク"
```

### 2. Long-Term Memory (Semantic Memory)
**System**: Qdrant Vector Database
**Purpose**: Persistent knowledge and patterns

| Property | Value |
|----------|-------|
| Storage | Qdrant (localhost:6333) |
| TTL | Permanent |
| Max Items | Unlimited |
| Search | Vector similarity |
| Use Cases | Code patterns, learned solutions, domain knowledge |

```
# Store important pattern
qdrant-store text="認証にはJWTを使用し..." metadata={topic: "auth"}

# Semantic search
qdrant-find query="認証の実装方法"
```

### 3. Episodic Memory (Event Memory)
**System**: claude-mem Observations
**Purpose**: Decision history and context trails

| Property | Value |
|----------|-------|
| Storage | JSONL files |
| TTL | 30 days |
| Max Items | ~50/day |
| Search | ID, timestamp, type |
| Use Cases | Past decisions, debugging context, learning history |

```
# Auto-captured by hooks
# Access via MCP
mcp__claude-mem-search__search query="bugfix"
mcp__claude-mem-search__timeline date="2026-01-19"
```

## Memory Flow

### Information Lifecycle

```
1. CAPTURE (Short-Term)
   User input → Session context → Working memory

2. CONSOLIDATE (Short → Long)
   Important patterns → Vector embedding → Qdrant storage

3. OBSERVE (Episodic)
   Decisions, discoveries → claude-mem → Timestamped records

4. RETRIEVE (All Layers)
   Query → Router → Best matching layer → Response
```

### Consolidation Rules

| Trigger | Action |
|---------|--------|
| Session end | Important short-term → Long-term |
| Pattern detected | Auto-store in Qdrant |
| Decision made | Log to episodic |
| Error resolved | Store solution in long-term |

## Usage Patterns

### 1. Remember Important Information

```
User: このAPIパターンを覚えておいて
      [code snippet]

AI: 1. Short-term に即座に保存
    2. 重要度判定（コードパターン = HIGH）
    3. Qdrant に永続化
    4. claude-mem に観察記録
```

### 2. Retrieve Past Knowledge

```
User: 以前話した認証の実装方法は？

AI: 1. Qdrant でセマンティック検索
    2. claude-mem でエピソード検索
    3. 関連情報を統合
    4. コンテキスト付きで回答
```

### 3. Learn From Session

```
# Session end hook automatically:
1. Extracts key decisions
2. Stores successful patterns
3. Records errors and solutions
4. Updates long-term memory
```

## Performance Benefits (Mem0 Research)

| Metric | Improvement |
|--------|-------------|
| Accuracy | +26% |
| P95 Latency | -91% |
| Token Usage | -90% |

Source: [Mem0 Research Paper](https://arxiv.org/abs/2504.19413)

## Integration Points

### With Existing TAISUN Systems

| System | Integration |
|--------|-------------|
| taisun-proxy | memory_add, memory_search tools |
| Qdrant MCP | qdrant-store, qdrant-find tools |
| claude-mem | Auto-observation hooks |
| SessionStart | State injection |
| SessionEnd | Memory consolidation |

### With Other MCPs

```
# Context7 + Long-Term Memory
「use context7 でReact 19の新機能を学習して、覚えておいて」

# GPT Researcher + Memory
「市場調査して、重要なポイントを長期記憶に保存」
```

## Best Practices

1. **Explicit Memory Commands**
   ```
   ✅ 「これを長期記憶に保存して」
   ✅ 「前回のセッションで話した〇〇について」
   ❌ 「覚えておいて」（曖昧）
   ```

2. **Tag Important Information**
   ```
   metadata: { topic: "auth", type: "pattern", priority: "high" }
   ```

3. **Regular Memory Cleanup**
   ```
   Outdated patterns should be removed from long-term memory
   ```

4. **Trust the Consolidation**
   ```
   Let auto-hooks handle session → long-term migration
   ```

## Troubleshooting

### Memory Not Found
1. Check if Qdrant is running (`curl localhost:6333/health`)
2. Verify collection exists
3. Check search query specificity

### Slow Retrieval
1. Limit search scope with filters
2. Use appropriate memory layer
3. Check Qdrant index status

## Sources

- [Mem0 GitHub](https://github.com/mem0ai/mem0)
- [Mem0 Research (26% Accuracy Boost)](https://mem0.ai/research)
- [Mem0 arXiv Paper](https://arxiv.org/abs/2504.19413)
- [MCP-Mem0 Template](https://github.com/coleam00/mcp-mem0)
