# Phase 2: Project Discovery Skill

## Metadata
- skill_name: phase2-discovery
- activation_code: PHASE2_DISCOVERY_V1
- alternate_code: PHASE2_DISCOVERY_ENHANCE_V1
- version: 2.0.0
- category: discovery
- phase: 2

## Description

Interactive project discovery orchestrator. Guides users through artifact collection, scope definition, and PRD generation through a conversational eleven-stage process.

**New in v2.0:** Pre-Discovery Gate with artifact detection, Enhance Mode for existing PRDs, and .context/ integration for modular development.

## Activation Criteria

- User says "begin project discovery", "start discovery", or "discover"
- User opens a project with `.discovery/discovery-state.json` showing incomplete status
- User says "resume discovery"
- Before any Phase 3+ work when no PRD exists

---

## Pre-Discovery Gate (NEW - ALWAYS RUNS FIRST)

**Before starting any discovery flow, the system MUST run artifact detection and present a human confirmation gate.**

### Step 1: Artifact Detection

Scan for existing artifacts:

```javascript
const detection = {
  existing_prd: {
    found: exists("docs/PRD.md"),
    path: "docs/PRD.md",
    lines: countLines("docs/PRD.md"),
    last_modified: getModTime("docs/PRD.md"),
    sections_present: analyzePRDSections("docs/PRD.md"),
    completeness: sections_present.length / 19
  },
  context_artifacts: {
    manifest_found: exists(".context/context-manifest.json"),
    mandatory_present: [],
    mandatory_missing: [],
    architecture_diagram: exists(".context/mandatory/architecture.dot") ||
                          exists(".context/mandatory/architecture.mmd")
  },
  phase_overrides: {
    found: exists(".claude/phase-overrides.json"),
    externally_completed: parseOverrides(".claude/phase-overrides.json")
  },
  discovery_state: {
    found: exists(".discovery/discovery-state.json"),
    status: parseState(".discovery/discovery-state.json").status,
    current_stage: parseState(".discovery/discovery-state.json").current_stage
  }
};
```

### Step 2: Validate Context Manifest

If `.context/context-manifest.json` exists:

1. Parse against schema at `templates/context-manifest.schema.json`
2. Check each file in `mandatory` section:
   - architecture_diagram: Check for .dot, .gv, .mmd files
   - parent_prd: Check if file exists
   - api_contracts: Check if file exists
3. Record what's present vs. missing

### Step 3: Display Confirmation Gate

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                PRE-DISCOVERY GATE: Artifact Detection                      ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  I detected existing project artifacts:                                    ║
║                                                                            ║
║  ┌──────────────────────────────────────────────────────────────────────┐ ║
║  │ EXISTING PRD                                                          │ ║
║  ├──────────────────────────────────────────────────────────────────────┤ ║
║  │   📄 docs/PRD.md ({lines} lines, modified {date})                    │ ║
║  │   Sections complete: {count}/19                                       │ ║
║  │   Missing: {list of missing sections}                                 │ ║
║  │   Completeness: {percentage}%                                         │ ║
║  └──────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
║  ┌──────────────────────────────────────────────────────────────────────┐ ║
║  │ CONTEXT ARTIFACTS (.context/)                                         │ ║
║  ├──────────────────────────────────────────────────────────────────────┤ ║
║  │   {✓|✗} context-manifest.json                                        │ ║
║  │   {✓|✗} mandatory/architecture.dot                                   │ ║
║  │   {✓|✗} mandatory/parent-prd.md                                      │ ║
║  │   {✓|✗} mandatory/api-contracts.yaml                                 │ ║
║  └──────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
║  ┌──────────────────────────────────────────────────────────────────────┐ ║
║  │ PHASE OVERRIDES                                                       │ ║
║  ├──────────────────────────────────────────────────────────────────────┤ ║
║  │   {✓|✗} .claude/phase-overrides.json                                 │ ║
║  │   Externally completed: {list or "none"}                              │ ║
║  └──────────────────────────────────────────────────────────────────────┘ ║
║                                                                            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  How would you like to proceed?                                            ║
║                                                                            ║
║  [E] Enhance existing PRD (fill gaps, add missing sections)                ║
║  [F] Fresh start (archive existing, create new PRD)                        ║
║  [R] Review existing PRD first (show detailed analysis)                    ║
║  [C] Create missing context artifacts first                                ║
║  [S] Skip discovery (PRD is complete, proceed to validation)               ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### Step 4: Handle Human Decision

| Choice | Action | Next State |
|--------|--------|------------|
| **[E] Enhance** | Load existing PRD, enter Enhance Mode | `mode: "enhance"` |
| **[F] Fresh** | Archive to `docs/PRD.archived.{date}.md`, start standard flow | `mode: "fresh"` |
| **[R] Review** | Show detailed PRD analysis, return to gate | Stay at gate |
| **[C] Context** | Invoke dot-architect for missing diagrams, then return | Stay at gate |
| **[S] Skip** | Emit PHASE2_COMPLETE signal, proceed to Phase 3 | Skip discovery |

### Step 5: Record Decision in State

```json
// .discovery/discovery-state.json
{
  "version": "2.0",
  "pre_discovery_gate": {
    "detection": {
      "existing_prd": true,
      "prd_completeness": 0.74,
      "context_complete": false,
      "missing_context": ["architecture.dot"]
    },
    "human_decision": "enhance",
    "decided_at": "2025-12-21T10:00:00Z",
    "rationale": "PRD exists from infrastructure planning, needs implementation details"
  },
  "mode": "enhance",
  "status": "in_progress",
  "current_stage": "2.1"
}
```

---

## Enhance Mode (NEW)

**Activated when human chooses [E] at Pre-Discovery Gate, or when PHASE2_DISCOVERY_ENHANCE_V1 is triggered.**

### Philosophy

Enhance Mode recognizes that PRDs often come from:
- Parent system planning (modular development)
- Previous development cycles
- External stakeholders
- Different teams

Rather than discarding this work, Enhance Mode:
1. **Preserves** existing content
2. **Identifies gaps** against the 19-section template
3. **Asks targeted questions** only for missing/incomplete sections
4. **Merges** new content without losing existing

### Enhance Mode Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ENHANCE MODE FLOW                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐                                                    │
│  │ Load Existing PRD │                                                   │
│  └────────┬─────────┘                                                    │
│           ▼                                                              │
│  ┌──────────────────┐                                                    │
│  │ Analyze Against  │  Compare to templates/PRD-template.md              │
│  │ 19-Section       │  Identify missing/incomplete sections              │
│  │ Template         │                                                    │
│  └────────┬─────────┘                                                    │
│           ▼                                                              │
│  ┌──────────────────┐                                                    │
│  │ Present Gap      │  Show what's complete vs. missing                  │
│  │ Analysis         │  Prioritize gaps by importance                     │
│  └────────┬─────────┘                                                    │
│           ▼                                                              │
│  ┌──────────────────┐                                                    │
│  │ For Each Gap:    │  Ask targeted questions                            │
│  │ • Question       │  Gather missing information                        │
│  │ • Research       │  Offer web research if helpful                     │
│  │ • Merge          │  Insert into existing PRD                          │
│  └────────┬─────────┘                                                    │
│           ▼                                                              │
│  ┌──────────────────┐                                                    │
│  │ Validate Against │  Run same checks as fresh PRD                      │
│  │ Context Manifest │  Ensure interface contracts align                  │
│  └────────┬─────────┘                                                    │
│           ▼                                                              │
│  ┌──────────────────┐                                                    │
│  │ Architecture     │  MANDATORY gate before synthesis                   │
│  │ Review Gate      │  Get human approval                                │
│  └────────┬─────────┘                                                    │
│           ▼                                                              │
│  ┌──────────────────┐                                                    │
│  │ Emit Enhanced    │  PHASE2_COMPLETE with mode: "enhanced"             │
│  │ PRD Signal       │                                                    │
│  └──────────────────┘                                                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Load and Parse Existing PRD

