---
name: error-logger
description: Maintains detailed log of errors, bugs, and debugging sessions encountered during development. Use when encountering errors, debugging issues, or solving technical problems. Creates structured ERROR_LOG.md with error details, root causes, solutions, and prevention strategies. Complements project-logger (strategic decisions) with tactical debugging knowledge.
---

# Error Logger

## Overview

This skill maintains a detailed ERROR_LOG.md file that chronicles all errors, bugs, and debugging sessions. Unlike LOG.md (which tracks strategic project evolution), ERROR_LOG.md captures tactical debugging knowledge: what went wrong, why, and how it was fixed.

## When to Use This Skill

Use this skill when:
- Encountering an error or exception
- Debugging a tricky issue
- Discovering an edge case
- Solving a technical problem
- Finding a workaround for a limitation
- Identifying a pattern of recurring errors

**Typical triggers:**
- "Log this error"
- "Document this debugging session"
- "Record how I fixed this bug"

## Workflow

### Step 1: Identify Error Event

Recognize when to create an error log entry:

**Log immediately when:**
- Error or exception occurred
- Spent >15 minutes debugging
- Found non-obvious solution
- Discovered edge case
- Implemented workaround

**Don't log for:**
- Simple typos (unless revealing deeper issue)
- Expected errors (user input validation)
- Trivial fixes (<5 minutes)

### Step 2: Gather Error Information

Collect all relevant details:

**Required information:**
1. **Error message**: Full traceback or error output
2. **Location**: File path, line number, function name
3. **Context**: What were you doing when error occurred?
4. **Timestamp**: When did this happen?

**Optional but helpful:**
5. Environment details (Python version, OS, dependencies)
6. Input data that triggered the error
7. Related errors or previous occurrences

**How to gather:**
```bash
# Copy full error traceback
# Note current file and line number
# Describe the action that triggered it
```

### Step 3: Classify Error

Determine error type and severity:

**Error Types:**
- **SYNTAX**: Code syntax errors, typos in code
- **TYPE**: Type errors, None errors, attribute errors
- **LOGIC**: Logic bugs, incorrect algorithms
- **DEPENDENCY**: Import errors, version conflicts, missing packages
- **ENVIRONMENT**: Path issues, permission errors, OS-specific
- **PERFORMANCE**: Timeouts, memory issues, slow operations
- **INTEGRATION**: API errors, external service failures
- **DATA**: Data format issues, parsing errors, validation failures
- **EDGE_CASE**: Unexpected input or state
- **REGRESSION**: Previously working code now broken

**Severity Levels:**
- **Critical**: Blocks all work, data loss risk
- **High**: Blocks major functionality
- **Medium**: Workaround exists, impacts some workflows
- **Low**: Minor issue, easy to avoid

### Step 4: Debug and Find Root Cause

Investigate the underlying issue:

**Debugging process:**
1. Reproduce the error consistently
2. Isolate the failing component
3. Trace execution flow
4. Identify root cause (not just symptom)
5. Understand why it happened

**Document your process:**
- What did you try first?
- What led you to the root cause?
- What false leads did you follow?

**Root cause should answer:**
- Why did the error occur?
- What assumption was violated?
- What condition wasn't handled?

### Step 5: Implement Solution

Fix the error and document the solution:

**Solution types:**
- **Fix**: Corrected the root cause
- **Workaround**: Temporary solution, root cause remains
- **Refactor**: Restructured code to prevent issue
- **Config**: Changed configuration or environment
- **Dependency**: Updated/changed dependency version

**Document:**
- What code changed?
- Why does this fix work?
- Are there any trade-offs?
- Is this temporary or permanent?

### Step 6: Add Prevention Strategy

Identify how to avoid this in the future:

**Prevention strategies:**
- Code pattern to follow (or avoid)
- Validation to add
- Test to write
- Documentation to update
- Design principle to remember

**Examples:**
- "Always check for None before accessing attributes"
- "Validate input types at function boundaries"
- "Add unit test for empty list edge case"
- "Document API rate limits in code comments"

### Step 7: Write Error Log Entry

Create structured entry in ERROR_LOG.md:

**Location**: `.claude/ERROR_LOG.md`

**Entry format:**
```markdown
## [ERROR_TYPE] Error Title

**Timestamp:** YYYY-MM-DD HH:MM
**Severity:** [Critical/High/Medium/Low]
**Status:** [Resolved/Workaround/Open]

### Location

- File: `path/to/file.py:123`
- Function: `function_name()`
- Component: [which part of the system]

### Context

[What were you doing when this happened? What was the expected behavior?]

### Error Message

\`\`\`
[Full error traceback or error output]
\`\`\`

### Root Cause

[Why did this error occur? What was the underlying issue?]

### Solution

**Type:** [Fix/Workaround/Refactor/Config/Dependency]

[How was it fixed? What code changed?]

\`\`\`python
# Code snippet showing the fix
[before/after comparison if helpful]
\`\`\`

### Prevention

[How to avoid this in the future?]

- [Prevention strategy 1]
- [Prevention strategy 2]

### Related

- Similar errors: [Links to related error entries]
- Extracted to: [Which skill was updated with this knowledge]
- Issue tracker: [External issue link if applicable]

---
```

