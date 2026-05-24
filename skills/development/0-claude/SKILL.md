---
name: claude-ecosystem
description: "Claude Code ecosystem expertise. Modules: CLI tool (setup, slash commands, MCP servers, hooks, plugins, CI/CD), extensibility (agents, skills, output styles creation), CLAUDE.md (project instructions, optimization). Actions: configure, troubleshoot, create, deploy, integrate, optimize Claude Code. Keywords: Claude Code, Anthropic, CLI tool, slash command, MCP server, Agent Skill, hook, plugin, CI/CD, enterprise, CLAUDE.md, agentic coding, agent, skill, output-style, SKILL.md, subagent, Task tool, project instructions, token optimization. Use when: learning Claude Code features, configuring settings, creating skills/agents/hooks, setting up MCP servers, troubleshooting issues, CI/CD integration, initializing or optimizing CLAUDE.md files."
---

# Claude Ecosystem

Comprehensive guide for Claude Code CLI tool, extensibility (agents/skills/output styles), and CLAUDE.md architecture.

## Module Selection

| Need | Module | Reference |
|------|--------|-----------|
| **Setup/Configuration** | CLI | `references/getting-started.md`, `references/configuration.md` |
| **Slash Commands** | CLI | `references/slash-commands.md` |
| **MCP Servers** | CLI | `references/mcp-integration.md` |
| **Hooks & Plugins** | CLI | `references/hooks-and-plugins.md` |
| **Create Agents** | Extensibility | `references/agent-development.md` |
| **Create Skills** | Extensibility | `references/skill-development.md` |
| **Output Styles** | Extensibility | `references/skill-development.md` |
| **Init CLAUDE.md** | Architecture | `references/initialization-workflow.md` |
| **Optimize CLAUDE.md** | Architecture | `references/optimization-patterns.md` |
| **Enterprise/CI-CD** | CLI | `references/enterprise-features.md`, `references/cicd-integration.md` |
| **Troubleshooting** | CLI | `references/troubleshooting.md` |

---

## Quick Reference

### Extension Types

| Type | Invocation | Purpose | Location |
|------|------------|---------|----------|
| **Agents** | Task tool | Specialized sub-processes | `.claude/agents/` |
| **Skills** | Model-invoked | Domain knowledge | `.claude/skills/{name}/` |
| **Output Styles** | `/output-style` | Modify main agent | `.claude/output-styles/` |

### Model Selection (Agents)

| Model | Use When | Target Time |
|-------|----------|-------------|
| `haiku` | Fast tasks, exploration | < 3s |
| `sonnet` | Balanced, most use cases | < 10s |
| `opus` | Complex reasoning | < 30s |

### CLAUDE.md Token Budget

| Complexity | Target Tokens |
|-----------|---------------|
| Simple | 100-200 |
| Medium | 200-400 |
| Complex | 400-800 |
| Maximum | 1000 |

---

## Extensibility Principles

### Core Truths

| Truth | Meaning |
|-------|---------|
| **Expertise Transfer** | Make Claude *think* like expert, not follow steps |
| **Flow, Not Friction** | Produce output, not intermediate work |
| **Voice Matches Domain** | Sound like practitioner, not documentation |
| **Focused Beats Comprehensive** | Constrain ruthlessly |

### Decision Heuristics

| Rule | Guidance |
|------|----------|
| **3-File Rule** | 3+ files → agent. Enhances YOUR work → skill. |
| **Delegation Test** | Runs independently? Agent. Guides you? Skill. |
| **Activation Breadth** | Trigger on 80% of relevant requests |
| **Tool Constraint** | Start with 2-3 essential tools |

### Activation Keywords

**The description field is your activation gate.** Include:
1. Task verbs: create, build, debug, fix, deploy
2. Problem descriptions: slow, broken, failing
3. Artifact types: component, API, database
4. Casual synonyms: "make it faster" → optimize

