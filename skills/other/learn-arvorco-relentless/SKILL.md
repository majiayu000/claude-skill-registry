---
name: learn
description: "Distill learnings from completed features and propose amendments to constitution.md or prompt.md. Use after feature completion. Triggers on: capture learnings, learn from feature, distill learnings, relentless learn."
---

# Relentless Learning System

Capture learnings from completed features and propose amendments to improve future runs.

**Philosophy**: "Loop Ralph" - Create a feedback loop where each feature execution improves the system for future features.

---

## SpecKit Workflow

This skill is **optional** and runs after feature completion:

specify → plan → tasks → convert → analyze → implement → **(optional) learn**

Prerequisites:
- Feature must be complete (all stories `passes: true` or `skipped: true`)
- `progress.txt` must exist with iteration learnings
- `prd.json` must exist with execution data
- `constitution.md` and/or `prompt.md` must exist in `relentless/`

---

## The Job

1. Extract learnings from completed feature (using CLI scripts)
2. Classify each learning (Constitutional / Tactical / Discard)
3. Generate proposals for human approval
4. Apply approved amendments to constitution.md or prompt.md
5. Save learning log to feature directory
6. Update aggregate stats

---

## Step 0: Run Extraction Scripts

**IMPORTANT**: Use CLI scripts for extraction - do NOT read entire files into context.

Run the extraction scripts from `.claude/skills/learn/scripts/`:

```bash
# Main extraction - runs all extractors
bash .claude/skills/learn/scripts/extract-learnings.sh relentless/features/<feature-name>

# Individual extractors (run by main script):
# - extract-patterns.sh - Patterns from progress.txt
# - extract-costs.sh - Cost accuracy from prd.json
# - extract-failures.sh - Failed checks from checklist.md
# - extract-errors.sh - Error patterns from progress.txt
```

The output is compact JSON (~500 tokens max):

```json
{
  "patterns": ["Pattern 1: description", "Pattern 2: description"],
  "costs": {"feature": "name", "estimated": 0.45, "actual": 0.52},
  "failures": ["Unchecked item 1", "Unchecked item 2"],
  "errors": ["Error context 1", "Error context 2"]
}
```

**If more context is needed for a specific story:**

```bash
# Extract session context for deeper investigation
bash .claude/skills/learn/scripts/extract-session-context.sh relentless/features/<feature-name> US-XXX
```

---

## Step 1: Parse Extracted Data

Parse the JSON output from the extraction scripts:

1. **Patterns**: Reusable learnings discovered during implementation
2. **Costs**: Cost accuracy metrics (estimated vs actual)
3. **Failures**: Unchecked checklist items (potential gaps)
4. **Errors**: Error patterns that were fixed (potential rules)

Count and categorize:
- How many patterns were discovered?
- Was cost estimation accurate (>80%)?
- Are there unchecked checklist items (quality gaps)?
- What error patterns emerged?

---

## Step 2: Classify Learnings

For each learning, classify as:

| Type | Target | Criteria | Example |
|------|--------|----------|---------|
| **Constitutional** | constitution.md | Applies to ALL features, governance/quality/process, prevents significant issues | "Always export new types with implementation" |
| **Tactical** | prompt.md | Specific to task types or tech stack, workflow tips, common pitfalls | "Mock CLI calls in adapter tests" |
| **Discard** | None | One-time edge case, already covered, too specific | "Fixed typo in variable name" |

**Constitutional criteria** (becomes a MUST or SHOULD rule):
- Applies universally to all features
- Related to governance, quality, or process
- Prevents significant issues if violated
- Not already covered in constitution

**Tactical criteria** (becomes a prompt.md pattern):
- Specific to certain task types or tech stack
- Workflow tip or common pitfall
- Helps agents avoid repeated mistakes
- Not governance-level

**Discard criteria** (do not propose):
- One-time edge case
- Already covered by existing rules
- Too specific to be reusable
- Subjective preference

---

## Step 3: Generate Proposals

Generate **maximum 5 constitutional + 5 tactical proposals** per feature.

### Constitutional Proposal Format:

```markdown
### PROP-C01: [Short Title]

**Target:** constitution.md > Principle [N] > [MUST|SHOULD]

**Amendment:**
> [1-2 sentence rule in imperative form]

**Evidence:**
> [Quote from progress.txt showing the issue]

**Classification:** Constitutional - [Rationale why this applies to all features]
```

### Tactical Proposal Format:

```markdown
### PROP-T01: [Short Title]

**Target:** prompt.md > [Section Name]

**Amendment:**
> [1-2 sentence tip or pattern]

**Evidence:**
> [Quote from progress.txt showing the context]

**Classification:** Tactical - [Rationale why this is task-specific]
```

### Discarded Learnings (include for transparency):

```markdown
### Discarded Learnings

| Learning | Reason |
|----------|--------|
| Fixed typo in variable name | One-time edge case |
| Used specific API endpoint | Already covered in docs |
```

---

## Step 4: Present for Human Approval

Use the proposal template from `templates/learning-proposal.md` to format the output.

