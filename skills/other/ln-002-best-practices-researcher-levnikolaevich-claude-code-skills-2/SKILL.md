---
name: ln-002-best-practices-researcher
description: Research best practices via MCP Ref/Context7/WebSearch and create documentation (guide/manual/ADR/research). Single research, multiple output types.
---

# Best Practices Researcher

Research industry standards and create project documentation in one workflow.

## Purpose & Scope
- Research via MCP Ref + Context7 for standards, patterns, versions
- Create 4 types of documents from research results:
  - Guide: Pattern documentation (Do/Don't/When table)
  - Manual: API reference (methods/params/doc links)
  - ADR: Architecture Decision Record (Q&A dialog)
  - Research: Investigation document answering specific question
- Return document path for linking in Stories/Tasks

## Phase 0: Stack Detection

**Objective**: Identify project stack to filter research queries and adapt output.

**Detection:**

| Indicator | Stack | Query Prefix | Official Docs |
|-----------|-------|--------------|---------------|
| `*.csproj`, `*.sln` | .NET | "C# ASP.NET Core" | Microsoft docs |
| `package.json` + `tsconfig.json` | Node.js | "TypeScript Node.js" | MDN, npm docs |
| `requirements.txt`, `pyproject.toml` | Python | "Python" | Python docs, PyPI |
| `go.mod` | Go | "Go Golang" | Go docs |
| `Cargo.toml` | Rust | "Rust" | Rust docs |
| `build.gradle`, `pom.xml` | Java | "Java" | Oracle docs, Maven |

**Usage:**
- Add `query_prefix` to all MCP search queries
- Link to stack-appropriate official docs

## When to Use
- ln-310-story-validator detects missing documentation
- Need to document a pattern, library, or decision
- Replaces: ln-321-guide-creator, ln-322-adr-creator, ln-323-manual-creator

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| doc_type | Yes | "guide" / "manual" / "adr" / "research" |
| topic | Yes | What to document (pattern name, package name, decision title, research question) |
| story_context | No | Story/Task context for relevance |

## Research Tools

| Tool | Use Case | Query Pattern |
|------|----------|---------------|
| `ref_search_documentation` | Standards, patterns, RFCs | `"[topic] RFC standard best practices 2025"` |
| `context7__resolve-library-id` | Get library ID for docs | `libraryName="[topic]"` |
| `context7__query-docs` | Library API, methods | `topic="[stack_prefix] [topic]"` |
| `WebSearch` | Market, competitors, versions | `"[topic] latest 2025"` or `"[topic] vs alternatives"` |

**Time-box:** 5-10 minutes for research; skip if topic is trivial

## Research Methodology by Type (for doc_type="research")

| Type | Focus | Primary Sources | Key Questions |
|------|-------|-----------------|---------------|
| **Technical** | Solution comparison | Docs, benchmarks, RFCs | "Which solution fits our use-case?" |
| **Market** | Industry landscape | Reports, blogs, articles | "What's the market size/trend?" |
| **Competitor** | How others solve it | Product pages, reviews, demos | "What features do competitors offer?" |
| **Requirements** | User needs | Feedback, support tickets, forums | "What do customers complain about?" |
| **Feasibility** | Can we build it? | PoC, prototypes, local tests | "Is it technically possible?" |
| **Feature Demand** | Feature viability | Competitor features + blogs/socials + user complaints | "Is this feature worth building?" |

## Workflow by doc_type

| doc_type | Purpose | Research Source | Template | Output Path | Words |
|----------|---------|-----------------|----------|-------------|-------|
| **guide** | Pattern with Do/Don't/When table | `ref_search` (best practices) | guide_template.md | `guides/NN-[slug].md` | 300-500 |
| **manual** | API/library reference | `context7__query-docs` | manual_template.md | `manuals/[pkg]-[ver].md` | 300-500 |
| **adr** | Architecture decision | Dialog (5 questions) | adr_template.md | `adrs/adr-NNN-[slug].md` | 300-500 |
| **research** | Investigation answering question | See Methodology table above | research_template.md | `research/rsh-NNN-[slug].md` | 300-700 |

**Common Workflow:** Detect number (if needed) → Research → Generate from template → Validate (SCOPE, POSIX) → Save → Return path

**Extract & Sections by doc_type:**
- **guide:** Extract principle, 2-3 do/don'ts, sources → Sections: Principle, Our Implementation, Patterns table, Sources, Related
- **manual:** Extract methods, params (type/required/default), returns → Sections: Package info, Overview, Methods table, Config table, Limitations
- **adr:** Dialog answers → Sections: Context, Decision, Rationale, Alternatives table, Consequences, Related
- **research:** Findings by methodology → Sections: Question, Context, Methodology, Findings (tables!), Conclusions, Next Steps, Sources

**Validation specifics:** guide: patterns table present; manual: version in filename; adr: ISO date, status field; all: sources ≥2025

**ADR Dialog (5 questions):** Q1: Title? → Q2: Category (Strategic/Technical)? → Q3: Context? → Q4: Decision + Rationale? → Q5: Alternatives (2 with pros/cons)?

**Output:** File path for linking in Stories/Tasks; for ADR remind to reference in architecture.md; for Research suggest ADR if decision needed

## Critical Rules

**NO_CODE_EXAMPLES (ALL document types):**

| Forbidden | Allowed |
|-----------|---------|
| Code snippets | Tables (params, config, alternatives) |
| Implementation examples | ASCII diagrams, Mermaid diagrams |
| Code blocks >1 line | Method signatures (1 line inline) |
| | Links to official docs |

**Format Priority (STRICT):**
```
┌───────────────────────────────────────────────┐
│ 1. TABLES + ASCII diagrams  ←── PRIORITY      │
│    Params, Config, Alternatives, Flows        │
├───────────────────────────────────────────────┤
│ 2. LISTS (enumerations only)                  │
│    Enumeration items, file lists, tools       │
├───────────────────────────────────────────────┤
│ 3. TEXT (last resort)                         │
│    Only if cannot express as table            │
└───────────────────────────────────────────────┘
```

| Content Type | Format |
|--------------|--------|
| Parameters | Table: Name \| Type \| Required \| Default |
| Configuration | Table: Option \| Type \| Default \| Description |
| Alternatives | Table: Alt \| Pros \| Cons \| Why Rejected |
| Patterns | Table: Do \| Don't \| When |
| Workflow | ASCII diagram: `A → B → C` |

**Other Rules:**
- Research ONCE per invocation; reuse results
- Cite sources with versions/dates (>=2025)
- One pattern per guide; one decision per ADR; one package per manual
- Preserve language (EN/RU) from story_context
- Link to stack-appropriate docs (Microsoft for .NET, MDN for JS, etc.)
- Do not create if target directory missing (warn instead)

## Definition of Done
- Research completed (standards/patterns/versions extracted) - for guide/manual
- Dialog completed (5 questions answered) - for ADR
- Document generated with all required sections; no placeholders
- Standards validated (SCOPE, maintenance, POSIX)
- File saved to correct directory with proper naming
- Path returned; README updated if placeholder present

## Reference Files
- Guide template: `shared/templates/guide_template.md`
- Manual template: `shared/templates/manual_template.md`
- ADR template: `shared/templates/adr_template.md`
- Research template: `shared/templates/research_template.md`
- Standards: `docs/DOCUMENTATION_STANDARDS.md` (if exists)

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
