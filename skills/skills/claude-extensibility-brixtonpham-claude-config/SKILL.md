---
name: claude-extensibility
description: "Claude Code extensibility: agents, skills, output styles. Capabilities: create/update/delete agents and skills, YAML frontmatter, system prompts, tool/model selection, resumable agents, CLI-defined agents. Actions: create, edit, delete, optimize, test extensions. Keywords: agent, skill, output-style, SKILL.md, subagent, Task tool, progressive disclosure. Use when: creating agents/skills, editing extensions, configuring tool access, choosing models, testing activation."
---

# Claude Code Extensibility

CRUD operations for agents, skills, and output styles. This skill transfers expertise in building extensions that actually activate and deliver value.

## Related Skills

**IMPORTANT:** When creating or editing prompts, use `prompt-architect` skill to improve quality.

```
Skill("prompt-architect")  → Create/enhance skill/agent prompt content
```

## Core Principles

- **Simplicity**: Direct tool calls, avoid complex abstractions
- **Focus**: Single, clear responsibility per extension
- **Conciseness**: Target <800 lines, use progressive disclosure
- **Efficiency**: Optimize for token usage and response time

## Core Truths

Every extension must embody these principles:

| Truth | Meaning | Test |
|-------|---------|------|
| **Expertise Transfer** | Make Claude *think* like expert, not follow steps | Does it transfer patterns or just procedures? |
| **Flow, Not Friction** | Produce output, not intermediate work | Does it help produce results or create busywork? |
| **Voice Matches Domain** | Sound like practitioner, not documentation | Would an expert recognize this as their thinking? |
| **Focused Beats Comprehensive** | Constrain ruthlessly | Does every section earn its place? |

## Decision Heuristics

| Rule | Guidance |
|------|----------|
| **3-File Rule** | Task touches 3+ files → agent (needs autonomy). Enhances how YOU work → skill. |
| **Delegation Test** | "Does this run independently while I do other work?" Yes → agent. No → skill. |
| **Expert Test** | "Would an expert do this differently than beginner?" Big difference → skill. |
| **Activation Breadth** | Trigger on 80% of relevant requests, not 100%. Over-broad = noise. |
| **Composition Preference** | When in doubt, 2 small focused extensions > 1 large monolith. |
| **Tool Constraint** | Start with 2-3 essential tools. Adding is easy; removing breaks things. |

## Expert Patterns

### The "Everything Tool" Request
**When you see:** User wants one agent/skill to handle auth, database, API, and testing
**This indicates:** Scope creep that will create bloated, unfocused extension
**Therefore:** Split into focused single-responsibility extensions; suggest composition
**Watch out:** User may resist - explain that 3 focused skills outperform 1 swiss-army-knife

### The Wrapper Trap
**When you see:** Skill that just wraps a CLI tool with no added expertise
**This indicates:** Missing the expertise transfer opportunity
**Therefore:** Ask "what would an expert know that the tool doesn't tell you?"
**Watch out:** The skill becomes redundant with just reading --help

### Activation Keyword Starvation
**When you see:** Frontmatter description uses only formal/technical terms
**This indicates:** Skill won't activate when users use casual language
**Therefore:** Add synonyms, verbs, casual phrasings to description
**Watch out:** Over-broad keywords cause false activations

### The Procedure Manual
**When you see:** Step 1, Step 2, Step 3... (long numbered instructions)
**This indicates:** Procedures don't transfer judgment - expert skips steps, adapts order
**Therefore:** Teach patterns and heuristics. Let reader apply judgment.
**Watch out:** Some workflows genuinely need sequence - use sparingly

## Extension Types

| Type | Invocation | Purpose | Location |
|------|------------|---------|----------|
| **Agents** | Task tool | Specialized sub-processes | `.claude/agents/` |
| **Skills** | Model-invoked (autonomous) | Domain knowledge | `.claude/skills/{name}/` |
| **Output Styles** | `/output-style` command | Modify main agent behavior | `.claude/output-styles/` |

## Activation Keyword Engineering

**The description field is your activation gate.** System reads ONLY frontmatter to decide loading. Brilliant skill + poor keywords = dead skill.

### Keyword Categories to Include

1. **Task Verbs**: create, build, debug, fix, deploy, optimize, refactor
2. **Problem Descriptions**: slow, broken, failing, error, conflict
3. **Artifact Types**: component, API, database, test, config
4. **Tool/Framework Names**: React, PostgreSQL, Docker (exact + misspellings)
5. **Casual Synonyms**: "make it faster" → optimize, performance

