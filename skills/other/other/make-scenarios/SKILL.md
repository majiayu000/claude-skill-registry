---
name: make-scenarios
description: Analyze a plan or codebase to generate scenarios in "Actor wants to..." format from a stated perspective. Use when user says "make scenarios", "generate scenarios", "jeopardy requirements", or wants to identify extension points and use cases.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: make-scenarios] Generating scenarios...'"
          once: true
---

# Scenario Generation Skill

Analyze a plan, codebase, or feature description and produce scenarios — statements of what an actor wants to be able to do. Scenarios are perspective-driven: the user provides the lens (developer extensibility, end-user capability, operator workflow, security posture, etc.) and the skill discovers what scenarios matter from that perspective.

Scenarios follow the form: **"{Actor} wants to {action} {target}"**

These scenarios become input for requirements generation via `/make-req` in a separate session.

## When to Use

- User says "make scenarios", "generate scenarios", "jeopardy requirements"
- User wants to discover extension points, use cases, or capability gaps
- User wants to understand what a system should accommodate from a specific perspective

## Core Principles

- **Scenarios are perspective-dependent.** The same codebase yields different scenarios for a developer vs. an end-user vs. an operator. The user provides the perspective.
- **Scenarios state desires, not solutions.** Each scenario says what an actor wants to achieve, never how the system should enable it.
- **Scenarios are discovered, not invented.** They emerge from what the codebase or plan reveals — variation points, hardcoded assumptions, existing abstractions, domain concepts.

## Critical Constraints

**NEVER:**
- Modify any source code files
- Create files outside `temp/make-scenarios/` directory
- Prescribe solutions or approaches in scenarios
- Invent scenarios that have no basis in the analyzed material
- Mix perspectives in a single scenario (each scenario has one actor type)

**ALWAYS:**
- Require the user to state the perspective/lens before proceeding
- Use subagents for parallel exploration
- Ground every scenario in evidence from the codebase or plan
- Write output to `temp/make-scenarios/` directory

## Workflow

### Step 0: Establish Perspective

If the user has not stated a perspective, ask. Examples:

- **Developer extensibility**: "Developer wants to add/swap/extend..."
- **End-user capability**: "User wants to filter/export/customize..."
- **Operator workflow**: "Operator wants to monitor/configure/rotate..."
- **Security posture**: "Attacker wants to escalate/exfiltrate/bypass..."
- **Data analyst**: "Analyst wants to query/export/visualize..."

The perspective determines what the subagents look for and how scenarios are framed.

### Step 1: Analyze Source Material

Identify the input: a plan file, codebase area, feature description, or conversation context. Read it fully.

Launch parallel Explore subagents tailored to the stated perspective:

**For developer extensibility perspective:**
- Variation points — Where does the system parameterize behavior?
- Hardcoded assumptions — Where is the system locked to one implementation?
- Extension patterns — Base classes, registries, plugin directories, strategy patterns
- Domain entities — First-class concepts that could reasonably be added or swapped

**For end-user capability perspective:**
- User-facing behaviors — What can the user do today?
- Workflow gaps — Where does the user hit dead ends or workarounds?
- Configuration surface — What can/can't the user control?
- Output formats — What forms does data take when presented to users?

**For operator workflow perspective:**
- Deployment topology — How is the system run?
- Configuration mechanisms — What knobs exist?
- Observability — What can be monitored, what's opaque?
- Recovery paths — What happens on failure?

**For security posture perspective:**
- Trust boundaries — Where does the system validate input?
- Privilege levels — What access controls exist?
- Data exposure — What sensitive data flows where?
- Attack surface — What interfaces are externally reachable?

Adapt subagent prompts to the stated perspective. The above are examples, not exhaustive categories.

### Step 2: Identify Scenario Candidates

From subagent findings, extract candidate scenarios. For each:

1. Frame as **"{Actor} wants to {action} {target}"**
2. Note the **evidence** — what in the codebase or plan revealed this scenario
3. Note the **current state** — does the system support this partially, not at all, or fully?

Discard scenarios where the system already fully supports the capability (nothing to require).

### Step 3: Curate and Rank

- Remove duplicates and overlapping scenarios
- Rank by significance: scenarios that would require the most architectural consideration come first
- Aim for 5-15 scenarios. Fewer if the scope is narrow, more if analyzing a broad system
- Group related scenarios under thematic headings if natural groupings emerge

### Step 4: Write the Scenarios Document

Save to: `temp/make-scenarios/scenarios_{perspective}_{topic}_{YYYY-MM-DD_HHMMSS}.md`

```markdown
# Scenarios: {Topic}

**Date:** {YYYY-MM-DD}
**Source:** {What was analyzed — plan name, codebase area, or description}
**Perspective:** {The stated perspective/lens}

## Overview
{One paragraph: what these scenarios describe, the perspective used, and their intended use as input for requirements generation}

---

## {Thematic Group 1} (if grouping applies)

### SCEN-001: {Actor} wants to {action} {target}
**Evidence:** {What in the codebase/plan revealed this}
**Current state:** {Not supported | Partially supported | Hardcoded to single implementation}

### SCEN-002: {Actor} wants to {action} {target}
**Evidence:** {…}
**Current state:** {…}

---

## {Thematic Group 2}

### SCEN-003: {Actor} wants to {action} {target}
**Evidence:** {…}
**Current state:** {…}

---

{Repeat for each scenario}
```

**Numbering:** Sequential across the entire document (SCEN-001 through SCEN-NNN).

### Step 5: Provide Follow-Up Instructions

After writing the file, output to terminal:

```
Scenarios written to: temp/make-scenarios/scenarios_{perspective}_{topic}_{timestamp}.md

Review and edit the scenarios file — remove any you don't want requirements for.
Then in a new session, run /make-req with the scenarios file as input.
```

## Output Quality Checks

Before finalizing, verify:

- Every scenario names a specific actor and a specific desire
- Every scenario has evidence grounded in the analyzed material
- No scenario prescribes a solution or technology
- Scenarios are framed from the stated perspective consistently
- A reader could take any single scenario and understand what capability is being described without reading the others
