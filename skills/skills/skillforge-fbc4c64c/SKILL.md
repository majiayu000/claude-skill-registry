---
name: skillforge
description: "Intelligent skill router and creator. Analyzes ANY input to recommend existing skills, improve them, or create new ones. Uses deep iterative analysis with 11 thinking models, regression questioning, evolution lens, and multi-agent synthesis panel. Phase 0 triage ensures you never duplicate existing functionality."
license: MIT
metadata:
  version: 4.0.0
  model: claude-opus-4-5-20251101
  subagent_model: claude-opus-4-5-20251101
  domains: [meta-skill, automation, skill-creation, orchestration, agentic, routing]
  type: orchestrator
  inputs: [any-input, user-goal, domain-hints]
  outputs: [SKILL.md, references/, scripts/, SKILL_SPEC.md, recommendations]
---

# SkillForge 4.0 - Intelligent Skill Router & Creator

Analyzes ANY input to find, improve, or create the right skill.

---

## Quick Start

**Any input works.** SkillForge will intelligently route to the right action:

```
# These all work - SkillForge figures out what you need:

SkillForge: create a skill for automated code review
→ Creates new skill (after checking no duplicates exist)

help me debug this TypeError
→ Recommends ErrorExplainer skill (existing)

improve the testgen skill to handle React components better
→ Enters improvement mode for TestGen

do I have a skill for database migrations?
→ Recommends DBSchema, database-migration skills

TypeError: Cannot read property 'map' of undefined
→ Routes to debugging skills (error detected)
```

---

## Triggers

### Creation Triggers
- `SkillForge: {goal}` - Full autonomous skill creation
- `create skill` - Natural language activation
- `design skill for {purpose}` - Purpose-first creation
- `ultimate skill` - Emphasize maximum quality
- `skillforge --plan-only` - Generate specification without execution

### Routing Triggers (NEW in v4.0)
- `{any input}` - Analyzes and routes automatically
- `do I have a skill for` - Searches existing skills
- `which skill` / `what skill` - Recommends matching skills
- `improve {skill-name} skill` - Enters improvement mode
- `help me with` / `I need to` - Detects task and routes

| Input | Output | Quality Gate |
|-------|--------|--------------|
| Any input | Triage → Route → Action | Phase 0 analysis |
| Explicit create | New skill | Unanimous panel approval |
| Task/question | Skill recommendation | Match confidence ≥60% |

---

## Process Overview

```
ANY USER INPUT
(prompt, error, code, URL, question, task request)
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ Phase 0: SKILL TRIAGE (NEW)                         │
│ • Classify input type (create/improve/question/task)│
│ • Scan 250+ skills in ecosystem                     │
│ • Match against existing skills with confidence %   │
│ • Route to: USE | IMPROVE | CREATE | COMPOSE        │
├─────────────────────────────────────────────────────┤
│         ↓ USE_EXISTING    ↓ IMPROVE      ↓ CREATE   │
│      [Recommend]      [Load & Enhance] [Continue]   │
└─────────────────────────────────────────────────────┘
    │ (if CREATE_NEW or IMPROVE_EXISTING)
    ▼
┌─────────────────────────────────────────────────────┐
│ Phase 1: DEEP ANALYSIS                              │
│ • Expand requirements (explicit, implicit, unknown) │
│ • Apply 11 thinking models + Automation Lens        │
│ • Question until no new insights (3 empty rounds)   │
│ • Identify automation/script opportunities          │
├─────────────────────────────────────────────────────┤
│ Phase 2: SPECIFICATION                              │
│ • Generate XML spec with all decisions + WHY        │
│ • Include scripts section (if applicable)           │
│ • Validate timelessness score ≥ 7                   │
├─────────────────────────────────────────────────────┤
│ Phase 3: GENERATION                                 │
│ • Write SKILL.md with fresh context                 │
│ • Generate references/, assets/, and scripts/       │
├─────────────────────────────────────────────────────┤
│ Phase 4: SYNTHESIS PANEL                            │
│ • 3-4 Opus agents review independently              │
│ • Script Agent added when scripts present           │
│ • All agents must approve (unanimous)               │
│ • If rejected → loop back with feedback             │
└─────────────────────────────────────────────────────┘
    │
    ▼
Production-Ready Agentic Skill
```

