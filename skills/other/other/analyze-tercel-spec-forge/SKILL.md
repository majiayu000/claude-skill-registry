---
name: analyze
description: >
  Analyze a collection of documents to build a knowledge map, identify themes, find gaps, duplicates,
  conflicts, and staleness, then produce an organized analysis with improvement recommendations.
  Designed for document ecosystems (cross-repo docs, research collections, mixed-format doc repos)
  where the challenge is understanding the landscape, not auditing against code.
instructions: >
  Follow the workflow below exactly. This skill is exploratory — it reads a collection of
  documents, builds a mental model of the landscape, and produces a structured analysis.
  Unlike /audit which checks docs against code, /analyze focuses on the documents themselves
  as a body of knowledge. Do NOT modify any source documents. The output is an analysis
  report with a document map, theme clusters, and improvement recommendations.
---

# Analyze — Document Landscape Analysis & Knowledge Mapping

Map, understand, and evaluate a collection of documents as a body of knowledge. Identify structure, themes, gaps, redundancies, conflicts, and staleness. Produce an actionable analysis with reorganization recommendations.

## Core Principles

1. **Landscape-first**: Build the map before judging — understand what exists before critiquing
2. **Theme-driven**: Group documents by what they're about, not just where they live
3. **Conflict detection**: Find contradictions between documents that may confuse readers
4. **Staleness awareness**: Identify documents that may be outdated based on content signals
5. **Non-destructive**: Only reads and reports — never modifies source documents
6. **Reorganization as suggestion**: Propose better structures, don't impose them

## When to Use Analyze vs. Audit

| Situation | Use |
|-----------|-----|
| Single project with docs/ and source code | `/spec-forge:audit` |
| Docs-only repo with mixed content | `/spec-forge:analyze` |
| Cross-repo documentation ecosystem | `/spec-forge:analyze` |
| Research notes, ideas, decision records | `/spec-forge:analyze` |
| API docs need checking against code | `/spec-forge:audit` |
| "I have a mess of docs and need to understand them" | `/spec-forge:analyze` |

## Workflow

### Step 1: Determine Scope

Parse the arguments to determine what to analyze:

1. If a path argument is provided (e.g., `/spec-forge:analyze ../../aipartnerup-docs`), use that as the root
2. If no path, use the current working directory's `docs/` directory
3. If multiple paths are provided, analyze all of them as one collection

Use `AskUserQuestion` to understand the user's goals:
- **What is this collection?** (e.g., "ecosystem docs for multiple products", "research notes", "mixed specs and decisions")
- **What do you want to understand?** Options:
  - Full landscape analysis (recommended for first time)
  - Find conflicts and contradictions
  - Find gaps and missing coverage
  - Suggest reorganization
  - All of the above

### Step 2: Document Discovery & Inventory

Scan all documents in the target path(s):

1. **Glob for all markdown files** recursively
2. **Read every document** (first 300 lines for large files) to understand content
3. **Extract metadata** for each document:
   - File path and directory position
   - Title (first H1 or filename)
   - Approximate word count
   - Last modified date (git log if available, file stat otherwise)
   - Document type classification (see below)
   - Key entities mentioned (product names, system names, technologies)
   - Key claims or decisions stated
   - Internal links to other documents
   - Apparent audience (developers, product, leadership, external)

**Document type classification:**

| Type | Signals |
|------|---------|
| `vision` | Mission, vision, strategy, roadmap, long-term goals |
| `architecture` | System design, component diagrams, data flow, technical architecture |
| `spec` | Requirements, specifications, protocols, standards, conformance |
| `research` | Analysis, investigation, comparison, feasibility study, market research |
| `decision` | ADR, decision record, strategy choice, trade-off analysis |
| `idea` | Brainstorm, proposal, exploration, "what if", future thinking |
| `guide` | How-to, tutorial, getting started, cookbook |
| `reference` | API reference, data dictionary, glossary, type mapping |
| `blueprint` | Master plan, project plan, implementation roadmap |
| `report` | Status report, audit report, analysis output |
| `meta` | README, index, navigation, table of contents |

Display the inventory:

```
Document Collection: {name}
  Root: {path}
  Total documents: {N}
  Total words: ~{N}k

  Directory Structure:
    {dir}/           ({n} docs) — {apparent purpose}
    {dir}/{subdir}/  ({n} docs) — {apparent purpose}
    ...

  By Type:
    vision:       {n} docs
    architecture: {n} docs
    research:     {n} docs
    ...
```

