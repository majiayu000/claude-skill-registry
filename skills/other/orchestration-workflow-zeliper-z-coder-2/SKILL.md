---
name: orchestration-workflow
description: /orchestrate 커맨드의 상세 워크플로우 가이드. 모든 Phase 처리 및 sub-agent spawn 전략
allowed-tools: Task, TaskOutput, Read, AskUserQuestion, EnterPlanMode, TodoWrite
---

# 오케스트레이션 워크플로우

/orchestrate 커맨드가 작업을 효율적으로 처리하기 위한 상세 워크플로우입니다.

---

## 금지 사항 (엄격히 준수)

**/orchestrate는 절대로 직접 검색/코드 작성을 하지 않습니다:**

### 1. 직접 검색 금지
- Search, Glob, Grep 직접 사용 금지
- Read로 코드 파일 탐색 금지 (config.json, task 파일만 허용)
- **반드시 codebase-search-agent, reference-agent를 Task tool로 spawn**

### 2. 직접 코드 작성 금지
- Write, Edit 직접 사용 금지
- **반드시 coder-agent를 Task tool로 spawn**

### 3. 직접 문서 작성 금지
- Write로 .md 파일 직접 작성 금지
- **반드시 markdown-writer-agent를 Task tool로 spawn**

### 4. 할 수 있는 것
- config.json, task 파일 읽기 (Read)
- Task tool로 sub-agent spawn
- TaskOutput으로 결과 수신
- AskUserQuestion, EnterPlanMode 사용
- TodoWrite로 진행 상황 관리

**위반 시 agent chain이 작동하지 않습니다.**

---

## 작업 유형별 에이전트 매핑

| 작업 유형 | 사용할 에이전트 |
|---------|--------------|
| 코드 탐색/분석 | codebase-search-agent |
| 레퍼런스 검색 | reference-agent |
| 외부 정보 검색 | web-search-agent |
| 코드 작성/수정 | coder-agent |
| 빌드/테스트 | builder-agent |
| 커밋 생성 | commit-agent |
| 문서/계획 작성 | markdown-writer-agent |
| 복잡한 판단 | decision-agent |
| 태스크 관리 | task-manager-agent |

---

## 모드 선택 (작업 시작 전)

### Plan Mode (계획 검토 필요 시)

작업 시작 전에 계획을 검토하고 싶다면:
1. 정보 수집 완료 후 계획 작성
2. 사용자에게 계획 제시 및 승인 요청
3. 승인 후 Execute Mode로 전환

**Plan Mode 진입 조건:**
- 사용자가 명시적으로 "계획 먼저 보여줘" 요청
- 복잡한 작업 (다수 파일 수정, 아키텍처 변경)
- 파괴적 변경 (삭제, 대규모 리팩토링)
- 다중 구현 방식 존재
- 요구사항이 모호함

### Execute Mode (기본)

계획 검토 없이 바로 실행:
- 단순한 작업
- 사용자가 신뢰 표시한 경우
- 명확한 요구사항

### 모드 전환 흐름

```
┌─────────────────────────────────────────────────────────┐
│                    Execute Mode                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 자동 실행: spawn → 결과 수신 → 다음 작업        │    │
│  └─────────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────────┘
                     │ [입력 필요 감지]
                     ▼
┌─────────────────────────────────────────────────────────┐
│                     Plan Mode                            │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 1. 상황 정리 및 옵션 제시                        │    │
│  │ 2. AskUserQuestion 또는 계획 작성                │    │
│  │ 3. 사용자 응답/승인 대기                         │    │
│  └─────────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────────┘
                     │ [사용자 응답 수신]
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    Execute Mode                          │
│  사용자 결정 반영하여 작업 재개                          │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: 초기화 및 정보 수집

### 1.1 설정 확인
1. `.claude/config.json` 읽기
2. 프로젝트 설정 및 커스텀 에이전트 목록 확인
3. `tasks/` 폴더에서 진행중인 task 파일 확인

### 1.2 검색 에이전트 병렬 Spawn

새 태스크인 경우 **동시에** Task tool 호출 (단일 메시지에서 여러 Task tool):

```
Task tool #1:
  subagent_type: "codebase-search-agent"
  run_in_background: true
  prompt: "프로젝트 코드에서 관련 코드를 찾아주세요..."

