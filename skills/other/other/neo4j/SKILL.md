---
name: neo4j
cluster: core-openclaw
description: "Neo4j graph database: schema management, CRUD, backup, Cypher queries via bolt protocol"
tags: ["neo4j", "graph-db", "cypher", "bolt"]
dependencies: ["cypher"]
composes: ["skill-graph"]
similar_to: []
called_by: []
manages: []
monitors: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "neo4j graph database node edge cypher query bolt driver community edition"
---

# Neo4j

## Purpose
Neo4j Community Edition graph database: schema management, CRUD operations, backup, Cypher queries via bolt protocol.

## When to Use
- When the task involves Neo4j graph database capabilities
- Match query: neo4j graph database node edge cypher query bolt driver

## Key Capabilities
- Neo4j Community Edition: schema management, CRUD, Cypher via bolt://localhost:7687
- Namespaced labels (OCAgent, OCMemory, OCTool) to avoid collisions with other graphs
- Python neo4j driver for programmatic access
- cypher-shell for CLI queries

## Graph Relationships
- DEPENDS_ON: ["cypher"]
- COMPOSES: ["skill-graph"]
- SIMILAR_TO: []
- CALLED_BY: []
