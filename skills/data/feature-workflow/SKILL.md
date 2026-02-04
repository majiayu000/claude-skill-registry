---
name: feature-workflow
description: |
  일반적인 기능 구현을 위한 단계별 워크플로우를 제공합니다.
  .ai/tasks/ 디렉토리 구조를 사용하여 작업을 체계적으로 관리합니다.

  새 기능 구현 시:
  - 워크플로우를 이용, 기능 구현, 기능 개발, 기능 추가, 새 기능, 신규 개발
  - 기능 구현해줘, 기능 개발해줘, 구현해줘
  - feature, implement, new feature, add feature

  작업 재개 시 (티켓 번호 패턴: XXXX-NNN 형식):
  - TASK-001 이어서, AI-TOOLKIT-001 진행, PROJ-001 계속, FEAT-123 시작
  - 작업 이어서, 작업 계속, 작업 진행, 다음 단계, 이어서 해줘
  - resume, continue, proceed, next step

  .ai/tasks 관련:
  - .ai/tasks 확인, 작업 상태, task status, 진행 상황
license: MIT
metadata:
  author: ai-toolkit
  version: '1.0.0'
  category: workflow
allowed-tools: Bash Read Write Edit Glob Grep
---

# Feature Workflow Implementation

기능 구현을 체계적으로 진행하는 5단계 워크플로우입니다.

## 핵심 원칙

1. **Context Isolation**: 각 Step은 새 대화에서 실행 권장
2. **Human in the Loop**: 사용자 입력 확인 후 진행
3. **Document as Interface**: Step 간 통신은 문서로 수행
4. **Git as History**: 각 Step 완료 시 커밋으로 체크포인트 생성

## 규칙 로드

**각 Step 시작 시 반드시 규칙을 로드하세요:**

1. [assets/rules/AGENTS.md](assets/rules/AGENTS.md) 읽기 (규칙 인덱스)
2. **필수 규칙**: `MUST/workflow-rule.md` 항상 로드
3. **도메인 규칙**: 작업 컨텍스트에 따라 동적 로드

```
Step 시작
    │
    ├─→ MUST/workflow-rule.md (항상)
    │
    └─→ 작업 컨텍스트에 따라:
        ├─ React 작업 → react/AGENTS.md
        ├─ 테스트 작업 → testing/AGENTS.md
        ├─ API 작업 → api/AGENTS.md
        └─ (디렉토리 없으면 건너뛰기)
```

## 워크플로우 개요

```
Step 1: Requirements    → 요구사항 분석 및 정리
Step 2: System Design   → 설계 및 구현 계획 수립
Step 3: Task Analysis   → 구현 작업 분해 및 병렬화 계획
Step 4: Implementation  → 코드 구현 및 테스트
Step 5: Review          → 검토 및 문서화
```

| Step | 역할                 | 입력                        | 출력                        | 상세                                         |
| ---- | -------------------- | --------------------------- | --------------------------- | -------------------------------------------- |
| 1    | Requirements Analyst | 00-user-prompt.md           | 10-output-plan.md           | [references/step-1.md](references/step-1.md) |
| 2    | System Designer      | 10-output-plan.md           | 20-output-system-design.md  | [references/step-2.md](references/step-2.md) |
| 3    | Task Analyzer        | 10+20                       | 30-output-task.md + todos/  | [references/step-3.md](references/step-3.md) |
| 4    | Developer            | 20-output-system-design.md  | 40-output-implementation.md | [references/step-4.md](references/step-4.md) |
| 5    | Reviewer             | 40-output-implementation.md | 50-output-review.md         | [references/step-5.md](references/step-5.md) |

---

## 시작하기

### 새 작업 시작

1. **Task ID 결정**: 사용자에게 요청 (예: `PROJ-001`)
2. **Task 초기화**: `./scripts/task.sh init <TASK_ID>`
3. **입력 작성**: `.ai/tasks/<TASK_ID>/00-user-prompt.md` 편집
4. **규칙 로드**: [assets/rules/AGENTS.md](assets/rules/AGENTS.md) 읽기
5. **Step 1 실행**: [references/step-1.md](references/step-1.md) 참조

### 작업 재개

**사용자가 `.ai/tasks/<TASK_ID>/` 경로를 언급하거나 "작업 이어서" 요청 시:**

1. **status.yaml 읽기**:

   ```bash
   cat .ai/tasks/<TASK_ID>/status.yaml
   ```

2. **현재 상태 파악**:
   - `current_step`: 현재 진행 중인 Step
   - `steps.<step-N>.status`: 각 Step의 상태 (pending/in_progress/completed)

3. **규칙 로드**:
   - [assets/rules/AGENTS.md](assets/rules/AGENTS.md) 읽기
   - 해당 Step의 필수 규칙 섹션 로드

