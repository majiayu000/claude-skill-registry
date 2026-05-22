---
name: verify-lazy-loading
description: 탭/모달의 React.lazy + Suspense + ErrorBoundary 패턴을 검증합니다. 탭 컴포넌트 추가/수정 후 사용.
---

## Purpose

1. **Lazy import 일관성** - TabContent.tsx의 모든 탭 컴포넌트가 React.lazy()로 import되는지 검증
2. **Suspense 래핑** - lazy 컴포넌트가 Suspense로 감싸져 있고 적절한 fallback이 있는지 검증
3. **ErrorBoundary 존재** - TabContent 전체가 ErrorBoundary로 감싸져 있는지 검증
4. **ModalManager 패턴** - 모달 컴포넌트도 lazy load되는지 검증
5. **TimetableManager 패턴** - 시간표 내부의 lazy import가 유지되는지 검증

## When to Run

- `components/Layout/TabContent.tsx`에 새 탭을 추가한 후
- `components/Layout/ModalManager.tsx`에 새 모달을 추가한 후
- `components/Timetable/TimetableManager.tsx`의 lazy import를 수정한 후
- 번들 사이즈 최적화 작업 후
- 새로운 탭 레벨 매니저 컴포넌트를 생성한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/Layout/TabContent.tsx` | 탭 라우팅 (32개 React.lazy import + Suspense + ErrorBoundary) |
| `components/Layout/ModalManager.tsx` | 글로벌 모달 관리 (4개 React.lazy import + Suspense) |
| `components/Timetable/TimetableManager.tsx` | 시간표 매니저 (7개 lazy import + Suspense) |
| `components/Common/ErrorBoundary.tsx` | ErrorBoundary 컴포넌트 |
| `components/Common/VideoLoading.tsx` | 로딩 fallback 컴포넌트 |
| `components/StudentManagement/StudentManagementTab.tsx` | 학생 관리 탭 (5개 lazy import) |
| `components/Dashboard/roles/MasterDashboard.tsx` | 마스터 대시보드 (3개 lazy import) |
| `components/StudentConsultation/ConsultationManagementTab.tsx` | 상담 관리 탭 (2개 lazy import) |
| `components/RegistrationConsultation/ConsultationManager.tsx` | 등록 상담 매니저 (2개 lazy import) |
| `components/Embed/EmbedRouter.tsx` | 임베드 라우터 (2개 lazy import) |

## Workflow

### Step 1: TabContent lazy import 카운트 검증

**파일:** `components/Layout/TabContent.tsx`

**검사:** 모든 탭 컴포넌트가 React.lazy()로 import되어야 합니다. 현재 32개의 lazy import가 존재해야 합니다.

```bash
grep -c "React.lazy(" components/Layout/TabContent.tsx
```

**PASS 기준:** 30개 이상의 lazy import 존재 (탭 추가 시 증가 가능)
**FAIL 기준:** lazy import 수가 감소했거나, 직접 import로 전환된 탭이 있음

**추가 검증:** 직접 import된 대형 컴포넌트가 없는지 확인

```bash
grep -n "^import.*from '\.\./.*Manager\|^import.*from '\.\./.*Tab'" components/Layout/TabContent.tsx
```

**PASS 기준:** Manager/Tab 직접 import 없음 (모두 lazy)
**FAIL 기준:** 대형 컴포넌트가 직접 import됨

**수정:** `const Component = React.lazy(() => import('../Path/Component'))` 패턴으로 변경

### Step 2: TabContent Suspense + ErrorBoundary 래핑 검증

**파일:** `components/Layout/TabContent.tsx`

**검사:** ErrorBoundary로 전체 래핑, 각 탭이 Suspense로 감싸져 있어야 합니다.

```bash
grep -c "Suspense" components/Layout/TabContent.tsx
grep -n "ErrorBoundary" components/Layout/TabContent.tsx
```

**PASS 기준:**
- `Suspense` 10회 이상 사용 (각 탭 그룹마다 1개 이상)
- `ErrorBoundary` import 및 래핑 존재

**FAIL 기준:** Suspense 없이 lazy 컴포넌트 렌더링 (런타임 에러)

**수정:** `<Suspense fallback={<TabLoadingFallback />}>` 래핑 추가

### Step 3: ModalManager lazy import 검증

**파일:** `components/Layout/ModalManager.tsx`

**검사:** 글로벌 모달이 lazy load되고 Suspense로 감싸져 있어야 합니다.

```bash
grep -c "React.lazy(" components/Layout/ModalManager.tsx
grep -c "Suspense" components/Layout/ModalManager.tsx
```

**PASS 기준:** 4개 이상의 lazy import + Suspense 래핑 존재
**FAIL 기준:** 모달이 직접 import됨

**수정:** `const Modal = React.lazy(() => import('../Path/Modal'))` + `<Suspense>` 래핑

### Step 4: TimetableManager lazy import 검증

**파일:** `components/Timetable/TimetableManager.tsx`

**검사:** 시간표 내부의 대형 하위 컴포넌트가 lazy load되어야 합니다.

```bash
grep -c "lazy(" components/Timetable/TimetableManager.tsx
grep -n "Suspense" components/Timetable/TimetableManager.tsx
```

**PASS 기준:** 5개 이상의 lazy import + Suspense 사용
**FAIL 기준:** lazy import 수 감소 (직접 import로 전환)

**수정:** `const Component = lazy(() => import('./Path/Component'))` 패턴 복원

### Step 5: ErrorBoundary 컴포넌트 존재 검증

**파일:** `components/Common/ErrorBoundary.tsx`

**검사:** ErrorBoundary 컴포넌트가 존재하고 올바르게 export되어야 합니다.

```bash
ls components/Common/ErrorBoundary.tsx 2>/dev/null || echo "MISSING"
grep -n "export default" components/Common/ErrorBoundary.tsx
```

**PASS 기준:** 파일 존재 + export default 있음
**FAIL 기준:** ErrorBoundary 파일 누락

**수정:** React ErrorBoundary 클래스 컴포넌트 생성

### Step 6: 서브매니저/탭 lazy import 검증

**검사:** 2개 이상의 lazy import를 사용하는 서브매니저/탭 컴포넌트가 Suspense로 감싸져 있는지 확인합니다.

```bash
for f in \
  "components/StudentManagement/StudentManagementTab.tsx" \
  "components/Dashboard/roles/MasterDashboard.tsx" \
  "components/StudentConsultation/ConsultationManagementTab.tsx" \
  "components/RegistrationConsultation/ConsultationManager.tsx" \
  "components/Embed/EmbedRouter.tsx"; do
  lazy_count=$(grep -c "lazy(" "$f" 2>/dev/null);
  suspense_count=$(grep -c "Suspense" "$f" 2>/dev/null);
  if [ "$suspense_count" -eq 0 ] && [ "$lazy_count" -gt 0 ]; then
    echo "WARNING: $f has $lazy_count lazy imports but no Suspense";
  fi;
