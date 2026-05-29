---
name: repo-understanding-repository-architecture
description: Six-layer governance hierarchy (Vision → Principles → Conventions → Development → Agents → Workflows). Use when understanding repository structure, tracing rules to foundational values, explaining architectural decisions, or navigating layer relationships.
---

# Repository Architecture - Six-Layer Hierarchy

This Skill provides guidance on the six-layer architecture governing the open-sharia-enterprise repository. Each layer builds on the foundation above, creating complete traceability from vision to workflows.

## Purpose

Use this Skill when:

- Understanding repository governance structure
- Tracing rules back to foundational values
- Explaining architectural decisions
- Navigating layer relationships
- Creating new conventions or practices
- Understanding where Skills fit in the architecture

## The Six Layers

```
Layer 0: Vision       WHY WE EXIST       (foundational purpose)
Layer 1: Principles   WHY - Values       (governs L2, L3)
Layer 2: Conventions  WHAT - Doc Rules   (governs L3, L4)
Layer 3: Development  HOW - Practices    (governs L4)
Layer 4: AI Agents    WHO - Executors    (atomic tasks)
Layer 5: Workflows    WHEN - Orchestrate (multi-step processes)
```

**Key relationships:**

- Vision inspires Principles
- Principles govern Conventions and Development
- Conventions govern Development and Agents
- Development governs Agents
- Workflows orchestrate Agents

## Quick Layer Reference

| Layer | Location                | Purpose                       | Changes?        | Answers?                  |
| ----- | ----------------------- | ----------------------------- | --------------- | ------------------------- |
| **0** | governance/vision/      | WHY we exist                  | Extremely rare  | Why does project exist?   |
| **1** | governance/principles/  | WHY we value approaches       | Rarely          | Why value this approach?  |
| **2** | governance/conventions/ | WHAT documentation rules      | Occasionally    | What documentation rules? |
| **3** | governance/development/ | HOW we develop software       | More frequently | How develop software?     |
| **4** | .opencode/agent/        | WHO enforces rules            | Often           | Who enforces rules?       |
| **5** | governance/workflows/   | WHEN run agents in what order | As needed       | When run which agents?    |

## Layer 0: Vision (WHY WE EXIST)

**Purpose**: Foundational purpose - WHY the project exists and WHAT change we seek.

**Location**: `governance/vision/`

**Key Document**: [Vision - Open Sharia Enterprise](../../../governance/vision/open-sharia-enterprise.md)

**Core Vision**:

- Democratize Shariah-compliant enterprise
- Make Islamic finance accessible to everyone
- Open-source halal solutions anyone can use

**Characteristics**:

- Immutable foundational purpose
- Changes extremely rarely
- All other layers serve this vision

## Layer 1: Principles (WHY - Values)

**Purpose**: Foundational values that govern all conventions and development practices.

**Location**: `governance/principles/`

**Key Document**: [Core Principles Index](../README.md)

**Ten Principles** (abbreviated):

1. Simplicity Over Complexity
2. Accessibility First
3. Documentation First
4. No Time Estimates
5. Progressive Disclosure
6. Automation Over Manual
7. Explicit Over Implicit
8. Immutability Over Mutability
9. Pure Functions Over Side Effects
10. Reproducibility First

**Requirements**:

- Each principle MUST include "Vision Supported" section
- Stable, rarely change
- Govern both L2 (Conventions) and L3 (Development)

**Example Traceability**:

```
Vision: "Accessible to everyone"
    ↓ inspires
Principle: Accessibility First
    ↓ governs
Convention: Color Accessibility Convention
Development: Hugo Development Convention (semantic HTML)
```

## Layer 2: Conventions (WHAT - Documentation Rules)

**Purpose**: Documentation standards implementing core principles. Defines WHAT rules for writing, organizing, formatting documentation.

**Location**: `governance/conventions/`

**Key Document**: [Conventions Index](../README.md)

**Scope**:

- docs/ directory (all markdown)
- Hugo sites (ayokoding-web, ose-platform-web)
- plans/ directory
- README files

**Example Conventions**:

- File Naming Convention
- Linking Convention
- Color Accessibility Convention
- Content Quality Principles
- Diátaxis Framework

**Requirements**:

