---
name: audit
description: >
  Audit existing project documentation for quality, completeness, consistency, and code alignment.
  Scans docs against the actual codebase to find stale references, missing coverage, internal
  contradictions, and quality issues. Generates a structured findings report with severity levels
  and actionable fix recommendations. Works on any project with a docs/ directory.
instructions: >
  Follow the workflow below exactly. This skill is analytical — it reads and evaluates existing
  documents, it does NOT generate new specification documents. The output is a findings report
  with prioritized issues. Each finding must cite the specific file, line or section, and provide
  a concrete fix suggestion. Do NOT fabricate issues — only report what you actually find.
---

# Audit — Documentation Quality & Consistency Review

Systematically review existing project documentation for quality, completeness, consistency with code, and internal coherence. Produce a prioritized findings report.

## Core Principles

1. **Evidence-based**: Every finding must cite a specific file, section, or line — no vague complaints
2. **Code-grounded**: Cross-reference documentation claims against the actual codebase
3. **Prioritized**: Findings are classified by severity so the user can fix what matters first
4. **Read-only by default**: This skill only reads and reports — document modifications require explicit user opt-in (Step 8)
5. **Honest**: Report real issues, don't inflate findings to look thorough

## Severity Levels

| Severity | Meaning | Example |
|----------|---------|---------|
| **Critical** | Documentation is wrong or dangerously misleading | API doc shows deleted endpoint, security guide has incorrect auth flow |
| **Major** | Significant gap or inconsistency that causes confusion | Feature doc missing for a core module, conflicting architecture descriptions |
| **Minor** | Quality issue that degrades usefulness but isn't blocking | Typos in API params, outdated version numbers, missing examples |
| **Info** | Observation or improvement suggestion | Better organization possible, diagram would help clarity |

## Workflow

### Step 1: Determine Audit Scope

Parse the arguments to determine what to audit:

1. If a path argument is provided (e.g., `/spec-forge:audit ../../other-project`), use that as the project root
2. If no path, use the current working directory
3. Verify the target has documentation (check for `docs/`, `README.md`, or markdown files)

If no documentation found, inform the user and stop.

Use `AskUserQuestion` to ask:
- **Audit focus**: Full audit, or focus on a specific area? (Options: Full / API docs only / Feature docs only / Architecture docs only / Custom path)
- **Code alignment**: Should I cross-reference docs against the codebase? (Yes / No — skip if docs-only repo like aipartnerup-docs)

### Step 2: Document Inventory

Scan the documentation landscape and build a complete inventory.

1. **Glob for all markdown files** in the docs directory (and README at root)
2. **Categorize each document** by type:
   - `api` — API reference documentation
   - `architecture` — Architecture, design, system overview
   - `feature` — Feature specifications or descriptions
   - `guide` — How-to guides, tutorials, getting started
   - `spec` — Protocol specs, conformance, standards
   - `decision` — ADRs, decision records
   - `reference` — Data models, type mappings, glossaries
   - `meta` — READMEs, indexes, navigation docs
   - `other` — Doesn't fit above categories
3. **Read each document** (or at least the first 200 lines for very large files) to understand its content and structure
4. **Record metadata** for each document:
   - File path
   - Category
   - Approximate word count
   - Last modified date (from git if available)
   - Key topics covered
   - Cross-references to other docs (internal links)
   - Cross-references to code (file paths, class/function names mentioned)

Display the inventory:

```
Document Inventory: {project-name}
  Path: {project-root}
  Total documents: {N}

  Category          | Count | Files
  api               |   4   | api/README.md, api/executor-api.md, ...
  feature           |   8   | features/acl-system.md, ...
  guide             |   7   | guides/creating-modules.md, ...
  ...
```

### Step 3: Code Alignment Check

**Skip this step if the user opted out in Step 1 (e.g., docs-only repo).**

Cross-reference documentation against the actual codebase:

#### 3.1 API Surface Audit

1. **Scan the codebase** for public API surfaces: exported functions, classes, interfaces, types, endpoints
2. **Compare against API docs**: For each documented API, verify:
   - Does the function/class/endpoint still exist in code?
   - Do parameter names and types match?
   - Do return types match?
   - Are documented examples still valid?
3. **Find undocumented APIs**: Public APIs that exist in code but have no documentation

Report findings:
- **Stale API docs**: Documented APIs that no longer exist or have changed
- **Undocumented APIs**: Code APIs with no corresponding documentation
- **Parameter mismatches**: Documented params that don't match code signatures

#### 3.2 Feature Coverage Audit

1. **Identify features in code**: Major modules, systems, or functional areas in the codebase
2. **Compare against feature docs**: Is each significant feature documented?
3. **Check feature doc accuracy**: Do feature descriptions match the current implementation?

Report findings:
- **Undocumented features**: Significant code modules with no feature documentation
- **Stale feature docs**: Feature docs describing behavior that has changed
- **Missing feature aspects**: Feature docs that exist but skip important aspects (config, error handling, limitations)

#### 3.3 Architecture Alignment

1. **Infer architecture from code**: Module structure, dependency graph, communication patterns
2. **Compare against architecture docs**: Does the documented architecture match reality?
3. **Check for architectural drift**: Places where code has evolved away from the documented design

