---
name: spec-generator
description: Specification generator - 6 phase document chain producing product brief, PRD, architecture, and epics. Triggers on "generate spec", "create specification", "spec generator", "workflow:spec".
allowed-tools: Agent, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, Read, Write, Edit, Bash, Glob, Grep, Skill
---

# Spec Generator

Structured specification document generator producing a complete specification package (Product Brief, PRD, Architecture, Epics) through 6 sequential phases with multi-CLI analysis and interactive refinement. **Document generation only** - execution handoff to existing workflows (lite-plan, plan, req-plan).

## Architecture Overview

```
Phase 0:   Specification Study (Read specs/ + templates/ - mandatory prerequisite)
           |
Phase 1:   Discovery               -> spec-config.json + discovery-context.json
           |                           (includes spec_type selection)
Phase 1.5: Req Expansion           -> refined-requirements.json (interactive discussion + CLI gap analysis)
           |                           (-y auto mode: auto-expansion, skip interaction)
Phase 2:   Product Brief            -> product-brief.md + glossary.json  (multi-CLI parallel analysis)
           |
Phase 3:   Requirements (PRD)      -> requirements/  (_index.md + REQ-*.md + NFR-*.md)
           |                           (RFC 2119 keywords, data model definitions)
Phase 4:   Architecture            -> architecture/  (_index.md + ADR-*.md, multi-CLI review)
           |                           (state machine, config model, error handling, observability)
Phase 5:   Epics & Stories         -> epics/  (_index.md + EPIC-*.md)
           |
Phase 6:   Readiness Check         -> readiness-report.md + spec-summary.md
           |                           (terminology + scope consistency validation)
           ├── Pass (>=80%): Handoff to execution workflows
           ├── Review (60-79%): Handoff with caveats
           └── Fail (<60%): Phase 6.5 Auto-Fix (max 2 iterations)
                 |
Phase 6.5: Auto-Fix               -> Updated Phase 2-5 documents
                 |
                 └── Re-run Phase 6 validation
```

## Key Design Principles

1. **Document Chain**: Each phase builds on previous outputs, creating a traceable specification chain from idea to executable stories
2. **Multi-Perspective Analysis**: CLI tools (Gemini/Codex/Claude) provide product, technical, and user perspectives in parallel
3. **Interactive by Default**: Each phase offers user confirmation points; `-y` flag enables full auto mode
4. **Resumable Sessions**: `spec-config.json` tracks completed phases; `-c` flag resumes from last checkpoint
5. **Template-Driven**: All documents generated from standardized templates with YAML frontmatter
6. **Pure Documentation**: No code generation or execution - clean handoff to existing execution workflows
7. **Spec Type Specialization**: Templates adapt to spec type (service/api/library/platform) via profiles for domain-specific depth
8. **Iterative Quality**: Phase 6.5 auto-fix loop repairs issues found in readiness check (max 2 iterations)
9. **Terminology Consistency**: glossary.json generated in Phase 2, injected into all subsequent phases

---

## Mandatory Prerequisites

> **Do NOT skip**: Before performing any operations, you **must** completely read the following documents. Proceeding without reading the specifications will result in outputs that do not meet quality standards.

### Specification Documents (Required Reading)

| Document | Purpose | Priority |
|----------|---------|----------|
| [specs/document-standards.md](specs/document-standards.md) | Document format, frontmatter, naming conventions | **P0 - Must read before execution** |
| [specs/quality-gates.md](specs/quality-gates.md) | Per-phase quality gate criteria and scoring | **P0 - Must read before execution** |

### Template Files (Must read before generation)

| Document | Purpose |
|----------|---------|
| [templates/product-brief.md](templates/product-brief.md) | Product brief document template |
| [templates/requirements-prd.md](templates/requirements-prd.md) | PRD document template |
| [templates/architecture-doc.md](templates/architecture-doc.md) | Architecture document template |
| [templates/epics-template.md](templates/epics-template.md) | Epic/Story document template |

---

## Execution Flow

