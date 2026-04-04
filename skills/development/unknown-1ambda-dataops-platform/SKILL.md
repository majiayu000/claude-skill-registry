# Phase Tracking Skill

다단계(Multi-Phase) 기능 구현을 체계적으로 추적하고 관리하는 프로세스.

## 문제 배경

Agent가 Phase 1 MVP 완료 후 Phase 2 항목을 방치하는 문제:
- Phase 2 항목이 "Future Work" 문서로 이동 후 능동적 추적 종료
- "MVP 완료" 선언 후 나머지 항목 시작 트리거 없음
- 외부 의존성 항목이 무기한 대기
- 전체 기능 완료까지의 진행률 파악 어려움

## 적용 시점

이 skill은 다음 상황에서 적용:
- *_FEATURE.md에서 Phase 1/2 구분 발견 시
- "Phase N complete" 선언 시
- `gap-analysis`에서 Phase 2 항목 발견 시
- 사용자가 phase 상태 요청 시

---

## Phase 식별 기준

### FEATURE 문서에서 Phase 마커 인식

```markdown
### 인식 패턴

| 패턴 | Phase |
|------|-------|
| "Phase 1", "Phase 1 MVP", "MVP" | Phase 1 |
| "Phase 2", "Future", "향후" | Phase 2 |
| "Phase 3", "Long-term" | Phase 3 |
| 테이블 내 "MVP ✅" | Phase 1 |
| 테이블 내 "Phase 2" 열 | Phase 2 |

### 예시

```markdown
## 1.3 주요 기능

| 기능 | MVP |
|------|-----|
| Quality Spec YML | ✅ |
| Generic Tests | ✅ |
| Airflow DAG | Phase 2 |
| Slack 알림 | Phase 2 |
```

→ Phase 1: Quality Spec YML, Generic Tests
→ Phase 2: Airflow DAG, Slack 알림
```

---

## Phase 관리 프로세스

### Step 1: Phase 파싱

*_FEATURE.md에서 Phase별 항목 추출:

```markdown
## Phase Structure: FEATURE_QUALITY

### Phase 1 (MVP)
| # | Item | Category |
|---|------|----------|
| 1 | Quality Spec YML schema | Core |
| 2 | QualityAPI (list, get, run, validate) | API |
| 3 | CLI commands (list, get, run, validate) | CLI |
| 4 | DLI-6xx error codes | Errors |
| 5 | Built-in Generic Tests (5 types) | Tests |

**Total:** 5 items

### Phase 1.5 (Server Integration) - Inferred
| # | Item | Dependency |
|---|------|------------|
| 1 | QualityAPI.run(mode=SERVER) | Basecamp Server API |
| 2 | QualityAPI.list/get (real server) | Basecamp Server API |

**Total:** 2 items
**Dependency:** feature-basecamp-server

### Phase 2 (Automation)
| # | Item | Dependency |
|---|------|------------|
| 1 | Airflow DAG generation | Airflow |
| 2 | Slack notifications | Basecamp Connect |
| 3 | Email notifications | Basecamp Connect |
| 4 | Expression test type | None |
| 5 | Row Count test type | None |
| 6 | Git Sync | TBD |
| 7 | Basecamp UI integration | Basecamp UI |

**Total:** 7 items
```

### Step 2: Phase 상태 추적

```markdown
## Phase Status: FEATURE_QUALITY

| Phase | Total | Complete | In Progress | Blocked | Status |
|-------|-------|----------|-------------|---------|--------|
| Phase 1 MVP | 5 | 5 | 0 | 0 | ✅ COMPLETE |
| Phase 1.5 | 2 | 0 | 0 | 2 | ⏳ BLOCKED |
| Phase 2 | 7 | 0 | 0 | 3 | ⏳ NOT STARTED |

**Overall Progress:** 5/14 (36%)

### Blockers

| Phase | Item | Blocked By |
|-------|------|------------|
| 1.5 | SERVER mode | Basecamp Server API 미구현 |
| 1.5 | Real server calls | Basecamp Server API 미구현 |
| 2 | Slack notifications | Basecamp Connect API 미구현 |
| 2 | Email notifications | Basecamp Connect API 미구현 |
| 2 | Basecamp UI | Basecamp UI 미구현 |
```

### Step 3: Phase 전환 관리