- Each convention MUST include "Principles Implemented/Respected" section
- Implemented by AI agents (Layer 4)
- Changes more frequently than principles

## Layer 3: Development (HOW - Software Practices)

**Purpose**: Software practices implementing core principles. Defines HOW we develop, test, deploy software.

**Location**: `governance/development/`

**Key Document**: [Development Index](../README.md)

**Scope**:

- Source code (JS, TS, future: Java, Kotlin, Python)
- Hugo themes and layouts
- Build systems and tooling
- AI agents (.opencode/agent/)
- Git workflows

**Example Practices**:

- Trunk Based Development
- Code Quality Convention (git hooks)
- AI Agents Convention
- Maker-Checker-Fixer Pattern
- Implementation Workflow

**Requirements**:

- Each practice MUST include BOTH "Principles Implemented/Respected" AND "Conventions Implemented/Respected" sections
- Implemented by AI agents and automation
- Changes more frequently than conventions

## Layer 4: AI Agents (WHO - Executors)

**Purpose**: Automated implementers enforcing conventions and development practices.

**Location**: `.opencode/agent/`

**Key Document**: [Agents Index](../README.md)

**Agent Families**:

- **Makers** (Blue) - Create/update content
- **Checkers** (Green) - Validate quality
- **Fixers** (Purple/Yellow) - Apply validated fixes
- **Navigation** - Manage structure
- **Operations** - Deploy and manage

**Characteristics**:

- Each agent enforces specific conventions/practices
- Atomic - one clear responsibility
- Frontmatter: name, description, tools, model, color

**Example Traceability**:

```
Convention: Color Accessibility
    ↓ implemented by
Agent: docs__checker (validates colors)
Agent: docs__fixer (applies corrections)
```

## Layer 5: Workflows (WHEN - Multi-Step Processes)

**Purpose**: Orchestrated multi-step processes composing AI agents.

**Location**: `governance/workflows/`

**Key Document**: [Workflows Index](../README.md)

**Workflow Families**:

- Maker-Checker-Fixer (content quality)
- Check-Fix (iterative validation)
- Plan-Execute-Validate (planning)

**Characteristics**:

- Define sequences (sequential/parallel/conditional)
- Manage state between steps
- Include human approval checkpoints
- Clear termination criteria

**Example**:

```
Maker-Checker-Fixer Workflow:
1. Maker creates → draft
2. Checker validates → audit report
3. User reviews → approve/reject
4. Fixer applies fixes → corrected
5. Terminate: all findings resolved
```

## Complete Traceability Example

### Color Accessibility (Vision → Agents)

**L0 - Vision**: Democratize Islamic enterprise → accessible to everyone

**L1 - Principle**: Accessibility First

- Vision supported: Accessible tools enable global participation
- Key value: Universal access from start

**L2 - Convention**: Color Accessibility Convention

- Implements: Accessibility First
- Rule: Verified color-blind friendly palette
- WCAG AA compliance required

**L3 - Development**: AI Agents Convention

- Respects: Color Accessibility Convention
- Practice: Agent colors use accessible palette
- Implementation: Frontmatter `color` field limited

**L4 - Agents**:

- docs\_\_checker - Validates diagram colors
- docs\_\_fixer - Applies color corrections
- agent\_\_maker - Validates agent frontmatter colors

**L5 - Workflow**: Maker-Checker-Fixer

- Orchestrates: maker → checker → fixer
- Ensures: All diagrams use accessible colors

## Where Skills Fit in the Architecture

**IMPORTANT**: Skills are **delivery infrastructure**, NOT a governance layer.

Skills sit alongside CLAUDE.md, AGENTS.md and direct references as delivery mechanisms, operating in two distinct modes:

### Inline Skills (Knowledge Delivery)

**Default behavior** - Progressive knowledge injection:

```
Knowledge Flow (Inline):
L2: Conventions ──┬── CLAUDE.md/AGENTS.md (startup) ──> Claude/OpenCode
                  ├── Skills inline (on-demand) ────> Current conversation
                  └── Direct refs (explicit) ───────> L4: Agents

L3: Development ──┬── CLAUDE.md/AGENTS.md (startup) ──> Claude/OpenCode
                  ├── Skills inline (on-demand) ────> Current conversation
                  └── Direct refs (explicit) ───────> L4: Agents
```