```javascript
const existingPRD = readFile("docs/PRD.md");

// Parse into sections
const sections = parsePRDSections(existingPRD);
// Returns: { "0": content, "1": content, ..., "18": content }
```

### Step 2: Gap Analysis

Compare against required 19 sections:

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    PRD GAP ANALYSIS                                        ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  COMPLETE SECTIONS (no action needed):                                     ║
║    ✓ Section 0: Vision & Problem Statement                                 ║
║    ✓ Section 1: Architectural Layer                                        ║
║    ✓ Section 4: Executive Summary                                          ║
║    ✓ Section 6: Feature Requirements                                       ║
║                                                                            ║
║  INCOMPLETE SECTIONS (need enhancement):                                   ║
║    ⚠ Section 3: Interface Contracts (missing EXPORTS)                      ║
║    ⚠ Section 7: Non-Functional Requirements (missing security)             ║
║    ⚠ Section 5: System Architecture (diagrams referenced but missing)      ║
║                                                                            ║
║  MISSING SECTIONS (need creation):                                         ║
║    ✗ Section 8: Tech Stack Selection                                       ║
║    ✗ Section 12: Risks & Assumptions                                       ║
║    ✗ Section 17: Research References                                       ║
║                                                                            ║
║  PRIORITY ORDER:                                                           ║
║    1. Section 8 (Tech Stack) - blocks specification phase                  ║
║    2. Section 3 (Interface Contracts) - blocks integration                 ║
║    3. Section 5 (Architecture) - MANDATORY for gate                        ║
║    4. Others...                                                            ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

Shall I walk you through filling these gaps? [Y/n]
```

### Step 3: Targeted Questions

For each gap, ask only what's needed:

**Example for missing Section 8 (Tech Stack):**

```
SECTION 8: TECH STACK SELECTION

Your PRD mentions "Node.js" and "PostgreSQL" but doesn't have a formal
tech stack section.

Let me confirm and expand:

Backend:
  • Runtime: Node.js (mentioned) - which version? [20.x LTS / 22.x / other]
  • Framework: [Express / Fastify / NestJS / Hono / other]
  • ORM/DB: PostgreSQL (mentioned) - via [Prisma / Drizzle / raw pg / other]

Frontend:
  • Your PRD doesn't mention frontend. Is there one? [Yes / No / External]
  • If yes: [React / Vue / Svelte / other]

Should I research best practices for your stack combination? [Y/n]
```

### Step 4: Merge Content

When adding new content:

1. **Find insertion point** in existing PRD
2. **Preserve existing content** - never delete user's words
3. **Add new content** with clear markers
4. **Update section header** if needed

```markdown
## Section 8: Technical Architecture

<!-- EXISTING CONTENT PRESERVED -->
The system will use Node.js for the backend.

<!-- ENHANCED 2025-12-21 -->
### Tech Stack Details

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Runtime | Node.js | 20.x LTS | Stability, long-term support |
| Framework | Fastify | 4.x | Performance, TypeScript support |
| Database | PostgreSQL | 16 | ACID compliance, JSON support |
| ORM | Drizzle | 0.29+ | Type-safe, lightweight |

<!-- END ENHANCEMENT -->
```

### Step 5: Context Validation

If `.context/context-manifest.json` exists, validate:

1. **Interface alignment**: PRD EXPORTS/IMPORTS match manifest declarations
2. **Parent PRD consistency**: Layer assignment compatible with parent
3. **Contract versions**: No conflicts with declared versions

```
CONTEXT VALIDATION

Checking PRD against .context/context-manifest.json...

✓ Module identity matches (PRD-025: Auth Module)
✓ Parent system reference valid (PRD-000)
⚠ Interface mismatch detected:

  PRD declares EXPORT:
    - AuthGateway v1.9.0

  Context manifest declares:
    - AuthGateway v2.0.0

  [Update PRD to v2.0.0 / Update manifest to v1.9.0 / Discuss]
```

### Enhance Mode Completion

When all gaps are filled:

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    PRD ENHANCEMENT COMPLETE                                ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  Enhanced sections:                                                        ║
║    ✓ Section 3: Interface Contracts (added EXPORTS)                        ║
║    ✓ Section 5: Architecture (embedded diagrams)                           ║
║    ✓ Section 8: Tech Stack (new section)                                   ║
║    ✓ Section 12: Risks (new section)                                       ║
║    ✓ Section 17: Research References (new section)                         ║
║                                                                            ║
║  PRD completeness: 74% → 100%                                              ║
║  Context validated: ✓                                                       ║
║  Architecture approved: ✓                                                   ║
║                                                                            ║
║  Ready to proceed to Phase 3 (PRD Validation)?                             ║
║  [Y] Proceed / [R] Review changes / [E] Edit more                          ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## Discovery Modes

### Quick Mode (Express Discovery)

For users who already know what they want to build. Uses rapid yes/no questions instead of deep exploration.

**Activation:** "quick discovery", "express discovery", "fast PRD"

```
QUICK DISCOVERY MODE

I'll ask rapid-fire questions. Answer with:
  • Y/N for yes/no
  • Skip to use defaults
  • Expand to dive deeper on any topic

Ready? Let's go...
```

**Quick Mode Flow:**

```
┌─────────────────────────────────────────────────────────────────┐
│  QUICK DISCOVERY CHECKLIST                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  VISION (30 seconds)                                            │
│  ├─ One-line description: _______________________               │
│  └─ Primary user: _______________________                       │
│                                                                 │
│  SCOPE (Y/N/Skip for each)                                      │
│  ├─ Backend API?          [Y/N]                                 │
│  ├─ Frontend UI?          [Y/N]                                 │
│  ├─ Database?             [Y/N]                                 │
│  ├─ Authentication?       [Y/N]                                 │
│  ├─ External APIs?        [Y/N]                                 │
│  └─ Mobile?               [Y/N]                                 │
│                                                                 │
│  LAYER (pick one)                                               │
│  └─ L0/L1/L2/L3/L4/L5?    [___]                                 │
│                                                                 │
│  CONSTRAINTS (Y/N/Skip)                                         │
│  ├─ High performance?     [Y/N] → If Y: latency target? ___    │
│  ├─ Security critical?    [Y/N] → If Y: compliance? ___        │
│  ├─ High availability?    [Y/N] → If Y: SLA target? ___        │
│  └─ Edge deployment?      [Y/N]                                 │
│                                                                 │
│  SOFTWARE POTENTIAL (Y/N/Future/Skip)                           │
│  ├─ Public API?           [Y/N/F]                               │
│  ├─ Plugin system?        [Y/N/F]                               │
│  ├─ Multi-tenant?         [Y/N/F]                               │
│  ├─ Self-hosted option?   [Y/N/F]                               │
│  └─ ML/AI features?       [Y/N/F]                               │
│                                                                 │
│  PIPELINE CONFIG                                                │
│  ├─ Skip deployment phase? [Y/N] (component mode)               │
│  ├─ Skip E2E tests?        [Y/N] (tested elsewhere)             │
│  └─ Generate tasks.json?   [Y/N]                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Time:** 5-10 minutes (vs 45-120 for full discovery)

