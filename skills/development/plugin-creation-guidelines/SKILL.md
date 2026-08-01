---
name: plugin-creation-guidelines
description: 'Comprehensive plugin architecture patterns, best practices, templates,
  and validation guidelines distilled from research sources. Use when: creating new
  plugins, designing plugin architecture, validat'
---

---
name: plugin-creation-guidelines
description: Comprehensive plugin architecture patterns, best practices, templates, and validation guidelines distilled from research sources. Use when: creating new plugins, designing plugin architecture, validating plugin structure, or optimizing token usage. Do NOT use for: general coding tasks, non-plugin development, or debugging existing code.
---

# Plugin Creation Guidelines

Comprehensive reference for building well-architected Claude Code plugins following industry best practices, token optimization principles, and architectural patterns from official Anthropic sources and validated implementations.

*This skill distills best practices from blog posts, Anthropic examples, and official documentation. See [Research Sources](#research-sources) section and [references.md](references.md) for complete attribution.*

## Architecture Patterns

Choose the appropriate architecture pattern based on your plugin's requirements. Each pattern has specific use cases and trade-offs.

### 1. Single Agent Pattern

**Description**: One agent handles all responsibilities for the plugin.

**When to Use**:
- Simple, focused functionality (e.g., code formatter, linter)
- No parallel execution needed
- Single workflow with sequential steps
- Token budget fits comfortably in 300-400 lines

**Structure**:
```
plugin-name/
├── .claude-plugin/plugin.json
├── agents/
│   └── plugin-name.md           # Single agent (300-400 lines)
├── commands/
│   └── command-name.md           # Entry point
└── README.md
```

**Example**: Simple code analyzer that runs sequentially through files.

**Decision Factors**:
- Can all logic fit in one agent (< 400 lines)?
- Is workflow naturally sequential?
- Does task require minimal coordination?

### 2. Orchestrator-Worker Pattern

**Description**: One orchestrator agent coordinates multiple specialized worker agents executing in parallel.

**When to Use**:
- Parallel execution provides significant speedup
- Multiple independent subtasks (e.g., auditing multiple pages)
- Need for specialized workers with different tool access
- Orchestrator needs coordination logic but workers are focused

**Structure**:
```
plugin-name/
├── .claude-plugin/plugin.json
├── agents/
│   ├── plugin-orchestrator.md    # Coordinator (250-350 lines)
│   └── plugin-worker.md          # Worker(s) (100-200 lines)
├── commands/
│   └── command-name.md           # Entry point
├── skills/
│   └── shared-guidelines/
│       └── SKILL.md               # Shared knowledge (300-500 lines)
└── README.md
```

**Example**: UI/UX Audit plugin - orchestrator crawls site and spawns parallel page auditors.

**Key Characteristics**:
- Orchestrator uses `Task` tool to spawn workers
- Workers are stateless, focused on single subtask
- Skill provides shared evaluation criteria/methodology
- Orchestrator compiles final results

**Decision Factors**:
- Are subtasks independent and parallelizable?
- Do workers need different tool sets?
- Is coordination logic substantial (>100 lines)?

**Reference Implementation**: `plugins/ui-ux-audit/`
- Orchestrator: 281 lines (crawling, coordination, summary)
- Worker: 108 lines (single page audit)
- Skill: 322 lines (audit methodology, terminology)

### 3. Pipeline Pattern

**Description**: Sequential chain of agents where each agent's output becomes the next agent's input.

**When to Use**:
- Multi-stage processing workflow
- Each stage requires different expertise/tools
- Output from one stage feeds next stage
- Clear stage boundaries with distinct responsibilities

**Structure**:
```
plugin-name/
├── .claude-plugin/plugin.json
├── agents/
│   ├── stage-1-agent.md          # First stage
│   ├── stage-2-agent.md          # Second stage
│   └── stage-3-agent.md          # Final stage
├── commands/
│   └── command-name.md           # Entry point
└── README.md
```

**Example**: Data processing pipeline - extract, transform, load stages.

**Key Characteristics**:
- First agent delegates to second via Task tool
- Second agent delegates to third, etc.
- Each agent validates input from previous stage
- Final agent produces consolidated output

**Decision Factors**:
- Is workflow naturally sequential?
- Does each stage require distinct tooling?
- Are stage outputs well-defined?

### 4. Skill-Augmented Pattern

**Description**: Single or multiple agents augmented with comprehensive skill reference(s) for shared knowledge.

**When to Use**:
- Significant domain knowledge or methodology needed
- Multiple agents need same reference material
- Templates, checklists, or evaluation criteria to share
- Keeping agents concise by externalizing static knowledge

**Structure**:
```
plugin-name/
├── .claude-plugin/plugin.json
├── agents/
│   └── agent-name.md             # References skill(s)
├── commands/
│   └── command-name.md
├── skills/
│   └── domain-guidelines/
│       ├── SKILL.md               # 300-500 lines
│       ├── templates/             # Optional
│       └── scripts/               # Optional
└── README.md
```

**Example**: Plugin-creator with comprehensive creation guidelines skill.

**Key Characteristics**:
- Skills are 300-500 lines (larger than agents is OK)
- Agents explicitly reference: "Use the `skill-name` skill for..."
- Skills contain methodology, not workflow logic
- Can combine with any other pattern

**Decision Factors**:
- Is there >100 lines of reference material?
- Do multiple agents need same knowledge?
- Is knowledge relatively static (not workflow logic)?

### Pattern Selection Decision Tree

```
Start
  │
  ├─ Is workflow parallelizable?
  │   ├─ Yes → Orchestrator-Worker Pattern
  │   └─ No ↓
  │
  ├─ Is workflow multi-stage with stage boundaries?
  │   ├─ Yes → Pipeline Pattern
  │   └─ No ↓
  │
  ├─ Is there >100 lines of reference material?
  │   ├─ Yes → Skill-Augmented Pattern (+ Single Agent)
  │   └─ No ↓
  │
  └─ Use Single Agent Pattern
```

**Note**: Patterns can be combined (e.g., Orchestrator-Worker + Skill-Augmented).

## Best Practices from Research Sources

### Token Optimization

**Target Agent Size**: 300-400 lines maximum

**Rationale**:
- Agents are loaded into context with every execution
- Larger agents = more tokens consumed per invocation
- 300-400 lines balances comprehensiveness with efficiency
- Reference: ui-ux-audit-orchestrator (281 lines), page auditor (108 lines)

**DRY Principle Application**:

**Bad** - Duplicating knowledge across agents:
```markdown
# agent-1.md (500 lines)
[150 lines of evaluation criteria]
[350 lines of workflow logic]

# agent-2.md (500 lines)
[150 lines of evaluation criteria - DUPLICATED]
[350 lines of workflow logic]
```

**Good** - Extract to skill:
```markdown
# agents/agent-1.md (200 lines)
Use the `evaluation-guidelines` skill for criteria.
[200 lines of workflow logic]

# agents/agent-2.md (200 lines)
Use the `evaluation-guidelines` skill for criteria.
[200 lines of workflow logic]

# skills/evaluation-guidelines/SKILL.md (400 lines)
[400 lines of evaluation criteria - single source of truth]
```

**Token Savings**: 1000 lines → 800 lines

**Reference Instead of Duplicate**:
- Extract methodology to skills
- Reference templates instead of inlining
- Use supporting scripts for boilerplate generation
- Link to external documentation for detailed specs

**Skills Are Exempted from Line Limits**:
- Skills can be 300-500 lines (comprehensive reference)
- Skills are loaded only when agents reference them
- Multiple agents can reference same skill (shared knowledge)

### Description Engineering

**WHEN + WHEN NOT Pattern**: Explicitly define boundaries to prevent incorrect routing.

**Structure**:
```
[What it does]. Use PROACTIVELY for [triggers]. Do NOT use for: [anti-patterns].
```

**Agent Examples**:

**Good**:
```yaml
description: Orchestrates comprehensive UI/UX audits by crawling web applications and coordinating parallel page auditors. Use PROACTIVELY for `/ui-ux-audit` command. Do NOT use for: single-page audits, code analysis, or accessibility testing.
```

**Bad** - Missing boundaries:
```yaml
description: Handles UI/UX audits for web applications.
```

**Skill Examples**:

**Good**:
```yaml
description: Professional UI/UX audit methodology and design vocabulary. Use when: conducting UI/UX audits, evaluating visual hierarchy, analyzing responsive design, assessing interaction patterns. Do NOT use for: code reviews, accessibility audits (WCAG), performance analysis, or security assessments.
```

**Bad** - No use case clarity:
```yaml
description: UI/UX audit guidelines and terminology.
```

**Key Elements**:
1. **Primary Function**: What the component does
2. **Proactive Triggers**: When to use it automatically (for agents with command entry points)
3. **Explicit Anti-patterns**: What NOT to use it for (prevents routing errors)

### Naming Conventions

**Plugin Names**:
- **Format**: `kebab-case`
- **Pattern**: `domain-focus` or `action-target`
- **Examples**: `ui-ux-audit`, `plugin-creator`, `development-workflow`
- **Avoid**: CamelCase, snake_case, spaces

**Agent Names**:
- **Format**: `kebab-case`
- **Pattern**: `[plugin-prefix-]role-descriptor`
- **Single-agent plugins**: `plugin-name` (matches plugin)
- **Multi-agent plugins**: `plugin-prefix-role` (e.g., `ui-ux-audit-orchestrator`)
- **Examples**: `plugin-creator`, `ui-ux-audit-orchestrator`, `ui-ux-page-auditor`

**Skill Names**:
- **Format**: `kebab-case`
- **Pattern**: `domain-guidelines` or `topic-reference`
- **Examples**: `plugin-creation-guidelines`, `ui-ux-audit-guidelines`
- **Directory name matches skill name**

**Command Names**:
- **Format**: `kebab-case` or `snake_case` (both acceptable)
- **Pattern**: `verb-object` or `action-target`
- **Examples**: `/create-plugin`, `/ui-ux-audit`, `/validate-plugin`
- **File name**: `command-name.md` (without the `/` prefix)

**Consistency Rules**:
- File name matches component name exactly
- Multi-agent plugins use consistent prefix
- All names lowercase only
- Hyphens for word separation (or underscores for commands)

### Integration Patterns

**Commands → Agents**: Explicit delegation in command markdown.

**Pattern**:
```markdown
# Command File: /create-plugin

## Delegation

Use the `plugin-creator` agent to execute this workflow.
```

**Agents → Skills**: Explicit reference in agent prompt.

**Pattern**:
```markdown
# Agent File: plugin-creator.md

## Skill Reference

Use the `plugin-creation-guidelines` skill for:
- Architecture patterns and decision trees
- Best practices from research sources
- Template structures and boilerplate patterns
```

**Agents → Agents**: Task tool delegation for spawning.

**Orchestrator Example**:
```markdown
### Delegation Protocol

Use the `Task` tool to spawn parallel auditors:
- Provide each auditor with assigned page URL
- Specify shared output file path
```

**Worker Example**:
```markdown
# Agent: ui-ux-page-auditor.md

## Statelessness Note

One-shot execution: Complete audit and append to shared file in single invocation.
```

**Skills → Scripts**: Skills can reference supporting scripts.

**Pattern**:
```markdown
# Skill: plugin-creation-guidelines

## Supporting Scripts

Available scripts in `scripts/` directory:
- `create-plugin-structure.sh <plugin-name>` - Creates directory skeleton
- `validate-naming.py <plugin-path>` - Validates naming conventions
```

**Integration Documentation**:
- Every component documents its integration points
- README includes component relationship diagram (text-based)
- Agents specify which other components they work with

### Tool Access Patterns

**Principle**: Only grant necessary tools to each agent.

**Common Tool Categories**:

| Category | Tools | Use When |
|----------|-------|----------|
| File Operations | Read, Write, Edit | Agent needs file access |
| Code Search | Grep, Glob | Agent searches codebase |
| Progress Tracking | TodoWrite | Complex multi-step workflows |
| Agent Coordination | Task | Spawning other agents |
| Sequential Thinking | mcp__sequentialthinking__sequentialthinking | Complex decision-making |
| User Interaction | AskUserQuestion | Interactive workflows |
| Shell Operations | Bash | Running scripts or commands |

**Anti-patterns**:
- Giving all agents all tools (token waste)
- Workers with `Task` tool when they never spawn subagents
- Agents with `Bash` when they never run scripts

**Note**: Skills and commands have NO tools. See orchestrator vs worker tool lists in `plugins/ui-ux-audit/agents/` for practical examples.

## Component Templates

Templates are available in the `templates/` directory:
- `plugin.json.template` - Plugin metadata structure
- `agent-frontmatter.template` - Agent YAML structure
- `skill-frontmatter.template` - Skill YAML structure
- `command-template.md` - Command markdown structure
- `README-template.md` - Plugin documentation structure

Read template files directly for complete structure and placeholders. Use generation scripts in `scripts/` for automated creation with proper formatting.

## Supporting Scripts

Scripts in the `scripts/` directory provide automation:
- **Generation**: `create-plugin-structure.sh`, `generate-plugin-json.py`, `generate-agent-boilerplate.py`, `generate-skill-boilerplate.sh`, `generate-command-boilerplate.sh`
- **Validation**: `validate-structure.sh`, `validate-naming.py`, `validate-schemas.py`, `count-tokens.sh`

All scripts support `--help` flag for detailed usage. Scripts output JSON for programmatic parsing.

## Validation

Use automated validation scripts for deterministic checks and `plugin-validator` agent for subjective analysis. See `checklists/` directory for comprehensive validation criteria including `component-validation.md` and `security-validation.md`.

## Reference Implementation

Study `plugins/ui-ux-audit/` for validated implementation of Orchestrator-Worker + Skill-Augmented pattern (orchestrator: 281 lines, worker: 108 lines, skill: 322 lines). Demonstrates all best practices including WHEN/WHEN NOT patterns, tool access optimization, and skill references.

## Integration Points

This skill is used by:
- `plugin-creator` agent for architecture planning and content generation
- `plugin-validator` agent for quality assurance checks
- `/create-plugin` command workflow (via plugin-creator agent)
- `/validate-plugin` command workflow (via plugin-validator agent)

## Research Sources

Best practices distilled from authoritative sources including blog posts, Anthropic official examples, and validated implementations.

**See `references.md` for complete source URLs and detailed attribution.**
