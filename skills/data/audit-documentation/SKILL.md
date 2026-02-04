---
name: audit-documentation
description:
  Run a multi-stage parallel documentation audit with 18 specialized agents
---

# Multi-Stage Parallel Documentation Audit

**Version:** 2.0 **Total Agents:** 18 parallel agents across 5 stages + 1
synthesis stage

---

## Overview

This audit uses parallel agent execution across 6 stages to comprehensively
analyze documentation quality, accuracy, and lifecycle status. Each stage
produces JSONL output that feeds into the final synthesis.

**Output Directory:**
`docs/audits/single-session/documentation/audit-[YYYY-MM-DD]/`

---

## Pre-Audit Setup

**Step 0: Episodic Memory Search (Session #128)**

Before running documentation audit, search for context from past sessions:

```javascript
// Search for past documentation audit findings
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["documentation audit", "stale docs", "broken links"],
    limit: 5,
  });

// Search for doc structure decisions
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["DOCUMENTATION_STANDARDS", "tier", "lifecycle"],
    limit: 5,
  });
```

**Why this matters:**

- Compare against previous doc health metrics
- Identify recurring documentation gaps
- Track which docs were flagged for updates before
- Prevent re-flagging known orphans or intentional gaps

---

**Step 1: Create Output Directory**

```bash
AUDIT_DIR="docs/audits/single-session/documentation/audit-$(date +%Y-%m-%d)"
mkdir -p "$AUDIT_DIR"
echo "Audit output: $AUDIT_DIR"
```

**Step 2: Load False Positives Database**

Read `docs/audits/FALSE_POSITIVES.jsonl` and note patterns to exclude from
findings (filter by category: `documentation`).

**Step 3: Check Thresholds**

Run `npm run review:check` - proceed regardless of result (user invoked
intentionally).

---

## Stage 1: Inventory & Baseline (3 Parallel Agents)

Launch these 3 agents in parallel:

### Agent 1A: Document Inventory

**Task:** Build complete document catalog

```
Count all .md files by directory and tier:
- Root level: ROADMAP.md, README.md, etc.
- docs/: by subdirectory
- .claude/: skills, plans

Extract metadata from each:
- Version number (if present)
- Last Updated date (if present)
- Status field (if present)
- Word count

Output: ${AUDIT_DIR}/stage-1-inventory.md
Format: Markdown summary with counts and file list
```

### Agent 1B: Baseline Metrics

**Task:** Capture current state via existing tools

```bash
# Run these commands and capture output:
npm run docs:check > ${AUDIT_DIR}/baseline-docs-check.txt 2>&1
npm run docs:sync-check > ${AUDIT_DIR}/baseline-sync-check.txt 2>&1
npm run format:check -- docs/ > ${AUDIT_DIR}/baseline-format-check.txt 2>&1

# Check DOCUMENTATION_INDEX.md for orphans
grep -c "orphan" docs/DOCUMENTATION_INDEX.md || echo "0"
```

Output: `${AUDIT_DIR}/stage-1-baselines.md`

### Agent 1C: Link Extraction

**Task:** Build link graph for later stages

```
Extract from all .md files:
1. Internal links: [text](path.md) -> list with source file:line
2. External URLs: https://... -> list with source file:line
3. Anchor links: #section -> list with source file:line

Output: ${AUDIT_DIR}/stage-1-links.json
Schema:
{
  "internal": [{"source": "file.md", "line": 1, "target": "other.md", "text": "..."}],
  "external": [{"source": "file.md", "line": 1, "url": "https://...", "text": "..."}],
  "anchors": [{"source": "file.md", "line": 1, "anchor": "#section", "text": "..."}]
}
```

### Stage 1 Completion Audit

Before proceeding to Stage 2, verify:

- [ ] `stage-1-inventory.md` exists and is non-empty
- [ ] `stage-1-baselines.md` exists with metrics
- [ ] `stage-1-links.json` exists and is valid JSON
- [ ] Display summary: "Stage 1 Complete: X docs, Y internal links, Z external
      URLs"

---

## Stage 2: Link Validation (4 Parallel Agents)

Launch these 4 agents in parallel using Stage 1 outputs:

### Agent 2A: Internal Link Checker

**Task:** Verify internal .md links resolve

```
For each internal link from stage-1-links.json:
1. Check target file exists
2. If link has anchor (#section), verify heading exists in target
3. Detect circular references (A→B→C→A)

Output: ${AUDIT_DIR}/stage-2-internal-links.jsonl
JSONL schema per finding (JSONL_SCHEMA_STANDARD.md format):
{
  "category": "documentation",
  "title": "Broken internal link to target.md",
  "fingerprint": "documentation::source.md::broken-link-target",
  "severity": "S1|S2",
  "effort": "E0",
  "confidence": 90,
  "files": ["source.md:123"],
  "why_it_matters": "Broken links frustrate readers and indicate stale documentation",
  "suggested_fix": "Update link to correct path or remove if target no longer exists",
  "acceptance_tests": ["Link resolves correctly", "No 404 when clicking"],
  "evidence": ["target: path.md", "resolved: /full/path.md"]
}
```

### Agent 2B: External URL Checker

**Task:** HTTP HEAD requests to external URLs

```bash
# Use the new script for external link checking
npm run docs:external-links -- --output ${AUDIT_DIR}/stage-2-external-links.jsonl
```

Or manually check each URL from stage-1-links.json with:

- 10-second timeout
- Rate limiting (100ms between same domain)
- Cache results
- Flag: 404, 403, 5xx, timeouts, redirects

Output: `${AUDIT_DIR}/stage-2-external-links.jsonl`

### Agent 2C: Cross-Reference Validator

**Task:** Verify references to project artifacts

```
Check documentation references:
1. ROADMAP item references (P1.2, Phase 3, etc.) - do they exist?
2. PR/Issue references (#123) - format valid?
3. SESSION_CONTEXT references - files mentioned exist?
4. Skill/hook path references - paths valid?

Output: ${AUDIT_DIR}/stage-2-cross-refs.jsonl
```

### Agent 2D: Orphan & Connectivity

**Task:** Find disconnected documents

```
From stage-1-links.json, identify:
1. Docs with zero inbound links (orphans)
2. Docs with only broken outbound links
3. Isolated clusters (group of docs only linking to each other)

Exclude from orphan detection:
- README.md (entry point)
- Root-level canonical docs
- Archive docs

Output: ${AUDIT_DIR}/stage-2-orphans.jsonl
```

### Stage 2 Completion Audit

Before proceeding to Stage 3, verify:

- [ ] All 4 JSONL files exist
- [ ] Run schema validation:
      `node scripts/debt/validate-schema.js ${AUDIT_DIR}/stage-2-*.jsonl`
- [ ] Display summary: "Stage 2 Complete: X link issues found"

---

## Stage 3: Content Quality (4 Parallel Agents)

Launch these 4 agents in parallel:

### Agent 3A: Accuracy Checker

**Task:** Verify content matches codebase

```bash
# Use the new script for accuracy checking
node scripts/check-content-accuracy.js --output ${AUDIT_DIR}/stage-3-accuracy.jsonl
```

Checks:

- Version numbers match package.json
- File paths mentioned exist
- npm script references valid
- Code snippet syntax (basic validation)

Output: `${AUDIT_DIR}/stage-3-accuracy.jsonl`

### Agent 3B: Completeness Checker

**Task:** Check for missing/incomplete content

```
For each document, check:
1. Required sections present per tier:
   - Tier 1: Purpose, Version History
   - Tier 2: Purpose, Version History, AI Instructions
   - Tier 3+: Purpose, Status, Version History
2. No TODO/TBD/FIXME placeholders
3. No empty sections (heading with no content)
4. No stub documents (< 100 words, excluding code blocks)

Output: ${AUDIT_DIR}/stage-3-completeness.jsonl
```

### Agent 3C: Coherence Checker

**Task:** Check terminology and duplication

```
Analyze across all documents:
1. Terminology inconsistency:
   - "skill" vs "command" vs "slash command"
   - "agent" vs "subagent" vs "worker"
   - Collect all term usages, flag inconsistencies
2. Duplicate content:
   - Exact match: identical content blocks (>50 words)
   - Fuzzy match: 80%+ similarity (same topic, minor rewording)
3. Contradictory information (conflicting guidance for same task)

Output: ${AUDIT_DIR}/stage-3-coherence.jsonl
```

### Agent 3D: Freshness Checker

**Task:** Check for stale content

```bash
# Use the new script for placement/staleness
npm run docs:placement -- --output ${AUDIT_DIR}/stage-3-freshness.jsonl
```

Tier-specific staleness thresholds:

- Tier 1 (Canonical): >60 days
- Tier 2 (Foundation): >90 days
- Tier 3+ (Planning/Reference/Guides): >120 days

Additional checks:

- Outdated version references
- Deprecated terminology still used

Output: `${AUDIT_DIR}/stage-3-freshness.jsonl`

### Stage 3 Completion Audit

Before proceeding to Stage 4, verify:

- [ ] All 4 JSONL files exist
- [ ] Schema validation passes
- [ ] Display summary: "Stage 3 Complete: X content quality issues"

---

## Stage 4: Format & Structure (3 Parallel Agents)

Launch these 3 agents in parallel:

### Agent 4A: Markdown Lint

**Task:** Run markdownlint on all docs

```bash
# Note: docs:lint should lint all markdown locations:
# "*.md" "docs/**/*.md" ".claude/**/*.md"
npm run docs:lint > ${AUDIT_DIR}/markdownlint-raw.txt 2>&1

# Parse output into JSONL findings
# Each markdownlint violation becomes a finding
```

Convert violations to JSONL format in `${AUDIT_DIR}/stage-4-markdownlint.jsonl`

### Agent 4B: Prettier Compliance

**Task:** Check Prettier formatting

```bash
npm run format:check -- docs/ > ${AUDIT_DIR}/prettier-raw.txt 2>&1

# Parse output for files that need formatting
```

Convert violations to JSONL format in `${AUDIT_DIR}/stage-4-prettier.jsonl`

### Agent 4C: Structure Standards

**Task:** Check document structure conventions

````
For each document, verify:
1. Frontmatter present and valid (for skill docs)
2. Required headers per tier
3. Version history format (table with Version|Date|Description)
4. Table formatting consistency (aligned pipes)
5. Code block language tags (all ``` blocks have language)
6. Heading uniqueness (no duplicate headings in same doc)

Output: ${AUDIT_DIR}/stage-4-structure.jsonl
````

### Stage 4 Completion Audit

Before proceeding to Stage 5, verify:

- [ ] All 3 JSONL files exist
- [ ] Schema validation passes
- [ ] Display summary: "Stage 4 Complete: X format issues"

---

## Stage 5: Placement & Lifecycle (4 Parallel Agents)

Launch Agents 5A, 5B, 5C in parallel, then 5D sequentially after 5B completes:

### Agent 5A: Location Validator

**Task:** Check documents in correct directories

```
Verify placement rules:
- Plans → docs/plans/ or .planning/
- Archives → docs/archive/
- Templates → docs/templates/
- Audits → docs/audits/
- Tier 1 → root level
- Tier 2 → docs/ or root

Output: ${AUDIT_DIR}/stage-5-location.jsonl
```

### Agent 5B: Archive Candidate Finder (Surface-Level)

**Task:** Quick scan for archive candidates

```
Surface-level detection:
1. Completed plans not archived (status: completed)
2. Session handoffs > 30 days old
3. Old audit results (> 60 days, likely in MASTER_DEBT.jsonl already)
4. Plans not referenced in current ROADMAP.md

Output: ${AUDIT_DIR}/stage-5-archive-candidates-raw.jsonl
```

### Agent 5C: Cleanup Candidate Finder

**Task:** Find files that should be deleted/merged

```
Identify:
1. Exact duplicate files (same content hash)
2. Near-empty files (< 50 words)
3. Draft files > 60 days old
4. Temp/test files (names starting with temp, test, scratch)
5. Merge candidates (fragmented docs on same topic)

Output: ${AUDIT_DIR}/stage-5-cleanup-candidates.jsonl
```

### Agent 5D: Deep Lifecycle Analysis (Runs After 5B)

**Sequential dependency: Read 5B output first**

**Task:** Detailed analysis of archive candidates

```
For each candidate from stage-5-archive-candidates-raw.jsonl:
1. Read the actual document content
2. Determine original purpose
3. Assess current status:
   - Purpose met? (completed successfully)
   - Overtaken? (superseded by other work)
   - Deprecated? (no longer relevant)
4. Check if content was consumed:
   - Audit findings → in MASTER_DEBT.jsonl?
   - Plan outcomes → documented elsewhere?
5. Provide recommendation with justification

Output: ${AUDIT_DIR}/stage-5-lifecycle-analysis.jsonl
Extended schema:
{
  ...standard fields...,
  "purpose": "Original intent of the document",
  "status_reason": "Why marked for archive",
  "consumed_by": "Where content lives now (if applicable)",
  "recommendation": "ARCHIVE|DELETE|KEEP|MERGE_INTO:<target>"
}
```

### Stage 5 Completion Audit

Before proceeding to Stage 6, verify:

- [ ] All 4 JSONL files exist (5A, 5B raw, 5C, 5D analysis)
- [ ] Schema validation passes
- [ ] Display summary: "Stage 5 Complete: X lifecycle issues, Y archive
      candidates"

---

## Stage 6: Synthesis & Prioritization (Sequential)

This stage runs sequentially after all parallel stages complete.

### Step 6.1: Merge All Findings

```bash
# Combine all stage outputs
cat ${AUDIT_DIR}/stage-2-*.jsonl \
    ${AUDIT_DIR}/stage-3-*.jsonl \
    ${AUDIT_DIR}/stage-4-*.jsonl \
    ${AUDIT_DIR}/stage-5-location.jsonl \
    ${AUDIT_DIR}/stage-5-archive-candidates-raw.jsonl \
    ${AUDIT_DIR}/stage-5-cleanup-candidates.jsonl \
    ${AUDIT_DIR}/stage-5-lifecycle-analysis.jsonl > ${AUDIT_DIR}/all-findings-raw.jsonl
```

### Step 6.2: Deduplicate

**Input:** `${AUDIT_DIR}/all-findings-raw.jsonl` **Output:**
`${AUDIT_DIR}/all-findings-deduped.jsonl`

```
Remove duplicates where same file:line appears from multiple agents.
Keep the finding with:
1. Higher severity
2. Higher confidence
3. More evidence items
```

### Step 6.3: Cross-Reference FALSE_POSITIVES.jsonl

**Input:** `${AUDIT_DIR}/all-findings-deduped.jsonl` **Output:**
`${AUDIT_DIR}/all-findings.jsonl` (final file for TDMS intake)

```
Filter out findings matching patterns in docs/audits/FALSE_POSITIVES.jsonl:
- Match by file pattern
- Match by title pattern
- Check expiration dates
```

### Step 6.4: Priority Scoring

```
For each finding, calculate priority:

priority = (severityWeight × categoryMultiplier × confidenceWeight) / effortWeight

Where:
- severityWeight: S0=100, S1=50, S2=20, S3=5
- categoryMultiplier: links=1.5, accuracy=1.3, freshness=1.0, format=0.8
- confidenceWeight: HIGH=1.0, MEDIUM=0.7, LOW=0.4
- effortWeight: E0=1, E1=2, E2=4, E3=8

Sort findings by priority descending.
```

### Step 6.5: Generate Action Plan

```
Create three queues:

1. IMMEDIATE FIXES (S0/S1, E0/E1):
   - List with specific file:line and fix command

2. ARCHIVE QUEUE:
   - node scripts/archive-doc.js commands for each candidate

3. DELETE/MERGE QUEUE:
   - Justification for each deletion
   - Merge target for consolidations
```

### Step 6.6: Generate Final Report

Output: `${AUDIT_DIR}/FINAL_REPORT.md`

````markdown
# Documentation Audit Report - [DATE]

## Executive Summary

- **Total findings:** X
- **By severity:** S0: X, S1: X, S2: X, S3: X
- **By category:** Links: X, Content: X, Format: X, Lifecycle: X
- **False positives filtered:** X

## Baseline Comparison

| Metric               | Before | After Fixes |
| -------------------- | ------ | ----------- |
| docs:check errors    | X      | -           |
| docs:sync issues     | X      | -           |
| Orphaned docs        | X      | -           |
| Stale docs (>90 day) | X      | -           |

## Top 20 Priority Items

| #   | Severity | File | Issue | Effort |
| --- | -------- | ---- | ----- | ------ |
| 1   | S1       | ...  | ...   | E0     |

## Stage-by-Stage Breakdown

### Stage 2: Link Validation

- Internal link errors: X
- External link errors: X
- Orphaned documents: X

### Stage 3: Content Quality

- Accuracy issues: X
- Completeness issues: X
- Coherence issues: X
- Freshness issues: X

### Stage 4: Format & Structure

- Markdownlint violations: X
- Prettier violations: X
- Structure issues: X

### Stage 5: Lifecycle

- Location issues: X
- Archive candidates: X
- Cleanup candidates: X

## Action Plan

### Immediate Fixes (Do Now)

1. `file.md:line` - Fix description

### Archive Queue

```bash
node scripts/archive-doc.js "path/to/doc.md"
```
````

### Cleanup Queue

- DELETE: `path/to/temp-file.md` (reason)
- MERGE: `fragmented.md` → `main-doc.md`

## Recommendations

1. ...
2. ...

---

## Post-Audit Actions

### 1. Save Outputs

Verify all files saved to `${AUDIT_DIR}/`:

- [ ] stage-1-\*.md, stage-1-links.json
- [ ] stage-2-\*.jsonl
- [ ] stage-3-\*.jsonl
- [ ] stage-4-\*.jsonl
- [ ] stage-5-\*.jsonl
- [ ] all-findings.jsonl (merged, deduplicated)
- [ ] FINAL_REPORT.md

### 2. TDMS Integration

```bash
node scripts/debt/intake-audit.js ${AUDIT_DIR}/all-findings.jsonl --source "audit-documentation-$(date +%Y-%m-%d)"
```

### 3. Update AUDIT_TRACKER.md

Add entry to "Documentation Audits" table:

| Date    | Session | Commits | Files | Findings  | Confidence | Validation |
| ------- | ------- | ------- | ----- | --------- | ---------- | ---------- |
| [today] | [#]     | [X]     | [Y]   | [summary] | HIGH       | PASSED     |

### 4. Reset Threshold

Single-session audits reset the documentation category threshold.

### 5. Offer Fixes

Ask user: "Would you like me to fix any immediate items now?"

---

## Category Mapping for TDMS

| Stage         | Category ID Prefix | TDMS Category |
| ------------- | ------------------ | ------------- |
| 2 - Links     | DOC-LINK-\*        | documentation |
| 3 - Content   | DOC-CONTENT-\*     | documentation |
| 4 - Format    | DOC-FORMAT-\*      | documentation |
| 5 - Lifecycle | DOC-LIFECYCLE-\*   | documentation |

---

## Recovery Procedures

### If Stage Fails

1. **Missing output file:** Re-run specific agent with explicit file write
2. **Empty output file:** Check agent for errors, re-run with verbose
3. **Schema validation fails:** Parse errors line-by-line, fix malformed
4. **Context compaction:** Verify AUDIT_DIR path, re-run from last checkpoint

### If Context Compacts Mid-Audit

Read the partial outputs already saved to `${AUDIT_DIR}/` and resume from the
last completed stage.

---

## Multi-AI Escalation

After 3 single-session documentation audits, a full multi-AI Documentation Audit
is recommended. Track in AUDIT_TRACKER.md "Single audits completed" counter.

---

## Update Dependencies

When modifying this skill, also update:

| Document                                                  | Section                        |
| --------------------------------------------------------- | ------------------------------ |
| `docs/templates/MULTI_AI_DOCUMENTATION_AUDIT_TEMPLATE.md` | Sync category list             |
| `docs/SLASH_COMMANDS_REFERENCE.md`                        | /audit-documentation reference |

---

## Version History

| Version | Date       | Description                                             |
| ------- | ---------- | ------------------------------------------------------- |
| 2.0     | 2026-02-02 | Complete rewrite: 6-stage parallel audit with 18 agents |
| 1.0     | 2025-xx-xx | Original single-session sequential audit                |

---

## Documentation References

Before running this audit, review:

### TDMS Integration (Required)

- [PROCEDURE.md](docs/technical-debt/PROCEDURE.md) - Full TDMS workflow
- [MASTER_DEBT.jsonl](docs/technical-debt/MASTER_DEBT.jsonl) - Canonical debt
  store
- Intake command:
  `node scripts/debt/intake-audit.js <output.jsonl> --source "audit-documentation-<date>"`

### Documentation Standards (Critical for This Audit)

- [JSONL_SCHEMA_STANDARD.md](docs/templates/JSONL_SCHEMA_STANDARD.md) - Output
  format requirements and TDMS field mapping
- [DOCUMENTATION_STANDARDS.md](docs/DOCUMENTATION_STANDARDS.md) - **The
  canonical guide** this audit validates against (5-tier hierarchy, metadata
  requirements, quality protocols)
