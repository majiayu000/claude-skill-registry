---
name: promptcraft
description: >
  Use when user asks to "create a skill", "make a command", "generate a prompt",
  "write a slash command", "build a Claude extension", or needs help crafting
  optimized skills and commands with proper frontmatter.
argument-hint: "[skill|command] [name] - or leave empty to interview"
---

# Skill & Command Generator

Generate well-structured skills or slash commands. Both are markdown files with YAML frontmatter—they share the same structure but differ in how they're triggered and described.

## Phase 0: Fetch Current Documentation

**Before generating**, retrieve the latest documentation:

```
Use Task tool with subagent_type=claude-code-guide:
"List all current frontmatter options for skills and commands, including any execution modifiers, model selection, and structural options."
```

Integrate findings into your generation process. Documentation evolves—don't assume you know all options.

## Context Engineering

Every token counts. LLM context is finite. Goal: smallest possible set of high-signal tokens that maximize outcomes

| Do | Don't |
|---|---|
| "Validate input before processing" | "You should always make sure to validate..." |
| "Use grep to search" | "You might want to consider using..." |
| Bulleted constraints | Paragraphs with buried requirements |
| Imperative voice ("Analyze") | First person ("I will analyze") |

**Progressive discovery:** Core instructions in main file, details in `references/` subdirectory. Just-in-time information > front-loaded context
**Trust Claude:** Provide direction, not dictation. Claude extrapolates well from precise nudges.
**Optimize Signal-to-Noise:** Clear, direct language over verbose explanations. High-value tokens that drive behavior

### Degrees of Freedom

Match specificity to the task's fragility and variability:

| Level | When to Use | Format |
|-------|-------------|--------|
| **High freedom** | Multiple valid approaches, context-dependent decisions | Text instructions, heuristics |
| **Medium freedom** | Preferred pattern exists, some variation acceptable | Pseudocode, scripts with parameters |
| **Low freedom** | Fragile operations, consistency critical, specific sequence required | Exact scripts, few parameters |

Think of it as path guidance: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

## Phase 1: Understand Requirements

Parse `$ARGUMENTS` for type hint. If unclear, use AskUserQuestion:
- "Are you creating a skill (auto-triggered by description) or a command (user-invoked via /slash)?"

Gather requirements (interview user using `/interview`):
1. **Primary objective** - What should this do?
2. **Trigger scenarios** - When should it activate?
3. **Inputs/outputs** - What does it receive and produce?
4. **Complexity** - Simple, standard, or complex?
5. **Execution needs** - Isolated context? Delegated to specialized agent?

## Phase 2: Generate

Skills and commands share the same structure. The key difference is in the **description**:
- **Skills:** Trigger-rich, third-person ("This skill should be used when...")
- **Commands:** Concise, verb-first, under 60 chars

### Common Frontmatter Options

```yaml
---
name: identifier                    # Required for skills
description: >                      # How it's described/triggered
  [See description patterns below]

# Execution modifiers
model: sonnet                       # haiku (fast), sonnet (balanced), opus (complex)
context: fork                       # Run in isolated sub-agent, preserves main context
agent: Explore                      # Route to specialized agent (Explore, Plan, custom)

# Tool access
allowed-tools:                      # Restrict available tools
  - Read
  - Grep
  - Bash(git:*)

# Lifecycle hooks (optional)
hooks:
  PreToolUse:
    - command: "validation-script.sh"
  PostToolUse:
    - command: "cleanup.sh"

# Behavior modifiers
user-invocable: true                # Show in /command menu (default true)
disable-model-invocation: true      # Prevent programmatic invocation (commands only)
argument-hint: [arg1] [arg2]        # Document expected arguments (commands only)
---
```

### Description Patterns

**For Skills (auto-triggered):**

Write in third-person with 3-5 varied trigger phrases:

```yaml
# Good - trigger-rich
description: >
  This skill should be used when the user asks to "create a hook",
  "add validation", "implement lifecycle automation", or mentions
  pre/post tool events.

# Bad - vague
description: Provides guidance for hooks.
```

**For Commands (user-invoked):**

Write concise, verb-first, under 60 chars:

```yaml
description: Fix GitHub issue by number
description: Review code for security issues
description: Deploy to staging environment
```

### Body Structure

Both skills and commands follow the same body pattern:

```markdown
# Name

Brief overview (1-2 sentences).

## Process
1. Step one (imperative voice)
2. Step two
3. Step three
```

**Key principle**
- Commands are instructions FOR Claude, not TO the user.

**Construction Rules:**
- State objective explicitly in first sentence
- Use imperative voice ("Analyze", "Generate", "Identify")
- No first-person narrative ("I will", "I am")
- Context only when necessary for understanding
- XML tags only for complex structured data
- Examples only when they clarify expectations
- Every word must earn its place

### Dynamic Content

| Syntax | Purpose |
|--------|---------|
| `$ARGUMENTS` | All arguments as string |
| `$1`, `$2`, `$3` | Positional arguments |
| `@path/file` | Load file contents |
| `@$1` | Load file from argument |
| Exclamation + backticks | Execute bash command, include output |

### Progressive Disclosure

For complex skills, organize into subdirectories:

```
skill-name/
├── SKILL.md          # Core instructions (keep under 500 lines)
├── scripts/          # Executable code (Python/Bash)
├── references/       # Docs loaded into context as needed
└── assets/           # Files used in output (templates, icons, fonts)
```

