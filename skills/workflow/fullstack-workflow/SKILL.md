---
name: fullstack-workflow
description: 풀스택 워크플로우를 시작합니다. 계획 수립(prd.md + task.md) -> Agent 분담 실행 -> 코드 리뷰 -> 완료 순서로 체계적인 개발을 진행합니다. "풀스택 워크플로우", "/fullstack-workflow", "풀스택으로" 등의 명령으로 활성화됩니다.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TodoWrite, Skill, AskUserQuestion
---

# 풀스택 워크플로우 (Fullstack Workflow)

복잡한 기능 요청을 체계적인 워크플로우로 관리하는 오케스트레이터입니다.

## 활성화 방법

다음 명령어로 워크플로우를 시작합니다:

- `풀스택 워크플로우` 또는 `풀스택 워크플로우로 진행해줘`
- `/fullstack-workflow`
- `풀스택으로 [요청 내용]`

### 예시

```
사용자: 풀스택 워크플로우로 사용자 인증 기능을 추가해줘
사용자: /fullstack-workflow 파일 업로드에 바이러스 스캔 추가
```

---

## 워크플로우 개요

```
[요청 접수]
    |
    v
[Phase 1: 계획 수립] ─────────────────────────────
    |  - task-planner agent 호출
    |  - prd.md 생성 (요구사항)
    |  - task.md 생성 (작업 목록 + 상태 추적)
    |  - 사용자 확인
    v
[Phase 2: Agent 분담 및 실행] ─────────────────────
    |  - 순차/병렬로 Agent 실행
    |  - task.md 실시간 업데이트
    v
[Phase 3: 코드 리뷰] ─────────────────────────────
    |  - code-reviewer agent 실행
    +──[결함 발견]──> [task.md 업데이트] ──> [Phase 2]
    |
    v
[Phase 4: 완료] ──────────────────────────────────
    - 문서 업데이트
    - 결과 보고
```

---

## Phase 1: 계획 수립

task-planner agent를 호출하여 작업 계획을 수립합니다.

### 실행 방법

```
Task(
  subagent_type: "task-planner",
  prompt: "[사용자 요청] - 풀스택 워크플로우로 실행 계획을 수립해주세요."
)
```

### 결과물

1. `prd.md` - 요구사항 정의 문서
2. `.workflow/task.md` - 작업 분해, Agent 할당, 상태 추적 통합 문서

### task.md 형식 (작업 목록 + 상태 추적 통합)

```markdown
# Task: [작업명]

## 메타 정보
- 생성일: YYYY-MM-DD HH:MM
- 상태: 진행중 | 리뷰중 | 완료
- 반복 횟수: 0

## 관련 문서
- PRD: prd.md

---

## 작업 목록

### 준비 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 1.1 | 코드베이스 분석 | Explore | 대기 | - |
| 1.2 | 아키텍처 설계 | code-architect | 대기 | - |

### 구현 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 2.1 | [구현 작업] | tdd-developer | 대기 | - |
| 2.2 | [구현 작업] | api-implementer | 대기 | - |

### 검증 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 3.1 | 코드 리뷰 | code-reviewer | 대기 | - |
| 3.2 | 테스트 검증 | test-writer | 대기 | - |

---

## 리뷰 피드백 히스토리

### 1차 리뷰 (YYYY-MM-DD)
- [ ] 피드백 1
- [ ] 피드백 2

---

## 변경 로그
- YYYY-MM-DD HH:MM: 초기 생성
```

### 사용자 확인

계획 수립 후 반드시 사용자에게 확인을 받습니다:

```
계획이 수립되었습니다:
- PRD: [요약]
- 총 [N]개 작업

진행하시겠습니까? (Y/n)
```

---

## Phase 2: Agent 분담 및 실행

각 작업을 담당 Agent에게 할당하고 실행합니다.

### Agent 매핑 테이블

