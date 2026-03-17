---
name: brainstorm-proof-of-concept-plan
description: Use when requirements specify risky technical assumptions, unfamiliar APIs, or complex integrations before implementing full features - creates sequential POC plans with parallel research validation, design documentation, and risk mitigation for incremental confidence building
---

# Brainstorm Proof-of-Concept Plan

## Overview

Transform risky requirements into validated POC plans through parallel research, risk prioritization, and sequential validation. Use after design is complete but technical assumptions remain unproven.

**Core principle:** Validate riskiest assumptions first with minimal code, data-driven decisions, and clear go/no-go criteria.

## When to Use

**Use this skill when:**
- Design complete (via brainstorming skill) but technical risks remain
- Requirements specify unfamiliar technologies or untested integrations
- Multiple competing approaches need validation (algorithm choice, library selection)
- Team needs confidence before committing to full implementation

**Don't use for:**
- Proven technologies with known patterns
- Design exploration (use brainstorming skill instead)
- Implementation planning (use writing-plans skill instead)

## Workflow Position

```text
brainstorming (design) → brainstorm-proof-of-concept-plan (validation) → writing-plans (implementation)
```

## The Process

**Use TodoWrite to track each step:**

### 1. Identify Riskiest Assumptions

Review requirements and extract technical risks:
- Unfamiliar APIs or libraries
- Performance requirements without proof
- Integration patterns never attempted
- Competing technology choices (OT vs CRDT, REST vs GraphQL)

**Prioritize by:**
- Technical uncertainty (how much unknown)
- Architectural impact (affects other decisions)
- Failure cost (cost of discovering late)

### 2. Elicit Implicit Risks from User

Requirements often miss hidden assumptions. Use AskUserQuestion:

```typescript
AskUserQuestion({
  questions: [{
    question: "Which risks should POC prioritize? I recommend [X] because [Y].",
    header: "POC Priority",
    multiSelect: false,
    options: [
      { label: "Risk A First", description: "Foundation for others..." },
      { label: "Risk B First", description: "Highest uncertainty..." },
      { label: "All Sequentially", description: "Validate each in order..." },
      { label: "Research First", description: "Need investigation before deciding..." }
    ]
  }]
})
```

**Why:** User may have domain knowledge that changes priority ("We already validated X, focus on Y").

### 3. Launch Parallel Research Agents (Agents Write Own Reports)

**Critical:** Each research agent writes its own report file. Main agent does NOT write research reports.

For 3+ research areas, dispatch Task agents simultaneously:

```typescript
// Each agent writes directly to design-docs/research/
Task({
  subagent_type: "general-purpose",
  prompt: `Research VitePress WebSocket integration patterns.

**Output:** Write findings to design-docs/research/vitepress-websocket-integration.md

**Format:**
# VitePress WebSocket Integration Research

**Research Date:** YYYY-MM-DD
**Sources:** [URLs]

## Key Findings
- Finding (Source: URL)

## Implications for POC
- What this means

## Recommendation
[Data-driven choice]

**Use elements-of-style:writing-clearly-and-concisely skill for writing.**`
})
```

**Launch 3-4 agents in parallel:**
- Current system analysis (existing code/config)
- Technology comparison (Library A vs B)
- API/integration patterns (how others solved this)
- Performance characteristics (benchmarks, limitations)

**Why parallel:** 4x speed, each produces focused brief with citations.

**Never:** Write research reports yourself. Always delegate to Task agents.

### 4. Synthesize Research Findings

After research agents complete:
- Read all reports from design-docs/research/
- Identify common themes and conflicting recommendations
- Prepare synthesis for POC design decisions

**You synthesize, but agents wrote the reports.**

### 5. Design Sequential POCs (Document ALL POCs)

**Critical:** Document the COMPLETE POC strategy, not just the first POC.

Break validation into phases that build on each other:

**Example:**
- **POC-1:** Layout Override + Width Validation (foundation)
- **POC-2:** File-Based Diff Loading (build on POC-1)
- **POC-3:** TOC Integration in Left Nav (build on POC-2)

