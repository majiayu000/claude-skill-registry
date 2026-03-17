---
name: "research-first-development"
description: "Build knowledge bases that build software — research before code, teach before execute"
---

# Research-First Development

> Build knowledge bases that build software — research before code, teach before execute

Methodology for AI-assisted development where investment in research, skill creation, and knowledge encoding **precedes** implementation. Discovered through the Dead Letter heir's masterclass on cognitive architecture utilization (February 2026).

---

## When to Use

- Starting any new project with Alex
- Entering a new implementation phase of an existing project
- Onboarding Alex to an unfamiliar domain
- When AI output quality is inconsistent (symptom: insufficient context)
- Before any complex multi-subsystem implementation

---

## Core Insight

Traditional software development: **Requirements → Design → Code → Test**

AI-assisted development with cognitive architecture: **Research → Teach → Plan → Execute**

> **The quality of AI output is directly proportional to the quality of knowledge in its context.**

Instead of the human writing code with AI assistance, **the human orchestrates intent while AI handles execution**. But AI can only execute what it understands. Therefore: invest in teaching before asking for output.

---

## The Research-First Paradigm

### Phase 0: Research Sprint (Before Any Code)

| Step | Activity | Output |
|------|----------|--------|
| 1 | **Competitive landscape analysis** | Understanding of prior art |
| 2 | **Technical feasibility research** | Deep research documents (3-5 minimum) |
| 3 | **Architecture decision records** | ADRs documenting key choices |
| 4 | **Core domain research** | Comprehensive domain knowledge |
| 5 | **Branding/identity decisions** | Project character and voice |

Each research document should:
- Explore one domain **exhaustively**
- Cite sources: academic papers, industry best practices, competitive analysis
- Be structured with clear sections, code examples, decision rationales
- Live in a `/docs/` or `/research/` directory

### Phase 1: Knowledge Encoding (Research → Skills)

| Step | Activity | Output |
|------|----------|--------|
| 1 | **Skill extraction** | 1-3 skills per research document |
| 2 | **Context instruction** | Central hub: `{project}-context.instructions.md` |
| 3 | **Workflow instruction** | Dev process: `{project}-development-workflow.instructions.md` |
| 4 | **Agent creation** | Builder + Validator agents |
| 5 | **Synapse wiring** | 2-4 connections per new file |

**Key distinction**:
- **Skills** encode *patterns and principles* — reusable, domain knowledge ("how does X work?")
- **Instructions** encode *procedures* — project-specific workflows ("how do I do X here?")

### Phase 2: Plan → Execute (Now You Code)

With sufficient knowledge encoded, implementation becomes **conversational**:

```
Human: "Implement the EventBus from the game engine spec"
Alex: [Loads skill, reads patterns, implements with full context]
```

No re-explanation. No context loss. No hallucinated patterns.

---

## The 4-Dimension Gap Analysis

**When**: Before each major implementation phase.
**Purpose**: Ensure knowledge coverage across all four knowledge types before coding begins.
**Cadence**: Every phase boundary, every major milestone.
**Interactive**: Run `/gapanalysis` prompt for guided execution.

### The Four Dimensions

| Code | Dimension | Question | Covers |
|------|-----------|----------|--------|
| **GA-S** | Skills | "Does Alex know the *patterns*?" | Domain knowledge, reusable techniques |
| **GA-I** | Instructions | "Does Alex know the *procedures*?" | Project-specific workflows, step-by-step |
| **GA-A** | Agents | "Does Alex have the right *roles*?" | Builder, Validator, Specialists |
| **GA-P** | Prompts | "Does Alex have the right *interactive workflows*?" | Guided commands, repeatable rituals |

### Protocol (Per Dimension)

#### Step 1: Inventory What You're Building

List all subsystems, features, and integrations for this phase.

```markdown
## Phase N: Implementation Scope
- [ ] Subsystem A: {description}
- [ ] Subsystem B: {description}
- [ ] Integration: {description}
```

#### Step 2: Inventory Existing Knowledge

Catalogue current knowledge across all four dimensions:

```markdown
## Current Knowledge Inventory
| Dimension | Count | Relevant to Phase N |
|-----------|-------|---------------------|
| Skills (GA-S) | {N} | {list relevant} |
| Instructions (GA-I) | {N} | {list relevant} |
| Agents (GA-A) | {N} | {list relevant} |
| Prompts (GA-P) | {N} | {list relevant} |
```