| Agent 타입 | 용도 | 사용 시점 |
|-----------|------|----------|
| `Explore` | 코드베이스 탐색 | 구조 파악, 파일 검색 |
| `feature-dev:code-architect` | 아키텍처 설계 | 새 기능 설계 |
| `feature-dev:code-explorer` | 심층 코드 분석 | 실행 경로 추적 |
| `tdd-developer` | TDD 개발 | 테스트 우선 구현 |
| `test-writer` | 테스트 작성 | 테스트 코드 작성 |
| `general-purpose` | 범용 작업 | 일반 구현 작업 |
| `feature-dev:code-reviewer` | 코드 리뷰 | 품질/보안 검토 |
| `senior-code-reviewer` | 시니어 리뷰 | 종합 검토 |
| `workflow-orchestrator` | 워크플로우 조율 | Phase 전환, 체크포인트 관리 |
| `api-implementer` | API 구현 | 4계층 구조 API 엔드포인트 |
| `schema-designer` | 스키마 설계 | TypeBox 스키마 작성 |

### 실행 규칙

1. **순차 실행**: 의존성이 있는 작업은 순차 실행
2. **병렬 실행**: 독립적인 작업은 병렬로 Task 호출
3. **상태 업데이트**: 작업 완료 시 즉시 task.md 업데이트
4. **결과 기록**: 각 작업 결과를 task.md "결과" 열에 기록

### 상태 표기

| 상태 | 표기 | 설명 |
|------|------|------|
| 대기 | `대기` | 아직 시작되지 않음 |
| 진행중 | `진행중` | 현재 실행 중 |
| 완료 | `완료` | 성공적으로 완료 |
| 실패 | `실패` | 문제 발생 |
| 재작업 | `재작업` | 리뷰 후 수정 필요 |

### task.md 업데이트 예시

```markdown
### 구현 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 2.1 | 스캔 서비스 구현 | tdd-developer | 완료 | src/services/scanner.ts 생성 |
| 2.2 | 핸들러 수정 | general-purpose | 진행중 | - |
```

---

## Phase 3: 코드 리뷰

구현 완료 후 코드 리뷰를 진행합니다.

### 리뷰 실행

```
Task(
  subagent_type: "feature-dev:code-reviewer",
  prompt: "Phase에서 구현한 코드를 리뷰해주세요. 버그, 보안, 품질 이슈를 확인합니다.
  변경된 파일: [파일 목록]"
)
```

### 리뷰 결과 처리

#### 결함 발견 시

1. task.md의 "리뷰 피드백 히스토리" 섹션에 피드백 추가
2. 해당 작업의 상태를 `재작업`으로 변경
3. "반복 횟수" 증가
4. 담당 Agent에게 재할당하여 Phase 2 재실행

```markdown
## 리뷰 피드백 히스토리

### 1차 리뷰 (2024-01-15)
- [x] scanner.ts: 에러 핸들링 누락 -> 재작업 완료
- [x] handler.ts: 타입 정의 부정확 -> 재작업 완료
```

#### 결함 없음

1. 모든 작업 상태를 `완료`로 변경
2. Phase 4로 진행

### 반복 제한

- 최대 3회까지 리뷰 반복
- 초과 시 사용자에게 확인 요청

---

## Phase 4: 완료

### 마무리 작업

1. **문서 업데이트**: `codebase-update` 스킬 호출
2. **task.md 아카이브**: `.workflow/archived/` 폴더로 이동
3. **결과 보고**: 사용자에게 최종 결과 보고

### 아카이브

```bash
mkdir -p .workflow/archived
mv .workflow/task.md .workflow/archived/YYYY-MM-DD_[작업명].md
```

### 결과 보고 형식

```markdown
## 풀스택 워크플로우 완료

### 작업 요약
- 작업명: [작업명]
- 총 작업 수: [N]개
- 리뷰 반복: [N]회

### 변경된 파일
- src/services/scanner.ts (신규)
- src/handlers/upload.ts (수정)
- test/scanner.test.ts (신규)

### 다음 단계
- [ ] PR 생성
- [ ] 배포 검토
```

---

## 전체 흐름 예시

