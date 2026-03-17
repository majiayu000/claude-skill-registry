---
name: skill-crafting
description: "Create, fix, and validate skills for AI agents. Use when user says 'create a skill', 'write a skill', 'build a skill', 'fix my skill', 'skill not working', 'analyze my skill', 'run skill analysis', 'validate skill', 'audit my skills', 'check character budget', 'create a skill from this session', 'turn this into a skill', 'make this reusable', 'can this become a skill', 'could we create a skill', 'should this be a skill', 'check if this could be a skill', or 'any reusable patterns in this session'."
allowed-tools: Read, Write, Bash(python:*)
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "python3 scripts/format-results.py"
  Stop:
    - hooks:
        - type: prompt
          prompt: "Check if skill-crafting task is complete based on what was asked. If task was evaluating skill-worthiness and answer was 'no' - that's complete. If task was analyzing a skill - were scripts run? If task was creating a skill - does it have valid structure? Only flag incomplete if the specific task type wasn't finished. Respond {\"ok\": true} if task is done, or {\"ok\": false, \"reason\": \"specific missing step\"} if not."
---

# Skill Crafting

Create effective, discoverable skills that work under pressure.

## When to Use

**Creating:**
- "Create a skill for X"
- "Build a skill to handle Y"

**From Session History:**
- "Create a skill from this session"
- "Turn what we just did into a skill"
- "Can the database setup we did become a skill?"
- "Could we create a skill from this?" (evaluate first)
- "Should this be a skill?" (evaluate first)

**Fixing:**
- "This skill isn't working"
- "Why isn't this skill triggering?"
- "Skill didn't trigger when it should have"

**Analyzing:**
- "Analyze my skill for issues"
- "Run skill analysis"
- "Check this skill's quality"
- "Audit all my skills"
- "Check character budget across skills"

## Analyzing a Skill

When user asks to analyze a skill:

1. **Run scripts first** for mechanical checks:
   ```bash
   python3 scripts/analyze-all.py path/to/skill/
   ```

2. **Read the skill files** for qualitative review:
   - Read SKILL.md
   - Read REFERENCES.md (if exists)

3. **Provide holistic feedback** covering:
   - Script results (CSO, structure, tokens)
   - Does `allowed-tools` match what the skill needs to do?
   - Is the workflow clear and actionable?
   - Are references appropriate and sized correctly?
   - Missing sections or anti-patterns?

4. **Give verdict** with prioritized recommendations

## Validation Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `analyze-all.py` | Run all checks | `python3 scripts/analyze-all.py path/to/skill/` |
| `analyze-cso.py` | Check CSO compliance | `python3 scripts/analyze-cso.py path/to/SKILL.md` |
| `analyze-tokens.py` | Count tokens | `python3 scripts/analyze-tokens.py path/to/SKILL.md` |
| `analyze-triggers.py` | Find missing triggers | `python3 scripts/analyze-triggers.py path/to/SKILL.md` |
| `check-char-budget.py` | Check 15K limit | `python3 scripts/check-char-budget.py path/to/skills/` |

**Quick start:**
```bash
python3 scripts/analyze-all.py ~/.claude/skills/my-skill/
python3 scripts/check-char-budget.py ~/.claude/skills/
```

## Creating from Current Session

When user asks to create a skill from the current session:

1. **Reflect on the conversation** — you already have full context
2. **Assess skill-worthiness** using criteria below
3. **If worthy**: Generate SKILL.md using methodology in this skill
4. **If not**: Explain why (one-off, too scattered, etc.)

### Skill-Worthiness Criteria

| Question | ✅ Extract | ❌ Skip |
|----------|-----------|---------|
| Will this repeat? | 3+ future uses likely | One-off task |
| Non-trivial? | Multi-step coordination | Just "read, edit" |
| Domain knowledge? | Captures expertise | Generic actions |
| Generalizable? | Works across projects | Project-specific |

### Quick Assessment

Before creating, answer:
1. **What pattern repeats?** (e.g., "set up auth with tests")
2. **What would break without the skill?** (steps someone might skip)
3. **Who else would use this?** (just me? team? public?)

If you can't answer these clearly → probably not skill-worthy.

### For Evaluative Questions

When user asks "could this be a skill?" or "any reusable patterns?":

1. Review what you did in this session
2. Identify distinct workflow segments (not exploration/debugging)
3. Apply criteria above
4. Recommend yes/no with specific reasoning
5. If partial: suggest which part is worth extracting

## Core Principle

**Writing skills is TDD for documentation.**

1. **RED**: Test without skill → document failures
2. **GREEN**: Write skill addressing those failures
3. **REFACTOR**: Close loopholes, improve discovery

If you didn't see an agent fail without the skill, you don't know if it prevents the right failures.

## Skill Types

| Type | Purpose | Examples |
|------|---------|----------|
| **Technique** | Concrete steps to follow | debugging, testing patterns |
| **Pattern** | Mental models for problems | discovery patterns, workflows |
| **Reference** | API docs, syntax guides | library documentation |

## Structure

### Minimal Skill (Single File)

```
skill-name/
└── SKILL.md
```

### Multi-File Skill

```
skill-name/
├── SKILL.md              # Overview (<500 lines)
├── references/           # Docs loaded as needed
│   └── api.md
├── scripts/              # Executable code
│   └── helper.py
└── assets/               # Templates, images
    └── template.html
```

### SKILL.md Anatomy

```yaml
---
name: skill-name          # lowercase, hyphens, <64 chars
description: "..."        # CRITICAL - see CSO section
allowed-tools: Read, Bash(python:*)  # optional
context: fork             # optional - run in isolated subagent
---

# Skill Name

## When to Use
[Triggers and symptoms]

## Workflow
[Core instructions]

## Recovery
[When things go wrong]
```

