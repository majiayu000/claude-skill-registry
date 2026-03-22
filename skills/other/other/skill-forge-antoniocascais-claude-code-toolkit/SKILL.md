---
name: skill-forge
description: Creates new Claude Code skills with proper structure and best practices. Use when user wants to create a skill, update an existing skill, add a new command, scaffold a workflow, define skill hooks, or asks "how do I make a skill".
allowed-tools: Read Write Edit Glob Grep AskUserQuestion
argument-hint: [use-case-description]
compatibility: Claude Code (uses context, agent, model, and hooks extensions)
---

# Skill Creator

Creates Claude Code skills following official best practices.

## Core Principles

### Only Add What Claude Doesn't Have
Claude is already smart. Only include domain-specific context it lacks:
- API quirks, library gotchas, edge cases
- Your org's conventions and patterns
- Domain knowledge not in training data

### Degrees of Freedom
Match instruction specificity to task fragility:

| Level | When | Example |
|-------|------|---------|
| **High freedom** | Multiple valid approaches | Code review (heuristics, not rigid steps) |
| **Medium freedom** | Preferred pattern exists | Reports (customizable scripts) |
| **Low freedom** | Fragile operations | DB migrations (exact commands, no deviation) |

### Progressive Disclosure
Context loads in 3 levels:
1. **Metadata** (~100 tokens) - name + description, always in context
2. **SKILL.md body** (<5000 tokens recommended) - loaded when skill triggers
3. **Resources** (unlimited) - scripts/, references/, assets/ loaded as needed

## Workflow

### Step 1: Gather Requirements

Use AskUserQuestion to collect:

1. **Skill name** - lowercase, hyphens only, ≤64 chars
   - Good: `pdf-processor`, `code-reviewer`, `deploy-helper`
   - Bad: `PDF_Processor`, `my cool skill`

2. **Description** - what it does + when to use it (≤1024 chars)
   - Third person ("Processes...", "Generates...")
   - Include ALL trigger keywords in description (primary discovery mechanism)
   - Example: "Processes PDF files to extract text and tables. Use when working with PDFs, extracting document content, or converting PDF to markdown."

3. **Allowed tools** (optional) - restrict capabilities
   - Space-delimited: `Read Glob Grep`
   - YAML list (cleaner for many tools):
     ```yaml
     allowed-tools:
       - Read
       - Write
       - Bash(git:*)
     ```
   - Bash patterns: `Bash(git:*)`, `Bash(git diff:*)`
   - Unrestricted: omit field entirely

4. **Complexity** - determines resource structure
   - Simple: SKILL.md only
   - Medium: + references/ for docs
   - Complex: + scripts/ for automation, assets/ for templates and static files

5. **Execution context** (optional)
   - Needs isolated context? → `context: fork`
   - Specific agent type? → `agent: Explore` / `Plan`
   - Model override? → `model: haiku` / `sonnet` / `opus`

