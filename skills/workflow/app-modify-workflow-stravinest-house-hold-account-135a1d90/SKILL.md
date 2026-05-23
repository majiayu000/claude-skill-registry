---
name: app-modify-workflow
description: 앱 수정 워크플로우를 시작합니다. 현황 분석 -> UI/UX 검토 -> 엣지 케이스 확인 -> 사용자 질문 -> 계획 수립 -> 구현 -> 코드 리뷰 반복 순서로 체계적인 앱 수정을 진행합니다. "/app-modify-workflow", "앱 수정 워크플로우", "수정 워크플로우로" 등의 명령으로 활성화됩니다.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TodoWrite, Skill, AskUserQuestion, EnterPlanMode, ExitPlanMode, mcp__mobile-mcp__mobile_take_screenshot, mcp__mobile-mcp__mobile_list_elements_on_screen, mcp__mobile-mcp__mobile_click_on_screen_at_coordinates, mcp__mobile-mcp__mobile_launch_app, mcp__mobile-mcp__mobile_list_available_devices
---

# 앱 수정 워크플로우 (App Modify Workflow)

기존 앱 기능을 수정/개선할 때 사용하는 체계적인 6단계 워크플로우입니다.
새 기능 개발이 아닌 **기존 기능의 변경, 버그 수정, UI/UX 개선**에 특화되어 있습니다.

## 활성화 방법

다음 명령어로 워크플로우를 시작합니다:

- `앱 수정 워크플로우` 또는 `수정 워크플로우로 진행해줘`
- `/app-modify-workflow`
- `앱 수정으로 [요청 내용]`

### 예시

```
사용자: 앱 수정 워크플로우로 결제수단 관리 화면을 개선해줘
사용자: /app-modify-workflow 카테고리 선택 UI 수정
사용자: 수정 워크플로우로 거래 입력 폼의 UX 개선해줘
```

---

## 워크플로우 개요

```
[요청 접수]
    |
    v
[Phase 1: 현황 분석] ─────────────────────────────────
    |  - 수정 대상 코드 분석
    |  - UI/UX 현황 파악
    |  - 엣지 케이스 식별
    v
[Phase 2: 요구사항 명확화] ───────────────────────────
    |  - AskUserQuestion으로 질문
    |  - 답변 기반 요구사항 정리
    v
[Phase 3: 계획 수립] ─────────────────────────────────
    |  - plan 모드로 상세 계획 작성
    |  - 사용자 승인
    v
[Phase 4: 구현] ──────────────────────────────────────
    |  - modify-todo.md 생성 및 실행
    |  - Agent 분담 작업
    v
[Phase 5: 코드 리뷰 및 반복] ─────────────────────────
    |  - code-reviewer 실행
    +──[결함 발견]──> [modify-todo.md 업데이트] ──> [Phase 4]
    |
    v
[Phase 6: 완료] ──────────────────────────────────────
    - 테스트 검증
    - 결과 보고
    - 아카이브
```

---

## Phase 1: 현황 분석

### 1.1 수정 대상 코드 분석

수정 대상 기능과 관련된 코드를 심층 분석합니다.

```
Task(
  subagent_type: "feature-dev:code-explorer",
  prompt: "[수정 대상 기능]의 현재 구현을 분석해주세요.
  - 관련 파일 목록
  - 실행 경로 추적
  - 의존성 맵핑
  - 현재 아키텍처 패턴"
)
```

### 1.2 UI/UX 현황 파악

현재 UI/UX 상태를 분석하고 개선점을 식별합니다.

#### 분석 항목

| 항목 | 확인 사항 |
|------|----------|
| 레이아웃 | 요소 배치, 간격, 정렬 |
| 색상 | 일관성, 접근성, 다크모드 지원 |
| 폰트 | 크기, 가독성, 계층 구조 |
| 인터랙션 | 터치 영역, 피드백, 애니메이션 |
| 상태 표시 | 로딩, 에러, 빈 상태 처리 |
| 반응성 | 다양한 화면 크기 대응 |

#### 스크린샷 분석 (선택사항)

```
# 현재 화면 캡처
mcp__mobile-mcp__mobile_take_screenshot

# UI 요소 분석
mcp__mobile-mcp__mobile_list_elements_on_screen
```

### 1.3 엣지 케이스 식별

수정 시 고려해야 할 엣지 케이스를 식별합니다.

#### 공통 엣지 케이스 체크리스트

| 카테고리 | 엣지 케이스 |
|----------|-----------|
| 데이터 | 빈 데이터, 대량 데이터, 특수 문자, 긴 텍스트 |
| 네트워크 | 오프라인, 느린 연결, 타임아웃 |
| 사용자 입력 | 유효하지 않은 입력, 빠른 연속 클릭, 동시 요청 |
| 권한 | 권한 없음, 읽기 전용, 만료된 세션 |
| 디바이스 | 작은 화면, 큰 화면, 접근성 설정 |
| 상태 | 초기 상태, 중간 상태, 에러 복구 |

