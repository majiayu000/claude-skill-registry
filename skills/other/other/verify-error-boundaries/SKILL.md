---
name: verify-error-boundaries
description: ErrorBoundary + fallback UI + 에러 복구 패턴을 검증합니다. 컴포넌트 에러 처리 수정 후 사용.
---

## Purpose

1. **ErrorBoundary 래핑** - lazy 로드되는 주요 탭이 ErrorBoundary로 보호되는지 검증
2. **fallback UI** - 에러 발생 시 사용자에게 적절한 대체 UI가 표시되는지 검증
3. **에러 복구 메커니즘** - ErrorBoundary에 재시도/복구 기능이 있는지 검증
4. **중첩 ErrorBoundary** - 세부 영역에서 에러가 전체 탭을 중단시키지 않는지 검증

## When to Run

- `components/Common/ErrorBoundary.tsx` 수정 후
- `components/Layout/TabContent.tsx`의 에러 처리를 변경한 후
- 새로운 탭이나 대형 모달 컴포넌트를 추가한 후
- lazy import 패턴을 변경한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/Common/ErrorBoundary.tsx` | ErrorBoundary 클래스 컴포넌트 |
| `components/Common/VideoLoading.tsx` | Suspense fallback |
| `components/Layout/TabContent.tsx` | 탭 라우팅 (ErrorBoundary + Suspense 래핑) |
| `components/Layout/ModalManager.tsx` | 글로벌 모달 관리 |
| `index.tsx` | 앱 진입점 (최상위 ErrorBoundary) |

## Workflow

### Step 1: ErrorBoundary 컴포넌트 존재 및 구현 검증

**검사:** ErrorBoundary 파일이 존재하고 React Error Boundary 패턴(getDerivedStateFromError, componentDidCatch)을 구현하는지 확인합니다.

```bash
ls components/Common/ErrorBoundary.tsx 2>/dev/null || echo "MISSING"
grep -n "getDerivedStateFromError\|componentDidCatch\|hasError\|ErrorBoundary" components/Common/ErrorBoundary.tsx 2>/dev/null | head -10
```

**PASS 기준:** 파일 존재 + getDerivedStateFromError 또는 componentDidCatch 구현
**FAIL 기준:** ErrorBoundary 파일 누락 또는 필수 메서드 미구현

### Step 2: TabContent의 ErrorBoundary 래핑 검증

**검사:** TabContent.tsx에서 lazy 로드된 탭이 ErrorBoundary로 감싸져 있는지 확인합니다.

```bash
grep -n "ErrorBoundary" components/Layout/TabContent.tsx | head -5
```

**PASS 기준:** ErrorBoundary import 및 래핑 존재
**FAIL 기준:** lazy 컴포넌트가 ErrorBoundary 없이 렌더링

**수정:** `<ErrorBoundary><Suspense fallback={...}>...</Suspense></ErrorBoundary>` 패턴 적용

### Step 3: 최상위 ErrorBoundary 검증

**검사:** index.tsx 또는 App.tsx에서 앱 전체를 감싸는 최상위 ErrorBoundary가 있는지 확인합니다.

```bash
grep -n "ErrorBoundary" index.tsx App.tsx 2>/dev/null | head -10
```

**PASS 기준:** 최상위 레벨에 ErrorBoundary 존재
**FAIL 기준:** 앱 전체를 보호하는 ErrorBoundary 없음

### Step 4: ErrorBoundary fallback UI 검증

**검사:** ErrorBoundary에 에러 표시 및 복구 UI가 포함되어 있는지 확인합니다.

```bash
grep -n "fallback\|retry\|reset\|다시\|재시도\|새로고침" components/Common/ErrorBoundary.tsx 2>/dev/null | head -10
```

**PASS 기준:** 에러 메시지 표시 + 재시도/복구 버튼 존재
**FAIL 기준:** 에러 발생 시 빈 화면 또는 에러 메시지만 표시

### Step 5: Suspense fallback 일관성 검증

**검사:** VideoLoading이 존재하고 Suspense의 fallback으로 사용되는지 확인합니다.

```bash
ls components/Common/VideoLoading.tsx 2>/dev/null || echo "MISSING"
grep -c "VideoLoading\|TabLoadingFallback" components/Layout/TabContent.tsx 2>/dev/null
```

**PASS 기준:** VideoLoading 존재 + TabContent에서 fallback으로 사용
**FAIL 기준:** fallback 컴포넌트 누락

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | ErrorBoundary 구현 | ErrorBoundary.tsx | PASS/FAIL | |
| 2 | TabContent 래핑 | TabContent.tsx | PASS/FAIL | |
| 3 | 최상위 ErrorBoundary | index.tsx/App.tsx | PASS/FAIL | |
| 4 | fallback UI 존재 | ErrorBoundary.tsx | PASS/FAIL | |
| 5 | Suspense fallback | VideoLoading.tsx | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **ModalManager의 ErrorBoundary 부재** - 모달은 TabContent의 ErrorBoundary 아래에서 렌더되므로 별도 ErrorBoundary 불필요
2. **함수형 ErrorBoundary 사용** - react-error-boundary 라이브러리의 함수형 패턴을 사용하는 것도 유효
3. **서브매니저의 개별 ErrorBoundary 부재** - 부모(TabContent)의 ErrorBoundary가 커버하므로, 서브매니저마다 별도 ErrorBoundary는 선택사항
