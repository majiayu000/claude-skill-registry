---
version: 2.0.0
name: meta-continuous-learning
description: >
  Analyze session patterns and extract reusable skills, rules, or conventions.
  Turns recurring corrections, debugging techniques, and workarounds into
  permanent knowledge. Use when the user says "learn from this session",
  "extract patterns", "what did we learn", or at session wrap-up when
  significant patterns were discovered.
disable-model-invocation: true
user-invocable: true
argument-hint: "[--review | --extract | --adaptations | --status]"
---

# Continuous Learning — Session Pattern Extraction

Analyze the current session (or recent sessions) for patterns worth extracting
as reusable knowledge. This turns one-time fixes into permanent improvements.

## Philosophy

The agentic-workflow system has a memory hierarchy:

```
Session conversation (volatile — lost on context clear)
    ↓ wrap-up captures
Daily memory file (raw notes — kept 30 days)
    ↓ periodic distillation
MEMORY.md (curated wisdom — permanent)
    ↓ THIS SKILL extracts
New skills / rules / SOUL.md updates (actionable — permanent)
```

Most memory captures *what happened*. This skill captures *what to do differently*.

## When to Activate

- After a session where you had to correct Claude multiple times on the same issue
- When a debugging technique took effort to discover and will likely recur
- When you established a project convention that isn't obvious from the code
- When a workaround was needed for a tool, library, or framework quirk
- During `/meta-wrap-up` when the learnings section has significant entries
- When the user says "remember this pattern", "learn from this", "extract this"

## What to Extract

### Pattern Types

| Type | Example | Destination |
|------|---------|-------------|
| **Correction** | "Don't use `rm`, use `trash`" | `context/SOUL.md` or `.claude/rules/` |
| **Convention** | "Tests go in `__tests__/` next to source" | Project CLAUDE.md or rule file |
| **Technique** | "Debug Aspire by checking resource logs first" | New skill or MEMORY.md |
| **Workaround** | "EF Core needs explicit include for nested entities" | MEMORY.md or rule file |
| **Workflow** | "Always run `dotnet format` before committing C#" | New hook or skill |
| **Skill Adaptation** | "The TDD skill needs an Aspire integration phase" | `context/adaptations.md` |

### Confidence Assessment

Before extracting, assess confidence:

| Level | Criteria | Action |
|-------|----------|--------|
| **High** | Pattern observed 3+ times, user confirmed | Extract immediately |
| **Medium** | Pattern observed 1-2 times, seems generalizable | Extract as draft, flag for review |
| **Low** | Single occurrence, might be situational | Note in MEMORY.md, don't extract yet |

## Extraction Process

### Step 1: Identify Candidates

Review the session for extractable patterns:

1. Read today's daily memory file (`context/memory/{YYYY-MM-DD}.md`)
2. Check the session's Decisions and Learnings sections
3. Look at git diff for what was changed
4. Identify any corrections the user made ("no, don't do X, do Y instead")
5. Identify any debugging paths that were non-obvious

### Step 2: Categorize and Draft

For each candidate pattern:

1. Determine the best destination (see Pattern Types table above)
2. Draft the extraction:
   - **For SOUL.md updates:** Add to the Development Values or as a new section
   - **For rules:** Create a `.claude/rules/{topic}.md` file
   - **For skills:** Create a new skill in `.claude/skills/{category}-{name}/SKILL.md`
   - **For MEMORY.md:** Add to the Lessons Learned section
   - **For hooks:** Create or update a hook script

### Step 3: Present for Review

Present all candidates to the user in a table:

```
### Extracted Patterns

| # | Pattern | Confidence | Destination | Action |
|---|---------|-----------|-------------|--------|
| 1 | Always check resource logs before restarting Aspire services | High | MEMORY.md | Add to Lessons Learned |
| 2 | Use `trash` instead of `rm` for recoverable deletes | High | SOUL.md | Already there ✓ |
| 3 | Run dotnet format after C# edits | Medium | New hook | Draft hook script |

Apply all? Or select specific ones?
```

### Step 4: Apply

Only apply after user approval. For each approved pattern:

1. Write the extraction to its destination
2. Note in today's daily memory: "Extracted pattern: {description} → {destination}"
3. If a new skill was created, run `/meta-skill-catalog rebuild` to update the catalog

## Skill Adaptation Detection

When a pattern involves modifying an installed skill's behavior, log it as an adaptation
rather than (or in addition to) a regular extraction.

### When to Detect

- User corrects a skill's workflow ("don't do X in the TDD skill, do Y instead")
- A skill is edited directly (SKILL.md modified during the session)
- A workaround is needed because a skill doesn't cover a specific case

### Classification

| Classification | Meaning | Example |
|---|---|---|
| `universal` | Any project using this skill's stack would benefit | "TDD skill should handle integration tests with TestContainers" |
| `stack-specific` | Applicable to same stack but may need tweaks | "Verification should check Aspire health endpoints" |
| `project-specific` | Only relevant to this project | "TDD needs custom EventStoreTestFixture from this repo" |

### Logging to adaptations.md

Write adaptations to `context/adaptations.md`. Create the file if it doesn't exist.

Format:

```markdown
# Skill Adaptations

## {skill-name} (installed: {version})

### {YYYY-MM-DD} — {short description}
- **Classification:** {universal | stack-specific | project-specific}
- **What:** {What was changed or needs changing}
- **Why:** {Why the adaptation was needed}
- **Diff summary:** {Brief description of what changed in the SKILL.md}
- **Status:** {pending-contribution | local-only}
```

Set status to `pending-contribution` for universal/stack-specific adaptations,
`local-only` for project-specific ones.

### Integration with Wrap-Up

During `/meta-wrap-up`, if any skill was modified during the session:

```
[SKILL ADAPTATION] Detected modifications to dev-tdd-backend.
Classify this adaptation? (universal / stack-specific / project-specific / skip)
```

## Flags

| Flag | Behavior |
|------|----------|
| `--review` | Review recent sessions for unextracted patterns (read-only) |
| `--extract` | Run full extraction on current session |
| `--status` | Show what's been extracted recently (check daily memory files) |
| `--adaptations` | Review and classify skill modifications from this session |

## Anti-Pattern Guards

- **Don't extract obvious things:** "Use git for version control" is not a useful extraction
- **Don't extract one-offs:** A bug fix specific to one ticket isn't a pattern
- **Don't over-extract:** 2-3 patterns per session is a good rate; 10+ means you're being too granular
- **Don't skip review:** Always present candidates before applying
- **Don't create skills for simple rules:** A one-liner belongs in `.claude/rules/`, not a full skill

## Integration with Wrap-Up

During `/meta-wrap-up`, if the Learnings section has entries with high confidence:

```
[CONTINUOUS LEARNING] Found 2 patterns worth extracting:
1. "EF Core: always use .Include() for navigation properties in queries" (High)
2. "Aspire: check /health endpoint before assuming service is ready" (Medium)

Run /meta-continuous-learning --extract to formalize these, or skip.
```

This is a suggestion, not automatic. The user decides.
