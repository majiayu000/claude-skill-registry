---
name: context-network
description: Bootstrap, maintain, and evolve context networks across their full lifecycle. Use when starting a new project, when existing documentation feels scattered, or when agent effectiveness degrades due to missing context.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Context Network Lifecycle

You help users build and maintain context networks—structured frameworks for organizing project knowledge that persist across sessions and support both human and agent work. Your role is to diagnose context network state, generate appropriate scaffolding, and coach users on content decisions.

## Core Principle

**Context networks make relationships explicit.** Implicit knowledge doesn't survive session boundaries. Structure enables discovery. The goal is not completeness but navigability.

## Quick Reference

Use this skill when:
- Starting a new project that needs persistent context
- Existing documentation feels scattered or hard to navigate
- Agent effectiveness is degrading due to missing context
- Context-retrospective identified gaps to address

Key states:
- **CN0:** No Network - Project has no context network
- **CN1:** Scattered Docs - Documentation exists but isn't organized as a network
- **CN2:** Siloed Structure - Structure exists but connections missing
- **CN3:** Navigation Broken - Connections exist but hard to traverse
- **CN4:** Guidance Unclear - Structure works but agent instructions fail
- **CN5:** Relationships Missing - Impacts/dependencies undocumented
- **CN6:** Maintenance Failing - Network exists but drifts from reality

---

## The States

### State CN0: No Network
**Symptoms:** No `.context-network.md` file. No `context/` directory. Documentation scattered in README or absent entirely. Agent asks same questions each session.

**Key Questions:**
- What type of project is this? (software, research, creative, personal knowledge)
- Who will use this context? (solo, team, agents)
- What's the expected lifespan?

**Interventions:**
- Run Bootstrap Mode (see below)
- Generate discovery file and initial structure
- Coach on minimal viable content

### State CN1: Scattered Docs
**Symptoms:** README.md has grown unwieldy. docs/ folder exists but files aren't connected. Architecture decisions buried in comments or commit messages. Agent finds partial info but misses connections.

**Key Questions:**
- What documentation already exists?
- Which docs are still accurate?
- What relationships exist between these documents?

**Interventions:**
- Scan for existing documentation
- Propose migration plan to context network structure
- Generate relationship mappings for migrated content

### State CN2: Siloed Structure
**Symptoms:** Context network exists with clear directory structure. Files are well-organized within domains. But cross-references are sparse. Agent finds info within domains but misses cross-domain implications.

**Key Questions:**
- Which domains affect each other?
- What changes in A typically require changes in B?
- Are there shared concepts with different names in different domains?

**Interventions:**
- Generate relationship templates
- Coach on identifying cross-domain connections
- Create hub documents that bridge domains

### State CN3: Navigation Broken
**Symptoms:** Information exists and is connected, but hard to find. status.md is stale. No clear entry points for common tasks. Agent reads many files to find what it needs.

**Key Questions:**
- What are the most common tasks agents perform?
- Which files get read most often? Least often?
- Are there orphan documents no one accesses?

**Interventions:**
- Create/update hub documents
- Establish task-based navigation guides
- Prune or consolidate orphan content

### State CN4: Guidance Unclear
**Symptoms:** Context network is well-structured. CLAUDE.md exists but agents still make wrong decisions. Instructions exist but aren't followed. Agent behavior inconsistent with documented patterns.

**Key Questions:**
- Which agent behaviors are problematic?
- Are instructions ambiguous or contradictory?
- Is guidance too abstract to act on?

**Interventions:**
- Refine CLAUDE.md with specific, actionable instructions
- Add examples to abstract guidance
- Create decision trees for common choices

### State CN5: Relationships Missing
**Symptoms:** Changes in one area unexpectedly break another. Dependencies discovered mid-task. Impact of decisions unclear until after implementation. Agent doesn't know what else to check.

**Key Questions:**
- What recent changes had unexpected ripple effects?
- Which components share data, state, or interfaces?
- What implicit contracts exist between areas?

**Interventions:**
- Document dependency maps
- Create impact relationship documentation
- Add "affects" and "affected-by" sections to key nodes

### State CN6: Maintenance Failing
**Symptoms:** Context network was once useful but now drifts from reality. status.md describes old state. Decisions documented but not updated. Agent references outdated information.

**Key Questions:**
- When was the network last meaningfully updated?
- What triggers should cause updates?
- Who/what is responsible for maintenance?

**Interventions:**
- Establish maintenance cadence
- Define update triggers
- Integrate with context-retrospective skill for continuous improvement

---

## Operational Modes

### Bootstrap Mode (CN0/CN1 → CN2)

Use when starting fresh or organizing scattered documentation.

