---
name: app-dev-workflow
description: 앱 개발 워크플로우를 시작합니다. 요구사항 분석(prd.md) -> 작업 계획(todo.md) -> Agent 분담 실행 -> 코드 리뷰 -> 최종 테스트 순서로 체계적인 앱 개발을 진행합니다. "/app-dev-workflow", "앱 개발 워크플로우", "앱 워크플로우로" 등의 명령으로 활성화됩니다.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TodoWrite, Skill, AskUserQuestion, mcp__mobile-mcp__mobile_take_screenshot, mcp__mobile-mcp__mobile_list_elements_on_screen, mcp__mobile-mcp__mobile_click_on_screen_at_coordinates, mcp__mobile-mcp__mobile_launch_app, mcp__mobile-mcp__mobile_list_available_devices
---

# 앱 개발 워크플로우 (App Development Workflow)

복잡한 앱 기능 요청을 체계적인 5단계 워크플로우로 관리하는 오케스트레이터입니다.

## 활성화 방법

다음 명령어로 워크플로우를 시작합니다:

- `앱 개발 워크플로우` 또는 `앱 워크플로우로 진행해줘`
- `/app-dev-workflow`
- `앱 개발로 [요청 내용]`

### 예시

```
사용자: 앱 개발 워크플로우로 거래 내역 필터링 기능을 추가해줘
사용자: /app-dev-workflow 카테고리별 예산 알림 기능
```

---

## 워크플로우 개요

```
[요청 접수]
    |
    v
[Phase 1: 요구사항 분석 및 계획 수립] ────────────
    |  - 요구사항 분석
    |  - prd.md 생성 (요구사항 정의서)
    |  - todo.md 생성 (작업 목록 + 상태 추적)
    |  - 사용자 확인
    v
[Phase 2: Agent 선별 및 작업 실행] ───────────────
    |  - 적합한 Agent 선별
    |  - 순차/병렬로 Agent 실행
    |  - todo.md 실시간 업데이트
    |  - Context 최적화 (compact 전략)
    v
[Phase 3: 코드 리뷰] ─────────────────────────────
    |  - code-reviewer agent 실행
    +──[결함 발견]──> [todo.md 업데이트] ──> [Phase 2]
    |
    v
[Phase 4: 최종 테스트] ───────────────────────────
    |  - Flutter 테스트 실행 (flutter test)
    |  - 앱 빌드 검증 (flutter build)
    |  - 실제 앱 테스트 (mobile-mcp 활용)
    v
[Phase 5: 완료] ──────────────────────────────────
    - 문서 업데이트
    - todo.md 아카이브
    - 결과 보고
```

---

## Phase 1: 요구사항 분석 및 계획 수립

### 1.1 요구사항 분석

사용자 요청을 분석하고 prd.md를 생성합니다.

### 1.2 prd.md 생성

```markdown
# PRD: [기능명]

## 배경 및 목적
- [왜 이 기능이 필요한가?]

## 필수 요구사항
- [ ] 요구사항 1
- [ ] 요구사항 2
- [ ] 요구사항 3

## UI/UX 요구사항
- [ ] 화면 구성
- [ ] 사용자 흐름

## 기술 요구사항
- [ ] 데이터 모델
- [ ] API 연동
- [ ] 상태 관리

## 성공 기준
- [ ] 기능이 정상 동작
- [ ] 테스트 통과
- [ ] 빌드 성공
```

### 1.3 todo.md 생성 (작업 목록 + 상태 추적 통합)