**Key principles:**
- **Phase 0 prevents duplicates** - Always checks existing skills first
- Evolution/timelessness is the core lens (score ≥ 7 required)
- Every decision includes WHY
- Zero tolerance for errors
- Autonomous execution at maximum depth
- Scripts enable self-verification and agentic operation

---

## Commands

| Command | Action |
|---------|--------|
| `SkillForge: {goal}` | Full autonomous execution |
| `SkillForge --plan-only {goal}` | Generate specification only |
| `SkillForge --quick {goal}` | Reduced depth (not recommended) |
| `SkillForge --triage {input}` | Run Phase 0 triage only |
| `SkillForge --improve {skill}` | Enter improvement mode for existing skill |

---

## Phase 0: Skill Triage (NEW in v4.0)

Before creating anything, SkillForge intelligently analyzes your input to determine the best action.

### How It Works

```
┌────────────────────────────────────────────────────────────────────┐
│                        ANY USER INPUT                               │
│  (prompt, error, code, URL, question, task request, anything)      │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│  Step 1: INPUT CLASSIFICATION                                       │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐       │
│  │ explicit_create │ │ explicit_improve│ │ skill_question  │       │
│  │ "create skill"  │ │ "improve skill" │ │ "do I have..."  │       │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘       │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐       │
│  │  task_request   │ │  error_message  │ │  code_snippet   │       │
│  │ "help me with"  │ │ "TypeError..."  │ │ [pasted code]   │       │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘       │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│  Step 2: SKILL ECOSYSTEM SCAN                                       │
│  • Load index of 250+ skills (discover_skills.py)                  │
│  • Match input against all skills with confidence scoring          │
│  • Identify top matches with reasons                               │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│  Step 3: DECISION MATRIX                                            │
│                                                                     │
│  Match ≥80%  + explicit create → CLARIFY (duplicate warning)       │
│  Match ≥80%  + other input     → USE_EXISTING (recommend skill)    │
│  Match 50-79%                  → IMPROVE_EXISTING (enhance match)  │
│  Match <50%  + explicit create → CREATE_NEW (proceed to Phase 1)   │
│  Multi-domain detected         → COMPOSE (suggest skill chain)     │
│  Ambiguous input               → CLARIFY (ask for more info)       │
└────────────────────────────────────────────────────────────────────┘
```

### Decision Actions

| Action | When | Result |
|--------|------|--------|
| **USE_EXISTING** | Match ≥80% | Recommends existing skill(s) to invoke |
| **IMPROVE_EXISTING** | Match 50-79% | Loads skill and enters enhancement mode |
| **CREATE_NEW** | Match <50% | Proceeds to Phase 1 (Deep Analysis) |
| **COMPOSE** | Multi-domain | Suggests skill chain via SkillComposer |
| **CLARIFY** | Ambiguous or duplicate | Asks user to clarify intent |

### Triage Script

```bash
# Run triage on any input
python scripts/triage_skill_request.py "help me debug this error"

# JSON output for automation
python scripts/triage_skill_request.py "create a skill for payments" --json

# Examples:
python scripts/triage_skill_request.py "TypeError: Cannot read property 'map'"
# → USE_EXISTING: Recommends ErrorExplainer (92%)

python scripts/triage_skill_request.py "create a skill for code review"
# → CLARIFY: CodeReview skill exists (85%), create anyway?

python scripts/triage_skill_request.py "help me with API and auth and testing"
# → COMPOSE: Multi-domain, suggests APIDesign + AuthSystem + TestGen chain
```

### Ecosystem Index

Phase 0 uses a pre-built index of all skills:

```bash
# Rebuild skill index (run periodically or after installing new skills)
python scripts/discover_skills.py

# Index location: ~/.cache/skillrecommender/skill_index.json
# Scans: ~/.claude/skills/, plugins/marketplaces/*, plugins/cache/*
```

### Integration with Phases 1-4

- **USE_EXISTING**: Exits early, no creation needed
- **IMPROVE_EXISTING**: Loads existing skill → Phase 1 analyzes gaps → Phase 2-4 enhance
- **CREATE_NEW**: Full pipeline (Phase 1 → 2 → 3 → 4)
- **COMPOSE**: Suggests using SkillComposer instead
- **CLARIFY**: Pauses for user input before proceeding

---

## Validation & Packaging

Before distribution, validate your skill:

```bash
# Quick validation (required for packaging)
python scripts/quick_validate.py ~/.claude/skills/my-skill/

# Full structural validation
python scripts/validate-skill.py ~/.claude/skills/my-skill/

# Package for distribution
python scripts/package_skill.py ~/.claude/skills/my-skill/ ./dist
```

### Frontmatter Requirements

Skills must use only these allowed frontmatter properties:

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Hyphen-case, max 64 chars |
| `description` | Yes | Max 1024 chars, no angle brackets |
| `license` | No | MIT, Apache-2.0, etc. |
| `allowed-tools` | No | Restrict tool access |
| `metadata` | No | Custom fields (version, model, etc.) |

```yaml
---
name: my-skill
description: What this skill does
license: MIT
metadata:
  version: 1.0.0
  model: claude-opus-4-5-20251101
---
```

---

## Skill Output Structure

```
~/.claude/skills/{skill-name}/
├── SKILL.md                    # Main entry point (required)
├── references/                 # Deep documentation (optional)
│   ├── patterns.md
│   └── examples.md
├── assets/                     # Templates (optional)
│   └── templates/
└── scripts/                    # Automation scripts (optional)
    ├── validate.py             # Validation/verification
    ├── generate.py             # Artifact generation
    └── state.py                # State management
```

### Scripts Directory

Scripts enable skills to be **agentic** - capable of autonomous operation with self-verification.

| Category | Purpose | When to Include |
|----------|---------|-----------------|
| **Validation** | Verify outputs meet standards | Skill produces artifacts |
| **Generation** | Create artifacts from templates | Repeatable artifact creation |
| **State Management** | Track progress across sessions | Long-running operations |
| **Transformation** | Convert/process data | Data processing tasks |
| **Calculation** | Compute metrics/scores | Scoring or analysis |

**Script Requirements:**
- Python 3.x with standard library only (graceful fallbacks for extras)
- `Result` dataclass pattern for structured returns
- Exit codes: 0=success, 1=failure, 10=validation failure, 11=verification failure
- Self-verification where applicable
- Documented in SKILL.md with usage examples

See: [references/script-integration-framework.md](references/script-integration-framework.md)

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Duplicate skills | Bloats registry | Check existing first |
| Single trigger | Hard to discover | 3-5 varied phrases |
| No verification | Can't confirm success | Measurable outcomes |
| Over-engineering | Complexity without value | Start simple |
| Missing WHY | Can't evolve | Document rationale |
| Invalid frontmatter | Can't package | Use allowed properties only |

---

## Verification Checklist

After creation:

- [ ] Frontmatter valid (only allowed properties)
- [ ] Name is hyphen-case, ≤64 chars
- [ ] Description ≤1024 chars, no `<` or `>`
- [ ] 3-5 trigger phrases defined
- [ ] Timelessness score ≥ 7
- [ ] `python scripts/quick_validate.py` passes

---

<details>
<summary><strong>Deep Dive: Phase 1 - Analysis</strong></summary>

### 1A: Input Expansion

Transform user's goal into comprehensive requirements:

