---
name: golden-dataset-validation
description: Use when validating golden dataset quality. Runs schema checks, duplicate detection, and coverage analysis to ensure dataset integrity for AI evaluation.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge AI Agent Hub
tags: [golden-dataset, validation, integrity, schema, duplicate-detection, 2025]
allowed-tools:
  - Read
  - Grep
  - Glob
user-invocable: false
---

# Golden Dataset Validation

**Ensure data integrity, prevent duplicates, and maintain quality standards**

## Overview

This skill provides comprehensive validation patterns for the golden dataset, ensuring every entry meets quality standards before inclusion.

**When to use this skill:**
- Validating new documents before adding
- Running integrity checks on existing dataset
- Detecting duplicate or similar content
- Analyzing coverage gaps
- Pre-commit validation hooks

---

## Schema Validation

### Document Schema (v2.0)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "title", "source_url", "content_type", "sections"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "description": "Unique kebab-case identifier"
    },
    "title": {
      "type": "string",
      "minLength": 10,
      "maxLength": 200
    },
    "source_url": {
      "type": "string",
      "format": "uri",
      "description": "Canonical source URL (NOT placeholder)"
    },
    "content_type": {
      "type": "string",
      "enum": ["article", "tutorial", "research_paper", "documentation", "video_transcript", "code_repository"]
    },
    "bucket": {
      "type": "string",
      "enum": ["short", "long"]
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 2,
      "maxItems": 10
    },
    "sections": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "title", "content"],
        "properties": {
          "id": {"type": "string", "pattern": "^[a-z0-9-/]+$"},
          "title": {"type": "string"},
          "content": {"type": "string", "minLength": 50},
          "granularity": {"enum": ["coarse", "fine", "summary"]}
        }
      }
    }
  }
}
```

### Query Schema

```json
{
  "type": "object",
  "required": ["id", "query", "difficulty", "expected_chunks", "min_score"],
  "properties": {
    "id": {"type": "string", "pattern": "^q-[a-z0-9-]+$"},
    "query": {"type": "string", "minLength": 5, "maxLength": 500},
    "modes": {"type": "array", "items": {"enum": ["semantic", "keyword", "hybrid"]}},
    "category": {"enum": ["specific", "broad", "negative", "edge", "coarse-to-fine"]},
    "difficulty": {"enum": ["trivial", "easy", "medium", "hard", "adversarial"]},
    "expected_chunks": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "min_score": {"type": "number", "minimum": 0, "maximum": 1}
  }
}
```

---

## Validation Rules Summary

| Rule | Purpose | Severity |
|------|---------|----------|
| No Placeholder URLs | Ensure real canonical URLs | Error |
| Unique Identifiers | No duplicate doc/query/section IDs | Error |
| Referential Integrity | Query chunks reference valid sections | Error |
| Content Quality | Title/content length, tag count | Warning |
| Difficulty Distribution | Balanced query difficulty levels | Warning |

---

## Quick Reference

### Duplicate Detection Thresholds

| Similarity | Action |
|------------|--------|
| >= 0.90 | **Block** - Content too similar |
| >= 0.85 | **Warn** - High similarity detected |
| >= 0.80 | **Note** - Similar content exists |
| < 0.80 | **Allow** - Sufficiently unique |

### Coverage Requirements

| Metric | Minimum |
|--------|---------|
| Tutorials | >= 15% of documents |
| Research papers | >= 5% of documents |
| Domain coverage | >= 5 docs per expected domain |
| Hard queries | >= 10% of queries |
| Adversarial queries | >= 5% of queries |

### Difficulty Distribution Requirements

| Level | Minimum Count |
|-------|---------------|
| trivial | 3 |
| easy | 3 |
| medium | 5 |
| hard | 3 |

---

## References

For detailed implementation patterns, see:

- `references/validation-rules.md` - URL validation, ID uniqueness, referential integrity, content quality, and duplicate detection code
- `references/quality-metrics.md` - Coverage analysis, pre-addition validation workflow, full dataset validation, and CLI/hook integration

---

## Related Skills

- `golden-dataset-curation` - Quality criteria and workflows
- `golden-dataset-management` - Backup/restore operations
- `pgvector-search` - Embedding-based duplicate detection

---

**Version:** 1.0.0 (December 2025)
**Issue:** #599

## Capability Details

### schema-validation
**Keywords:** schema, validation, schema check, format validation
**Solves:**
- Validate entries against document schema
- Check required fields are present
- Verify data types and constraints

### duplicate-detection
**Keywords:** duplicate, detection, deduplication, similarity check
**Solves:**
- Detect duplicate or near-duplicate entries
- Use semantic similarity for fuzzy matching
- Prevent redundant entries in dataset

### referential-integrity
**Keywords:** referential, integrity, foreign key, relationship
**Solves:**
- Verify relationships between documents and queries
- Check source URL mappings are valid
- Ensure cross-references are consistent

### coverage-analysis
**Keywords:** coverage, analysis, distribution, completeness
**Solves:**
- Analyze dataset coverage across domains
- Identify gaps in difficulty distribution
- Report coverage metrics and recommendations