### Component Mode

For building components that integrate into a larger system. Skips deployment and certain operational phases.

**Activation:** "component mode", "library mode", "building a component"

**What's different:**
- Skips Phase 8 (Deployment) - deployment happens at system level
- Skips E2E user workflows - tested at integration level
- Focuses on interface contracts and API design
- Emphasizes testability and documentation

**Pipeline ends at:** Phase 6 (Integration Testing) or Phase 7 (if E2E included)

```json
{
  "pipeline_config": {
    "mode": "component",
    "skip_phases": [8, 8.5],
    "optional_phases": [7],
    "focus_areas": ["interface_contracts", "unit_tests", "documentation"],
    "deployment_venue": "external",
    "e2e_venue": "integration_repo"
  }
}
```

### Full Mode (Default)

Complete 9-stage discovery with deep exploration of each area. Best for:
- Greenfield projects
- Complex systems
- When you're not sure what to build

## Web Research Integration

This skill integrates with the **Web Researcher** skill for structured external research using Claude Code's built-in WebSearch and WebFetch tools.

### Research Prompt

**At the start of discovery, offer research:**
```
Before we dive in, would you like me to research the landscape?

I can look up:
  • Competitors - pricing, features, differentiators
  • Technical patterns - how others solve similar problems
  • Market data - size, trends, opportunities

This helps inform our decisions but won't drive requirements.
Your vision stays primary.

Say "research competitors" or "skip research" to continue.
```

### When to Offer Research

| Stage | Offer | Trigger Phrase |
|-------|-------|----------------|
| Start of discovery | Competitor/market research | "research competitors" |
| Stage 2.1 (Artifacts) | Similar projects | "find similar projects" |
| Stage 2.2.5 (Users) | User behavior patterns | "research user patterns" |
| Stage 2.3 (Scope) | Feature benchmarks | "what features do others have" |
| Stage 2.4 (I/O) | API documentation | "fetch API docs for [service]" |
| Stage 2.5 (Constraints) | Industry benchmarks | "research benchmarks" |

### Research Output Integration

Web research results are saved to `.research/` and can feed into PRD:
- **Section 3 (Market Context)**: Competitor landscape, market size
- **Section 5 (Anti-Requirements)**: "Unlike X, we won't..."
- **Section 8 (Architecture)**: Technical pattern recommendations

**Note:** Research-sourced additions get -0.15 confidence penalty with Plan Guardian.

---

## Internet-Enabled Discovery

This skill has **full internet access**. Leverage this throughout the discovery process:

### Available Research Capabilities

| Capability | When to Use | Tools |
|------------|-------------|-------|
| **Web Search** | Research competitors, similar projects, best practices | WebSearch, WebFetch |
| **API Documentation** | Fetch specs for integrations the user mentions | WebFetch |
| **GitHub Research** | Analyze similar open-source projects, find patterns | GitHub MCP tools |
| **Technical Standards** | Look up compliance requirements, protocols, formats | WebSearch, WebFetch |
| **Library/Framework Docs** | Research technology choices | WebFetch |
| **Competitive Analysis** | Understand market landscape | WebSearch |
| **Web Researcher** | Structured multi-source research | Web Researcher skill |

### Proactive Research Opportunities

During discovery, **proactively offer to research**:

1. **Stage 2.1 (Artifacts)**: "Would you like me to find similar open-source projects or competitor products for reference?"

2. **Stage 2.2 (Context)**: "I can research common architectural patterns for [project type]. Want me to look that up?"

3. **Stage 2.3 (Scope)**: "Should I check what features similar products typically include?"

4. **Stage 2.4 (I/O)**: "I can fetch the API documentation for [mentioned service]. Would that help?"

5. **Stage 2.5 (Constraints)**: "Want me to look up industry benchmarks for [performance/security] requirements?"

6. **Stage 2.6 (Requirements)**: "I can research how similar systems handle [specific functionality]. Interested?"

### Research Output

When conducting research, save findings to `.discovery/artifacts/research/`:
- `competitors.md` — Competitive analysis
- `api-specs/` — Downloaded API documentation
- `best-practices.md` — Industry best practices
- `benchmarks.md` — Performance/security benchmarks
- `technology-options.md` — Technology comparison notes

## Discovery State

Track progress in `.discovery/discovery-state.json`:

```json
{
  "version": "2.0",
  "status": "in_progress",
  "current_stage": "0.1",
  "stages": {
    "0.1": { "name": "Artifact Collection", "status": "pending", "started_at": null, "completed_at": null },
    "0.2": { "name": "Project Context", "status": "pending", "started_at": null, "completed_at": null },
    "0.2.5": { "name": "User Discovery", "status": "pending", "started_at": null, "completed_at": null },
    "0.3": { "name": "Scope Bounding", "status": "pending", "started_at": null, "completed_at": null },
    "0.4": { "name": "Input/Output Definition", "status": "pending", "started_at": null, "completed_at": null },
    "0.4.5": { "name": "Dependency Documentation Capture", "status": "pending", "started_at": null, "completed_at": null },
    "0.5": { "name": "Constraint Elicitation", "status": "pending", "started_at": null, "completed_at": null },
    "0.6": { "name": "Requirements Discovery", "status": "pending", "started_at": null, "completed_at": null },
    "0.6.5": { "name": "Architecture Design", "status": "pending", "started_at": null, "completed_at": null, "human_approved": false },
    "0.7": { "name": "PRD Synthesis", "status": "pending", "started_at": null, "completed_at": null },
    "0.8": { "name": "Strategic Alignment", "status": "pending", "started_at": null, "completed_at": null }
  },
  "artifacts_collected": [],
  "project_type": null,
  "layer_assignment": null,
  "personas": [],
  "software_potential": null,
  "mvp_scope": null
}
```

## Starting Discovery

When user initiates discovery:

1. **Check for existing state**
   - If `.discovery/discovery-state.json` exists and is incomplete, offer to resume
   - Otherwise, create fresh discovery state

2. **Create directory structure**
```
.discovery/
├── artifacts/
│   ├── existing-prds/
│   ├── architecture/
│   ├── interfaces/
│   ├── existing-code/
│   ├── compliance/
│   └── research/
├── scope/
├── discovery-state.json
└── discovery-log.md
```

