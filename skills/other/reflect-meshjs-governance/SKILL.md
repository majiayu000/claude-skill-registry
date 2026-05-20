---
name: reflect
updated: 2026-02-20
description: Deep reflection on the skill learning system itself. Analyzes what's working, what's stale, and proposes structural improvements. The meta-skill.
argument-hint: "[focus area]"
user-invocable: true
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, AskUserQuestion
---

# Reflect — System Self-Improvement

A periodic deep-thinking session about the skill learning system itself. Like a craftsperson stepping back to look at their workshop — not the work, but the tools and how they're organized.

Run this when things feel off, when the system feels heavy, or just periodically to keep skills sharp and lean.

## Usage

```
/reflect              # Full reflection across everything
/reflect theming      # Focus on a specific area
```

## Arguments

- `$0` (optional) - Focus area: a skill name, "patterns", "journeys", or "system"

---

## Step 1: Gather the Full Picture

Read everything that makes up the learning system:

```
.claude/skills/*/SKILL.md          — All skill definitions
.claude/skills/_patterns.md        — Shared cross-cutting knowledge
.claude/skills/wrap-up/SKILL.md    — The learning engine
.claude/journeys/*.md              — Recent session learnings (last 5-10)
```

Also check:
- How many skills exist and their `updated` dates
- Which skills have been actively evolved
- Size of each SKILL.md (are any bloated?)

---

## Step 2: Analyze Through the Learning Lens

For each skill, consider:

### Is it earning its context window cost?
Every skill loaded into a session consumes tokens. A 500-line skill that's rarely used is expensive. Ask:
- When was it last updated? (stale = potentially wasteful)
- How specific and actionable are the instructions? (vague = not helping)
- Are there sections that repeat what's in `_patterns.md`? (duplicate = remove from skill)

### Is it accurate?
- Do the code examples match current codebase patterns?
- Are file paths and import references still correct?
- Have project conventions changed since the skill was written?

### Is it the right granularity?
- Too broad? Should it be split?
- Too narrow? Should it be merged with another skill?
- Is there knowledge trapped in journeys that should be in a skill?

### Is `_patterns.md` pulling its weight?
- Are there patterns in individual skills that should be shared?
- Are there stale patterns that no longer apply?
- Is there missing cross-cutting knowledge?

---

## Step 3: Check for Drift

Compare skill instructions against the actual codebase:

```bash
# Check if key files referenced in skills still exist
# Check if import patterns match reality
# Check if component names are current
```

Look for:
- Skills referencing files that moved or were renamed
- Code examples using old APIs or deprecated patterns
- Checklist items that are no longer relevant

---

## Step 4: Assess the Learning Loop Itself

Reflect on whether the system structure is working:

- **wrap-up**: Is it doing its job? Are skills actually getting better over time?
- **Learning notes**: Are `<!-- LEARNING -->` comments being used during work? If not, why?
- **Journeys**: Are they useful to future sessions or just noise?
- **_patterns.md**: Is it being referenced and kept current?

Look at recent journeys and see if the same mistakes keep recurring. If so, the learning loop has a gap — knowledge isn't reaching the right skill.

---

## Step 5: Present Findings

Use `AskUserQuestion` to present findings organized by priority:

### Categories:
1. **Stale** — Skills or sections that are outdated
2. **Bloated** — Skills that have grown too large for their value
3. **Missing** — Knowledge in journeys that should be in skills
4. **Duplicate** — Content repeated between skills and `_patterns.md`
5. **Structural** — Changes to how the system itself works

For each finding, propose a specific action:
- "Remove section X from skill Y (moved to _patterns.md)"
- "Update file paths in skill Z (files moved)"
- "Create new skill for W (pattern appears in 3+ journeys)"
- "Simplify wrap-up step 4 (too many substeps, never all followed)"

---

## Step 6: Implement Approved Changes

Apply the changes the user approves. This might include:
- Editing SKILL.md files
- Updating `_patterns.md`
- Creating new skills
- Removing or merging skills
- Restructuring the wrap-up workflow
- Archiving stale journeys

Update `updated` dates on any modified skills.

---

## When to Run This

- Every ~10 sessions or when you notice friction
- After a major project change (new framework, architecture shift)
- When skills feel "off" — producing wrong or outdated guidance
- When the skill system itself feels heavy or over-engineered

This is NOT a frequent tool. It's the periodic "sharpen the saw" moment.

---

## Philosophy

This skill exists because learning systems need to learn too.

A carpenter's workshop evolves — tools get reorganized, broken jigs get replaced, the workbench gets adjusted. But the carpenter doesn't reorganize every day. They do it when things feel wrong, or when they step back and see the clutter.

`/reflect` is that step back.
