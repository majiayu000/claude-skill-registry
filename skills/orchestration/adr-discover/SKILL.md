---
name: adr-discover
description: Discover ADR candidates across Specvital platform repositories with multi-agent collaboration
allowed-tools: Read, Write, Glob, Grep, Bash, WebFetch, Task
---

# ADR Discovery Command

Discover and prioritize ADR candidates across the Specvital platform repositories.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## Overview

Scan all Specvital platform repositories (web, core, worker, infra) to discover architectural decisions that need ADR documentation.

**Multi-Agent Collaboration Pipeline**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADR Discovery Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1: specvital-specialist                                   │
│    → Collect GitHub commit history                               │
│    → Identify missing ADRs compared to existing docs             │
│    → Summarize major changes per repository                      │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: product-strategist                                     │
│    → Prioritize ADR candidates                                   │
│    → Classify scope (Platform vs Repository level)              │
│    → Evaluate complexity and urgency                             │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: general-doc-writer                                     │
│    → Generate final list-up document                             │
│    → Format as table/list                                        │
│    → Write adr-candidates.md file                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Input Interpretation

The command accepts **natural language input**. Analyze the user's input to extract:

### Focus Keywords

If the user mentions specific topics, focus the search on those areas:

**Examples**:

- "AI spec document" → Focus on SpecView, AI integration, Gemini
- "pricing policy" → Focus on subscription, billing, plans
- "usage tracking" → Focus on quota, usage events, limits
- "domain hints" → Focus on parser hints, classification
- "worker separation" → Focus on binary separation, queue isolation

### Repository Scope

Detect if the user wants to limit scope:

- "only core" / "core repository" → Scan only specvital/core
- "web related" → Scan only specvital/web
- "cross-cutting" / "platform level" → Focus on multi-repo decisions

### Search Mode

| User Intent                                 | Behavior                      |
| ------------------------------------------- | ----------------------------- |
| Empty or broad ("find all ADR candidates")  | Full scan of all repositories |
| Specific topic ("AI spec document related") | Focused search on that topic  |
| Repository scope ("in worker repo")         | Limit to specific repository  |
| Mixed ("pricing in web and infra")          | Combined scope + topic filter |

---

## Execution Flow

### Phase 1: Discovery (specvital-specialist)

**Task tool invocation**:

```
Task(subagent_type="specvital-specialist", prompt="""
Discover ADR candidates by performing these tasks:

1. **Collect GitHub Commit History**
   - Repositories: specvital/core, specvital/worker, specvital/web, specvital/infra
   - Timeframe: Last 60 days (or as specified)
   - Use gh CLI or GitHub MCP

2. **Compare Against Existing ADRs**
   - Scan all ADRs under docs/en/adr/
   - Identify architectural decisions in commits that lack ADR documentation

3. **Output Format**
   For each candidate:
   - Title (English)
   - 제목 (한글) - 명사형 종결 사용
   - Related repositories
   - Related commits/PRs (if available)
   - Brief description (1-2 sentences)

**User Context**:
{user_input}

**Focus Areas** (if user specified topics):
{extracted_topics}
""")
```

**Discovery Patterns**:

- New technology stack adoption
- Architecture pattern changes
- API design decisions
- Data model changes
- Infrastructure configuration
- Business logic policies (pricing, usage limits, etc.)
- AI/ML related features

---

### Phase 2: Strategic Analysis (product-strategist)

**Task tool invocation**:

```
Task(subagent_type="product-strategist", prompt="""
Prioritize and classify ADR candidates:

**Input**: ADR candidate list from Phase 1

**Evaluation Criteria**:

1. **Scope**
   - Platform Level: Affects multiple repositories
   - Repository Level: Contained within single repository

2. **Complexity**
   - High: Multiple components affected, migration required
   - Medium: Specific module impact
   - Low: Simple policy/pattern documentation

3. **Urgency**
   - Urgent: Required for features currently in development
   - Normal: Technical debt reduction, documentation clarity
   - Low: Nice to have

4. **Value**
   - Decision tracking value
   - Onboarding assistance
   - Future change reference

**Output**:
For each candidate: 4-dimension evaluation + overall priority score (P1/P2/P3)
""")
```