Task tool #2:
  subagent_type: "reference-agent"
  run_in_background: true
  prompt: "레퍼런스/예제 코드를 찾아주세요..."

Task tool #3: (필요시)
  subagent_type: "web-search-agent"
  run_in_background: true
  prompt: "외부 정보를 검색해주세요..."

Task tool #4: (config.json에 등록된 경우)
  subagent_type: "{custom_agent}"
  run_in_background: true
  prompt: "..."
```

### 1.3 작업 계획 수립

결과 수신 후:
1. `todo-list-agent` spawn → 작업 분해
2. task 파일 생성 (`./tasks/TASK-{ID}.md`)
3. 결과를 task 파일에 기록

---

## Phase 2: Step 실행 루프

### Step 실행 흐름

```
FOR each Step in task.steps:
  IF step.status == 'completed': CONTINUE

  1. coder-agent 백그라운드 spawn → Step 작업
  2. 결과 수신 후 USER_INPUT_REQUIRED 확인
  3. builder-agent 백그라운드 spawn → 빌드/테스트

  IF 빌드 실패:
    - LESSONS_LEARNED.md 업데이트
    - 재시도 (최대 3회)
    - 3회 실패 시 사용자 보고

  IF 빌드 성공:
    - commit-agent spawn → [TASK-ID] 형식 커밋
    - test-case-agent spawn → 테스트 케이스 생성
    - step.status = 'completed'
    - 결과 기록

  Step 완료 보고
```

### 빌드 실패 처리

1. 에러 메시지 분석
2. LESSONS_LEARNED.md 확인 및 업데이트
3. coder-agent에 수정 지시
4. 최대 3회 재시도
5. 3회 실패 시 사용자에게 보고 및 입력 요청

### 빌드 성공 후 처리

#### 커밋 생성
`commit-agent` spawn:
- 커밋 메시지: `[TASK-ID] Description`
- 변경된 파일만 커밋
- 민감 정보 파일 제외

#### 테스트 케이스 생성
`test-case-agent` spawn:
- `./Test/[TASK-ID-TXX] Description.md` 생성
- Step 내용 기반 테스트 항목 도출
- 수동 테스트 가이드 작성

---

## Phase 3: 테스트 대기

모든 Step 완료 시:

```
모든 Step 완료
    ↓
Task 상태: pending_test
    ↓
사용자에게 안내:
"테스트를 실행하고 결과를 보고해주세요:
/test-report TASK-001-T01 {결과}"
```

---

## Phase 4: 마무리

### 아카이브 조건 (모든 조건 충족 필요)
- 모든 Step: completed
- 모든 테스트: PASSED

### 테스트 통과 후

```
/test-report 성공 수신
    ↓
task-manager-agent → 결과 기록
    ↓
archive-task.py hook → 파일 이동
    ↓
완료 보고
```

archive-task.py 실행 결과:
- task 파일 → `tasks/archive/`
- 테스트 파일 → `Test/Archive/`

---

## USER_INPUT_REQUIRED 처리

### Sub Agent 입력 요청 형식

Sub Agent가 사용자 입력이 필요할 때 결과에 포함:

```markdown
## {agent-name} 결과
- 상태: PENDING_INPUT
- USER_INPUT_REQUIRED:
  - type: "choice" | "confirm" | "plan"
  - reason: "{입력이 필요한 이유}"
  - options: ["{선택지1}", "{선택지2}", ...] (choice인 경우)
  - context: "{추가 컨텍스트}"
```

### input_type별 처리

| input_type | 행동 |
|------------|------|
| choice | AskUserQuestion (선택지 제시) |
| confirm | AskUserQuestion (예/아니오) |
| plan | EnterPlanMode (상세 계획 필요) |

### 처리 흐름

```
Sub Agent 결과 수신
  ↓
USER_INPUT_REQUIRED 플래그 확인
  ↓
[있음] → input_type 확인
         ├─ "choice"   → AskUserQuestion (선택지 제시)
         ├─ "confirm"  → AskUserQuestion (예/아니오)
         └─ "plan"     → EnterPlanMode (상세 계획 필요)
  ↓