**scripts/** - Deterministic, token-efficient. May be executed without loading into context. Use when the same code is rewritten repeatedly or reliability is critical.

**references/** - Documentation Claude reads while working. Keeps SKILL.md lean. For files >100 lines, include a table of contents. Only load when needed.

**assets/** - Files NOT loaded into context. Used in output: templates, images, fonts, boilerplate. Example: `assets/hello-world/` for a React template.

#### Progressive Disclosure Patterns

**Pattern 1: High-level guide with references**

```markdown
# PDF Processing

## Quick start
Extract text with pdfplumber:
[code example]

## Advanced features
- **Form filling**: See references/forms.md
- **API reference**: See references/api.md
```

Claude loads references only when needed.

**Pattern 2: Domain-specific organization**

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing)
    ├── sales.md (pipeline, opportunities)
    └── product.md (API usage, features)
```

When user asks about sales, Claude only reads sales.md.

**Pattern 3: Variant-based organization**

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

User chooses AWS → Claude only reads aws.md.

### Execution Modifiers

Use these when the default behavior isn't sufficient:

- **`context: fork`** — Run in isolated sub-agent. Use for heavy workflows that would pollute main context, or when you need clean separation.

- **`agent: [type]`** — Route to a specialized agent. Examples: `Explore` for codebase search, `Plan` for architecture decisions, or custom agents you've defined.

- **`model: [level]`** — Override the model. Use `sonnet` for balance, `opus` for complex analysis requiring deep reasoning.

- **`hooks`** — Run scripts before/after tool use. Useful for validation, logging, or side effects.

### Tool Selection

Default generous, restrict only when needed:

- **Always allow:** Read, Grep, Glob
- **Usually allow:** Edit, Write, WebSearch, Task
- **Scope Bash:** Use patterns like `Bash(git:*)`, `Bash(npm:*)`
- **Required if interactive:** AskUserQuestion

### Before Finalizing

Scan for existing resources:
- Does a skill/command already handle part of this?
- Can this delegate to existing workflows?
- Is there redundancy with other features?

#### Delegation & Modularization

Before finalizing, scan for delegation opportunities:

```
Review available: skills, commands, agents, MCPs
For each workflow step, ask: "Do we already have this?"
```

**Common delegation patterns:**
- Git commits → `SlashCommand: /commit`
- Code review → `SlashCommand: /code-review`
- Plugin creation → `SlashCommand: /plugin-dev:create-plugin`
- Hook creation → `Skill: plugin-dev:hook-development`
- Command creation → `Skill: plugin-dev:command-development`
- Documentation lookup → `SlashCommand: /docs [topic]`

**Always use fully qualified names:**
- `Skill: plugin-dev:hook-development` (not just "hook-development")
- `SlashCommand: /plugin-dev:create-plugin` (not just "create-plugin")
- `Task: subagent_type=plugin-dev:agent-creator`

### Explain Your Choices

When presenting the generated skill/command to the user, briefly explain:
- **What you set and why** — "Added `context: fork` because this workflow generates heavy output"
- **What you excluded and why** — "Left `model` unset (inherits default), `hooks` omitted (no validation needed)"
- **What they might want to change** — "You may want to add more trigger phrases if this doesn't activate reliably"

This transparency helps users understand the design and provide feedback.

### Bundled Scripts

This skill includes helper scripts to accelerate skill creation.

**Initialize a new skill:**
```bash
~/.claude/skills/promptcraft/scripts/init_skill.py <name> --path <dir> [--resources scripts,references,assets] [--examples]
```

Creates a skill directory with templated SKILL.md and optional resource directories.

**Validate a skill:**
```bash
~/.claude/skills/promptcraft/scripts/validate_skill.py <skill-directory>
```

Checks frontmatter format, naming conventions, description completeness, and body content.

**Package for distribution:**
```bash
~/.claude/skills/promptcraft/scripts/package_skill.py <skill-directory> [output-dir]
```

Creates a `.skill` file (zip format) after validation passes.

## Phase 3: Deliver

### Output Paths

| Type | Location |
|------|----------|
| User skill | `~/.claude/skills/<name>/SKILL.md` |
| User command | `~/.claude/commands/<name>.md` |
| Project skill | `.claude/skills/<name>/SKILL.md` |
| Project command | `.claude/commands/<name>.md` |

### Write and Confirm

Before writing:
```
Writing to: [path]
This will [create new / overwrite existing] file.
Proceed?
```

### After Creation

Summarize what was created:
- Name and type
- Path
- How to invoke/trigger
- Suggested test scenario

## Evaluation

**Evaluate the generated/optimized prompt:**

| Dimension | Criteria |
|-----------|----------|
| **Clarity (0-10)** | Instructions unambiguous, objective clear |
| **Precision (0-10)** | Appropriate specificity without over-constraint |
| **Efficiency (0-10)** | Token economy—maximum value per token |
| **Completeness (0-10)** | Covers requirements without gaps or excess |
| **Usability (0-10)** | Practical, actionable, appropriate for target use |

**Target: 9.0/10.0**

Present evaluation, then:
- If < 9.0: Refine addressing weakness, re-evaluate once
- If ≥ 9.0: Proceed to delivery


## Quality Standards

Apply Context Engineering Principles (see above). Additionally:

**Format Economy:**
- Simple task → direct instruction, no sections
- Moderate task → light organization with headers
- Complex task → full semantic structure

**Balance Flexibility with Precision:**
- Loose enough for creative exploration
- Tight enough to prevent ambiguity

**Remove ruthlessly:** Filler phrases, obvious implications, redundant framing, excessive politeness

## Error Handling

| Issue | Action |
|-------|--------|
| Unclear requirements | Ask clarifying questions |
| Missing context | Request examples or constraints |
| Path issues | Verify directory exists, create with confirmation |
| Type unclear | Default to skill if auto-triggering desired |

---

Execute phases sequentially. Always fetch current documentation first.