The proposal should include:
1. **Feature Summary**: Name, stories, escalations, cost accuracy
2. **Constitutional Proposals**: PROP-C01, PROP-C02, etc.
3. **Tactical Proposals**: PROP-T01, PROP-T02, etc.
4. **Discarded Learnings**: With reasons
5. **Approval Request**: Ask user to approve, modify, or reject each proposal

**Ask the user:**
```
Please review the proposals above. For each one:
- APPROVE: Apply as written
- MODIFY: Suggest changes
- REJECT: Do not apply

Which proposals do you approve?
```

---

## Step 5: Apply Approved Amendments

For each approved proposal:

### Constitutional Amendments (constitution.md):

1. Read current version from constitution.md frontmatter
2. Find the appropriate Principle section
3. Add the new rule under MUST or SHOULD
4. Update version number:
   - **MUST rules**: Bump MINOR version (e.g., 2.0.0 → 2.1.0)
   - **SHOULD rules**: Bump PATCH version (e.g., 2.0.0 → 2.0.1)
5. Update `LAST_AMENDED_DATE` to today
6. Add amendment note at top of file

**Amendment note format:**
```markdown
<!-- Amendment: v2.1.0 - Added [rule title] from feature [feature-name] -->
```

### Tactical Amendments (prompt.md):

1. Find the appropriate section in prompt.md
2. Add the new pattern or tip
3. Update "Generated" date at bottom
4. If no appropriate section exists, create a new "## Learned Patterns" section

---

## Step 6: Save Learning Log

Create a learning log file in the feature directory:

**Path:** `relentless/features/<feature-name>/learnings.md`

```markdown
# Learnings: [Feature Name]

**Extracted:** [date]
**Proposals Generated:** [count]
**Approved:** [count]
**Applied:** [count]

## Constitutional Amendments Applied

- PROP-C01: [Title] → constitution.md v[version]

## Tactical Amendments Applied

- PROP-T01: [Title] → prompt.md

## Discarded Learnings

- [Learning] - [Reason]

---

*Generated by /relentless.learn*
```

---

## Step 7: Update Aggregate Stats

Run the stats generator to update `relentless/stats.md`:

```bash
bash .claude/skills/learn/scripts/generate-stats.sh relentless
```

This generates a human-readable report with:
- Total features, stories, completion rate
- Cost summary (estimated vs actual)
- Token usage
- Complexity distribution
- Escalation rate
- Model usage breakdown

The stats file is for human review, NOT loaded into agent context.

---

## Version Bumping Rules

| Amendment Type | Version Bump | Example |
|----------------|--------------|---------|
| MUST rule | MINOR | 2.0.0 → 2.1.0 |
| SHOULD rule | PATCH | 2.0.0 → 2.0.1 |
| Multiple rules | Highest bump applies | 2.0.0 → 2.1.0 if any MUST |

**Never bump MAJOR** - only `/relentless.constitution` can do that (for breaking governance changes).

---

## Common Patterns to Look For

### Constitutional-Level Patterns:
- Type safety rules (export types with implementation)
- Testing patterns (TDD workflow, test structure)
- Error handling patterns (graceful degradation)
- Documentation requirements (JSDoc, README updates)
- Code quality patterns (zero-lint, typecheck)

### Tactical-Level Patterns:
- Schema naming conventions (XxxSchema for Zod)
- Mock patterns for testing (mock CLI, mock adapters)
- File organization patterns (where to put new files)
- Common pitfalls for specific tech stack
- Performance optimizations

### Patterns to Discard:
- Typo fixes
- One-time debugging steps
- Temporary workarounds (already removed)
- Personal preferences (formatting choices)
- Already documented patterns

---

## Example Session

**Input:**
```
/relentless.learn 001-queued-prompts
```

**Extraction Output:**
```json
{
  "patterns": [
    "Atomic writes: Use temp file + rename for safety",
    "Zod naming: Use XxxSchema to avoid no-redeclare"
  ],
  "costs": {"estimated": 0.45, "actual": 0.52, "accuracy": "87%"},
  "failures": [],
  "errors": ["ESLint no-redeclare on UserStory type - fixed with XxxSchema pattern"]
}
```

**Generated Proposals:**
```markdown
### PROP-C01: Atomic Write Pattern

**Target:** constitution.md > Principle 11 (Data Safety) > SHOULD
**Amendment:**
> Use atomic writes (temp file + rename) when modifying files to prevent corruption.

**Evidence:**
> "Uses atomic writes (temp file + rename) to prevent corruption" - progress.txt

**Classification:** Constitutional - Applies to all file-modifying operations across features
```

**User Response:** "APPROVE PROP-C01"

**Applied:** constitution.md v2.0.1 updated with new SHOULD rule

---

## Notes

- This skill is **opt-in** - only run after user decides to capture learnings
- Maximum 10 proposals per feature to avoid overwhelming the user
- Use extraction scripts to minimize context usage
- Human approval required for all amendments
- Stats file is for transparency, not agent context
- Session context extraction is available for deeper investigation when needed
