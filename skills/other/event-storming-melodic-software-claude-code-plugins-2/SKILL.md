---
name: event-storming
description: AI-simulated event storming workshop with multi-persona support. Use when discovering domain events, commands, actors, and bounded contexts. Supports three modes - full-simulation (5 persona agents debate), quick (single-pass analysis), and guided (interactive with user). Orchestrates persona agents and synthesizes results.
allowed-tools: Read, Write, Glob, Grep, Skill, Task, AskUserQuestion
---

# Event Storming

## Interactive Workshop Configuration

Use AskUserQuestion to configure the event storming session:

```yaml
# Question 1: Workshop Mode (MCP: Event Storming methodology)
question: "Which event storming mode do you need?"
header: "Mode"
options:
  - label: "Full Simulation (Recommended)"
    description: "All 5 personas debate in parallel, 6 phases (~15K tokens)"
  - label: "Quick"
    description: "Single analysis pass, no personas (~3K tokens)"
  - label: "Guided"
    description: "Interactive with user, personas on-demand"
  - label: "Codebase Analysis"
    description: "Discover events from existing code structure"

# Question 2: Domain Scope (MCP: DDD bounded context patterns)
question: "How complex is the domain you're exploring?"
header: "Scope"
options:
  - label: "Single Bounded Context"
    description: "One domain area, focused discovery"
  - label: "Multiple Contexts"
    description: "Identify 2-5 bounded context boundaries"
  - label: "Enterprise Domain"
    description: "Comprehensive cross-domain mapping"
  - label: "Unknown"
    description: "Help me determine scope first"
```

Use these responses to select the appropriate workshop mode and calibrate depth of analysis.

## When to Use This Skill

Use this skill when you need to:

- Discover domain events for a business process
- Identify commands and actors in a system
- Find bounded context boundaries
- Simulate a multi-stakeholder event storming workshop
- Prepare for actual event storming facilitation
- Analyze an existing codebase for domain events

**Keywords:** event storming, domain events, commands, actors, bounded contexts, aggregates, domain discovery, workshop simulation, multi-persona, DDD

## What is Event Storming?

Event Storming is a workshop-based method for collaborative domain discovery. Participants use sticky notes to map out:

- **Events** (Orange) - Things that happen in the domain
- **Commands** (Blue) - Actions that trigger events
- **Actors** (Yellow) - Who issues commands
- **Aggregates** (Yellow) - Business entities that handle commands
- **Read Models** (Green) - Information needed for decisions
- **Policies** (Purple) - Business rules and reactions
- **External Systems** (Pink) - Outside integrations
- **Hot Spots** (Red/Pink) - Areas of confusion or conflict

## Workshop Modes

This skill supports three modes of operation:

| Mode | Description | Token Cost | Use Case |
| --- | --- | --- | --- |
| `full-simulation` | All 5 personas debate in parallel, 6 phases | ~15K tokens | Comprehensive discovery |
| `quick` | Single analysis pass, no personas | ~3K tokens | Quick domain overview |
| `guided` | Interactive with user, personas on-demand | Variable | User wants control |

### Mode Selection Guide

**Use `full-simulation` when:**

- Starting a new project or major feature
- You need comprehensive domain discovery
- Multiple perspectives are valuable
- Time is less critical than thoroughness

**Use `quick` when:**

- You need a fast domain overview
- Token budget is constrained
- Domain is relatively simple
- You'll refine later

**Use `guided` when:**

- You want to drive the process
- You have specific questions
- You want to invoke specific personas
- Interactive exploration is preferred

## Multi-Persona Simulation

The full-simulation mode uses 5 specialized agents to simulate different stakeholder perspectives:

| Persona Agent | Role | Perspective | Contributions |
| --- | --- | --- | --- |
| `domain-expert` | Subject Matter Expert | Deep business knowledge | Domain events, business rules, edge cases |
| `developer-persona` | Technical Implementation | System constraints | Technical events, integration points |
| `business-analyst` | Process & Requirements | Process flow | Commands, actors, acceptance criteria |
| `product-owner` | Product Vision | User value | Priorities, MVP scope, user stories |
| `devils-advocate` | Challenger | Identify gaps | Hot spots, missing scenarios, contradictions |

## 6 Workshop Phases (Full Simulation)

### Phase 1: Chaotic Exploration

All personas brainstorm events independently. No constraints, no ordering.

**Orchestration:**

```markdown
Launch 5 parallel Task agents:
- Task(event-storming-persona domain-expert, "Identify all domain events for: {domain}")
- Task(event-storming-persona developer, "Identify technical events for: {domain}")
- Task(event-storming-persona business-analyst, "Identify commands and actors for: {domain}")
- Task(event-storming-persona product-owner, "Prioritize and identify MVP scope for: {domain}")
- Task(event-storming-persona devils-advocate, "Challenge and identify gaps for: {domain}")
```

