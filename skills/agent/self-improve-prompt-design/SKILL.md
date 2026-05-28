---
name: self-improve-prompt-design
description: Write self-improve prompts that sync expertise files with codebase reality. Use when creating maintenance workflows for agent experts, designing validation logic, or implementing the LEARN step of Act-Learn-Reuse.
allowed-tools: Read, Grep, Glob, Write
---

# Self-Improve Prompt Design

Guide for writing self-improve prompts that maintain expertise file accuracy.

## Core Purpose

Self-improve prompts teach agents HOW to learn. They:

- Validate expertise against actual codebase (source of truth)
- Identify drift between mental model and reality
- Update expertise files automatically
- Enforce line limits to prevent context bloat
- Run after every ACT step in Act-Learn-Reuse

## When to Use

- Creating maintenance workflows for agent experts
- Designing validation logic for expertise files
- Implementing the LEARN step of Act-Learn-Reuse
- Writing self-improve prompts for new domains
- Reviewing or debugging existing self-improve prompts
- Setting up git diff conditional checks for efficiency

## Self-Improve Prompt Template

````markdown
---
description: Sync {domain} expertise with codebase reality
argument-hint: [check-git-diff]
---

# Self-Improve: {Domain} Expert

Maintain expertise accuracy by validating against codebase implementation.

## Arguments

- `$1`: check_git_diff flag (optional, default: "true")
  - "true": Only check files changed in git diff
  - "false": Full rescan of all domain files

## Configuration

- **EXPERTISE_FILE**: `.claude/commands/experts/{domain}/expertise.yaml`
- **MAX_LINES**: 1000
- **DOMAIN_PATHS**: ["path/to/domain/files/"]

## Workflow

### Step 1: Check Git Diff (Conditional)

If `$1` is "true" or not provided:

1. Run `git diff --name-only HEAD~1` to get changed files
2. Filter to files in DOMAIN_PATHS
3. If no relevant changes, report "No domain changes detected" and exit
4. Continue with changed files only

If `$1` is "false":
- Skip git diff check
- Process all files in DOMAIN_PATHS

### Step 2: Read Current Expertise

1. Load EXPERTISE_FILE
2. Parse YAML structure
3. Note current line count
4. Identify sections present

### Step 3: Validate Against Codebase

For each section in expertise:

**core_implementation:**
- Verify all file paths exist
- Check line counts are approximately correct
- Confirm key exports still exist

**key_operations:**
- Verify function names exist
- Check signatures match
- Validate file locations

**schema_structure:** (if applicable)
- Compare against actual schema definitions
- Check field names and types

**best_practices:**
- Ensure still relevant to current patterns

**known_issues:**
- Check if any resolved
- Look for new issues in domain

### Step 4: Identify Discrepancies

Create a list of findings:

| Section | Issue | Action |
| --- | --- | --- |
| core_implementation | file.ext renamed | Update path |
| key_operations | new function added | Add entry |
| known_issues | issue #123 resolved | Remove entry |

### Step 5: Update Expertise File

Apply changes:

1. Update outdated information
2. Add new discoveries
3. Remove stale entries
4. Maintain YAML structure

### Step 6: Enforce Line Limit

If line count > MAX_LINES:

1. Identify lowest priority sections
2. Summarize verbose entries
3. Remove least critical items
4. Continue until under limit

Priority order (highest to lowest):
1. core_implementation
2. key_operations
3. best_practices
4. known_issues
5. patterns_and_conventions
6. testing_notes

### Step 7: Validation Check

1. Parse updated YAML (ensure valid syntax)
2. Verify line count: {current}/{MAX_LINES}
3. Run quick sanity checks on paths/names

## Output Report

```markdown
## Self-Improve Complete: {domain}

### Summary
- Files scanned: X
- Changes detected: Y
- Updates applied: Z

### Changes Made
| Section | Change | Reason |
| --- | --- | --- |
| ... | ... | ... |

### Expertise Health
| Metric | Value |
| --- | --- |
| Line count | X/1000 |
| Files validated | X/X exist |
| Functions verified | X/X accurate |
| Schema accuracy | X% |

### Recommendations
- [Any manual review suggestions]
```

## Notes

- Mental model is NOT source of truth - codebase is
- Run after every ACT (build, fix, modify)
- Check git diff by default to save time
- Full rescan periodically or when drift suspected
````

## Key Design Principles

### 1. Conditional Git Diff Check

Always include git diff optimization:

```markdown
If check_git_diff is true:
  - Only process changed files
  - Exit early if no relevant changes
  - Saves time on routine syncs
```

### 2. Line Limit Enforcement

Must be explicit and prioritized:

```markdown
MAX_LINES: 1000

If over limit:
  1. Summarize verbose sections
  2. Remove lowest priority items
  3. Never exceed limit
```

### 3. Validation Before Update

Always validate before writing:

```markdown
Before writing updated expertise:
  1. Parse as YAML (catch syntax errors)
  2. Count lines
  3. Verify critical paths exist
```

### 4. Actionable Output

Report should enable follow-up:

```markdown
## Changes Made
| Section | Change | Reason |
| --- | --- | --- |

## Recommendations
- Items requiring human review
- Potential issues to investigate
```

## Validation Patterns

### File Path Validation

```markdown
For each file path in expertise:
  1. Check if file exists at path
  2. If not, search for file by name
  3. If found elsewhere, update path
  4. If not found, mark for removal
```

### Function Validation

```markdown
For each function in key_operations:
  1. Search file for function definition
  2. Compare signature if found
  3. Update or flag discrepancy
```

### Schema Validation

```markdown
For each table/entity in schema_structure:
  1. Find schema definition file
  2. Compare fields and types
  3. Note additions/removals
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| No git diff option | Wastes time on no-ops | Always include conditional check |
| No line limit | Context overflow | Enforce MAX_LINES strictly |
| Silent failures | Drift undetected | Report all validation results |
| Manual edits | Human time wasted | Self-improve only updates |
| No validation | Bad YAML written | Always parse before save |

## Integration with Act-Learn-Reuse

```text
┌─────────────────────────────────────────────┐
│ ACT: Build, Fix, or Answer                  │
│      (Agent performs useful work)           │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ LEARN: Self-Improve Prompt                  │
│      • Check git diff                       │
│      • Validate expertise against code      │
│      • Update mental model                  │
│      • Enforce line limits                  │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ REUSE: Next Execution                       │
│      (Agent reads updated expertise first)  │
└─────────────────────────────────────────────┘
```

## Testing Self-Improve Prompts

To validate a self-improve prompt works correctly:

1. **Initial state**: Run against seeded expertise
2. **Introduce change**: Modify a file in domain
3. **Run self-improve**: Check it detects change
4. **Verify update**: Confirm expertise updated correctly
5. **Line limit test**: Add content until limit hit, verify truncation

## Related Skills

- `expertise-file-design`: Structure of expertise files
- `agent-expert-creation`: Full agent expert workflow
- `meta-agentic-creation`: Self-improving at scale

---

**Last Updated:** 2025-12-15

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