3. **Display welcome message**
```
PHASE 2: PROJECT DISCOVERY

I'll guide you through defining your project requirements. We'll cover:

  Stage 2.1:   Artifact Collection     (gather context + web research)
  Stage 2.2:   Project Context         (understand positioning)
  Stage 2.2.5: User Discovery          (personas, journeys, pain points)
  Stage 2.3:   Scope Bounding          (define boundaries + software potential)
  Stage 2.4:   Input/Output Definition (specify interfaces + fetch API docs)
  Stage 2.4.5: Dependency Docs Capture (version-pinned API documentation)
  Stage 2.5:   Constraint Elicitation  (non-negotiables + benchmarks)
  Stage 2.6:   Requirements Discovery  (define what system does)
  Stage 2.6.5: Architecture Design     (C4 diagrams + human approval) ← MANDATORY
  Stage 2.7:   PRD Synthesis           (generate PRD from discovery artifacts)
  Stage 2.8:   Strategic Alignment     (business validation + MVP scope)

I have full internet access — I can research competitors, fetch API
docs, look up benchmarks, and analyze similar projects as we go.

This process ensures we're building the RIGHT thing (Stages 2.1-2.8)
before we build it RIGHT (Phases 3-12).

Time estimate: 45-120 minutes

You can pause anytime and resume later.

Ready to begin? Let's start with Stage 2.1: Artifact Collection.
```

## Stage 2.1: Artifact Collection

**Goal:** Gather existing materials that provide context — both local files AND web resources.

**Questions to ask:**

1. "Do you have any existing materials to share that would help me understand your project?"

2. Present categories for **local artifacts**:
   - Parent or related PRDs (if part of larger system)
   - Architecture diagrams
   - Interface specifications (APIs, protocols)
   - Existing codebase (if improving existing code)
   - Compliance/regulatory documents
   - Research papers or whitepapers
   - Meeting notes or decision records

3. **Offer web-based research:**
   - "Would you like me to research similar projects or competitors online?"
   - "Are there any APIs or services you plan to integrate with? I can fetch their documentation."
   - "Should I look up any technical standards or compliance frameworks relevant to your project?"

4. For each artifact provided:
   - Copy to appropriate `.discovery/artifacts/` subdirectory
   - Analyze and extract key information
   - Summarize findings to user

5. For web research conducted:
   - Save to `.discovery/artifacts/research/`
   - Summarize key findings
   - Note sources for traceability

6. If user says "none" or "skip":
   - Acknowledge greenfield project
   - Still offer: "Even without local artifacts, I can research similar projects online. Interested?"

**Web Research Actions:**

| User Mentions | Research Action |
|---------------|-----------------|
| Competitor name | Search for their product, features, pricing |
| API integration | Fetch API docs, OpenAPI specs if available |
| Technology stack | Research best practices, common patterns |
| Industry/domain | Look up domain-specific requirements, standards |
| Similar product | Find open-source alternatives on GitHub |

**Completion criteria:**
- User confirms all artifacts collected
- Web research completed (if requested)
- Summary of all artifacts displayed
- State updated with `artifacts_collected` list

## Stage 2.2: Project Context

**Goal:** Understand project type and positioning.

**Questions to ask:**

1. "What type of project is this?"
   - Greenfield (new from scratch)
   - Brownfield (improving existing code)
   - Replacement (rewriting legacy system)
   - Integration (connecting existing systems)

2. If brownfield/replacement: "What's being kept vs. replaced?"

3. "Where does this fit architecturally?" (Explain L0-L5 layers)
   - L0: Primitives (math, types, no dependencies)
   - L1: Infrastructure (logging, config, networking)
   - L2: Spatial (coordinates, transforms)
   - L3: Processing (algorithms, data processing)
   - L4: Fusion (multi-source integration)
   - L5: Interface (APIs, user-facing)

4. "What systems does this depend on?" (upstream)

5. "What systems depend on this?" (downstream)

**If artifacts include parent PRD:**
- Extract positioning information automatically
- Confirm with user

**Completion criteria:**
- Project type determined
- Layer assignment confirmed
- Dependencies documented

## Stage 2.2.5: User Discovery (NEW)

**Goal:** Understand who will use this and why, before defining scope.

**Why this matters:** Scope decisions should be driven by user needs, not technical convenience. This stage ensures we build the right thing for the right people.

### Step 1: Identify User Types

Ask: "Who are the different types of people who will use this system?"

For each user type, capture:
- Role/title
- Primary goal with the system
- Technical sophistication level
- Frequency of use

### Step 2: Create Primary Persona

**Template:**
```
Persona: [Name]
Role: [Job title/role]
Goals:
  - [Primary goal]
  - [Secondary goal]
Pain Points:
  - [Current frustration 1]
  - [Current frustration 2]
Context: [When/where/how they'd use this]
Quote: "[Something this persona might say about the problem]"
```

**Proactive Research:**
- "Want me to research user behavior patterns for [this type of user]?"
- "I can look up UX best practices for [industry/domain]. Interested?"

### Step 3: Map User Journey

For the primary persona, map their journey:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Awareness  │────▶│   First Use │────▶│  Regular Use│────▶│   Advocacy  │
│  How they   │     │  Onboarding │     │  Core value │     │  Sharing    │
│  find us    │     │  experience │     │  delivery   │     │  with others│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

Ask at each stage:
- What are they trying to accomplish?
- What emotions are they feeling?
- What could go wrong?

### Step 4: Identify Pain Points

Ask: "What's frustrating about how users solve this problem today?"

Categories:
- Time wasters
- Error-prone steps
- Missing information
- Context switching
- Waiting/delays

### Step 5: Define Value Proposition

Help user articulate:
- Core benefit (primary value)
- Unique differentiator (why choose this)
- Proof points (how we demonstrate value)

**Generate:** `.discovery/scope/personas.yaml`, `.discovery/scope/user-journey.md`

**Completion criteria:**
- At least one primary persona defined
- User journey mapped for primary persona
- Top 3 pain points identified
- Value proposition articulated

## Stage 2.3: Scope Bounding

**Goal:** Explicitly define what's IN and OUT of scope.

**Ask about each component category:**

| Component | Response Options |
|-----------|------------------|
| Backend/Core Processing | In scope / Out of scope / N/A |
| Frontend/UI | In scope / Out of scope / N/A |
| Mobile Applications | In scope / Out of scope / N/A |
| Database/Persistence | In scope / Out of scope / N/A |
| External API (public) | In scope / Out of scope / N/A |
| Internal API (service) | In scope / Out of scope / N/A |
| Authentication/Auth | In scope / Out of scope / N/A |
| Monitoring/Observability | In scope / Out of scope / N/A |
| Deployment/Infrastructure | In scope / Out of scope / N/A |

**Generate:** `.discovery/scope/boundaries.yaml`

### Software Potential Checklist (NEW)

After defining basic scope, explore future potential dimensions:

**Ask:** "Let's think about what this could become. For each dimension, tell me if it's relevant now, might be relevant later, or not applicable."

