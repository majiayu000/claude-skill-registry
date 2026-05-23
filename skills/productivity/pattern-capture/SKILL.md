---
name: pattern-capture
description: "This skill should be used when the user asks to 'find repeated feedback', 'what do I keep correcting', 'capture this pattern', 'DRY my prompting', 'stop repeating myself', 'turn this into a check', 'automate this correction', or when the same type of feedback has been given 3+ times across sessions."
user-invocable: false
---

# Pattern Capture

Detect repetitive feedback across sessions and convert it into the right enforcement artifact — a memory entry, a validation hook, an enforcement pattern, or a standalone skill.

## The Problem This Solves

Users give the same corrections repeatedly:
- "Don't mock the database in tests" (session 1, 3, 7, 12)
- "Use jq explicit syntax, not shorthand" (session 2, 5, 8)
- "Check the build before claiming it works" (session 1, 4, 6, 9, 11)

Each correction costs the user time and erodes trust. The DRY principle applies to prompting: **if you've said it twice, it should be automated.**

## When to Use

- User says "I keep telling you..." or "Again, don't..."
- You notice you're receiving the same type of correction
- At end of session, to audit what feedback was given
- Proactively, when continuous-learning detects `user_corrections` patterns
- User explicitly asks to capture a pattern or DRY their prompting

## Process

### Step 1: Gather Evidence

Collect instances of the repeated pattern. Sources (check in order):

```
1. Memory files (fastest)
   → Grep pattern="<keyword>" path="<memory_dir>" glob="*.md"
   → Look for feedback-type memories

2. Session transcripts (if CLAUDE_TRANSCRIPT_PATH is set)
   → Grep for user corrections: "no", "don't", "stop", "again", "I said"
   → Count occurrences of similar corrections

3. Spotless archives (if available, cross-session)
   → Search conversation history for repeated correction patterns

4. User report (always valid)
   → User says "I keep having to tell you X" = sufficient evidence
```

**Minimum evidence threshold:** 2 independent instances (same correction, different contexts). A single user report of "I keep telling you" counts as meeting threshold — trust the user's observation.

### Step 2: Classify the Pattern

Every repeated pattern maps to exactly ONE artifact type. Use this decision tree. **Evaluate branches top-to-bottom; stop at the FIRST match.**

```
Is the pattern about WHEN to do something?
  YES → Is it about tool/command selection?
    YES → MEMORY (feedback type)
    NO  → Is it about workflow sequencing?
      YES → ENFORCEMENT PATTERN (add to existing workflow skill)
      NO  → MEMORY (feedback type)
  NO  →
Is the pattern about HOW to do something?
  YES → Is it a single rule (< 3 sentences)?
    YES → Is it project-specific?
      YES → MEMORY (project type)
      NO  → MEMORY (feedback type)
    NO  → Does it require multi-step verification?
      YES → VALIDATION HOOK
      NO  → Is it reusable across projects?
        YES → SKILL (learned skill)
        NO  → MEMORY (feedback type)
  NO  →
Is the pattern about WHAT NOT to do?
  YES → Can the violation be detected programmatically?
    YES → VALIDATION HOOK
    NO  → RED FLAG (add to existing skill's Red Flags table)
  NO  →
Default → MEMORY (feedback type)
```

#### Artifact Type Reference

| Artifact | When | Example | Where It Lives |
|----------|------|---------|----------------|
| **Memory (feedback)** | Simple behavioral rule | "Don't add trailing summaries" | `<memory_dir>/feedback_*.md` |
| **Memory (project)** | Project-specific convention | "jq 1.6 in container, use explicit syntax" | `<memory_dir>/project_*.md` |
| **Enforcement pattern** | Workflow drift prevention | "Must run build before claiming completion" | Added to existing SKILL.md |
| **Validation hook** | Programmatically checkable | "No mocks in integration tests" | PreToolUse/PostToolUse hook |
| **Red Flag entry** | Anti-pattern with observable trigger | "About to use `git add .`" | Added to existing skill's table |
| **Learned skill** | Multi-step reusable procedure | "Debug pixi environment issues" | `~/.claude/skills/learned/` |

### Step 3: Generate the Artifact

Based on classification, generate the appropriate artifact:

#### For MEMORY entries

```markdown
---
name: feedback_<descriptive-slug>
description: <one-line description specific enough to match in future>
type: feedback
---

<The rule, stated clearly>

**Context:** <Why this matters — what went wrong when it was violated>
**Source:** <How this was discovered — "corrected N times" or "user reported">
```