---

## Common Workflows

### Create Agent

```yaml
---
name: agent-name
description: "Use when [use case]. PROACTIVELY for [triggers].\n\nExamples:\n<example>\nContext: [situation]\nuser: [request]\nassistant: [response]\n</example>"
tools: Grep, Glob, Read, Bash
model: haiku
---

# Agent Name

Mission statement.

## Strategy
[Approach]

## Does NOT Do
- [boundary] (use X instead)
```

### Create Skill

```yaml
---
name: skill-name
description: "[Core purpose]. [Technologies]. Capabilities: [list].
  Actions: [verbs]. Keywords: [triggers]. Use when: [scenarios]."
allowed-tools: Read, Grep, Glob
---

# Skill Name

## Patterns

### [Pattern Name]
**When you see:** [Observable trigger]
**This indicates:** [Expert insight]
**Therefore:** [Action]
**Watch out:** [Pitfall]
```

### Initialize CLAUDE.md

1. Analyze codebase (language, framework, structure)
2. Extract code style, commands, patterns
3. Generate with template, customize
4. Validate commands, check token count
5. Target <400 lines, prefer <250

**Detailed:** `references/initialization-workflow.md`

### Optimize CLAUDE.md

1. Evaluate token efficiency
2. Find redundancy, outdated info
3. Apply token reduction techniques
4. Target 40%+ reduction
5. Verify critical info retained

**Detailed:** `references/optimization-patterns.md`

---

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| **Kitchen Sink Agent** | 10+ tools, handles "everything" | Constrain to 3-5 tools |
| **Echo Skill** | Restates docs without insight | Add expert layer |
| **Invisible Trigger** | Description uses only formal terms | Include user language |
| **Procedure Manual** | Step 1, 2, 3... | Teach patterns, not steps |
| **Over-Documentation** | CLAUDE.md > 400 lines | Document project-specific only |

---

## Quality Signals

### Good Signs
- Frontmatter reads like "when to use" guide
- First 10 lines provide actionable guidance
- Expert would nod "yes, that's how I think"
- Explicit constraints on what it does NOT handle

### Warning Signs
- >50% reference tables or field definitions
- No mention of "when NOT to use"
- Generic language for any domain
- Body exceeds 600 lines

---

## References

### CLI Tool
- `references/getting-started.md` - Installation, setup, auth
- `references/slash-commands.md` - Complete command catalog
- `references/mcp-integration.md` - MCP server configuration
- `references/hooks-and-plugins.md` - Hook types, plugin structure
- `references/configuration.md` - Settings hierarchy
- `references/enterprise-features.md` - IAM, SSO, sandboxing
- `references/cicd-integration.md` - GitHub Actions, GitLab CI
- `references/ide-integration.md` - VS Code, JetBrains
- `references/advanced-features.md` - Extended thinking, caching
- `references/troubleshooting.md` - Common issues
- `references/api-reference.md` - Admin, Messages, Skills APIs
- `references/best-practices.md` - Project organization, security
- `references/agent-skills.md` - Creating skills via CLI

### Extensibility
- `references/agent-development.md` - Full YAML structure, system prompts
- `references/skill-development.md` - Structure, triggers, hooks

### CLAUDE.md
- `references/initialization-workflow.md` - Creating new CLAUDE.md
- `references/optimization-patterns.md` - Token reduction techniques
- `references/integration-strategies.md` - Global config, MCP tools
- `references/output-templates.md` - Standard output formats

---

## Related Skills

**IMPORTANT:** When creating/editing prompts, use `prompt-architect` skill.

```
Skill("prompt-architect") → Create/enhance skill/agent prompt content
```

---

**Documentation:**
- llms.txt: https://context7.com/websites/claude_en_claude-code/llms.txt?tokens=10000
- Main docs: https://docs.claude.com/en/docs/claude-code/
- GitHub: https://github.com/anthropics/claude-code