```
USER INPUT: "Create a skill for X"
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│ EXPLICIT REQUIREMENTS                                    │
│ • What the user literally asked for                      │
│ • Direct functionality stated                            │
├─────────────────────────────────────────────────────────┤
│ IMPLICIT REQUIREMENTS                                    │
│ • What they probably expect but didn't say               │
│ • Standard quality expectations                          │
│ • Integration with existing patterns                     │
├─────────────────────────────────────────────────────────┤
│ UNKNOWN UNKNOWNS                                         │
│ • What they don't know they need                         │
│ • Expert-level considerations they'd miss                │
│ • Future needs they haven't anticipated                  │
├─────────────────────────────────────────────────────────┤
│ DOMAIN CONTEXT                                           │
│ • Related skills that exist                              │
│ • Patterns from similar skills                           │
│ • Lessons from skill failures                            │
└─────────────────────────────────────────────────────────┘
```

**Check for overlap with existing skills:**
```bash
ls ~/.claude/skills/
# Grep for similar triggers in existing SKILL.md files
```

| Match Score | Action |
|-------------|--------|
| >7/10 | Use existing skill instead |
| 5-7/10 | Clarify distinction before proceeding |
| <5/10 | Proceed with new skill |

### 1B: Multi-Lens Analysis

Apply all 11 thinking models systematically:

| Lens | Core Question | Application |
|------|---------------|-------------|
| **First Principles** | What's fundamentally needed? | Strip convention, find core |
| **Inversion** | What guarantees failure? | Build anti-patterns |
| **Second-Order** | What happens after the obvious? | Map downstream effects |
| **Pre-Mortem** | Why did this fail? | Proactive risk mitigation |
| **Systems Thinking** | How do parts interact? | Integration mapping |
| **Devil's Advocate** | Strongest counter-argument? | Challenge every decision |
| **Constraints** | What's truly fixed? | Separate real from assumed |
| **Pareto** | Which 20% delivers 80%? | Focus on high-value features |
| **Root Cause** | Why is this needed? (5 Whys) | Address cause not symptom |
| **Comparative** | How do options compare? | Weighted decision matrix |
| **Opportunity Cost** | What are we giving up? | Explicit trade-offs |

**Minimum requirement:** All 11 lenses scanned, at least 5 applied in depth.

See: [references/multi-lens-framework.md](references/multi-lens-framework.md)

### 1C: Regression Questioning

Iterative self-questioning until no new insights emerge:

```
ROUND N:
│
├── "What am I missing?"
├── "What would an expert in {domain} add?"
├── "What would make this fail?"
├── "What will this look like in 2 years?"
├── "What's the weakest part of this design?"
└── "Which thinking model haven't I applied?"
    │
    └── New insights > 0?
        │
        ├── YES → Incorporate and loop
        └── NO → Check termination criteria
```

**Termination Criteria:**
- Three consecutive rounds produce no new insights
- All 11 thinking models have been applied
- At least 3 simulated expert perspectives considered
- Evolution/timelessness explicitly evaluated
- Automation opportunities identified

See: [references/regression-questions.md](references/regression-questions.md)

### 1D: Automation Analysis

Identify opportunities for scripts that enable agentic operation:

```
FOR EACH operation in the skill:
│
├── Is this operation repeatable?
│   └── YES → Consider generation script
│
├── Does this produce verifiable output?
│   └── YES → Consider validation script
│
├── Does this need state across sessions?
│   └── YES → Consider state management script
│
├── Does this involve external tools?
│   └── YES → Consider integration script
│
└── Can Claude verify success autonomously?
    └── NO → Add self-verification script
```

**Automation Lens Questions:**

| Question | Script Category if YES |
|----------|----------------------|
| What operations will be repeated identically? | Generation |
| What outputs require validation? | Validation |
| What state needs to persist? | State Management |
| Can the skill run overnight autonomously? | All categories |
| How will Claude verify correct execution? | Verification |

**Decision: Script vs No Script**

| Create Script When | Skip Script When |
|-------------------|------------------|
| Operation is deterministic | Requires human judgment |
| Output can be validated | One-time setup |
| Will be reused across invocations | Simple text output |
| Enables autonomous operation | No verification needed |
| External tool integration | Pure Claude reasoning |

See: [references/script-integration-framework.md](references/script-integration-framework.md)