```yaml
software_potential:
  # API & Extensibility
  api_extensibility:
    public_api: [In v1 / Future / Never / TBD]
    webhook_support: [In v1 / Future / Never / TBD]
    developer_sdk: [In v1 / Future / Never / TBD]
    plugin_system: [In v1 / Future / Never / TBD]
    custom_integrations: [In v1 / Future / Never / TBD]

  # Deployment Models
  deployment_models:
    saas_hosted: [In v1 / Future / Never / TBD]
    self_hosted: [In v1 / Future / Never / TBD]
    edge_deployment: [In v1 / Future / Never / TBD]
    air_gapped_offline: [In v1 / Future / Never / TBD]
    multi_region: [In v1 / Future / Never / TBD]

  # Multi-Tenancy & Scale
  multi_tenancy:
    shared_infrastructure: [In v1 / Future / Never / TBD]
    tenant_isolation: [In v1 / Future / Never / TBD]
    custom_domains: [In v1 / Future / Never / TBD]
    white_label: [In v1 / Future / Never / TBD]

  # Data & Intelligence
  data_strategy:
    analytics_dashboard: [In v1 / Future / Never / TBD]
    data_export: [In v1 / Future / Never / TBD]
    ml_ai_features: [In v1 / Future / Never / TBD]
    data_marketplace: [In v1 / Future / Never / TBD]

  # Platform Evolution
  platform_potential:
    app_marketplace: [In v1 / Future / Never / TBD]
    partner_ecosystem: [In v1 / Future / Never / TBD]
    developer_community: [In v1 / Future / Never / TBD]
    certification_program: [In v1 / Future / Never / TBD]

  # Monetization
  monetization:
    subscription: [In v1 / Future / Never / TBD]
    usage_based: [In v1 / Future / Never / TBD]
    freemium: [In v1 / Future / Never / TBD]
    enterprise_licensing: [In v1 / Future / Never / TBD]
    marketplace_revenue: [In v1 / Future / Never / TBD]
```

**Why this matters:** Decisions made now affect future potential. Understanding future possibilities helps make better architectural choices today.

**Proactive Research:**
- "I can research how similar products evolved over time. Want me to look that up?"
- "Should I find examples of successful platform/ecosystem plays in this space?"

**Generate:** `.discovery/scope/software-potential.yaml`

**Completion criteria:**
- All categories addressed
- User confirms scope summary
- boundaries.yaml created
- software-potential.yaml created

## Stage 2.4: Input/Output Definition

**Goal:** Precisely define system interfaces.

**For INPUTS, ask:**
- What data/requests does the system receive?
- Where does each input come from?
- What format (JSON, protobuf, binary, etc.)?
- What rate/frequency?

**For OUTPUTS, ask:**
- What data/responses does the system produce?
- Who/what consumes each output?
- What format?
- What rate/frequency?

**Don't forget:**
- Configuration inputs
- Metrics outputs
- Log outputs
- Event outputs

**Web Research for Interfaces:**

When user mentions an external service or API:
1. **Offer to fetch documentation**: "I can pull the API docs for [service]. Want me to?"
2. **Look up OpenAPI/Swagger specs** if available
3. **Research common integration patterns** for that service
4. **Save specs** to `.discovery/artifacts/api-specs/`

| Service Type | Research Action |
|--------------|-----------------|
| Cloud provider (AWS, GCP, Azure) | Fetch relevant service API docs |
| SaaS integration (Stripe, Twilio, etc.) | Get API reference, rate limits, auth patterns |
| Database | Look up connection patterns, query formats |
| Message queue (Kafka, RabbitMQ, etc.) | Research message formats, consumer patterns |
| OAuth/Auth provider | Fetch token formats, flow documentation |

**Generate:** `.discovery/scope/inputs.yaml`, `.discovery/scope/outputs.yaml`

**Completion criteria:**
- All inputs documented with source, format, rate
- All outputs documented with consumer, format, rate
- External API specs fetched (if applicable)
- User confirms I/O summary

## Stage 2.4.5: Dependency Documentation Capture (NEW - CRITICAL)

**Goal:** Capture version-specific documentation for ALL planned dependencies to enable contract-based validation.

> **Why This Stage Exists:**
> Bugs often arise from misunderstanding how dependencies actually work at the exact version used.
> Generic web searches aren't enough - we need authoritative, version-pinned API documentation
> that can be validated against during implementation and testing.

**Step 1: Enumerate All Dependencies**

Compile a complete list from PRD Section 2 and discovered I/O:

```yaml
# docs/discovery/dependencies/dependency-manifest.yaml
dependencies:
  host_systems:
    - name: "macOS"
      version: "15.1+"
      relevant_apis: ["Accessibility", "Keychain", "Notifications"]

  runtime_platforms:
    - name: "Node.js"
      version: "20.x LTS"
      relevant_features: ["ESM modules", "fetch API", "crypto"]

  libraries:
    - name: "axios"
      version: "1.6.0"  # EXACT version, not ^1.6.0
      usage: "HTTP client for API calls"

    - name: "react"
      version: "18.2.0"
      usage: "UI framework"

  cloud_services:
    - name: "AWS Lambda"
      runtime: "nodejs20.x"
      relevant_apis: ["Invocation", "Layers", "Environment"]

  external_apis:
    - name: "Stripe"
      api_version: "2024-11-20"
      endpoints_used: ["PaymentIntents", "Customers"]

  messaging_systems:
    - name: "Redis"
      version: "7.2"
      usage: "Pub/Sub, Caching"
```

**Step 2: Fetch Version-Specific Documentation**

For EACH dependency, capture authoritative documentation:

| Dependency Type | Documentation Source | What to Capture |
|-----------------|---------------------|-----------------|
| **Host OS APIs** | Official developer docs | Permission requirements, API surface, version notes |
| **Runtime** | Official docs for exact version | Breaking changes, new features, deprecations |
| **Libraries** | Package docs, GitHub releases | API reference, changelog for version, known issues |
| **Cloud Services** | Provider documentation | API limits, quotas, authentication, error codes |
| **External APIs** | Official API reference | Endpoints, request/response formats, rate limits |
| **Databases** | Official docs for version | Query syntax, connection pooling, error handling |

**Documentation Capture Process:**

```markdown
For each dependency:
1. Identify official documentation URL
2. Fetch documentation for EXACT version (not latest)
3. Extract relevant API surface:
   - Function/method signatures
   - Request/response formats
   - Error codes and handling
   - Rate limits and quotas
   - Authentication requirements
   - Known issues/edge cases
4. Store in structured format
5. Note any version-specific behavior changes
```

**Step 3: Create Structured Documentation Cache**

Store in `docs/discovery/dependencies/`:

```
docs/discovery/dependencies/
├── dependency-manifest.yaml      # Master list linking deps to docs
├── host-systems/
│   ├── macos-15.1-accessibility.md
│   └── macos-15.1-keychain.md
├── runtimes/
│   └── nodejs-20.x-api-surface.md
├── libraries/
│   ├── axios-1.6.0/
│   │   ├── api-reference.md      # Core API surface
│   │   ├── error-handling.md     # Error types and codes
│   │   └── breaking-changes.md   # Changes from previous versions
│   └── react-18.2.0/
│       ├── hooks-reference.md
│       └── concurrent-features.md
├── cloud-services/
│   └── aws-lambda-nodejs20/
│       ├── runtime-api.md
│       ├── limits-quotas.md
│       └── error-codes.md
├── external-apis/
│   └── stripe-2024-11-20/
│       ├── payment-intents.md
│       └── error-codes.md
└── messaging/
    └── redis-7.2/
        ├── commands-reference.md
        └── pubsub-patterns.md
```

