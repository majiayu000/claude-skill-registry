---
name: task-add
description: "[Task Mgmt] A Skill that adds new tasks with priority tags to Docs/Task/{StepName}_Task.md documents for multi-agent parallel development. AI agent MUST invoke this skill AUTOMATICALLY when (1) discovering new work items during implementation, (2) user requests a new feature/fix, (3) breaking down a large task into subtasks, (4) identifying follow-up work after completing a task. CRITICAL - Never modify document structure, only add tasks with proper priority tags (!high, !medium, !low). Tasks should be distributed to avoid file conflicts between workers. (user)"
---

# Task Add

Add new tasks to Task documents when work items are discovered. Design tasks for parallel development across multiple workers.

## Trigger Conditions

| Agent Action | Example |
|--------------|---------|
| User requests new feature | "Add dark mode toggle" |
| Discovering bug during work | Found edge case that needs fix |
| Breaking down large task | Split into subtasks |
| Identifying follow-up work | "After this, we need to..." |

## Task Format

```markdown
- [ ] TaskTitle #tag !priority Deadline(yyyy:mm:dd)
  - [ ] Subtask 1
  - [ ] Subtask 2
  - [ ] Subtask 3
```

## ⛔ CRITICAL: Subtask is MANDATORY

**Every task MUST have at least 3 subtasks. A task without subtasks is INCOMPLETE and will be REJECTED.**

❌ **FORBIDDEN - Task without subtasks:**
```markdown
- [ ] Implement login feature #auth !high
```

✅ **REQUIRED - Task WITH subtasks:**
```markdown
- [ ] Implement login feature #auth !high
  - [ ] Design login UI layout
  - [ ] Create LoginView SwiftUI component
  - [ ] Implement form validation logic
  - [ ] Add API integration for authentication
  - [ ] Handle error states and messages
```

### Subtask Requirements

| Requirement | Rule |
|-------------|------|
| **Minimum Count** | Every task MUST have **at least 3 subtasks** |
| **Granularity** | Each subtask completable in 1-2 hours |
| **Specificity** | Use action verbs: Create, Implement, Add, Design, Configure |
| **Independence** | Each subtask independently verifiable |

### Subtask Generation by Task Type

| Task Type | Required Subtasks |
|-----------|-------------------|
| New Feature | UI 설계, 컴포넌트 생성, 로직 구현, API 연동, 에러 처리 |
| Bug Fix | 원인 분석, 수정 코드 작성, 엣지 케이스 확인, 테스트 검증 |
| Refactoring | 기존 코드 분석, 새 구조 설계, 마이그레이션, 테스트 |
| Documentation | 구조 파악, 내용 작성, 예제 추가 |

## Section Placement

| Task Type | Target Section |
|-----------|----------------|
| New feature request | Backlog |
| Bug found during work | Backlog |
| Subtask breakdown | Same section as parent |
| Follow-up work | Backlog |

## 🔀 Parallel Development Guidelines

**⚠️ CRITICAL: When adding tasks, consider parallel development:**

1. **Design for Independence**: Each task should be completable without modifying files that other tasks touch
2. **Isolate by Directory**: Prefer tasks that work in separate directories (e.g., `/Views/FeatureA/` vs `/Views/FeatureB/`)
3. **Avoid Shared File Edits**: Don't create multiple tasks that modify the same file

## Tag Reference

| Tag | Use Case |
|-----|----------|
| `#feature` | New functionality |
| `#bug` | Bug fix |
| `#refactor` | Code improvement |
| `#docs` | Documentation |
| `#test` | Testing |
| `#ui` | UI/UX work |

## Priority Reference

| Priority | Use Case | Examples |
|----------|----------|----------|
| `!high` | Urgent, blocker | Build failure, crash, critical bug |
| `!medium` | Normal priority | General feature development (default) |
| `!low` | Nice to have | Refactoring, documentation, code cleanup |

## ⚠️ CRITICAL: Format Protection

**Absolute Rules:**
- NEVER modify existing Task document structure
- ONLY add priority tags (`!high`, `!medium`, `!low`)
- NEVER change section order, table structure, or markdown format

## ⚠️ CRITICAL: Task Document Format Rules

**Strict Format Requirements:**
- Subtasks MUST use exactly 2-space indentation (no more, no less)
- NO intermediate grouping headers (e.g., `### Phase 1`, `#### Step A`) are allowed
- Task hierarchy is flat: Parent task → Subtasks (2-space indent) ONLY

## ⛔ CRITICAL: Duplicate Section Prevention

**Before ANY edit, verify document structure:**

1. **Read entire file first** - Check existing section headers
2. **Count section occurrences** - Each section (`## Backlog`, `## Worker1`, etc.) MUST appear exactly ONCE
3. **If duplicates found** - STOP and fix by merging duplicate sections
4. **Add tasks to EXISTING sections** - NEVER create new section headers

**Detection Pattern:**
```
## Review    ← First occurrence (KEEP)
...tasks...
## Done      ← First occurrence (KEEP)
...tasks...
## Review    ← DUPLICATE (REMOVE - merge tasks to first ## Review)
## Done      ← DUPLICATE (REMOVE - merge tasks to first ## Done)
```

**Fix Procedure:**
1. Identify all duplicate sections
2. Merge tasks from duplicate sections into first occurrence
3. Delete duplicate section headers and empty lines
4. Verify only ONE of each section exists

## Workflow

1. **Read entire Task file** - Verify no duplicate sections exist
2. Identify new work item
3. Determine appropriate Task file (by stage)
4. **Determine priority** (use Priority Decision Guide)
5. Format task with proper syntax including priority tag
6. **⛔ MANDATORY: Generate 3+ subtasks** - Analyze scope, break down by work type
7. **Find existing target section** (DO NOT create new section)
8. Add task WITH subtasks to section (bottom of existing section)
9. **Verify subtask count** - Must have at least 3 subtasks
10. **Before saving** - Verify no duplicate sections created
11. Save file

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `task-segmentation` | Before moving task to Worker, segment subtasks into granular items |
| `task-mover` | After adding task, move between sections as work progresses |