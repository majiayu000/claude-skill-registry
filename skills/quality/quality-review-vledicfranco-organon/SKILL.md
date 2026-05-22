---
name: quality-review
description: Semantic review of organon files that goes beyond automated gates. Checks whether invariants are testable, principles are genuinely prioritized, identity statements define real boundaries, and heuristics cover actual recurring decisions. Use for weekly quality checks or when reviewing new organon files.
protocol_id: PROTO-ORG-7
protocol_file: organon/protocols/PROTOCOLS.md
tools: [organon-verify, organon-validate, organon-health]
loads:
  - book-llms/ETHOS.md
  - book-llms/patterns.md
  - book-llms/workflow-authoring.md
  - CLAUDE.md
---

# Quality Review Workflow

> Implements PROTO-ORG-7 from `organon/protocols/PROTOCOLS.md`. Semantic quality review that catches what automation cannot.

---

## When to Use This Skill

Use this skill when:
- **Reviewing new organon files** — before merging, check semantic quality
- **Weekly quality audits** — periodic check beyond automated gates
- **After significant methodology changes** — verify meaning wasn't lost
- **When something "feels off"** — gut check against quality standards

**Purpose:** Automated gates check structure (frontmatter present, sections exist, references resolve). This workflow checks *meaning* (invariants testable, principles ordered correctly, heuristics covering real decisions).

---

## Context Loading

1. Load quality standards:
   - Read `book-llms/ETHOS.md` (meta-organon constraints — what every organon must follow)
   - Read `book-llms/patterns.md` (anti-pattern tables — common mistakes to check for)
   - Read `book-llms/workflow-authoring.md` (workflow quality attributes)
2. Load project constraints:
   - Read `CLAUDE.md` (project-level guidance)

---

## Steps

### Step 1: Select Review Scope

Choose what to review:
- **Single file** — focused review of one organon file
- **Directory** — review all organon files in a scope (e.g., `organon/domains/testing/`)
- **Project-wide** — full quality audit of all organon files

### Step 2: Run Automated Gates First

```bash
cd packages/tools && npx organon verify
cd packages/tools && npx organon validate <path>
```

Fix any automated failures before proceeding. Semantic review is only meaningful when structural issues are resolved.

### Step 3: Review Invariants

For each invariant in the target file(s), apply these filters:

| Filter | Question | Pass Criteria |
|--------|----------|---------------|
| **Testable?** | Can you write a verification gate for this? | Yes — describes a checkable condition |
| **Specific?** | Does this constrain behavior concretely? | Yes — not a vague aspiration like "be good" |
| **Enforceable?** | Is the enforcement mechanism real? | Yes — references a specific tool, gate, or process |
| **Non-redundant?** | Does this say something the parent scope doesn't already say? | Yes — adds value beyond inheritance |
| **Correctly IDed?** | Does the ID follow the INV-SCOPE-N format? | Yes — matches scope and sequential numbering |

**Red flags:**
- "Should be high quality" → too vague, rewrite
- "Enforced by: reviews" → too weak, specify which gate or tool
- Duplicates parent invariant verbatim → remove (inherited automatically)

### Step 4: Review Principle Ordering

For each principle list, test the ordering:

1. **Conflict test:** If principle 3 conflicts with principle 1, does 1 genuinely win? If not, reorder.
2. **Independence test:** Are any two principles actually saying the same thing? If so, merge.
3. **Actionability test:** Can an agent use this ordering to make a decision? If not, principles are too abstract.

**Example of bad ordering:**
```
1. Clarity over complexity
2. Simplicity over complexity
```
These overlap significantly — merge or differentiate.

**Example of good ordering:**
```
1. Correctness over performance
2. Clarity over brevity
```
These are distinct and genuinely prioritized — correctness beats clarity when they conflict.

### Step 5: Review Identity Statements

For each IS/IS NOT section:

| Check | Good Example | Bad Example |
|-------|-------------|-------------|
| **Specific?** | "A semantic testing framework for tier-4 invariant verification" | "A good testing framework" |
| **Distinguishing?** | Could describe only *this* thing, not any similar thing | Could describe any testing framework |
| **Boundary-defining?** | IS NOT statements prevent scope creep | IS NOT statements are obvious negations |

