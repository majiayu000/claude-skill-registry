---
name: command-refine
description: "Analyze conversation and files to refine commands. Use when user says 'no' or 'wrong', when command behavior needs improvement, or when @/! injection fails. Includes conversation analysis, issue classification, evidence-based findings, and concrete refinements. Not for skills."
---

<mission_control>
<objective>Analyze conversation and files to identify command refinements, especially @/! injection patterns</objective>
<success_criteria>Evidence-based findings documented, injection patterns validated, safe ! commands verified</success_criteria>
</mission_control>

## Quick Start

**If user said "no" or "wrong":** Analyze what went wrong → Output refinements → Prevent recurrence

**If command failed:** Check injection patterns → Identify root cause → Fix @/!

**If files provided:** Analyze alongside conversation → Cross-reference findings

**Why:** Meta-analysis turns corrections into prevention—every mistake becomes a rule.

## Navigation

| If you need...              | Read this section...               |
| :-------------------------- | :--------------------------------- |
| Analyze conversation        | ## PATTERN: Conversation Analysis  |
| Classify issues             | ## PATTERN: Issue Classification   |
| Output refinements          | ## PATTERN: Refinement Output      |
| Anti-patterns to avoid      | ## ANTI-PATTERN: Lazy Analysis     |
| Verification                | ## PATTERN: Verification           |

## PATTERN: Conversation Analysis

### What to Look For

| Signal | Means | Action |
| :----- | :----- | :----- |
| "No, that's wrong" | Pattern violation | Fix injection/syntax |
| "I said X, not Y" | Misunderstanding | Refine description |
| "Command failed" | Injection issue | Check @/! patterns |
| "Wrong output" | Format issue | Verify command syntax |
| "Not what I meant" | Intent mismatch | Clarify triggers |
| User repeats correction | Persistent gap | Strengthen constraint |

### Conversation-First Analysis

The conversation IS your primary input. No file reads needed for context.

**When @files provided:**
- Read injected content for additional context
- Cross-reference with conversation
- Synthesize findings from both sources

**When no @files:**
- Conversation alone is sufficient

### Analysis Format

Each finding MUST have:

```
**Issue:** One-line description
**Evidence:** Quote from conversation or @file
**Root Cause:** Why it happened (not just symptoms)
**Fix:** Specific change to apply
```

### Example

```
**Issue:** @path file may not exist
**Evidence:** User said "No" when command referenced missing file
**Root Cause:** No fallback for missing file
**Fix:** Add "(if exists)" handling after @path
```

---

## PATTERN: Issue Classification

### Classification Matrix

| Error Signal | Root Cause Type | Target |
| :----------- | :-------------- | :----- |
| "Command failed" | @ path issue | Add fallback |
| "Wrong output" | ! command issue | Fix syntax |
| "Not what I meant" | Description issue | Clarify triggers |
| "Skipped validation" | Process Violation | Add constraint |
| "Wrong pattern" | Anti-pattern Gap | Add ANTI-PATTERN |
| "Structure wrong" | Single-file violation | Restructure |

### Severity Levels

| Level | Signal | Language |
| :---- | :----- | :------- |
| **CRITICAL** | Destructive !, missing security | USE STRONG WORDS |
| **HIGH** | Missing fallback, broken @/! | Clear directive |
| **MEDIUM** | Argument pattern, format | Guidance |
| **LOW** | Nice-to-have improvement | Consider |

---

## PATTERN: Refinement Output

### Concrete Changes Format

**File:** `path/to/command.md`
**Section:** `## PATTERN: X`
**Change:** `[Specific edit to apply]`
**Why:** `[Reason for change]`

### Verification Checklist

1. Read the actual file
2. Apply the change
3. Verify no regressions
4. Test with similar conversation pattern

### Output Template

```
## Refinement 1: [Title]

**File:** `.claude/commands/command-name.md`
**Section:** `## PATTERN: [Name]`
**Current:** [What exists]
**Change:** [What to add/replace]
**Why:** [Reason]

