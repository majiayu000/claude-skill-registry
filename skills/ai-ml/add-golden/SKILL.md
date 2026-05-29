---
name: add-golden
description: Curate and add documents to the golden dataset with multi-agent validation. Use when adding test data, creating golden datasets, saving examples.
context: fork
version: 1.0.0
author: SkillForge
tags: [curation, golden-dataset, evaluation, testing]
user-invocable: true
---

# Add to Golden Dataset

Multi-agent curation workflow for adding high-quality documents.

## Quick Start

```bash
/add-golden https://example.com/article
/add-golden https://arxiv.org/abs/2312.xxxxx
```

## Phase 1: Input Collection

Get URL and detect content type:
- article (blog post, tech article)
- tutorial (step-by-step guide)
- documentation (API docs, reference)
- research_paper (academic, whitepaper)

## Phase 2: Fetch and Extract

Extract document structure:
- Title and sections
- Code blocks
- Key technical terms
- Metadata (author, date)

## Phase 3: Parallel Analysis (4 Agents)

| Agent | Task |
|-------|------|
| code-quality-reviewer | Quality evaluation |
| Explore #1 | Difficulty classification |
| Explore #2 | Domain tagging |
| Explore #3 | Test query generation |

### Quality Dimensions

| Dimension | Weight |
|-----------|--------|
| Accuracy | 0.25 |
| Coherence | 0.20 |
| Depth | 0.25 |
| Relevance | 0.30 |

### Difficulty Levels

- trivial: Direct keyword match (>0.85 score)
- easy: Common synonyms (>0.70 score)
- medium: Paraphrased intent (>0.55 score)
- hard: Multi-hop reasoning (>0.40 score)
- adversarial: Edge cases, robustness

## Phase 4: Validation Checks

- URL validation (no placeholders)
- Schema validation (required fields)
- Duplicate check (>80% similarity)
- Quality gates (min sections, content length)

## Phase 5: Decision Thresholds

| Score | Decision |
|-------|----------|
| >= 0.75 | INCLUDE |
| >= 0.55 | REVIEW |
| < 0.55 | EXCLUDE |

## Phase 6: User Approval

Present results for user decision:
- Approve: Add with generated queries
- Modify: Edit details before adding
- Reject: Do not add

## Phase 7: Write to Dataset

Update fixture files:
- `documents_expanded.json`
- `source_url_map.json`
- `queries.json`

Validate fixture consistency after writing.

## Summary

**Total Parallel Agents: 4**
- 1 code-quality-reviewer
- 3 Explore agents

**Quality Gates:**
- Minimum score: 0.55 for review
- No placeholder URLs
- No duplicates (>90% similar)
- At least 2 tags, 2 sections

## Related Skills

- `golden-dataset-validation` - Validate existing golden datasets for quality and coverage
- `llm-evaluation` - LLM output evaluation patterns used in quality scoring
- `test-data-management` - General test data strategies and fixture management

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Quality Threshold | >= 0.55 for review | Balances precision with recall for dataset curation |
| Duplicate Detection | 80% similarity | Prevents near-duplicates while allowing related content |
| Parallel Agents | 4 concurrent | Optimal parallelism for quality/difficulty/tagging analysis |
| Weighting | Relevance highest (0.30) | Retrieval relevance most critical for RAG evaluation |

## References

- [Quality Scoring](references/quality-scoring.md)