### Phase 2: Timeline Ordering

Synthesize and order events chronologically. Create the timeline.

### Phase 3: Command Discovery

Identify what triggers each event. Map commands to events.

### Phase 4: Actor Identification

Map who issues each command. Define roles and systems.

### Phase 5: Bounded Context Discovery

Group related events/commands. Identify natural boundaries.

### Phase 6: Hot Spot Resolution

Devil's advocate challenges. Resolve conflicts and gaps.

**Detailed phase guidance:** See `references/workshop-facilitation.md`

## Sticky Note Color Convention

| Color | Represents | Example |
| --- | --- | --- |
| 🟧 Orange | Domain Event | "Order Placed", "Payment Received" |
| 🟦 Blue | Command | "Place Order", "Process Payment" |
| 🟨 Yellow (small) | Actor | "Customer", "Admin", "System" |
| 🟨 Yellow (large) | Aggregate | "Order", "Customer", "Product" |
| 🟩 Green | Read Model | "Order Summary", "Product Catalog" |
| 🟪 Purple | Policy | "When order placed, reserve inventory" |
| 🟫 Pink | External System | "Payment Gateway", "Email Service" |
| ❗ Red/Pink | Hot Spot | Areas of confusion or conflict |

**Detailed conventions:** See `references/sticky-note-types.md`

## Orchestration Pattern

Since Claude Code subagents cannot spawn other subagents, the main conversation orchestrates:

```text
Main Conversation
    ↓
Invokes event-storming skill
    ↓
Skill guides parallel Task tool calls:
    ├── Task(event-storming-persona domain-expert, prompt)
    ├── Task(event-storming-persona developer, prompt)
    ├── Task(event-storming-persona business-analyst, prompt)
    ├── Task(event-storming-persona product-owner, prompt)
    └── Task(event-storming-persona devils-advocate, prompt)
    ↓
Skill synthesizes results with provenance tracking
    ↓
Outputs event catalog with [persona] attribution
```

## Quick Start

### Full Simulation Mode

```markdown
I want to run a full event storming simulation for an e-commerce order management system.

Please:
1. Launch all 5 persona agents in parallel
2. Have them analyze the domain
3. Synthesize their findings
4. Identify bounded contexts
5. Resolve any hot spots
```

### Quick Mode

```markdown
Give me a quick event storm overview for a subscription billing system.
Focus on the core happy path events.
```

### Guided Mode

```markdown
Let's do a guided event storming session for a hospital appointment system.
Start with the patient booking journey and I'll guide from there.
```

## Output Format

The event storming session produces a structured event catalog:

```markdown
# Event Storm: [Domain Name]

## Event Catalog

### [Bounded Context Name]

**Events:**
- [Event Name] [Domain Expert] - [Description]
- [Event Name] [Developer] - [Description]

**Commands:**
- [Command Name] → [Event Name] [Business Analyst]

**Actors:**
- [Actor Name]: [Commands they can issue]

**Aggregates:**
- [Aggregate Name]: [Events it produces]

**Policies:**
- [Policy Name]: [Trigger] → [Action]

## Bounded Contexts Identified

1. [Context Name]
   - Core Domain / Supporting / Generic
   - [Events in this context]

## Hot Spots

- [Issue] - [Resolution or TODO]
```

**Full template:** See `references/templates/event-storm-output.md`

## Integration with Other Skills

Event storming connects with:

- **domain-storytelling** - Stories feed into event discovery
- **modular-architecture** - Bounded contexts become modules
- **fitness-functions** - Module isolation tests
- **adr-management** - Document bounded context decisions

**Workflow:**

```text
Domain Storytelling → Event Storming → Modular Architecture
(understand "what")   (design "how")   (implement "where")
```

## Best Practices

1. **Start with events** - Events are facts, commands are debatable
2. **Use past tense** - "Order Placed" not "Place Order"
3. **Explore boundaries** - Events help find module boundaries
4. **Embrace chaos** - Initial brainstorming should be messy
5. **Track provenance** - Know which perspective each insight came from
6. **Resolve hot spots** - Don't leave conflicts unaddressed

## References

- `references/workshop-facilitation.md` - Phase orchestration and timing
- `references/persona-prompts.md` - Prompt templates for each persona
- `references/sticky-note-types.md` - Color conventions and usage
- `references/bounded-context-discovery.md` - Context identification patterns
- `references/templates/event-storm-output.md` - Output format with provenance

## Version History

- **v1.0.0** (2025-12-22): Initial release
  - Multi-persona simulation with 5 agents
  - Three workshop modes (full, quick, guided)
  - 6-phase workshop structure
  - Provenance tracking for insights
  - Integration with domain-storytelling and modular-architecture

---

## Last Updated

**Date:** 2025-12-22
**Model:** claude-opus-4-5-20251101
