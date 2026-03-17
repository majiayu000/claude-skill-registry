---
name: agent-creator
description: Use when creating expert agents. Generates agent.md with frontmatter, hooks, required sections, and skill references.
versions:
  claude-plugins: "1.35"
user-invocable: true
references: references/architecture.md, references/frontmatter.md, references/required-sections.md, references/hooks.md, references/registration.md, references/templates/agent-template.md, references/templates/hook-scripts.md
related-skills: skill-creator, exploration
---

# Agent Creator

## Agent Workflow (MANDATORY)

Before ANY agent creation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing agents, analyze patterns
2. **fuse-ai-pilot:research-expert** - Fetch latest agent conventions
3. **mcp__context7__query-docs** - Get examples from existing agents

After creation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Action | When to Use |
|--------|-------------|
| **New Agent** | New domain/framework expert needed |
| **Adapt** | Copy from similar agent (Next.js → React) |
| **Update** | Add skills, modify hooks |

---

## Critical Rules

1. **ALL content in English** - Never French or other languages
2. **Frontmatter complete** - name, description, model, tools, skills, hooks
3. **Agent Workflow section** - Always first content section
4. **SOLID rules reference** - Link to solid-[stack] skill
5. **Register in marketplace.json** - Or agent won't load
6. **Hook scripts executable** - `chmod +x`

---

## Architecture

```
plugins/<plugin-name>/
├── agents/
│   └── <agent-name>.md      # Agent definition
├── skills/
│   ├── skill-a/
│   └── solid-[stack]/
├── scripts/
│   └── validate-*.sh        # Hook scripts
└── .claude-plugin/
    └── plugin.json
```

→ See [architecture.md](references/architecture.md) for details

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Architecture** | [architecture.md](references/architecture.md) | Understanding agent structure |
| **Frontmatter** | [frontmatter.md](references/frontmatter.md) | YAML configuration |
| **Required Sections** | [required-sections.md](references/required-sections.md) | Mandatory content |
| **Hooks** | [hooks.md](references/hooks.md) | Pre/Post tool validation |
| **Registration** | [registration.md](references/registration.md) | marketplace.json |

### Templates

| Template | When to Use |
|----------|-------------|
| [agent-template.md](references/templates/agent-template.md) | Creating new agent |
| [hook-scripts.md](references/templates/hook-scripts.md) | Validation scripts |

---

## Quick Reference

### Create New Agent

```bash
# 1. Research existing agents
→ explore-codebase + research-expert

# 2. Create files
touch plugins/<plugin>/agents/<agent-name>.md
touch plugins/<plugin>/scripts/validate-<stack>-solid.sh
chmod +x plugins/<plugin>/scripts/*.sh

# 3. Register in marketplace.json

# 4. Validate
→ sniper
```

### Adapt Existing Agent

```bash
# 1. Copy similar agent
cp plugins/nextjs-expert/agents/nextjs-expert.md plugins/new-plugin/agents/new-expert.md

# 2. Adapt with sed
sed -i '' "s/nextjs/newstack/g; s/Next\.js/NewStack/g" agents/new-expert.md

# 3. Update skills, tools, register
```

---

## Validation Checklist

- [ ] ALL content in English
- [ ] Frontmatter complete (name, description, model, tools, skills)
- [ ] Agent Workflow section present
- [ ] Mandatory Skills Usage table
- [ ] SOLID Rules reference to solid-[stack]
- [ ] Local Documentation paths valid
- [ ] Hook scripts executable
- [ ] Registered in marketplace.json

---

## Related: Skill Creator

**When creating an agent, you often need to create skills too.**

Use **`/fuse-ai-pilot:skill-creator`** to create skills for the agent:

| Scenario | Action |
|----------|--------|
| New agent needs skills | Create skills with skill-creator first |
| Agent references skills | Ensure skills exist in skills/ |
| Adapting agent | Adapt related skills too |

---

## Best Practices

### DO
- Use skill-creator for associated skills
- Reference solid-[stack] skill for SOLID rules
- Include Gemini Design section for UI agents
- Make hook scripts executable

### DON'T
- Write in French (English only)
- Skip Agent Workflow section
- Forget marketplace registration
- Create agent without its skills
- Hard-code paths in hooks (use `$CLAUDE_PLUGIN_ROOT`)
