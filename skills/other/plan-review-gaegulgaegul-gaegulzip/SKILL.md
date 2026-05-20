---
name: plan-review
description: |
  설계/코드의 체계적 리뷰를 수행합니다.
  PDCA 두 시점에서 사용:
  - Design → Do 사이: brief.md 기반 설계 리뷰 (Architecture + Test 전략)
  - Analyze 단계: 실제 코드 기반 코드 리뷰 (Code Quality + Tests + Performance)

  BIG CHANGE (섹션당 최대 4이슈) / SMALL CHANGE (섹션당 1이슈) 모드 선택.
  각 이슈마다 트레이드오프 분석 + 추천 옵션 + 사용자 확인.

  "리뷰해줘", "설계 리뷰", "코드 리뷰", "plan-review" 요청 시 사용합니다.
argument-hint: "[design|code] [feature]"
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__search_for_pattern
  - mcp__plugin_serena_serena__find_referencing_symbols
---

# Plan Review Skill

> Engineering Preferences(`.claude/guide/engineering-preferences.md`) 기반의 체계적 리뷰.
> PDCA 워크플로우의 **Design → Do 사이** 및 **Analyze 단계**에서 사용.

## 엔지니어링 기준 (필수 참조)

리뷰 시작 전 반드시 읽기:
```
Read(".claude/guide/engineering-preferences.md")
```

5가지 기준으로 이슈를 판단합니다:
1. **DRY** — 반복 공격적 제거
2. **테스트** — 적은 것보다 많은 것
3. **적정 엔지니어링** — 부족하지도 과하지도 않게
4. **Edge Case** — 시스템 경계에서 적극, 내부에서 최소
5. **Explicit > Clever** — 명시적 우선

---

## Arguments

| Argument | 설명 | PDCA 시점 |
|----------|------|-----------|
| `design [feature]` | brief.md 기반 설계 리뷰 | Design → Do 사이 |
| `code [feature]` | 구현 코드 기반 코드 리뷰 | Analyze 단계 |

인자 없이 호출하면 `.pdca-status.json`의 현재 phase로 자동 판별:
- phase = `design` → design 모드
- phase = `do` 또는 `check` → code 모드

---

## Step 0: 리뷰 규모 선택 (공통)

```
AskUserQuestion(
  question: "리뷰 규모를 선택해주세요",
  options: [
    { label: "BIG CHANGE", description: "섹션당 최대 4개 이슈. 대규모 변경, 새 기능에 적합" },
    { label: "SMALL CHANGE", description: "섹션당 1개 이슈. 버그 수정, 소규모 변경에 적합" }
  ]
)
```

- **BIG CHANGE**: 4개 섹션 × 최대 4이슈 = 최대 16이슈
- **SMALL CHANGE**: 4개 섹션 × 1이슈 = 최대 4이슈

---

## Design 모드 (설계 리뷰)

### 대상 문서
```
Read("docs/{product}/{feature}/{platform}-brief.md")
Read("docs/{product}/{feature}/{platform}-design-spec.md")  # Mobile/Web
Read("docs/{product}/{feature}/api-contract.md")              # Fullstack
Read("docs/{product}/{feature}/user-story.md")
```

### 리뷰 섹션

#### Section 1: Architecture (설계 구조)
- 시스템 설계와 컴포넌트 경계
- 의존성 그래프와 결합도
- 데이터 흐름 패턴과 잠재 병목
- 확장성 특성과 단일 장애 지점
- 보안 아키텍처 (인증, 데이터 접근, API 경계)

#### Section 2: 테스트 전략
- brief.md의 Test Scenarios 완전성
- 누락된 엣지 케이스 시나리오
- 실패 모드와 에러 경로 커버리지
- 통합 테스트 필요 지점

#### Section 3: 설계 품질
- DRY 위반 가능성 (중복 API, 중복 스키마)
- 과잉/부족 설계 영역
- 누락된 에러 핸들링 시나리오 (시스템 경계)
- 기술 부채 위험 영역

#### Section 4: 성능 예측
- N+1 쿼리 위험 패턴
- 캐싱 전략 필요성
- 대용량 데이터 처리 고려
- API 응답 크기 최적화

