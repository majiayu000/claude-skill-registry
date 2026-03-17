---
name: editing-claude
description: |
  Validate and optimize CLAUDE.md files using Anthropic's best practices for focused sessions.
  Detects contradictions, redundancy, excessive length (200+ lines), emphasis overuse (2%+ density),
  broken links, and orphaned sections. Scores health 0-50 points. Suggests safe automated fixes
  and extraction opportunities. Use when editing CLAUDE.md, before commits, when document grows
  past 200 lines, user says "optimize CLAUDE.md", "check contradictions", "validate documentation",
  or during quarterly reviews. Works with project and global CLAUDE.md files (.md extension).
  Based on Anthropic 2025 context engineering best practices.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Edit
  - MultiEdit
---

# editing-claude

Validate and optimize CLAUDE.md files to maintain focus and effectiveness.

## Purpose

This skill validates CLAUDE.md files against Anthropic's best practices, detects quality issues (contradictions, redundancy, excessive length, emphasis overuse), and suggests safe automated fixes or extraction strategies. Based on comprehensive research into context engineering best practices.

## Table of Contents

### Core Sections
- [When to Use](#when-to-use) - Explicit, implicit, and file type triggers
- [What This Skill Does](#what-this-skill-does) - 8-step workflow and health scoring
- [Instructions](#instructions) - Complete implementation guide
  - [Step 1: Discover CLAUDE.md Files](#step-1-discover-claudemd-files) - Find global, project, and local files
  - [Step 2: Analyze Structure](#step-2-analyze-structure) - Parse headings, measure sections, detect orphans
  - [Step 3: Analyze Emphasis Usage](#step-3-analyze-emphasis-usage) - Count MUST/NEVER/ALWAYS markers
  - [Step 4: Detect Redundancy](#step-4-detect-redundancy) - Intra-file and cross-file duplication
  - [Step 5: Detect Contradictions](#step-5-detect-contradictions) - Find conflicting directives
  - [Step 6: Identify Extraction Opportunities](#step-6-identify-extraction-opportunities) - Content for specialized docs
  - [Step 7: Validate Links](#step-7-validate-links) - Check internal/external links
  - [Step 8: Generate Health Report](#step-8-generate-health-report) - Compile comprehensive analysis
- [Safe Automated Fixes](#safe-automated-fixes) - Fixes that can be applied automatically
  - [Fix 1: Remove Cross-File Redundancy](#fix-1-remove-cross-file-redundancy) - Replace duplication with references
  - [Fix 2: Fix Broken Links](#fix-2-fix-broken-links) - Update links to correct paths
  - [Fix 3: Fix Orphaned Sections](#fix-3-fix-orphaned-sections) - Promote or nest sections
  - [Fix 4: Reduce Emphasis Density](#fix-4-reduce-emphasis-density-2) - Remove redundant emphasis
- [Examples](#examples) - Real-world usage scenarios
- [Validation](#validation) - Verify skill execution and outcomes
- [Integration Points](#integration-points) - Quality gates, git workflow, documentation reviews

### Advanced Topics
- [Supporting Files](#supporting-files) - Scripts, templates, and references
- [Red Flags](#red-flags) - Common mistakes to avoid
- [Troubleshooting](#troubleshooting) - Common issues and fixes
- [Requirements](#requirements) - Python, bash tools, and dependencies

### Supporting Resources
- [Reference](references/reference.md) - Anthropic best practices, algorithms, validation checklist
- [Examples](examples/examples.md) - Quarterly review, redundancy fixes, extraction strategy

## Quick Start

**Analyze current CLAUDE.md:**
```bash
Skill(command: "editing-claude")
```

**Expected output:** Health report (0-50 score), issues found (critical/warning/info), extraction opportunities, automated fixes available.

## When to Use

**Explicit Triggers:**
- "Edit CLAUDE.md"
- "Optimize CLAUDE.md"
- "Check for contradictions in CLAUDE.md"
- "Validate documentation"
- "CLAUDE.md is too long"

**Implicit Triggers:**
- Before committing CLAUDE.md changes
- Document exceeds 200 lines (warn at 200, error at 500)
- Quarterly documentation reviews
- After adding new rules/sections

**File Types:**
- CLAUDE.md (project or global)
- .claude/*.md (specialized docs)
- *.CLAUDE.md (local overrides)

## What This Skill Does

**8-Step Workflow:**

1. **Discovery** - Find all CLAUDE.md files (global, project, local)
2. **Structure Analysis** - Parse headings, measure sections, detect orphans
3. **Emphasis Analysis** - Count MUST/NEVER/ALWAYS/MANDATORY/CRITICAL markers
4. **Redundancy Detection** - Find duplicate content (intra-file and cross-file)
5. **Contradiction Detection** - Find conflicting directives
6. **Extraction Opportunities** - Identify content for specialized docs
7. **Link Validation** - Verify all internal/external links
8. **Report & Recommendations** - Generate health score with prioritized fixes

**Health Score Components (50 points):**
- Length: 10 points (100-200 lines = 10, >500 = 0)
- Emphasis Density: 10 points (<1% = 10, >2% = 0)
- Contradictions: 10 points (0 = 10, >3 = 0)
- Redundancy: 10 points (0 instances = 10, >5 = 0)
- Links: 5 points (all valid = 5)
- Structure: 5 points (no orphans = 5)
- Extraction Potential: 5 points (<20% = 5)
- Freshness: 5 points (updated <30 days = 5)

## Instructions

### Step 1: Discover CLAUDE.md Files

**Find all CLAUDE.md files in hierarchy:**

```bash
# Global CLAUDE.md
test -f ~/.claude/CLAUDE.md && echo "Global: ~/.claude/CLAUDE.md" || echo "No global"

# Project CLAUDE.md
test -f ./CLAUDE.md && echo "Project: ./CLAUDE.md" || echo "No project"

# Get line counts
wc -l ~/.claude/CLAUDE.md ./CLAUDE.md 2>/dev/null
```

**Read the target CLAUDE.md file (usually project).**

### Step 2: Analyze Structure

**Extract headings and calculate section lengths:**

```bash
# Extract all headings with line numbers
grep -n "^#" ./CLAUDE.md

# Count sections
grep -c "^## " ./CLAUDE.md  # H2 sections
grep -c "^### " ./CLAUDE.md  # H3 subsections
```

**Use Python script for detailed analysis:**

```bash
python .claude/skills/editing-claude/scripts/analyze_structure.py ./CLAUDE.md
```

**Detect issues:**
- Document >200 lines (warning), >500 lines (error)
- Sections >100 lines (suggest extraction)
- Orphaned sections (H3 without H2 parent)
- Heading hierarchy skips (H1 → H3 without H2)

### Step 3: Analyze Emphasis Usage

**Extract emphasis markers:**

```bash
# Find all CRITICAL/MANDATORY/MUST/NEVER/ALWAYS instances
grep -n "\(CRITICAL\|MANDATORY\|MUST\|NEVER\|ALWAYS\)" ./CLAUDE.md
```

**Calculate emphasis density:**

```bash
python .claude/skills/editing-claude/scripts/analyze_emphasis.py ./CLAUDE.md
```

**Thresholds:**
- <1%: ✅ Optimal (restrained)
- 1-2%: ✅ Acceptable (within range)
- 2-5%: ⚠️ Warning (overuse)
- >5%: ❌ Error (nothing is critical)

### Step 4: Detect Redundancy

**Intra-file redundancy (same file):**

Run semantic similarity analysis:

```bash
python .claude/skills/editing-claude/scripts/detect_redundancy.py ./CLAUDE.md
```

**Distinguish redundancy from reinforcement:**
- **Redundancy:** Exact duplication in same context → Fix
- **Reinforcement:** Same info in escalating contexts (catalog → section → checklist) → Keep

**Cross-file redundancy (global vs project):**

```bash
python .claude/skills/editing-claude/scripts/detect_redundancy.py ~/.claude/CLAUDE.md ./CLAUDE.md
```

**Common redundant rules:**
- MultiEdit requirement
- Testing philosophy
- Critical thinking principle

**Fix:** Replace project duplication with reference to global.

### Step 5: Detect Contradictions

**Run semantic contradiction analysis:**

```bash
python .claude/skills/editing-claude/scripts/detect_contradictions.py ./CLAUDE.md
```

**Contradiction patterns:**
- Direct opposition: "ALWAYS use X" + "NEVER use X"
- Priority conflicts: "X is critical" + "X is optional"
- Conflicting delegation: Multiple agents for same task
- Tool preference conflicts: Skill vs direct tool (check if conditional)

**Validation:** Check if apparent contradictions are actually conditional fallbacks (not true contradictions).

### Step 6: Identify Extraction Opportunities

**Analyze each section:**

```bash
python .claude/skills/editing-claude/scripts/identify_extractions.py ./CLAUDE.md
```

**Extraction criteria:**
- Section >50 lines
- Detailed how-to content (should be in guide)
- Low-frequency content (edge cases)
- Catalog-style content (lists of items)

**Common extraction targets:**
- Skills Catalog (if >40 lines) → .claude/docs/skills-index.md
- Workflow details → .claude/docs/workflow-guides.md
- Anti-pattern details → .claude/docs/enforcement-guide.md
- Agent reference → ../orchestrate-agents/references/dispatch.md (if not already there)

**Keep in CLAUDE.md:**
- 5 most critical items from each catalog
- Core principles (not implementation details)
- Links to specialized docs

### Step 7: Validate Links

**Extract and validate all links:**

```bash
python .claude/skills/editing-claude/scripts/validate_links.py ./CLAUDE.md
```

**Check:**
- Internal links (file exists)
- Relative paths (not absolute)
- External links (HTTP 200) - optional
- Link text descriptive (not "click here")

**Fix broken links automatically (safe operation).**

### Step 8: Generate Health Report

**Compile all analyses into comprehensive report:**

```bash
python .claude/skills/editing-claude/scripts/generate_report.py ./CLAUDE.md
```

**Report format:**

```markdown
# CLAUDE.md Health Report

**Overall Score: X/50** 🟢 EXCELLENT | 🟡 GOOD | 🟠 NEEDS WORK | 🔴 CRITICAL

## Issues Found

### 🔴 Critical (Fix Immediately)
- [Issue with line numbers and fix]

### 🟠 High Priority (Fix Soon)
- [Issue with line numbers and fix]

### 🟡 Medium Priority (Improve)
- [Issue with line numbers and suggestion]

### 🟢 Low Priority (Optional)
- [Issue with line numbers and suggestion]

## Extraction Opportunities
- [Section] (X lines) → [target-file.md]

## Automated Fixes Available
- [ ] Fix 1 (safe, low-risk)
- [ ] Fix 2 (requires review)

## Recommendations
1. [Priority action]
2. [Next action]
3. [Future improvement]
```

**Write report to `.claude/artifacts/YYYY-MM-DD/reports/claude-md-health-report.md`.**
- Use `reports/` subfolder for health reports
- If multiple reports exist for same topic, group in topic subfolder (e.g., `reports/claude-md-optimization/`)

## Safe Automated Fixes

The following fixes can be applied automatically (with --apply flag):

### Fix 1: Remove Cross-File Redundancy

**When:** Same rule in global and project CLAUDE.md

**Action:** Replace project duplication with reference to global

```markdown
# Before (project CLAUDE.md)
### Token Optimization (MultiEdit Required)
[13 lines of MultiEdit explanation]

# After
### Token Optimization
**Global Rule:** See [~/.claude/CLAUDE.md](~/.claude/CLAUDE.md) for MultiEdit requirement
```

**Validation:** Ensure global CLAUDE.md exists and contains the rule.

### Fix 2: Fix Broken Links

**When:** Internal link points to non-existent file

**Action:** Update link to correct path OR remove if file truly missing

**Validation:** File exists at new path AND content matches expected.

### Fix 3: Fix Orphaned Sections

**When:** H3 section without H2 parent

**Action:** Promote to H2 OR nest under appropriate existing H2

**Validation:** Requires semantic understanding - **ASK USER** for confirmation.

### Fix 4: Reduce Emphasis Density (>2%)

**When:** Too many CRITICAL/MANDATORY markers

**Action:** Remove redundant emphasis (e.g., heading + body both have emphasis)

**Validation:** Meaning preserved, emphasis still clear.

## Examples

### Python Examples

- [analyze_structure.py](./scripts/analyze_structure.py) - Parse headings, measure sections, detect orphans
- [analyze_emphasis.py](./scripts/analyze_emphasis.py) - Extract MUST/NEVER/ALWAYS, calculate density
- [validate_links.py](./scripts/validate_links.py) - Link extraction, existence checking
- [generate_report.py](./scripts/generate_report.py) - Compile analyses into comprehensive report

### Complete Walkthroughs

See [examples/examples.md](./examples/examples.md) for:
- Example 1: Quarterly Review - Full analysis workflow
- Example 2: Fixing Redundancy - Cross-file duplication
- Example 3: Extraction Strategy - Skills Catalog extraction
- Example 4: Contradiction Resolution - Detecting conflicts
- Example 5: Length Optimization - 502 → 250 lines
- Example 6: Emergency Fix - Broken links and orphans

## Supporting Files

- **scripts/analyze_structure.py** - Parse headings, measure sections, detect orphans
- **scripts/analyze_emphasis.py** - Extract MUST/NEVER/ALWAYS, calculate density
- **scripts/validate_links.py** - Link extraction, existence checking
- **scripts/generate_report.py** - Compile analyses into comprehensive report
- **examples/examples.md** - Comprehensive examples and use cases
- **templates/extraction-template.md** - Template for creating specialized docs
- **templates/report-template.md** - Template for health report
- **references/reference.md** - Technical depth on algorithms and best practices

## Validation

**Verify skill execution:**

1. **Health score calculated:** 0-50 range
2. **All 8 analyses run:** Structure, emphasis, redundancy, contradictions, extraction, links, freshness, report
3. **Report generated:** Saved to `.claude/artifacts/YYYY-MM-DD/reports/`
4. **No false positives:** Reinforcement not flagged as redundancy
5. **Safe fixes only:** No destructive operations without confirmation

**Expected outcomes:**
- ✅ Report shows health score matching manual assessment
- ✅ Extraction suggestions align with research (e.g., 191 lines identified in Phase 2)
- ✅ No false positives on current CLAUDE.md (0 contradictions expected)
- ✅ Automated fixes apply without breaking links

## Integration Points

**With Quality Gates:**
- Run before committing CLAUDE.md changes
- Warn if health score <40 (FAIR threshold)

**With Git Workflow:**
- Pre-commit hook validates CLAUDE.md
- Blocks if health score <30 (POOR threshold)

**With Documentation Reviews:**
- Quarterly review using this skill
- Track health score over time

**With Skill Creator:**
- Detects when Skills Catalog grows >40 lines
- Recommends extraction to skills-index.md

## Red Flags

**Common mistakes when using this skill:**

1. ❌ **Auto-apply extraction without review** → Always get user approval first
2. ❌ **Flag reinforcement as redundancy** → Check if same info in different contexts
3. ❌ **Flag conditional fallbacks as contradictions** → Validate context
4. ❌ **Break links during fix** → Verify target file exists AND content matches
5. ❌ **Remove emphasis from Core Rules** → Some sections SHOULD have emphasis
6. ❌ **Ignore project-specific patterns** → Adapt recommendations to project needs
7. ❌ **No rollback plan** → Create git commit before applying fixes
8. ❌ **Overwhelming reports** → Prioritize (critical → warning → info)
9. ❌ **No A/B testing** → Measure Claude adherence before/after changes
10. ❌ **Assume extraction preserves effectiveness** → Test impact on adherence

## Troubleshooting

**Issue:** Script not found
- **Fix:** Ensure scripts/ directory exists with all Python files
- **Check:** `ls .claude/skills/editing-claude/scripts/`

**Issue:** False positive contradictions
- **Fix:** Check if statements are conditional (if-then logic)
- **Manual review:** Validate semantic analysis

**Issue:** Health score seems wrong
- **Fix:** Check scoring algorithm in scripts/generate_report.py
- **Validate:** Manual calculation vs automated

**Issue:** Extraction suggestions break document
- **Fix:** Keep 80% of high-frequency content in CLAUDE.md
- **Test:** Measure Claude adherence before/after extraction

**Issue:** Links break after fixes
- **Fix:** Validate all links after applying fixes
- **Rollback:** `git checkout CLAUDE.md` if needed

## Requirements

**Python 3.8+** with standard library:
- `re` (regex)
- `os` (file operations)
- `sys` (arguments)
- `pathlib` (path handling)

**Bash tools:**
- `grep` (pattern matching)
- `wc` (line counting)
- `test` (file existence)

**Claude Code tools:**
- Read, Write, Grep, Glob, Bash, Edit, MultiEdit

**Optional:**
- `git` (for rollback, history analysis)
- `markdownlint` (markdown validation)

## See Also

- [reference.md](./references/reference.md) - Anthropic best practices, algorithms, validation checklist
- [examples.md](./examples/examples.md) - Real-world usage scenarios
- [Anthropic Context Engineering Best Practices](https://docs.anthropic.com/) - Official guidance
- [../manage-session-workspace/references/session-workspace-guidelines.md](../../docs/session-workspace-guidelines.md) - Where to save reports
- [research artifacts](../../artifacts/2025-10-19/sessions/07-37-claude-md-skill-research/) - Full research findings
