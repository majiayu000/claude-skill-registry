---
name: golden-dataset-curation
description: Use when creating or improving golden datasets for AI evaluation. Defines quality criteria, curation workflows, and multi-agent analysis patterns for test data.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge AI Agent Hub
tags: [golden-dataset, curation, quality, multi-agent, langfuse, 2025]
user-invocable: false
---

# Golden Dataset Curation

**Curate high-quality documents for the golden dataset with multi-agent validation**

## Overview

This skill provides patterns and workflows for **adding new documents** to the golden dataset with thorough quality analysis. It complements `golden-dataset-management` which handles backup/restore.

**When to use this skill:**
- Adding new documents to the golden dataset
- Classifying content types and difficulty levels
- Generating test queries for new documents
- Running multi-agent quality analysis

---

## Content Types

| Type | Description | Quality Focus |
|------|-------------|---------------|
| `article` | Technical articles, blog posts | Depth, accuracy, actionability |
| `tutorial` | Step-by-step guides | Completeness, clarity, code quality |
| `research_paper` | Academic papers, whitepapers | Rigor, citations, methodology |
| `documentation` | API docs, reference materials | Accuracy, completeness, examples |
| `video_transcript` | Transcribed video content | Structure, coherence, key points |
| `code_repository` | README, code analysis | Code quality, documentation |

---

## Difficulty Levels

| Level | Semantic Complexity | Expected Score | Characteristics |
|-------|---------------------|----------------|-----------------|
| **trivial** | Direct keyword match | >0.85 | Technical terms, exact phrases |
| **easy** | Common synonyms | >0.70 | Well-known concepts, slight variations |
| **medium** | Paraphrased intent | >0.55 | Conceptual queries, multi-topic |
| **hard** | Multi-hop reasoning | >0.40 | Cross-domain, comparative analysis |
| **adversarial** | Edge cases | Graceful degradation | Robustness tests, off-domain |

---

## Quality Dimensions

| Dimension | Weight | Perfect | Acceptable | Failing |
|-----------|--------|---------|------------|---------|
| **Accuracy** | 0.25 | 0.95-1.0 | 0.70-0.94 | <0.70 |
| **Coherence** | 0.20 | 0.90-1.0 | 0.60-0.89 | <0.60 |
| **Depth** | 0.25 | 0.90-1.0 | 0.55-0.89 | <0.55 |
| **Relevance** | 0.30 | 0.95-1.0 | 0.70-0.94 | <0.70 |

**Evaluation focuses:**
- **Accuracy:** Technical correctness, code validity, up-to-date info
- **Coherence:** Logical structure, clear flow, consistent terminology
- **Depth:** Comprehensive coverage, edge cases, appropriate detail
- **Relevance:** Alignment with AI/ML, backend, frontend, DevOps domains

---

## Multi-Agent Pipeline

```
INPUT: URL/Content
        |
        v
+------------------+
|   FETCH AGENT    |  Extract structure, detect type
+--------+---------+
         |
         v
+-----------------------------------------------+
|  PARALLEL ANALYSIS AGENTS                      |
|  Quality | Difficulty | Domain  | Query Gen   |
+-----------------------------------------------+
         |
         v
+------------------+
| CONSENSUS        |  Weighted score + confidence
| AGGREGATOR       |  -> include/review/exclude
+--------+---------+
         |
         v
+------------------+
|  USER APPROVAL   |  Show scores, confirm
+--------+---------+
         |
         v
OUTPUT: Curated document entry
```

### Decision Thresholds

| Quality Score | Confidence | Decision |
|---------------|------------|----------|
| >= 0.75 | >= 0.70 | **include** |
| >= 0.55 | any | **review** |
| < 0.55 | any | **exclude** |

---

## Quality Thresholds

```yaml
# Recommended thresholds for golden dataset inclusion
minimum_quality_score: 0.70
minimum_confidence: 0.65
required_tags: 2          # At least 2 domain tags
required_queries: 3       # At least 3 test queries
```

---

## Coverage Balance Guidelines

Maintain balanced coverage across:
- **Content types:** Don't over-index on articles
- **Difficulty levels:** Need trivial AND hard queries
- **Domains:** Spread across AI/ML, backend, frontend, etc.

### Duplicate Prevention Checklist

Before adding:
1. Check URL against existing `source_url_map.json`
2. Run semantic similarity against existing document embeddings
3. Warn if >80% similar to existing document

### Provenance Tracking

Always record:
- Source URL (canonical)
- Curation date
- Agent scores (for audit trail)
- Langfuse trace ID

---

## Langfuse Integration

### Trace Structure

```python
trace = langfuse.trace(
    name="golden-dataset-curation",
    metadata={"source_url": url, "document_id": doc_id}
)

# Log individual dimension scores
trace.score(name="accuracy", value=0.85)
trace.score(name="coherence", value=0.90)
trace.score(name="depth", value=0.78)
trace.score(name="relevance", value=0.92)

# Final aggregated score
trace.score(name="quality_total", value=0.87)
trace.event(name="curation_decision", metadata={"decision": "include"})
```

### Managed Prompts

| Prompt Name | Purpose |
|-------------|---------|
| `golden-content-classifier` | Classify content_type |
| `golden-difficulty-classifier` | Assign difficulty |
| `golden-domain-tagger` | Extract tags |
| `golden-query-generator` | Generate test queries |

---

## References

For detailed implementation patterns, see:

- `references/selection-criteria.md` - Content type classification, difficulty stratification, quality evaluation dimensions, and best practices
- `references/annotation-patterns.md` - Multi-agent pipeline architecture, agent specifications, consensus aggregation logic, and Langfuse integration

---

## Related Skills

- `golden-dataset-management` - Backup/restore operations
- `golden-dataset-validation` - Validation rules and checks
- `langfuse-observability` - Tracing patterns
- `pgvector-search` - Duplicate detection

---

**Version:** 1.0.0 (December 2025)
**Issue:** #599

## Capability Details

### content-classification
**Keywords:** content type, classification, document type, golden dataset
**Solves:**
- Classify document content types for golden dataset
- Categorize entries by domain and purpose
- Identify content requiring special handling

### difficulty-stratification
**Keywords:** difficulty, stratification, complexity level, challenge rating
**Solves:**
- Assign difficulty levels to golden dataset entries
- Ensure balanced difficulty distribution
- Identify edge cases and challenging examples

### quality-evaluation
**Keywords:** quality, evaluation, quality dimensions, quality criteria
**Solves:**
- Evaluate entry quality against defined criteria
- Score entries on multiple quality dimensions
- Identify entries needing improvement

### multi-agent-analysis
**Keywords:** multi-agent, parallel analysis, consensus, agent evaluation
**Solves:**
- Run parallel agent evaluations on entries
- Aggregate consensus from multiple analysts
- Resolve disagreements in classifications