done
```

**PASS 기준:** lazy import를 사용하는 모든 서브매니저에 Suspense 래핑 존재
**FAIL 기준:** lazy 컴포넌트를 Suspense 없이 렌더링 (런타임 에러)

**수정:** `<Suspense fallback={<div>Loading...</div>}>` 또는 부모의 Suspense에 의존

## Output Format

| # | 검사 항목 | 파일 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | TabContent lazy import 카운트 | TabContent.tsx | PASS/FAIL | N개 |
| 2 | TabContent 직접 import 없음 | TabContent.tsx | PASS/FAIL | |
| 3 | Suspense + ErrorBoundary | TabContent.tsx | PASS/FAIL | |
| 4 | ModalManager lazy + Suspense | ModalManager.tsx | PASS/FAIL | |
| 5 | TimetableManager lazy | TimetableManager.tsx | PASS/FAIL | |
| 6 | ErrorBoundary 컴포넌트 존재 | ErrorBoundary.tsx | PASS/FAIL | |
| 7 | 서브매니저 lazy + Suspense | 5개 서브매니저 | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **소형 유틸리티 컴포넌트의 직접 import** - `ErrorBoundary`, `VideoLoading`, `Skeleton` 등 작은 공통 컴포넌트는 lazy load 불필요 (번들에 이미 포함)
2. **ModalManager에서 fallback={null}** - 모달은 화면 전체를 차지하지 않으므로 로딩 스피너 대신 null fallback 사용 가능
3. **조건부 렌더링 내부의 lazy 컴포넌트** - 삼항 연산자 내부에서 렌더되는 lazy 컴포넌트는 상위 Suspense가 커버하면 개별 Suspense 불필요
4. **`.then(m => ({ default: m.ComponentName }))` 패턴** - named export를 lazy load할 때 사용하는 정상적인 패턴
5. **1개의 lazy import만 가진 서브매니저** - `BillingManager`, `CalendarBoard`, `WithdrawalManagementTab` 등 단일 lazy import는 번들 영향이 미미하여 검증 대상에서 제외
6. **부모 Suspense에 의존하는 서브매니저** - TabContent의 Suspense가 하위 lazy 컴포넌트를 이미 커버하는 경우, 서브매니저 내부에 별도 Suspense가 없어도 정상