```
Input Parsing:
   |- Parse $ARGUMENTS: extract idea/topic, flags (-y, -c, -m)
   |- Detect mode: new | continue
   |- If continue: read spec-config.json, resume from first incomplete phase
   |- If new: proceed to Phase 1

Phase 1: Discovery & Seed Analysis
   |- Ref: phases/01-discovery.md
   |- Generate session ID: SPEC-{slug}-{YYYY-MM-DD}
   |- Parse input (text or file reference)
   |- Gemini CLI seed analysis (problem, users, domain, dimensions)
   |- Codebase exploration (conditional, if project detected)
   |- Spec type selection: service|api|library|platform (interactive, -y defaults to service)
   |- User confirmation (interactive, -y skips)
   |- Output: spec-config.json, discovery-context.json (optional)

Phase 1.5: Requirement Expansion & Clarification
   |- Ref: phases/01-5-requirement-clarification.md
   |- CLI gap analysis: completeness scoring, missing dimensions detection
   |- Multi-round interactive discussion (max 5 rounds)
   |  |- Round 1: present gap analysis + expansion suggestions
   |  |- Round N: follow-up refinement based on user responses
   |- User final confirmation of requirements
   |- Auto mode (-y): CLI auto-expansion without interaction
   |- Output: refined-requirements.json

Phase 2: Product Brief
   |- Ref: phases/02-product-brief.md
   |- 3 parallel CLI analyses: Product (Gemini) + Technical (Codex) + User (Claude)
   |- Synthesize perspectives: convergent themes + conflicts
   |- Generate glossary.json (terminology from product brief + CLI analysis)
   |- Interactive refinement (-y skips)
   |- Output: product-brief.md (from template), glossary.json

Phase 3: Requirements / PRD
   |- Ref: phases/03-requirements.md
   |- Gemini CLI: expand goals into functional + non-functional requirements
   |- Generate acceptance criteria per requirement
   |- RFC 2119 behavioral constraints (MUST/SHOULD/MAY)
   |- Core entity data model definitions
   |- Glossary injection for terminology consistency
   |- User priority sorting: MoSCoW (interactive, -y auto-assigns)
   |- Output: requirements/ directory (_index.md + REQ-*.md + NFR-*.md, from template)

Phase 4: Architecture
   |- Ref: phases/04-architecture.md
   |- Gemini CLI: core components, tech stack, ADRs
   |- Codebase integration mapping (conditional)
   |- State machine generation (ASCII diagrams for lifecycle entities)
   |- Configuration model definition (fields, types, defaults, constraints)
   |- Error handling strategy (per-component classification + recovery)
   |- Observability specification (metrics, logs, health checks)
   |- Spec type profile injection (templates/profiles/{type}-profile.md)
   |- Glossary injection for terminology consistency
   |- Codex CLI: architecture challenge + review
   |- Interactive ADR decisions (-y auto-accepts)
   |- Output: architecture/ directory (_index.md + ADR-*.md, from template)

Phase 5: Epics & Stories
   |- Ref: phases/05-epics-stories.md
   |- Gemini CLI: requirement grouping into Epics, MVP subset tagging
   |- Story generation: As a...I want...So that...
   |- Dependency mapping (Mermaid)
   |- Interactive validation (-y skips)
   |- Output: epics/ directory (_index.md + EPIC-*.md, from template)

Phase 6: Readiness Check
   |- Ref: phases/06-readiness-check.md
   |- Cross-document validation (completeness, consistency, traceability)
   |- Quality scoring per dimension
   |- Terminology consistency validation (glossary compliance)
   |- Scope containment validation (PRD <= Brief scope)
   |- Output: readiness-report.md, spec-summary.md
   |- Handoff options: lite-plan, req-plan, plan, issue:new, export only, iterate

Phase 6.5: Auto-Fix (conditional, triggered when Phase 6 score < 60%)
   |- Ref: phases/06-5-auto-fix.md
   |- Parse readiness-report.md for Error/Warning items
   |- Group issues by originating Phase (2-5)
   |- Re-generate affected sections via CLI with error context
   |- Re-run Phase 6 validation
   |- Max 2 iterations, then force handoff
   |- Output: Updated Phase 2-5 documents

Complete: Full specification package ready for execution

Phase 6 → Handoff Bridge (conditional, based on user selection):
   ├─ lite-plan: Extract first MVP Epic description → direct text input
   ├─ plan / req-plan: Create WFS session + .brainstorming/ bridge files
   │   ├─ guidance-specification.md (synthesized from spec outputs)
   │   ├─ feature-specs/feature-index.json (Epic → Feature mapping)
   │   └─ feature-specs/F-{num}-{slug}.md (one per Epic)
   ├─ issue:new: Create issues per Epic
   └─ context-search-agent auto-discovers .brainstorming/
       → context-package.json.brainstorm_artifacts populated
       → action-planning-agent consumes: guidance_spec (P1) → feature_index (P2)
```

