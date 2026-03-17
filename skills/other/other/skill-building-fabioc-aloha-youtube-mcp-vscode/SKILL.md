---
name: "Skill Building"
description: "Create effective, reusable skills from real-world experience for promotion to Master Alex"
applyTo: "**/*skill*,**/*SKILL*,**/skills/**"
---

# Skill Building

> Create effective, reusable skills from real-world experience

Meta-skill for heirs to build high-quality skills that can be promoted to Master Alex.

---

## When to Use

- After completing a project with reusable learnings
- When you've discovered gotchas worth documenting
- When patterns are ready to be promoted to Master
- When creating new domain expertise from scratch

---

## The Skill Creation Workflow

### Phase 1: Wait for Validation

**Never create skills from theory.** Wait for:

| ✅ Ready Signal | ❌ Too Early |
|-----------------|--------------|
| Project shipped/deployed | Still designing |
| Bug discovered and fixed | Theoretical solution |
| Pattern used 3+ times | First attempt |
| Gotcha encountered | Guessing at edge cases |

> *A skill written after successful delivery is worth 10x one written from theory.*

### Phase 2: Define Scope

**Answer these questions first:**

1. **What problem does this skill solve?** (1 sentence)
2. **What are the key gotchas?** (list 3-5)
3. **What would I tell a colleague?** (elevator pitch)
4. **Does this already exist?** (check skill catalog)

**Scope Check:**

| Scope | Symptom | Action |
|-------|---------|--------|
| Too broad | "Everything about X" | Split into multiple skills |
| Too narrow | Only one use case | Merge into related skill |
| Just right | Clear boundaries, multiple uses | Proceed |

### Phase 3: Create the Skill

**Folder Structure:**

```text
.github/skills/{skill-name}/
├── SKILL.md          # Required: Main content
├── synapses.json     # Optional: Brain connections
└── {assets}          # Optional: Templates, CSS, scripts
```

**Naming Convention:**

| Pattern | Examples |
|---------|----------|
| `{domain}-{sub}` | `azure-architecture-patterns`, `api-design` |
| `{tool}-{purpose}` | `markdown-mermaid`, `sharp-cli` |
| `{action}-{context}` | `debugging-patterns`, `error-recovery` |

---

## SKILL.md Template

```markdown
---
applyTo: "{glob-patterns}"
---

# {Skill Name}

> {One-line description — what + who}

{2-3 sentence intro with context}

---

## When to Use

- {Primary use case}
- {Secondary use case}
- {Edge case that surprised you}

---

## Quick Reference

{Most important info — tables, cheat sheets, one-liners}

---

## {Module 1: Core Concept}

{Main content organized by topic}

### {Sub-section}

{Details, patterns, examples}

---

## {Module N: Advanced}

{Progressive disclosure — basics first, advanced later}

---

## Troubleshooting

### {Problem Title}

**Problem**: {What goes wrong}

**Solution**: {How to fix it}

**Why**: {Root cause for learning}

---

## Activation Patterns

| Trigger | Response |
|---------|----------|
| "{keyword}" | Full skill activation |
| "{partial keyword}" | {Specific module} |

---

*Skill created: {date} | Category: {category} | Status: Active*

---

## Synapses

- [{related-skill}/SKILL.md] ({Strength}, {Type}, {Direction}) - "{When}"
- [{related-instructions}.md] ({Strength}, {Type}, {Direction}) - "{When}"
```

---

## applyTo Patterns

Choose patterns that match when this skill should activate:

| Pattern | When to Use | Example Skills |
|---------|-------------|----------------|
| `**/*.{ext}` | File-type specific | `typescript-patterns` |
| `**/*{keyword}*` | Name-based activation | `markdown-mermaid` |
| `**/test*` | Context-based | `testing-strategies` |
| `src/**` | Location-based | `frontend-patterns` |

**Common Combinations:**

```yaml
# Documentation skills
applyTo: "**/*.md,**/readme*,**/docs/**"

# TypeScript skills  
applyTo: "**/*.ts,**/*.tsx,**/tsconfig*"

# Azure skills
applyTo: "**/azure*,**/bicep*,**/arm*,**/*.bicep"

# Broad activation (use sparingly)
applyTo: "**/*"
```

---

## Synapse Guidelines

### When to Add Synapses

| Connection Type | When | Example |
|-----------------|------|---------|
| **Enables** | This skill makes another possible | slide-design → dissertation-defense |
| **Enhances** | This skill improves another | coaching → executive-storytelling |
| **Requires** | This skill depends on another | citation → literature-review |
| **Extends** | This skill adds to another | airs-integration → appropriate-reliance |

### Strength Values

| Strength | Meaning | Use When |
|----------|---------|----------|
| **Critical** (0.95-1.0) | Always co-activate | Core dependencies |
| **High** (0.8-0.94) | Usually co-activate | Strong relationships |
| **Medium** (0.6-0.79) | Sometimes co-activate | Contextual connections |
| **Low** (0.4-0.59) | Rarely co-activate | Weak associations |

### Direction Types

