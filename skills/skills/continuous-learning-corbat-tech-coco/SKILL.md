---
name: continuous-learning
description: Capture, organize, and apply learned patterns across sessions. Run at the end of any session where you solved something non-trivial. Concrete 4-step workflow.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Continuous Learning

Capture patterns from this session and build them into reusable tooling. Run at the end of any session where something non-trivial was solved.

## When to Use

- After solving a bug that took more than 30 minutes
- After figuring out a non-obvious pattern in corbat-coco
- After discovering a better way to do something recurring
- After writing code you'd want to reuse verbatim next time

## Exit Criteria

You're done when:
- At least one new skill or instinct has been saved
- `ls .claude/skills/learned/` shows new entries
- Any recurring workflow has a `/skill-create` generated skill

---

## Step 1: List What Was Learned This Session

Before capturing anything, explicitly state what was non-trivial:

```
What was hard about this session?
- [ ] Found a pattern I'll use again
- [ ] Fixed something non-obvious
- [ ] Discovered a better approach
- [ ] Identified a recurring workflow
```

If nothing qualifies, stop — don't save noise.

## Step 2: Capture Patterns with /learn

For each non-trivial finding, run:

```
/learn
```

This prompts you to describe the pattern. Be specific:
- **Bad**: "ESM imports need .js"
- **Good**: "When importing TypeScript source in Vitest, use `.js` not `.ts` — Node ESM resolves the compiled output path"

Saves to: `.claude/skills/learned/<pattern>/SKILL.md` (directory created automatically on first use)

Verify it saved:
```bash
ls .claude/skills/learned/
```

## Step 3: Generate Skills from Recurring Workflows

If you repeated a multi-step workflow more than once this session, generate a skill for it:

```
/skill-create
```

This analyzes recent git commits and creates a SKILL.md template. Review and edit before keeping.

Saves to: `.claude/skills/generated/<workflow>/SKILL.md`

If the generated skill is good, promote it:
```bash
mv .claude/skills/generated/<name> .claude/skills/<name>
```

## Step 4: Promote to rules/ if Always-Applicable

If the learned pattern should be active on every session (not just when you invoke a skill), add it to `rules/`:

```bash
# Add to existing rule file if it fits a category
printf '\n## Pattern: <Name>\n<content>\n' >> rules/typescript/patterns.md

# Or create a new rule file
touch rules/common/<new-pattern>.md
```

Use this sparingly — only for patterns that:
- Apply to every corbat-coco session
- Are non-obvious (not in official docs)
- Won't become outdated quickly

---

## Skill Quality Criteria

A skill is worth keeping if:
- ✅ Specific to corbat-coco (not in general TypeScript docs)
- ✅ Saves ≥5 minutes when applied
- ✅ Non-obvious
- ✅ Has a concrete code example
- ✅ States clearly when to apply it

## Directory Structure

```
.claude/skills/
├── (core skills — always available)
├── learned/          ← from /learn (raw session captures)
├── generated/        ← from /skill-create (needs review before promoting)
└── user-project/     ← skills for corbat-coco user projects, not corbat-coco itself
```

## Sharing with the Team

Commit promoted skills to share with the team:
```bash
git add .claude/skills/learned/<name>
git commit -m "chore(skills): add <pattern> instinct"
```
