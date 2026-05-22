---
name: ADR Assistant
description: Helps create, analyze, and maintain Architecture Decision Records
trigger: Creating architectural decisions, evaluating alternatives, documenting technical choices
---

# ADR Assistant Skill

I autonomously help with Architecture Decision Records when you're making architectural or technical decisions.

## When I Activate

I trigger when you're:
- Discussing technology choices
- Evaluating alternatives
- Making architectural decisions
- Documenting technical choices
- Updating existing ADRs

## What I Provide

### 1. ADR Analysis
- Review existing ADRs in `${WORKSPACE_DIR}/adr/`
- Identify related decisions
- Check for conflicts or dependencies
- Suggest improvements

### 2. ADR Creation
- Generate next ADR number (currently 0012+)
- Follow established template structure
- Research alternatives using Deepwiki
- Document consequences and tradeoffs
- Include implementation timeline

### 3. ADR Template Structure
```markdown
# NNNN. Title

Date: YYYY-MM-DD

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
- Current situation
- Pain points
- Requirements
- Drivers

## Decision
What we decided and why

## Alternatives Considered
- Alt 1: Pros/Cons/Reason for rejection
- Alt 2: ...

## Consequences
- Positive
- Negative
- Neutral
- Risks with mitigations

## Implementation
- Action items
- Timeline
- Success metrics

## References
- Links to docs, commits, related ADRs

## Notes
- Additional insights
```

### 4. Best Practices
- Use Deepwiki to research similar ADRs
- Consider 3-5 alternatives minimum
- Document concrete consequences
- Include measurable success metrics
- Link to related ADRs
- Update ADR README index

## Current ADR Index (as of 2025-11-07)

- 0001: Use Bun as Primary Package Manager
- 0002: Adopt Turbo for Monorepo Build Orchestration
- 0003: Migrate from Docker to RAILPACK for Railway Deployment
- 0004: Use PostgreSQL for Primary Database
- 0005: Adopt ElizaOS for AI Agent Framework
- 0006: Enforce TypeScript Strict Typing Standards
- 0007: Real Gameplay Testing with Playwright
- 0008: Adopt Privy HD Wallets for User Wallet Management
- 0009: Semi-Automated Asset Approval Workflow
- 0010: Meshy.ai API Integration for 3D Asset Generation
- 0011: VRM Avatar System Architecture

Next number: **0012**

## Example Usage

**User:** "Should we use GraphQL or REST for our new API?"

**Me:** *I notice you're evaluating API architecture. Let me help create ADR-0012.*

I'll:
1. Research GraphQL vs REST using Deepwiki
2. Analyze your current tech stack (Elysia, TypeScript)
3. Consider Hyperscape-specific requirements
4. Document alternatives with detailed pros/cons
5. Propose decision with implementation plan
6. Create ADR file at `adr/0012-api-architecture-choice.md`
7. Update ADR README index

## Integration with Project

- Follows ADR template from existing records
- Updates README.md index automatically
- Links to related ADRs
- Aligns with project standards (CLAUDE.md)
- Uses Deepwiki for research
