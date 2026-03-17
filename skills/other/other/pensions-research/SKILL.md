---
name: pensions-research
description: Research UK pensions regulations, LGPS rules, TPR guidance, and trustee obligations using Neo4j knowledge graphs and RAG
allowed-tools: Read, Grep, mcp__neo4j-apex__*, mcp__neo4j-psps__*, mcp__neo4j-cms-handbook__*, mcp__neo4j-scheme-docs__*
context: fork
agent: general-purpose
model: claude-opus-4-5-20251101
---

# pensions-research

<!-- AUTO-GENERATED from ~/.45black/skills/pensions-research.skill.yaml -->
<!-- DO NOT EDIT - run: ~/.45black/scripts/transpile-skills.sh -->

## Description

Research UK pensions regulations, LGPS rules, TPR guidance, and trustee obligations using Neo4j knowledge graphs and RAG

## Triggers

**Keywords:** pensions research, LGPS, Local Government Pension Scheme, TPR, The Pensions Regulator, trustee, trustee duties, pension law, UK retirement benefits, CMS Handbook, scheme rules, pension regulations

## Workflow

### understand_query
Identify the regulation area

### search_knowledge_bases
Query relevant Neo4j databases

### cross_reference
Validate findings across multiple sources

### cite_sources
Provide proper citations

### verify_claims
Use hallucination detector for statutory claims

## Model Preference

**opus** - Complex regulatory reasoning, high-stakes legal domain

---
*Generated from universal skill format v1.0.0 on 2026-01-17*