| Direction | Meaning | Symbol |
|-----------|---------|--------|
| **Forward** | I help them | → |
| **Bidirectional** | Mutual benefit | ↔ |
| **Backward** | They help me | ← |

**Format:**
```markdown
- [.github/skills/{skill}/SKILL.md] (High, Enables, Bidirectional) - "When X happens"
```

---

## Quality Checklist

Before promoting to Master, verify:

### Content Quality

- [ ] **Validated**: Based on real-world experience, not theory
- [ ] **Gotchas included**: Hard-won lessons documented
- [ ] **Actionable**: Reader can immediately apply
- [ ] **Examples**: Code/patterns are concrete, not abstract

### Structure Quality

- [ ] **Quick Reference**: Most useful info first
- [ ] **Progressive disclosure**: Basics → Advanced
- [ ] **Troubleshooting**: Common problems solved
- [ ] **Activation patterns**: Clear triggers defined

### Integration Quality

- [ ] **applyTo set**: Appropriate glob patterns
- [ ] **Synapses defined**: 2-5 meaningful connections
- [ ] **No duplication**: Doesn't overlap with existing skills
- [ ] **Keywords identified**: For skill-activation index

---

## Promotion Readiness Score

Calculate before requesting Master promotion:

| Criterion | Points | Your Score |
|-----------|--------|------------|
| Has applyTo frontmatter | +2 | |
| Has Synapses section | +3 | |
| Has Troubleshooting | +2 | |
| Has code examples | +2 | |
| Content > 100 lines | +1 | |
| Content > 200 lines | +2 | |
| Uses generic terms (not project-specific) | +1-3 | |
| Has Activation Patterns | +1 | |
| **Total** | | **/16** |

**Promotion thresholds:**
- **≥12**: Ready for Master
- **8-11**: Needs refinement
- **<8**: Keep developing

---

## Recognizing Shallow vs Deep Content

The biggest failure mode in skill creation is the **capabilities-list anti-pattern** — a skill that reads like a product brochure instead of encoding real knowledge.

### The Capabilities-List Anti-Pattern

```markdown
# ❌ SHALLOW — adds zero value
Expert in domain-agnostic knowledge acquisition.

## Capabilities
- Guide conversational knowledge acquisition
- Create skill files
- Build expertise through progressive questioning

## When to Use
- User wants to learn something new
- Teaching Alex about a domain
```

**Why this fails**: An LLM already knows how to "guide conversational learning" generically. The skill adds nothing the model didn't already have. It's a capability *label*, not capability *knowledge*.

### What Deep Looks Like

```markdown
# ✅ DEEP — encodes specific, actionable knowledge

## Phase 2: Foundation — Nail the core concepts

- Ask for the simplest possible explanation of each concept
- Demand concrete examples, not abstractions
- Test understanding by explaining it back
- **Red flag**: If the explanation uses jargon from the same domain, you haven't bottomed out

**Exit criteria**: Can explain core concepts without jargon.
```

### Depth Assessment Rubric

| Signal | Shallow | Deep |
|--------|---------|------|
| Opening line | "Expert in X" / "Capabilities:" | Specific insight or principle |
| Tables | Category labels only | Real data: thresholds, trade-offs, examples |
| Sections | "When to Use" / "Input/Output" | Domain-specific knowledge modules |
| Advice | Generic ("be careful") | Specific ("timeout after 30s because...") |
| Examples | None or abstract | Concrete, copy-pasteable, with context |
| Anti-patterns | Not mentioned | Named, explained, with alternatives |

### The Litmus Test

For each section, ask: **"Would an LLM produce something equally useful without this skill?"**

- If **yes** → the section is shallow, rewrite or remove it
- If **no** → the section earns its place

---

## Trifecta Decision Framework

A **trifecta** = SKILL.md (declarative) + .instructions.md (procedural) + .prompt.md (interactive). Not every skill needs one.

### When to Build a Trifecta

| Signal | Needs Trifecta? | Why |
|--------|:-:|------|
| Skill describes a multi-step workflow | **Yes** | Steps need procedural memory (.instructions.md) |
| Users need guided conversation | **Yes** | Interactive workflow needs episodic memory (.prompt.md) |
| Skill is reference knowledge only | **No** | Table lookups don't need procedures |
| Process is already covered by another trifecta | **No** | Avoid duplication |
| Skill is used frequently + is error-prone | **Yes** | High value from step-by-step guidance |
| Skill is domain expertise (patterns, anti-patterns) | **No** | SKILL.md alone is the right memory type |

### Trifecta Components — What Goes Where

| Component | Memory Type | Contains | Example |
|-----------|-------------|----------|----------|
| SKILL.md | Declarative ("what") | Domain knowledge, tables, thresholds, patterns | testing-strategies: pyramid, mock rules, coverage philosophy |
| .instructions.md | Procedural ("how") | Step-by-step process, decision points, checkpoints | release-management: version bump → changelog → build → publish |
| .prompt.md | Episodic ("interact") | Guided conversation, user Q&A, session templates | /learn: Socratic learning flow |

**Rule**: If the skill's value is in its *reference data* (tables, thresholds, patterns), a SKILL.md alone is correct. Only add procedures/prompts when there's a genuine *process* to guide.

