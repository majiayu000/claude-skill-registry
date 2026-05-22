---
name: building-blocks-advisor
description: Analyzes user requests to recommend appropriate Claude Code building blocks (skills, subagents, MCP servers, hooks, templates, or prompts). Use when users ask about extending Claude Code functionality, automating workflows, connecting external data, or when unclear which extensibility mechanism to use. Triggers include questions like "how do I...", "should I use a skill or agent", "how to automate...", "how to connect to...", or any request about creating extensions.
---

# Building Blocks Advisor

Helps choose the right Claude Code extensibility mechanism by analyzing requirements and recommending appropriate building blocks: Skills, Subagents, MCP Servers, Hooks, Templates, or Prompts.

## Decision Framework

Follow this process when a user asks about extending Claude Code or automating workflows:

### Step 1: Identify Core Requirements

Ask these questions (mentally or to the user if unclear):

**Data & Connectivity:**
- Does this need access to external data or systems?
- Is data from APIs, databases, or third-party tools required?

**Persistence:**
- Should this work across multiple conversations?
- Is this a one-time request or repeated workflow?

**Automation:**
- Should this trigger automatically at specific events?
- Or should it run only when explicitly requested?

**Specialization:**
- Does this need isolated context or specific tool permissions?
- Should multiple instances run in parallel?

**Content Structure:**
- Is this primarily about reusable content/boilerplate?
- Or about procedural knowledge and workflows?

### Step 2: Apply Decision Logic

Use this flowchart to recommend building blocks:

```
┌─────────────────────────────────────┐
│ Does it need external data/systems? │
└─────────────┬───────────────────────┘
              │
        YES ──┴── Recommend: MCP Server
              │   Examples: Database access, GitHub, Slack,
              │             Google Drive, custom APIs
              │
         NO ──┘
              │
┌─────────────▼───────────────────────┐
│ Should it trigger automatically?    │
└─────────────┬───────────────────────┘
              │
        YES ──┴── Recommend: Hook
              │   Examples: Auto-format on save, run tests
              │             before commit, validate on edit
              │
         NO ──┘
              │
┌─────────────▼───────────────────────┐
│ Is it primarily reusable content?   │
└─────────────┬───────────────────────┘
              │
        YES ──┴── Recommend: Template
              │   Examples: Boilerplate code, document
              │             templates, config file patterns
              │
         NO ──┘
              │
┌─────────────▼───────────────────────┐
│ Does it need isolated context or    │
│ specific tool permissions?          │
└─────────────┬───────────────────────┘
              │
        YES ──┴── Recommend: Subagent
              │   Examples: Code reviewer, security auditor,
              │             test generator, parallel tasks
              │
         NO ──┘
              │
┌─────────────▼───────────────────────┐
│ Will this be used across multiple   │
│ conversations?                      │
└─────────────┬───────────────────────┘
              │
        YES ──┴── Recommend: Skill
              │   Examples: Brand guidelines, domain expertise,
              │             workflows, coding standards
              │
         NO ──┘
              │
         └──── Recommend: Prompt
                 Examples: One-off requests, ad-hoc tasks,
                           interactive refinement
```

### Step 3: Recommend Building Block(s)

Based on the decision logic, recommend one or more building blocks. Many use cases benefit from combining multiple blocks.

**Present your recommendation in this format:**

```markdown
## Recommendation: [Building Block Name]

**Why:** [1-2 sentences explaining why this fits the requirements]

**What to create:** [Specific guidance on what to build]

**Example structure:** [Optional - show file/folder structure if helpful]

**Additional considerations:** [Optional - mention complementary building blocks or caveats]
```

### Common Combinations

Many scenarios benefit from combining multiple building blocks:

**Skill + MCP:**
- MCP provides data access
- Skill teaches Claude how to use that data
- Example: MCP for BigQuery + Skill for query patterns

**Skill + Template:**
- Template provides content structure
- Skill teaches when and how to use templates
- Example: Skill for brand guidelines + Templates for branded documents

**Subagent + Skill:**
- Subagent provides isolated context
- Skill teaches domain expertise
- Example: Code review subagent + Testing best practices skill

**Hook + Skill:**
- Hook automates triggering
- Skill provides the workflow/logic
- Example: Pre-commit hook + Linting skill

**MCP + Subagent:**
- MCP connects to external data
- Subagent processes data with specific permissions
- Example: Database MCP + Analytics subagent (read-only access)

## Example Analyses

### Example 1: "I want Claude to always use my company's branding"

**Analysis:**
- Needs to persist across conversations ✓
- Not automated/event-driven ✗
- Not external data ✗
- Procedural knowledge (brand guidelines) ✓

**Recommendation: Skill**

Why: Brand guidelines are persistent procedural knowledge that should apply across conversations. A skill can include color palettes, typography rules, logo assets, and usage guidelines.

What to create:
```
brand-guidelines/
├── SKILL.md (brand rules and when to apply them)
└── assets/
    ├── logo.png
    ├── color-palette.png
    └── templates/ (branded document templates)
```

### Example 2: "I need to query my PostgreSQL database"

**Analysis:**
- Needs external data access ✓
- Persistent connection ✓

**Recommendation: MCP Server**

Why: Accessing external databases requires an MCP server to establish persistent connections and expose query tools.

What to create: Use an existing PostgreSQL MCP server or create a custom one if you need specific query patterns.

Additional considerations: Combine with a Skill that teaches Claude about your database schema and common query patterns.

### Example 3: "I want code review before every commit"

**Analysis:**
- Event-driven automation ✓
- Pre-commit timing ✓
- Specialized review context ✓

**Recommendation: Hook + Subagent**

Why: Use a pre-commit hook to trigger automatically, and a code-reviewer subagent for isolated context and specialized analysis.

What to create:
1. Configure a `pre-commit` hook in Claude Code settings
2. Hook should spawn the `code-reviewer` subagent
3. Subagent reviews changes and blocks commit if issues found

### Example 4: "I need standard API error response format"

**Analysis:**
- Reusable content structure ✓
- Not automated ✗
- Not external data ✗

**Recommendation: Template (in Skill)**

Why: This is a reusable content pattern that doesn't require procedural knowledge.

What to create:
```
api-patterns/
├── SKILL.md (when to use error templates)
└── assets/
    └── error-response-template.json
```

## Quick Reference Table

| If the user needs... | Recommend... |
|---------------------|--------------|
| Access external data (APIs, databases, files) | **MCP Server** |
| Automate at specific events (pre-commit, on-save) | **Hook** |
| Isolated context or parallel execution | **Subagent** |
| Procedural knowledge across conversations | **Skill** |
| Reusable content/boilerplate | **Template** (often in Skill assets) |
| One-off or ad-hoc request | **Prompt** |
| Teach workflows + access data | **Skill + MCP** |
| Auto-trigger + specialized analysis | **Hook + Subagent** |

## Detailed Definitions

For comprehensive explanations of each building block, including characteristics, structure, and best practices, see [references/building-blocks.md](references/building-blocks.md).

**When to consult the reference:**
- Need detailed characteristics or capabilities
- Want to understand implementation structure
- Looking for more examples
- Comparing multiple building blocks
