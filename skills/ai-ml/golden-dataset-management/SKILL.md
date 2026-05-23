---
name: golden-dataset-management
description: Use when backing up, restoring, or validating golden datasets. Prevents data loss and ensures test data integrity for AI/ML evaluation systems.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
author: SkillForge AI Agent Hub
tags: [golden-dataset, backup, data-protection, testing, regression, 2025]
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash  # For backup/restore scripts
user-invocable: false
---

# Golden Dataset Management

**Protect and maintain high-quality test datasets for AI/ML systems**

## Overview

A **golden dataset** is a curated collection of high-quality examples used for:
- **Regression testing:** Ensure new code doesn't break existing functionality
- **Retrieval evaluation:** Measure search quality (precision, recall, MRR)
- **Model benchmarking:** Compare different models/approaches
- **Reproducibility:** Consistent results across environments

**When to use this skill:**
- Building test datasets for RAG systems
- Implementing backup/restore for critical data
- Validating data integrity (URL contracts, embeddings)
- Migrating data between environments

---

## SkillForge's Golden Dataset

**Stats (Production):**
- **98 analyses** (completed content analyses)
- **415 chunks** (embedded text segments)
- **203 test queries** (with expected results)
- **91.6% pass rate** (retrieval quality metric)

**Purpose:**
- Test hybrid search (vector + BM25 + RRF)
- Validate metadata boosting strategies
- Detect regressions in retrieval quality
- Benchmark new embedding models

---

## Core Concepts

### Data Integrity Contracts

**The URL Contract:**
Golden dataset analyses MUST store **real canonical URLs**, not placeholders.

```python
# WRONG - Placeholder URL (breaks restore)
analysis.url = "https://skillforge.dev/placeholder/123"

# CORRECT - Real canonical URL (enables re-fetch if needed)
analysis.url = "https://docs.python.org/3/library/asyncio.html"
```

**Why this matters:**
- Enables re-fetching content if embeddings need regeneration
- Allows validation that source content hasn't changed
- Provides audit trail for data provenance

---

## Backup Strategy Comparison

| Strategy | Version Control | Restore Speed | Portability | Inspection |
|----------|-----------------|---------------|-------------|------------|
| **JSON** (recommended) | Yes | Slower (regen embeddings) | High | Easy |
| **SQL Dump** | No (binary) | Fast | DB-version dependent | Hard |

**SkillForge uses JSON backup** for version control and portability.

---

## Quick Reference

### Backup Format

```json
{
  "version": "1.0",
  "created_at": "2025-12-19T10:30:00Z",
  "metadata": {
    "total_analyses": 98,
    "total_chunks": 415,
    "total_artifacts": 98
  },
  "analyses": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "url": "https://docs.python.org/3/library/asyncio.html",
      "content_type": "documentation",
      "status": "completed",
      "created_at": "2025-11-15T08:20:00Z",
      "chunks": [
        {
          "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
          "content": "asyncio is a library...",
          "section_title": "Introduction to asyncio"
          // embedding NOT included (regenerated on restore)
        }
      ]
    }
  ]
}
```

**Key Design Decisions:**
- Embeddings excluded (regenerate on restore with current model)
- Nested structure (analyses -> chunks -> artifacts)
- Metadata for validation
- ISO timestamps for reproducibility

### CLI Commands

```bash
cd backend

# Backup golden dataset
poetry run python scripts/backup_golden_dataset.py backup

# Verify backup integrity
poetry run python scripts/backup_golden_dataset.py verify

# Restore from backup (WARNING: Deletes existing data)
poetry run python scripts/backup_golden_dataset.py restore --replace

# Restore without deleting (adds to existing)
poetry run python scripts/backup_golden_dataset.py restore
```

### Validation Checks

| Check | Error/Warning | Description |
|-------|---------------|-------------|
| Count mismatch | Error | Analysis/chunk count differs from metadata |
| Placeholder URLs | Error | URLs containing skillforge.dev or placeholder |
| Missing embeddings | Error | Chunks without embeddings after restore |
| Orphaned chunks | Warning | Chunks with no parent analysis |

---

## Best Practices Summary

1. **Version control backups** - Commit to git for history and diffs
2. **Validate before deployment** - Run verify before production changes
3. **Test restore in staging** - Never test restore in production first
4. **Document changes** - Track additions/removals in metadata

---

## Disaster Recovery Quick Guide

| Scenario | Steps |
|----------|-------|
| Accidental deletion | `restore --replace` -> `verify` -> run tests |
| Migration failure | `alembic downgrade -1` -> `restore --replace` -> fix migration |
| New environment | Clone repo -> setup DB -> `restore` -> run tests |

---

## References

For detailed implementation patterns, see:

- `references/storage-patterns.md` - Backup strategies, JSON format, backup script implementation, CI/CD automation
- `references/versioning.md` - Restore implementation, embedding regeneration, validation checklist, disaster recovery scenarios

---

## Related Skills

- `golden-dataset-validation` - Schema and integrity validation
- `golden-dataset-curation` - Quality criteria and curation workflows
- `pgvector-search` - Retrieval evaluation using golden dataset
- `ai-native-development` - Embedding generation for restore

---

**Version:** 1.0.0 (December 2025)
**Status:** Production-ready patterns from SkillForge's 98-analysis golden dataset

## Capability Details

### backup
**Keywords:** golden dataset, backup, export, json backup, version control data
**Solves:**
- How do I backup the golden dataset?
- Export analyses to JSON for version control
- Protect critical test datasets
- Create portable database snapshots

### restore
**Keywords:** restore dataset, import analyses, regenerate embeddings, disaster recovery, new environment
**Solves:**
- How do I restore from backup?
- Import golden dataset to new environment
- Regenerate embeddings after restore
- Disaster recovery procedures

### validation
**Keywords:** verify dataset, url contract, data integrity, validate backup, placeholder urls
**Solves:**
- How do I validate dataset integrity?
- Check URL contracts (no placeholders)
- Verify embeddings exist
- Detect orphaned chunks

### ci-cd-automation
**Keywords:** automated backup, github actions, ci cd backup, scheduled backup
**Solves:**
- How do I automate dataset backups?
- Set up GitHub Actions for weekly backups
- Commit backups to git automatically
- CI/CD integration patterns

### disaster-recovery
**Keywords:** disaster recovery, accidental deletion, migration failure, rollback
**Solves:**
- What if I accidentally delete the dataset?
- Database migration gone wrong
- Restore after data corruption
- Rollback procedures

### skillforge-golden-dataset
**Keywords:** skillforge, 98 analyses, 415 chunks, retrieval evaluation, real world
**Solves:**
- What is SkillForge's golden dataset?
- How does SkillForge protect test data?
- Real-world backup/restore examples
- Production golden dataset stats