---
name: spawn-task-manager
description: 태스크 관리 작업을 task-manager-agent에 위임
allowed-tools: Task, Read
---

# Task Manager Agent 활용 가이드

태스크 파일 관리 작업을 task-manager-agent에 위임하는 방법입니다.

## 핵심 원칙

**태스크 파일 직접 수정 대신 task-manager-agent에 위임합니다.**

상태 업데이트, 테스트 결과 기록, 아카이빙 등 모든 태스크 관리 작업을 위임합니다.

## 사용 시나리오

**반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

### 1. 태스크 목록 조회

```
Task tool 호출:
  subagent_type: "task-manager-agent"
  run_in_background: true
  prompt: |
액션: list
필터: in_progress (선택적)

.claude/agents/task-manager-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 2. 태스크 상태 조회

```
Task tool 호출:
  subagent_type: "task-manager-agent"
  run_in_background: true
  prompt: |
액션: get
대상: TASK-001

.claude/agents/task-manager-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 3. 상태 업데이트

```
Task tool 호출:
  subagent_type: "task-manager-agent"
  run_in_background: true
  prompt: |
액션: update
대상: TASK-001
새 상태: pending_test

.claude/agents/task-manager-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 4. 테스트 결과 기록

```
Task tool 호출:
  subagent_type: "task-manager-agent"
  run_in_background: true
  prompt: |
액션: record_test
대상: TASK-001
테스트 결과:
  - 테스트 ID: TASK-001-T01
  - 결과: PASSED
  - 일시: 2024-01-15T14:30:00
  - 비고: 모든 케이스 통과

.claude/agents/task-manager-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 5. 내용 추가

```
Task tool 호출:
  subagent_type: "task-manager-agent"
  run_in_background: true
  prompt: |
액션: add_content
대상: TASK-001
섹션: 에이전트 결과
내용:
  ### coder_agent_result (Step 2)
  - 상태: COMPLETED
  - 수정 파일: [목록]

.claude/agents/task-manager-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 6. 아카이빙

```
Task tool 호출:
  subagent_type: "task-manager-agent"
  run_in_background: true
  prompt: |
액션: archive
대상: TASK-001

.claude/agents/task-manager-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

## 액션 목록

| 액션 | 설명 | 필수 파라미터 |
|------|------|---------------|
| list | 태스크 목록 조회 | (없음) |
| get | 특정 태스크 조회 | task_id |
| update | 상태 업데이트 | task_id, status |
| add_content | 내용 추가 | task_id, section, content |
| record_test | 테스트 결과 기록 | task_id, test_result |
| archive | 아카이빙 | task_id |

## 결과 처리

### 성공

```markdown
## task-manager-agent 결과
- 상태: COMPLETED
- 액션: update
- 대상: TASK-001
- 결과: 상태가 pending_test로 업데이트됨
```

### 실패

```markdown
## task-manager-agent 결과
- 상태: FAILED
- 액션: archive
- 대상: TASK-001
- 에러: 테스트가 완료되지 않음 (pending_test 상태)
```

## 워크플로우 통합

### 일반 작업 흐름

```
Step 완료
    ↓
task-manager-agent (상태: in_progress → completed)
    ↓
모든 Step 완료
    ↓
task-manager-agent (상태: completed → pending_test)
```

### /test-report 흐름

```
테스트 결과 수신
    ↓
task-manager-agent (record_test)
    ↓ [모든 테스트 PASSED]
task-manager-agent (archive)
```

## 주의사항

1. **아카이브 조건**: 모든 테스트가 PASSED일 때만 아카이브 가능
2. **상태 흐름**: pending → in_progress → completed → pending_test → archived
3. **실패 처리**: 아카이브 실패 시 에러 메시지 확인 후 조치

---

<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->