## Refinement 2: [Title]
...
```

---

## PATTERN: Injection Refinement

### @ Path Fixes

| Issue | Fix |
| :---- | :--- |
| File may not exist | Add "(if exists)" |
| No wrapper | Wrap in `<injected_content>` |
| Wrong path | Use absolute/relative path correctly |
| Static content | Remove @, inline content |

### ! Command Fixes

| Issue | Fix |
| :---- | :--- |
| Destructive command | Replace with read-only alternative |
| No error handling | Add graceful fallback |
| Complex logic | Simplify or use script |
| Unsafe command | Use safe alternative |

### Argument Fixes

| Issue | Fix |
| :---- | :--- |
| $1 for flags | Use ID/slug pattern only |
| Missing hint | Add `argument-hint` |
| Complex args | Use $IF($1, ..., ...) pattern |

---

## ANTI-PATTERN: Lazy Analysis

### Anti-Pattern: Vague Findings

```
❌ Wrong:
"The command has issues"

✅ Correct:
"Line 45: @.claude/missing/file.yaml - path may not exist.
Root cause: No fallback handling.
Fix: Add '(if exists)' after @path."
```

**Strong language:** BE SPECIFIC. Vague findings = lazy analysis.

### Anti-Pattern: Symptom-Only Reports

```
❌ Wrong:
"Command didn't work"

✅ Correct:
"User said 'No' at line 52.
Issue: !`rm *.log` is destructive.
Root cause: Unsafe ! command used.
Fix: Replace with !`ls *.log | wc -l`"
```

### Anti-Pattern: No Evidence

```
❌ Wrong:
"The injection needs fixing"

✅ Correct:
"Command failed when @file was missing.
Evidence: 'No such file' error at line 23.
Fix: Add fallback handling after @path."
```

### Anti-Pattern: Missing Root Cause

```
❌ Wrong:
"Fix the ! command"

✅ Correct:
"!`rm *.log` is destructive (line 41).
Impact: Deletes files without confirmation.
Fix: Use read-only !`ls *.log | wc -l`"
```

---

## PATTERN: Verification

### Before Publishing Refinements

| Check | Pass If |
| :---- | :------ |
| Evidence quoted | Every finding has conversation/file quote |
| Root cause analyzed | Not just symptoms reported |
| Fix is concrete | File + section + change specified |
| No false positives | Only real issues flagged |
| Language appropriate | Strong for failures, positive for correct |

### Verification Commands

```markdown
1. Read target command file
2. Apply refinement
3. Run: `mcp__ide__getDiagnostics`
4. Verify: No errors
5. Test: Does this prevent the original issue?
```

---

## EDGE: Multiple Issues

### Prioritization

When conversation has multiple problems:

1. **Critical first** — Security, destructive operations
2. **High frequency next** — Most common issues
3. **Group related** — Single fix for multiple occurrences

### Batch Output

```
## Refinements (Priority Order)

### 1. CRITICAL: [Issue Title]
[Evidence] → [Root Cause] → [Fix]

### 2. HIGH: [Issue Title]
[Evidence] → [Root Cause] → [Fix]

### 3. MEDIUM: [Issue Title]
...
```

---

## EDGE: No Issues Found

### When Analysis Yields Nothing

```
## Analysis Result: No Issues Detected

**What happened:** Command executed without corrections
**What this means:** Commands working as intended

