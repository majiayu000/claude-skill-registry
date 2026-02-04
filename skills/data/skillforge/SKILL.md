---
name: skillforge
version: 4.0.0
description: Intelligent skill router and creator. Analyzes ANY input to recommend
  existing skills, improve them, or create new ones. Uses deep iterative analysis
  with 11 thinking models, regression questioning, evolution lens, and multi-agent
  synthesis panel. Phase 0 triage ensures you never duplicate existing functionality.
license: MIT
model: claude-opus-4-5
metadata:
  subagent_model: claude-opus-4-5
  domains:
  - meta-skill
  - automation
  - skill-creation
  - orchestration
  - agentic
  - routing
  type: orchestrator
  inputs:
  - any-input
  - user-goal
  - domain-hints
  outputs:
  - SKILL.md
  - references/
  - scripts/
  - SKILL_SPEC.md
  - recommendations
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

## Deep Dives

For detailed implementation guides, see:

- [Phase 1: Analysis](references/phase1-analysis-deep-dive.md) - Input expansion, multi-lens analysis, regression questioning, automation analysis
- [Phase 2: Specification](references/phase2-specification-deep-dive.md) - Specification structure and validation
- [Phase 3: Generation](references/phase3-generation-deep-dive.md) - Generation order and quality checks
- [Phase 4: Multi-Agent Synthesis](references/phase4-synthesis-deep-dive.md) - Panel composition, evaluation, consensus protocol
- [Evolution/Timelessness](references/evolution-timelessness.md) - Temporal projection, timelessness scoring, anti-obsolescence patterns
- [Architecture Patterns](references/architecture-patterns.md) - Pattern selection decision tree
- [Configuration](references/configuration.md) - SkillForge configuration settings

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