### Description Format (WHAT + WHEN)

```yaml
# Bad - too vague, won't trigger
description: Helps with documents

# Bad - missing WHEN triggers
description: PDF skill

# Good - multiple trigger points
description: "Extract text and tables from PDF files, fill forms, merge documents.
  Formats: .pdf. Tools: pypdf, pdfplumber. Actions: extract, fill, merge PDFs.
  Keywords: PDF, form, document. Use when: working with PDF files, extracting data."
```

### Frontmatter Checklist

- [ ] Name is clear and descriptive (not abbreviation)
- [ ] Description includes file types if applicable (.docx, .pdf)
- [ ] Description includes task verbs (creating, editing, analyzing)
- [ ] Description includes synonyms users might say
- [ ] Description includes contexts (reports, professional documents)

### Keyword Density Test

Read description aloud. For every 10 words, at least 3 should be potential triggers.

---

## Agent Development

**Reference:** `references/agent-development.md` - Full YAML structure, system prompt patterns, optimization techniques.

### Quick Start: Agent

```yaml
---
name: agent-name
# CRITICAL: Description is the ONLY thing system reads to decide activation
# Include: task verbs, problem descriptions, synonyms users actually say
description: Use this agent when [use case]. Use PROACTIVELY for [triggers].\n\nExamples:\n<example>\nContext: [situation]\nuser: [request]\nassistant: [response]\n<commentary>[reasoning]</commentary>\n</example>
# CONSTRAIN RUTHLESSLY: 3-5 tools = focused. 10+ tools = confused.
tools: Grep, Glob, Read, Bash
model: haiku
permissionMode: default
skills: skill-name
---

# Agent Name

Brief mission statement.

## Core Strategy

### 1. Phase Name
Approach and techniques

## What This Agent Does NOT Do
- Does not [boundary 1] (use X agent)
- Does not [boundary 2] (escalate to user)

<format>
Expected output structure
</format>
```

### YAML Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphens (e.g., `code-reviewer`) |
| `description` | Yes | Single line with `\n` for newlines, include examples |
| `tools` | No | Comma-separated; inherits all if omitted |
| `model` | No | `haiku`, `sonnet`, `opus`, `inherit` (default: sonnet) |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Comma-separated skill names to auto-load |

### Model Selection

| Model | Use When | Target Time |
|-------|----------|-------------|
| `haiku` | Fast tasks, exploration, search | < 3s |
| `sonnet` | Balanced, most use cases | < 10s |
| `opus` | Complex reasoning, architecture | < 30s |
| `inherit` | Match main conversation model | varies |

### Built-in Subagents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| `general-purpose` | Sonnet | All | Complex research, multi-step operations |
| `plan` | Sonnet | Read, Glob, Grep, Bash | Research in plan mode |
| `Explore` | Haiku | Read-only | Fast codebase search (quick/medium/very thorough) |

### Agent Locations

| Location | Scope | Priority |
|----------|-------|----------|
| `.claude/agents/` | Project | Highest |
| `~/.claude/agents/` | User (all projects) | Lower |
| Plugin `agents/` | Plugin-specific | Varies |
| `--agents` CLI flag | Session only | Medium |

### CLI-Defined Agents

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

### Resumable Agents

Continue previous conversations:
- Each execution gets unique `agentId`
- Transcript stored in `agent-{agentId}.jsonl`
- Resume with previous `agentId` to continue with full context

---

## Skill Development

**Reference:** `references/skill-development.md` - Full structure, trigger patterns, hook system.

### Quick Start: Skill

```yaml
---
name: skill-name
# WHAT it does + WHEN to use it (both required!)
description: "[Core purpose]. [Technologies]. Capabilities: [list].
  Actions: [verbs]. Keywords: [triggers]. Use when: [scenarios]."
allowed-tools: Read, Grep, Glob
---

# Skill Name

## Purpose
What this skill helps with - in practitioner voice.

## Patterns

### [Pattern Name]
**When you see:** [Observable trigger]
**This indicates:** [Expert insight]
**Therefore:** [Action to take]
**Watch out for:** [Common pitfall]

## Heuristics
- **[Rule of thumb]**: [When/why it applies]

## When to Use Something Else
- For X → use `other-skill`
- For Y → escalate to user
```

