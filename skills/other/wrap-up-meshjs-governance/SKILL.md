---
name: wrap-up
updated: 2026-02-20
description: End-of-session automation. Creates a journey, consolidates learning notes, evolves skills, cross-pollinates shared patterns.
argument-hint: [title]
user-invocable: true
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Session Wrap-Up

The single learning engine for the skill system. Mirrors how learning works in nature:

```
Experience (work) → Awareness (learning notes) → Consolidation (wrap-up)
```

## Usage

```
/wrap-up {session title}
```

## Arguments

- `$0` - Session title describing the main work done (e.g., "Auth System Refactor")

---

## Step 1: Gather All File Changes

**CRITICAL**: Before anything else, run git commands to capture ALL changes. In long sessions, memory alone will miss things.

```bash
git status
git diff HEAD
git ls-files --others --exclude-standard
```

From the output, build a comprehensive list of:
- All modified files and what changed
- All new files created
- All deleted files
- Nature of changes (bug fix, feature, refactor, etc.)

**DO NOT proceed to Step 2 until git output is reviewed.**

---

## Step 2: Create Journey

Using file changes from Step 1 AND conversation context, create a journey at `.claude/journeys/{date}-{slug}.md`.

Include:
- **Summary**: What was accomplished and why it matters
- **What Was Done**: Numbered list of major items
- **Key Learnings**: Insights that prevent future mistakes
- **Files Changed**: Table of files and changes
- **Patterns Discovered**: Code examples of reusable patterns
- **Decisions Made**: Table of decisions and rationale

---

## Step 3: Process Learning Notes

Search ALL skill files for inline learning notes left during the session:

```bash
grep -r "<!-- LEARNING" .claude/skills/
```

For each learning note found:
1. **Read the note** and its surrounding context in the SKILL.md
2. **Integrate** the learning into the skill's proper text — rewrite the relevant section to include the new knowledge naturally
3. **Remove the raw note** — the `<!-- LEARNING ... -->` comment gets replaced by the integrated content
4. **Update the `updated` date** in the skill's frontmatter

### Learning Note Format (for reference)

During work, learning notes are left inline:
```markdown
### Some Section
Existing instruction text...

<!-- LEARNING 2026-02-04: Discovered that X actually needs Y because Z -->
```

After consolidation, the section reads naturally with the learning absorbed:
```markdown
### Some Section
Existing instruction text. Note: X needs Y because Z.
```

---

## Step 4: Evolve Skills from Journey

Read all skills from `.claude/skills/*/SKILL.md` and compare against journey learnings.

For each skill, check:
- Does the journey contain patterns the skill should document?
- Were there edge cases or gotchas the skill should warn about?
- Are there new verification checklist items?
- Did we discover something that contradicts current skill instructions?

For each skill that needs updates:
1. Read current SKILL.md
2. Apply changes based on learnings
3. Update the `updated` date in frontmatter

---

## Step 5: Cross-Pollinate Shared Patterns

Check if any learnings from the session apply across multiple skills.

1. Read `.claude/skills/_patterns.md`
2. If a learning is cross-cutting (applies to multiple skills), add it to `_patterns.md`
3. If a pattern in `_patterns.md` is outdated based on session work, update it

---

## Step 6: Prune Stale Content

Review skills touched during the session. Look for:
- Sections documenting patterns for deprecated/removed features
- Duplicate content that now lives in `_patterns.md`
- Instructions that conflict with current codebase reality

If something looks stale, remove it. Keep skills lean — context window space is valuable.

---

## Step 7: Update Journey with Evolutions

Add a section to the journey documenting skill changes:

```markdown
## Skills Evolved

| Skill | Changes |
|-------|---------|
| build-fix | Added new error pattern |
| _patterns | Updated data conventions |
```

---

## Skill Evolution Guidelines

| Session Content | Action |
|-----------------|--------|
| New code pattern | Add to relevant skill's patterns section |
| Bug fix with root cause | Add to gotchas/checklist in relevant skill |
| Cross-cutting convention | Update `_patterns.md` |
| Framework gotcha | Update `_patterns.md` with framework section |

---

## Example Output

```
Session: Auth System Refactor

1. Gathered file changes (8 modified, 2 created)
2. Created journey: .claude/journeys/2026-02-20-auth-system-refactor.md
3. Processed 2 learning notes:
   - security-review: integrated JWT expiry check
   - code-review: updated auth pattern
4. Evolved 2 skills from journey learnings:
   - security-review: added session management checks
   - verify: added auth-specific verification step
5. Cross-pollinated: added auth convention to _patterns.md
6. Pruned: removed outdated cookie example from security-review
7. Updated journey with evolution summary
```
