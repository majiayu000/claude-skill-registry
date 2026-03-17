---
name: ac-knowledge-graph
description: Manage knowledge graph for autonomous coding. Use when storing relationships, querying connected knowledge, building project understanding, or maintaining semantic memory.
---

# AC Knowledge Graph

Build and query knowledge graphs for project understanding.

## Purpose

Maintains a knowledge graph of project concepts, relationships, and learnings for intelligent decision-making.

## Quick Start

```python
from scripts.knowledge_graph import KnowledgeGraph

graph = KnowledgeGraph(project_dir)
await graph.add_entity("User", {"type": "model"})
await graph.add_relation("User", "has", "Profile")
related = await graph.query("User")
```

## API Reference

See `scripts/knowledge_graph.py` for full implementation.