**Step 4: Document Version-Specific Gotchas**

Create `docs/discovery/dependencies/version-notes.md`:

```markdown
# Version-Specific Notes

## axios 1.6.0
- **Breaking Change**: Error response structure changed from 1.5.x
- **New**: `formToJSON` utility added
- **Gotcha**: Default timeout is now `0` (infinite) not `10000`

## macOS 15.1 Accessibility
- **Requirement**: App must be added to System Preferences > Privacy > Accessibility
- **Gotcha**: Silent failure if not authorized - no error thrown
- **Detection**: Use `AXIsProcessTrusted()` to check

## Node.js 20.x
- **New**: Native `fetch()` API now stable
- **Gotcha**: `fetch()` doesn't throw on 4xx/5xx - must check `response.ok`
- **Breaking**: `--experimental-modules` no longer needed
```

**Step 5: Generate Contract Summary**

Create `docs/discovery/dependencies/contract-summary.md`:

```markdown
# Dependency Contract Summary

This document summarizes the API contracts that implementation must follow.
Use this during code review and testing validation.

## HTTP Client (axios 1.6.0)

### Request Pattern
```javascript
const response = await axios.get(url, {
  timeout: 5000,  // MUST set - default is infinite
  validateStatus: (status) => status < 500  // Handle 4xx as success
});
```

### Error Handling Contract
```javascript
try {
  await axios.post(url, data);
} catch (error) {
  if (error.response) {
    // Server responded with 4xx/5xx
    // error.response.data, error.response.status
  } else if (error.request) {
    // Request made but no response (network error)
  } else {
    // Request setup error
  }
}
```

## macOS Accessibility (15.1+)

### Permission Check Contract
```swift
// MUST check before using accessibility APIs
if !AXIsProcessTrusted() {
  // Prompt user to grant access
  let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue(): true]
  AXIsProcessTrustedWithOptions(options as CFDictionary)
}
```
```

**Research Actions:**

| Question | Research Action |
|----------|-----------------|
| "What version of X should we use?" | Compare latest stable vs LTS, check compatibility |
| "What's different in X version Y?" | Fetch changelog, migration guide |
| "What are common issues with X?" | Search GitHub issues, Stack Overflow |
| "What permissions does X need?" | Fetch platform-specific requirements |

**Completion Criteria:**
- [ ] All dependencies from PRD Section 2 enumerated in manifest
- [ ] Version-specific documentation captured for each dependency
- [ ] Host system API requirements documented
- [ ] Breaking changes and gotchas noted
- [ ] Contract summary created for implementation reference
- [ ] User confirms dependency documentation is complete

**Output Files:**
- `docs/discovery/dependencies/dependency-manifest.yaml`
- `docs/discovery/dependencies/*/` (per-dependency docs)
- `docs/discovery/dependencies/version-notes.md`
- `docs/discovery/dependencies/contract-summary.md`

---

## Stage 2.5: Constraint Elicitation

**Goal:** Document non-negotiable requirements.

**Walk through four categories:**

### Performance Constraints
- Latency requirements (target, max, P99)
- Throughput requirements
- Memory limits
- CPU/GPU requirements
- Startup time

### Security Constraints
- Network model (traditional, zero trust, air-gapped)
- Authentication requirements
- Data classification
- Compliance frameworks
- Encryption requirements

### Reliability Constraints
- Availability target
- Failure mode (fail-fast, fail-safe, graceful)
- Recovery time objective
- Redundancy requirements

### Compliance Constraints
- Industry standards
- Regulatory requirements
- Audit requirements

**Web Research for Constraints:**

When user is uncertain, **proactively research benchmarks**:

| Constraint Type | Research Action |
|-----------------|-----------------|
| Latency targets | Search for industry benchmarks (e.g., "e-commerce API latency benchmarks") |
| Availability | Look up SLA standards for similar services |
| Compliance | Fetch framework requirements (SOC2, HIPAA, PCI-DSS, GDPR) |
| Security standards | Research OWASP, NIST, CIS benchmarks |
| Performance | Find case studies from similar-scale systems |

**Offer research when user says "I don't know":**
- "I can look up typical [latency/availability/etc.] requirements for [industry/project type]. Want me to?"
- "Should I research what [compliance framework] specifically requires?"
- "I can find benchmarks from similar projects. Interested?"

**Save research to:** `.discovery/artifacts/research/benchmarks.md`

**For any "I don't know" responses:**
- Offer to research benchmarks
- Suggest reasonable defaults based on research
- Mark as "TBD" if user prefers

**Generate:** `.discovery/scope/constraints.yaml`

**Completion criteria:**
- All constraint categories addressed
- Benchmarks researched (if requested)
- User confirms constraints summary
- constraints.yaml created

## Stage 2.6: Requirements Discovery

**Goal:** Define functional requirements in EARS format.

**EARS Format:**
```
WHEN [trigger condition], the system SHALL [required behavior].
```

**Process:**
1. Start with core functionality based on project description
2. Propose requirements from artifacts (if any)
3. Ask clarifying questions
4. For each requirement:
   - State in EARS format
   - Assign ID (R_XXX)
   - Ask user to Accept / Modify / Reject

**Requirement categories to cover:**
- Core functionality
- Error handling
- Performance (derived from constraints)
- Security (derived from constraints)
- Observability
- Integration points

**Completion criteria:**
- All major functional areas covered
- Each requirement in EARS format with ID
- User confirms requirements are complete

## Stage 2.6.5: Architecture Design & Adjudication (MANDATORY)

**Goal:** Create C4 architecture diagrams through an ITERATIVE ADJUDICATION PROCESS with human stakeholders, achieving explicit approval BEFORE PRD synthesis.

> **Why This Stage Matters:**
> Architecture diagrams force explicit thinking about system structure, dependencies,
> and data flows. This prevents "discovery drift" where research is gathered but
> not incorporated into the final design.
>
> **CRITICAL:** Diagrams are not "done" when AI thinks they're right—they're done
> when ALL stakeholders explicitly agree they accurately represent the system.

**Agent Invocation:**

This stage invokes the **dot-architect** agent (opus model) to drive the adjudication:

```
Task: Invoke dot-architect agent
Model: opus (required for PhD-level architectural reasoning)
Prompt: "Create and adjudicate mandatory architecture diagrams for this project.
         Read all discovery research first, then create C4 diagrams with
         iterative human approval. Track all revisions in diagram-approvals.json."
```

**Step 1: Initialize Discovery & Context Structure**

If directories don't exist, create them:

```
docs/discovery/
├── research/           <- Web research findings (from earlier stages)
├── diagrams/           <- Architecture diagrams (DOT/Mermaid)
│   ├── c4-context.dot      (MANDATORY)
│   ├── c4-containers.dot   (MANDATORY)
│   ├── data-flow.dot       (MANDATORY)
│   ├── interface-map.dot   (MANDATORY)
│   └── deployment.dot      (Optional)
├── decisions/          <- Architecture Decision Records
└── agreements/         <- Human approval tracking
    └── approval-log.md

.context/               <- Module context (for modular development)
├── mandatory/
│   ├── c4-context.dot
│   ├── c4-containers.dot
│   ├── data-flow.dot
│   └── interface-map.dot
├── diagram-approvals.json  <- Tracks approval status per diagram
└── context-manifest.json
```