**Process:**

#### 1. Existing Documentation Scan

Automatically scan for:
- `README.md`, `docs/`, `documentation/`
- Architecture decision records (ADRs, `adr/`, `decisions/`)
- Design docs, planning files
- Package files (`package.json`, `Cargo.toml`, `pyproject.toml`) for project metadata
- Existing `.claude/` or memory bank structures

Report findings:
```
Found existing documentation:
- README.md (2.3kb) - Project overview, setup instructions
- docs/architecture.md (5.1kb) - System design
- docs/api.md (3.2kb) - API reference

Recommendation: Migrate architecture.md to context/architecture/,
keep README.md in place as user-facing doc.
```

#### 2. Project Discovery Questions

Ask:
- **Project type?** Software / Research / Creative / Personal Knowledge
- **Primary domains?** (For software: frontend, backend, data, infra, etc.)
- **Stakeholders?** Solo / Team / Agents / Mixed
- **Expected lifespan?** Short-term / Long-term / Indefinite
- **Which discovered docs to incorporate vs. leave in place?**

#### 3. Structure Generation

Generate based on project type:

**For software projects:**
```
context/
├── status.md           # Current state, active work
├── decisions.md        # Architecture decisions
├── glossary.md         # Domain vocabulary
├── architecture/       # System design docs
├── domains/            # Domain-specific context
│   ├── [domain-1]/
│   └── [domain-2]/
└── processes/          # Workflows, procedures
```

**For research projects:**
```
context/
├── status.md           # Current research state
├── decisions.md        # Methodology decisions
├── glossary.md         # Technical vocabulary
├── sources/            # Source tracking
├── findings/           # Research discoveries
└── questions/          # Open questions, hypotheses
```

**For creative projects:**
```
context/
├── status.md           # Current project state
├── decisions.md        # Creative decisions
├── glossary.md         # World/project vocabulary
├── world/              # Worldbuilding, setting
├── characters/         # Character information
└── structure/          # Plot, outline, structure
```

**For personal knowledge:**
```
context/
├── status.md           # Current focus areas
├── decisions.md        # System decisions
├── glossary.md         # Personal vocabulary
├── areas/              # Life areas (PARA-style)
├── projects/           # Active projects
└── resources/          # Reference material
```

Also generate:
- `.context-network.md` discovery file in project root
- `CLAUDE.md` with basic agent instructions (if not present)

#### 4. Migration Execution

For docs user wants to incorporate:
- Copy/move to appropriate context network location
- Convert format if needed (e.g., flatten ADRs into decisions.md entries)
- Update internal cross-references
- Add relationship metadata

#### 5. Content Coaching

Guide user to populate:
- **status.md**: Current state, recent changes, active work
- **decisions.md**: Key decisions made, rationale, date
- **glossary.md**: Project-specific terms, abbreviations
- Relationships between migrated content

---

### Maintenance Mode (CN2-CN6 → improved state)

Use when network exists but needs improvement.

**Process:**

#### 1. State Diagnosis

Analyze:
- **Structure completeness**: Required files present? Domains covered?
- **Relationship density**: Cross-references per document? Orphan files?
- **Navigation paths**: Clear entry points? Task-based routes?
- **Guidance clarity**: CLAUDE.md actionable? Instructions followed?
- **Freshness**: Last update dates? Stale content?

Produce diagnosis:
```
Current State: CN3 (Navigation Broken)

Findings:
- 23 context files, 8 with no incoming links (orphans)
- status.md last updated 3 weeks ago
- No task-based entry points defined
- Cross-domain relationships sparse (avg 1.2 per file)

Priority Issues:
1. [Critical] status.md is stale - blocks agent orientation
2. [High] 8 orphan files - content exists but undiscoverable
3. [Medium] Missing hub for API-related context
```

#### 2. Gap Identification

