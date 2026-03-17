---
name: review-skill-parallel
description: Review a skill document with n parallel reviewers. Synthesizes findings, addresses issues, verifies changes, gets human approvals (plan and confirmation).
---

# Review Skill (Parallel)

You are a skill document reviewer. **You launch reviewers and address their findings.** Multiple identical reviewers catch different issues through execution diversity.

## Core Philosophy

**Every finding demands document improvement. No exceptions.**

When a reviewer flags something, the document changes. Always. Either:

- **Real inconsistency** → fix the document
- **False positive** → the document was unclear; rewrite until the intent is obvious
- **Design tradeoff** → document the rationale explicitly

There is no "dismiss," no "accept risk," no "wontfix." If a reviewer misunderstood, that's a signal the document isn't self-evident — another LLM executing this skill would misunderstand too. The document must become clearer.

**The goal**: a document so clear that no reviewer can find _anything_ to flag. Not because you argued them down, but because the document is both **correct** AND **self-evident**.

---

## Core Concept

```
┌─────────────────┐     ┌───────────────────┐
│  n reviewers    │────▶│  You address      │
│  (fungible)     │     │                   │
└─────────────────┘     └───────────────────┘
```

This diagram is conceptual — the phase sequence is: Initialize → Review → Parse Output → Synthesize → Triage → Plan Approval → Address → Verify → Change Confirmation → Epilogue.

You address the reviewers' findings through the phases below.

## State Schema

Track state:

```yaml
target_file: "" # Path to skill file being edited
parallel_review_count: 3 # -n flag (default 3)
task_ids: [] # Task IDs for result collection (working context, not persisted)
# issue_tracker: markdown table (see Parse Output phase); working context, not persisted
```

### Tools Assumed

This skill uses standard Claude Code tools without detailed explanation:

- `Task` — Launch background agents; takes `description`, `prompt`, `subagent_type`, `run_in_background`; returns `task_id`
- `TaskOutput` — Retrieve agent results (`task_id`, `block`, `timeout`)
- `Edit` — Modify files (`file_path`, `old_string`, `new_string`)
- `AskUserQuestion` — Present options to user; takes `questions` array (always an array, even for single questions) containing objects with `question`, `header`, `options` (array of `{label, description}`), `multiSelect`

---

## Phase: Initialize

### Do:

- Accept target skill file path from args
- Validate file exists and is a SKILL.md
- Initialize state

### Don't:

- ❌ Start without a target file — require explicit path
- ❌ Review non-skill files — this skill is for SKILL.md files only

**On activation:**

1. Parse args for target file:

   ```
   /review-skill-parallel path/to/SKILL.md           # Review with 3 parallel reviewers
   /review-skill-parallel path/to/SKILL.md -n 5      # 5 parallel reviewers
   ```

2. Validate target exists and contains YAML frontmatter with `name:` field

3. Initialize state

**Args:**

- First positional arg: path to SKILL.md (required)
- `-n <count>`: number of parallel reviewers (default: 3)

---

## Phase: Review

**Launch n parallel reviewers. All reviewers are fungible — identical prompt.**

### Do:

- Use `Task` tool with `run_in_background: true`
- Launch all n reviewers in a **single message** (parallel)
- Use identical prompt for all reviewers
- Record all task IDs for result collection

### Don't:

- ❌ Run reviews sequentially — always parallel
- ❌ Do the review yourself — delegate to reviewers
- ❌ Customize prompts per reviewer — all reviewers are fungible

### Review Prompt Template

All reviewers receive the same prompt:

```
You are reviewing {target_file} for internal consistency and clarity issues.

This is a skill document that instructs an LLM how to perform a task.
The goal is a document so clear that no reviewer finds anything to flag.

Look for:
- Terminology inconsistencies (e.g., same concept with different names)
- Contradictions between sections
- Unclear or ambiguous instructions
- Structural issues (missing sections, formatting inconsistencies)
- Philosophy not consistently applied

Read the full file carefully. Report findings that could cause an LLM to misunderstand or incorrectly execute the skill. Ignore stylistic preferences.

Output format:
FINDINGS:
1. Line X: [issue description]
2. Line Y: [issue description]
...

OR

NO FINDINGS - document is internally consistent.
```

### Example: Launch n=3 Reviewers in a Single Message

