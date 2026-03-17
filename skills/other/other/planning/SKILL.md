---
name: planning
description: Transform ideas into actionable implementation plans. Combines Socratic questioning for requirements discovery with detailed task breakdown for zero-context engineers. Use before any feature development.
allowed-tools: Read, Glob, Grep, Edit, Write, AskUserQuestion
license: MIT
metadata:
  author: obra/superpowers
  version: "2.0"
---

# Planning

아이디어를 구체적인 구현 계획으로 발전시키는 통합 스킬입니다.

## Phase 1: Discovery (Brainstorming)

### Socratic Process

```
1. 핵심 목표 파악
   - "이것이 해결하려는 문제가 무엇인가요?"
   - "성공을 어떻게 측정할 수 있나요?"

2. 제약 조건 탐색
   - "반드시 지켜야 할 제약이 있나요?"
   - "기술적/비즈니스적 한계는?"

3. 대안 탐색
   - 최소 3가지 접근법 도출
   - 각 접근법의 장단점 분석
```

### Output: Discovery Summary

```markdown
## Discovery Summary

### 핵심 요구사항
- [필수 요구사항 목록]

### 기술적 결정사항
- [합의된 접근법]

### 열린 질문
- [추가 탐색 필요 항목]
```

---

## Phase 2: Plan Writing

### Core Principle

> **"가정: 엔지니어가 코드베이스 컨텍스트가 전혀 없음"**

### Plan Structure

```markdown
# [Feature Name] Implementation Plan

## Goal
[한 문장 목표]

## Tech Stack
- Framework: [프레임워크]
- Dependencies: [의존성]

## File Structure
[영향받는 파일 목록]
```

### Bite-sized Tasks (각 2-5분)

```markdown
## Task 1: [태스크명]

### Files
- `src/feature/file.ts` (신규/수정)

### Test First
[테스트 코드]

### Implementation
[구현 코드]

### Commit
```bash
git commit -m "feat(scope): description"
```
```

---

## Workflow

```
Discovery → Plan → Execute

┌────────────────┐
│  Brainstorm    │ ← 요구사항 도출
└───────┬────────┘
        ▼
┌────────────────┐
│  Write Plan    │ ← 태스크 분해
└───────┬────────┘
        ▼
┌────────────────┐
│  Execute       │ ← TDD 사이클
└────────────────┘
```

## Plan Storage

```
docs/plans/YYYY-MM-DD-<feature-name>.md
```

## Checklist

### Discovery 완료

- [ ] 핵심 목표 명확
- [ ] 제약 조건 파악
- [ ] 접근법 결정

### Plan 완료

- [ ] 모든 파일 경로 정확
- [ ] 각 태스크 2-5분 분량
- [ ] 테스트 코드 포함
- [ ] 커밋 메시지 작성됨