### 사용자 요청

```
사용자: 풀스택 워크플로우로 파일 업로드에 바이러스 스캔 기능 추가해줘
```

### 실행 과정

```
[Phase 1] task-planner 호출
   -> prd.md 생성: "바이러스 스캔 기능 요구사항"
   -> task.md 생성: 5개 작업 정의 + Agent 할당 + 상태 추적
   -> 사용자 확인: "진행하시겠습니까?"

[Phase 2] Agent 순차 실행 (task.md 실시간 업데이트)
   1.1 Explore -> 완료: "upload.ts, fileService.ts 분석"
   1.2 code-architect -> 완료: "스캔 서비스 인터페이스 설계"
   2.1 tdd-developer -> 완료: "scanner.ts, scanner.test.ts 생성"
   2.2 general-purpose -> 완료: "upload.ts 수정"

[Phase 3] 코드 리뷰
   code-reviewer -> "에러 핸들링 추가 필요"
   -> task.md 업데이트, 2.1 재작업
   -> tdd-developer 재실행 -> 완료
   -> 2차 리뷰 -> 통과

[Phase 4] 완료
   codebase-update 호출
   task.md 아카이브
   결과 보고
```

---

## 주의사항

1. **단일 task.md 파일**: `.workflow/task.md`는 항상 하나만 존재
2. **상태 동기화**: 작업 완료 시 즉시 task.md 업데이트 필수
3. **리뷰 반복 제한**: 최대 3회 (초과 시 사용자 확인)
4. **컨텍스트 유지**: Agent 간 결과 공유를 위해 task.md에 기록
5. **사용자 확인**: Phase 1 완료 후 반드시 사용자 승인 필요

---

## 체크포인트 시스템 (Context 관리)

> **중요**: 풀스택 워크플로우는 컨텍스트를 많이 소모합니다.
> "Context low" 에러 방지를 위해 체크포인트 시스템을 사용합니다.

### 체크포인트 개요

```
[Phase 완료] -> [체크포인트 저장] -> [/compact 실행] -> [체크포인트에서 재개]
```

### 체크포인트 파일 구조

```
.workflow/
├── task.md              # 작업 목록 + 상태 추적 (통합)
├── checkpoint.md        # 현재 체크포인트 (진행 상태)
├── context/             # 각 Phase별 컨텍스트 저장
│   ├── phase1-result.md # Phase 1 결과
│   ├── phase2-result.md # Phase 2 결과
│   └── review-result.md # 리뷰 결과
├── results/             # Agent 작업 결과
│   └── task-X.X.md
└── archived/            # 완료된 워크플로우
```

### checkpoint.md 형식

```markdown
# Workflow Checkpoint

## 현재 상태
- 작업명: [작업명]
- 현재 Phase: [1-4]
- 현재 작업: [작업 번호]
- 마지막 업데이트: YYYY-MM-DD HH:MM

## 다음 단계
- 다음 Phase: [Phase 번호]
- 다음 작업: [작업 설명]
- 담당 Agent: [Agent 타입]

## 재개 명령어
\`\`\`
풀스택 워크플로우 재개
\`\`\`

## 컨텍스트 파일 참조
- task.md: .workflow/task.md
- Phase 1 결과: .workflow/context/phase1-result.md
- ...
```

### Phase별 자동 체크포인트

각 Phase 완료 시 자동으로 체크포인트가 저장됩니다:

| Phase | 체크포인트 저장 내용 | 파일 |
|-------|---------------------|------|
| Phase 1 | prd.md, task.md 생성 완료 | `context/phase1-result.md` |
| Phase 2 | 각 작업 완료 결과, 변경된 파일 목록 | `context/phase2-result.md` |
| Phase 3 | 리뷰 결과, 피드백 목록 | `context/review-result.md` |

### 워크플로우 재개

#### 재개 명령어

```
풀스택 워크플로우 재개
/fullstack-workflow resume
풀스택 재개
```

#### 재개 프로세스