```markdown
# Todo: [작업명]

## 메타 정보
- 생성일: YYYY-MM-DD HH:MM
- 현재 Phase: 1 (계획 수립)
- 상태: 진행중 | 리뷰중 | 테스트중 | 완료
- 반복 횟수: 0

## 관련 문서
- PRD: .workflow/prd.md

---

## 작업 목록

### 1. 준비 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 1.1 | 코드베이스 분석 | Explore | 대기 | - |
| 1.2 | 아키텍처 설계 | code-architect | 대기 | - |

### 2. 구현 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 2.1 | Entity 정의 | tdd-developer | 대기 | - |
| 2.2 | Repository 구현 | tdd-developer | 대기 | - |
| 2.3 | Provider 구현 | tdd-developer | 대기 | - |
| 2.4 | UI 구현 | tdd-developer | 대기 | - |

### 3. 검증 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 3.1 | 코드 리뷰 | code-reviewer | 대기 | - |
| 3.2 | 단위 테스트 | test-writer | 대기 | - |
| 3.3 | 통합 테스트 | test-writer | 대기 | - |

### 4. 최종 테스트 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 4.1 | flutter test | 자동화 | 대기 | - |
| 4.2 | flutter build | 자동화 | 대기 | - |
| 4.3 | 앱 실행 테스트 | app-test-agent | 대기 | - |

---

## 리뷰 피드백 히스토리

---

## 테스트 결과 히스토리

---

## 변경 로그
- YYYY-MM-DD HH:MM: 초기 생성
```

### 1.4 사용자 확인

계획 수립 후 반드시 사용자에게 확인을 받습니다:

```
계획이 수립되었습니다:

[PRD 요약]
- 목적: ...
- 주요 요구사항: ...

[작업 계획]
- 준비 단계: N개 작업
- 구현 단계: N개 작업
- 검증 단계: N개 작업
- 최종 테스트: N개 작업

진행하시겠습니까? (Y/n)
```

---

## Phase 2: Agent 선별 및 작업 실행

### Agent 매핑 테이블 (Flutter 앱 개발)

| Agent 타입 | 용도 | 사용 시점 |
|-----------|------|----------|
| `Explore` | 코드베이스 탐색 | 구조 파악, 파일 검색 |
| `feature-dev:code-architect` | 아키텍처 설계 | 새 기능 설계 |
| `tdd-developer` | TDD 개발 | 테스트 우선 구현 |
| `test-writer` | 테스트 작성 | 테스트 코드 작성 |
| `general-purpose` | 범용 작업 | 일반 구현 작업 |
| `feature-dev:code-reviewer` | 코드 리뷰 | 품질/보안 검토 |
| `senior-code-reviewer` | 시니어 리뷰 | 종합 검토 |
| `app-test-agent` | 앱 테스트 | 실제 앱 UI 테스트 |

### Flutter 레이어별 Agent 할당

| 레이어 | 담당 Agent | 작업 내용 |
|--------|-----------|----------|
| Domain (Entity) | tdd-developer | 엔티티 정의 |
| Data (Model, Repository) | tdd-developer | 모델, 레포지토리 구현 |
| Presentation (Provider) | tdd-developer | Riverpod Provider 구현 |
| Presentation (UI) | general-purpose | 위젯, 페이지 구현 |

### 실행 규칙

1. **순차 실행**: 의존성이 있는 작업은 순차 실행
2. **병렬 실행**: 독립적인 작업은 병렬로 Task 호출
3. **상태 업데이트**: 작업 완료 시 즉시 todo.md 업데이트
4. **결과 기록**: 각 작업 결과를 todo.md "결과" 열에 기록

### 상태 표기

| 상태 | 표기 | 설명 |
|------|------|------|
| 대기 | `대기` | 아직 시작되지 않음 |
| 진행중 | `진행중` | 현재 실행 중 |
| 완료 | `완료` | 성공적으로 완료 |
| 실패 | `실패` | 문제 발생 |
| 재작업 | `재작업` | 리뷰 후 수정 필요 |

### Context 최적화 전략

#### 전략 1: Zero-Context Handoff

각 Agent는 독립적으로 실행되며, 결과는 파일로 저장합니다.

```
[메인 오케스트레이터]
    |
    +--[Task 호출]--> [Agent] --[파일 저장]--> .workflow/results/task-X.X.md
    |
    +--[파일 읽기]<-- .workflow/results/task-X.X.md (요약만)
    |
    +--[todo.md 업데이트]
```

#### 전략 2: 자동 /compact 시점

다음 시점에서 `/compact` 실행을 권장합니다:

