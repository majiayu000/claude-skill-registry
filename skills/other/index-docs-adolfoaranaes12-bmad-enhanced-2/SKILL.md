---
name: index-docs
description: Create searchable knowledge base from existing documentation and code for fast context lookup in brownfield projects. Indexes .md files with sections/keywords, maps code exports to documentation, generates search.json, quick-ref.md, and glossary.md in .claude/index/. Use when onboarding to brownfield projects or when documentation needs better discoverability.
version: 1.0
category: Brownfield
acceptance:
  documentation_indexed: "All documentation files (.md) indexed with sections, keywords, and cross-references extracted"
  code_indexed: "Code files indexed with exports, functions, and documentation links mapped"
  search_index_created: "Searchable index files created (search.json, quick-ref.md, glossary.md) in .claude/index/"
inputs:
  refresh:
    required: false
    description: "Refresh existing index (incremental) vs rebuild from scratch"
outputs:
  files_indexed:
    description: "Total number of files indexed (docs + code)"
  keywords_count:
    description: "Total unique keywords identified"
  references_count:
    description: "Total cross-references and links created"
  index_location:
    description: "Path to generated index files"
telemetry:
  emit: "skill.index-docs.completed"
  track:
    - files_indexed
    - docs_files_count
    - code_files_count
    - keywords_count
    - references_count
    - index_size_bytes
    - operation_type  # build | refresh
---

# Index Documentation and Code Skill

## Purpose

Create a searchable, structured knowledge base from existing documentation and codebase. This enables fast context lookup during task planning and implementation in brownfield projects through semantic search, documentation-to-code mapping, and quick reference systems.

**Core Principle:** In brownfield projects, context discovery is the bottleneck—indexing eliminates repeated searching.

## Prerequisites

- Existing documentation in `docs/` directory
- Structured, readable codebase
- Write access to `.claude/index/` location
- Optional: `document-project` skill completed first

---

## Workflow

### 1. Load Configuration and Validate

**Check prerequisites and configuration:**

```yaml
# .claude/config.yaml
brownfield:
  docsPath: docs/
  codebasePath: src/
  indexLocation: .claude/index/
  includeCode: true
  maxDepth: 3
```

**Validate:**
- Documentation directory exists with files
- Index location is writable
- Check if index exists (offer refresh vs rebuild)

---

### 2. Index Documentation

**Parse and structure documentation content:**

1. **Scan documentation files** (.md files in docs/)
2. **Extract structure:**
   - Headings and sections
   - Code blocks and examples
   - Keywords and concepts (API names, domain terms, technologies)
3. **Build document index** with sections, keywords, line numbers
4. **Create cross-references** between documents

**Output:** Documentation indexed (file count), sections extracted, keywords identified, cross-references created

**See:** `references/templates.md#step-2-output` for complete format and index structure

---

### 3. Index Codebase (Optional)

**Map code to documentation:**

1. **Scan key code files:**
   - Models, schemas, types
   - Routes, controllers, services
2. **Extract code elements:**
   - Exports, imports, functions
   - Map to line numbers
3. **Build code-to-docs mapping:**
   - Find code mentions in docs
   - Create bidirectional links

**Output:** Code files indexed, exports/functions mapped, code-to-docs links created

**See:** `references/templates.md#step-3-output` for complete format and code-mapping.md for strategies

---

### 4. Build Searchable Index

**Create fast lookup structures:**

1. **Create search index:**
   - Keyword → Documents
   - Concept → Sections
   - Code → Documentation
2. **Generate quick reference:**
   - Data models with file locations
   - API endpoints with docs links
   - Patterns and where documented
3. **Create glossary:**
   - Terms and definitions
   - Links to detailed documentation

**Output:** search.json (searchable index), quick-ref.md (quick reference), glossary.md (term definitions) created in .claude/index/

**See:** `references/templates.md#step-4-output` for complete file formats and examples

---

## Using the Index

**Quick searches:** grep for keywords in search.json | Look up endpoints in quick-ref.md | Find term definitions in glossary.md

**Integration:** create-task-spec loads relevant docs | implement-feature looks up patterns | document-project refreshes index

**See:** `references/templates.md#search-examples` for complete search commands and `#integration-examples` for workflows

---

## Index Maintenance

**When to refresh:** Documentation updated | New code modules | Architecture changes | Quarterly maintenance

**Refresh vs Rebuild:** Refresh=incremental update (faster, preserves customizations) | Rebuild=full re-index (slower, clean slate)

**See:** `references/templates.md#index-maintenance` for detailed refresh process and output examples

---

## Best Practices

Index early (before implementation) | Keep docs updated (refresh after changes) | Use quick ref (faster than full docs) | Maintain glossary (project-specific terms) | Include code selectively (key files only)

---

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats (Steps 1-4), search.json structure, quick-ref.md format, glossary.md format, search examples, integration workflows, index maintenance, JSON output format

- **indexing-format.md**: Index structure details (comprehensive in templates.md)

- **code-mapping.md**: Code-to-docs mapping strategies

---

## When to Escalate

- Documentation is sparse or missing (run `document-project` first)
- Codebase structure is unclear or chaotic
- Index becomes too large (>100MB)
- Search performance degrades

---

*Part of BMAD Enhanced Brownfield Suite*