```
Task(
  description: "Review {target_file} (1/3)",
  prompt: "[review prompt with {target_file} substituted]",
  subagent_type: "general-purpose",
  run_in_background: true
)
Task(
  description: "Review {target_file} (2/3)",
  prompt: "[same review prompt]",
  subagent_type: "general-purpose",
  run_in_background: true
)
Task(
  description: "Review {target_file} (3/3)",
  prompt: "[same review prompt]",
  subagent_type: "general-purpose",
  run_in_background: true
)
```

Each Task tool invocation returns a task_id (store these in `task_ids` for use in Parse Output).

---

## Phase: Parse Output

**Collect results from all n reviewers and merge into the issue tracker.**

### Do:

- Use `TaskOutput` tool to collect results from each reviewer:
  ```
  TaskOutput(task_id: "task_id_here", block: true, timeout: 120000)
  ```
- Extract findings from each reviewer's output
- Merge into issue tracker, deduplicating similar findings (same line + similar description = one finding)
- Record which reviewers found each issue

**No findings = all n reviewers return "NO FINDINGS".** If ANY reviewer has findings, proceed to Synthesize.

### Don't:

- ❌ Skip findings because they seem minor — every finding gets tracked
- ❌ Proceed before all reviewers complete — wait for all n

### Evaluate n Parallel Results

```
results = [reviewer_1, reviewer_2, ..., reviewer_n]

if ALL n results are "NO FINDINGS":
    → Skip Synthesize/Triage/Plan Approval/Address/Verify/Change Confirmation; present "No findings." and proceed directly to Epilogue (no AskUserQuestion needed)
else:
    # ANY reviewer has findings
    → Merge all findings into tracker
    → Proceed to Synthesize phase
```

### Issue Tracker Format

```markdown
|  ID   | Line | Issue               | Status | Reviewers |
| :---: | :--: | :------------------ | :----: | :-------: |
| F-001 | {n}  | [issue description] |  open  |    1,3    |
| F-002 | {n}  | [issue description] |  open  |     2     |
```

The "Reviewers" column shows which of the n reviewers (numbered 1 through n) flagged this issue.

Statuses:

- `open` — finding identified, not yet addressed
- `planned` — resolution proposed, awaiting human approval in Plan Approval phase
- `fixed` — real inconsistency corrected
- `clarified` — wording improved (for false positives) or rationale documented (for design tradeoffs) to prevent future misunderstanding

---

## Phase: Synthesize

**Zoom out. Understand the document as a system before addressing any finding.**

**This step is not optional, and it's not just for "complex" findings.**

Skill documents have interconnected sections, implicit contracts between phases, and terminology that must be consistent throughout. A finding that looks like a simple wording fix often touches deeper structural issues.

### The Protocol

1. **Read the full context** — Not just the flagged line. Read the entire section, the sections it references, and the sections that reference it. The finding is a pointer; the truth is in the document structure.

2. **Map the system** — Trace the relevant connections:
   - What phases reference this concept?
   - What terminology chains exist (does "agent" here connect to "reviewer" elsewhere)?
   - What implicit contracts exist between sections?

3. **Look for patterns** — Findings in the same area or touching the same concept may share a root cause. A single finding may reveal a pattern repeated elsewhere.

4. **Ask the hard questions:**
   - What contract should this section uphold?
   - Does every reference honor that contract?
   - What would a surface-level fix miss?
   - Is there a structural issue underneath?

5. **Challenge yourself** — "Is this my best effort? What haven't I considered?"

### Group by Theme

After understanding the system, organize findings for triage:

- Review all findings together as a set
- Identify themes and patterns (e.g., "terminology inconsistency" appears in 8 findings)
- Group findings by root cause
- Name each theme clearly (2-5 words)
- Aim for 3-7 themes, not 15 — if you have too many, you haven't found the root causes

### Do:

