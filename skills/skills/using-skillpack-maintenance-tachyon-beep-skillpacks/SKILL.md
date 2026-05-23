---
name: using-skillpack-maintenance
description: Use when maintaining, enhancing, or modifying existing Claude Code plugins - handles skills, commands, agents, hooks, and reference sheets through systematic domain analysis, structure review, behavioral testing, and quality improvements
---

# Plugin Maintenance

Systematic maintenance of Claude Code plugins including skills, commands, agents, hooks, and reference sheets.

## Core Principle

**Maintenance = behavioral validation, not syntactic checking.** Test if components guide Claude correctly, not if they parse correctly.

## Scope: What This Skill Maintains

| Component | Location | Frontmatter |
|-----------|----------|-------------|
| **Skills** | `skills/*/SKILL.md` | `name`, `description`, `allowed-tools` |
| **Reference sheets** | `skills/using-*/*.md` | (none - content files) |
| **Commands** | `commands/*.md` | `description`, `allowed-tools`, `argument-hint` |
| **Agents** | `agents/*.md` | `description`, `model`, `tools` |
| **Hooks** | `hooks/hooks.json` | JSON with event matchers |

## When to Use

**Use for:**
- Enhancing existing plugins (e.g., "refresh yzmir-deep-rl")
- Adding/removing/modifying components
- Identifying coverage gaps
- Validating component quality

**Do NOT use for:**
- Creating new plugins from scratch (design first)
- Creating brand new skills (use `superpowers:writing-skills`)

---

## Reference Sheet Location

All reference sheets are in this skill's directory:
- `analyzing-pack-domain.md` - Domain investigation
- `reviewing-pack-structure.md` - Structure review, scorecard
- `testing-skill-quality.md` - Behavioral testing methodology
- `implementing-fixes.md` - Execution and versioning

When reading `analyzing-pack-domain.md`, find it at:
  `skills/using-skillpack-maintenance/analyzing-pack-domain.md`

---

## Workflow: Review → Discuss → Execute

### Stage 1: Investigation

**Load:** `analyzing-pack-domain.md`

1. **User scope** - Ask about intent, boundaries, target audience
2. **Domain mapping** - What should this plugin cover?
3. **Inventory audit** - What exists? Skills, commands, agents, hooks?
4. **Gap analysis** - What's missing vs. coverage map?

**Output:** Coverage map, component inventory, gaps identified

### Stage 2: Structure Review

**Load:** `reviewing-pack-structure.md`

Generate fitness scorecard:
- **Critical** - Plugin unusable, consider rebuild
- **Major** - Significant gaps or structural issues
- **Minor** - Polish and improvements
- **Pass** - Structurally sound

**Decision gate:** Present scorecard → User decides: Proceed / Rebuild / Cancel

### Stage 3: Behavioral Testing

**Load:** `testing-skill-quality.md`

Test each component with challenging scenarios:
- **Pressure tests** - Does it hold under "just do it quickly" pressure?
- **Edge cases** - Does it handle corner cases?
- **Real-world complexity** - Does it guide correctly in messy situations?

**Output:** Per-component test results (Pass / Fix needed)

### Stage 4: Discussion

Present findings by category:

**Gaps requiring new components:**
- Skills needing `superpowers:writing-skills` (each = separate RED-GREEN-REFACTOR)
- Commands to create
- Agents to create

**Existing components needing fixes:**
- Skills/commands/agents with behavioral failures
- Hooks with issues

**Get user approval before execution.**

### Stage 5: Execution

**Load:** `implementing-fixes.md`

**CRITICAL CHECKPOINT:**
If gaps were identified → Use `superpowers:writing-skills` for EACH new skill first.
Do NOT create new skills inline. They require behavioral testing.

Execute approved changes:
1. Structural fixes (remove duplicates, update router)
2. Content enhancements (fix behavioral failures)
3. Component creation (commands, agents - NOT skills)
4. Version bump and commit

---

## Component-Specific Guidance

### Skills (SKILL.md)

```yaml
---
name: skill-name
description: When to use this skill and what it does
allowed-tools: [Read, Grep, Glob]  # optional
---
```

**Key questions:**
- Does description trigger correct activation?
- Is guidance actionable under pressure?
- Are there missing anti-patterns?

### Commands (commands/*.md)

```yaml
---
description: What this command does
allowed-tools: [Read, Bash, Glob, Grep]
argument-hint: "[optional_arg]"
---
```

**Key questions:**
- Is the command user-invocable (vs skill which is model-invoked)?
- Does it have clear entry point?
- Are tool restrictions appropriate?

### Agents (agents/*.md)

```yaml
---
description: What this agent specializes in
model: sonnet  # or opus, haiku
tools: [Read, Grep, Glob, Bash, Write]
---
```

**Key questions:**
- Clear scope boundaries (what it does / doesn't do)?
- Appropriate model selection for complexity?
- Activation examples (positive and negative)?

### Hooks (hooks/hooks.json)

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{"type": "command", "command": "script.sh"}]
    }]
  }
}
```

**Events:** PreToolUse, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStop, SessionStart, SessionEnd, PreCompact

**Key questions:**
- Correct event type for the use case?
- Matcher pattern accurate?
- Script executable and tested?

---

## Version Bump Rules

| Impact | Bump | Examples |
|--------|------|----------|
| **Low** | Patch (x.y.Z) | Typos, formatting, minor clarifications |
| **Medium** | Minor (x.Y.0) | Enhanced guidance, new components, better examples |
| **High** | Major (X.0.0) | Components removed, structural changes, philosophy shifts |

**Default for maintenance: Minor bump**

---

## Red Flags - Stop and Reconsider

| Thought | Reality |
|---------|---------|
| "I'll write new skills during execution" | NO. Use `superpowers:writing-skills` for each gap |
| "Syntax looks correct, no need to test" | Parsing ≠ effectiveness. Test behavior. |
| "This is a quick fix, skip the process" | Quick untested = broken later |
| "The command/agent is simple enough" | Simple things fail in edge cases. Test anyway. |

---

## Quick Reference

```
Investigation → Scorecard → Testing → Discussion → Execution
     ↓              ↓           ↓           ↓            ↓
  Domain map    Fitness    Behavioral   Present      Apply
  + inventory   rating     validation   + approve    changes
```

**Load briefings at each stage. Test with scenarios. Get approval. Execute.**