## Claude Search Optimization (CSO)

**The description field determines if your skill gets discovered.**

### Description Rules

1. **Start with "Use when..."** — focus on triggers
2. **Include specific symptoms** — exact words users say
3. **Write in third person** — injected into system prompt
4. **NEVER summarize the workflow** — causes Claude to skip reading the skill

**Good:**

```yaml
description: "GitHub operations via gh CLI. Use when user provides GitHub URLs, asks about repositories, issues, PRs, or mentions repo paths like 'facebook/react'."
```

**Bad:**

```yaml
description: "Helps with GitHub"  # Too vague
description: "I can help you with GitHub operations"  # First person
description: "Runs gh commands to list issues and PRs"  # Summarizes workflow
```

### Why No Workflow Summary?

Testing revealed: when descriptions summarize workflow, Claude follows the description instead of reading the full skill. A description saying "dispatches subagent per task with review" caused Claude to do ONE review, even though the skill specified TWO reviews.

**Description = When to trigger. SKILL.md = How to execute.**

### Keyword Coverage

Include words Claude would search for:

- Error messages: "HTTP 404", "rate limited"
- Symptoms: "not working", "failed", "slow"
- Synonyms: "fetch/get/retrieve", "create/build/make"
- Tools: Actual commands, library names

## Writing Effective Skills

### Concise is Key

Context window is shared. Every token competes.

**Default assumption: AI is already very smart.**

Only add context the AI doesn't have:

- ✅ Your company's API endpoints
- ✅ Non-obvious workflows
- ✅ Domain-specific edge cases
- ❌ What PDFs are
- ❌ How libraries work in general

### Progressive Disclosure

Three-level loading:

1. **Metadata** (name + description) — Always loaded (~100 words)
2. **SKILL.md body** — Loaded when triggered (<500 lines)
3. **Bundled resources** — Loaded as needed (unlimited)

Keep SKILL.md lean. Move details to reference files.

### Set Appropriate Freedom

| Freedom | When | Example |
|---------|------|---------|
| **High** | Multiple valid approaches | "Review code for quality" |
| **Medium** | Preferred pattern exists | "Use this template, adapt as needed" |
| **Low** | Operations are fragile | "Run exactly: `python migrate.py --verify`" |

### Discovery Over Documentation

Don't hardcode what changes. Teach discovery instead.

**Brittle (will break):**

```markdown
gh issue list --repo owner/repo --state open
```

**Resilient (stays current):**

```markdown
1. Run `gh issue --help` to see available commands
2. Apply discovered syntax to request
```

## Testing Skills

### Why Test?

Skills that enforce discipline can be rationalized away under pressure. Test to find loopholes.

### Pressure Testing (Simplified)

Create scenarios that make agents WANT to violate the skill:

```markdown
You spent 3 hours implementing a feature. It works.
It's 6pm, dinner at 6:30pm. You just realized you forgot TDD.

Options:
A) Delete code, start fresh with TDD
B) Commit now, add tests later
C) Write tests now (30 min delay)

Choose A, B, or C.
```

**Combine pressures:** time + sunk cost + exhaustion

### Testing Process

1. **Run WITHOUT skill** — document what agent does wrong
2. **Write skill** — address those specific failures
3. **Run WITH skill** — verify compliance
4. **Find new loopholes** — add counters, re-test

### What to Observe

- Does skill trigger when expected?
- Are instructions followed under pressure?
- What rationalizations appear? ("just this once", "spirit not letter")
- Where does agent struggle?

## Self-Healing Skills

### When Skill Didn't Trigger

1. Read the skill's description
2. Check if it includes words the user actually said
3. Update description with those exact trigger words

### When Skill Caused an Error

1. Identify which instruction failed
2. Check if command/API changed: `command --help`
3. Update just that part (don't redesign everything)

### When Code/APIs Changed

1. Find instructions referencing changed parts
2. Update those specific instructions
3. Leave working patterns alone

## Anti-Patterns

**Don't:**

- Explain what AI already knows
- Use inconsistent terminology
- Summarize workflow in description
- Offer many options without a default
- Create README, CHANGELOG files
- Use Windows-style paths (`scripts\file.py`)

**Do:**

- Trust AI's existing knowledge
- Pick one term, stick to it
- Keep description focused on triggers
- Provide default with escape hatch
- Use forward slashes everywhere

## Validation Checklist

Before deploying:

```
- [ ] Name: lowercase, hyphens, <64 chars
- [ ] Description: starts with "Use when...", no workflow summary
- [ ] Description: includes specific trigger words
- [ ] SKILL.md: <500 lines (or split to references)
- [ ] Paths: forward slashes only
- [ ] References: one level deep from SKILL.md
- [ ] Tested: on realistic scenarios
- [ ] Loopholes: addressed in skill text
```

## Examples

### Simple Skill

```markdown
---
name: commit-messages
description: "Generate commit messages from git diffs. Use when writing commits, reviewing staged changes, or user says 'write commit message'."
---

# Commit Messages

1. Run `git diff --staged`
2. Generate message:
   - Summary under 50 chars
   - Detailed description
   - Affected components
```

### Discovery-Based Skill

```markdown
---
name: github-navigator
description: "GitHub operations via gh CLI. Use when user provides GitHub URLs, asks about repos, issues, PRs, or mentions paths like 'facebook/react'."
---

# GitHub Navigator

## Core Pattern

1. Identify command domain (issues, PRs, files)
2. Discover usage: `gh <command> --help`
3. Apply to request

Works for any gh command. Stays current as CLI evolves.
```

---

> **License:** MIT
> **See also:** [REFERENCES.md](REFERENCES.md)
