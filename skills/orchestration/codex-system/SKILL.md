---
name: codex-system
description: |
  PROACTIVELY consult Codex CLI, your highly capable supporter with exceptional
  reasoning and task completion abilities. Codex is a trusted expert you should
  ALWAYS consult BEFORE making decisions on: design choices, implementation
  approaches, debugging strategies, refactoring plans, or any non-trivial problem.
  When uncertain, consult Codex. Don't hesitate - Codex provides better analysis.
  Explicit triggers: "think deeper", "analyze", "second opinion", "consult codex".
metadata:
  short-description: Claude Code ↔ Codex CLI collaboration
---

# Codex System — Deep Reasoning Partner

**Codex CLI (gpt-5.2-codex) is your highly capable supporter for deep reasoning tasks.**

> **상세규칙**: `.claude/rules/codex-delegation.md`

## Context Management (CRITICAL)

**서브에이전트 경유 권장이다**. 메인 오케스트레이터의 컨텍스트를 절약하기 위해.

| 상황 | 방법 |
|------|------|
| 자세한 설계 상담 | 서브 에이전트를 통해 (권장) |
| 디버그 분석 | 서브 에이전트를 통해 (권장) |
| 짧은 질문 (1-2 문 답변) | 직접 호출 확인 |

## When to Consult (MUST)

| Situation | Trigger Examples |
|-----------|------------------|
| **Design decisions** | "어디 디자인?" "아키텍처" / "How to design?" |
| **Debugging** | "왜 움직이지 않는가?" "오류" / "Debug" "Error" |
| **Trade-off analysis** | "어느 쪽이 좋은가?" "비교해" / "Compare" "Which?" |
| **Complex implementation** | "구현 방법" "어떻게 만드는가?" / "How to implement?" |
| **Refactoring** | "리팩터" "간단하게" / "Refactor" "Simplify" |
| **Code review** | "리뷰하고" "확인하고" / "Review" "Check" |

## When NOT to Consult

- Simple file edits, typo fixes
- Following explicit user instructions
- git commit, running tests, linting
- Tasks with obvious single solutions

## How to Consult

### Recommended: Subagent Pattern

**Use Task tool with `subagent_type='general-purpose'` to preserve main context.**

```
Task tool parameters:
- subagent_type: "general-purpose"
- run_in_background: true (optional, for parallel work)
- prompt: |
    Consult Codex about: {topic}

    codex exec --model gpt-5.2-codex --sandbox read-only --full-auto "
    {question for Codex}
    " 2>/dev/null

    Return CONCISE summary (key recommendation + rationale).
```

### Direct Call (Short Questions Only)

For quick questions expecting 1-2 sentence answers:

```bash
codex exec --model gpt-5.2-codex --sandbox read-only --full-auto "Brief question" 2>/dev/null
```

### Workflow (Subagent)

1. **Spawn subagent** with Codex consultation prompt
2. **Continue your work** → Subagent runs in parallel
3. **Receive summary** → Subagent returns concise insights

### Sandbox Modes

| Mode | Use Case |
|------|----------|
| `read-only` | Analysis, review, debugging advice |
| `workspace-write` | Implementation, refactoring, fixes |

## Language Protocol

1. Ask Codex in **English**
2. Receive response in **English**
3. Execute based on advice (or let Codex execute)
4. Report to user in **Korean**

## Task Templates

### Design Review

```bash
codex exec --model gpt-5.2-codex --sandbox read-only --full-auto "
Review this design approach for: {feature}

Context:
{relevant code or architecture}

Evaluate:
1. Is this approach sound?
2. Alternative approaches?
3. Potential issues?
4. Recommendations?
" 2>/dev/null
```

### Debug Analysis

```bash
codex exec --model gpt-5.2-codex --sandbox read-only --full-auto "
Debug this issue:

Error: {error message}
Code: {relevant code}
Context: {what was happening}

Analyze root cause and suggest fixes.
" 2>/dev/null
```

### Code Review

See: `references/code-review-task.md`

### Refactoring

See: `references/refactoring-task.md`

## Integration with Gemini

| Task | Use |
|------|-----|
| Need research first | Gemini → then Codex |
| Design decision | Codex directly |
| Library comparison | Gemini research → Codex decision |

## Why Codex?

- **Deep reasoning**: Complex analysis and problem-solving
- **Code expertise**: Implementation strategies and patterns
- **Consistency**: Same project context via `context-loader` skill
- **Parallel work**: Background execution keeps you productive