</details>

<details>
<summary><strong>Deep Dive: Phase 2 - Specification</strong></summary>

### Specification Structure

The specification captures all analysis insights in XML format:

```xml
<skill_specification>
  <metadata>
    <name>skill-name</name>
    <analysis_iterations>N</analysis_iterations>
    <timelessness_score>X/10</timelessness_score>
  </metadata>

  <context>
    <problem_statement>What + Why + Who</problem_statement>
    <existing_landscape>Related skills, distinctiveness</existing_landscape>
  </context>

  <requirements>
    <explicit>What user asked for</explicit>
    <implicit>Expected but unstated</implicit>
    <discovered>Found through analysis</discovered>
  </requirements>

  <architecture>
    <pattern>Selected pattern with WHY</pattern>
    <phases>Ordered phases with verification</phases>
    <decision_points>Branches and defaults</decision_points>
  </architecture>

  <scripts>
    <decision_summary>needs_scripts + rationale</decision_summary>
    <script_inventory>name, category, purpose, patterns</script_inventory>
    <agentic_capabilities>autonomous, self-verify, recovery</agentic_capabilities>
  </scripts>

  <evolution_analysis>
    <timelessness_score>X/10</timelessness_score>
    <extension_points>Where skill can grow</extension_points>
    <obsolescence_triggers>What would break it</obsolescence_triggers>
  </evolution_analysis>

  <anti_patterns>
    <pattern>What to avoid + WHY + alternative</pattern>
  </anti_patterns>

  <success_criteria>
    <criterion>Measurable + verification method</criterion>
  </success_criteria>
</skill_specification>
```

See: [references/specification-template.md](references/specification-template.md)

### Specification Validation

Before proceeding to Phase 3:

- [ ] All sections present with no placeholders
- [ ] Every decision includes WHY
- [ ] Timelessness score ≥ 7 with justification
- [ ] At least 2 extension points documented
- [ ] All requirements traceable to source
- [ ] Scripts section complete (if applicable)
- [ ] Agentic capabilities documented (if scripts present)

</details>

<details>
<summary><strong>Deep Dive: Phase 3 - Generation</strong></summary>

**Context:** Fresh, clean (no analysis artifacts polluting)
**Standard:** Zero errors—every section verified before proceeding

### Generation Order

```
1. Create directory structure
   mkdir -p ~/.claude/skills/{skill-name}/references
   mkdir -p ~/.claude/skills/{skill-name}/assets/templates
   mkdir -p ~/.claude/skills/{skill-name}/scripts  # if scripts needed

2. Write SKILL.md
   • Frontmatter (YAML - allowed properties only)
   • Title and brief intro
   • Quick Start section
   • Triggers (3-5 varied phrases)
   • Quick Reference table
   • How It Works overview
   • Commands
   • Scripts section (if applicable)
   • Validation section
   • Anti-Patterns
   • Verification criteria
   • Deep Dive sections (in <details> tags)

3. Generate reference documents (if needed)
   • Deep documentation for complex topics
   • Templates for generated artifacts
   • Checklists for validation

4. Create assets (if needed)
   • Templates for skill outputs

5. Create scripts (if needed)
   • Use script-template.py as base
   • Include Result dataclass pattern
   • Add self-verification
   • Document exit codes
   • Test before finalizing
```

### Quality Checks During Generation

| Check | Requirement |
|-------|-------------|
| Frontmatter | Only allowed properties (name, description, license, allowed-tools, metadata) |
| Name | Hyphen-case, ≤64 chars |
| Description | ≤1024 chars, no angle brackets |
| Triggers | 3-5 distinct, natural language |
| Phases | 1-3 max, not over-engineered |
| Verification | Concrete, measurable |
| Tables over prose | Structured information in tables |
| No placeholder text | Every section fully written |
| Scripts (if present) | Shebang, docstring, argparse, exit codes, Result pattern |
| Script docs | Scripts section in SKILL.md with usage examples |

</details>