**Step 2: Consolidate Research**

Before creating diagrams, READ and summarize all research conducted:
1. Read `.discovery/artifacts/research/*` (older format)
2. Read `docs/discovery/research/*` (new format)
3. Read `.research/*` (web researcher output)

**Step 3: ITERATIVE DIAGRAM ADJUDICATION**

For each mandatory diagram, run the adjudication cycle:

### Mandatory Diagram Collection

| # | Diagram | File | Purpose | Approval Required |
|---|---------|------|---------|-------------------|
| 1 | **System Context (C4 L1)** | `c4-context.dot` | Where does this fit? | YES |
| 2 | **Container Diagram (C4 L2)** | `c4-containers.dot` | Major components | YES |
| 3 | **Data Flow Diagram** | `data-flow.dot` | How data moves | YES |
| 4 | **Interface Contract Map** | `interface-map.dot` | IMPORTS/EXPORTS | YES |

### The Adjudication Cycle (Per Diagram)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DIAGRAM ADJUDICATION CYCLE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. DRAFT DIAGRAM                                                            │
│     • Create from PRD/discovery research                                     │
│     • Apply C4 conventions and color coding                                  │
│     • Use DOT format (preferred) or Mermaid                                  │
│                                                                              │
│  2. PRESENT TO HUMAN                                                         │
│     • Show rendered diagram (PNG/SVG) or describe in detail                  │
│     • Provide plain-language explanation                                     │
│     • Highlight key decisions and assumptions                                │
│                                                                              │
│  3. GATHER TARGETED FEEDBACK                                                 │
│     • "Does this accurately represent [aspect]?"                             │
│     • "Are [components] correct?"                                            │
│     • "Is anything missing?"                                                 │
│                                                                              │
│  4. ADJUDICATE                                                               │
│     • [A] APPROVE → Record in diagram-approvals.json, next diagram           │
│     • [R] REVISE  → Document feedback, increment version, loop to step 1     │
│     • [D] DISCUSS → Clarify context, then re-present                         │
│                                                                              │
│  REPEAT until diagram is APPROVED                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Example Adjudication Presentation

```
╔═══════════════════════════════════════════════════════════════════════════╗
║      ARCHITECTURE ADJUDICATION: System Context (C4 L1) - Version 2        ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  DIAGRAM: c4-context.dot                                                  ║
║  [Visual representation or link to rendered PNG]                          ║
║                                                                           ║
║  PLAIN LANGUAGE DESCRIPTION:                                              ║
║  This diagram shows [Module Name] within the context of [Parent System].  ║
║  The module:                                                              ║
║  • Receives requests from [external system]                               ║
║  • Validates against [external provider]                                  ║
║  • Publishes events to [message system]                                   ║
║  • Depends on [other module] for [capability]                             ║
║                                                                           ║
║  KEY DECISIONS/ASSUMPTIONS:                                               ║
║  1. [Decision 1 with rationale]                                           ║
║  2. [Decision 2 with rationale]                                           ║
║  3. [Decision 3 with rationale]                                           ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  REVIEW QUESTIONS:                                                        ║
║                                                                           ║
║  1. Does this accurately show where this module fits in the system?       ║
║  2. Are the external systems correctly represented?                       ║
║  3. Are any components or relationships missing?                          ║
║  4. Do you agree with the key decisions listed above?                     ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  [A] APPROVE - Diagram accurately represents the architecture             ║
║  [R] REVISE  - Provide feedback for revision                              ║
║  [D] DISCUSS - Need more context before deciding                          ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

**Step 4: Track All Revisions**

Every revision is recorded in `.context/diagram-approvals.json`:

```json
{
  "version": "1.0.0",
  "diagrams": {
    "c4-context": {
      "file": ".context/mandatory/c4-context.dot",
      "status": "approved",
      "version": 3,
      "approved_by": "human",
      "approved_at": "2025-12-21T10:30:00Z",
      "revision_history": [
        {"version": 1, "feedback": "Missing external IdP system"},
        {"version": 2, "feedback": "Auth flow arrows should be reversed"},
        {"version": 3, "feedback": "Approved - accurately represents system"}
      ]
    },
    "c4-containers": {
      "file": ".context/mandatory/c4-containers.dot",
      "status": "pending",
      "version": 1,
      "revision_history": []
    }
  },
  "all_mandatory_approved": false
}
```

**Step 5: Create ADRs for Major Decisions**

For each significant architectural choice surfaced during adjudication:
- Technology stack selections
- Framework choices
- Database selection
- Integration patterns

Save to: `docs/discovery/decisions/ADR-001-[topic].md`

**Step 6: Final Architecture Gate**

Only after ALL mandatory diagrams are approved, present the final gate:

```
╔═══════════════════════════════════════════════════════════════════════════╗
║              FINAL ARCHITECTURE APPROVAL GATE                             ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  All mandatory diagrams have been individually approved:                  ║
║                                                                           ║
║  ✓ System Context (C4 L1)     - Version 3, approved 10:30                 ║
║  ✓ Container Diagram (C4 L2)  - Version 2, approved 10:45                 ║
║  ✓ Data Flow Diagram          - Version 1, approved 10:50                 ║
║  ✓ Interface Contract Map     - Version 4, approved 11:15                 ║
║                                                                           ║
║  ADRs Created: [count]                                                    ║
║                                                                           ║
║  Research Incorporated:                                                   ║
║  • Technology stack from [sources]                                        ║
║  • Best practices from [sources]                                          ║
║  • Competitor insights from [sources]                                     ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  Ready to proceed to PRD Synthesis with approved architecture.            ║
║                                                                           ║
║  Say "Proceed to PRD" to continue to Stage 2.7                            ║
║  Say "Revisit [diagram]" to re-open adjudication for a diagram            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

**DO NOT proceed to Stage 2.7 until:**
1. All 4 mandatory diagrams have status "approved" in diagram-approvals.json
2. User explicitly says "Proceed to PRD" or similar confirmation

**Step 7: Generate Stakeholder Presentations (Optional)**

Once diagrams are approved, generate polished versions for stakeholder presentations:

```bash
# Render all diagrams for stakeholder presentation
./scripts/render-diagrams.sh stakeholder --theme 4 --format png

# Or generate both technical and stakeholder versions
./scripts/render-diagrams.sh all
```

This creates:
- `docs/diagrams/rendered/technical/` - Quick DOT renders for engineers
- `docs/diagrams/rendered/stakeholder/` - Polished D2 renders with themes

The rendering pipeline:
1. **DOT files** → Graphviz (technical) or converts to D2 (stakeholder)
2. **D2 files** → Uses ELK/TALA layout with selected theme
3. **Mermaid files** → Uses mmdc if available

**Completion criteria:**
- docs/discovery/ and .context/ structures exist
- All 4 mandatory diagrams created in DOT or D2 format
- Each diagram went through adjudication cycle with tracked revisions
- `diagram-approvals.json` shows `all_mandatory_approved: true`
- Research summarized and incorporated into diagrams
- At least one ADR for major technology choice
- User explicitly approved final architecture gate
- `ARCHITECTURE_APPROVED` signal emitted