**Insertion point:**
- New errors go at the top (most recent first)
- Maintains reverse chronological order

### Step 8: Link to Knowledge Extraction

Connect error to skill improvements:

**If error reveals general knowledge:**
1. Note which skill should be updated
2. Add "Extracted to: [skill-name]/references/troubleshooting.md"
3. Later use skill-updater to add troubleshooting guidance

**If error is project-specific:**
1. Note "Project-specific: stays in ERROR_LOG.md"
2. No extraction needed

**Examples:**
- Git merge conflict resolution → Extract to git-workflow
- Python type error pattern → Extract to python-best-practices (if exists)
- API rate limiting → Extract to api-integration-skill

## Error Log Patterns

### Pattern 1: Quick Error

**Scenario:** Simple error with obvious fix

**Example:** TypeError from typo

**Log format (condensed):**
```markdown
## [TYPE] TypeError: 'NoneType' object is not subscriptable

**Timestamp:** 2025-12-31 14:30
**Severity:** Low
**Status:** Resolved

**Location:** `skill_analyzer.py:45`

**Root Cause:** Forgot to check if section exists before accessing

**Solution:** Added None check: `if section is not None:`

**Prevention:** Always validate before accessing optional data

---
```

### Pattern 2: Complex Debugging Session

**Scenario:** Multi-hour debugging with false leads

**Log format (detailed):**
```markdown
## [PERFORMANCE] Skill loading timeout after 30 seconds

**Timestamp:** 2025-12-31 09:00
**Severity:** High
**Status:** Resolved

**Location:** `.claude/core/skill_loader.py:234`

**Context:**
Loading skills from directory with 50+ skills causes timeout.
Expected load time <1s, actual time >30s.

**Error Message:**
\`\`\`
TimeoutError: Skill loading exceeded 30 second timeout
  at skill_loader.py:234 in load_all_skills()
\`\`\`

**Debugging Process:**
1. First thought: Too many files → profiled file I/O (not the issue)
2. Second attempt: Large SKILL.md files → checked file sizes (all <100KB)
3. Key insight: Noticed repeated regex compilation in loop
4. Root cause found: Regex pattern recompiled for each skill

**Root Cause:**
Regex pattern for parsing frontmatter was compiled inside the loop,
causing O(n) regex compilations instead of O(1).

**Solution:**
**Type:** Refactor

Moved regex compilation outside loop:
\`\`\`python
# Before
for skill in skills:
    pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
    match = pattern.search(skill_content)

# After
pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
for skill in skills:
    match = pattern.search(skill_content)
\`\`\`

Load time reduced from 30s → 0.3s (100x improvement)

**Prevention:**
- Profile before optimizing (avoid premature optimization)
- Move invariant computations out of loops
- Cache compiled regex patterns
- Add performance tests for operations on collections

**Related:**
- Extracted to: skill-creator/references/performance-patterns.md
- Similar pattern: references/common-mistakes.md#loop-invariants

---
```

### Pattern 3: Recurring Error

**Scenario:** Same error type appears multiple times

**Log format (with links):**
```markdown
## [TYPE] AttributeError: 'dict' object has no attribute 'get_value'

**Timestamp:** 2025-12-31 16:45
**Severity:** Medium
**Status:** Resolved

**Context:**
Third occurrence of this pattern - trying to call method on dict
instead of accessing key.

**Root Cause:**
Confusion between dict access (dict['key'] or dict.get('key'))
and object attribute access (obj.attribute).

**Solution:**
Changed to dict access: `config.get('value')` → `config['value']`

**Prevention:**
- Use type hints to catch at development time
- Remember: dicts use [], not .attribute
- Consider using dataclasses for structured config

**Related:**
- Previous occurrences: See [TYPE] entries from 2025-12-30
- Pattern documented in: python-patterns/references/dict-vs-object.md

---
```

## ERROR_LOG.md Management

### When to Clean Up

**Archive old errors when:**
- ERROR_LOG.md exceeds 1000 lines
- Error is >6 months old and resolved
- Knowledge already extracted to skills

**Archive location:**
- Create `ERROR_LOG_ARCHIVE_2025.md`
- Move old entries
- Keep link in main ERROR_LOG.md

**Never delete:**
- Recurring error patterns
- Critical errors with complex solutions
- Errors that led to important insights

### Integration with knowledge-extractor

**knowledge-extractor analyzes ERROR_LOG.md to:**
1. Identify recurring error patterns
2. Find troubleshooting knowledge to extract
3. Recommend adding to skill references/troubleshooting.md
4. Generate prevention guidelines

**Example extraction:**
- 3 git merge conflict errors → Extract pattern to git-workflow
- 5 API timeout errors → Create api-resilience-patterns.md
- 10 None-check errors → Add to python-defensive-programming.md

## Resources

### references/error_log_template.md

Complete ERROR_LOG.md template with:
- Header structure
- Error type taxonomy
- Example entries for each error type
- Best practices for error documentation

See this file for the full template and examples.

## Skill Contract

**Stable:** 8-step workflow, error classification taxonomy, entry format structure
**Mutable:** Error type categories, example patterns, prevention strategies, integration with knowledge-extractor
**Update rules:** See `references/contract.md` for detailed rules

> Full contract specification in `references/contract.md`