4. **다음 동작 결정**:
   - 현재 Step의 status가 `pending` → 해당 Step 시작
   - 현재 Step의 status가 `in_progress` → 계속 진행
   - 현재 Step의 status가 `completed` → 다음 Step으로 이동

5. **사용자에게 안내**:

   ```
   📍 현재 상태: Step X (상태)
   📋 완료된 Step: Step 1, Step 2, ...
   ▶️  다음 Step: Step Y

   Step Y를 시작하시겠습니까?
   ```

**수동 재개 명령어**:

```
"<TASK_ID> 작업 이어서 진행해줘"
"<TASK_ID> Step 2 시작"
"<TASK_ID> 다음 단계 계속"
```

---

## Step 상세 가이드

각 Step의 상세 내용은 아래 참조 문서를 확인하세요:

### Step 1: Requirements Analysis

- **역할**: Requirements Analyst
- **목표**: 사용자 요구사항을 명확히 이해하고 구조화된 문서로 정리
- **입력**: `.ai/tasks/<TASK_ID>/00-user-prompt.md`
- **출력**: `.ai/tasks/<TASK_ID>/10-output-plan.md`
- **완료 조건**: 출력 파일 생성 + Git 커밋
- **상세**: [references/step-1.md](references/step-1.md)

### Step 2: Design & Planning

- **역할**: System Designer
- **목표**: 요구사항을 기반으로 구현 가능한 설계 및 계획 수립
- **입력**: `.ai/tasks/<TASK_ID>/10-output-plan.md`
- **출력**: `.ai/tasks/<TASK_ID>/20-output-system-design.md`
- **완료 조건**: 출력 파일 생성 + Git 커밋
- **상세**: [references/step-2.md](references/step-2.md)

### Step 3: Task Analysis

- **역할**: Task Analyzer
- **목표**: 설계를 작은 구현 작업으로 분해하고 병렬화 계획 수립
- **입력**:
  - `.ai/tasks/<TASK_ID>/10-output-plan.md` (요구사항)
  - `.ai/tasks/<TASK_ID>/20-output-system-design.md` (설계)
- **출력**:
  - `.ai/tasks/<TASK_ID>/30-output-task.md`
  - `.ai/tasks/<TASK_ID>/todos/00-TASK_MASTER.md`
  - `.ai/tasks/<TASK_ID>/todos/01-TASK.md`, `02-TASK.md`, ...
- **완료 조건**: 모든 출력 파일 생성 + Git 커밋
- **상세**: [references/step-3.md](references/step-3.md)

### Step 4: Implementation

- **역할**: Coordinator (Task Executor Agent 조율)
- **목표**: Task Executor Agent를 활용하여 설계에 따라 코드를 구현하고 테스트
- **입력**:
  - `.ai/tasks/<TASK_ID>/20-output-system-design.md`
  - `.ai/tasks/<TASK_ID>/30-output-task.md`
  - `.ai/tasks/<TASK_ID>/todos/*.md`
- **출력**: `.ai/tasks/<TASK_ID>/40-output-implementation.md` + 실제 코드
- **완료 조건**:
  1. `todos/` 내 모든 서브태스크 completed
  2. `40-output-implementation.md` 생성됨
  3. Git 커밋 완료
- **상세**: [references/step-4.md](references/step-4.md)

### Step 5: Review & Documentation

- **역할**: Reviewer
- **목표**: 구현 결과 검토, 문서화, PR 준비
- **입력**: `.ai/tasks/<TASK_ID>/40-output-implementation.md`
- **출력**: `.ai/tasks/<TASK_ID>/50-output-review.md`
- **완료 조건**: 출력 파일 생성 + PR 생성/준비 + Git 커밋
- **상세**: [references/step-5.md](references/step-5.md)

---

## 진행 상태 확인

```bash
./scripts/task.sh status <TASK_ID>
./scripts/task.sh list
```

---

## 템플릿 및 리소스

- **출력 템플릿**: [assets/templates/](assets/templates/)
  - `00-user-prompt.md` - 초기 요구사항 입력
  - `10-output-plan.md` - Step 1 출력
  - `20-output-system-design.md` - Step 2 출력
  - `30-output-task.md` - Step 3 출력
  - `40-output-implementation.md` - Step 4 출력
  - `50-output-review.md` - Step 5 출력
  - `TASK_MASTER.md` - 전체 조율 문서 템플릿
  - `TASK.md` - 개별 서브태스크 템플릿

- **실행 스크립트**: [scripts/task.sh](scripts/task.sh)
  - `init <TASK_ID>` - 작업 초기화
  - `status <TASK_ID>` - 상태 확인
  - `list` - 모든 작업 목록