---

## Stage 2.7: PRD Synthesis

**Goal:** Generate the final PRD, deeply incorporating ALL discovery artifacts.

> **CRITICAL:** The PRD must reference and incorporate all research and diagrams
> from docs/discovery/. This is NOT optional.

**Pre-Synthesis Checklist (MANDATORY):**

Before generating PRD, verify you have READ:
- [ ] `docs/discovery/research/technology-stack.md`
- [ ] `docs/discovery/research/competitor-analysis.md`
- [ ] `docs/discovery/research/best-practices.md`
- [ ] `docs/discovery/research/sources.md`
- [ ] `docs/discovery/diagrams/context.mmd`
- [ ] `docs/discovery/diagrams/container.mmd`
- [ ] `docs/discovery/diagrams/dataflow.mmd`
- [ ] `docs/discovery/diagrams/deployment.mmd`
- [ ] `docs/discovery/decisions/ADR-*.md` (all ADRs)

If ANY of these files don't exist, STOP and complete Stage 2.6.5 first.

**Process:**
1. Read ALL docs/discovery/* artifacts
2. Compile all discovery outputs from previous stages
3. Generate PRD using Template v2.0 structure
4. **Embed diagrams in Section 5 (System Architecture)**
5. **Reference research in Section 17 (Research References)**
6. Populate all 19 sections
7. Present summary to user

**PRD Sections to generate:**
0. Vision & Problem Statement (from Stage 0.2.5)
1. Architectural Layer Assignment
2. Dependency Declaration
3. Interface Contract Summary
4. Executive Summary
5. System Architecture
6. Feature Requirements (from Stage 0.6) + Anti-Requirements
7. Non-Functional Requirements (from Stage 0.5)
8. Code Structure
9. TDD Implementation Guide
10. Integration Testing
11. Documentation Requirements
12. Operational Readiness
13. Compliance & Audit
14. Migration & Rollback
15. Risk & Assumptions
16. Success Metrics
17. Task Decomposition Guidance
18. Future Potential & Evolution (from Stage 0.3 software potential)
Appendices A-E

**Present to user:**
```
DISCOVERY COMPLETE

PRD generated at: docs/PRD.md

Summary:
  - Requirements: [count]
  - Project Type: [type]
  - Layer: [L0-L5]
  - Dependencies: [count] upstream, [count] downstream

Next steps:
  1. Review the PRD
  2. Make any edits directly
  3. Say "PRD approved, begin automated development" to proceed
```

**Completion criteria:**
- PRD generated at docs/PRD.md
- User has reviewed initial draft

## Stage 2.8: Strategic Alignment (NEW)

**Goal:** Validate the PRD against business objectives before proceeding to execution.

**Why this matters:** Technical requirements should serve business goals. This gate ensures we're building the right thing before we build it right.

### Step 1: Business Model Validation

Ask: "How does this software create and capture value?"

| Question | Answer |
|----------|--------|
| Who pays? | [Customer / Advertiser / Enterprise / N/A] |
| How do they pay? | [Subscription / Usage / One-time / Free] |
| What's the unit economics? | [Cost to serve vs. revenue per user] |
| What's the growth model? | [Viral / Sales / Content / Product-led] |

### Step 2: Stakeholder Alignment

Ask: "Who needs to approve or be informed about this project?"

| Stakeholder | Interest | Influence | Status |
|-------------|----------|-----------|--------|
| [Name/Role] | [Their goals] | [High/Medium/Low] | [Approve/Inform/Consult] |

### Step 3: MVP Definition

Ask: "What's the smallest version that delivers value?"

```
MUST HAVE (MVP):
- [Feature 1] - Required for core value
- [Feature 2] - Required for core value

SHOULD HAVE (v1.1):
- [Feature 3] - Important but not critical
- [Feature 4] - Enhances experience

COULD HAVE (v2.0):
- [Feature 5] - Nice to have
- [Feature 6] - Future expansion

WON'T HAVE (This version):
- [Feature 7] - Out of scope
- [Feature 8] - Technical debt we accept
```

### Step 4: Success Criteria Review

Review success metrics from PRD Section 0.5:

| Metric | Target | Realistic? | Measurable? | Aligned with Business? |
|--------|--------|------------|-------------|------------------------|
| [Metric 1] | [Target] | [Y/N] | [Y/N] | [Y/N] |
| [Metric 2] | [Target] | [Y/N] | [Y/N] | [Y/N] |

### Step 5: Risk Acknowledgment

Review top risks from discovery:

| Risk | Impact | Probability | Mitigation | Accepted? |
|------|--------|-------------|------------|-----------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Strategy] | [Y/N] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Strategy] | [Y/N] |

### Step 6: Final Approval

Present summary:
```
╔══════════════════════════════════════════════════════════════╗
║                    STRATEGIC ALIGNMENT GATE                   ║
╠══════════════════════════════════════════════════════════════╣
║  Vision: [One-line vision]                                   ║
║  Primary Persona: [Name]                                     ║
║  Value Proposition: [Core benefit]                           ║
║  MVP Scope: [X features]                                     ║
║  Estimated Effort: [Based on task decomposition guidance]    ║
║  Key Risks: [Top 2 risks]                                    ║
╠══════════════════════════════════════════════════════════════╣
║  Business Model: [Type]                                      ║
║  Success Metric: [Primary KPI]                               ║
║  Stakeholder Approval: [Status]                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Ready to proceed to automated development?                  ║
║                                                              ║
║  Say: "Approved, begin development" to continue              ║
║  Say: "Revise [section]" to make changes                     ║
╚══════════════════════════════════════════════════════════════╝
```

**Generate:** `.discovery/strategic-alignment.yaml`

**Completion criteria:**
- Business model validated
- Stakeholders identified
- MVP scope confirmed
- Success criteria reviewed
- Risks acknowledged
- User gives final approval

## Commands

Handle these commands during discovery:

| Command | Action |
|---------|--------|
| `discovery status` | Show current stage and progress |
| `discovery pause` | Save state and pause |
| `discovery resume` | Resume from saved state |
| `discovery restart` | Start over (keeps artifacts) |
| `skip` | Skip current question |
| `back` | Return to previous question |
| `help` | Show help for current stage |
| `example` | Show example for current question |

## Transition to Phase 3

When user approves PRD:
1. Update discovery state to complete
2. Create `.claude/.signals/phase2-complete.json`
3. Transition to Phase 3 (PRD Validation)

## Error Recovery

If user seems stuck:
- Offer to show an example
- Offer to skip and return later
- Suggest breaking down the question

If artifacts fail to load:
- Log error
- Continue without that artifact
- Note gap in discovery-log.md

## Output Files

```
docs/
├── PRD.md                    # Generated PRD
└── discovery-summary.md      # Summary of discovery process

.discovery/
├── artifacts/                # Collected reference materials
├── scope/
│   ├── boundaries.yaml       # In/out of scope
│   ├── inputs.yaml           # System inputs
│   ├── outputs.yaml          # System outputs
│   └── constraints.yaml      # Non-negotiables
├── discovery-log.md          # Full conversation transcript
└── discovery-state.json      # Progress tracking
```
