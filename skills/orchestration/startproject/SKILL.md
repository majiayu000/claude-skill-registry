---
name: startproject
description: |
  Start a new project/feature implementation with multi-agent collaboration.
  Includes multi-session review workflow for quality assurance.
metadata:
  short-description: Project kickoff with multi-agent collaboration
---

# Start Project

**멀티 에이전트 협업으로 프로젝트를 시작한다.**

## Overview

이 스킬은 3개의 에이전트(Claude, Codex, Gemini)를 협조시켜 프로젝트 개시부터 구현후 리뷰까지를 커버한다.

## Workflow

```
Phase 1: Research (Gemini via Subagent)
    ↓
Phase 2: Requirements & Planning (Claude)
    ↓
Phase 3: Design Review (Codex via Subagent)
    ↓
Phase 4: Task Creation (Claude)
    ↓
Phase 5: CLAUDE.md Update (Claude)
    ↓
[Implementation...]
    ↓
Phase 6: Multi-Session Review (New Session + Codex)
```

---

## Phase 1: Gemini Research (Background)

**Task tool에서 하위 에이전트를 시작하고 Gemini에서 리포지토리 분석한다.**

```
Task tool parameters:
- subagent_type: "general-purpose"
- run_in_background: true
- prompt: |
    Research for: {feature}

    1. Call Gemini CLI:
       gemini -p "Analyze this repository for: {feature}

       Provide:
       1. Repository structure and architecture
       2. Relevant existing code and patterns
       3. Library recommendations
       4. Technical considerations
       " --include-directories . 2>/dev/null

    2. Save full output to: .claude/docs/research/{feature}.md

    3. Return CONCISE summary (5-7 bullet points)
```

---

## Phase 2: Requirements Gathering (Claude)

**사용자에게 질문하여 요구 사항을 명확히 한다.**

Ask in Korean:

1. **목적**: 무엇을 달성하고 싶습니까?
2. **스코프**: 포함하거나 제외하는 것은?
3. **기술적 요건**: 특정 라이브러리, 제약은?
4. **성공기준**: 완료의 판단기준은?

**Draft implementation plan based on Gemini research + user answers.**

---

## Phase 3: Codex Design Review (Background)

**Task tool에서 하위 에이전트를 시작하고 Codex에서 계획 검토한다.**

```
Task tool parameters:
- subagent_type: "general-purpose"
- run_in_background: true
- prompt: |
    Review plan for: {feature}

    Draft plan: {plan from Phase 2}

    1. Call Codex CLI:
       codex exec --model gpt-5.2-codex --sandbox read-only --full-auto "
       Review this implementation plan:
       {plan}

       Analyze:
       1. Approach assessment
       2. Risk analysis
       3. Implementation order
       4. Improvements
       " 2>/dev/null

    2. Return CONCISE summary:
       - Top 3-5 recommendations
       - Key risks
       - Suggested order
```

---

## Phase 4: Task Creation (Claude)

**서브에이전트 요약을 통합하고 작업 목록을 작성한다.**

Use TodoWrite to create tasks:

```python
{
    "content": "Implement {specific feature}",
    "activeForm": "Implementing {specific feature}",
    "status": "pending"
}
```

---

## Phase 5: CLAUDE.md Update (IMPORTANT)

**프로젝트 관련 정보를 CLAUDE.md에 추가한다.**

Add to CLAUDE.md:

```markdown
---

## Current Project: {feature}

### Context
- Goal: {1-2 sentences}
- Key files: {list}
- Dependencies: {list}

### Decisions
- {Decision 1}: {rationale}
- {Decision 2}: {rationale}

### Notes
- {Important constraints or considerations}
```

**This ensures context persists across sessions.**

---

## Phase 6: Multi-Session Review (Post-Implementation)

**구현 완료 후 다른 세션에서 리뷰를 실시한다.**

### Option A: New Claude Session

1. Start new Claude Code session
2. Run: `git diff main...HEAD` to see all changes
3. Ask Claude to review the implementation

### Option B: Codex Review (via Subagent)

```
Task tool parameters:
- subagent_type: "general-purpose"
- prompt: |
    Review implementation for: {feature}

    1. Run: git diff main...HEAD
    2. Call Codex CLI:
       codex exec --model gpt-5.2-codex --sandbox read-only --full-auto "
       Review this implementation:
       {diff output}

       Check:
       1. Code quality and patterns
       2. Potential bugs
       3. Missing edge cases
       4. Security concerns
       " 2>/dev/null

    3. Return findings and recommendations
```

### Why Multi-Session Review?

- **Fresh perspective**: New session has no bias from implementation
- **Different context**: Can focus purely on review, not implementation details
- **Codex strength**: Deep analysis without context pollution

---

## User Confirmation

Present final plan to user (in Korean):

```markdown
## 프로젝트 계획 : {feature}

### 조사 결과 (Gemini)
{Key findings - 3-5 bullet points}

### 설계 정책 (Codex 검토)
{Approach with refinements}

### 작업 목록 ({N}개)
{Task list}

### 위험과 주의사항
{From Codex analysis}

### 다음 단계
1. 이 계획으로 진행하시겠습니까?
2. 구현 완료 후 다른 세션에서 검토를 수행한다.

---
이 계획으로 진행하시겠습니까?
```

---

## Output Files

| File | Purpose |
|------|---------|
| `.claude/docs/research/{feature}.md` | Gemini research output |
| `CLAUDE.md` | Updated with project context |
| Task list (internal) | Progress tracking |

---

## Tips

- **All Codex/Gemini work through subagents** to preserve main context
- **Update CLAUDE.md** to persist context across sessions
- **Use multi-session review** for better quality assurance
- **Ctrl+T**: Toggle task list visibility
