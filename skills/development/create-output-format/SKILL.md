---
name: create-output-format
description: Scaffold a new planning output format adapter. Creates a format directory with all required files implementing the output format contract.
disable-model-invocation: true
---

# Create Output Format

Scaffold a new output format adapter for the technical-planning workflow. Each format adapter is a directory of 5 files, one per concern.

## Step 1: Gather Information

Before writing anything, understand the tool. Ask the user for:

1. **What is the tool/system called?**
2. **Documentation links** — official docs, API references, MCP server docs, anything relevant

If the user provided these upfront, skip straight to research.

### Research

Fetch and read all provided documentation using WebFetch. From the docs, establish:

- How tasks are stored (API, database, files, etc.)
- How to interact with it (MCP server, REST API, CLI tool, filesystem)
- How to create, read, update, and query tasks
- What task properties are supported — status values, priority levels, labels/tags, estimation
- Whether it supports blocking/dependency relationships (within a project and across projects)
- How concepts map — what represents a project, a phase, a task, a dependency?
- What setup or configuration is required
- Benefits and trade-offs vs simpler approaches
- Any constraints or limitations

### Clarify Gaps

Present what you've learned as a summary and ask the user to confirm or correct. Use AskUserQuestion to clarify anything the documentation didn't cover or left ambiguous — motivation for choosing this format, preferred interface if multiple exist, setup specifics, etc.

Suggest a kebab-case format key based on the tool name and confirm with the user.

Do not proceed until the user confirms your understanding.

## Step 2: Understand the Contract

Read **[references/contract.md](references/contract.md)** — this defines the 5-file interface every format must implement.

## Step 3: Create the Format Directory

Create the directory at:

```
skills/technical-planning/references/output-formats/{format-key}/
```

## Step 4: Write the Files

Using the information gathered in Step 1, write each of the 5 required files. Use the scaffolding templates from **[references/scaffolding/](references/scaffolding/)** as structural guides:

| Template | Creates |
|----------|---------|
| [about.md](references/scaffolding/about.md) | `{format}/about.md` |
| [authoring.md](references/scaffolding/authoring.md) | `{format}/authoring.md` |
| [reading.md](references/scaffolding/reading.md) | `{format}/reading.md` |
| [updating.md](references/scaffolding/updating.md) | `{format}/updating.md` |
| [graph.md](references/scaffolding/graph.md) | `{format}/graph.md` |

For each file:

1. Start from the scaffolding template structure
2. Replace all `{placeholder}` tokens with format-specific content from your gathered information
3. Remove template guidance comments (lines starting with `<!-- -->`)
4. Include concrete commands, API calls, or MCP operations — not vague descriptions

## Step 5: Register the Format

Add an entry to `skills/technical-planning/references/output-formats.md` following the existing pattern:

```markdown
### {Format Name}
format: `{format-key}`

adapter: [{format-key}/](output-formats/{format-key}/)

{One-line description of the format.}

- **Pros**: ...
- **Cons**: ...
- **Best for**: ...
```

## Step 6: Validate

Verify:

- [ ] Directory contains exactly 5 files: about.md, authoring.md, reading.md, updating.md, graph.md
- [ ] All `{placeholder}` tokens have been replaced
- [ ] About.md includes a structure mapping table
- [ ] Authoring.md documents task properties: status, phase grouping, labels (NOT priority or dependencies)
- [ ] Authoring.md includes a complete task creation example
- [ ] Reading.md explains next-task ordering using status, priority, dependencies, and phase
- [ ] Updating.md covers all status transitions and how to modify task properties
- [ ] Graph.md covers priority levels and adding/removing dependencies
- [ ] Format is registered in output-formats.md