Write to memory directory and update MEMORY.md index.

#### For ENFORCEMENT PATTERNS (added to existing skills)

Identify which skill the pattern belongs to, then add the appropriate enforcement element:

**Iron Law** (for high-drift actions the agent rationalizes skipping):
```markdown
<EXTREMELY-IMPORTANT>
**[RULE IN ALL CAPS]. This is not negotiable.**

[One sentence explaining concrete user harm if violated.]
</EXTREMELY-IMPORTANT>
```

**Rationalization Table entry** (for patterns where the agent makes excuses):
```markdown
| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "<exact excuse the agent generates>" | "<why this is wrong>" | "<correct action>" |
```

**Red Flag entry** (for observable wrong actions):
```markdown
| Action | Why It's Wrong | Do Instead |
|--------|----------------|------------|
| "<observable behavior>" | "<concrete harm>" | "<correct alternative>" |
```

#### For VALIDATION HOOKS

Generate a PreToolUse or PostToolUse hook:

```typescript
// hooks/<hook-name>.ts
// Pattern: <description of what this catches>
// Source: User corrected this N times across sessions

export default {
  event: "PreToolUse",  // or PostToolUse
  name: "<tool-name>",  // e.g., "Bash", "Write", "Edit"
  async handler({ input }) {
    // Detection logic
    const violation = /* check for the anti-pattern */;
    if (violation) {
      return {
        decision: "block",  // or "ask"
        reason: "<explanation of why this is blocked>"
      };
    }
    return { decision: "approve" };
  }
};
```

#### For LEARNED SKILLS

Delegate to skill-creator:
```
Skill(skill="skill-creator", args="Create skill from captured pattern: <description>")
```

Provide the skill-creator with:
- Pattern description and evidence
- Example correct/incorrect behaviors
- Suggested enforcement level (from classification)

### Step 4: Verify Integration

After generating the artifact, verify it's properly integrated:

| Artifact Type | Verification |
|---------------|-------------|
| Memory | `Grep` for the memory file, verify MEMORY.md updated |
| Enforcement pattern | Read the modified SKILL.md, verify pattern appears in correct section |
| Validation hook | Syntax check the hook file, verify it's in the right hooks directory |
| Red Flag entry | Read the modified skill, verify table is well-formed |
| Learned skill | Verify SKILL.md exists with frontmatter, description is trigger-only |

### Step 5: Report

Output a summary:

```
## Pattern Captured

**Pattern:** <one-line description>
**Evidence:** <N instances across M sessions>
**Classification:** <artifact type>
**Artifact:** <file path or location>
**Prevention:** <how this prevents future repetition>
```

## Proactive Detection

When invoked without a specific pattern (e.g., "find repeated feedback"), scan all available sources:

1. Read all feedback-type memory files
2. Search session transcripts for correction language:
   - `"no,? (don't|stop|not|never|instead|again)"`
   - `"I (already|just) (told|said|asked|mentioned)"`
   - `"(wrong|incorrect|that's not|not what I)"`
3. Group similar corrections by semantic similarity
4. For each group with 2+ instances, run the classification tree
5. Present findings to user for confirmation before generating artifacts

## Iron Laws

<EXTREMELY-IMPORTANT>
**NEVER GENERATE AN ARTIFACT WITHOUT EVIDENCE. This is not negotiable.**

Fabricating patterns the user hasn't actually repeated leads to over-engineered enforcement that constrains legitimate behavior. Every artifact must trace to specific observed instances.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
**NEVER ADD ENFORCEMENT TO A SKILL WITHOUT READING THE FULL SKILL FIRST. This is not negotiable.**

Adding a Red Flag or Iron Law without understanding the skill's existing enforcement creates conflicts, duplicates, and confusion. Read the entire SKILL.md before modifying it.
</EXTREMELY-IMPORTANT>

## Red Flags - STOP If You Catch Yourself:

| Action | Why It's Wrong | Do Instead |
|--------|----------------|------------|
| Creating a skill for a one-sentence rule | Over-engineering; a memory entry suffices | Use the classification tree — simple rules are memories |
| Adding enforcement without observed violations | Speculative enforcement constrains legitimate work | Wait for 2+ real instances before adding enforcement |
| Modifying a skill you haven't read | You'll create conflicts with existing patterns | Read the full SKILL.md first |
| Creating a validation hook for a subjective rule | Hooks need programmatic detection; "code quality" isn't checkable | Use a Red Flag or memory instead |
| Skipping user confirmation for proactive detection | You might misclassify the pattern or the user might disagree | Always present findings before generating |

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "This pattern is obvious, it doesn't need evidence" | Obvious patterns are obvious TO YOU — the user may not have this correction in mind | Find concrete instances before generating |
| "A skill is more powerful than a memory" | Power isn't the goal; fit is. Most patterns are simple rules that belong in memory | Use the classification tree honestly |
| "I'll add this to all relevant skills" | Shotgun enforcement creates maintenance burden and contradictions | Add to the ONE most relevant skill |
| "Adding this rule now will prevent future issues" | Speculative enforcement without observed drift adds cognitive cost and devalues existing Iron Laws | Only add enforcement for patterns with real observed drift |

## Integration Points

| System | How Pattern-Capture Integrates |
|--------|-------------------------------|
| **continuous-learning** | Consumes `user_corrections` patterns as input; pattern-capture classifies and routes them |
| **skill-creator** | Delegates learned skill generation; provides evidence and enforcement level |
| **workflow-creator** | Informational — when adding enforcement to a workflow skill, consult workflow-creator's audit mode to verify the addition fits the workflow's phase structure |
| **Memory system** | Primary output target — most patterns become feedback memories |
| **Hook system** | Secondary output — programmatically detectable anti-patterns become hooks |

## Examples

### Example 1: Simple Behavioral Rule → Memory

**Evidence:** User said "stop summarizing at the end" in 3 sessions
**Classification:** WHEN to do something → tool selection? No → workflow? No → MEMORY (feedback)
**Artifact:**
```markdown
---
name: feedback_no_trailing_summaries
description: Do not add summary paragraphs after completing a task — user reads diffs directly
type: feedback
---
Do not summarize what you just did at the end of responses. The user reads diffs and tool output directly.

**Context:** Trailing summaries waste time and feel patronizing to experienced users.
**Source:** Corrected 3 times across sessions.
```

### Example 2: Build Verification → Enforcement Pattern

**Evidence:** Agent claimed "build passes" without running build in 4 sessions
**Classification:** HOW → multi-step verification? Yes → but dev-verify already handles this → ENFORCEMENT PATTERN
**Artifact:** Add to dev-verify's Red Flags table:
```markdown
| "Build should still pass from earlier" | Earlier results are stale — any code change invalidates them | Run `npm run build` fresh RIGHT NOW |
```

### Example 3: No Mocks in Integration Tests → Validation Hook

**Evidence:** Agent used jest.mock() in integration test files 3 times
**Classification:** WHAT NOT TO DO → programmatically detectable? Yes (grep for `jest.mock` in `tests/integration/`) → VALIDATION HOOK
**Artifact:** PostToolUse hook on Write/Edit that warns when `jest.mock` appears in integration test files.

### Example 4: Project-Specific Convention → Project Memory

**Evidence:** User corrected jq syntax 3 times — container uses jq 1.6, not 1.7
**Classification:** HOW → single rule → project-specific → MEMORY (project)
**Artifact:**
```markdown
---
name: project_jq_16_explicit_syntax
description: NanoClaw container runs jq 1.6 which requires explicit field syntax, not shorthand
type: project
---
Container runs jq 1.6. Always use explicit syntax: `{title: .title}` not `{title, location: expr}`.

**Applies to:** NanoClaw container agent, any jq commands in container scripts.
**Context:** jq 1.6 does not support mixing shorthand + explicit fields. Causes silent failures.
**Source:** Corrected 3 times across sessions.
```

### Example 5: Complex Debugging Procedure → Learned Skill

**Evidence:** User walked through the same pixi debugging steps in 3 sessions
**Classification:** HOW → single rule? No (5+ steps) → multi-step verification? No → reusable? Yes → SKILL
**Artifact:** Delegate to skill-creator with the debugging steps as input.

## References

- **Classification quick reference:** `references/classification-guide.md` — fast-path matrix and enforcement strength ladder
- **Artifact templates:** `references/artifact-templates.md` — copy-paste templates for all artifact types with formatting guidance
- **Enforcement checklist:** `references/enforcement-checklist.md` — full 12-pattern reference (when adding enforcement to existing skills)
- **Continuous-learning:** `../continuous-learning/SKILL.md` — upstream pattern detection (feeds into this skill)
- **Skill-creator:** `../skill-creator/SKILL.md` — downstream skill generation (this skill delegates to it for learned skills)
