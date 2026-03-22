---
name: docs
description: Write, update, and review project documentation
---

# Docs

Uses **Implementer** (primary). Create, update, and review documentation following established conventions.

**Prerequisites:** Clear documentation target (what to document), access to relevant source material

---

## Phase 1: Assess Documentation Need

### Identify Scope

1. Determine the documentation type:
   - **ADR** — Architectural Decision Record (`docs/adr/`)
   - **Guide** — How-to or getting-started (`docs/guides/`)
   - **Architecture** — System design documentation (`docs/architecture/`)
   - **README** — Project or directory overview
   - **Inline** — Code comments and JSDoc/XML doc
   - **Note** — Research findings and analysis (`docs/notes/`)
2. Check for existing documentation to update vs. create new
3. Identify the target audience

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title> (if applicable)
- **Phase:** 1 — Assess

## Documentation Plan

**Type:** <ADR | Guide | Architecture | README | Inline | Observation>
**Action:** Create new | Update existing
**Target:** <file path>
**Audience:** <developers | operators | contributors>

## Next Step

Draft the documentation.

**Approval Required:** No
```

---

## Phase 2: Draft

### Writing Rules

- Follow markdownlint conventions
- Use ATX-style headings (`#` not underlines)
- One sentence per line in source (for clean diffs)
- Use tables for structured comparisons
- Include code examples where helpful
- Link to related documentation

### ADR Format

Follow the template in `docs/adr/`:

```markdown
# <number>. <Title>

Date: YYYY-MM-DD

## Status

Proposed | Accepted | Deprecated | Superseded by [ADR-NNNN]

## Context

<What is the issue that we're seeing that is motivating this decision?>

## Decision

<What is the change that we're proposing and/or doing?>

## Consequences

<What becomes easier or more difficult to do because of this change?>
```

### Guide Format

```markdown
# <Title>

<Brief description of what this guide covers>

## Prerequisites

- <what you need before starting>

## Steps

### 1. <First Step>

<instructions>

### 2. <Second Step>

<instructions>

## Troubleshooting

| Problem | Solution |
| ------- | -------- |
| <issue> | <fix>    |
```

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 2 — Draft

## Documentation Created/Updated

**File:** <path>
**Summary:** <what was documented>

## Next Step

Review the documentation for accuracy and completeness.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not finalize without human review of content accuracy.

---

## Phase 3: Review and Finalize

### Review Checklist

- [ ] Content is accurate and complete
- [ ] Links to related docs are correct
- [ ] Code examples are tested/verified
- [ ] Follows markdownlint conventions
- [ ] No broken internal links
- [ ] Appropriate for target audience

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 3 — Finalize

## Documentation Summary

| File   | Action  | Description    |
| ------ | ------- | -------------- |
| <path> | Created | <what it docs> |

## Next Step

<commit / PR / further edits>

**Approval Required:** No
```

### ⛔ CHECKPOINT

**STOP.** Verify documentation is complete and accurate before committing.

---

## Error Handling

| Error                     | Recovery                                |
| ------------------------- | --------------------------------------- |
| Conflicting documentation | Flag conflict, propose resolution       |
| Missing source material   | Ask for clarification before drafting   |
| Outdated referenced docs  | Update references as part of the change |