### Step 3: Theme & Cluster Analysis

Group documents by what they're actually about, regardless of directory structure:

#### 3.1 Identify Themes

Read through all documents and identify the major themes/topics that emerge:
- Product/system names mentioned across multiple docs
- Recurring concepts or concerns
- Shared vocabulary or domain terms

#### 3.2 Build Theme Clusters

For each theme, list which documents contribute to it:

```
Theme Clusters:

  "{Theme A}" — {description}
    Primary:    {docs that are mainly about this}
    Secondary:  {docs that touch on this}
    Coverage:   {Good / Partial / Sparse}

  "{Theme B}" — {description}
    Primary:    ...
    Secondary:  ...
    Coverage:   ...
```

#### 3.3 Cross-Reference Map

Build a document relationship map:
- Which docs reference each other?
- Which docs should reference each other but don't?
- Are there isolated documents with no connections?

Generate a Mermaid graph showing document relationships.

### Step 4: Conflict & Contradiction Detection

Systematically compare documents for conflicts:

#### 4.1 Factual Conflicts

Look for places where two documents state contradictory facts:
- Different architecture descriptions for the same system
- Conflicting technology choices or version numbers
- Contradictory timelines or priorities
- Inconsistent naming (same thing called different names, or same name for different things)

For each conflict:
```
CONFLICT-{NNN}: {title}
  Doc A: {path} — states "{claim A}" (section: {section})
  Doc B: {path} — states "{claim B}" (section: {section})
  Nature: {factual contradiction / naming inconsistency / version mismatch / priority conflict}
  Impact: {who gets confused and how}
  Resolution suggestion: {which doc is likely correct, or how to reconcile}
```

#### 4.2 Strategic Conflicts

Look for higher-level misalignments:
- Vision docs that contradict architecture decisions
- Research findings that aren't reflected in decisions
- Ideas that overlap with or contradict existing plans
- Decisions that seem to ignore relevant research

#### 4.3 Temporal Conflicts

Look for staleness-related contradictions:
- Old docs describing plans that newer docs have superseded
- Documents referencing deprecated technologies or abandoned features
- Timelines or milestones that have clearly passed without update

### Step 5: Gap Analysis

Identify what's missing from the document collection:

#### 5.1 Coverage Gaps

Based on the themes and types identified:
- Are there themes with no vision/strategy doc?
- Are there systems with no architecture doc?
- Are there decisions with no supporting research?
- Are there ideas that were never evaluated or decided on?
- Is there a getting-started guide for new team members?

#### 5.2 Depth Gaps

Some areas may be documented but not deeply enough:
- Vision without concrete roadmap
- Architecture without component details
- Research without conclusions or recommendations
- Decisions without recorded rationale

#### 5.3 Audience Gaps

Check if all relevant audiences are served:
- Developer documentation (architecture, API, guides)
- Product documentation (vision, requirements, roadmap)
- Leadership documentation (strategy, metrics, status)
- External documentation (README, getting started, examples)

### Step 6: Redundancy Detection

Find documents that overlap significantly:

1. **Near-duplicates**: Documents covering the same topic with slightly different content
2. **Superseded docs**: Older versions that should have been replaced but weren't
3. **Scattered coverage**: Same topic spread across multiple docs that could be consolidated

For each redundancy:
```
REDUNDANCY-{NNN}: {title}
  Documents: {list of overlapping docs}
  Overlap: {what they share}
  Recommendation: {merge into X / archive Y / consolidate into new doc Z}
```

### Step 7: Staleness Assessment

Evaluate document freshness:

1. **Age signals**: Last modified date, referenced dates in content
2. **Content signals**: Mentions of deprecated technologies, past tense for future plans, "TODO" items that should have been resolved
3. **Context signals**: Referenced systems that no longer exist, links that would be broken

Classify each document:
- **Current**: Content appears up-to-date
- **Possibly stale**: Some signals of age but content may still be valid
- **Likely stale**: Strong signals that content is outdated
- **Archival**: Document is historical record, not meant to be current

### Step 8: Generate Analysis Report

Write the analysis report to `{target-root}/analysis-report.md` (or user-specified path).

**Report format:**

