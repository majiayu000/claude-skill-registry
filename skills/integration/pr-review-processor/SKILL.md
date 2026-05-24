---
name: pr-review-processor
description:
  Comprehensive AI code review processor for CodeRabbit and Qodo feedback.
  Handles 50-3000+ line reviews with multi-pass verification, mandatory learning
  capture, and full issue resolution. Use when processing any AI-generated code
  review feedback.
---

# PR Review Processor

Standardized protocol for processing AI code review feedback with maximum
thoroughness and complete issue resolution.

## When to Use This Skill

- Processing CodeRabbit PR comments/suggestions
- Processing CodeRabbit CLI output
- Processing Qodo compliance reviews
- Processing Qodo PR suggestions
- Any AI-generated code review feedback (50-3000+ lines)

## Core Principles

1. **Fix Everything** - Including trivial items
2. **Learning First** - Create log entry before fixes
3. **Multi-Pass Verification** - Never miss an issue
4. **Agent Augmentation** - Invoke specialists when needed
5. **Full Documentation** - Every decision tracked

---

## Protocol Overview

```
INPUT (Raw Review)
    ↓
PARSE (Multi-pass extraction)
    ↓
CATEGORIZE (Critical/Major/Minor/Trivial)
    ↓
PLAN (TodoWrite all items)
    ↓
CONTEXT (Load AI_REVIEW_PROCESS.md, learnings log, claude.md)
    ↓
LEARNING STUB (Create entry FIRST)
    ↓
AGENTS (Invoke specialists per issue type)
    ↓
FIX (Priority order, verify each)
    ↓
VERIFY (Multi-pass confirmation)
    ↓
DOCUMENT (Complete learning entry)
    ↓
COMMIT (Following project conventions)
```

---

## Detailed Protocol

### Phase 1: Intake & Parsing

**For large reviews (500+ lines), use multi-pass parsing:**

**Pass 1 - Header Extraction:**

- Scan for issue markers: "suggestion", "issue", "warning", "error", "nitpick",
  "improvement"
- Extract file paths and line numbers
- Create skeleton list

**Pass 2 - Detail Extraction:**

- For each identified issue, extract:
  - Full description
  - Code snippets (before/after if provided)
  - Severity indicators
  - Suggested fixes

**Pass 3 - Verification:**

- Re-scan entire input
- Compare against extracted list
- Catch any missed items

**Output:** Numbered master list with all issues

### Phase 2: Categorization

Use the categorization matrix from `AI_REVIEW_PROCESS.md`:

| Severity     | Examples                                    | This Protocol's Action |
| ------------ | ------------------------------------------- | ---------------------- |
| **CRITICAL** | Security holes, data loss, breaking changes | Fix immediately        |
| **MAJOR**    | Bugs, performance, missing validation       | Fix before proceeding  |
| **MINOR**    | Style, naming, tests, docs                  | **Fix** (not defer)    |
| **TRIVIAL**  | Typos, whitespace, comments                 | **Fix** (not skip)     |

### Phase 3: Planning with TodoWrite

Create comprehensive todo list:

```javascript
todos: [
  {
    content: "Add Review #N stub to AI_REVIEW_LEARNINGS_LOG.md",
    status: "in_progress",
    activeForm: "Adding Review #N stub to learnings log",
  },
  // ALL issues, including trivial
  {
    content: "Fix [SEVERITY]: [description] in [file]",
    status: "pending",
    activeForm: "Fixing [SEVERITY]: [description]",
  },
];
```

### Phase 4: Context Loading

**Automatically read:**

1. `AI_REVIEW_PROCESS.md` - Full process
2. `AI_REVIEW_LEARNINGS_LOG.md` (first 200 lines) - Recent patterns
3. `claude.md` Section 4 - Anti-patterns to avoid

### Phase 5: Agent Invocation

| Issue Domain             | Agent                  | Invocation                         |
| ------------------------ | ---------------------- | ---------------------------------- |
| Security vulnerabilities | `security-auditor`     | Task tool with security issues     |
| Test gaps                | `test-engineer`        | Task tool with test requirements   |
| Performance              | `performance-engineer` | Task tool with perf issues         |
| Documentation            | `technical-writer`     | Task tool with doc issues          |
| Complex debugging        | `debugger`             | Task tool with bug context         |
| Architecture             | `backend-architect`    | Task tool with design concerns     |
| Frontend issues          | `frontend-developer`   | Task tool with UI/component issues |