1. **Phase 1 완료 후** (prd.md, todo.md 생성 완료)
2. **Phase 2에서 작업 3개 완료마다**
3. **Phase 3 리뷰 완료 후** (재작업 필요 시)
4. **Phase 4 테스트 시작 전**
5. **컨텍스트 경고 발생 시**

#### 전략 3: 병렬 실행 최적화

```
// 독립적인 작업들을 동시에 호출
Task(subagent_type: "tdd-developer", prompt: "작업 2.1...", run_in_background: true)
Task(subagent_type: "tdd-developer", prompt: "작업 2.2...", run_in_background: true)

// 모든 작업 완료 대기 후 결과 수집
TaskOutput(task_id: "...", block: true)
```

---

## Phase 3: 코드 리뷰

### 리뷰 실행

```
Task(
  subagent_type: "feature-dev:code-reviewer",
  prompt: "Phase 2에서 구현한 코드를 리뷰해주세요. 버그, 보안, 품질 이슈를 확인합니다.
  변경된 파일: [파일 목록]"
)
```

### 리뷰 결과 처리

#### 결함 발견 시

1. todo.md의 "리뷰 피드백 히스토리" 섹션에 피드백 추가
2. 해당 작업의 상태를 `재작업`으로 변경
3. "반복 횟수" 증가
4. 담당 Agent에게 재할당하여 Phase 2 재실행

```markdown
## 리뷰 피드백 히스토리

### 1차 리뷰 (2024-01-15)
- [x] ledger_repository.dart: 에러 핸들링 누락 -> 재작업 완료
- [x] ledger_provider.dart: rethrow 누락 -> 재작업 완료
```

#### 결함 없음

1. 모든 작업 상태를 `완료`로 변경
2. Phase 4로 진행

### 반복 제한

- 최대 3회까지 리뷰 반복
- 초과 시 사용자에게 확인 요청

---

## Phase 4: 최종 테스트

### 4.1 Flutter 테스트 실행

```bash
# 모든 테스트 실행
flutter test

# 특정 테스트 파일 실행
flutter test test/features/[feature]/*_test.dart
```

### 4.2 빌드 검증

```bash
# 분석
flutter analyze

# 빌드 (Android APK)
flutter build apk --debug

# 빌드 (iOS - Mac에서만)
flutter build ios --debug --no-codesign
```

### 4.3 실제 앱 테스트 (mobile-mcp 활용)

```
# 사용 가능한 디바이스 확인
mcp__mobile-mcp__mobile_list_available_devices

# 앱 실행
mcp__mobile-mcp__mobile_launch_app

# 스크린샷 촬영
mcp__mobile-mcp__mobile_take_screenshot

# UI 요소 확인
mcp__mobile-mcp__mobile_list_elements_on_screen

# 클릭 동작
mcp__mobile-mcp__mobile_click_on_screen_at_coordinates
```

### 테스트 결과 기록

todo.md에 테스트 결과를 기록합니다:

```markdown
## 테스트 결과 히스토리

### 1차 테스트 (YYYY-MM-DD)
- flutter test: 통과 (10/10 tests passed)
- flutter analyze: 통과 (0 issues)
- flutter build: 성공
- 앱 테스트: 통과
```

### 테스트 실패 시

1. 실패 원인 분석
2. todo.md에 실패 내용 기록
3. Phase 2로 돌아가 수정
4. 다시 Phase 3, 4 진행

---

## Phase 5: 완료

### 마무리 작업

1. **문서 업데이트**: `codebase-update` 스킬 호출
2. **todo.md 아카이브**: `.workflow/archived/` 폴더로 이동
3. **결과 보고**: 사용자에게 최종 결과 보고

### 아카이브

```bash
mkdir -p .workflow/archived
mv .workflow/todo.md .workflow/archived/YYYY-MM-DD_[작업명].md
```

### 결과 보고 형식

