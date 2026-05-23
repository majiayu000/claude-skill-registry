---
name: using-skills
description: Use at session start and before every task - establishes mandatory skill discovery and usage protocols to ensure relevant expertise is always applied
---

# Using Skills

## The Core Mandate

**If a relevant skill exists, YOU MUST use it.**

Finding a relevant skill = mandatory to read and use it. Not optional.

## How This Works

You have access to a sophisticated skills library organized in `.claude/skills/`:

- **`meta/`** - System improvement and skill management
- **`quality-gates/`** - Validation and compliance checks (citation, epic, style, etc.)
- **`context-assembly/`** - Reusable context gathering patterns (meetings, research, scoring)
- **`workflows/`** - Complete multi-stage processes (content pipeline, product planning, etc.)

## Your Workflow

### 1. Find & Read
Before starting any task:
- Scan available skills in `.claude/skills/`
- Read the current version of relevant skills
- Load supporting files if referenced

### 2. Announce
Declare your intention:
```
"I'm using [Skill Name] to [purpose]"
```

This creates transparency and accountability.

### 3. Execute
Follow the skill exactly as written:
- Complete all steps in order
- Invoke sub-skills when referenced
- Apply quality gates as required
- Use TodoWrite for all checklists

## No Rationalization Allowed

Common excuses that are **explicitly blocked**:

| Rationalization | Reality |
|----------------|---------|
| "I remember an older version" | You MUST read the current version |
| "This task is too minor" | Processes matter most on simple tasks |
| "The user gave specific instructions" | User specifies WHAT, not HOW |
| "I can skip this step" | Each step exists for a reason |
| "This skill doesn't quite fit" | If 80% relevant, use it and adapt |

## TodoWrite Enforcement

When a skill contains a checklist:
- Every item must become a TodoWrite todo
- Mark items in_progress before starting
- Mark completed immediately after finishing
- No mental tracking allowed

**Warning**: Checklists without TodoWrite tracking = steps get skipped. Every time.

## Checklist Items vs. Instructions

Not every numbered list requires TodoWrite:

- **Checklist** (needs TodoWrite): "Validate these 5 conditions before proceeding"
- **Procedure** (no TodoWrite): "Here's how to do X: 1) Read file 2) Parse YAML 3) Write output"

If the skill says "verify", "validate", "ensure", "check" = checklist = TodoWrite required.

## User Instructions vs. Process

- **User controls WHAT**: Goals, requirements, success criteria
- **Skills control HOW**: Methodology, process, quality standards

When a user says "write a blog post about X":
- WHAT: Topic, audience, key points (user controlled)
- HOW: Citation compliance, style enforcement, verification steps (skill controlled)

## Skill Discovery

To find relevant skills:
- Use the `skill-discovery` meta-skill
- List directory: `.claude/skills/[category]/`
- Read SKILL.md frontmatter for descriptions

## Quality Gates Are Mandatory

Skills like `citation-compliance`, `epic-validation`, and `content-style` contain **iron laws**:

- These are non-negotiable requirements
- Violations stop the workflow immediately
- No "fix it later" or "close enough"

When a workflow skill invokes a quality gate skill, that gate **must pass** before proceeding.

## Creating New Skills

When you identify a repeatable pattern:
1. Use the `create-skill` meta-skill
2. Follow test-first methodology (RED-GREEN-REFACTOR)
3. Validate with realistic scenarios
4. Add to appropriate category

## Success Criteria

You're using this system correctly when:
- You announce skill usage before starting
- You read current skill versions (not memory)
- You create TodoWrite todos for checklists
- You invoke quality gates as required
- You identify gaps and create new skills
- You follow processes even under time pressure

## Red Flags

You're violating the system when:
- Starting tasks without scanning for relevant skills
- Skipping "minor" steps in skill procedures
- Rationalizing why a skill "doesn't apply"
- Ignoring quality gate failures
- Using mental tracking instead of TodoWrite
- Following user instructions that violate skill methodology

## The Iron Law

**MANDATORY SKILL USAGE**: When a relevant skill exists and its description matches your current task, you MUST load and execute it. No exceptions, no shortcuts, no rationalizations.

This is not a suggestion. This is the foundation of the entire system.