6. **Invocation control** (optional)
   - User-only trigger (side effects like deploy, commit)? → `disable-model-invocation: true`
   - Claude-only (background knowledge, not actionable as command)? → `user-invocable: false`
   - See [Invocation Control](#invocation-control) for the interaction matrix

7. **Arguments** (optional)
   - Does the skill accept arguments? → use `$ARGUMENTS` in body
   - Autocomplete hint? → `argument-hint: [issue-number]`

8. **Hooks** (optional) - lifecycle automation
   - Validation after writes?
   - Logging before tool use?
   - See `references/hooks.md` for patterns

### Step 2: Validate Name

```
- Only lowercase letters, numbers, hyphens
- No leading/trailing hyphens, no consecutive hyphens
- ≤64 characters
- Not reserved: anthropic, claude
- Must match parent directory name
```

### Step 3: Generate Skill

**Default location**: `~/.claude/skills/{skill-name}/`

Create `SKILL.md` with:

```yaml
---
name: {skill-name}
description: {description}
allowed-tools: {tools}                # optional: space-delimited or YAML list
context: fork                         # optional: isolated execution
agent: {agent-type}                   # optional: Explore, Plan, general-purpose
model: {model}                        # optional: haiku, sonnet, opus
disable-model-invocation: true        # optional: user-only invocation
user-invocable: false                 # optional: Claude-only invocation
argument-hint: {hint}                 # optional: autocomplete hint
hooks: {}                             # optional: see references/hooks.md
---
```

Generate skill body matching the degree of freedom needed. Use imperative/infinitive form for instructions.

### Step 4: Post-Creation

```
✅ Skill created at: ~/.claude/skills/{skill-name}/
✅ Skill is immediately available (hot-reload enabled)
```

### Step 5: Iterate (User)

Inform user of the iteration loop:
1. Test skill on real tasks
2. Note where Claude struggles or produces poor output
3. Return to refine SKILL.md or add references/scripts
4. Repeat until quality is consistent

## Invocation Control

Two fields control who can invoke a skill and how it loads into context:

| Frontmatter | User can invoke | Claude can invoke | Context loading |
|-------------|----------------|-------------------|-----------------|
| (default) | Yes | Yes | Description always in context, body loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description NOT in context, body loads when user invokes |
| `user-invocable: false` | No | Yes | Description always in context, body loads when invoked |

**When to use `disable-model-invocation: true`:**
- Skills with side effects: deploy, commit, send messages, delete resources
- Skills where timing matters: user wants to control when it runs

**When to use `user-invocable: false`:**
- Background knowledge that isn't actionable as a command
- Context skills like `legacy-system-context` — Claude should know it, but `/legacy-system-context` isn't a meaningful user action

## Workflow Patterns

**Sequential**: Step 1 → 2 → 3 (most skills)
**Conditional**: Decision trees based on input type or user choice (see `webapp-testing/`)
**Multi-phase**: Plan → validate → execute → verify (for destructive operations)

For enforcing phase gates (hard stops between phases), see `references/advanced-features.md`.

For resource types (scripts/, references/, assets/) and their context loading behavior, see `references/spec-reference.md`.

## Anti-Patterns

- No README.md, CHANGELOG.md, INSTALLATION_GUIDE.md — only include what Claude needs to execute
- No "When to Use This Skill" in body — triggers come from description; body loads AFTER triggering
- No duplicated info between SKILL.md and references/ — pick one location
- No deeply nested references — keep one level deep from SKILL.md (except `examples/` subdirectories)
- No time-sensitive information (dates, version-specific instructions that will rot)
- No hardcoded absolute paths

## Advanced Features

For isolated execution (`context: fork`), string substitution (`$ARGUMENTS`), dynamic context injection, phase gates, and skill hooks — see `references/advanced-features.md`.

For skill hook syntax and patterns, see `references/hooks.md`.

## Quick Reference

For the condensed field spec, directory structure, and description budget, see `references/spec-reference.md`.

## Example Output

Generated skill examples at each complexity level:
- `references/examples/simple.md` — SKILL.md only, no resources
- `references/examples/medium.md` — with references/ and allowed-tools

Use these as templates when generating skills. For more examples: `git clone https://github.com/anthropics/skills.git /tmp/claude-skills-examples`

## Troubleshooting

### Skill name collision
Before creating, check if a skill already exists: `ls ~/.claude/skills/{name}/`. If it does, ask the user whether to update or choose a different name.

### YAML parse errors
Common causes:
- Description contains unquoted colons — wrap in quotes: `description: "Deploy helper: automates releases"`
- Missing `---` delimiters (need both opening and closing)
- Indentation mismatch in YAML lists

### Skill not triggering after creation
The description is the primary discovery mechanism. Check:
- Does it include trigger phrases users would actually say?
- Is it too generic? ("Helps with projects" won't trigger)
- Is it too narrow? Missing synonyms or paraphrases

## Best Practices Checklist

Before finalizing:

- [ ] Description is third person with ALL trigger keywords
- [ ] Description includes both what + when (trigger scenarios)
- [ ] SKILL.md under 500 lines (split to references/ if needed)
- [ ] Degree of freedom matches task fragility
- [ ] No hardcoded paths or time-sensitive info
- [ ] No "When to Use" section in body (triggers belong in description)
- [ ] Consistent terminology throughout
- [ ] Reference files >100 lines have TOC
- [ ] References one level deep (except `examples/` subdirectories)
- [ ] Scripts are black-box (documented inputs/outputs, not read into context)
- [ ] Skills with side effects use `disable-model-invocation: true`
- [ ] Skills using Claude Code extensions include `compatibility` field