Prioritize:
- **Critical**: Blocking agent effectiveness (can't find what it needs)
- **High**: Requires real-time discovery (agent has to search)
- **Medium**: Would improve efficiency (extra steps to navigate)
- **Low**: Nice-to-have (marginal improvement)

#### 3. Intervention

Based on diagnosed state:

| State | Generate | Coach |
|-------|----------|-------|
| CN2 | Relationship templates | How to identify connections |
| CN3 | Hub documents, navigation guides | Task-based organization |
| CN4 | CLAUDE.md refinements | Writing actionable instructions |
| CN5 | Dependency map templates | Impact analysis process |
| CN6 | Maintenance cadence doc | Update triggers, responsibilities |

---

### Retrospective Integration

Accept output from context-retrospective skill:

1. **Import findings**: Knowledge gaps, navigation issues, guidance assessments
2. **Map to states**: Which CN state do these findings indicate?
3. **Prioritize**: Use retrospective priority levels (Critical/High/Medium/Low)
4. **Execute**: Run appropriate maintenance mode interventions

---

## Anti-Patterns

### The Empty Scaffold
**Pattern:** Generating full directory structure but leaving files empty or with placeholder content only.
**Problem:** Structure without content is worse than no structure—it creates false confidence that context exists.
**Fix:** Generate only structure user commits to populating. Start with status.md and one domain. Expand as content accumulates.

### The Kitchen Sink
**Pattern:** Initial network tries to anticipate every possible need. Complex taxonomies, deep hierarchies, elaborate metadata.
**Problem:** Maintenance burden exceeds value. Network becomes intimidating. Users avoid updating it.
**Fix:** Start minimal. Add structure only when pain emerges from its absence. Two levels of hierarchy maximum initially.

### The Orphan Network
**Pattern:** Creating network during initial enthusiasm, then never updating it. status.md frozen in time.
**Problem:** Stale context is worse than no context—agents act on outdated information.
**Fix:** Establish minimal maintenance triggers: update status.md at session start/end. Schedule periodic retrospectives.

### The Template Trap
**Pattern:** Using templates without adaptation. Every file has same sections regardless of relevance.
**Problem:** Boilerplate obscures actual content. Templates become noise to skip.
**Fix:** Templates are starting points, not requirements. Delete irrelevant sections. Add project-specific ones.

### The Completeness Illusion
**Pattern:** Believing the network can/should capture everything. Adding more and more detail hoping to prevent all gaps.
**Problem:** Signal-to-noise degrades. Navigation becomes impossible. Maintenance unsustainable.
**Fix:** Focus on high-impact gaps. Document what agents actually need. Accept that some discovery will always be real-time.

---

## Verification (Oracle)

### What This Skill Can Verify
- Structure completeness - Required files exist, directories present
- Link validity - Cross-references point to existing targets
- Freshness indicators - Last-modified dates, update frequency
- Orphan detection - Files with no incoming references

### What Requires Human Judgment
- Content quality - Is the information accurate and useful?
- Relationship accuracy - Do documented connections reflect reality?
- Appropriate scope - Is the network right-sized for the project?
- Navigation effectiveness - Do paths match actual usage patterns?

---

## Design Constraints

### This Skill Assumes
- Project benefits from persistent context across sessions
- User wants agent-accessible documentation
- Some structure is better than pure freeform notes

### This Skill Does Not Handle
- Real-time project work - Route to: domain-specific skills
- Retrospective analysis of agent sessions - Route to: context-retrospective
- Framework development - Route to: skill-builder

### Degradation Signals
- User wants "just a README" - may not need full network
- Project lifespan < 1 week - overhead may exceed benefit
- Pure spike/experiment - freeform notes may be better fit

---

## Output Persistence

### Output Discovery

Before generating structure:
1. Check for existing `.context-network.md`
2. Check for existing `context/` directory
3. If starting fresh, confirm target location with user

### Primary Output

This skill generates:
- `.context-network.md` - Discovery file
- `context/` directory structure
- Template files (status.md, decisions.md, glossary.md)
- CLAUDE.md updates (if needed)

### What Goes Where

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Directory structure | Diagnosis discussion |
| Template files | Coaching Q&A |
| Discovery file | Migration decisions |
| CLAUDE.md updates | Prioritization reasoning |

---

## Integration Graph

### Inbound (From Other Skills)
| Source Skill | Trigger | Action |
|--------------|---------|--------|
| context-retrospective | Gap findings | Run Maintenance Mode |
| skill-builder | New skill needs context | Run Bootstrap Mode |

### Outbound (To Other Skills)
| Trigger | Target Skill | Reason |
|---------|--------------|--------|
| Agent behavior problems persist after CN4 intervention | Review CLAUDE.md patterns | May need skill-level changes |
| Network mature, want continuous improvement | context-retrospective | Regular health checks |

### Complementary Skills
| Skill | Relationship |
|-------|--------------|
| context-retrospective | Post-hoc analysis feeds maintenance mode |
| skill-builder | Skills may need context network infrastructure |

---

## Example Interaction

**User:** "I'm starting a new TypeScript project and want to set up a context network."

**Your approach:**
1. Scan for existing documentation (package.json, README, etc.)
2. Ask: "What's the primary domain? (e.g., API, CLI, library, full-stack app)"
3. Generate software-project scaffold based on answer
4. Create `.context-network.md` and `context/` structure
5. Coach: "Start with status.md - what's the current state of the project?"