**Red flags:**
- "IS: well-designed and useful" → generic, could be anything
- "IS NOT: bad" → obvious negation, not a real boundary
- All IS statements could apply to competitors → not specific enough

### Step 6: Review Heuristics

For each decision heuristic table:

| Check | Question |
|-------|----------|
| **Coverage** | Do these cover the decisions that actually recur in this scope? |
| **Missing decisions** | Are there common decisions NOT in the table? |
| **Actionability** | Are the actions specific enough to follow without judgment? |
| **Overlap** | Do any heuristics give conflicting advice for the same situation? |

**How to find missing heuristics:** Think about the last 5 times you worked in this scope. What decisions did you make? Are they in the table?

### Step 7: Check Cross-File Terminology

Search for key terms across all organon files:

Use the Grep tool to search for key terms across all project files:

```
Grep pattern="workflow" path="." glob="*.md"
Grep pattern="skill" path="." glob="*.md"
```

Flag inconsistencies:
- "Skill" used as generic term (should be "workflow")
- Same concept with different names in different files
- Outdated terminology from previous methodology versions

**Known terminology rules (from MEMORY.md):**
- "Workflow" = generic term for agent binding layer (Layer 2)
- "Skill" = specific instance (Claude Code skills, Cursor rules)
- Never use "skill" as the generic term — always "workflow"

### Step 8: Check Anti-Patterns

Compare content against anti-pattern tables:

1. **`book-llms/ETHOS.md` anti-patterns** (~17 entries) — organon authoring mistakes
2. **`book-llms/patterns.md` anti-patterns** (~17 entries) — broader project anti-patterns

For each anti-pattern, check: does the reviewed content exhibit this pattern?

**Common anti-patterns found in reviews:**
- Phantom Enforcement: invariant claims enforcement but mechanism doesn't exist
- Aspiration as Invariant: "should be" language in invariant (should be "must be")
- Context Overload: workflow loads too many files
- Missing Error Recovery: workflow has no failure/recovery table

### Step 9: Generate Review Report

Structure findings by severity:

```
## Quality Review Report — [scope]

### Errors (must fix)
- [file:line] — [finding] — [fix]

### Warnings (should fix)
- [file:line] — [finding] — [fix]

### Suggestions (consider)
- [file:line] — [finding] — [suggestion]

### Summary
- Files reviewed: N
- Errors: N
- Warnings: N
- Suggestions: N
```

### Step 10: Track Improvements

If fixes are made during the review:

```bash
cd packages/tools && npx organon verify
cd packages/tools && npx organon health
```

Confirm no regressions. Health score should be equal to or higher.

---

## Verification

- [ ] All automated gates pass (prerequisite for semantic review)
- [ ] Every invariant passes the "testable?" filter
- [ ] Principle ordering is defensible (1 genuinely beats 2 in conflicts)
- [ ] Identity statements are specific and distinguishing
- [ ] Heuristics cover actual recurring decisions
- [ ] No anti-pattern matches found
- [ ] Terminology is consistent across all files reviewed
- [ ] Review report generated with findings by severity

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| Invariant is untestable | Rewrite to be more specific. If it can't be made testable, move it to principles (aspirational, not invariant). |
| Principles not truly prioritized | Reorder with explicit trade-off reasoning. Document conflicts between adjacent principles. |
| Identity too generic | Add specifics: technology names, scope boundaries, unique characteristics that distinguish this from similar things. |
| Anti-pattern found in content | Apply the fix from the anti-pattern table. If the fix is unclear, read the full anti-pattern description in the source file. |
| Terminology inconsistent | Choose the canonical term (check MEMORY.md for established conventions). Grep-and-replace across all affected files. |
| Too many findings to fix | Prioritize errors over warnings over suggestions. Fix errors first, then create TODOs for the rest. |
| Review scope too large | Narrow to a single directory or file. Project-wide reviews should be broken into multiple focused sessions. |
