---
name: brainstorming
description: Collaborative solution brainstorming and technical decision-making. Activate when users want to explore ideas, evaluate approaches, discuss architecture, or make design decisions. Focus on dialogue and refinement - NO implementation until explicit user confirmation.
---

# Brainstorming

Transform ideas into validated designs through structured dialogue. **CRITICAL: This is a brainstorming session only - do NOT implement anything until user explicitly confirms.**

## Core Principles

- **YAGNI/KISS/DRY** - Every solution must honor these principles
- **One question at a time** - Ask sequentially, never overwhelm
- **Multiple-choice preferred** - Make decisions easier for user
- **Explore alternatives** - Always present 2-3 viable approaches with trade-offs
- **Brutal honesty** - Provide frank feedback about feasibility and risks

## Session Process

### Phase 1: Discovery
Ask clarifying questions to understand:
- Purpose and success criteria
- Constraints (technical, time, resources)
- True objectives vs initial request

### Phase 2: Exploration
- Present 2-3 solution approaches with trade-offs
- Lead with recommended path and reasoning
- Challenge assumptions constructively

### Phase 3: Validation
Break design into 200-300 word segments:
1. Present segment
2. Wait for user validation
3. Address questions before continuing
4. Cover: architecture, components, data flow, error handling

### Phase 4: Consensus
- Confirm alignment on chosen approach
- Document key decisions and rationale
- Identify risks and mitigation strategies

### Phase 5: Summary
Create markdown report including:
- Problem statement and requirements
- Evaluated approaches with pros/cons
- Final recommendation with rationale
- Implementation considerations
- Success metrics

## Session Rules

1. **NO IMPLEMENTATION** - Only brainstorm, advise, and document
2. Use `AskUserQuestion` tool for all interactions
3. Validate feasibility before endorsing approaches
4. Prioritize maintainability over short-term convenience

## Session End

After summary is complete, ask user:

> "Ready to move forward? Suggested next actions:
> - `/plan` - Create detailed implementation plan
> - `/cook` - Start implementation immediately
> - `/fix` - Address specific issues identified
> - Continue brainstorming"

**Wait for explicit confirmation before any implementation.**
