---
name: vibe-audit
description: >-
  Brutal Vibe Audit for engineering quality. Auto-activates on:
  "code review", "technical audit", "engineering quality",
  "is this production ready", "vibe check", "slop check",
  "AI-generated code", "technical due diligence",
  "can we ship this", "quality assessment"
---

# Brutal Vibe Audit

When the user questions code quality, asks for technical reviews, or wants to distinguish real engineering from AI slop, apply the 20-metric engineering audit.

## Auto-Trigger Patterns

- "Code review" or "technical audit" requests
- Questions about "production readiness"
- "Vibe check" or "slop check" on code
- Concerns about "AI-generated code" quality
- Technical due diligence needs
- Questions like "can we ship this?"
- Architecture reviews
- Security or performance concerns
- Quality assessment requests

## What This Skill Does

Scores engineering reality across 20 metrics (0-5 each, 100 total):

**Section A: Architecture & Vibe (1-5)**
1. Architectural Justification
2. Dependency Bloat
3. README vs Reality Gap
4. AI Hallucination Smell
5. Folder Structure Sanity

**Section B: Core Engineering (6-10)**
6. Error Handling Strategy
7. Concurrency Model
8. Data Structures & Algorithms
9. Memory Management
10. Type Safety & Contracts

**Section C: Performance & Scale (11-14)**
11. Critical Path Latency
12. Backpressure & Limits
13. State Management
14. Network Efficiency

**Section D: Security & Robustness (15-17)**
15. Input Validation & Trust
16. Secrets & Supply Chain
17. Observability

**Section E: QA & Operations (18-20)**
18. Test Reality
19. CI/CD & Reproducibility
20. Bus Factor & Maintainability

## Verdict Bands

- **0-40:** VIBE CODING SCRAP - Rewrite
- **41-60:** AI/JUNIOR PROTOTYPE - 70% rewrite
- **61-75:** TECHNICAL DEBT BOMB - Refactor before scaling
- **76-85:** SOLID ENGINEERING - Ship with monitoring
- **86-95:** PROFESSIONAL GRADE - Minor polish
- **96-100:** UNICORN TIER - NASA level

## When to Use

- Pre-launch technical reviews
- Code quality assessments
- Technical due diligence (M&A, investment)
- AI-generated code validation
- Architecture decisions
- Performance concerns
- Security audits

## Complementary Audits

- **Jobs Audit**: If UX/design also needs review
- **Carlin Audit**: If marketing claims need verification
- **Multi-Audit**: For comprehensive product analysis

## Invoke

Use `/vibe-audit [codebase path]` for explicit invocation.
