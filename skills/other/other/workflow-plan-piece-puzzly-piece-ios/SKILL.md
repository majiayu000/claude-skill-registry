---
name: _workflow-plan
version: 1.0.0
description: 코드 분석 + 작업 계획 수립 (🔴 Complex 모드)
user-invocable: false
---

# Workflow Plan Skill

> 🔴 **Complex 모드 전용** - `/workflow`에서 복잡도 🔴 선택 시 자동 호출됩니다.
>
> 🟢 Simple, 🟡 Medium 모드에서는 이 스킬을 사용하지 않습니다.

spec.md를 기반으로 **코드베이스 분석**과 **작업 계획 수립**을 함께 수행합니다.

> ⚠️ 기존 analyze 단계가 이 스킬에 통합되었습니다.

## 전제 조건

- `.claude/work-docs/spec.md` 파일이 존재해야 함
- spec.md의 status가 `spec`이어야 함

## 목적

1. **코드베이스 분석** (기존 analyze 역할)
   - 영향 받는 도메인/모듈 파악
   - 수정 대상 파일 목록 도출
   - 재사용 가능한 코드 발견
   - 참고할 패턴 파악

2. **작업 계획 수립** (기존 plan 역할)
   - 작업 순서 및 의존성 파악
   - Phase별 작업 그룹화
   - 병렬 실행 가능 여부 결정

## 실행 워크플로우

### Step 1: spec.md 읽기

```
.claude/work-docs/spec.md
```

분석할 요구사항 파악:
- 필요한 기능 목록
- API 엔드포인트
- UI 컴포넌트

### Step 2: 코드베이스 분석 (researcher 에이전트 활용)

```typescript
Task({
  subagent_type: "researcher",
  model: "sonnet",
  prompt: `## 목적
spec.md의 요구사항 구현을 위한 코드베이스 분석

## 분석 대상
${spec.md 내용 요약}

## 질문
1. 영향 받는 도메인/모듈은?
2. 수정이 필요한 파일은?
3. 참고할 기존 패턴은?
4. 재사용 가능한 코드는?
5. 테스트 환경은 어떤가?`
})
```

**분석 항목**:
| 항목 | 내용 |
|------|------|
| 영향 범위 | 도메인, 모듈 목록 |
| 수정 파일 | 기존 파일 중 수정 필요 |
| 신규 파일 | 새로 생성할 파일 |
| 참고 패턴 | 유사 기능 기존 구현 |
| 재사용 코드 | 활용 가능한 유틸/뷰모델/뷰 |
| 테스트 분석 | 테스트 파일 위치, Mock 필요 |

### Step 3: 작업 계획 수립 (planner 에이전트 활용)

researcher 분석 결과를 바탕으로 **planner** 에이전트가 구체적인 작업 계획을 수립합니다.

```typescript
Task({
  subagent_type: "planner",
  model: "opus",
  prompt: `## 목적
${이슈번호} 구현을 위한 작업 계획 수립

## 요구사항 요약
${spec.md 핵심 내용}

## 분석 결과
${researcher 에이전트 분석 결과}

## 제약사항
- TDD 필수 대상: ViewModel, Service, Util

## 출력 요구사항
- Phase별 작업 목록 (기존 형식)
- Execution Groups (implementer용 Task 분할)
- Task Details (각 Task 상세 정보)`
})
```

**planner 출력 항목**:

| 항목 | 내용 |
|------|------|
| 파일 변경 요약 | 신규/수정 파일 목록 |
| Phase별 작업 | 의존성 기반 그룹화 |
| 실행 순서 | 시각화된 의존성 맵 |
| **Execution Groups** | implementer용 Task 그룹 |
| **Task Details** | 각 Task 상세 정보 (yaml 형식) |
| TDD 대상 | 🧪 표시된 작업 목록 |
| 리스크 | 주의사항 및 잠재 문제 |

### Step 4: plan.md 생성

`.claude/work-docs/plan.md` 파일 생성

## plan.md 템플릿