**For the FIRST POC only:**
Create detailed design with:
- Goal (what we're validating)
- Success criteria (quantitative metrics)
- Timeline (days, not weeks)
- Implementation details (enough to build)
- Deliverable (working code or measurements)
- Go/no-go decision (proceed, pivot, or stop)

**For REMAINING POCs:**
Document high-level:
- Goal (what risk it validates)
- Why it comes after previous POC (dependency)
- Rough timeline

**Why:** Complete strategy shows big picture. Detailed design for POC-1 enables immediate implementation.

### 6. Write POC Design Document

**Location:** Same folder as whiteboard/requirements documents

**Naming pattern:** Append `-poc{{N}}-{{short-slug}}` to the base filename
- Example: If requirements file is `diff-view-monaco-requirements.md`
- POC-1 becomes: `diff-view-monaco-poc1-validate-diff-view-builds.md`
- POC-2 becomes: `diff-view-monaco-poc2-props-and-theme.md`

**Required sections:**
- **Problem** (what risks we're validating)
- **Approach** (why this approach) - **MUST cite requirements, research, or external sources**
- **Complete POC Strategy** (ALL planned POCs with brief descriptions)
- **Architecture** (detailed for POC-N being built) - **MUST cite requirements for each design decision**
- **Success Metrics** (how we'll measure)
- **Implementation Details** (enough to build POC-N)
- **Risk Mitigation** (what if it fails)
- **Out of Scope** (what we're NOT validating) - **MUST link to requirement IDs**
- **References** (link to research/ files and external sources)

**Citation Requirements:**
Every design decision MUST be backed by:
- Requirements document links: `[FR-2.1](./requirements-file.md#^FR2-1)`
- Research document links: `[Research](./research/topic-research.md)`
- External sources: `[Source](https://url)` with full URL

**Format:** Use markdown links with anchors for requirement references. Use relative paths `./` for same-folder files.

**Example "Complete POC Strategy" section:**

```markdown
## Complete POC Strategy

### POC-1: Layout Override and Width Validation (This Document)
**Goal:** Prove we can disable right sidebar and achieve 600px+ per diff pane
**Timeline:** 2-3 days
**Status:** Detailed design below

### POC-2: File-Based Diff Loading
**Goal:** Validate SystemPromptDiff can load content from file paths
**Dependencies:** Requires POC-1 layout working
**Timeline:** 1-2 days
**Status:** Future

### POC-3: TOC Integration in Left Sidebar
**Goal:** Merge page TOC into left navigation sidebar
**Dependencies:** Requires POC-1 and POC-2 complete
**Timeline:** 3-4 days
**Status:** Future
```

**Required:** Use elements-of-style:writing-clearly-and-concisely skill for design doc.

## Integration with Other Skills

**Before this skill:**
- **brainstorming** - Complete design with unproven assumptions

**After this skill:**
- **writing-plans** - Create implementation plan once POC validates approach

**During this skill:**
- **elements-of-style:writing-clearly-and-concisely** - Required for all documentation (by both main agent and research agents)
- **Task tool** - Dispatch parallel research agents who write their own reports

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "I'll write research reports myself" | Agents write their own reports. You synthesize. Delegate. |
| "Just document POC-1, others are future work" | Document complete strategy. Detailed design for POC-1 only. |
| "Parallel research is overkill" | Parallel = 4x speed with focused briefs. Always use for 3+ areas. |
| "User already specified risks" | User lists known risks. AskUserQuestion surfaces hidden ones. |
| "Documentation structure doesn't matter" | Same-folder location enables discovery. Always follow naming pattern. |
| "Writing skill slows me down" | Concise docs save implementation time. Required for all reports. |
| "POC planning is too formal" | POC without plan = random prototyping. Structure prevents waste. |
| "Citations are obvious from context" | Future readers need explicit links. Always cite requirements/research/sources. |
| "I'll add citations later" | Design decisions without citations = unverifiable claims. Add during writing. |
| "General approach doesn't need citations" | Every design choice needs backing. Cite requirements or research for all decisions. |

## Success Criteria

POC plan succeeds when you can answer:
1. Which risks need validation (prioritized list)
2. What sequence to validate them (complete POC strategy with ALL identified POCs)
3. How to measure success for POC-1 (quantitative criteria)
4. What to build for POC-1 (minimal scope with implementation details)
5. What to do if it fails (pivot options)

All answers backed by research with citations (written by research agents).

## Quick Reference

| Step | Action | Tool | Who Writes |
|------|--------|------|------------|
| Identify risks | Extract from requirements | Analysis | You |
| Prioritize | Matrix (uncertainty × impact × cost) | Judgment | You |
| Elicit hidden risks | Ask which matters most | AskUserQuestion | You |
| Research | 3+ areas simultaneously | Task (parallel) | **Agents write reports** |
| Synthesize | Read reports, find themes | Read tool | You |
| Design POCs | ALL POCs + detailed POC-1 | docs/plans/ | You |
| Validate | Build minimal code, measure | Next step | Future |

## Real-World Impact

**Speed:** Parallel research saves hours compared to serial investigation.

**Quality:** Research citations (from agent reports) enable verification.

**Clarity:** Complete POC strategy prevents "what comes next?" confusion.

**Delegation:** Research agents write reports while you orchestrate and synthesize.
