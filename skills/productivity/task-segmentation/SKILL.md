---
name: task-segmentation
description: "[Task Mgmt] A Skill that segments subtasks into more granular, actionable items before starting work. AI agent MUST invoke this skill AUTOMATICALLY when moving a task to In Progress. Break down existing 2-space indented subtasks into smaller, more specific subtasks to provide clearer objectives for the agent. (user)"
---

# Task Segmentation

Segment subtasks into granular, actionable items before starting implementation.

## ⛔ CRITICAL: Every Task MUST Have Subtasks

**A task without subtasks is INCOMPLETE. AI MUST ensure every task has at least 3 specific, actionable subtasks.**

## Trigger Conditions

| Agent Action | Required Action |
|--------------|-----------------|
| **Any new task is added** | ⛔ MUST have 3+ subtasks immediately |
| Moving task to In Progress | Segment subtasks BEFORE starting work |
| Subtask is vague or broad | Break into specific implementation steps |
| Subtask takes >30 min to complete | Split into smaller units |
| **Task has no subtasks** | ⛔ STOP - Add subtasks first |

## Workflow

1. **BEFORE** moving task to Worker
2. Read the task and its subtasks
3. Analyze each subtask for granularity
4. Segment vague subtasks into specific, actionable items
5. Update the Task document with segmented subtasks
6. **THEN** move task to Worker (use `task-mover`)

## Segmentation Rules

**When to Segment:**
- Subtask description is vague (e.g., "Implement feature")
- Subtask covers multiple concerns (e.g., "Add UI and logic")
- Subtask would take significant time to complete

**When NOT to Segment:**
- Subtask is already specific and actionable
- Subtask is a single, atomic operation
- Further breakdown adds no clarity

## ⚠️ CRITICAL: Format Rules

- ALL subtasks MUST use exactly 2-space indentation
- NO deeper nesting (no 4-space or 6-space indents)
- NO intermediate grouping headers (e.g., `### Phase 1`)

## Example

**Before Segmentation:**
```
- [ ] Implement user authentication #feature !high
  - [ ] Add login functionality
  - [ ] Handle errors
```

**After Segmentation:**
```
- [ ] Implement user authentication #feature !high
  - [ ] Create login form UI component
  - [ ] Add form validation logic
  - [ ] Implement API call to auth endpoint
  - [ ] Store auth token in secure storage
  - [ ] Add loading state during auth
  - [ ] Display error message for invalid credentials
  - [ ] Handle network error with retry option
```

## Subtask Generation by Task Type

| Task Type | Required Subtask Categories |
|-----------|----------------------------|
| **New Feature** | UI 설계 → 컴포넌트 생성 → 로직 구현 → API 연동 → 에러 처리 → 테스트 |
| **Bug Fix** | 원인 분석 → 재현 확인 → 수정 코드 작성 → 엣지 케이스 확인 → 테스트 |
| **Refactoring** | 기존 코드 분석 → 새 구조 설계 → 점진적 마이그레이션 → 테스트 확인 |
| **Documentation** | 구조 파악 → 내용 작성 → 예제 추가 → 리뷰 반영 |
| **UI/UX** | 레이아웃 설계 → 컴포넌트 구현 → 스타일 적용 → 반응형 처리 → 접근성 확인 |

## More Examples

### Example: New Feature Task
```markdown
- [ ] 다크모드 토글 기능 추가 #feature #ui !medium
  - [ ] 다크모드 상태 저장 로직 구현 (UserDefaults)
  - [ ] ThemeManager 싱글톤 생성
  - [ ] 설정 화면에 토글 UI 추가
  - [ ] 색상 팔레트 다크모드 버전 정의
  - [ ] 전체 앱 테마 적용 확인
```

### Example: Bug Fix Task
```markdown
- [ ] 로그인 실패 시 크래시 버그 수정 #bug !high
  - [ ] 크래시 로그 분석 및 원인 파악
  - [ ] nil 체크 로직 추가
  - [ ] 에러 핸들링 코드 수정
  - [ ] 다양한 실패 케이스 테스트
  - [ ] 회귀 테스트 수행
```

## Pre-Segmentation Checklist

**Before saving any task, verify:**

- [ ] Task has **at least 3 subtasks**
- [ ] Each subtask uses **action verb** (Create, Implement, Add, Design, Configure, Handle)
- [ ] Each subtask is **specific and actionable** (not vague)
- [ ] Each subtask is **completable in 1-2 hours**
- [ ] Subtasks cover **all aspects** of the task (UI, Logic, Data, Integration, Testing)
- [ ] Subtasks use **exactly 2-space indentation**