```markdown
# Document Landscape Analysis

> Collection: {name}
> Root: {path}
> Analyzed: {date}
> Documents: {N} ({total words}k words)

## Executive Summary

{3-4 paragraphs: what this collection is about, its strengths as a knowledge base,
the most important issues found, and the top recommended actions}

## Document Map

### By Directory

| Directory | Docs | Purpose | Health |
|-----------|------|---------|--------|
| {dir}     | {n}  | {purpose} | {Good/Mixed/Poor} |

### By Type

| Type | Count | Key Documents |
|------|-------|---------------|
| vision | {n} | {most important ones} |
| architecture | {n} | ... |
| ... | ... | ... |

### Relationship Graph

~~~mermaid
graph LR
  ...
~~~

## Theme Analysis

### {Theme 1}: {name}

**Coverage**: {Good / Partial / Sparse}
**Key documents**: {list}
**Gaps**: {what's missing}

### {Theme 2}: {name}
...

## Findings

### Conflicts ({n} found)

{Ordered by severity}

#### CONFLICT-001: {title}
...

### Gaps ({n} found)

#### GAP-001: {title}
- **Area**: {theme/topic}
- **What's missing**: {description}
- **Why it matters**: {impact}
- **Recommendation**: {what to create or expand}

### Redundancies ({n} found)

#### REDUNDANCY-001: {title}
...

### Staleness ({n} documents flagged)

| Document | Status | Signals | Recommendation |
|----------|--------|---------|----------------|
| {path}   | Likely stale | {signals} | {update/archive/delete} |

## Reorganization Recommendations

{If the current structure has significant issues, propose an alternative organization.
Show current structure → proposed structure side by side.
Only propose reorganization if it would meaningfully improve navigability — don't reorganize for aesthetics.}

### Current Structure
~~~
{current directory tree}
~~~

### Proposed Structure
~~~
{proposed directory tree with annotations}
~~~

### Migration Steps
1. {step — which files to move/merge/archive}
2. ...

## Priority Actions

| # | Action | Addresses | Effort | Impact |
|---|--------|-----------|--------|--------|
| 1 | {action} | CONFLICT-001, GAP-003 | {S/M/L} | {High/Med/Low} |
| 2 | {action} | REDUNDANCY-001 | {S/M/L} | {High/Med/Low} |
| ... | ... | ... | ... | ... |
```

### Step 9: Present Results

Display a summary to the user:

```
Analysis complete: {collection-name}

  Documents analyzed: {N}
  Themes identified: {N}
  Conflicts: {n}
  Gaps: {n}
  Redundancies: {n}
  Stale documents: {n}

  Report: {path-to-analysis-report.md}

  Top 3 priority actions:
    1. {action} — {impact}
    2. {action} — {impact}
    3. {action} — {impact}
```

Use `AskUserQuestion` to ask what to do next:
- **Deep dive**: Explore a specific theme or conflict in detail
- **Fix conflicts**: Help resolve specific contradictions
- **Fill gaps**: Generate missing documents using spec-forge skills
- **Reorganize**: Execute the proposed reorganization (move/rename/merge files)
- **Done**: Just the report for now

### Step 10: Follow-Up Actions (Optional)

Based on user choice:

**Deep dive**: Read the relevant documents in full, provide a detailed analysis of the specific area, and discuss with the user.

**Fix conflicts**: For each conflict, read both documents in full, determine the correct information (asking the user when uncertain), and propose specific edits. Only apply edits after user approval.

**Fill gaps**: For identified gaps, suggest which spec-forge skill to use:
- Missing architecture doc → `/spec-forge:tech-design`
- Missing requirements → `/spec-forge:prd` or `/spec-forge:srs`
- Missing test plan → `/spec-forge:test-plan`
- Missing strategy/research → manual writing or `/spec-forge:idea` for exploration

**Reorganize**: Execute file moves/renames step by step, confirming with user before each destructive action (deletes, merges). Update internal links after moves.

## Notes

1. **Cross-repo support**: Can analyze documents across multiple repositories by providing multiple paths
2. **No code requirement**: Unlike /audit, /analyze works purely on documents — no codebase needed
3. **Preserves originals**: Never modifies source documents during analysis (only during explicit follow-up actions)
4. **Incremental**: If a previous `analysis-report.md` exists, note what changed since last analysis
5. **Language agnostic**: Works with any documentation regardless of the project's programming language
6. **Scale aware**: For very large collections (50+ docs), focus depth on the most important documents and provide breadth coverage for the rest
