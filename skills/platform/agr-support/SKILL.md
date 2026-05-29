---
name: agr-support
description: Help users with agr/agrx CLI questions, troubleshooting, and best practices. Use when users ask about installing resources, syncing, local authoring, dependency management, repository setup, or troubleshooting agr/agrx commands. Provides guided, step-by-step instructions with examples.
---

# agr-support

Help users with agr/agrx CLI operations, troubleshooting, and workflows.

## Response Format

When answering questions:

1. **Lead with the answer** - Start with the direct solution or command
2. **Show concrete examples** - Include runnable commands
3. **Explain briefly** - Add context only when needed
4. **Link to references** - Point to reference files for deeper dives

Format responses as:

```
**Answer**: [Direct answer with command]

**Example**:
[Runnable example]

**Explanation**: [Brief context if needed]

**See also**: [Reference file if relevant]
```

## Question Handling Workflow

1. **Identify the topic**: Installation, execution, sync, authoring, or troubleshooting
2. **Consult the appropriate reference file**:
   - CLI commands and syntax: `references/commands.md`
   - Step-by-step workflows: `references/workflows.md`
   - Error messages and solutions: `references/troubleshooting.md`
3. **Respond with guidance**: Command + example + explanation

## Scope

### In scope
- All `agr` and `agrx` commands
- Resource installation and management
- Local authoring workflows
- Dependency tracking with `agr.toml`
- Repository setup and publishing
- Troubleshooting common errors

### Out of scope (redirect appropriately)
- General Claude Code questions (not agr-specific)
- Writing SKILL.md content (use `skill-creator` skill)
- GitHub authentication issues (point to GitHub docs)
- Network/system administration (general troubleshooting)

## Example Q&A

### How do I install a skill?

**Answer**: Use `agr add` with the username and resource name.

**Example**:
```bash
agr add kasperjunge/hello-world
```

**Explanation**: The resource type is auto-detected. Use `--type skill` if disambiguation is needed.

**See also**: `references/commands.md` for full `agr add` syntax.

---

### What's the difference between agr and agrx?

**Answer**: `agr add` installs permanently; `agrx` runs temporarily without permanent installation.

**Example**:
```bash
# Permanent install
agr add kasperjunge/hello-world

# Temporary run (cleaned up after)
agrx kasperjunge/hello-world "your prompt"
```

**Explanation**: Use `agrx` to try skills before committing, or for one-off tasks.

**See also**: `references/commands.md` for command details.

---

### How do I sync local resources?

**Answer**: Run `agr sync` to copy resources from authoring paths to `.claude/`.

**Example**:
```bash
# Set up authoring structure
agr init

# Create a skill
agr init skill my-skill

# Edit the skill
$EDITOR skills/my-skill/SKILL.md

# Sync to .claude/
agr sync
```

**See also**: `references/workflows.md` for the complete local authoring workflow.

---

### Why do I get "Resource found in multiple types"?

**Answer**: The resource name exists as both a skill and command. Use `--type` to specify which one.

**Example**:
```bash
agr add kasperjunge/hello --type skill
agr add kasperjunge/hello --type command
```

**See also**: `references/troubleshooting.md` for other error solutions.

---

### How do I create a shareable repository?

**Answer**: Use `agr init repo` to scaffold a repository others can install from.

**Example**:
```bash
# Create locally
agr init repo my-resources

# Or create and push to GitHub
agr init repo my-resources --github
```

**Explanation**: Name it `agent-resources` to let users install with `agr add username/resource` (shorter syntax).

**See also**: `references/workflows.md` for the complete repository setup workflow.