### 1.4 분석 결과 저장

분석 결과를 파일로 저장합니다.

```markdown
# 현황 분석 결과

## 수정 대상: [기능명]

### 관련 파일
- lib/features/[feature]/presentation/pages/xxx_page.dart
- lib/features/[feature]/presentation/widgets/xxx_widget.dart
- ...

### 현재 UI/UX 상태
- 강점: ...
- 개선점: ...

### 식별된 엣지 케이스
1. [엣지 케이스 1]
2. [엣지 케이스 2]
3. ...

### 의존성
- Provider: ...
- Repository: ...
```

저장 위치: `.workflow/context/analysis-result.md`

---

## Phase 2: 요구사항 명확화

### 2.1 사용자 질문

분석 결과를 바탕으로 사용자에게 구체적인 질문을 합니다.

```
AskUserQuestion(
  questions: [
    {
      "question": "UI 개선 방향을 선택해주세요",
      "header": "UI 방향",
      "options": [
        {"label": "레이아웃 재구성", "description": "요소 배치와 구조를 변경"},
        {"label": "스타일 개선", "description": "색상, 폰트, 간격 조정"},
        {"label": "인터랙션 개선", "description": "애니메이션, 피드백 추가"},
        {"label": "전면 리디자인", "description": "전체적으로 새롭게 설계"}
      ],
      "multiSelect": false
    },
    {
      "question": "우선 처리할 엣지 케이스를 선택해주세요",
      "header": "엣지 케이스",
      "options": [
        {"label": "데이터 관련", "description": "빈 데이터, 대량 데이터 처리"},
        {"label": "에러 처리", "description": "네트워크 오류, 타임아웃"},
        {"label": "입력 검증", "description": "유효하지 않은 입력 처리"},
        {"label": "모든 케이스", "description": "전부 처리"}
      ],
      "multiSelect": true
    }
  ]
)
```

### 2.2 질문 카테고리

| 카테고리 | 질문 예시 |
|----------|----------|
| 범위 | 어떤 부분까지 수정할까요? (특정 컴포넌트 / 전체 화면) |
| 우선순위 | 가장 중요한 개선 사항은 무엇인가요? |
| 제약사항 | 유지해야 할 기존 동작이 있나요? |
| 호환성 | 이전 버전과의 호환성이 필요한가요? |
| 테스트 | 어떤 시나리오를 반드시 테스트해야 하나요? |

### 2.3 요구사항 정리

사용자 답변을 바탕으로 요구사항을 정리합니다.

```markdown
# 수정 요구사항

## 기능: [기능명]

### 사용자 요청 요약
- [핵심 요청 내용]

### UI/UX 요구사항
- [ ] [UI 요구사항 1]
- [ ] [UI 요구사항 2]

### 기능 요구사항
- [ ] [기능 요구사항 1]
- [ ] [기능 요구사항 2]

### 엣지 케이스 처리
- [ ] [엣지 케이스 1]
- [ ] [엣지 케이스 2]

### 제약사항
- [유지해야 할 동작]
- [호환성 요구사항]
```

저장 위치: `.workflow/modify-requirements.md`

---

## Phase 3: 계획 수립

### 3.1 Plan 모드 진입

요구사항을 바탕으로 상세 구현 계획을 수립합니다.

```
EnterPlanMode()
```

### 3.2 계획 작성 가이드

Plan 모드에서 다음 내용을 포함하여 계획을 작성합니다:

```markdown
# 수정 계획: [기능명]

## 변경 범위

### 수정할 파일
| 파일 | 변경 유형 | 변경 내용 |
|------|----------|----------|
| xxx_page.dart | 수정 | 레이아웃 구조 변경 |
| xxx_widget.dart | 신규 | 새 위젯 추가 |
| xxx_provider.dart | 수정 | 상태 로직 개선 |

### 영향받는 영역
- 직접 영향: [영향받는 기능 1], [영향받는 기능 2]
- 간접 영향: [관련 기능]

## 구현 단계

### 1단계: [제목]
- 작업 내용
- 예상 변경 사항

### 2단계: [제목]
- 작업 내용
- 예상 변경 사항

## 테스트 계획

### 단위 테스트
- [ ] [테스트 케이스 1]
- [ ] [테스트 케이스 2]

### 통합 테스트
- [ ] [시나리오 1]
- [ ] [시나리오 2]

### 엣지 케이스 테스트
- [ ] [엣지 케이스 1]
- [ ] [엣지 케이스 2]

## 리스크 및 대응

| 리스크 | 대응 방안 |
|--------|----------|
| [리스크 1] | [대응 1] |
| [리스크 2] | [대응 2] |
```