### YAML Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphens, max 64 chars |
| `description` | Yes | WHAT + WHEN format, max 1024 chars, quoted |
| `allowed-tools` | No | Restrict tool access (security) |

### Tool Access Control

Restrict Claude's tools with `allowed-tools`:

```yaml
---
name: safe-reader
description: "Read-only file access. Use when viewing code without modifications."
allowed-tools: Read, Grep, Glob
---
```

### Skill Locations

| Location | Scope |
|----------|-------|
| `.claude/skills/{name}/SKILL.md` | Project (shared via git) |
| `~/.claude/skills/{name}/SKILL.md` | User (all projects) |
| Plugin `skills/` | Plugin-bundled |

### Skill Structure

```
my-skill/
├── SKILL.md (required, <800 lines)
├── references/ (optional - detailed docs)
├── scripts/ (optional - utilities)
└── templates/ (optional - templates)
```

### Core Sections (Include What's Needed)

| Section | Purpose | Include When |
|---------|---------|--------------|
| **Frontmatter** | Activation trigger | **Always - required** |
| **Context** | Domain framing | When domain context helps |
| **Patterns** | Expert recognition | Core - almost always |
| **Heuristics** | Decision guidance | When judgment needed |
| **Anti-Patterns** | What to avoid | When mistakes are common/costly |
| **Workflow** | Process guidance | When sequence matters |
| **Quality Signals** | How to verify good work | When quality is hard to assess |
| **Tools/Commands** | Technical specifics | When implementation details matter |
| **Output Spec** | Expected format | When format is specific |

---

## Output Styles

Modify Claude Code's main agent behavior.

### Quick Start: Output Style

```markdown
---
name: My Custom Style
description: Brief description of behavior
keep-coding-instructions: true
---

# Custom Style Instructions

You are an interactive CLI tool that helps users...

## Specific Behaviors
[Define assistant behavior...]
```

### YAML Fields

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Display name | Filename |
| `description` | UI description | None |
| `keep-coding-instructions` | Retain coding instructions | `false` |

### Built-in Styles

- **Default**: Standard software engineering
- **Explanatory**: Educational insights between tasks
- **Learning**: Collaborative with `TODO(human)` markers

### Output Style Locations

- User: `~/.claude/output-styles/`
- Project: `.claude/output-styles/`

### Usage

```bash
/output-style              # Access menu
/output-style explanatory  # Switch directly
```

---

## Writing Principles

### Voice
- Sound like a practitioner, not documentation
- Direct and confident, not hedging
- Specific and concrete, not abstract

**Before (documentation voice):**
> It is recommended that users consider implementing appropriate error handling mechanisms.

**After (practitioner voice):**
> Always handle errors explicitly. Silent failures are debugging nightmares.

### Density
- Every sentence should transfer knowledge
- No filler, no redundancy
- If it doesn't change behavior, cut it

### Scannability
- Claude reads this during tasks
- Headers help Claude find relevant sections
- Patterns are scannable by name
- Bold key terms

### Patterns Over Procedures

Transform procedures to patterns when expertise matters:

**Before (procedure):**
```
1. Open the file
2. Check the format
3. Validate the data
4. Process the content
```

**After (pattern):**
```markdown
### Format Recognition
**When you see:** File extension and initial bytes
**This indicates:** Expected structure and parsing approach
**Therefore:** Choose parser before reading content
**Watch out for:** Extension doesn't always match actual format
```

---

## Anti-Patterns

### The Kitchen Sink Agent
**Looks like:** Agent with 10+ tools, handles "everything related to X"
**Why wrong:** Broad agents make poor decisions, consume tokens exploring options
**Instead:** Constrain to 3-5 core tools. Create sibling agents for related domains.

### The Echo Skill
**Looks like:** Skill that restates tool documentation without adding insight
**Why wrong:** No expertise transfer. User could just read the docs.
**Instead:** Add the "expert layer" - pitfalls, non-obvious combos, when NOT to use.

### The Invisible Trigger
**Looks like:** Description uses only official tool/framework name
**Why wrong:** Users say "help me deploy" not "invoke kubernetes-orchestrator"
**Instead:** Include task verbs, user-language synonyms, problem descriptions.

### Missing Boundaries
**Looks like:** No explicit "what this does NOT do" section
**Why wrong:** Scope creep, incorrect expectations, overlapping extensions
**Instead:** Every extension needs 3+ explicit out-of-scope declarations.

