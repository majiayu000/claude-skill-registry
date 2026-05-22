---
name: aget-search-literature
description: Search and review literature and prior work
archetype: researcher
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# aget-search-literature

Search and review relevant literature, papers, and prior work. Prioritizes internal KB before external sources.

## Instructions

When this skill is invoked:

1. **Search Internal KB First**
   - L-docs in `.aget/evolution/`
   - Patterns in `.aget/patterns/`
   - Specs in `specs/`
   - SOPs in `sops/`

2. **Search External (if enabled)**
   - Academic sources
   - Technical documentation
   - Web resources

3. **Synthesize Findings**
   - Summarize key points
   - Note convergence/divergence
   - Identify gaps

4. **Provide Citations**
   - Proper attribution
   - Accessible references
   - Context for each

## Output Format

```markdown
## Literature Review: [Topic]

### Search Parameters

| Parameter | Value |
|-----------|-------|
| Topic | [Search terms] |
| Scope | [KB Only / KB + External] |
| Date | [YYYY-MM-DD] |

---

### Internal KB Results

#### L-docs
| ID | Title | Relevance |
|----|-------|-----------|
| L[XXX] | [Title] | [How it relates] |

#### Patterns
- [Pattern name]: [Relevance]

#### Specs
- [Spec name]: [Relevance]

---

### External Results (if searched)

| Source | Title | Key Finding |
|--------|-------|-------------|
| [URL/Ref] | [Title] | [Relevant insight] |

---

### Synthesis

**Key Themes**:
1. [Theme 1]: [Summary]
2. [Theme 2]: [Summary]

**Convergence**: [Where sources agree]

**Divergence**: [Where sources differ]

---

### Knowledge Gaps

1. [Gap 1]: [What's missing]
2. [Gap 2]: [What's missing]

---

### Citations

1. [Full citation 1]
2. [Full citation 2]
```

## Constraints

- **C1**: NEVER fabricate sources or citations — research integrity essential
- **C2**: NEVER present paraphrased content without attribution — plagiarism must be avoided
- **C3**: NEVER claim comprehensive coverage without noting limitations — search scope must be acknowledged

## Related

- SKILL-029: aget-search-literature specification
- ONTOLOGY_researcher.yaml: Literature, Citation, Knowledge_Gap concepts
- CAP-RES-001: Literature Search capability