### 3.3 사용자 승인

계획 완료 후 승인을 요청합니다.

```
ExitPlanMode()
```

---

## Phase 4: 구현

### 4.1 modify-todo.md 생성

```markdown
# Modify Todo: [작업명]

## 메타 정보
- 생성일: YYYY-MM-DD HH:MM
- 현재 Phase: 4 (구현)
- 상태: 진행중
- 리뷰 반복 횟수: 0

## 관련 문서
- 분석 결과: .workflow/context/analysis-result.md
- 요구사항: .workflow/modify-requirements.md

---

## 작업 목록

### 1. 준비 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 1.1 | 기존 코드 백업 확인 | - | 대기 | - |
| 1.2 | 의존성 확인 | Explore | 대기 | - |

### 2. 구현 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 2.1 | [수정 작업 1] | tdd-developer | 대기 | - |
| 2.2 | [수정 작업 2] | general-purpose | 대기 | - |
| 2.3 | [UI 수정] | general-purpose | 대기 | - |

### 3. 엣지 케이스 처리
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 3.1 | [엣지 케이스 1] | tdd-developer | 대기 | - |
| 3.2 | [엣지 케이스 2] | tdd-developer | 대기 | - |

### 4. 검증 단계
| 번호 | 작업 | 담당 Agent | 상태 | 결과 |
|------|------|-----------|------|------|
| 4.1 | 코드 리뷰 | code-reviewer | 대기 | - |
| 4.2 | 테스트 작성 | test-writer | 대기 | - |

---

## 리뷰 피드백 히스토리

---

## 변경 로그
- YYYY-MM-DD HH:MM: 초기 생성
```

저장 위치: `.workflow/modify-todo.md`

### 4.2 Agent 할당 테이블

| 작업 유형 | 담당 Agent | 설명 |
|----------|-----------|------|
| 코드 분석 | `Explore` | 기존 코드 구조 파악 |
| 로직 수정 | `tdd-developer` | 테스트 우선 개발로 안전한 수정 |
| UI 수정 | `general-purpose` | 위젯, 레이아웃 변경 |
| 테스트 | `test-writer` | 테스트 코드 작성 |
| 리뷰 | `feature-dev:code-reviewer` | 코드 품질 검토 |

### 4.3 실행 규칙

1. **순차 실행**: 의존성 있는 작업은 순차 실행
2. **병렬 실행**: 독립적인 UI 작업은 병렬 가능
3. **상태 업데이트**: 작업 완료 시 즉시 modify-todo.md 업데이트
4. **결과 기록**: 변경된 파일과 주요 내용 기록

---

## Phase 5: 코드 리뷰 및 반복

### 5.1 리뷰 실행

```
Task(
  subagent_type: "feature-dev:code-reviewer",
  prompt: "수정된 코드를 리뷰해주세요.

  확인 항목:
  1. 버그: 로직 오류, 예외 처리 누락
  2. 보안: 취약점, 데이터 노출
  3. 성능: 불필요한 렌더링, 메모리 누수
  4. 품질: 코드 스타일, 가독성
  5. 호환성: 기존 기능 영향

  변경된 파일: [파일 목록]"
)
```

### 5.2 리뷰 결과 처리

#### 결함 발견 시

1. modify-todo.md의 "리뷰 피드백 히스토리" 섹션에 피드백 추가
2. 해당 작업의 상태를 `재작업`으로 변경
3. "리뷰 반복 횟수" 증가
4. 담당 Agent에게 재할당하여 Phase 4 재실행

```markdown
## 리뷰 피드백 히스토리

### 1차 리뷰 (YYYY-MM-DD)
- [x] xxx_page.dart: dispose에서 리소스 해제 누락 -> 재작업 완료
- [x] xxx_widget.dart: 에러 상태 UI 미구현 -> 재작업 완료
```

#### 결함 없음

1. 모든 작업 상태를 `완료`로 변경
2. Phase 6으로 진행

### 5.3 반복 제한

- **최대 3회**까지 리뷰 반복
- 초과 시 사용자에게 확인 요청

```
3회 이상 리뷰가 반복되었습니다.
현재 남은 이슈:
- [이슈 1]
- [이슈 2]

계속 진행하시겠습니까? (Y/n)
```

---

## Phase 6: 완료

### 6.1 테스트 검증

```bash
# 단위 테스트
flutter test test/features/[feature]/

# 전체 분석
flutter analyze

# 빌드 검증
flutter build apk --debug
```

### 6.2 앱 테스트 (선택사항)

```
# 앱 실행 및 수정 사항 확인
mcp__mobile-mcp__mobile_launch_app
mcp__mobile-mcp__mobile_take_screenshot
```