## Directory Setup

```javascript
// Session ID generation
const slug = topic.toLowerCase().replace(/[^a-z0-9\u4e00-\u9fff]+/g, '-').slice(0, 40);
const date = new Date().toISOString().slice(0, 10);
const sessionId = `SPEC-${slug}-${date}`;
const workDir = `.workflow/.spec/${sessionId}`;

Bash(`mkdir -p "${workDir}"`);
```

## Output Structure

```
.workflow/.spec/SPEC-{slug}-{YYYY-MM-DD}/
├── spec-config.json              # Session configuration + phase state
├── discovery-context.json        # Codebase exploration results (optional)
├── refined-requirements.json     # Phase 1.5: Confirmed requirements after discussion
├── glossary.json                 # Phase 2: Terminology glossary for cross-doc consistency
├── product-brief.md              # Phase 2: Product brief
├── requirements/                 # Phase 3: Detailed PRD (directory)
│   ├── _index.md                 #   Summary, MoSCoW table, traceability, links
│   ├── REQ-NNN-{slug}.md         #   Individual functional requirement
│   └── NFR-{type}-NNN-{slug}.md  #   Individual non-functional requirement
├── architecture/                 # Phase 4: Architecture decisions (directory)
│   ├── _index.md                 #   Overview, components, tech stack, links
│   └── ADR-NNN-{slug}.md         #   Individual Architecture Decision Record
├── epics/                        # Phase 5: Epic/Story breakdown (directory)
│   ├── _index.md                 #   Epic table, dependency map, MVP scope
│   └── EPIC-NNN-{slug}.md        #   Individual Epic with Stories
├── readiness-report.md           # Phase 6: Quality report
└── spec-summary.md               # Phase 6: One-page executive summary
```

## State Management

**spec-config.json** serves as core state file:
```json
{
  "session_id": "SPEC-xxx-2026-02-11",
  "seed_input": "User input text",
  "input_type": "text",
  "timestamp": "ISO8601",
  "mode": "interactive",
  "complexity": "moderate",
  "depth": "standard",
  "focus_areas": [],
  "spec_type": "service",
  "iteration_count": 0,
  "iteration_history": [],
  "seed_analysis": {
    "problem_statement": "...",
    "target_users": [],
    "domain": "...",
    "constraints": [],
    "dimensions": []
  },
  "has_codebase": false,
  "refined_requirements_file": "refined-requirements.json",
  "phasesCompleted": [
    { "phase": 1, "name": "discovery", "output_file": "spec-config.json", "completed_at": "ISO8601" },
    { "phase": 1.5, "name": "requirement-clarification", "output_file": "refined-requirements.json", "discussion_rounds": 2, "completed_at": "ISO8601" },
    { "phase": 3, "name": "requirements", "output_dir": "requirements/", "output_index": "requirements/_index.md", "file_count": 8, "completed_at": "ISO8601" }
  ]
}
```

**Resume mechanism**: `-c|--continue` flag reads `spec-config.json.phasesCompleted`, resumes from first incomplete phase.

## Core Rules

1. **Start Immediately**: First action is TaskCreate initialization, then Phase 0 (spec study), then Phase 1
2. **Progressive Phase Loading**: Read phase docs ONLY when that phase is about to execute
3. **Auto-Continue**: All phases run autonomously; check TaskList to execute next pending phase
4. **Parse Every Output**: Extract required data from each phase for next phase context
5. **DO NOT STOP**: Continuous 6-phase pipeline until all phases complete or user exits
6. **Respect -y Flag**: When auto mode, skip all AskUserQuestion calls, use recommended defaults
7. **Respect -c Flag**: When continue mode, load spec-config.json and resume from checkpoint
8. **Inject Glossary**: From Phase 3 onward, inject glossary.json terms into every CLI prompt
9. **Load Profile**: Read templates/profiles/{spec_type}-profile.md and inject requirements into Phase 2-5 prompts
10. **Iterate on Failure**: When Phase 6 score < 60%, auto-trigger Phase 6.5 (max 2 iterations)