### Step 4: Internal Consistency Check

Check documents against each other for contradictions and coherence:

#### 4.1 Cross-Document Consistency

1. **Terminology consistency**: Same concept referred to by different names across docs?
2. **Factual consistency**: Do different docs make contradictory claims? (e.g., architecture doc says "microservices" but feature doc says "monolith")
3. **Version/dependency consistency**: Do different docs reference different versions of the same thing?
4. **Link integrity**: Do internal cross-references actually point to existing documents/sections?

#### 4.2 Structural Consistency

1. **Format consistency**: Do similar documents follow similar structures? (e.g., all feature docs should have similar sections)
2. **Depth consistency**: Are some areas documented exhaustively while others are skeletal?
3. **Naming consistency**: File naming conventions, heading styles, code formatting

### Step 5: Quality Assessment

Evaluate each document (or document category) on quality dimensions:

| Dimension | What to Check |
|-----------|---------------|
| **Completeness** | Missing sections, TBD/TODO markers, placeholder text, empty sections |
| **Accuracy** | Incorrect information (detected via code alignment or internal contradictions) |
| **Clarity** | Ambiguous language, undefined terms, unclear instructions |
| **Specificity** | Vague descriptions vs. concrete details (e.g., "fast" vs. "< 100ms p99") |
| **Actionability** | Can a developer act on this doc without guessing? Are examples provided? |
| **Currency** | Signs of staleness — old dates, deprecated references, outdated patterns |
| **Navigation** | Can readers find what they need? Cross-references, indexes, logical organization |

### Step 6: Generate Findings Report

Write the findings report to `{project-docs-path}/audit-report.md` (or a user-specified path).

**Report format:**

```markdown
# Documentation Audit Report

> Project: {project-name}
> Audited: {date}
> Scope: {full / api-only / feature-only / etc.}
> Documents reviewed: {N}
> Code alignment: {Yes / Skipped}

## Executive Summary

{2-3 paragraph overview: overall documentation health, biggest strengths, most critical gaps}

## Findings Summary

| Severity | Count | Categories |
|----------|-------|------------|
| Critical |   {n} | {which areas} |
| Major    |   {n} | {which areas} |
| Minor    |   {n} | {which areas} |
| Info     |   {n} | {which areas} |

## Document Health Matrix

| Document | Completeness | Accuracy | Clarity | Currency | Overall |
|----------|-------------|----------|---------|----------|---------|
| {path}   | {A/B/C/D}   | {A/B/C/D}| {A/B/C/D}| {A/B/C/D}| {A/B/C/D} |

(A = Excellent, B = Good, C = Needs Work, D = Poor)

## Critical Findings

### CRIT-001: {Finding title}
- **Location**: {file path, section/line}
- **Issue**: {What is wrong}
- **Evidence**: {How you know — code reference, conflicting doc, etc.}
- **Impact**: {Why this matters}
- **Fix**: {Concrete recommendation}

### CRIT-002: ...

## Major Findings

### MAJ-001: {Finding title}
...

## Minor Findings

### MIN-001: {Finding title}
...

## Observations & Suggestions

### INFO-001: {Suggestion title}
...

## Coverage Map

{Mermaid diagram showing documentation coverage — which areas are well-documented vs. gaps}

## Recommended Priority Actions

1. **{Action}** — fixes CRIT-001, CRIT-002 — {estimated effort: small/medium/large}
2. **{Action}** — fixes MAJ-001 through MAJ-003 — {effort}
3. ...
```

### Step 7: Present Results

Display a summary to the user:

```
Audit complete: {project-name}

  Documents reviewed: {N}
  Findings: {critical} critical, {major} major, {minor} minor, {info} info

  Report: {path-to-audit-report.md}

  Top 3 priority actions:
    1. {action} — {severity} — {effort}
    2. {action} — {severity} — {effort}
    3. {action} — {severity} — {effort}
```

Use `AskUserQuestion` to ask:
- **Fix mode**: Would you like me to fix any of these issues now?
  - Fix critical findings
  - Fix all findings (critical + major + minor)
  - Just the report, I'll fix manually
  - Fix specific findings (list IDs)

If the user wants fixes, proceed to Step 8.

### Step 8: Apply Fixes (Optional)

For each finding the user wants fixed:

1. Read the target document
2. Apply the fix described in the finding
3. Mark the finding as resolved in the report

**Rules for fixes:**
- Only modify the specific section cited in the finding
- Do NOT restructure or rewrite entire documents
- Do NOT add new documents — only fix existing ones
- If a fix requires information you don't have (e.g., the correct API signature), mark it as "needs manual review" instead of guessing
- After all fixes, re-run a quick validation to ensure fixes didn't introduce new issues

Update the audit report to mark resolved findings:
```markdown
### CRIT-001: {Finding title} [RESOLVED]
```

## Notes

1. **Scope flexibility**: The audit can target the current project, a sibling project, or any directory with docs
2. **Incremental audits**: If a previous `audit-report.md` exists, note which findings are new vs. recurring
3. **No false positives**: It's better to miss an issue than to report a non-issue. Every finding must have concrete evidence
4. **Respect existing structure**: The audit evaluates documentation as-is — it doesn't impose spec-forge's own document structure on projects that use different conventions
