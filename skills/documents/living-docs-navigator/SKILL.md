---
name: living-docs-navigator
description: Navigate and load project living documentation for context. Provides a table of contents for specs, ADRs, architecture docs, and operations runbooks. Use when implementing features, making design decisions, or needing project context. Keywords - living docs, context, ADR, architecture, specs, documentation, project knowledge.
---

# Living Docs Navigator

Access project knowledge stored in `.specweave/docs/internal/`.

## Quick Navigation

**When you need context**, read relevant files from these locations:

### 📋 Specifications (Features & User Stories)
```
.specweave/docs/internal/specs/
```
- Feature specifications with user stories
- Acceptance criteria
- Implementation history

**Find specs**: `ls .specweave/docs/internal/specs/`

### 📐 Architecture Decisions (ADRs)
```
.specweave/docs/internal/architecture/adr/
```
- WHY decisions were made
- Trade-offs considered
- Context for design choices

**Find ADRs**: `ls .specweave/docs/internal/architecture/adr/`

### 🏗️ System Architecture
```
.specweave/docs/internal/architecture/
```
- High-level design (HLD)
- System diagrams
- Component architecture

**Find architecture docs**: `ls .specweave/docs/internal/architecture/*.md`

### 📊 Operations
```
.specweave/docs/internal/operations/
```
- Runbooks
- SLOs
- Incident procedures

### 💼 Strategy
```
.specweave/docs/internal/strategy/
```
- Business requirements
- Product vision
- PRDs

### 🛡️ Governance
```
.specweave/docs/internal/governance/
```
- Security policies
- Coding standards
- Compliance docs

---

## How to Use

### Before Implementing a Feature

1. **Check for related specs**:
   ```bash
   grep -ril "keyword" .specweave/docs/internal/specs/
   ```

2. **Read relevant ADRs**:
   ```bash
   grep -l "topic" .specweave/docs/internal/architecture/adr/*.md
   ```

3. **Load the context** by reading the files found.

### Before Making Design Decisions

1. **Check existing ADRs** to avoid contradicting past decisions
2. **Read architecture docs** to understand current patterns
3. **Follow established conventions**

### Example Workflow

```
Task: "Implement user authentication"

1. Search for related docs:
   grep -ril "auth" .specweave/docs/internal/

2. Found:
   - .specweave/docs/internal/specs/backend/us-001-authentication.md
   - .specweave/docs/internal/architecture/adr/0001-jwt-vs-sessions.md
   - .specweave/docs/internal/architecture/auth-flow.md

3. Read each file for context before implementing.
```

---

## Progressive Disclosure Pattern

This skill follows **progressive disclosure**:

1. **Metadata only** (this SKILL.md) loads initially (~200 tokens)
2. **You search** for relevant docs using grep/ls
3. **You read** only the specific files you need
4. **Result**: Minimal tokens, maximum context

**No RAG needed** - Claude's native file reading is more accurate.

---

## Integration with /sw:do

When executing `/sw:do`:

1. Extract topic keywords from spec.md
2. Search living docs for matches
3. Read relevant ADRs and architecture docs
4. Apply context during implementation

---

## Tips

- **ADRs are critical** - always check before design decisions
- **Specs show history** - see what was already built
- **Use grep liberally** - find docs by keyword, not guessing paths
- **Cross-reference** - related documents link to each other