### 6.3 결과 보고

```markdown
## 앱 수정 워크플로우 완료

### 작업 요약
- 수정 대상: [기능명]
- 총 작업 수: [N]개
- 리뷰 반복: [N]회

### 변경된 파일
| 파일 | 변경 유형 | 주요 변경 내용 |
|------|----------|--------------|
| xxx_page.dart | 수정 | 레이아웃 개선 |
| xxx_widget.dart | 신규 | 에러 상태 위젯 추가 |

### 해결된 엣지 케이스
- [x] [엣지 케이스 1]
- [x] [엣지 케이스 2]

### 테스트 결과
- 단위 테스트: 통과 (N/N tests)
- 분석: 통과 (0 issues)
- 빌드: 성공

### 다음 단계
- [ ] 실제 디바이스 테스트
- [ ] PR 생성
- [ ] QA 검토
```

### 6.4 아카이브

```bash
mkdir -p .workflow/archived
mv .workflow/modify-todo.md .workflow/archived/YYYY-MM-DD_[작업명]_modify.md
```

---

## 체크포인트 시스템

### 파일 구조

```
.workflow/
├── modify-todo.md           # 작업 목록 + 상태 추적
├── modify-requirements.md   # 요구사항 정의
├── checkpoint.md            # 현재 체크포인트
├── context/
│   ├── analysis-result.md   # Phase 1 분석 결과
│   ├── questions-result.md  # Phase 2 질문 결과
│   └── plan-result.md       # Phase 3 계획
├── results/
│   └── task-X.X.md          # Agent 작업 결과
└── archived/
```

### checkpoint.md 형식

```markdown
# Modify Workflow Checkpoint

## 현재 상태
- 작업명: [작업명]
- 현재 Phase: [1-6]
- 현재 작업: [작업 번호]
- 마지막 업데이트: YYYY-MM-DD HH:MM

## 다음 단계
- 다음 Phase: [Phase 번호]
- 다음 작업: [작업 설명]
- 담당 Agent: [Agent 타입]

## 재개 명령어
앱 수정 워크플로우 재개

## 컨텍스트 파일 참조
- modify-todo.md: .workflow/modify-todo.md
- 분석 결과: .workflow/context/analysis-result.md
```

### 워크플로우 재개

```
앱 수정 워크플로우 재개
/app-modify-workflow resume
```

---

## 주의사항

1. **기존 기능 보존**: 수정 시 기존 동작이 깨지지 않도록 주의
2. **테스트 필수**: 수정 전후 테스트로 회귀 방지
3. **에러 처리 원칙 준수**: CLAUDE.md의 에러 처리 원칙 (rethrow 등)
4. **단일 modify-todo.md**: 동시에 하나의 수정 작업만 진행
5. **리뷰 반복 제한**: 최대 3회 (초과 시 사용자 확인)
6. **사용자 확인**: Phase 2, 3에서 반드시 사용자 승인 필요
7. **엣지 케이스 처리**: 식별된 엣지 케이스는 반드시 처리

---

## 전체 흐름 예시

### 사용자 요청

```
사용자: 앱 수정 워크플로우로 결제수단 관리 화면의 UX를 개선해줘
```

### 실행 과정

```
[Phase 1] 현황 분석
   -> 코드 분석: PaymentMethodManagementPage, 관련 위젯 분석
   -> UI/UX 파악: 현재 레이아웃, 인터랙션 분석
   -> 엣지 케이스: 빈 목록, 긴 이름, 삭제 확인 등 식별

[Phase 2] 요구사항 명확화
   -> 질문: "UI 개선 방향은?", "우선 엣지 케이스는?"
   -> 사용자 답변: "레이아웃 재구성", "에러 처리 우선"
   -> 요구사항 정리: modify-requirements.md 생성

[Phase 3] 계획 수립
   -> EnterPlanMode 진입
   -> 상세 계획 작성 (파일별 변경 사항, 단계별 작업)
   -> ExitPlanMode로 사용자 승인

[Phase 4] 구현
   -> modify-todo.md 생성: 8개 작업 정의
   -> 1.1 Explore -> 완료: "의존성 확인"
   -> 2.1 tdd-developer -> 완료: "리스트 구조 변경"
   -> 2.2 general-purpose -> 완료: "UI 개선"
   -> 3.1 tdd-developer -> 완료: "빈 상태 처리"

[Phase 5] 코드 리뷰 반복
   -> 1차 리뷰: "에러 메시지 개선 필요"
   -> 재작업: 에러 UI 수정
   -> 2차 리뷰: 통과

[Phase 6] 완료
   -> flutter test: 통과
   -> flutter analyze: 통과
   -> 결과 보고
   -> modify-todo.md 아카이브
```