#### Step 3: Map Capabilities to Needs (Per Dimension)

**GA-S (Skills)**: For each subsystem — "If I ask 'how does {X} work?', is there a skill?"
**GA-I (Instructions)**: For each workflow — "If I ask 'how do I do {X} here?', is there an instruction?"
**GA-A (Agents)**: For each role — "Is there an agent with this mental model and skill set?"
**GA-P (Prompts)**: For each interactive workflow — "Is there a guided `/command` for this?"

#### Step 4: Score Coverage

| Dimension | Coverage % | Items Needed |
|-----------|-----------|--------------|
| GA-S: Skills | {%} | {missing patterns} |
| GA-I: Instructions | {%} | {missing procedures} |
| GA-A: Agents | {%} | {missing roles} |
| GA-P: Prompts | {%} | {missing workflows} |

**Decision gate:**
- All 4 ≥ 75%: **Proceed to coding**
- Any < 75%: **Fill gaps first**
- Any < 50%: **Research sprint needed**

#### Step 5: Fill Gaps Before Coding

Create missing skills, instructions, agents, and prompts. Wire synapses. **Then** begin implementation.

### GA-A Deep Dive: Agent Gap Analysis

Agents encode **cognitive roles** — distinct mental models with curated skill sets:

| Question | What It Detects |
|----------|----------------|
| "Is there a builder?" | Missing constructive thinker |
| "Is there a validator?" | Missing adversarial thinker |
| "Do agents hand off at domain boundaries?" | Missing specialization |
| "Does each agent load role-appropriate skills?" | Skill misconfiguration |
| "Are there domain-specific specialists?" | Missing for security, data, infrastructure |

**Minimum viable agent set**: Builder + Validator (the Two-Agent Pattern).

### GA-P Deep Dive: Prompt Gap Analysis

Prompts encode **interactive workflows** — guided sequences for repeatable tasks:

| Question | What It Detects |
|----------|----------------|
| "What do developers do repeatedly?" | Missing implementation prompts |
| "What workflows need specific sequencing?" | Missing structured prompts |
| "What tasks benefit from guided Alex interaction?" | Missing mentoring prompts |
| "Are there review/audit rituals?" | Missing quality prompts |

**Prompt categories to check:**

| Category | Prompt Pattern | Example |
|----------|---------------|---------|
| Implementation | `/{project}-implement` | Guided feature development |
| Testing | `/{project}-test` or `/redteam` | Interactive test authoring |
| Deployment | `/{project}-deploy` | Deployment checklist |
| Review | `/review` or `/{project}-audit` | Quality review workflow |
| Learning | `/learn` | Domain learning session |

---

## The Two-Agent Pattern

For any non-trivial project, create at least two agents with **distinct mental models**:

| Agent Type | Focus | Mental Model | Question |
|------------|-------|--------------|----------|
| **Builder** | Feature implementation | Constructive | "How do I create this?" |
| **Validator** | Quality assurance | Adversarial | "How do I break this?" |

### Why Separate Agents?

Adversarial thinking requires a **different context** than constructive thinking. Separating agents allows each to:
- Optimize for its role's vocabulary and patterns
- Load only relevant skills (builder loads implementation skills; validator loads testing/security skills)
- Hand off cleanly at domain boundaries

### Naming Convention

| Agent | File | Trigger |
|-------|------|---------|
| Builder | `{project}-dev.agent.md` | Implementation tasks |
| Validator | `{project}-qa.agent.md` | Testing, review, audit tasks |

### Validator Agent Commands (Template)

| Command | Purpose |
|---------|---------|
| `/redteam` | Adversarial testing sweep |
| `/audit` | Compliance / quality audit |
| `/stress-test` | Performance and reliability |
| `/consistency` | Cross-system consistency check |

---

## Synapse Hygiene (During Development)

Synapses wired **at creation time** are 10x more valuable than synapses discovered during maintenance. Practice "clean as you go":

| Practice | Why | How |
|----------|-----|-----|
| Wire at creation | Fresh knowledge = accurate connections | Add synapses when creating any skill/instruction |
| 2-4 connections minimum | Prevents isolated knowledge islands | Every new file connects to at least 2 existing files |
| Star topology for instructions | Central activation hub | Every instruction connects to the project context instruction |
| Run Dream before major phases | Catch broken connections early | `Alex: Dream (Neural Maintenance)` |
| Strength reflects reality | Don't over-connect | Critical = always co-activate; Low = rarely |

