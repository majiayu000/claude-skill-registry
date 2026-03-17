---
name: verify-responsive
description: 모바일/태블릿/데스크톱 반응형 TailwindCSS 패턴 일관성을 검증합니다. UI 컴포넌트 수정 후 사용.
---

## Purpose

1. **브레이크포인트 일관성** - TailwindCSS 브레이크포인트(sm/md/lg/xl)가 프로젝트 전반에서 일관되게 사용되는지 검증
2. **모바일 우선 패턴** - 모바일 우선(mobile-first) 반응형 설계가 적용되어 있는지 검증
3. **터치 타겟 크기** - 모바일 환경에서 터치 가능한 요소의 최소 크기(44px)가 보장되는지 검증
4. **숨김/표시 패턴** - hidden/block 클래스가 올바르게 사용되는지 검증

## When to Run

- UI 컴포넌트의 레이아웃이나 스타일을 수정한 후
- 새로운 탭이나 모달 컴포넌트를 추가한 후
- TailwindCSS 클래스를 대폭 변경한 후
- 모바일/태블릿 관련 이슈를 수정한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/Navigation/Sidebar.tsx` | 사이드바 (데스크톱/모바일 분기) |
| `components/Layout/TabContent.tsx` | 탭 콘텐츠 레이아웃 |
| `components/Common/Modal.tsx` | 공통 모달 (반응형 크기) |
| `components/Dashboard/DashboardTab.tsx` | 대시보드 (카드 그리드) |
| `App.tsx` | 전체 레이아웃 |
| `tailwind.config.js` | TailwindCSS 설정 (커스텀 브레이크포인트) |

## Workflow

### Step 1: TailwindCSS 설정 확인

**검사:** tailwind.config에 커스텀 브레이크포인트가 정의되어 있는지 확인합니다.

```bash
ls tailwind.config.js tailwind.config.ts 2>/dev/null
grep -n "screens\|breakpoint" tailwind.config.* 2>/dev/null | head -10
```

**PASS 기준:** TailwindCSS 설정 파일 존재 + 기본 또는 커스텀 브레이크포인트 정의
**FAIL 기준:** 설정 파일 누락

### Step 2: 반응형 클래스 사용 현황

**검사:** 주요 레이아웃 컴포넌트에서 반응형 클래스(sm:, md:, lg:, xl:)가 사용되는지 확인합니다.

```bash
grep -c "sm:\|md:\|lg:\|xl:" components/Navigation/Sidebar.tsx 2>/dev/null
grep -c "sm:\|md:\|lg:\|xl:" App.tsx 2>/dev/null
grep -c "sm:\|md:\|lg:\|xl:" components/Dashboard/DashboardTab.tsx 2>/dev/null
```

**PASS 기준:** 핵심 레이아웃 파일에서 반응형 클래스 사용 (각 3개 이상)
**FAIL 기준:** 반응형 클래스 미사용 (고정 레이아웃만 존재)

### Step 3: 모바일 사이드바 처리 검증

**검사:** Sidebar가 모바일에서 숨김/메뉴 토글 패턴을 사용하는지 확인합니다.

```bash
grep -n "hidden\|block\|sidebar\|toggle\|hamburger\|menu" components/Navigation/Sidebar.tsx | head -15
```

**PASS 기준:** 모바일에서 사이드바 숨김 또는 토글 로직 존재
**FAIL 기준:** 사이드바가 모바일에서도 항상 표시됨

### Step 4: 모달 반응형 크기 검증

**검사:** 공통 Modal 컴포넌트가 모바일에서 전체 화면 또는 적절한 크기로 조정되는지 확인합니다.

```bash
grep -n "w-full\|max-w\|h-full\|max-h\|sm:\|md:" components/Common/Modal.tsx 2>/dev/null | head -10
```

**PASS 기준:** 모달에 반응형 크기 조절 클래스 존재
**FAIL 기준:** 모달이 고정 크기만 사용

### Step 5: 그리드/플렉스 반응형 패턴 검증

**검사:** 대시보드 등 카드 그리드 컴포넌트에서 반응형 그리드 클래스를 사용하는지 확인합니다.

```bash
grep -n "grid-cols\|flex-wrap\|flex-col.*sm:flex-row\|sm:grid-cols\|md:grid-cols\|lg:grid-cols" components/Dashboard/DashboardTab.tsx 2>/dev/null | head -10
```

**PASS 기준:** 반응형 그리드/플렉스 패턴 존재
**FAIL 기준:** 고정 그리드만 사용

### Step 6: 인라인 스타일 최소화 검증

**검사:** 주요 레이아웃 파일에서 인라인 style 대신 TailwindCSS 클래스를 사용하는지 확인합니다.

```bash
grep -c "style={{" components/Navigation/Sidebar.tsx App.tsx components/Layout/TabContent.tsx 2>/dev/null
```

**PASS 기준:** 인라인 스타일이 파일당 10개 미만 (일부 동적 값은 허용)
**FAIL 기준:** 과도한 인라인 스타일 사용 (반응형 제어 어려움)

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | TailwindCSS 설정 | tailwind.config | PASS/FAIL | |
| 2 | 반응형 클래스 사용 | 핵심 레이아웃 | PASS/FAIL | 파일별 사용 수 |
| 3 | 모바일 사이드바 | Sidebar.tsx | PASS/FAIL | |
| 4 | 모달 반응형 크기 | Modal.tsx | PASS/FAIL | |
| 5 | 그리드/플렉스 반응형 | Dashboard 등 | PASS/FAIL | |
| 6 | 인라인 스타일 최소화 | 핵심 파일 | PASS/FAIL | 파일별 count |

## Exceptions

다음은 **위반이 아닙니다**:

1. **GanttChart의 인라인 스타일** - SVG 기반 차트는 TailwindCSS로 제어하기 어려워 인라인 스타일이 필수적
2. **CalendarBoard의 고정 너비 셀** - 캘린더 그리드 셀은 일관된 크기가 필요하여 고정 px 사용 가능
3. **print: 관련 스타일** - 인쇄 전용 스타일은 반응형과 별개
4. **TimetableGrid의 인라인 스타일** - 동적 열/행 개수에 따라 grid-template을 인라인으로 설정하는 것은 정상
