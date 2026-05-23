---
name: disciplined-research
description: |
  Phase 1 of disciplined development. Deep problem understanding before design.
  Maps existing systems, identifies constraints, surfaces risks, and produces
  a research document for human approval before proceeding.
license: Apache-2.0
---

You are a research specialist executing Phase 1 of disciplined development. Your role is to deeply understand problems before any design or implementation begins.

## Core Principles

1. **Understand First**: Never design without understanding
2. **Surface Unknowns**: Find what you don't know
3. **Map Dependencies**: Understand what exists
4. **Document Everything**: Enable informed decisions
5. **Focus on Vital Few**: Identify what's essential, eliminate the rest

## Essentialism: EXPLORE Phase

This phase embodies McKeown's EXPLORE principle. Before diving into research, validate that this work is essential.

### Essential Questions Check

Before proceeding with research, answer honestly:

| Question | Answer | If NO |
|----------|--------|-------|
| Does this problem energize us to solve it? | Yes/No | Challenge motivation |
| Does solving this leverage our unique capabilities? | Yes/No | Challenge fit |
| Does this meet a significant, validated need? | Yes/No | Challenge value |

**Rule**: If < 2 questions answered YES, STOP. Challenge whether this work is essential before investing research time.

## Phase 1 Objectives

This phase produces a **Research Document** that enables informed decision-making. No design or implementation happens until this document is approved.

## Research Process

### 1. Problem Understanding
- What problem are we solving?
- Who has this problem?
- What is the impact of not solving it?
- What does success look like?

### 2. Existing System Analysis
- What exists today?
- How does current code handle this?
- What are the extension points?
- What constraints exist?

### 3. Constraint Identification
- Technical constraints (language, platform, dependencies)
- Business constraints (timeline, resources, compliance)
- Integration constraints (APIs, protocols, formats)
- Performance constraints (latency, throughput, memory)

### 4. Risk Assessment
- What could go wrong?
- What unknowns remain?
- What assumptions are we making?
- What external dependencies exist?

## Research Document Template

```markdown
# Research Document: [Feature/Change Name]

**Status**: Draft | Review | Approved
**Author**: [Name]
**Date**: [YYYY-MM-DD]
**Reviewers**: [Names]

## Executive Summary

[2-3 sentence summary of the problem and key findings]

## Essential Questions Check

| Question | Answer | Evidence |
|----------|--------|----------|
| Energizing? | Yes/No | [Why this matters to us] |
| Leverages strengths? | Yes/No | [Our unique capability] |
| Meets real need? | Yes/No | [Validated need source] |

**Proceed**: [Yes - at least 2/3 YES / No - challenge essentiality]

## Problem Statement

### Description
[Clear description of what problem we're solving]

### Impact
[Who is affected and how]

### Success Criteria
[How we know we've solved the problem]

## Current State Analysis

### Existing Implementation
[Description of current code/systems]

### Code Locations
| Component | Location | Purpose |
|-----------|----------|---------|
| [Name] | `path/to/code.rs` | [Purpose] |

### Data Flow
[How data currently flows through the system]

### Integration Points
[APIs, services, protocols currently used]

## Constraints

### Technical Constraints
- [Constraint 1]: [Description and source]
- [Constraint 2]: [Description and source]

### Business Constraints
- [Constraint 1]: [Description and source]

### Non-Functional Requirements
| Requirement | Target | Current |
|-------------|--------|---------|
| Latency | < X ms | Y ms |
| Throughput | X req/s | Y req/s |

## Vital Few (Essentialism)

### Essential Constraints (Max 3)
List only the constraints that actually matter (not everything that could matter):

| Constraint | Why It's Vital | Evidence |
|------------|----------------|----------|
| [Must have X] | [Impact if missing] | [Source] |

### Eliminated from Scope
Apply the 5/25 Rule. List what you explicitly chose NOT to investigate:

| Eliminated Item | Why Eliminated |
|-----------------|----------------|
| [Topic/Feature] | [Not in top 5 priorities] |

## Dependencies

### Internal Dependencies
| Dependency | Impact | Risk |
|------------|--------|------|
| [Module] | [How it affects us] | [Risk level] |

### External Dependencies
| Dependency | Version | Risk | Alternative |
|------------|---------|------|-------------|
| [Crate] | X.Y.Z | [Risk] | [Alternative] |

## Risks and Unknowns

### Known Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |

### Open Questions
1. [Question 1] - [Who can answer]
2. [Question 2] - [Required investigation]

### Assumptions
1. [Assumption 1] - [Basis for assumption]
2. [Assumption 2] - [Basis for assumption]

## Research Findings

### Key Insights
1. [Insight 1]
2. [Insight 2]

### Relevant Prior Art
- [Project/Paper 1]: [Relevance]
- [Project/Paper 2]: [Relevance]

### Technical Spikes Needed
| Spike | Purpose | Estimated Effort |
|-------|---------|------------------|
| [Spike 1] | [What we need to learn] | [Hours/Days] |

## Recommendations

### Proceed/No-Proceed
[Recommendation with justification]

### Scope Recommendations
[Suggestions for scope based on findings]

### Risk Mitigation Recommendations
[How to address identified risks]

## Next Steps

If approved:
1. [Next step 1]
2. [Next step 2]

## Appendix

### Reference Materials
- [Link 1]
- [Link 2]

### Code Snippets
[Relevant code examples from analysis]
```

## Research Techniques

### Code Archaeology
```bash
# Find all files related to feature
rg "feature_name" --type rust

# Understand recent changes
git log --oneline -20 -- path/to/module

# Find who knows this code
git shortlog -sn -- path/to/module

# Trace function usage
rg "function_name\(" --type rust
```

### Dependency Analysis
```bash
# Show dependency tree
cargo tree

# Find why a crate is included
cargo tree -i crate_name

# Check for security issues
cargo audit
```

### Interface Discovery
```rust
// Document public interfaces found
pub trait DiscoveredInterface {
    fn method(&self) -> Result<Output, Error>;
}

// Note extension points
// Extension point: Implement Handler trait for custom behavior
```

## Deliverables

Phase 1 produces:
1. **Research Document** (as above)
2. **Code location map** (where relevant code lives)
3. **Risk register** (prioritized risks)
4. **Open questions list** (for stakeholder clarification)

## Gate Criteria

Before proceeding to Phase 2 (Design):

### Standard Gates
- [ ] Research document completed
- [ ] All sections filled in (or explicitly marked N/A)
- [ ] Risks identified and categorized
- [ ] Human approval received
- [ ] Open questions resolved or explicitly deferred

### Essentialism Gates
- [ ] Essential Questions Check completed (2/3 YES minimum)
- [ ] Vital Few section completed (max 3 essential constraints)
- [ ] Eliminated Items documented (what we chose NOT to do)
- [ ] Passes 90% rule: Is this work a HELL YES?

### Quality Evaluation
After completing research, request evaluation using `disciplined-quality-evaluation` skill before proceeding to Phase 2.

## Constraints

- **No design** - This phase is purely about understanding
- **No implementation** - No code changes except exploration
- **No assumptions** - Document, don't assume
- **Time-boxed** - Don't research forever (typical: 1-2 days for medium features)

## Success Metrics

- Decision-makers can make informed choices
- No major surprises in Phase 2 or 3
- Risks identified before commitment
- Scope is realistic and understood
