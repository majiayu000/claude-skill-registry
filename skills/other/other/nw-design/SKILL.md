---
name: nw-design
description: "Designs system architecture with C4 diagrams and technology selection. Use when defining component boundaries, choosing tech stacks, or creating architecture documents."
user-invocable: true
argument-hint: '[component-name] - Optional: --residuality --paradigm=[auto|oop|fp]'
---

# NW-DESIGN: Architecture Design

**Wave**: DESIGN (wave 3 of 6) | **Agents**: Morgan (nw-solution-architect) | **Command**: `*design-architecture`

## Overview

Execute DESIGN wave through discovery-driven architecture design. Morgan asks about business drivers and constraints first, then recommends architecture that fits. Analyzes existing codebase, evaluates open-source alternatives, produces C4 diagrams (Mermaid) as mandatory output.

## Prior Wave Consultation

Before beginning DESIGN work, read targeted prior wave artifacts:

1. **DISCOVER** (synthesis check only): Read `docs/feature/{feature-id}/discover/wave-decisions.md` — if any decision is unclear or relevant to architecture, read the referenced source file
2. **DISCUSS** (primary input): Read these key artifacts from `docs/feature/{feature-id}/discuss/`:
   - `wave-decisions.md` — decision summary
   - `requirements.md` — functional requirements
   - `acceptance-criteria.md` — testable criteria driving architecture
   - `user-stories.md` — scope of what to build
   - `story-map.md` — walking skeleton and release slicing
   - `outcome-kpis.md` — quality attributes informing architecture

DISCUSS already synthesizes DISCOVER evidence into structured requirements. DESIGN does not need raw DISCOVER artifacts (problem-validation, interview-log, etc.) unless wave-decisions.md flags something architecturally significant.

**READING ENFORCEMENT**: You MUST read every file listed in Prior Wave Consultation above using the Read tool before proceeding. After reading, output a confirmation checklist (`✓ {file}` for each read, `⊘ {file} (not found)` for missing). Do NOT skip files that exist — skipping causes architectural decisions disconnected from requirements.

After reading, check whether any DESIGN decisions would contradict DISCUSS requirements. Flag contradictions and resolve with user before proceeding. Example: DISCUSS requires "real-time updates" but DESIGN chooses batch processing — this must be resolved.

## Document Update (Back-Propagation)

When DESIGN decisions change assumptions from prior waves:
1. Document the change in a `## Changed Assumptions` section at the end of the affected DESIGN artifact
2. Reference the original prior-wave document and quote the original assumption
3. State the new assumption and the rationale for the change
4. If architecture constraints require changes to user stories or acceptance criteria, note them in `docs/feature/{feature-id}/design/upstream-changes.md` for the product owner to review

## Discovery Flow

Architecture decisions driven by quality attributes, not pattern shopping:

### Step 1: Understand the Problem
Review JTBD artifacts from DISCUSS to understand which jobs the architecture must serve. Morgan asks: What are we building? For whom? Which quality attributes matter most? (scalability|maintainability|testability|time-to-market|fault tolerance|auditability)

### Step 2: Understand Constraints
Morgan asks: Team size/experience? Timeline? Existing systems to integrate? Regulatory requirements? Operational maturity (CI/CD, monitoring)?

### Step 3: Team Structure (Conway's Law)
Morgan asks: How many teams? Communication patterns? Does proposed architecture match org chart?

### Step 3.5: Development Paradigm Selection

Morgan identifies primary language(s) from constraints, then applies:

- **FP-native** (Haskell|F#|Scala|Clojure|Elixir): recommend Functional
- **OOP-native** (Java|C#|Go): recommend OOP
- **Multi-paradigm** (TypeScript|Kotlin|Python|Rust|Swift): present both, let user choose based on team experience and domain fit

After confirmation, ask user permission to write paradigm to project CLAUDE.md:
- FP: `This project follows the **functional programming** paradigm. Use @nw-functional-software-crafter for implementation.`
- OOP: `This project follows the **object-oriented** paradigm. Use @nw-software-crafter for implementation.`

Default if user declines/unsure: OOP. User can override later.

### Step 4: Recommend Architecture Based on Drivers
Recommend based on quality attribute priorities|constraints|paradigm from Steps 1-3.5. Default: modular monolith with dependency inversion (ports-and-adapters). Overrides require evidence.

If functional paradigm selected, Morgan adapts architectural strategy:
- Types-first design: define algebraic data types and domain models before components
- Composition pipelines: data flows through transformation chains, not method dispatch
- Pure core / effect shell: domain logic is pure, IO lives at boundaries (adapters are functions)
- Effect boundaries replace port interfaces: function signatures serve as ports
- Immutable state: state changes produce new values, no mutation in the domain
These are strategic guidance items for the architecture document — no code snippets.

### Step 5: Advanced Architecture Stress Analysis (HIDDEN -- `--residuality` flag only)
When activated: apply complexity-science-based stress analysis — stressors|attractors|residues|incidence matrix|resilience modifications. See `stress-analysis` skill.
When not activated: skip entirely, do not mention.

### Step 6: Produce Deliverables
- Architecture document with component boundaries|tech stack|integration patterns
- C4 System Context diagram (Mermaid) -- MANDATORY
- C4 Container diagram (Mermaid) -- MANDATORY
- C4 Component diagrams (Mermaid) -- only for complex subsystems
- ADRs for significant decisions

## Rigor Profile Integration

Before dispatching the architect agent, read rigor config from `.nwave/des-config.json` (key: `rigor`). If absent, use standard defaults.

- **`agent_model`**: Pass as `model` parameter to Task tool. If `"inherit"`, omit `model` (inherits from session).
- **`reviewer_model`**: If design review is performed, use this model for the reviewer agent. If `"skip"`, skip design review.
- **`review_enabled`**: If `false`, skip post-design review step.

## Agent Invocation

@nw-solution-architect

Execute \*design-architecture for {feature-id}.

Context files: see Prior Wave Consultation above.

**Configuration:**
- model: rigor.agent_model (omit if "inherit")
- interactive: moderate
- output_format: markdown
- diagram_format: mermaid (C4)
- stress_analysis: {true if --residuality flag, false otherwise}

**SKILL_LOADING**: Read your skill files at `~/.claude/skills/nw-{skill-name}/SKILL.md`. At Phase 4, always load: `nw-architecture-patterns`, `nw-architectural-styles-tradeoffs`. Do NOT load `nw-roadmap-design` during DESIGN wave -- roadmap creation belongs to the DELIVER wave (`/nw-roadmap` or `/nw-deliver`). Then follow your Skill Loading Strategy table for phase-specific skills.

## Success Criteria

- [ ] Business drivers and constraints gathered before architecture selection
- [ ] Existing system analyzed before design (codebase search performed)
- [ ] Integration points with existing components documented
- [ ] Reuse vs. new component decisions justified
- [ ] Architecture supports all business requirements
- [ ] Technology stack selected with clear rationale
- [ ] Development paradigm selected and (optionally) written to project CLAUDE.md
- [ ] Component boundaries defined with dependency-inversion compliance
- [ ] C4 System Context + Container diagrams produced (Mermaid)
- [ ] ADRs written with alternatives considered
- [ ] Handoff accepted by nw-platform-architect (DEVOPS wave)

## Next Wave

**Handoff To**: nw-platform-architect (DEVOPS wave)
**Deliverables**: See Morgan's handoff package specification in agent file

## Wave Decisions Summary

Before completing DESIGN, produce `docs/feature/{feature-id}/design/wave-decisions.md`:

```markdown
# DESIGN Decisions — {feature-id}

## Key Decisions
- [D1] {decision}: {rationale} (see: {source-file})

## Architecture Summary
- Pattern: {e.g., modular monolith with ports-and-adapters}
- Paradigm: {OOP|FP}
- Key components: {list top-level components}

## Technology Stack
- {language/framework}: {rationale}

## Constraints Established
- {architectural constraint}

## Upstream Changes
- {any DISCUSS assumptions changed, with rationale}
```

This summary enables DEVOPS and DISTILL to quickly assess architecture decisions without reading all DESIGN files.

## Expected Outputs

```
docs/feature/{feature-id}/design/
  architecture-design.md       (includes C4 diagrams in Mermaid)
  technology-stack.md
  component-boundaries.md
  data-models.md
  wave-decisions.md
docs/adrs/
  ADR-NNN-*.md
CLAUDE.md (project root)   (optional: ## Development Paradigm section)
```