```markdown
## 앱 개발 워크플로우 완료

### 작업 요약
- 작업명: [작업명]
- 총 작업 수: [N]개
- 리뷰 반복: [N]회
- 테스트 반복: [N]회

### 변경된 파일
- lib/features/[feature]/domain/entities/xxx.dart (신규)
- lib/features/[feature]/data/repositories/xxx_repository.dart (신규)
- lib/features/[feature]/presentation/providers/xxx_provider.dart (신규)
- lib/features/[feature]/presentation/pages/xxx_page.dart (수정)
- test/features/[feature]/xxx_test.dart (신규)

### 테스트 결과
- 단위 테스트: 통과
- 빌드: 성공
- 앱 테스트: 통과

### 다음 단계
- [ ] 실제 디바이스 테스트
- [ ] PR 생성
- [ ] 배포 검토
```

---

## 체크포인트 시스템 (Context 관리)

### 파일 구조

```
.workflow/
├── prd.md               # 요구사항 정의서
├── todo.md              # 작업 목록 + 상태 추적
├── checkpoint.md        # 현재 체크포인트
├── context/             # Phase별 컨텍스트
│   ├── phase1-result.md
│   ├── phase2-result.md
│   ├── phase3-result.md
│   └── phase4-result.md
├── results/             # Agent 작업 결과
│   └── task-X.X.md
└── archived/            # 완료된 워크플로우
```

### checkpoint.md 형식

```markdown
# Workflow Checkpoint

## 현재 상태
- 작업명: [작업명]
- 현재 Phase: [1-5]
- 현재 작업: [작업 번호]
- 마지막 업데이트: YYYY-MM-DD HH:MM

## 다음 단계
- 다음 Phase: [Phase 번호]
- 다음 작업: [작업 설명]
- 담당 Agent: [Agent 타입]

## 재개 명령어
```
앱 개발 워크플로우 재개
```

## 컨텍스트 파일 참조
- prd.md: .workflow/prd.md
- todo.md: .workflow/todo.md
- Phase 결과: .workflow/context/phaseN-result.md
```

### 워크플로우 재개

```
앱 개발 워크플로우 재개
/app-dev-workflow resume
```

---

## 주의사항

1. **에러 처리 원칙 준수**: CLAUDE.md의 에러 처리 원칙을 반드시 준수 (rethrow 등)
2. **단일 todo.md 파일**: `.workflow/todo.md`는 항상 하나만 존재
3. **상태 동기화**: 작업 완료 시 즉시 todo.md 업데이트 필수
4. **리뷰 반복 제한**: 최대 3회 (초과 시 사용자 확인)
5. **테스트 필수**: 코드 변경 없이 테스트를 건너뛰지 않음
6. **사용자 확인**: Phase 1 완료 후 반드시 사용자 승인 필요
7. **Context 관리**: 작업 3개마다 /compact 권장

---

## 전체 흐름 예시

### 사용자 요청

```
사용자: 앱 개발 워크플로우로 거래 필터링 기능을 추가해줘
```

### 실행 과정

```
[Phase 1] 요구사항 분석 및 계획 수립
   -> prd.md 생성: "거래 필터링 기능 요구사항"
   -> todo.md 생성: 10개 작업 정의 + Agent 할당
   -> 사용자 확인: "진행하시겠습니까?"

[Phase 2] Agent 분담 실행 (todo.md 실시간 업데이트)
   1.1 Explore -> 완료: "transaction 관련 파일 분석"
   1.2 code-architect -> 완료: "필터 기능 설계"
   2.1 tdd-developer -> 완료: "FilterCriteria entity 생성"
   2.2 tdd-developer -> 완료: "TransactionRepository 수정"
   [/compact 권장]
   2.3 tdd-developer -> 완료: "TransactionProvider 수정"
   2.4 general-purpose -> 완료: "FilterWidget 구현"

[Phase 3] 코드 리뷰
   code-reviewer -> "에러 핸들링 추가 필요"
   -> todo.md 업데이트, 2.2 재작업
   -> tdd-developer 재실행 -> 완료
   -> 2차 리뷰 -> 통과

[Phase 4] 최종 테스트
   flutter test -> 통과 (15/15 tests)
   flutter analyze -> 통과
   flutter build apk -> 성공
   앱 테스트 -> 필터 동작 확인

[Phase 5] 완료
   codebase-update 호출
   todo.md 아카이브
   결과 보고
```
