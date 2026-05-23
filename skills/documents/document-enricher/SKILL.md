# document-enricher

**Version**: 1.9.0
**Status**: Active
**Owner**: SDLC Agêntico Core Team

## Purpose

Automatically enriches existing reference documents with research findings from any SDLC phase. When agents perform research, the system:
1. Detects documents related to the research topic
2. Extracts content from original documents
3. Merges original content with research findings
4. Creates versioned enriched documents
5. Updates corpus and knowledge graph

## When to Use

**Automatic activation** when:
- Any research agent (`domain-researcher`, `doc-crawler`, `requirements-analyst`, `adr-author`, `threat-modeler`) receives a prompt
- Similarity to existing documents > 0.6
- Documents exist in `.project/references/`

**Manual activation**:
```bash
/doc-search <keywords>              # Search for related documents
/doc-enrich <doc-id> <research>     # Manually enrich document
/doc-view <enrichment-id>           # View enriched version
/doc-diff <doc-id> <enrich-id>      # Compare versions
```

## Architecture

### Workflow

```
Agent Receives Prompt
        ↓
Step 0: find_related.py
   ├─ Extract keywords (TF-IDF)
   ├─ Query _index.yml
   ├─ Hybrid search (text + semantic)
   └─ Filter by similarity > 0.6
        ↓
   Documents Found?
   ├─ YES → Extract content (document-processor)
   └─ NO  → Continue normal research
        ↓
Execute Research (web, academic, community)
        ↓
enrich.py
   ├─ Merge: original + research
   ├─ Generate synthesis
   ├─ Create ENRICH-{id}.yml
   ├─ Generate .enriched.vN.md
   └─ Update metadata
        ↓
update_index.py
   ├─ Update _index.yml
   ├─ Update graph.json
   └─ Add 'enriches' relation
        ↓
Notify User
```

### Similarity Scoring

Hybrid score formula:
```
similarity = 0.40 * keyword_overlap
           + 0.30 * title_similarity
           + 0.20 * summary_similarity
           + 0.10 * category_match
```

Threshold: `0.6` (configurable via `ENRICHMENT_MIN_SIMILARITY` env var)

## Components

### Scripts

| Script | Purpose |
|--------|---------|
| `find_related.py` | Finds documents related to research topic |
| `enrich.py` | Merges original content with research findings |
| `render_markdown.py` | Generates enriched Markdown files |
| `update_index.py` | Updates _index.yml and graph.json |

### Templates

| Template | Purpose |
|----------|---------|
| `enrichment_node.yml.template` | Corpus node structure for enrichments |
| `enriched_markdown.md.template` | Markdown format for enriched documents |

### Tests

- `test_find_related.py` - Unit tests for document search
- `test_enrich.py` - Unit tests for enrichment logic
- `test_render_markdown.py` - Unit tests for Markdown generation
- `test_integration.py` - End-to-end enrichment flow

## Data Structures

### Enrichment Metadata (_index.yml)

```yaml
documents:
  - id: DOC-001
    path: "references/technical/oauth2-spec.pdf"
    title: "OAuth 2.0 Specification"
    keywords: ["oauth", "authentication"]

    enrichments:
      - enrichment_id: ENRICH-001
        enriched_at: "2026-01-22T14:30:00Z"
        research_topic: "OAuth 2.1 migration"
        agent: "domain-researcher"
        phase: 1
        corpus_node: "corpus/nodes/learnings/ENRICH-001.yml"
        enriched_file: "references/technical/oauth2-spec.enriched.v1.md"
        version: 1
        similarity: 0.85
```

### Enrichment Corpus Node

```yaml
id: ENRICH-001
type: enrichment
title: "OAuth 2.0 Specification - Enhanced with OAuth 2.1 migration"
created_at: "2026-01-22T14:30:00Z"
agent: "domain-researcher"

source_document:
  id: DOC-001
  path: "references/technical/oauth2-spec.pdf"

research_context:
  prompt: "Pesquise OAuth 2.1 migration best practices"
  phase: 1
  similarity: 0.85

content:
  original_summary: |
    Summary of original document content
  research_findings: |
    New research results from web, academic sources
  synthesis: |
    Combined analysis merging original + research
  sources:
    - url: "https://oauth.net/2.1/"
      title: "OAuth 2.1 Draft"
      accessed_at: "2026-01-22T14:30:00Z"

relations:
  - type: enriches
    target: DOC-001

decay_metadata:
  last_validated_at: "2026-01-22T14:30:00Z"
  decay_score: 1.0
  decay_status: fresh

tags: ["oauth", "authentication", "migration", "oauth2.1"]
```