<details>
<summary><strong>Deep Dive: Phase 4 - Multi-Agent Synthesis</strong></summary>

**Panel:** 3-4 Opus agents with distinct evaluative lenses
**Requirement:** Unanimous approval (all agents)
**Fallback:** Return to Phase 1 with feedback (max 5 iterations)

### Panel Composition

| Agent | Focus | Key Criteria | When Active |
|-------|-------|--------------|-------------|
| **Design/Architecture** | Structure, patterns, correctness | Pattern appropriate, phases logical, no circular deps | Always |
| **Audience/Usability** | Clarity, discoverability, completeness | Triggers natural, steps unambiguous, no assumed knowledge | Always |
| **Evolution/Timelessness** | Future-proofing, extension, ecosystem | Score ≥7, extension points clear, ecosystem fit | Always |
| **Script/Automation** | Agentic capability, verification, quality | Scripts follow patterns, self-verify, documented | When scripts present |

### Script Agent (Conditional)

The Script Agent is activated when the skill includes a `scripts/` directory. Focus areas:

| Criterion | Checks |
|-----------|--------|
| **Pattern Compliance** | Result dataclass, argparse, exit codes |
| **Self-Verification** | Scripts can verify their own output |
| **Error Handling** | Graceful failures, actionable messages |
| **Documentation** | Usage examples in SKILL.md |
| **Agentic Capability** | Can run autonomously without human intervention |

**Script Agent Scoring:**

| Score | Meaning |
|-------|---------|
| 8-10 | Fully agentic, self-verifying, production-ready |
| 6-7 | Functional but missing some agentic capabilities |
| <6 | Requires revision - insufficient automation quality |

### Agent Evaluation

Each agent produces:

```markdown
## [Agent] Review

### Verdict: APPROVED / CHANGES_REQUIRED

### Scores
| Criterion | Score (1-10) | Notes |
|-----------|--------------|-------|

### Strengths
1. [Specific with evidence]

### Issues (if CHANGES_REQUIRED)
| Issue | Severity | Required Change |
|-------|----------|-----------------|

### Recommendations
1. [Even if approved]
```

### Consensus Protocol

```
IF all agents APPROVED (3/3 or 4/4):
    → Finalize skill
    → Run validate-skill.py
    → Update registry
    → Complete

ELSE:
    → Collect all issues (including script issues)
    → Return to Phase 1 with issues as input
    → Re-apply targeted questioning
    → Regenerate skill and scripts
    → Re-submit to panel

IF 5 iterations without consensus:
    → Flag for human review
    → Present all agent perspectives
    → User makes final decision
```

See: [references/synthesis-protocol.md](references/synthesis-protocol.md)

</details>

<details>
<summary><strong>Deep Dive: Evolution/Timelessness</strong></summary>

Every skill is evaluated through the evolution lens:

### Temporal Projection

| Timeframe | Key Question |
|-----------|--------------|
| 6 months | How will usage patterns evolve? |
| 1 year | What ecosystem changes are likely? |
| 2 years | What new capabilities might obsolete this? |
| 5 years | Is the core problem still relevant? |

### Timelessness Scoring

| Score | Description | Verdict |
|-------|-------------|---------|
| 1-3 | Transient, will be obsolete in months | Reject |
| 4-6 | Moderate, depends on current tooling | Revise |
| **7-8** | **Solid, principle-based, extensible** | **Approve** |
| 9-10 | Timeless, addresses fundamental problem | Exemplary |

**Requirement:** All skills must score ≥7.

### Anti-Obsolescence Patterns

| Do | Don't |
|----|-------|
| Design around principles | Hardcode implementations |
| Document the WHY | Only document the WHAT |
| Include extension points | Create closed systems |
| Abstract volatile dependencies | Direct coupling |
| Version-agnostic patterns | Pin specific versions |

See: [references/evolution-scoring.md](references/evolution-scoring.md)

</details>

<details>
<summary><strong>Architecture Pattern Selection</strong></summary>

Select based on task complexity:

| Pattern | Use When | Structure |
|---------|----------|-----------|
| **Single-Phase** | Simple linear tasks | Steps 1-2-3 |
| **Checklist** | Quality/compliance audits | ☐ Item verification |
| **Generator** | Creating artifacts | Input → Transform → Output |
| **Multi-Phase** | Complex ordered workflows | Phase 1 → Phase 2 → Phase 3 |
| **Multi-Agent Parallel** | Independent subtasks | Launch agents concurrently |
| **Multi-Agent Sequential** | Dependent subtasks | Agent 1 → Agent 2 → Agent 3 |
| **Orchestrator** | Coordinating multiple skills | Meta-skill chains |

### Selection Decision Tree

```
Is it a simple procedure?
├── Yes → Single-Phase
└── No → Does it produce artifacts?
    ├── Yes → Generator
    └── No → Does it verify/audit?
        ├── Yes → Checklist
        └── No → Are subtasks independent?
            ├── Yes → Multi-Agent Parallel
            └── No → Multi-Agent Sequential or Multi-Phase
```

</details>

<details>
<summary><strong>Configuration</strong></summary>

```yaml
SKILLCREATOR_CONFIG:
  mode: autonomous
  depth: maximum  # always
  core_lens: evolution_timelessness

  analysis:
    min_lens_depth: 5
    max_questioning_rounds: 7
    termination_empty_rounds: 3

  synthesis:
    panel_size: 3
    require_unanimous: true
    max_iterations: 5
    escalate_to_human: true

  evolution:
    min_timelessness_score: 7
    min_extension_points: 2
    require_temporal_projection: true

  model:
    primary: claude-opus-4-5-20251101
    subagents: claude-opus-4-5-20251101
```

</details>

---

## References

- [Regression Questions](references/regression-questions.md) - Complete question bank (7 categories)
- [Multi-Lens Framework](references/multi-lens-framework.md) - 11 thinking models guide
- [Specification Template](references/specification-template.md) - XML spec structure
- [Evolution Scoring](references/evolution-scoring.md) - Timelessness evaluation
- [Synthesis Protocol](references/synthesis-protocol.md) - Multi-agent panel details
- [Script Integration Framework](references/script-integration-framework.md) - When and how to create scripts
- [Script Patterns Catalog](references/script-patterns-catalog.md) - Standard Python patterns

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| skill-composer | Can orchestrate created skills |
| claude-authoring-guide | Deeper patterns reference |
| codereview | Pattern for multi-agent panels |
| maker-framework | Zero error standard source |

---

## Extension Points

1. **Additional Lenses:** Add new thinking models to `references/multi-lens-framework.md`
2. **New Synthesis Agents:** Extend panel beyond 4 agents for specific domains
3. **Custom Patterns:** Add architecture patterns to selection guide
4. **Domain Templates:** Add domain-specific templates to `assets/templates/`
5. **Script Patterns:** Add new patterns to `references/script-patterns-catalog.md`
6. **Script Categories:** Extend the 7 script categories for new use cases

---

## Changelog

### v3.2.0 (Current)
- Added Script Integration Framework for agentic skills
- Added 4th Script Agent to synthesis panel (conditional)
- Added Phase 1D: Automation Analysis
- Added Automation Lens questions to regression questioning
- Created `references/script-integration-framework.md`
- Created `references/script-patterns-catalog.md`
- Created `assets/templates/script-template.py`
- Updated skill-spec-template.xml with `<scripts>` section
- Updated validate-skill.py with script validation
- Skills can now include self-verifying Python scripts

### v3.1.0
- Added progressive disclosure structure
- Fixed frontmatter for packaging compatibility
- Added validation & packaging section
- Deep dive sections now collapsible

### v3.0.0
- Complete redesign as ultimate meta-skill
- Added regression questioning loop
- Added multi-lens analysis framework (11 models)
- Added evolution/timelessness core lens
- Added multi-agent synthesis panel

### v2.0.0
- Pattern selection guide
- Quality standards checklist

### v1.0.0
- Basic skill structure