1. **checkpoint.md 읽기**
2. **task.md에서 현재 상태 확인**
3. **필요한 컨텍스트만 로드** (해당 Phase의 result.md만)
4. **다음 작업부터 실행**

### 자동 /compact 권장 시점

다음 시점에서 `/compact` 실행을 권장합니다:

1. **Phase 1 완료 후** (prd.md, task.md 생성 완료)
2. **Phase 2에서 작업 3개 완료마다**
3. **Phase 3 리뷰 완료 후** (재작업 필요 시)
4. **컨텍스트 경고 발생 시**

---

## 고급 컨텍스트 최적화 전략

### 전략 1: Agent 격리 실행 (Zero-Context Handoff)

각 Agent는 **완전히 독립적으로** 실행되며, 메인 컨텍스트에 결과를 누적하지 않습니다.

```
[메인 오케스트레이터]
    |
    +--[Task 호출]--> [Agent A] --[파일 저장]--> .workflow/results/task-1.1.md
    |                    (독립 컨텍스트)
    |
    +--[파일 읽기]<-- .workflow/results/task-1.1.md (요약만)
    |
    +--[task.md 업데이트]
```

#### Agent 호출 패턴

```
Task(
  subagent_type: "tdd-developer",
  prompt: """
  [작업 지시서]
  - 작업 ID: 2.1
  - 작업: 스캔 서비스 구현
  - 입력 파일: .workflow/context/phase1-result.md
  - 출력 파일: .workflow/results/task-2.1.md

  결과를 출력 파일에 저장하세요:
  - 생성/수정 파일 목록
  - 주요 변경 사항 (3줄 이내)
  - 다음 작업을 위한 정보
  """
)
```

### 전략 2: 계층적 요약 시스템

```
.workflow/
├── summary.md           # Level 1: 전체 한 줄 요약
├── task.md              # Level 2: 작업 목록 + 상태
├── context/
│   └── overview.md      # Level 2: Phase별 핵심 정보
└── results/
    └── task-X.X.md      # Level 3: 상세 내용
```

### 전략 3: 최소 컨텍스트 전달 규칙

| Agent 타입 | 전달 정보 | 제외 정보 |
|-----------|----------|----------|
| Explore | 검색 대상 경로만 | 이전 분석 결과 |
| code-architect | 요구사항 + 기존 패턴 | 다른 Phase 결과 |
| tdd-developer | 구현 스펙 + 테스트 패턴 | 분석 과정 |
| code-reviewer | 변경 파일 목록만 | 구현 과정 |

### 전략 4: 병렬 실행 최적화

```
// 독립적인 작업들을 동시에 호출
Task(subagent_type: "tdd-developer", prompt: "작업 2.1...", run_in_background: true)
Task(subagent_type: "general-purpose", prompt: "작업 2.2...", run_in_background: true)
Task(subagent_type: "test-writer", prompt: "작업 2.3...", run_in_background: true)

// 모든 작업 완료 대기 후 결과 수집
TaskOutput(task_id: "...", block: true)
```

---

## 최적화된 워크플로우 실행 흐름

```
[Phase 1] 계획 수립
├── 로드: 없음 (처음 시작)
├── 실행: task-planner (독립 컨텍스트)
├── 저장: prd.md, task.md, summary.md
└── 정리: 계획 상세 내용 파일로 이동

[/compact] <- 자동 권장

[Phase 2] Agent 실행 (작업 3개씩)
├── 로드: task.md + 해당 작업 의존성만
├── 실행: Agent 병렬 실행 (3개)
├── 저장: results/task-X.X.md (각각)
├── 업데이트: task.md 상태 갱신
└── [/compact] <- 3개마다 자동 권장

[Phase 3] 리뷰
├── 로드: 변경 파일 목록만 (task.md에서)
├── 실행: code-reviewer (변경 파일 직접 읽기)
├── 저장: review-result.md
└── 업데이트: task.md 피드백 추가

[Phase 4] 완료
├── 로드: summary.md
├── 실행: 결과 보고
└── 아카이브: task.md 이동
```