### Enriched Markdown Structure

```markdown
# {Document Title} - Enhanced Research Edition

**Original Document**: `{path}`
**Enriched**: {date}
**Research Topic**: {topic}
**Agent**: {agent}
**Phase**: {phase}
**Version**: v{n}

---

## Original Content Summary

{extracted_summary}

---

## Research Findings

{research_data}

### Sources
- [{title}]({url}) - Accessed {date}

---

## Synthesis

{combined_analysis}

---

**🤖 Generated with SDLC Agêntico by @arbgjr**
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENRICHMENT_MIN_SIMILARITY` | 0.6 | Minimum similarity score for document matching |
| `ENRICHMENT_MAX_VERSIONS` | 10 | Max enrichment versions per document |
| `ENRICHMENT_AUTO_ARCHIVE` | true | Auto-archive old enrichments (> 1 year) |

## Integration with Agents

Modified agents include "Step 0" before research:

**Phase 1 (Discovery)**:
- `domain-researcher` - Research academic/web sources
- `doc-crawler` - Extract and index documentation

**Phase 2 (Requirements)**:
- `requirements-analyst` - Analyze requirements

**Phase 3 (Architecture)**:
- `adr-author` - Document architecture decisions
- `threat-modeler` - Model security threats

### Example Agent Modification

```markdown
# domain-researcher

## Your Task

### Step 0: Check for Related Documents (NEW)

Before starting research, check if existing documents relate to this topic:

1. Use `/doc-search` with extracted keywords from prompt
2. If similarity > 0.6:
   - Extract content from original document
   - Note key points to complement (not duplicate) in research
3. If no documents found:
   - Proceed with standard research

### Step 1: Execute Research

[... existing research steps ...]

### Final Step: Enrich Documents

If related documents were found in Step 0:
1. Use `/doc-enrich` to merge original + research findings
2. Verify enriched version was created
3. Notify user with enrichment details
```

## Quality Gates

### enrichment-quality.yml

```yaml
gate_id: enrichment-quality
name: "Enrichment Quality Gate"
applies_to:
  - phase: [1, 2, 3]
    condition: "enrichments_created > 0"

checks:
  - name: enrichment_has_sources
    severity: critical
    description: "Research findings must cite sources"

  - name: original_preserved
    severity: critical
    description: "Original document unchanged (SHA256 hash check)"

  - name: graph_relation_created
    severity: critical
    description: "Graph contains 'enriches' relation"

  - name: enrichment_version_incremented
    severity: warning
    description: "Version incremented correctly (v1 → v2 → ...)"

  - name: synthesis_quality
    severity: warning
    description: "Synthesis combines original + research coherently"
```

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Document Discovery Rate | > 70% | % of prompts that find related docs |
| Enrichment Quality | > 80% | % passing quality gate |
| Processing Time | < 30s | Time from research → enrichment |
| Graph Integrity | 100% | % of enrichments with valid relation |

## Dependencies

- **document-processor** (v1.3.0+) - Document extraction
- **rag-query** (v1.4.0+) - Hybrid search
- **graph-navigator** (v1.4.0+) - Graph management
- **decay-scoring** (v1.5.0+) - Freshness tracking

## Error Handling

| Error | Mitigation |
|-------|-----------|
| Document extraction fails | Log warning, continue with research only |
| Similarity computation timeout | Use cached results or skip enrichment |
| Graph update fails | Retry 3x, then create orphan enrichment |
| Markdown generation fails | Save raw YAML node, skip Markdown |

## Rollback Strategy

If enrichment causes issues:
```bash
# Revert to original document state
python3 .claude/skills/document-enricher/scripts/rollback.py --enrichment-id ENRICH-001

# Removes:
# - .enriched.vN.md file
# - ENRICH-{id}.yml corpus node
# - Graph relation
# - _index.yml entry
```

## Future Enhancements

- **v2.0**: Embeddings-based semantic search
- **v2.1**: Multi-document synthesis (combine 2+ docs)
- **v2.2**: Automatic re-enrichment on document updates
- **v2.3**: LLM-powered synthesis generation

---

**Related ADRs**:
- ADR-document-enrichment-architecture.yml (v1.9.0)

**Related Learnings**:
- LEARN-research-agent-patterns.yml