## Reference Documents by Phase

### Phase 1: Discovery
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/01-discovery.md](phases/01-discovery.md) | Seed analysis and session setup | Phase start |
| [templates/profiles/](templates/profiles/) | Spec type profiles | Spec type selection |
| [specs/document-standards.md](specs/document-standards.md) | Frontmatter format for spec-config.json | Config generation |

### Phase 1.5: Requirement Expansion & Clarification
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/01-5-requirement-clarification.md](phases/01-5-requirement-clarification.md) | Interactive requirement discussion workflow | Phase start |
| [specs/quality-gates.md](specs/quality-gates.md) | Quality criteria for refined requirements | Validation |

### Phase 2: Product Brief
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/02-product-brief.md](phases/02-product-brief.md) | Multi-CLI analysis orchestration | Phase start |
| [templates/product-brief.md](templates/product-brief.md) | Document template | Document generation |
| [specs/glossary-template.json](specs/glossary-template.json) | Glossary schema | Glossary generation |

### Phase 3: Requirements
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/03-requirements.md](phases/03-requirements.md) | PRD generation workflow | Phase start |
| [templates/requirements-prd.md](templates/requirements-prd.md) | Document template | Document generation |

### Phase 4: Architecture
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/04-architecture.md](phases/04-architecture.md) | Architecture decision workflow | Phase start |
| [templates/architecture-doc.md](templates/architecture-doc.md) | Document template | Document generation |

### Phase 5: Epics & Stories
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/05-epics-stories.md](phases/05-epics-stories.md) | Epic/Story decomposition | Phase start |
| [templates/epics-template.md](templates/epics-template.md) | Document template | Document generation |

### Phase 6: Readiness Check
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/06-readiness-check.md](phases/06-readiness-check.md) | Cross-document validation | Phase start |
| [specs/quality-gates.md](specs/quality-gates.md) | Quality scoring criteria | Validation |

### Phase 6.5: Auto-Fix
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/06-5-auto-fix.md](phases/06-5-auto-fix.md) | Auto-fix workflow for readiness issues | When Phase 6 score < 60% |
| [specs/quality-gates.md](specs/quality-gates.md) | Iteration exit criteria | Validation |

### Debugging & Troubleshooting
| Issue | Solution Document |
|-------|-------------------|
| Phase execution failed | Refer to the relevant Phase documentation |
| Output does not meet expectations | [specs/quality-gates.md](specs/quality-gates.md) |
| Document format issues | [specs/document-standards.md](specs/document-standards.md) |

## Error Handling

| Phase | Error | Blocking? | Action |
|-------|-------|-----------|--------|
| Phase 1 | Empty input | Yes | Error and exit |
| Phase 1 | CLI seed analysis fails | No | Use basic parsing fallback |
| Phase 1.5 | Gap analysis CLI fails | No | Skip to user questions with basic prompts |
| Phase 1.5 | User skips discussion | No | Proceed with seed_analysis as-is |
| Phase 1.5 | Max rounds reached (5) | No | Force confirmation with current state |
| Phase 2 | Single CLI perspective fails | No | Continue with available perspectives |
| Phase 2 | All CLI calls fail | No | Generate basic brief from seed analysis |
| Phase 3 | Gemini CLI fails | No | Use codex fallback |
| Phase 4 | Architecture review fails | No | Skip review, proceed with initial analysis |
| Phase 5 | Story generation fails | No | Generate epics without detailed stories |
| Phase 6 | Validation CLI fails | No | Generate partial report with available data |
| Phase 6.5 | Auto-fix CLI fails | No | Log failure, proceed to handoff with Review status |
| Phase 6.5 | Max iterations reached | No | Force handoff, report remaining issues |

### CLI Fallback Chain

Gemini -> Codex -> Claude -> degraded mode (local analysis only)