```markdown
---
feature: {기능명}
status: plan
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# {기능명} - 작업 계획

## 📊 분석 요약

### 영향 범위
| 도메인 | 설명 |
|--------|------|
| Auth | 인증 관련 기능 |

### 수정 파일
| 파일 | 수정 내용 |
|------|----------|
| `Services/AuthService.swift` | API 함수 추가 |

### 신규 파일
| 파일 | 설명 |
|------|------|
| `ViewModels/XxxViewModel.swift` | 새 ViewModel |

### 참고 패턴
| 파일 | 참고 내용 |
|------|----------|
| `ViewModels/LoginViewModel.swift` | ViewModel 구조, 에러 처리 |

### 재사용 코드
| 항목 | 위치 | 용도 |
|------|------|------|
| `CountdownTimer` | `Utils/` | 타이머 기능 |

## 📝 작업 목록

> 🧪 표시된 작업은 TDD 사이클로 진행

### Phase 1: 기반 작업 ⚡ 병렬 가능

| # | 작업 | 파일 | 의존성 | TDD |
|---|------|------|--------|-----|
| 1 | 모델 정의 | `Models/Xxx.swift` | 없음 | - |
| 2 | API 서비스 함수 | `Services/XxxService.swift` | 없음 | - |

### Phase 2: 로직 구현

| # | 작업 | 파일 | 의존성 | TDD |
|---|------|------|--------|-----|
| 3 | ViewModel 구현 | `ViewModels/XxxViewModel.swift` | 1, 2 | 🧪 |

### Phase 3: UI 구현

| # | 작업 | 파일 | 의존성 | TDD |
|---|------|------|--------|-----|
| 4 | 서브뷰 구현 | `Views/Xxx/XxxDetailView.swift` | - | - |
| 5 | 메인뷰 조립 | `Views/Xxx/XxxView.swift` | 3, 4 | - |

### Phase 4: 마무리

| # | 작업 | 파일 | 의존성 | TDD |
|---|------|------|--------|-----|
| 6 | 통합 검증 | - | 5 | - |

## 🔄 실행 순서 시각화

```
[1] 모델 정의 ──┐
               ├──→ [3] ViewModel 구현 🧪 ──→ [5] 메인뷰 조립 ──→ [6] 검증
[2] API 서비스 ─┘             ↑
                              │
                   [4] 서브뷰 ─┘
```

## 🚀 Execution Groups

> implementer 에이전트가 병렬 실행하는 Task 그룹

### Group 1 (independent) ⚡
| TaskId | Files | Description | Est |
|--------|-------|-------------|-----|
| 1-A | Xxx.swift | 모델 정의 | S |
| 1-B | XxxService.swift | API 서비스 | S |

### Group 2 (depends: Group 1)
| TaskId | Files | Description | Est |
|--------|-------|-------------|-----|
| 2-A | XxxViewModel.swift, XxxViewModelTests.swift | ViewModel + 테스트 🧪 | M |

### Group 3 (depends: Group 2)
| TaskId | Files | Description | Est |
|--------|-------|-------------|-----|
| 3-A | XxxDetailView.swift | 서브뷰 구현 | M |
| 3-B | XxxView.swift | 메인뷰 조립 | M |

### Group 4 (depends: Group 3)
| TaskId | Files | Description | Est |
|--------|-------|-------------|-----|
| 4-A | - | 통합 검증 | S |

## 📋 Task Details

### Task 1-A
```yaml
taskId: "1-A"
files:
  - Models/Xxx.swift
description: |
  - API 요청/응답 모델 정의 (Codable)
  - 상태 관련 enum 정의
refPatterns:
  - "Models/Auth.swift:1-30"
specSummary: |
  - 요청: XxxRequest (code: String)
  - 응답: XxxResponse (token: String, user: User)
outputForNext: |
  - XxxRequest, XxxResponse 모델 정의됨
```

### Task 1-B
```yaml
taskId: "1-B"
files:
  - Services/XxxService.swift
description: |
  - API 함수 구현 (async/await)
  - 에러 처리 포함
refPatterns:
  - "Services/AuthService.swift:10-40"
specSummary: |
  - POST /api/xxx
  - Bearer 토큰 필요
outputForNext: |
  - XxxService 클래스 정의됨
```

### Task 2-A
```yaml
taskId: "2-A"
files:
  - ViewModels/XxxViewModel.swift
  - Tests/XxxViewModelTests.swift
description: |
  - ViewModel 구현 (TDD)
  - @Published 상태 관리 + API 호출
refPatterns:
  - "ViewModels/LoginViewModel.swift:1-50"
specSummary: |
  - 상태: idle, loading, success, error
  - 자동 재시도: 1회
outputForNext: |
  - XxxViewModel 클래스 정의됨
tdd: true
```

## 🧪 TDD 작업 요약

| 작업 # | 대상 | 테스트 파일 |
|--------|------|------------|
| 2-A | XxxViewModel | `Tests/XxxViewModelTests.swift` |

## ⚠️ 주의사항

- [ ] 기존 함수 시그니처 유지
- [ ] 프로젝트 컨벤션 준수
- [ ] 파일 충돌 주의 (동일 파일 = 동일 Task)
```

## 완료 후 처리

### spec.md 상태 업데이트

spec.md의 frontmatter 상태 업데이트:
```yaml
status: plan
```

### 완료 메시지

```
✅ plan.md 생성 완료

📁 파일: .claude/work-docs/plan.md

📊 분석 요약:
- 영향 도메인: 2개
- 수정 파일: 3개
- 신규 파일: 2개
- 참고 파일: 4개

📋 작업 요약:
- 총 작업: 6개
- Phase 수: 4개
- 병렬 가능: Phase 1 (2개 작업)

🧪 TDD 작업: N개

▶️ 다음 단계: /workflow implement 실행
```

**중요**: 완료 메시지 출력 후 **스킬을 종료**합니다.

## 금지 사항

1. **코드 수정 금지**: 계획 수립만 수행, 실제 구현은 implement 단계에서
2. **별도 analyze.md 생성 금지**: plan.md에 분석 내용 통합
3. **spec.md 수정 금지**: 읽기만 함
