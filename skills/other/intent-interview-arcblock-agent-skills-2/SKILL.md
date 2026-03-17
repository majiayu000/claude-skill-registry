---
name: intent-interview
description: Transform vague ideas into implementation-ready specifications through structured interviewing. Use when user describes a new feature/product idea, has a problem to solve, needs to document requirements, or says things like "帮我梳理需求", "interview me about this", "细化这个想法", "spec out this project". Produces two artifacts - intent.md (technical spec for code agents) and overview.md (human-friendly summary for team).
---

# Intent Interview

A structured methodology for extracting, refining, and documenting product/feature requirements through deep interviewing.

## Output Artifacts

### intent.md (for Code Agents)
Detailed technical specification with:
- Architecture design
- Data contracts and schemas
- Implementation guide with code examples
- Project structure
- Decision rationale

### overview.md (for Humans)
One-page summary with:
- Problem statement
- Core experience flow
- Architecture diagram (ASCII)
- Key decisions table
- Scope and risks

## Interview Process

### Phase 1: Problem Space
Start by understanding WHAT before HOW.

```
Questions to ask:
- What is the core problem?
- Who is the target user?
- Is this a new product or addition to existing?
- What's the priority/urgency?
```

### Phase 2: Deep Dive (Iterative)
Cover these dimensions systematically, 3-4 questions per round:

| Dimension | Key Questions |
|-----------|---------------|
| Data | Sources, contracts, validation, conflicts, authentication |
| Rendering | Cross-platform strategy, components, theming, sizing |
| Sync/Update | Real-time requirements, refresh strategy, failure handling |
| Architecture | Storage, sharing, cloud/local, offline capability |
| UX | Configuration flow, error states, feedback mechanisms |
| Edge Cases | Failures, migrations, security, low-end devices |
| Scope | MVP boundaries, what's in/out, phasing |
| Tech Stack | Languages, frameworks, existing code to reuse |

### Phase 3: Contradiction Resolution
When answers conflict with earlier choices:
1. Point out the contradiction explicitly
2. Ask for clarification with specific options
3. Update understanding accordingly

### Phase 4: Implementation Readiness Check
Before writing specs, verify:
- Can a code agent implement this without asking questions?
- Are all technical choices specified?
- Are edge cases covered?

If gaps exist, continue interviewing.

## Question Design

### Do
- Ask non-obvious, probing questions
- Probe tradeoffs ("if X fails, should we Y or Z?")
- Use concrete scenarios
- Offer 3-4 mutually exclusive options
- Match user's language (中文/English)

### Don't
- Ask yes/no questions
- Ask obvious implementation details
- Ask multiple unrelated questions at once

### Format
Use `AskUserQuestion` tool with:
- 1-4 questions per round
- 2-4 options per question
- Short header (max 12 chars)
- Clear option descriptions

## intent.md Template

```markdown
# [Project] Specification

## 1. Overview
- Product positioning
- Core concept
- Priority
- Target user
- Project scope

## 2. Architecture
- Data layer
- Rendering layer
- Key subsystems

## 3. Detailed Behavior
- Update/refresh
- Error handling
- Data processing

## 4. User Experience
- Key flows
- Configuration

## 5. Technical Implementation Guide
- Project structure
- Code examples

## 6. Decisions Summary
| Decision | Choice | Rationale |

## 7. MVP Scope
- Included
- Excluded

## 8. Risks

## 9. Open Items
```

## overview.md Template

```markdown
# [Project]: One-line description

## One sentence explanation

## Why?
Problem in plain language

## Core experience
ASCII flow diagram

## Architecture
ASCII component diagram

## Key decisions
| Question | Choice | Why |

## Scope
In / Out

## Risk + Mitigation

## Next steps
```

## Workflow

```
User describes idea
    ↓
Phase 1: Problem space (1-2 rounds)
    ↓
Phase 2: Deep dive (multiple rounds)
    ↓
Phase 3: Resolve contradictions
    ↓
Phase 4: Check readiness
    ↓ (loop if gaps)
Generate intent.md
    ↓
Ask if overview needed
    ↓
Generate overview.md
    ↓
(Optional) Push to repository
```
