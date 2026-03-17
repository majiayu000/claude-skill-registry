---
name: verify-schedule-tabs
description: 일정 그룹(연간일정/간트차트) 탭의 컴포넌트 구조, 데이터 흐름, 핵심 기능을 검증합니다. 일정 관련 컴포넌트 수정 후 사용.
---

## Purpose

1. **캘린더 CRUD 무결성** - 이벤트 생성/수정/삭제 흐름이 올바르게 연결되어 있는지 검증
2. **간트 템플릿/프로젝트 구분** - isTemplate 플래그로 템플릿과 프로젝트가 올바르게 분리되는지 검증
3. **뷰 모드 전환** - 일간/주간/월간/연간 뷰 모드가 정상 동작하는지 검증
4. **이벤트 모달 상태 관리** - useEventModalState 훅의 상태 흐름이 일관적인지 검증
5. **아카이브 이벤트** - 이벤트 보관/복원 기능이 올바르게 동작하는지 검증

## When to Run

- `components/Calendar/` 디렉토리의 컴포넌트를 추가하거나 수정한 후
- `components/Gantt/` 디렉토리의 컴포넌트를 수정한 후
- `hooks/useEventCrud.ts`, `hooks/useArchivedEvents.ts`를 수정한 후
- `hooks/useGanttTemplates.ts`, `hooks/useGanttProjects.ts`를 수정한 후
- 캘린더 뷰 모드 또는 이벤트 관련 로직을 변경한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/Calendar/CalendarBoard.tsx` | 메인 캘린더 컴포넌트 (882줄) |
| `components/Calendar/WeekBlock.tsx` | 주간 캘린더 그리드 (494줄) |
| `components/Calendar/YearlyView.tsx` | 연간 캘린더 뷰 (570줄) |
| `components/Calendar/EventFormFields.tsx` | 이벤트 생성/수정 폼 (528줄) |
| `components/Calendar/EventModal.tsx` | 이벤트 모달 래퍼 (209줄) |
| `components/Calendar/SeminarEventModal.tsx` | 세미나 이벤트 모달 (840줄) |
| `components/Calendar/hooks/useEventModalState.ts` | 이벤트 모달 상태 관리 (449줄) |
| `components/Gantt/GanttManager.tsx` | 간트 매니저 (387줄) |
| `components/Gantt/GanttBuilder.tsx` | 간트 태스크 빌더 (757줄) |
| `components/Gantt/GanttChart.tsx` | 간트 차트 SVG 렌더링 (618줄) |
| `hooks/useEventCrud.ts` | 이벤트 CRUD 로직 |
| `hooks/useArchivedEvents.ts` | 이벤트 아카이브 로직 |
| `hooks/useGanttTemplates.ts` | 간트 템플릿 CRUD |
| `hooks/useGanttProjects.ts` | 간트 프로젝트 쿼리 |
| `hooks/useGanttCategories.ts` | 간트 카테고리 관리 |
| `hooks/useAppState.ts` | 캘린더 상태 (useCalendarState, useEventModalState, usePendingEventMoves) |
| `components/Calendar/CalendarSettingsModal.tsx` | 캘린더 설정 모달 (뷰 옵션, 표시 설정) |
| `components/Gantt/GanttSettingsModal.tsx` | 간트 설정 모달 (차트 표시 옵션) |

## Workflow

### Step 1: 캘린더 컴포넌트 export 검증

**검사:** CalendarBoard가 TabContent에서 정상적으로 lazy import되는지 확인합니다.

```bash
grep -n "CalendarBoard" components/Layout/TabContent.tsx
```

**PASS 기준:** React.lazy로 CalendarBoard가 import되어 있음
**FAIL 기준:** CalendarBoard import가 누락되거나 직접 import됨

**수정:** `const CalendarBoard = React.lazy(() => import('../Calendar/CalendarBoard'))` 추가

### Step 2: 이벤트 CRUD 함수 존재 검증

**검사:** useEventCrud 훅에서 핵심 CRUD 함수가 export되는지 확인합니다.

```bash
grep -n "handleSaveEvent\|handleDeleteEvent\|handleBatchAttendanceUpdate" hooks/useEventCrud.ts | head -10
```

**PASS 기준:** handleSaveEvent, handleDeleteEvent 함수가 모두 존재
**FAIL 기준:** 핵심 CRUD 함수 누락

**수정:** 누락된 함수를 useEventCrud.ts에 구현

### Step 3: 캘린더 뷰 모드 타입 검증

**검사:** CalendarBoard에서 지원하는 뷰 모드가 useCalendarState의 viewMode 타입과 일치하는지 확인합니다.

```bash
grep -n "viewMode" hooks/useAppState.ts | head -10
grep -n "viewMode" components/Calendar/CalendarBoard.tsx | head -10
```

**PASS 기준:** viewMode가 양쪽에서 일관되게 사용됨 (daily, weekly, monthly, yearly)
**FAIL 기준:** 뷰 모드 불일치 또는 미정의 모드 사용

### Step 4: 간트 매니저 뷰 모드 검증

**검사:** GanttManager의 뷰 모드(home, create, edit, execute)가 올바르게 정의되어 있는지 확인합니다.

```bash
grep -n "home\|create\|edit\|execute" components/Gantt/GanttManager.tsx | head -15
```

**PASS 기준:** 4가지 뷰 모드가 모두 처리됨
**FAIL 기준:** 뷰 모드 누락 또는 미처리 케이스 존재

### Step 5: 간트 템플릿 CRUD 검증

**검사:** useGanttTemplates에서 Create/Update/Delete mutation이 모두 존재하는지 확인합니다.

```bash
grep -n "useCreateTemplate\|useUpdateTemplate\|useDeleteTemplate" hooks/useGanttTemplates.ts
```

**PASS 기준:** 3개의 mutation 훅이 모두 존재
**FAIL 기준:** CRUD mutation 누락

### Step 6: 이벤트 모달 상태 초기화 검증

**검사:** 이벤트 모달이 열릴 때 상태가 올바르게 초기화되는지 확인합니다.

```bash
grep -n "openEventModal\|closeEventModal\|resetForm" components/Calendar/hooks/useEventModalState.ts | head -10
```

**PASS 기준:** 모달 열기/닫기 시 상태 초기화 로직 존재
**FAIL 기준:** 상태 초기화 누락 (이전 이벤트 데이터 잔존 가능)

### Step 7: 아카이브 이벤트 훅 연결 검증

**검사:** useArchivedEvents 훅이 CalendarBoard에서 사용되는지 확인합니다.

```bash
grep -n "useArchivedEvents\|showArchived\|archivedEvents" components/Calendar/CalendarBoard.tsx | head -5
```

**PASS 기준:** 아카이브 관련 로직이 CalendarBoard에 연결됨
**FAIL 기준:** 아카이브 기능이 UI에서 분리됨

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | CalendarBoard lazy import | TabContent.tsx | PASS/FAIL | |
| 2 | 이벤트 CRUD 함수 | useEventCrud.ts | PASS/FAIL | |
| 3 | 캘린더 뷰 모드 일관성 | AppState + CalendarBoard | PASS/FAIL | |
| 4 | 간트 뷰 모드 | GanttManager.tsx | PASS/FAIL | |
| 5 | 간트 템플릿 CRUD | useGanttTemplates.ts | PASS/FAIL | |
| 6 | 이벤트 모달 상태 초기화 | useEventModalState.ts | PASS/FAIL | |
| 7 | 아카이브 이벤트 연결 | CalendarBoard.tsx | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **CalendarSettingsModal의 별도 lazy import** - 설정 모달은 CalendarBoard 내부에서 lazy import되며, TabContent가 아닌 컴포넌트 레벨에서 분리됨
2. **useEventCrud의 invalidateQueries 부재** - App.tsx에서 onSnapshot으로 이벤트를 실시간 동기화하므로 별도 캐시 무효화 불필요
3. **GanttChart의 SVG 직접 렌더링** - React 컴포넌트가 아닌 SVG 요소를 직접 조작하는 것은 성능 최적화를 위한 의도적 패턴
4. **BucketModal의 단순 구조** - 166줄의 소형 모달로 별도 상태 관리 훅이 없어도 정상