```markdown
## Phase Transition Checklist

### Phase 1 → Phase 1.5 전환 조건

- [x] Phase 1 모든 항목 구현 완료
- [x] completion-gate PASSED
- [x] gap-analysis에서 Phase 1 BLOCKER 없음
- [ ] Phase 1.5 의존성 해결됨

**Status:** Phase 1.5 전환 대기 (의존성 미해결)

### Phase 1.5 → Phase 2 전환 조건

- [ ] Phase 1.5 모든 항목 구현 완료
- [ ] SERVER 모드 E2E 테스트 통과
- [ ] Phase 2 시작 의사결정 완료
```

---

## Phase 상태 정의

### Phase 상태 값

| Status | 의미 | 다음 액션 |
|--------|------|----------|
| `NOT_STARTED` | 시작 전 | 이전 Phase 완료 대기 |
| `IN_PROGRESS` | 진행 중 | 계속 구현 |
| `BLOCKED` | 의존성 대기 | 의존성 해결 요청 |
| `COMPLETE` | 완료 | 다음 Phase 전환 |
| `DEFERRED` | 연기됨 | 사유 문서화 |

### Phase 완료 기준

```markdown
## Phase Complete 조건

### Phase N 완료 선언 가능 조건

1. **모든 항목 구현**: Phase N 항목 100% 구현
2. **테스트 통과**: 관련 테스트 모두 PASS
3. **BLOCKER 없음**: gap-analysis에서 BLOCKER 0개
4. **문서화 완료**: *_RELEASE.md 작성

### Phase N 부분 완료 (Partial)

의존성으로 인해 일부 미완료 시:
- 완료된 항목 목록 명시
- 미완료 항목 사유 기록
- 예상 해결 시점 기록
```

---

## Phase 백로그 관리

### 자동 백로그 생성

Phase 1 완료 시 자동으로 Phase 2 백로그 생성:

```markdown
## Phase 2 Backlog: QUALITY

> Auto-generated from gap-analysis
> Created: {DATE}

### Backlog Items

| # | Item | Priority | Dependency | Owner | Status |
|---|------|----------|------------|-------|--------|
| 1 | SERVER mode execution | P0 | Basecamp Server | TBD | Blocked |
| 2 | Airflow DAG generation | P1 | Airflow | TBD | Not Started |
| 3 | Slack notifications | P1 | Basecamp Connect | TBD | Blocked |
| 4 | Email notifications | P2 | Basecamp Connect | TBD | Blocked |
| 5 | expression test type | P2 | None | feature-interface-cli | Not Started |
| 6 | row_count test type | P2 | None | feature-interface-cli | Not Started |
| 7 | Git Sync | P3 | TBD | TBD | Not Started |

### Dependency Summary

| Dependency | Items Blocked | Contact |
|------------|---------------|---------|
| Basecamp Server API | 1 | feature-basecamp-server |
| Basecamp Connect API | 2 | feature-basecamp-connect |
| Airflow | 1 | expert-devops-cicd |
```

### 우선순위 할당 기준

| Priority | 기준 | 예시 |
|----------|------|------|
| **P0** | Phase 1 항목 중 외부 의존성으로 Blocked | SERVER mode (Basecamp Server API 필요) |
| **P1** | 핵심 기능 확장 (Phase 2 필수) | Airflow DAG 생성, 알림 기능 |
| **P2** | 부가 기능 (Phase 2 선택) | 추가 테스트 타입, Git Sync |
| **P3** | Nice-to-have | UI 연동, 고급 옵션 |

### 백로그 → Serena Memory 저장

```python
# Phase 백로그를 Serena memory에 저장
mcp__serena__write_memory(
    memory_file_name="quality_phase2_backlog",
    content="""
# Quality Feature Phase 2 Backlog

## Items
1. SERVER mode - P0, Blocked (Basecamp Server)
2. Airflow DAG - P1, Not Started
...

## Last Updated: {DATE}
"""
)
```

---

## Phase 진행 보고

### 진행률 요약