### Connection Strategy

```
project-context.instructions.md  (hub)
    ├── skill-a (Critical, Enables)
    ├── skill-b (Critical, Enables)
    ├── instruction-1 (High, Enables)
    ├── instruction-2 (High, Enables)
    └── agent (High, Implements)
```

---

## Process Outcomes

| Outcome | Without Research-First | With Research-First |
|---------|----------------------|---------------------|
| Implementation quality | AI guesses at patterns | AI follows documented patterns |
| Style consistency | Varies per prompt | Single source of truth |
| Context between sessions | Lost, must re-explain | Persists in files, auto-loaded |
| Domain onboarding | Each prompt re-teaches | Knowledge loaded automatically |
| Debugging | Must re-teach context | References authoritative docs |
| Quality testing | Ad-hoc, incomplete | Encoded knowledge + QA agent |

---

## Replication Checklist

To apply Research-First Development to any new project:

- [ ] **Research phase**: Create 3-5 deep research documents before coding
- [ ] **Context instruction**: Create `{project}-context.instructions.md` as the hub
- [ ] **Workflow instruction**: Create `{project}-development-workflow.instructions.md`
- [ ] **Core skills**: Extract 5-10 skills from research docs
- [ ] **Builder agent**: Create `{project}-dev.agent.md` for implementation
- [ ] **Validator agent**: Create `{project}-qa.agent.md` for testing
- [ ] **Interactive prompts**: Create `{project}-implement`, `{project}-test`, `{project}-deploy` prompts
- [ ] **Synapse network**: Wire all new files with 2-4 connections each
- [ ] **4D gap analysis**: Run GA-S, GA-I, GA-A, GA-P before each phase
- [ ] **Dream validation**: Run `Alex: Dream` to validate network health

---

## Heir Generalization

This skill is `inheritable` — every heir gets the full methodology.

### What Heirs Inherit

| Component | Heir Gets | Heir Customizes |
|-----------|-----------|-----------------|
| Research-first paradigm | Full methodology | Domain-specific research topics |
| 4-dimension gap analysis | GA-S, GA-I, GA-A, GA-P templates | Project-specific subsystem lists |
| Two-agent pattern | Builder + Validator template | Agent names, skills, commands |
| Synapse hygiene | Wiring discipline | Project-specific connections |
| `/gapanalysis` prompt | Interactive workflow | — (universal) |

### Heir Adaptation Flow

```
Master provides: methodology + templates + quality gates
Heir adapts: project-specific skills, instructions, agents, prompts
Heir validates: run gap analysis with project scope
Master absorbs: generalizable patterns promoted back via heir-skill-promotion
```

### What Flows Back to Master

When heir knowledge is cross-project applicable:
1. **Patterns** → new Master skills or GK patterns
2. **Processes** → refined Master instructions
3. **Agent templates** → new agent patterns in Master
4. **Prompt workflows** → new prompts in Master

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|-------------|-------------|------------|
| "Just start coding" | AI has no context, hallucinates patterns | Research → Teach → Plan → Execute |
| Skipping gap analysis | Discover missing knowledge mid-implementation | Run 4D protocol (GA-S/I/A/P) at every phase boundary |
| One mega-agent | Conflates builder/validator mental models | Separate agents with distinct roles |
| Orphan skills | Knowledge islands that never activate | Wire 2-4 synapses at creation time |
| Research without encoding | Raw documents aren't loadable context | Extract skills from every research doc |
| Theory-only skills | Untested patterns break under pressure | Validate with real implementation, then encode |
| Skills-only gap analysis | Misses procedures, roles, and workflows | Always run all 4 dimensions |
| No prompts for repeatable work | Developers re-invent workflows each time | Create guided prompts for repeated tasks |

---

## Relationship to Existing Protocols

