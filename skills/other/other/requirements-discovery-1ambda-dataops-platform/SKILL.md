---
name: requirements-discovery
description: Stakeholder interview and requirements elicitation. Discovers hidden needs, surfaces contradictions, and produces structured specifications. Use when gathering requirements, conducting discovery interviews, or writing PRDs/feature specs.
---

# Requirements Discovery

Structured stakeholder discovery to uncover requirements, surface contradictions, and produce comprehensive specifications.

## When to Use

- New feature requirement gathering
- Stakeholder discovery interviews
- PRD/Feature specification writing
- Business requirements analysis
- Trade-off decision documentation
- Scope definition and non-goals clarification

## Context Gathering Workflow

```
# 1. Business/Market Context (Primary - Always First)
WebSearch("{feature} industry best practices 2025")
WebSearch("{competitor} {feature} implementation")

# 2. Past Decisions & Learnings
claude-mem.search(query="{feature_domain}", project="<project>")

# 3. Existing Specifications
Read: project-*/features/*_FEATURE.md
Read: docs/architecture.md

# 4. Technical Context (Secondary - When Relevant)
serena.read_memory("project_overview")
serena.list_memories()
```

## Key Principle

> **PM/PO discovers the "Why" and "What". Engineering discovers the "How".**

Focus on:
- Business value and user needs
- Success metrics and acceptance criteria
- Constraints and trade-offs

Avoid:
- Implementation details
- Code architecture decisions
- Technical solution design

---

## The 5 Discovery Phases

```
┌───────────────────────────────────────────────┐
│  Phase 1: PROBLEM SPACE                       │
│  "What problem are we really solving?"        │
├───────────────────────────────────────────────┤
│  Phase 2: USER & STAKEHOLDER                  │
│  "Who benefits and who is impacted?"          │
├───────────────────────────────────────────────┤
│  Phase 3: SOLUTION SCOPE                      │
│  "What's in, what's explicitly out?"          │
├───────────────────────────────────────────────┤
│  Phase 4: CONSTRAINTS & TRADE-OFFS            │
│  "What limits us and what choices must we make?"│
├───────────────────────────────────────────────┤
│  Phase 5: SUCCESS & RISKS                     │
│  "How do we know we succeeded?"               │
└───────────────────────────────────────────────┘
```

---

## Interview Techniques

### The "5 Whys" Technique

Drill down to root cause by asking "Why?" repeatedly:

```
User: "We need a dashboard."
You:  "Why do you need a dashboard?"
User: "To see metrics."
You:  "Why do you need to see those metrics?"
User: "To catch problems early."
You:  "Why do problems go unnoticed today?"
User: "Alerts are noisy and ignored."
→ Root Problem: Alert fatigue, NOT missing dashboards
```

### Quantifying Vague Requirements

Transform vague statements into measurable criteria:

| Vague | Probe | Quantified |
|-------|-------|------------|
| "Fast" | P50 latency target? Peak load degradation? | < 100ms P50, < 500ms P99 |
| "Secure" | Data classification? Audit needs? | PII, SOC2 audit trail |
| "Scalable" | Expected users? Growth rate? | 10K users, 50% QoQ growth |
| "Reliable" | Uptime SLA? MTTR target? | 99.9% uptime, < 15min MTTR |
| "Easy to use" | User proficiency? Task completion? | Junior dev, < 5 min setup |

### Surfacing Policy Contradictions

Identify conflicting requirements BEFORE they become bugs:

```
"You mentioned users can delete data anytime (Rule A),
 but also maintain 7-year audit trails (Rule B).
 These conflict—which takes precedence?"

"You want the API public (Rule A),
 but it contains competitive intelligence (Rule B).
 How do we reconcile this?"
```

### The "3 AM Test"

Test error handling and user self-service:

```
"Imagine a user encounters this error at 3 AM with no support.
 What information would let them self-diagnose and resolve it?"
```

### The "Worst Case" Scenario

Surface risk and failure modes:

```
"What's the worst thing that could happen if this goes wrong?"
"If we had to roll this back, what's the exit strategy?"
"What would make users NOT adopt this feature?"
```

---

## Question Templates by Phase

### Phase 1: Problem Space

| Focus | Question |
|-------|----------|
| Root Problem | "What user pain or business gap does this address? Share a specific incident." |
| Current State | "How are users solving this today? What's broken about that?" |
| Impact of Inaction | "If we don't build this, what happens in 6 months?" |
| Success Vision | "Imagine this is wildly successful. What does that look like?" |

### Phase 2: Users & Stakeholders

| Focus | Question |
|-------|----------|
| Primary Users | "Who uses this daily? What's their technical proficiency?" |
| Affected Parties | "Who else is impacted even if they don't use it directly?" |
| Conflicting Needs | "If User A wants X and User B wants Y, which wins?" |
| Adoption Barriers | "What would make users NOT adopt this?" |