```markdown
## Phase Progress Report: QUALITY

**Report Date:** 2026-01-01
**Feature:** Quality Spec

### Progress Overview

```
Phase 1 MVP:  [████████████████████] 100%  ✅
Phase 1.5:    [                    ]   0%  ⏳ Blocked
Phase 2:      [                    ]   0%  ⏳ Not Started
──────────────────────────────────────────
Overall:      [███████             ]  36%
```

### Timeline

| Phase | Start | End | Duration |
|-------|-------|-----|----------|
| Phase 1 MVP | 2025-12-30 | 2025-12-31 | 1 day |
| Phase 1.5 | TBD | TBD | - |
| Phase 2 | TBD | TBD | - |

### Blockers to Resolve

| Blocker | Impact | Resolution Path |
|---------|--------|-----------------|
| Basecamp Server API | Phase 1.5 blocked | Request API from basecamp-server team |
| Basecamp Connect API | Phase 2 Slack/Email blocked | Request API from connect team |
```

---

## completion-gate 연동

`completion-gate` 강화를 위한 Phase 경계 검사:

```markdown
## Completion Gate: Phase Boundary Check

### Phase 1 MVP 완료 선언 시

```
completion-gate PASSED (코드/테스트)
       ↓
[phase-tracking skill]
       ↓
Phase 1 항목 100% 확인
       ↓
  ┌─────────────────────────────┐
  │ Phase 2 항목 존재 시        │
  │  → 백로그 자동 생성        │
  │  → "Phase 1 Complete" 허용 │
  └─────────────────────────────┘
       ↓
"Phase 1 MVP Complete" 승인
+ "Phase 2 백로그 생성됨" 안내
```

### 출력 예시

```markdown
## Completion Gate: PASSED (Phase 1 MVP) ⚠️

### Code/Test Verification: ✅ PASSED
[기존 completion-gate 결과]

### Phase Boundary: Phase 2 Items Pending

Phase 1 MVP 완료가 승인되었습니다.

| Phase | Status |
|-------|--------|
| Phase 1 MVP | ✅ Complete (5/5) |
| Phase 1.5 | ⏳ Blocked (0/2) |
| Phase 2 | ⏳ Not Started (0/7) |

### Phase 2 Backlog Created

다음 항목이 Phase 2 백로그로 등록되었습니다:
1. SERVER mode execution (P0)
2. Airflow DAG generation (P1)
3. Slack notifications (P1)
... (7 items total)

### Declaration Options

1. **"Phase 1 MVP Complete"** ✅
   - STATUS.md: Phase 1 ✅, Phase 2 ⏳
   - Phase 2 백로그 추적 시작

2. **"Feature Complete"** ❌ (불가)
   - Phase 2 항목 존재로 전체 완료 불가
```

---

## 관련 Skills

- `gap-analysis`: Gap 분석에서 Phase 항목 식별 (선행)
- `completion-gate`: 완료 조건 검증 + Phase 경계 검사
- `dependency-coordination`: 의존성 추적 (후속)
- `implementation-checklist`: 항목별 구현 추적

---

## Agent Integration

### feature-interface-cli Agent 워크플로우

```markdown
## Multi-Phase Feature Workflow

### FEATURE 문서 수신 시

1. **Phase 파싱**
   - *_FEATURE.md에서 Phase 1/2 항목 추출
   - phase-tracking으로 구조 생성

2. **Phase 1 구현**
   - implementation-checklist로 Phase 1 항목 추적
   - 구현 완료 시 completion-gate 실행

3. **Phase 1 완료 선언**
   - completion-gate PASSED
   - phase-tracking으로 Phase 2 백로그 생성
   - "Phase 1 MVP Complete" 선언

4. **Phase 2 준비**
   - 백로그 항목 우선순위 확인
   - 의존성 해결 요청 (dependency-coordination)
   - Phase 2 시작 시점 결정
```

### Serena Memory 활용

```python
# Phase 상태 저장
mcp__serena__write_memory(
    "cli_phase_status",
    """
# CLI Feature Phase Status

## Quality
- Phase 1: Complete
- Phase 1.5: Blocked (Basecamp Server API)
- Phase 2: Not Started

## Workflow
- Phase 1: Complete
- Phase 2: Not Started

## Catalog
- Phase 1: Complete
- Phase 2: Partial
"""
)
```

---

## 사용 예시

```markdown
# Phase 상태 확인
"Quality 기능 phase 상태 보여줘"
→ phase-tracking 실행, 진행률 출력

# Phase 전환
"Phase 1 완료, Phase 2 백로그 생성해줘"
→ Phase 2 백로그 자동 생성

# 전체 진행률
"전체 기능 phase 진행률 보여줘"
→ 모든 FEATURE의 Phase 상태 요약
```