| Protocol | Phase | Relationship |
|----------|-------|-------------|
| **Bootstrap Learning** | Research | Research-first uses bootstrap learning for domains Alex doesn't know |
| **Skill Selection Optimization** | Plan | SSO selects from skills that research-first created |
| **Project Scaffolding** | Execute | Scaffolding creates files; research-first creates *knowledge* first |
| **Skill Building** | Encode | Skill-building quality gates apply to research-extracted skills |
| **Dream Protocol** | Validate | Dream validates the synapse network research-first wired |
| **Heir Skill Promotion** | Promote | Heir knowledge flows back to Master via promotion protocol |
| **Research-First Workflow** | Procedure | Instruction file provides step-by-step procedures for this skill |

---

## Troubleshooting

### AI output is inconsistent quality

**Problem**: Some responses are excellent, others miss the mark.

**Solution**: Run gap analysis. Inconsistency = knowledge coverage gaps. The subsystems with good output have skills; those without are getting guessed at.

**Why**: AI quality is proportional to context quality. No skill loaded = no patterns to follow.

### "I don't have time for research"

**Problem**: Feels slow to research before coding.

**Solution**: Research pays compound dividends. 2 days of research saves 2 weeks of debugging. The heir proved this: 18 skills + 9 instructions created before Phase 0 implementation began.

**Why**: You're not just building software — you're building a **knowledge base that builds software**.

### Gap analysis feels bureaucratic

**Problem**: 4 dimensions feels like overhead.

**Solution**: The ritual takes 15-30 minutes. It prevents days or weeks of rework. Scale it: small phases need a quick scan; major phases need the full 4D protocol. Use `/gapanalysis` prompt for guided execution.

**Why**: Discovering missing knowledge mid-implementation forces context-switching and rework.

---

## Activation Patterns

| Trigger | Response |
|---------|----------|
| "new project" | Full research-first workflow |
| "gap analysis" / "GA" | 4-dimension gap analysis (GA-S, GA-I, GA-A, GA-P) |
| "GA-S" / "skill gap" | Skills dimension only |
| "GA-I" / "instruction gap" | Instructions dimension only |
| "GA-A" / "agent gap" | Agents dimension only |
| "GA-P" / "prompt gap" | Prompts dimension only |
| "research first" | Core methodology explanation |
| "two-agent pattern" | Builder + Validator agent setup |
| "synapse hygiene" | Connection best practices |
| "before coding" | Pre-implementation checklist |
| "knowledge encoding" | Research → Skill extraction workflow |

---

## Origin

Discovered by the Dead Letter heir (AI mystery game project, February 2026). The heir independently created 18 project-specific skills, 9 instructions, 2 agents, and 251 synapses **before writing any implementation code** — proving that research-first investment in the cognitive architecture produces dramatically higher-quality AI-assisted development.

The 4-dimension gap analysis (GA-S, GA-I, GA-A, GA-P) was developed by Master Alex to generalize the heir's methodology into a repeatable protocol for all projects and heirs.

The meta-insight: **You're not just building software — you're building a knowledge base that builds software.** The investment in research and skill creation pays compound dividends as the project grows.

---

## Synapses

- [.github/skills/bootstrap-learning/SKILL.md] (High, Extends, Forward) - "Research-first uses bootstrap learning for unknown domains"
- [.github/skills/project-scaffolding/SKILL.md] (High, Extends, Forward) - "Research-first adds knowledge layer to scaffolding"
- [.github/skills/skill-building/SKILL.md] (Critical, Requires, Bidirectional) - "Skills extracted from research use skill-building quality gates"
- [.github/skills/knowledge-synthesis/SKILL.md] (High, Integrates, Bidirectional) - "Research generates knowledge that synthesis organizes"
- [.github/instructions/skill-selection-optimization.instructions.md] (High, Feeds, Forward) - "Gap analysis creates skills that SSO selects from"
- [.github/instructions/research-first-workflow.instructions.md] (Critical, Implements, Bidirectional) - "Instruction provides step-by-step procedures for this skill"
- [.github/instructions/heir-skill-promotion.instructions.md] (High, Integrates, Forward) - "Heir projects use this methodology, then promote skills back"
- [.github/prompts/gapanalysis.prompt.md] (High, Implements, Forward) - "Interactive prompt for 4-dimension gap analysis"

*Skill created: 2026-02-13 | Category: Architecture | Status: Active*
*Origin: Heir promotion — Dead Letter project cognitive architecture expansion*
*Updated: 2026-02-13 — Added 4-dimension gap analysis (GA-S, GA-I, GA-A, GA-P), heir generalization, instruction + prompt*