### Building the Trifecta

1. **Start with SKILL.md** — always create the declarative knowledge first
2. **Observe usage** — is there a repeatable process emerging?
3. **Add .instructions.md** — when you can write numbered steps with decision points
4. **Add .prompt.md** — when users need an interactive guided experience
5. **Register in catalogs** — update TRIFECTA-CATALOG.md

---

## Muscle Assessment

A **muscle** is an execution script in `.github/muscles/` — the motor cortex of the architecture. Scripts, not memory.

### When to Create a Muscle

| Signal | Create Muscle? | Example |
|--------|:-:|----------|
| Same terminal commands run repeatedly | **Yes** | `brain-qa.ps1` — synapse validation |
| File validation that could be automated | **Yes** | `validate-skills.ps1` — schema checking |
| Multi-file transformations | **Yes** | `sync-architecture.js` — heir sync |
| Decision-making that requires judgment | **No** | Code review (that's a skill, not a script) |
| Creative work | **No** | Writing (LLM does this, not a script) |
| One-time operation | **No** | Not worth automating |

### Muscle Naming Convention

| Pattern | Example | What It Does |
|---------|---------|---------------|
| `{verb}-{noun}.ps1` | `validate-synapses.ps1` | PowerShell validation |
| `{verb}-{noun}.js` | `sync-architecture.js` | Node.js transformation |
| `{noun}-{noun}.ps1` | `brain-qa.ps1` | PowerShell audit |

### Muscle + Trifecta Integration

A muscle is *referenced by* a trifecta but is never a memory component itself:

```
SKILL.md          → "What to check" (knowledge)
.instructions.md  → "Step 5: Run brain-qa.ps1" (procedure)
.prompt.md        → "Shall I run the health check?" (interaction)
brain-qa.ps1      → Actually runs the check (execution)
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Write skill before project starts | Ship first, document after |
| Copy-paste from docs | Add your insights and gotchas |
| Create single-use skills | Wait for 3+ use cases |
| Skip synapses | Connect to 2-5 related skills |
| Use project-specific names | Generalize (MyAppConfig → config patterns) |
| Mega-skill (1000+ lines) | Split into focused skills |
| Orphan skill (no connections) | Always connect to network |
| Write capabilities lists | Encode real domain knowledge |
| Build trifecta for reference skills | SKILL.md alone for lookup knowledge |
| Create muscle for one-time tasks | Only automate repeating operations |

---

## Examples: Good vs Bad

### ❌ Bad Skill Start

```markdown
# My Azure Function

> How I built my Azure Function

## Setup
1. Created function app
2. Added my config...
```

**Problems**: Project-specific, no reusability, no patterns

### ✅ Good Skill Start

```markdown
# Azure Functions Patterns

> Production patterns for serverless Azure development

## When to Use
- HTTP-triggered APIs
- Event-driven processing
- Scheduled jobs

## Quick Reference

| Trigger | Use When | Gotcha |
|---------|----------|--------|
| HTTP | API endpoints | Cold start 5-10s |
| Timer | Scheduled jobs | UTC timezone only |
...
```

**Why better**: General patterns, table for quick reference, gotchas included

---

## Skill Consolidation (KISS Merge)

When related skills exist, merge rather than proliferate:

### When to Merge

- 2+ skills serve same domain
- Skills would always be used together
- Content overlap > 30%

### Merge Process

1. **Choose anchor**: Most comprehensive skill
2. **Absorb content**: Move unique sections from others
3. **Update synapses**: Redirect connections to anchor
4. **Archive sources**: Keep in heir for history
5. **Document merge**: Note absorbed skills at bottom

**Example:**
```markdown
*Skill created: 2026-02-10 | Category: Communication | Status: Active*
*Merged: stakeholder-management, meeting-efficiency*
```

---

## After Creation: Register with Skill-Activation

Add your skill to the action-keyword index:

**Location**: `.github/skills/skill-activation/SKILL.md`

**Format:**
```markdown
| {skill-name} | {keyword1}, {keyword2}, {keyword3} |
```

**Choose keywords that users would actually say:**
- Action verbs: "create", "debug", "design"
- Domain terms: "azure", "mermaid", "citation"
- Problem phrases: "not working", "how to"

---

## Synapses

- [.github/instructions/skill-building.instructions.md] (Critical, Implements, Forward) - "Step-by-step procedure for creating and completing skills"
- [.github/instructions/bootstrap-learning.instructions.md] (High, Enables, Bidirectional) - "Learning becomes skill"
- [.github/instructions/heir-skill-promotion.instructions.md] (Critical, Implements, Forward) - "Skill ready for promotion"
- [.github/skills/skill-activation/SKILL.md] (High, Integrates, Forward) - "Register for discovery"
- [.github/skills/skill-catalog-generator/SKILL.md] (Medium, Triggers, Forward) - "Regenerate catalog after creation"
- [SYNAPSE-SCHEMA.md](../SYNAPSE-SCHEMA.md) (High, References, Backward) - "Canonical synapse architecture reference"

---

*Skill created: 2026-02-10 | Category: Meta-Skills | Status: Active*