**Invoke in parallel when possible** - Multiple agents can work simultaneously
on different issue types.

### Phase 6: Issue Resolution

**Priority Order:**

1. CRITICAL (separate commits if needed)
2. MAJOR (batch by area)
3. MINOR (batch by file)
4. TRIVIAL (batch all)

**For each issue:**

1. Read the target file
2. Understand surrounding context
3. Apply fix
4. Verify no regressions
5. Mark todo complete

### Phase 7: Verification Passes

**Pass 1 - File Review:**

- Re-read each modified file
- Check for introduced issues

**Pass 2 - Tooling:**

- Run `npm run lint` if available
- Run `npm run test` if available
- Run `npm run build` if available

**Pass 3 - Cross-Reference:**

- Go through original numbered list
- Confirm each item is addressed
- Mark any gaps

**Pass 4 - Pattern Check:**

- Run `npm run patterns:check` if available
- Verify no anti-patterns introduced

### Phase 8: Learning Capture

**MANDATORY - Create entry in AI_REVIEW_LEARNINGS_LOG.md:**

```markdown
#### Review #N: <Description> (YYYY-MM-DD)

**Source:** <CodeRabbit PR | Qodo Compliance | Mixed> **Branch:** <branch name>
**Suggestions:** X total (Critical: X, Major: X, Minor: X, Trivial: X)

**Patterns Identified:**

1. [Pattern]: [Description]
   - Root cause: [Why]
   - Prevention: [How to avoid]

**Resolution:**

- Fixed: X
- Deferred: X (rare - with justification)
- Rejected: X (rare - with justification)

**Key Learnings:**

- <Learning 1>
- <Learning 2>
```

### Phase 9: Final Output

```markdown
## PR Review Processing Complete

### Summary

| Category  | Count | Status             |
| --------- | ----- | ------------------ |
| Critical  | X     | All Fixed          |
| Major     | X     | All Fixed          |
| Minor     | X     | All Fixed          |
| Trivial   | X     | All Fixed          |
| **Total** | **X** | **100% Addressed** |

### Files Modified

- `file1.ts:L45-67` - [what was fixed]
- `file2.md:L12` - [what was fixed]

### Agents Used

- security-auditor: [X issues]
- test-engineer: [X issues]

### Learning Entry

- Review #N added to AI_REVIEW_LEARNINGS_LOG.md
- Patterns: [list key patterns]

### Verification

- [x] All suggestions cross-referenced
- [x] Linter passing
- [x] Tests passing
- [x] Learning entry complete

### Commit Ready
```

fix: Address Review #N - [summary]

Resolved X suggestions from [source]:

- Critical: X, Major: X, Minor: X, Trivial: X

See AI_REVIEW_LEARNINGS_LOG.md Review #N for patterns.

```

```

---

## Quick Reference

### Commands to Run

```bash
# Get next review number
grep -c "#### Review #" AI_REVIEW_LEARNINGS_LOG.md

# After fixes
npm run lint
npm run test
npm run patterns:check
```

### Files to Update

1. All files mentioned in review (fixes)
2. `AI_REVIEW_LEARNINGS_LOG.md` (learning entry)
3. Update consolidation counter if needed

### Agents Available

- `security-auditor`, `test-engineer`, `performance-engineer`
- `technical-writer`, `debugger`, `backend-architect`
- `frontend-developer`, `code-reviewer`

---

## Anti-Patterns to Avoid

- Skipping trivial items
- Deferring minor items without strong justification
- Editing files without reading first
- Forgetting learning entry
- Not using TodoWrite for tracking
- Not invoking specialist agents
- Single-pass parsing of large reviews

---

## Related Documents

- `AI_REVIEW_PROCESS.md` - Full process documentation
- `AI_REVIEW_LEARNINGS_LOG.md` - Learning audit trail
- `claude.md` Section 4 - Distilled patterns
- `.claude/commands/pr-review.md` - Slash command version