---

## Code 모드 (코드 리뷰)

### 대상 코드
```
# 플랫폼별 소스 디렉토리
Glob("apps/server/src/modules/{feature}/**")     # Server
Glob("apps/mobile/apps/wowa/lib/app/modules/{feature}/**")  # Mobile
Glob("apps/web/admin/app/**/{feature}*/**")      # Web

# 테스트 파일
Glob("apps/server/src/modules/{feature}/**/*.test.ts")
```

### 리뷰 섹션

#### Section 1: Architecture (코드 구조)
- 실제 컴포넌트 경계와 모듈 분리
- 의존성 방향과 순환 참조
- 데이터 흐름의 실제 구현
- brief.md 설계와 구현의 정합성

#### Section 2: Code Quality (코드 품질)
- 코드 조직과 모듈 구조
- DRY 위반 — 공격적으로 탐지
- 에러 핸들링 패턴과 누락된 엣지 케이스
- 기술 부채 핫스팟
- 과잉/부족 엔지니어링 영역

#### Section 3: Tests (테스트)
- 테스트 커버리지 갭 (단위, 통합, E2E)
- 테스트 품질과 assertion 강도
- 누락된 엣지 케이스 커버리지
- 테스트되지 않은 실패 모드와 에러 경로

#### Section 4: Performance (성능)
- N+1 쿼리와 DB 접근 패턴
- 메모리 사용 우려
- 캐싱 기회
- 느리거나 높은 복잡도의 코드 경로

---

## 이슈 출력 포맷 (양 모드 공통)

각 섹션의 이슈를 아래 형식으로 출력합니다.
이슈는 **번호**, 옵션은 **레터**로 표기합니다.

```markdown
### Issue #N: [이슈 제목]

**파일**: `path/to/file.ts:42` (code 모드) 또는 `brief.md Section 3` (design 모드)
**심각도**: CRITICAL / HIGH / MEDIUM / LOW

**문제**: [구체적 설명]

**옵션**:

| 옵션 | 설명 | 구현 난이도 | 리스크 | 다른 코드 영향 | 유지보수 부담 |
|------|------|------------|-------|--------------|-------------|
| **A (추천)** | [추천 옵션] | 낮음 | 낮음 | 없음 | 낮음 |
| **B** | [대안] | 중간 | 중간 | 일부 | 중간 |
| **C** | Do nothing | — | [리스크 설명] | — | — |

**추천: A** — [추천 이유, engineering-preferences 기준 근거]
```

### 섹션별 사용자 확인

각 섹션 완료 후 반드시 `AskUserQuestion`으로 확인합니다:

```
AskUserQuestion(
  question: "[Section명] 리뷰 결과입니다. 각 이슈의 옵션을 선택해주세요.",
  options: [
    { label: "#1-A, #2-A, #3-B (추천 따름)", description: "추천 옵션 기반 선택" },
    { label: "커스텀 선택", description: "이슈별로 다른 옵션을 선택하고 싶습니다" }
  ]
)
```

**다음 섹션은 현재 섹션의 사용자 피드백을 받은 후에만 진행합니다.**

---

## PDCA 연동

### Design → Do 사이 (`/pdca do` 실행 전)

PDCA Skill의 Do 단계에서 선행조건 검증 후, CTO 작업 분배 전에 선택적으로 호출:

```
# pdca/SKILL.md의 Do Step 0.5에서 호출
Skill("plan-review", args="design {feature}")
```

### Analyze 단계 (`/pdca analyze` 실행 시)

gap-detector 실행 후, CTO 통합 리뷰 전에 선택적으로 호출:

```
# pdca/SKILL.md의 Analyze Step 1.5에서 호출
Skill("plan-review", args="code {feature}")
```

---

## 리뷰 완료 후

1. 사용자가 선택한 옵션을 기반으로 **Action Items** 요약 생성
2. Design 모드: brief.md 수정 사항 목록 → 해당 Tech Lead에게 전달
3. Code 모드: 코드 수정 사항 목록 → FINDINGS 형태로 `analysis.md`에 추가
4. 다음 PDCA 단계로 진행