---

### Phase 3: Documentation (general-doc-writer)

**Task tool invocation**:

```
Task(subagent_type="general-doc-writer", prompt="""
Generate ADR candidates list-up document:

**File**: adr-candidates.md at root path

**Language**: Korean (한글)

**Structure**:
# ADR 후보 목록

## 개요
- 분석 일자
- 분석 범위 (레포지토리, 기간)
- 총 후보 수

## P1 - 높은 우선순위 후보

| # | 제목 (한글) | Title (English) | 레포지토리 | 복잡도 | 긴급도 | 가치 | 근거 |
|---|-----------|-----------------|-----------|--------|--------|------|------|

## P2 - 중간 우선순위 후보

| # | 제목 (한글) | Title (English) | 레포지토리 | 복잡도 | 긴급도 | 가치 | 근거 |
|---|-----------|-----------------|-----------|--------|--------|------|------|

## P3 - 낮은 우선순위 후보

### Core 리포지토리
| # | 제목 (한글) | Title (English) | 복잡도 | 긴급도 | 가치 | 비고 |
|---|-----------|-----------------|--------|--------|------|------|

### Worker 리포지토리
| # | 제목 (한글) | Title (English) | 복잡도 | 긴급도 | 가치 | 비고 |
|---|-----------|-----------------|--------|--------|------|------|

### Web 리포지토리
| # | 제목 (한글) | Title (English) | 복잡도 | 긴급도 | 가치 | 비고 |
|---|-----------|-----------------|--------|--------|------|------|

### Infrastructure 리포지토리
| # | 제목 (한글) | Title (English) | 복잡도 | 긴급도 | 가치 | 비고 |
|---|-----------|-----------------|--------|--------|------|------|

## ADR 번호 할당 (제안)

| 우선순위 | ADR 번호 | 제목 (한글) | Title (English) |
|----------|----------|-----------|-----------------|

## 다음 단계
- [ ] 팀과 P1 우선순위 검토 및 확정
- [ ] P1 항목 ADR 작성자 지정

## 관련 커밋 요약

| 후보 | 커밋 |
|------|------|

**Style**:
- Concise table format
- Sort by priority
- ALL content in Korean (한글)
- Technical terms can include English in parentheses
""")
```

---

## Output

### Generated File

```
./adr-candidates.md   # List-up document at root path
```

---

## Key Rules

### Must Do

- Follow agent sequence: specvital-specialist → product-strategist → general-doc-writer
- Pass each agent's output as input to the next agent
- Include only items not duplicated with existing ADRs
- Apply clear priority criteria
- Generate adr-candidates.md at root path

### Must Not Do

- Skip agent phases
- Generate candidates from speculation (must be based on actual commits/changes)
- Include existing ADR duplicates
- Use unclear priorities (must specify P1/P2/P3)

---

## Usage Examples

```bash
# Full scan - discover all ADR candidates
/adr-discover

# Topic-focused search
/adr-discover AI spec document, domain hints

# Repository-scoped search
/adr-discover web repository only, focusing on frontend patterns

# Combined scope and topic
/adr-discover pricing and usage tracking across all repos

# Natural language
/adr-discover Find everything related to the new subscription system we built
```

---

## Related Commands

- `/workflow-analyze`: Feature analysis with implementation plan
- `/document-business-rule`: Business rule documentation
- `/commit`: Commit message generation

## Related Agents

- `specvital-specialist`: Specvital platform expert
- `product-strategist`: Strategic analysis specialist
- `general-doc-writer`: Documentation specialist
- `prompt-engineer`: Prompt optimization (background)
- `context-manager`: Cross-session context preservation

---

## Execution

Now execute the workflow:

1. **Parse $ARGUMENTS**: Extract topics, repository scope, and search mode
2. **Phase 1**: Invoke Task(specvital-specialist) with user context
3. **Phase 2**: Invoke Task(product-strategist) with Phase 1 output
4. **Phase 3**: Invoke Task(general-doc-writer) with Phase 2 output
5. **Report**: Confirm adr-candidates.md file creation
