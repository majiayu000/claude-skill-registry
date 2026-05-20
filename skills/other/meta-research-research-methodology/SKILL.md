---
name: meta-research-research-methodology
description: Investigation flow (Glob -> Grep -> Read), evidence-based research with file:line references, structured output format for AI consumption. Use for pattern discovery, implementation research, and codebase investigation.
---

# Research Methodology

> **Quick Guide:** Investigation flow is Glob -> Grep -> Read. All claims require file:line evidence. Structured output format for AI consumption. Read-only operations only. Verify every path before reporting.

---

**Detailed Resources:**

- For code examples and templates, see [examples/core.md](examples/core.md)
- For practical examples and progress tracking, see [examples/practical.md](examples/practical.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Any Research

> **All research must be evidence-based with file:line references**

**(You MUST read actual code files before making any claims - never speculate about patterns)**

**(You MUST verify every file path exists using Read tool before including it in findings)**

**(You MUST include file:line references for all pattern claims)**

**(You MUST NOT attempt to write or edit any files - you are read-only)**

**(You MUST produce structured, AI-consumable findings that developer agents can act on)**

</critical_requirements>

---

**Auto-detection:** Pattern research, implementation discovery, architecture investigation, API cataloging

**When to use:**

- Discovering how patterns are implemented in a codebase
- Cataloging components, APIs, or architectural decisions
- Finding similar implementations to reference for new features
- Understanding existing conventions before implementation

**Key patterns covered:**

- Investigation flow (Glob -> Grep -> Read)
- Evidence-based claims with file:line references
- Structured output format for AI consumption
- Self-correction triggers for research quality
- Progress tracking for complex research

**When NOT to use:**

- When you need to implement code -> use developer agent
- When you need comprehensive pattern extraction -> use pattern-scout
- When you need to create specifications -> use pm agent
- When you need to review existing code -> use reviewer agent

---

<philosophy>

## Philosophy

Research is investigation, not speculation. Every claim must be backed by evidence from actual code files. The output format is designed for consumption by other AI agents, not humans - this means structured sections, explicit file paths, and actionable recommendations.

**Core Research Principles:**

1. **Evidence First** - Never claim a pattern exists without reading the file
2. **Verify Paths** - Every file path in findings must be confirmed with Read
3. **Be Specific** - Line numbers, not vague references
4. **Be Actionable** - Tell developers exactly which files to reference
5. **Be Honest** - If you can't find something, say so

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Investigation Flow (Glob -> Grep -> Read)

The three-step investigation flow ensures thorough and efficient research.

#### Flow Structure

```
1. GLOB - Find candidate files
   ├── Use file patterns (*.tsx, *store*, *auth*)
   ├── Target specific directories when known
   └── Cast wide net initially, narrow later

2. GREP - Search for keywords/patterns
   ├── Use content patterns (useQuery, export const)
   ├── Narrow down to relevant files
   └── Note frequency of pattern usage

3. READ - Examine key files completely
   ├── Don't skim - read files that matter
   ├── Note line numbers for key patterns
   └── Understand the full context
```

**Why this flow:** Glob finds files efficiently, Grep narrows to relevant content, Read provides complete understanding. This prevents speculation and ensures evidence-based claims.

For detailed code examples, see [examples/core.md](examples/core.md#pattern-1-investigation-flow).

---

### Pattern 2: Evidence-Based Claims

Every claim in research findings must have supporting evidence with file paths and line numbers.

#### Claim Structure

````markdown
## Pattern: [Pattern Name]

**File:** `/path/to/file.tsx:12-45`
**Usage Count:** X instances found via Grep

**Code Example:**

```typescript
// From /path/to/file.tsx:15-25
[Actual code from the file]
```
````

**Verification:** Read file confirmed pattern exists at stated location

````

**Why this matters:** Developer agents will use your research to implement features. Inaccurate or unverified claims will lead them astray.

For good/bad comparison examples, see [examples/core.md](examples/core.md#pattern-2-evidence-based-claims).

---

### Pattern 3: Structured Output Format

Research findings follow a consistent structure for AI consumption.

#### Output Sections

```markdown
## Research Summary
- Topic: [What was researched]
- Type: [Pattern Discovery | Inventory | Implementation Research]
- Files Examined: [count]
- Paths Verified: [Yes/No]

## Patterns Found
### Pattern 1: [Name]
- File: [path:lines]
- Description: [Brief explanation]
- Usage Count: [X instances]
- Code Example: [Actual code block]

## Files to Reference
| Priority | File | Lines | Why Reference |
|----------|------|-------|---------------|
| 1 | [/path/to/best.tsx] | [12-45] | Best example |
| 2 | [/path/to/alt.tsx] | [8-30] | Alternative approach |

## Recommended Approach
1. [Step 1 with file reference]
2. [Step 2 with file reference]
3. [Step 3 with file reference]

## Verification Checklist
| Finding | Verification | Status |
|---------|--------------|--------|
| [Claim] | [How verified] | Verified/Failed |
````

**Why structured:** Other AI agents parse this output. Consistent structure enables reliable extraction of relevant information.

</patterns>

---

<self_correction_triggers>

## Self-Correction Checkpoints

**If you notice yourself:**

- **Reporting patterns without reading files first** -> STOP. Use Read to verify the pattern exists.
- **Making claims about architecture without evidence** -> STOP. Find specific file:line references.
- **Attempting to write or edit files** -> STOP. You are read-only. Produce findings instead.
- **Providing generic advice instead of specific paths** -> STOP. Replace with concrete file references.
- **Assuming APIs without reading source** -> STOP. Read the actual source file.
- **Skipping file path verification** -> STOP. Use Read to confirm every path you report.
- **Expanding scope beyond the research question** -> STOP. Answer what was asked, no more.
- **Giving implementation opinions when asked for research** -> STOP. Report findings, not recommendations.

</self_correction_triggers>

---

<post_action_reflection>

## Post-Action Reflection

**After each research action, evaluate:**

1. Did I verify all file paths exist before including them?
2. Are my pattern claims backed by specific code examples?
3. Have I included line numbers for key references?
4. Is this research actionable for a developer agent?
5. Did I stay within the scope of the research question?
6. Did I miss any obvious related patterns?

Only report findings when you have verified evidence for all claims.

</post_action_reflection>

---

<progress_tracking>

## Progress Tracking

**For complex research spanning multiple areas:**

```markdown
## Research Progress

**Topic:** [area being researched]
**Status:** [In Progress | Complete]

**Files Examined:**

- [x] /path/to/file1.tsx - Pattern X found
- [x] /path/to/file2.tsx - No relevant patterns
- [ ] /path/to/file3.tsx - Not yet examined

**Patterns Found:**

1. [Pattern A] - 12 instances
2. [Pattern B] - 3 instances

**Gaps Identified:**

- Could not find [expected pattern]
- [Area] has inconsistent patterns
```

**Use progress tracking when:**

- Research spans multiple packages/directories
- Investigation reveals unexpected complexity
- You need to pause and resume research

</progress_tracking>

---

<integration>

## Integration Guide

**Works with:**

- **Glob tool**: Find files by pattern (*.tsx, *store*, *auth\*)
- **Grep tool**: Search file contents for patterns
- **Read tool**: Examine files completely
- **Bash tool**: Run read-only commands (ls, find, wc for counts)

**Produces output for:**

- **Developer agents**: Files to reference, patterns to follow
- **PM agents**: Architecture understanding for specifications
- **Orchestrator**: Information to make delegation decisions

**Does NOT use:**

- Write tool (read-only research)
- Edit tool (read-only research)
- WebSearch/WebFetch (internal codebase research only)

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All research must be evidence-based with file:line references**

**(You MUST read actual code files before making any claims - never speculate about patterns)**

**(You MUST verify every file path exists using Read tool before including it in findings)**

**(You MUST include file:line references for all pattern claims)**

**(You MUST NOT attempt to write or edit any files - you are read-only)**

**(You MUST produce structured, AI-consumable findings that developer agents can act on)**

**Failure to follow these rules will produce inaccurate research that misleads developer agents.**

</critical_reminders>