**Characteristics**:

- Progressive disclosure (name/description → full content on-demand)
- Inject convention/development knowledge into current conversation
- Enable knowledge composition (multiple skills work together)
- Serve agents but don't govern them

### Fork Skills (Task Delegation)

**Delegation behavior** with `context: fork`:

```
Delegation Flow (Fork):
Skills (context: fork) ──delegates to──> Isolated Agent Context
                         ──returns──> Summarized Results
                         ──to──> Main Conversation
```

**Characteristics**:

- Spawn isolated subagent contexts for focused work
- Delegate specialized tasks (research, analysis, exploration)
- Act as lightweight orchestrators
- Return results to main conversation
- Still service relationship (not governance)

**Key insight**: Skills SERVE agents through two modes:

- **Inline skills** - Deliver knowledge from L2/L3 to current conversation
- **Fork skills** - Delegate tasks to agents in isolated contexts
- Neither mode governs agents (service relationship, not governance)

**Governance test**:

- Conventions → Agents: Yes (agents MUST follow conventions)
- Development → Agents: Yes (agents MUST follow practices)
- Skills (inline) → Agents: **No** (inject knowledge, serve agents)
- Skills (fork) → Agents: **No** (delegate tasks, serve agents)

## Best Practices

### When Creating New Conventions

1. **Check principles first** - Which principle does this implement?
2. **Add traceability section** - "Principles Implemented/Respected"
3. **Document in Conventions Index** - Add to README.md
4. **Consider agent impact** - Which agents need to enforce this?

### When Creating New Development Practices

1. **Check both principles AND conventions** - What do you implement/respect?
2. **Add both traceability sections** - Principles AND Conventions
3. **Document in Development Index** - Add to README.md
4. **Consider automation** - Git hooks? AI agents?

### When Creating New Agents

1. **Identify governing layers** - Which conventions/practices does this enforce?
2. **Define atomic responsibility** - One clear purpose
3. **Choose tools carefully** - Match to task (Read-only, Write, Edit, Bash)
4. **Document in Agents Index** - Add to README.md

### When Creating Workflows

1. **Identify agent sequence** - What agents needed, in what order?
2. **Define termination criteria** - When does workflow complete?
3. **Add approval checkpoints** - Where does user review?
4. **Document state management** - How does state flow between steps?

## Common Misconceptions

### Misconception 1: "Skills are Layer 4.5"

❌ **Wrong**: Skills are not a layer between Development and Agents.

✅ **Correct**: Skills are delivery infrastructure (like AGENTS.md), not governance layer.

### Misconception 2: "Agents can ignore conventions if skilled"

❌ **Wrong**: Skills provide knowledge but don't override governance.

✅ **Correct**: Agents MUST follow conventions. Skills help agents understand conventions better.

### Misconception 3: "Workflows replace agents"

❌ **Wrong**: Workflows don't replace agents, they orchestrate them.

✅ **Correct**: Workflows compose multiple agents into multi-step processes.

### Misconception 4: "Principles can conflict"

❌ **Wrong**: Principles sometimes contradict each other.

✅ **Correct**: Principles complement each other. Apparent conflicts require nuanced application, not choosing one over another.

## References

- **[Repository Architecture](../../../governance/repository-governance-architecture.md)** - Complete architectural documentation with all traceability examples
- **[Core Principles Index](../README.md)** - All 10 foundational principles
- **[Conventions Index](../README.md)** - All 24 documentation conventions
- **[Development Index](../README.md)** - All 15 development practices
- **[Agents Index](../README.md)** - All AI agents and responsibilities
- **[Workflows Index](../README.md)** - All orchestrated processes

## Related Skills

- `maker-checker-fixer-pattern` - Understanding the three-stage quality workflow (fits in L3 Development)
- `color-accessibility-diagrams` - Example of L2 Convention implemented through Skills delivery
- `trunk-based-development` (Phase 2) - Example of L3 Development practice

---

**Note**: This Skill provides architectural overview. The authoritative Repository Architecture document contains complete traceability examples, detailed layer characteristics, and usage guidance.

See `reference.md` in this Skill directory for detailed layer characteristics and governance relationships.