**If this is wrong:**
- User may have silently accepted poor output
- Check for injection patterns that may fail edge cases
- Review ! commands for potential safety issues
```

---

## EDGE: Injection-Specific Checks

### When Analyzing @ Paths

- Path exists? If not, add fallback
- Content dynamic? Static content doesn't need @
- Wrapper used? Prefer `<injected_content>` grouping
- Error handling? Missing files handled gracefully

### When Analyzing ! Commands

- Read-only? No destructive operations
- Safe? No `rm`, `git push --force`, `chmod`
- Error handling? Failed commands don't crash
- Simple? Complex logic in scripts, not inline

### When Analyzing Arguments

- $1 for IDs only? Not flags/options
- Pattern consistent? ID/slug/hash format
- Fallback present? $IF($1, ..., ...) for optional

---

## Recognition Questions

| Question | Pass Means... |
| :------- | :------------ |
| Evidence provided? | Every finding has a quote |
| Root cause analyzed? | Not just surface symptoms |
| Fix is actionable? | Can apply directly |
| Language is strong? | Failures called out clearly |
| No false positives? | Only real issues flagged |
| @ paths validated? | Fallbacks present |
| ! commands safe? | No destructive operations |

---

## PATTERN: Quick Refinement Checklist

| Check | Description |
| :---- | :---------- |
| Specific evidence | Quote from conversation or file |
| Root cause | WHY it happened, not just WHAT |
| Concrete fix | File + section + change |
| No assumptions | Verified against actual files |
| Strong language | Failures clearly named |
| @ safe | Paths have fallbacks |
| ! safe | No destructive commands |

---

## Validation Checklist

Before claiming command refinement complete:

**Analysis Quality:**
- [ ] Evidence provided for every finding (conversation quote or file reference)
- [ ] Root cause analyzed, not just surface symptoms
- [ ] Fix is concrete (file + section + specific change)
- [ ] No false positives flagged
- [ ] No vague findings or assumptions

**Injection Safety:**
- [ ] All @ paths have fallback handling ("(if exists)")
- [ ] All ! commands are read-only (no rm, --force, etc.)
- [ ] Missing files handled gracefully
- [ ] Destructive commands replaced with safe alternatives

**Classification:**
- [ ] Issue correctly classified (@ issue, ! issue, description, etc.)
- [ ] Severity level assigned appropriately (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Target file and section identified correctly

**Output Format:**
- [ ] Concrete changes format used (File/Section/Change/Why)
- [ ] Language appropriate (strong for failures, positive for correct)
- [ ] Multiple issues prioritized (Critical first)

**Verification:**
- [ ] Actual file read before applying changes
- [ ] Diagnostics run after changes
- [ ] Fix prevents original issue (verified)

---

## Common Mistakes to Avoid

### Mistake 1: Vague Findings Without Evidence

❌ **Wrong:**
"The command description needs improvement."

✅ **Correct:**
**Issue:** Missing 'Not for' exclusion in description
**Evidence:** User said "No" when skill triggered for unrelated task
**Root Cause:** Description triggers too broad, includes unintended use cases
**Fix:** Add "Not for X" to description frontmatter at line 3

### Mistake 2: Skipping Root Cause Analysis

❌ **Wrong:**
"The @ path is wrong. Fix it."

✅ **Correct:**
**Issue:** @ path uses relative path that fails when invoked from different directory
**Evidence:** Command fails with "File not found" error
**Root Cause:** Path is relative to workspace root but command runs from project root
**Fix:** Change `@./docs/page.md` to `@/Users/project/docs/page.md`

### Mistake 3: Missing File Verification

❌ **Wrong:**
"Fix the frontmatter" (without reading the file)

✅ **Correct:**
**Issue:** Frontmatter missing 'model' field
**Evidence:** Read skill/SKILL.md lines 1-5
**Fix:** Add `model: inherit` to frontmatter

### Mistake 4: Dangerous ! Commands

❌ **Wrong:**
```markdown
!`rm -rf node_modules && npm install`
```

✅ **Correct:**
```markdown
!`npm list --depth=0`
```
(Use read-only commands in ! patterns)

### Mistake 5: No Severity Classification

❌ **Wrong:**
"The skill needs improvement."

✅ **Correct:**
**Issue:** Missing portability invariant (CRITICAL)
**Root Cause:** Skill references project rules (CLAUDE.md, CLAUDE.local.md, or .claude/rules/)
**Fix:** Remove all project rules references, bundle philosophy in file

---

## Best Practices Summary

✅ **DO:**
- Quote specific evidence from conversation or files
- Analyze root cause, not just symptoms
- Ensure all @ paths have fallback handling
- Ensure all ! commands are read-only (no destructive operations)
- Use strong language for destructive command issues
- Specify exact file, section, and change for each fix
- Verify changes against actual files

❌ **DON'T:**
- Make vague findings ("The command has issues")
- Use destructive ! commands (rm, --force, chmod)
- Skip fallback handling for @ paths that may not exist
- Report symptoms without root cause analysis
- Skip evidence (every finding must have a quote)
- Use weak language for safety issues
- Skip diagnostics after applying changes

---

<critical_constraint>
**Meta-Analysis Invariant:**

1. Conversation is PRIMARY input (already in context)
2. @files are OPTIONAL supplements
3. Output MUST be concrete (not vague recommendations)
4. Every finding MUST have evidence
5. Fixes MUST specify exact file and section
6. Strong language for agent failures
7. Verify everything against actual files
8. All `!` commands MUST be read-only
9. All `@` paths MUST have graceful fallback
10. Never use relative paths pointing outside the skill itself. When referencing other components, use: "invoke `skill-name`" or "invoke `skill-name` and read its file"

**NO VAGUE FINDINGS. NO DESTRUCTIVE COMMANDS. BE SPECIFIC.**
</critical_constraint>
