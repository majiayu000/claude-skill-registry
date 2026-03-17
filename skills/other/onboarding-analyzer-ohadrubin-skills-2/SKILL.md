---
name: onboarding-analyzer
description: Gather and analyze source material for onboarding documentation. Creates source_inventory.md and extraction_tables.md. Triggered by onboarding-start during source-material-gathering and key-information-extraction phases.
---

# Onboarding Analyzer

Gather source material and extract key information from a codebase for onboarding documentation.

## Workflow

### Phase 1: Source Material Gathering

Create `{name}_source_inventory.md` with the following procedure:

**1.1 Identify Keywords**
- Identify the most general keyword for the feature (e.g., "auth", "cache", "validation")
- Break it into related terms (e.g., "auth" → "auth", "login", "token", "session")

**1.2 BM25 Search**
- Uses `git ls-files` to search all tracked files. Pass each term with `-t`:
  ```bash
  uv run /path/to/skill/scripts/search.py -t auth -t login -t token
  ```
  VERY IMPORTANT: YOU MUST USE search.py using uv.
- Record top results with path and 1-2 sentence summary
- For each file found, note:
  - File path
  - Entry points (main functions, exports)
  - Brief 1-line description

**1.3 Identify Plans/Specs**
- Search for design docs, specs, requirements:
  ```bash
  uv run /path/to/skill/scripts/search.py -t spec -t design -t plan
  ```
- Note if absent.

### Phase 2: Key Information Extraction

Create `{name}_extraction_tables.md` with structured tables:

**2.1 Function Table**

| Function | File:Lines | Purpose |
|----------|-----------|---------|
| `foo()` | `main.py:42-50` | Initializes the config |
| `bar()` | `main.py:52-80` | Processes input data |

**2.2 Dependency Table**

| Dependency | Version/Source | Used By |
|------------|----------------|---------|
| `anthropic` | PyPI | `llm.py` |
| `requests` | PyPI | `api.py` |

**2.3 Data Flow**

Document the "happy path":
1. Entry: `main()` receives request
2. Calls: `validate()` checks input
3. Calls: `process()` does work
4. Returns: result to caller

## Key Questions to Answer

During gathering:
- What feature/phase is being documented?
- Which files are main implementation?
- What existing documentation exists?

During extraction:
- What are the main functions/classes?
- What calls what?
- What external APIs are used?

## Success Criteria

`{name}_source_inventory.md`:
- [ ] Keywords and related terms listed
- [ ] Files found via BM25 search with summaries and entry points
- [ ] Plans/specs noted (or marked absent)

`{name}_extraction_tables.md`:
- [ ] Function table with accurate line numbers
- [ ] Dependency table with versions
- [ ] Data flow from entry to exit documented