[없음] → Execute Mode 유지 → 다음 작업 진행
```

### 입력 요청 처리 예시

**예시 1: coder-agent가 구현 방식 선택 요청**
```
coder-agent 결과:
  - 상태: PENDING_INPUT
  - USER_INPUT_REQUIRED:
    - type: "choice"
    - reason: "인증 방식 선택 필요"
    - options: ["JWT", "Session", "OAuth2"]
    - context: "현재 프로젝트에 인증 시스템 없음"

/orchestrate 행동:
  → AskUserQuestion 호출
  → 선택지: JWT, Session, OAuth2
  → 사용자 선택 수신
  → coder-agent에 결과 전달하여 작업 재개
```

**예시 2: 직접 판단**
```
사용자 요청: "성능 최적화해줘"

/orchestrate 판단:
  → 범위가 모호함 (DB? API? 프론트?)
  → AskUserQuestion 호출
  → 질문: "어떤 영역을 최적화할까요?"
  → 선택지: ["데이터베이스 쿼리", "API 응답 속도", "프론트엔드 렌더링", "전체"]
```

### Task 파일 기록

모든 사용자 상호작용은 task 파일에 기록:

```markdown
## User Interactions

### [2024-01-15 10:30] 입력 요청 #1
- 요청 출처: coder-agent (Step 2)
- 유형: choice
- 질문: "인증 방식 선택 필요"
- 선택지: ["JWT", "Session", "OAuth2"]
- **사용자 응답**: JWT
- 처리 결과: coder-agent에 전달, Step 2 재개

### [2024-01-15 11:00] 입력 요청 #2
- 요청 출처: /orchestrate (직접)
- 유형: confirm
- 질문: "기존 인증 코드를 삭제할까요?"
- **사용자 응답**: 예
- 처리 결과: 삭제 진행
```

---

## Spawn 형식

### 절대 금지: Bash로 claude 명령어 실행

**다음은 절대 하지 마세요:**
- `claude --agent {agent-name}`
- `claude task --subagent {agent-name}`
- Bash tool로 claude CLI 실행

**반드시 Task tool (function call)을 사용하세요.**

### 올바른 Spawn 방법

Task tool을 function call로 호출합니다. 파라미터:
- `subagent_type`: 에이전트 이름 (예: "codebase-search-agent")
- `prompt`: 작업 지시 문자열
- `run_in_background`: true (백그라운드 실행)
- `description`: 짧은 설명

**예시: codebase-search-agent spawn**

| 파라미터 | 값 |
|---------|-----|
| subagent_type | "codebase-search-agent" |
| description | "코드베이스 분석" |
| run_in_background | true |
| prompt | "프로젝트 코드에서 관련 코드를 찾아주세요..." |

### 병렬 Spawn

여러 에이전트를 동시에 spawn하려면 **단일 응답에서 여러 Task tool 호출**을 합니다.

동시에 호출할 에이전트:
1. codebase-search-agent (프로젝트 코드 분석)
2. reference-agent (예제/템플릿 탐색)
3. web-search-agent (필요시)

---

## 중복 방지 로직

```
task 파일에 {agent_name}_result 섹션이 존재하면 해당 에이전트 spawn 하지 않음
```

---

## Skills 참조

| Skill | 용도 |
|-------|------|
| **spawn-search-agents** | 검색 에이전트 활용법 (codebase, reference, web) |
| **spawn-coder** | coder-agent 위임 가이드 |
| **spawn-builder** | builder-agent 위임 가이드 |
| **spawn-commit** | commit-agent 위임 가이드 (빌드 성공 후 커밋) |
| **spawn-test-case** | test-case-agent 위임 가이드 (테스트 케이스 생성) |
| **spawn-task-manager** | task-manager-agent 위임 가이드 (태스크 관리) |
| **spawn-orchestration-update** | orchestration-update-agent 위임 가이드 (시스템 업데이트) |
| **spawn-decision** | decision-agent 위임 가이드 (복잡한 판단) |
| **spawn-markdown-writer** | markdown-writer-agent 위임 가이드 (비정형 마크다운) |
| **markdown-templates** | 정형 마크다운 템플릿 사용 가이드 |

### 외부 도구 Skills

config.json의 `enabled_skills`에 등록된 Skills 확인:
- 해당 기능이 필요한 작업은 관련 Skill 참조
- 예: ilspy Skill (디컴파일), npm Skill (패키지 관리)

---

<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->