### Phase 3: Solution Scope

| Focus | Question |
|-------|----------|
| Must-Have | "If we could only ship ONE thing, what is it?" |
| Non-Goals | "What are we consciously NOT solving in this version?" |
| Boundaries | "What's the maximum scale this needs to handle?" |
| Integration | "What existing systems does this touch?" |

### Phase 4: Constraints & Trade-offs

| Focus | Question |
|-------|----------|
| Speed vs Quality | "Shipping fast vs polished—where's the balance?" |
| Consistency vs Flexibility | "Standard everywhere or user-configurable?" |
| Build vs Buy | "Is there an existing solution we should leverage?" |
| Breaking Changes | "Can we break backward compatibility? When?" |

### Phase 5: Success & Risks

| Focus | Question |
|-------|----------|
| Success Metrics | "After 30 days, what number tells us this worked?" |
| Failure Indicators | "What signals would tell us this is failing?" |
| Risk Scenarios | "What's the worst-case scenario?" |
| Rollback Plan | "If we need to undo this, what's the exit strategy?" |

---

## Domain-Specific Questions

### CLI/Developer Tools

- "Should this be scriptable (flags only) or interactive (prompts)?"
- "What's the output format for piping to other tools?"
- "If run twice with identical input, should it be idempotent?"
- "What works offline without server connection?"

### APIs/Services

- "When this API version breaks, how do clients migrate?"
- "For large result sets, cursor-based or offset-based pagination?"
- "In batch operations, fail-all-on-error or partial-success?"
- "Rate limiting: per-user, per-API-key, or global?"

### Data/Analytics

- "Is eventual consistency acceptable? Max staleness?"
- "What's the data retention policy? Auto-deletion rules?"
- "Which fields contain PII? Anonymization requirements?"
- "When schema changes, how is historical data migrated?"

### User-Facing Features

- "What's the user's mental model for this workflow?"
- "How does this integrate with existing navigation?"
- "What's the accessibility requirement (WCAG 2.1 AA/AAA)?"
- "What's the mobile/responsive requirement?"

---

## Output: *_FEATURE.md Structure

**IMPORTANT**: Follow existing document conventions. If existing docs are Korean, write in Korean.

```markdown
# FEATURE: {기능 이름}

> **Version:** 1.0.0
> **Status:** Draft
> **Last Updated:** {YYYY-MM-DD}

---

## 1. 개요
### 1.1 목적
### 1.2 핵심 원칙
### 1.3 주요 기능
### 1.4 유사 도구 참조

## 2. 아키텍처 / 설계
### 2.1 컴포넌트 관계
### 2.2 핵심 결정 사항

## 3. Use Cases
### 3.1 Use-case 1: {이름}
### 3.2 Edge Cases

## 4. 인터페이스 설계 (CLI/API)
### 4.1 커맨드/엔드포인트 구조
### 4.2 옵션/파라미터

## 5. 데이터 모델

## 6. 에러 처리

## 7. 구현 우선순위
### Phase 1 (MVP)
### Phase 2

## Appendix: 결정 사항 (인터뷰 기반)
```

---

## Quality Checklist

### Completeness
- [ ] Problem statement is specific, not vague
- [ ] Success metrics are quantified
- [ ] Non-goals are explicitly stated
- [ ] All user stories have acceptance criteria

### Clarity
- [ ] No TBD/TODO items remaining
- [ ] Acronyms defined in glossary
- [ ] Edge cases have defined behavior
- [ ] Error messages are user-actionable

### Consistency
- [ ] No policy contradictions
- [ ] Trade-offs explicitly documented
- [ ] Priorities clear (must-have vs nice-to-have)

### Feasibility
- [ ] Technical constraints validated
- [ ] Dependencies identified
- [ ] Risks have mitigation plans

---

## Anti-Patterns to Avoid

| Anti-Pattern | Risk | Better Approach |
|--------------|------|-----------------|
| Accepting first answer | Misses root cause | Use "5 Whys" |
| Skipping non-goals | Scope creep | Explicitly document exclusions |
| Vague metrics | Can't verify success | Quantify with numbers |
| Solution-first | Wrong problem solved | Exhaust problem space first |
| Ignoring conflicts | Politics later | Surface and resolve in discovery |
| Technical details | Overconstrains eng | State constraints, not implementation |

---

## Workflow Summary

```
1. Context Gathering (Silent)
   └─ WebSearch, claude-mem, existing docs

2. Discovery Interview (4-6 Rounds)
   └─ AskUserQuestion with 3-4 questions each
   └─ Probe deeper on vague answers
   └─ Surface contradictions immediately

3. Synthesis
   └─ Draft *_FEATURE.md
   └─ Highlight open questions

4. Validation
   └─ Review with stakeholder
   └─ Resolve open questions
   └─ Confirm priorities

5. Finalization
   └─ Quality checklist pass
   └─ Commit to features/ directory
```