### Vague Descriptions
**Looks like:** `description: Helps with documents`
**Why wrong:** Too vague to trigger on relevant requests
**Instead:** Include file types, task verbs, problem descriptions, synonyms.

---

## Quality Signals

### Good Signs
- Frontmatter reads like "when to use" guide, not feature list
- First 10 lines provide immediate actionable guidance
- Expert reading it would nod and say "yes, that's how I think"
- Explicit constraints on what it does NOT handle
- Examples show judgment calls, not just syntax
- Has named patterns with insights, not just steps

### Warning Signs
- More than 50% content is reference tables or field definitions
- No mention of tradeoffs or "when NOT to use"
- Generic language that could apply to any domain
- Activation keywords are all nouns, no verbs or problem descriptions
- Body exceeds 600 lines (probably doing too much)
- Second-person voice ("you should...")

---

## Validation Checklist

Before outputting, verify against Core Truths:

### Frontmatter (Most Critical)
- [ ] Has YAML frontmatter with name and description?
- [ ] Name is clear and searchable (not abbreviation)?
- [ ] Description includes trigger keywords?
- [ ] Description includes file types if applicable?
- [ ] Description includes task verbs (creating, editing, etc.)?
- [ ] Description includes synonyms users might use?

### Expertise Transfer
- [ ] Has named patterns with insights, not just steps?
- [ ] Transfers HOW to think, not just WHAT to do?
- [ ] Would an expert recognize their thinking here?

### Flow
- [ ] Helps produce output, not create busywork?
- [ ] No unnecessary intermediate steps?
- [ ] Actionable immediately?

### Focus
- [ ] Every section earns its place?
- [ ] No bloat?
- [ ] Ruthlessly constrained to what matters?

---

## Common Workflows

### Create Agent

1. Create `.claude/agents/{name}.md`
2. Write YAML frontmatter (name, description, tools, model)
3. Write system prompt (<800 lines)
4. **Use `Skill("prompt-architect")` to improve prompt**
5. Test with Task tool
6. Optimize based on performance

### Create Skill

1. Create `.claude/skills/{name}/SKILL.md`
2. Write YAML frontmatter with WHAT + WHEN description
3. Write content with patterns, not procedures
4. **Use `Skill("prompt-architect")` to improve prompt**
5. Add reference files for detailed content
6. Test: Does it activate when expected?

### Optimize Extension

1. Measure baseline (lines, token usage, response time)
2. Move details to reference files
3. **Use `Skill("prompt-architect")` to improve prompts**
4. Remove second-person voice
5. Use code blocks over prose
6. Add XML structure
7. Test and verify improvements

---

## Testing

### Key Question: Does it activate when expected?

**Agent Testing:**
```bash
Task(
  subagent_type="agent-name",
  description="Test task",
  prompt="Detailed test prompt"
)
```

**Skill Testing:**
- Test prompts that SHOULD trigger
- Test prompts that should NOT trigger
- Debug with: `claude --debug`

---

## Best Practices

### Anthropic Guidelines

✅ **800-line rule**: Keep SKILL.md and agent prompts under 800 lines
✅ **Progressive disclosure**: Use reference files for detailed content
✅ **Proactive language**: Include "use PROACTIVELY" in descriptions
✅ **WHAT + WHEN descriptions**: Both capability and triggers
✅ **Test first**: Build 3+ evaluations before extensive documentation
✅ **Least privilege**: Limit tools to necessary set

### Anti-Pattern Summary

❌ Vague descriptions without triggers
❌ Over 800 lines without references
❌ Second-person voice ("you should...")
❌ All tools when subset suffices
❌ No examples in agent descriptions
❌ Procedures without patterns

---

## Quick Reference

**Agent Model Selection:**
- Haiku: Fast, simple tasks (< 3s)
- Sonnet: Balanced, most use cases (< 10s)
- Opus: Complex reasoning (< 30s)
- Inherit: Match main conversation

**File Locations:**
- Agents: `.claude/agents/*.md`
- Skills: `.claude/skills/{name}/SKILL.md`
- Output Styles: `.claude/output-styles/*.md`

**Management Commands:**
- `/agents` - Interactive agent management
- `/output-style` - Switch output styles

---

**Status**: Production Ready | **Lines**: ~500 | **Progressive Disclosure**: ✅