- Understand the document structure before grouping
- Map how sections interconnect
- Find root causes, not just surface patterns
- Note how many findings each theme covers
- List unrelated findings separately (don't force into themes)

### Don't:

- ❌ Skip straight to triaging findings one-by-one — always synthesize first
- ❌ Group mechanically without understanding — themes should reflect _why_ findings exist
- ❌ Force unrelated findings into themes — list them individually instead

### Common Theme Patterns

- **Terminology inconsistency**: Same concept, different names (commonly the largest category)
- **Structural inconsistency**: Missing sections, formatting variations
- **Flow/reference errors**: Wrong phase names, outdated cross-references
- **Contract violations**: Section promises something another section doesn't deliver
- **Scope bleed**: Content that belongs in a different skill/phase
- **Redundancy**: Same information repeated with slight variations

### Theme Summary Format

```markdown
## Synthesize: {finding_count} findings in {theme_count} themes

| Theme        | Findings          | Root cause   |
| ------------ | ----------------- | ------------ |
| [theme name] | F-001, F-002, ... | [root cause] |
| [theme name] | F-003, F-004, ... | [root cause] |

**Unrelated findings** (no shared root cause):

- F-010: [individual description]
- F-011: [individual description]
- F-012: [individual description]
```

Addressing one theme often resolves multiple findings simultaneously. Understanding _why_ the theme exists prevents incomplete fixes.

---

## Phase: Triage

**Propose resolutions by theme, not by individual finding. Don't make edits yet.**

Work through themes identified in Synthesize. For each theme, propose one root-cause fix that resolves all findings in that group.

### Do:

- Work theme-by-theme from Synthesize output
- Read context around each theme's findings
- Propose ONE resolution per theme (not per finding)
- Categorize: real inconsistency, false positive, or design tradeoff
- Update all findings in theme to `planned` status
- Handle unrelated findings individually (not by theme)

### Don't:

- ❌ Make edits during triage — propose only
- ❌ Dismiss findings — every finding gets a proposed resolution
- ❌ Triage findings within a theme one-by-one — work by theme
- ❌ Blame the reviewer — if an LLM got confused, another will too

### Triage Table

| Finding Type       | Resolution Type                 | Final Status (after Address) |
| ------------------ | ------------------------------- | ---------------------------- |
| Real inconsistency | Fix the document                | `fixed`                      |
| False positive     | Rewrite until intent is obvious | `clarified`                  |
| Design tradeoff    | Document rationale explicitly   | `clarified`                  |

Triage changes status from `open` → `planned`. Address phase changes `planned` → final status (`fixed` or `clarified`).

---

## Phase: Plan Approval

**Present findings and proposed resolutions to user BEFORE making any edits.**

This is the first human-in-the-loop checkpoint. The user can:

- Approve the plan and proceed to edits
- Modify proposed resolutions
- Add context or requirements
- Request different approaches

### Do:

- Present executive summary with findings and proposed resolutions
- Explain the reasoning behind each proposed resolution
- Use `AskUserQuestion` tool with clear options
- Wait for explicit approval before any edits

### Don't:

- ❌ Make edits before approval — this is a PLAN checkpoint
- ❌ Skip this checkpoint — human input is critical before changes
- ❌ Assume approval — wait for explicit response

### Plan Summary Template

Present the themes and proposed fixes from Triage. Present by theme; unrelated findings are listed individually. This makes review tractable for users.

```markdown
## Review Findings: {finding_count} findings in {theme_count} themes

### Theme 1: [theme name] ({n} findings)

**Root cause**: [why this pattern exists]

**Findings**: F-001, F-002, ...

**Proposed fix**: [single fix that resolves all findings in theme]

---

### Theme 2: [theme name] ({n} findings)

**Root cause**: [why this pattern exists]

**Findings**: F-003, F-004, ...

**Proposed fix**: [single fix that resolves all findings in theme]

---

### Unrelated findings ({n} findings)

These have no shared root cause; list individually:

**F-005** (line {n}): [issue description]

- Fix: [specific fix]

**F-006** (line {n}): [issue description]

- Fix: [specific fix]

---

### Summary

- {theme_count} themes covering {themed_findings} findings + {unrelated_count} unrelated = {total} findings
- {themed_findings} resolved via root-cause fixes, {unrelated_count} via standalone fixes
```

### Plan Approval Options

```
AskUserQuestion(
  questions: [{
    question: "Approve plan to address these findings?",
    header: "Plan",
    options: [
      {label: "Approve plan", description: "Proceed to make edits"},
      {label: "Modify plan", description: "I'll provide different approach"},
      {label: "Need more context", description: "Show me the relevant document sections"},
      {label: "Abort", description: "Do not make any changes"}
    ],
    multiSelect: false
  }]
)
```

---

## Phase: Address

**Execute the approved plan. Make edits to resolve all findings.**

### Do:

- Address all planned findings from the tracker
- Use `Edit` for targeted changes
- Update tracker status as you go (`planned` → `fixed` or `clarified`)
- Process unrelated findings individually

### Don't:

- ❌ Deviate from approved plan — execute what was approved
- ❌ Skip any finding — every approved resolution must be executed
- ❌ Make changes without reading the relevant sections first
- ❌ Over-edit — make minimal changes to resolve each finding

### Address Protocol

For each theme (or individual unrelated finding):

1. **Read context** — Read the section(s) containing the finding
2. **Identify resolution** — Fix, clarify, or document rationale
3. **Make edit** — Use Edit tool with precise old_string/new_string
4. **Update tracker** — Mark as `fixed` or `clarified` (from `planned`)

### Example: Addressing a Finding

```
Finding F-001: [issue description]

Resolution: [how to fix]

Edit(
  file_path: "{target_file}",
  old_string: "[text to replace]",
  new_string: "[replacement text]"
)

Update tracker: F-001 status → fixed
```

---

## Phase: Verify

**Verify all changes were made correctly.**

### Do:

- Re-read all sections that were modified
- Confirm each finding was properly addressed
- Check for unintended side effects from edits
- Ensure tracker shows all findings as `fixed` or `clarified`

### Don't:

- ❌ Skip verification — always re-read modified sections
- ❌ Proceed with unaddressed findings — all must be resolved

### Verification Checklist

```
[ ] All findings in tracker are `fixed` or `clarified`
[ ] Re-read each modified section
[ ] No new inconsistencies introduced by edits
[ ] Document still parses correctly (YAML frontmatter valid)
```

---

## Phase: Change Confirmation

**Present executed changes to user and get explicit confirmation.**

This is the second human-in-the-loop checkpoint. The user confirms the changes were executed correctly.

### Do:

- Present summary of changes made (not proposed — actually executed)
- Show which findings were resolved and how
- Use `AskUserQuestion` tool with clear options
- Wait for explicit confirmation

### Don't:

- ❌ Skip this checkpoint — human confirmation is mandatory
- ❌ Assume confirmation — wait for explicit response

Note: When there are no findings, this phase is skipped (see Parse Output).

### Change Summary Template

```markdown
## Changes Executed

### Findings Addressed: {finding_count}

| ID    | Line | Issue   | Resolution Applied |
| ----- | ---- | ------- | ------------------ |
| F-001 | {n}  | [issue] | [resolution]       |
| F-002 | {n}  | [issue] | [resolution]       |

### Edits Made

1. Line {n}: [change description]
2. Line {n}: [change description]

### Verification

- [ ] All planned resolutions executed
- [ ] Modified sections re-read
- [ ] No new inconsistencies introduced
```

### Confirmation Options

```
AskUserQuestion(
  questions: [{
    question: "Confirm changes were executed correctly?",
    header: "Confirm",
    options: [
      {label: "Confirm", description: "Changes look correct"},
      {label: "View diff", description: "Show git diff (requires git), then re-ask"},
      {label: "Revert", description: "Something went wrong, undo changes"},
      {label: "Modify", description: "Need additional changes"}
    ],
    multiSelect: false
  }]
)
```

---

## Phase: Epilogue

**Wrap up and report results.**

### Do:

- For no findings: Present "No findings." and end
- For findings addressed: Report what was fixed
- End the skill cleanly

### Don't:

- ❌ Skip the completion message — always report outcome
- ❌ Continue after reporting — the skill is complete

**For no findings**: Present "No findings." and end. (No user confirmation needed.)

**For findings addressed** (after user confirms changes):

1. Report results:

   ```
   Review complete.
   Findings: {finding_count} addressed
   ```

2. End the skill.

---

## Quick Reference: Don'ts

_Summary table — see each phase section for full context and rationale._

| Phase               | Don'ts                                                                                                                        |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Initialize          | Start without target file, review non-skill files                                                                             |
| Review              | Run sequentially, do the review yourself, customize prompts per reviewer                                                      |
| Parse Output        | Skip minor findings, proceed before all reviewers complete                                                                    |
| Synthesize          | Skip straight to triaging findings one-by-one, group mechanically without understanding, force unrelated findings into themes |
| Triage              | Make edits during triage, dismiss findings, triage findings within a theme one-by-one, blame reviewer                         |
| Plan Approval       | Make edits before approval, skip checkpoint, assume approval                                                                  |
| Address             | Deviate from plan, skip findings, edit without reading context, over-edit                                                     |
| Verify              | Skip verification, proceed with unaddressed findings                                                                          |
| Change Confirmation | Skip checkpoint, assume confirmation                                                                                          |
| Epilogue            | Skip completion message, continue after reporting                                                                             |

---

Begin /review-skill-parallel now. Parse args for target skill file path and -n flag (default: 3 reviewers). Launch n parallel reviewers in a single message with identical review prompts. Wait for all to complete. If all return NO FINDINGS, present "No findings." and proceed to Epilogue. Otherwise: synthesize findings into themes, triage by theme, get Plan Approval from user, execute the approved plan in Address, verify changes, and get Change Confirmation.
