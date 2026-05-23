---
name: verify-timetable
description: 시간표 도메인(Math/shared)의 핵심 패턴과 규칙을 검증합니다. 시간표 컴포넌트/훅 수정 후 사용.
---

## Purpose

1. **React.memo 일관성** - 성능에 민감한 컴포넌트(ClassCard, TimetableGrid)가 React.memo로 래핑되어 있는지 검증
2. **Stale closure 방지 패턴** - useStudentDragDrop에서 useRef + useCallback 조합으로 최신 상태를 읽는 패턴이 유지되는지 검증
3. **Firebase writeBatch 패턴** - 반 이동 저장 시 writeBatch → commit → invalidateQueries 시퀀스가 올바른지 검증
4. **createPortal 사용** - 툴팁/오버레이가 createPortal로 렌더링되어 overflow 잘림을 방지하는지 검증
5. **테스트 커버리지** - 주요 컴포넌트/훅에 대한 테스트 파일이 존재하는지 검증
6. **고스트 카드 패턴** - 스케줄 변경 예정 클래스의 고스트 블록이 올바르게 생성/렌더링되는지 검증
7. **퇴원 드롭존 패턴** - ClassCard 하단 퇴원 드롭존이 수정 모드에서만 표시되고 enrollment만 종료하는지 검증
8. **스케줄 자동 적용** - pendingScheduleDate 도래 시 자동 적용 로직이 올바르게 동작하는지 검증

## When to Run

- `components/Timetable/Math/` 하위 파일을 수정한 후
- `components/Timetable/shared/` 하위 파일을 수정한 후
- `useStudentDragDrop` 훅의 드래그&드롭 로직을 변경한 후
- SimulationContext 또는 시나리오 관련 코드를 수정한 후
- 시간표 관련 새 컴포넌트/훅을 추가한 후
- 반 이동(Firebase writeBatch) 로직을 변경한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/Timetable/Math/components/ClassCard.tsx` | 수업 카드 컴포넌트 (React.memo + 커스텀 비교함수) |
| `components/Timetable/Math/components/TimetableGrid.tsx` | 시간표 그리드 (React.memo) |
| `components/Timetable/Math/components/TimetableHeader.tsx` | 시간표 헤더 (모드 전환, 검색, 보기 설정) |
| `components/Timetable/Math/components/ScheduledDateModal.tsx` | 예정일 모달 (반이동/퇴원/스케줄변경 공용) |
| `components/Timetable/Math/hooks/useStudentDragDrop.ts` | 학생 드래그&드롭 + 반 이동 저장 훅 |
| `components/Timetable/Math/context/SimulationContext.tsx` | 시나리오 모드 Context (writeBatch, sanitizeForFirestore) |
| `components/Timetable/Math/ScenarioManagementModal.tsx` | 시나리오 관리 모달 (writeBatch) |
| `components/Timetable/TimetableManager.tsx` | 시간표 매니저 (lazy load, 모드 관리) |
| `components/Timetable/shared/IntegrationClassCard.tsx` | 통합뷰 수업 카드 (createPortal 툴팁) |
| `components/Timetable/shared/IntegrationMiniGridRow.tsx` | 통합뷰 미니 그리드 행 |
| `components/Timetable/Math/hooks/useTimetableClasses.ts` | 시간표 수업 데이터 훅 |
| `components/Timetable/Math/hooks/useClassOperations.ts` | 수업 CRUD 훅 |
| `components/Timetable/Math/hooks/useMathClassStudents.ts` | 수학 수업 학생 데이터 훅 |
| `components/Timetable/Math/MathClassTab.tsx` | 수학 시간표 탭 (getWeekReferenceDate 사용) |
| `components/Timetable/English/EnglishTimetable.tsx` | 영어 시간표 (getWeekReferenceDate 사용) |
| `types/timetable.ts` | TimetableClass 타입 (pendingSchedule, isPendingSchedule 등) |
| `hooks/useClassMutations.ts` | 수업 수정 mutation (pendingSchedule 저장/삭제) |
| `components/ClassManagement/EditClassModal.tsx` | 수업 수정 모달 (스케줄 변경 감지 + 예정일 모달 연동) |
| `utils/dateUtils.ts` | 날짜 유틸 (getWeekReferenceDate - 주차 기준일 계산) |
| `tests/components/ClassCard.StudentItem.test.tsx` | ClassCard StudentItem 테스트 |
| `tests/components/ScheduledDateModal.test.tsx` | ScheduledDateModal 테스트 |
| `tests/hooks/useStudentDragDrop.test.ts` | useStudentDragDrop 테스트 |
| `tests/hooks/useSimulationContext.test.tsx` | SimulationContext 테스트 |

## Workflow

### Step 1: React.memo 래핑 검증

**파일:** `components/Timetable/Math/components/ClassCard.tsx`, `components/Timetable/Math/components/TimetableGrid.tsx`

**검사:** ClassCard과 TimetableGrid은 성능에 민감한 컴포넌트로, 반드시 `React.memo`로 export되어야 합니다.

```bash
grep -n "export default React.memo" components/Timetable/Math/components/ClassCard.tsx
grep -n "export default React.memo" components/Timetable/Math/components/TimetableGrid.tsx
```

**PASS 기준:** 두 파일 모두 `export default React.memo(...)` 패턴이 존재
**FAIL 기준:** React.memo 없이 `export default ClassCard` 또는 `export default TimetableGrid`로 export

**수정:** `export default React.memo(ComponentName)` 또는 커스텀 비교함수와 함께 `export default React.memo(ComponentName, compareFn)` 사용

### Step 2: ClassCard 커스텀 비교함수 검증

**파일:** `components/Timetable/Math/components/ClassCard.tsx`

**검사:** ClassCard은 많은 props를 받으므로 커스텀 비교함수가 필요합니다. `React.memo(ClassCard, (prevProps, nextProps) => ...)` 패턴이 있어야 합니다.

```bash
grep -n "React.memo(ClassCard," components/Timetable/Math/components/ClassCard.tsx
```

**PASS 기준:** `React.memo(ClassCard, (prevProps, nextProps) =>` 패턴 존재 (커스텀 비교함수 포함)
**FAIL 기준:** `React.memo(ClassCard)` (비교함수 없이 기본 얕은 비교만 사용)

**수정:** 성능에 중요한 props를 비교하는 커스텀 비교함수 추가

### Step 3: useStudentDragDrop Ref 패턴 검증

**파일:** `components/Timetable/Math/hooks/useStudentDragDrop.ts`

**검사:** stale closure를 방지하기 위해 `draggingStudentRef`와 `localClassesRef`가 useRef로 선언되고, handleDrop에서 ref를 통해 최신 상태를 읽어야 합니다.

```bash
grep -n "useRef" components/Timetable/Math/hooks/useStudentDragDrop.ts
grep -n "draggingStudentRef.current" components/Timetable/Math/hooks/useStudentDragDrop.ts
grep -n "localClassesRef.current" components/Timetable/Math/hooks/useStudentDragDrop.ts
```

**PASS 기준:**
- `draggingStudentRef = useRef<DraggingStudent | null>(null)` 존재
- `localClassesRef = useRef<TimetableClass[]>([])` 존재
- `handleDrop` 내에서 `draggingStudentRef.current`를 읽는 코드 존재

**FAIL 기준:** useRef 없이 useState만으로 draggingStudent를 handleDrop에서 직접 사용 (stale closure 발생)

**수정:** useState 값 대신 useRef를 통해 최신 상태를 읽도록 변경

### Step 4: writeBatch → commit → invalidateQueries 시퀀스 검증

**파일:** `components/Timetable/Math/hooks/useStudentDragDrop.ts`

**검사:** 반 이동 저장 시 writeBatch → commit → invalidateQueries 순서가 올바른지 확인합니다.

```bash
grep -n "writeBatch\|batch.commit\|invalidateQueries" components/Timetable/Math/hooks/useStudentDragDrop.ts
```

**PASS 기준:**
- `writeBatch(db)` 호출 존재
- `batch.commit()` 호출 존재 (await 포함)
- commit 이후 `invalidateQueries` 호출로 캐시 무효화

**FAIL 기준:**
- writeBatch 없이 개별 setDoc/updateDoc 사용 (원자성 없음)
- commit 후 invalidateQueries 누락 (UI 갱신 안됨)

**수정:** writeBatch 패턴 사용 + commit 후 관련 queryKey invalidate

### Step 5: createPortal 사용 검증

**파일:** `components/Timetable/Math/components/ClassCard.tsx`

**검사:** 툴팁이 셀 overflow에 잘리지 않도록 createPortal을 사용하는지 확인합니다.

```bash
grep -n "createPortal" components/Timetable/Math/components/ClassCard.tsx
grep -n "import.*createPortal.*from 'react-dom'" components/Timetable/Math/components/ClassCard.tsx
```

**PASS 기준:** `createPortal` import 및 사용이 존재
**FAIL 기준:** 툴팁/오버레이가 createPortal 없이 직접 렌더링 (overflow: hidden에 잘림)

**수정:** `import { createPortal } from 'react-dom'` 추가 후 툴팁을 `createPortal(tooltip, document.body)`로 렌더링

### Step 6: IntegrationClassCard createPortal 검증

**파일:** `components/Timetable/shared/IntegrationClassCard.tsx`

**검사:** 통합뷰의 수업시간 툴팁도 createPortal을 사용하여 overflow 잘림을 방지하는지 확인합니다.

```bash
grep -n "createPortal" components/Timetable/shared/IntegrationClassCard.tsx
grep -n "import.*createPortal.*from 'react-dom'" components/Timetable/shared/IntegrationClassCard.tsx
```

**PASS 기준:** `createPortal` import 및 사용이 존재 (Math ClassCard과 동일 패턴)
**FAIL 기준:** 툴팁이 createPortal 없이 부모 컨테이너 내부에 직접 렌더링 (overflow: hidden에 잘림)

**수정:** `import { createPortal } from 'react-dom'` 추가 후 툴팁을 `createPortal(tooltip, document.body)`로 렌더링

### Step 7: sanitizeForFirestore 사용 검증

**파일:** `components/Timetable/Math/context/SimulationContext.tsx`

**검사:** Firebase에 데이터 쓰기 전 undefined 값을 제거하는 sanitizeForFirestore 유틸리티가 존재하고 사용되는지 확인합니다.

```bash
grep -n "sanitizeForFirestore" components/Timetable/Math/context/SimulationContext.tsx
```

**PASS 기준:** `sanitizeForFirestore` 함수 정의 및 writeBatch 사용 근처에서 호출
**FAIL 기준:** undefined 값이 포함된 객체를 직접 Firebase에 쓰는 코드 (Firestore 에러 발생)

**수정:** Firebase에 쓰기 전 `sanitizeForFirestore(data)` 호출 추가

### Step 8: 테스트 커버리지 검증

**검사:** 주요 컴포넌트/훅에 대한 테스트 파일이 존재하는지 확인합니다.

```bash
ls tests/components/ClassCard.StudentItem.test.tsx 2>/dev/null || echo "MISSING: ClassCard test"
ls tests/components/ScheduledDateModal.test.tsx 2>/dev/null || echo "MISSING: ScheduledDateModal test"
ls tests/hooks/useStudentDragDrop.test.ts 2>/dev/null || echo "MISSING: useStudentDragDrop test"
ls tests/hooks/useSimulationContext.test.tsx 2>/dev/null || echo "MISSING: useSimulationContext test"
```

**PASS 기준:** 모든 테스트 파일 존재
**FAIL 기준:** 테스트 파일 누락 (MISSING 출력)

**수정:** 누락된 테스트 파일 생성

### Step 9: effectiveClasses 이중 페인트 방지 패턴 검증

**파일:** `components/Timetable/Math/hooks/useStudentDragDrop.ts`

**검사:** pendingMoves가 없을 때 initialClasses를 직접 사용하여 useEffect의 비동기 setLocalClasses로 인한 깜빡임을 방지하는 패턴이 유지되는지 확인합니다.

```bash
grep -n "effectiveClasses" components/Timetable/Math/hooks/useStudentDragDrop.ts
grep -n "pendingMoves.length === 0 ? initialClasses" components/Timetable/Math/hooks/useStudentDragDrop.ts
```

**PASS 기준:** `effectiveClasses = pendingMoves.length === 0 ? initialClasses : localClasses` 패턴 존재
**FAIL 기준:** localClasses만 사용 (useEffect가 paint 후 실행되어 깜빡임 발생)

**수정:** `const effectiveClasses = pendingMoves.length === 0 ? initialClasses : localClasses;` 패턴 복원

### Step 10: useClassOperations invalidateMathCaches 일관성 검증

**파일:** `components/Timetable/Math/hooks/useClassOperations.ts`

**검사:** 모든 쓰기 메서드(addClass, updateClass, deleteClass, addStudent, removeStudent, withdrawStudent, restoreStudent)가 `invalidateMathCaches()`를 호출하여 시간표 캐시를 무효화하는지 확인합니다. 이 패턴이 누락되면 수업 추가/수정 후 시간표가 실시간으로 갱신되지 않습니다.

```bash
grep -c "invalidateMathCaches()" components/Timetable/Math/hooks/useClassOperations.ts
```

**PASS 기준:** 7회 이상 호출 (7개 쓰기 메서드 각각 1회)
**FAIL 기준:** 7회 미만 (일부 메서드에서 캐시 무효화 누락)

**추가 검증:** invalidateMathCaches 함수가 `timetableClasses` 키를 포함하는지 확인

```bash
grep -A5 "const invalidateMathCaches" components/Timetable/Math/hooks/useClassOperations.ts | grep "timetableClasses"
```

**PASS 기준:** `timetableClasses` 쿼리 키가 무효화 대상에 포함
**FAIL 기준:** `timetableClasses` 키 누락 (시간표 뷰가 갱신되지 않음)

**수정:** 누락된 메서드에 `invalidateMathCaches()` 호출 추가, invalidateMathCaches 내에 `queryClient.invalidateQueries({ queryKey: ['timetableClasses'] })` 추가

### Step 11: PendingMove scheduledDate 필드 검증

**파일:** `components/Timetable/Math/hooks/useStudentDragDrop.ts`

**검사:** PendingMove 인터페이스에 scheduledDate 필드가 있고, 반 이동 저장 시 예정일을 올바르게 처리하는지 확인합니다.

```bash
grep -n "scheduledDate" components/Timetable/Math/hooks/useStudentDragDrop.ts
```

**PASS 기준:**
- `PendingMove` 인터페이스에 `scheduledDate?: string` 필드 존재
- 저장 로직에서 `move.scheduledDate || defaultToday` 패턴으로 예정일/즉시이동 분기

**FAIL 기준:** scheduledDate 필드 없이 항상 오늘 날짜만 사용

**수정:** PendingMove에 scheduledDate 추가, 저장 시 `effectiveDate = move.scheduledDate || defaultToday` 분기 추가

### Step 12: getWeekReferenceDate 일관성 검증

**파일:** `utils/dateUtils.ts`, 시간표 컴포넌트 전체

**검사:** 주차 이동 시 과거/현재/미래 주에 따라 기준일을 올바르게 계산하는 `getWeekReferenceDate` 유틸이 모든 시간표 컴포넌트에서 일관되게 사용되는지 확인합니다.

```bash
grep -rn "getWeekReferenceDate" utils/dateUtils.ts components/Timetable/ --include="*.tsx" --include="*.ts"
```

**PASS 기준:**
- `utils/dateUtils.ts`에 `getWeekReferenceDate` export 함수 존재
- `TimetableManager.tsx`, `MathClassTab.tsx`, `TimetableGrid.tsx`, `IntegrationClassCard.tsx`, `EnglishTimetable.tsx`에서 모두 사용
- 인라인 referenceDate 계산 대신 유틸 함수를 사용

**FAIL 기준:** 일부 컴포넌트에서 인라인으로 `formatDateKey(new Date())`만 사용 (과거 주 복원 불가)

**수정:** 인라인 계산을 `getWeekReferenceDate(weekStart)` 호출로 교체

### Step 13: ClassCard 퇴원예정 가로줄 패턴 검증

**파일:** `components/Timetable/Math/components/ClassCard.tsx`

**검사:** 퇴원예정 학생이 별도 섹션이 아닌 재원생 섹션에 오렌지 배경 + 가로줄(line-through)로 표시되는지 확인합니다 (통합뷰와 동일 동작).

```bash
grep -n "isWithdrawalScheduled" components/Timetable/Math/components/ClassCard.tsx | head -5
grep -n "bg-orange-100.*line-through" components/Timetable/Math/components/ClassCard.tsx
grep -n "commonWithdrawnFuture.*\[\]" components/Timetable/Math/components/ClassCard.tsx
```

**PASS 기준:**
- `isWithdrawalScheduled` prop이 StudentItemProps에 존재
- `bg-orange-100 text-orange-800 line-through` 스타일이 적용
- `commonWithdrawnFuture: any[] = []` (별도 섹션 빈 배열)
- 단일셀 `withdrawnFuture: any[] = []` (별도 섹션 빈 배열)

**FAIL 기준:** 퇴원예정 학생이 `withdrawnFuture` 배열에 분리되어 별도 "퇴원예정" 섹션에 표시

**수정:** 퇴원예정 학생을 active 필터에 포함 + isWithdrawalScheduled prop으로 가로줄 스타일 적용

### Step 14: ClassCard.memo 비교함수 referenceDate 포함 검증

**파일:** `components/Timetable/Math/components/ClassCard.tsx`

**검사:** ClassCard의 React.memo 커스텀 비교함수에 `referenceDate`가 포함되어, 주차 이동 시 카드가 올바르게 리렌더되는지 확인합니다.

```bash
grep -A30 "React.memo(ClassCard," components/Timetable/Math/components/ClassCard.tsx | grep "referenceDate"
```

**PASS 기준:** `prevProps.referenceDate === nextProps.referenceDate` 비교가 memo 비교함수에 포함
**FAIL 기준:** referenceDate 비교 누락 (주차 이동 시 학생 상태가 갱신되지 않음)

**수정:** memo 비교함수에 `prevProps.referenceDate === nextProps.referenceDate &&` 추가

### Step 15: 고스트 카드 렌더링 패턴 검증

**파일:** `components/Timetable/Math/components/ClassCard.tsx`, `components/Timetable/TimetableManager.tsx`

**검사:** 스케줄 변경 예정(`pendingSchedule`)이 있는 클래스에 대해 (1) TimetableManager에서 고스트 클래스 엔트리를 생성하고, (2) ClassCard에서 `isPendingSchedule` 분기로 회색 점선 카드를 렌더링하는지 확인합니다.

```bash
grep -n "isPendingSchedule" components/Timetable/Math/components/ClassCard.tsx | head -5
grep -n "_pending" components/Timetable/TimetableManager.tsx | head -3
grep -n "pendingSchedule.*pendingScheduleDate" components/Timetable/TimetableManager.tsx | head -3
```

**PASS 기준:**
- ClassCard에 `if (cls.isPendingSchedule)` 분기 + `bg-gray-200 border border-dashed border-gray-400` 스타일
- TimetableManager의 `filteredClasses`에서 `id: ${cls.id}_pending` 고스트 엔트리 생성
- 고스트 엔트리에 `isPendingSchedule: true`, `studentList: []`, `studentIds: []` 설정

**FAIL 기준:** isPendingSchedule 분기 없이 고스트 카드가 일반 카드와 동일하게 렌더링

**수정:** ClassCard에 isPendingSchedule early return 추가 + TimetableManager filteredClasses에 고스트 엔트리 추가

### Step 16: 퇴원 드롭존 패턴 검증

**파일:** `components/Timetable/Math/components/ClassCard.tsx`, `components/Timetable/TimetableManager.tsx`

**검사:** ClassCard에 퇴원 드롭존이 존재하고, 수정 모드에서만 표시되며, TimetableManager에서 enrollment의 withdrawalDate만 설정하는지 확인합니다.

```bash
grep -n "onWithdrawalDrop" components/Timetable/Math/components/ClassCard.tsx | head -5
grep -n "withdrawalModalInfo" components/Timetable/TimetableManager.tsx | head -5
grep -n "canEdit && onWithdrawalDrop" components/Timetable/Math/components/ClassCard.tsx | head -3
```

**PASS 기준:**
- ClassCard에 `onWithdrawalDrop` prop + `canEdit && onWithdrawalDrop` 조건부 렌더링
- TimetableManager에 `withdrawalModalInfo` 상태 + `handleWithdrawalDrop` + `handleWithdrawalConfirm`
- `handleWithdrawalConfirm`에서 enrollment `withdrawalDate`만 설정 (학생 글로벌 status 미변경)

**FAIL 기준:** 퇴원 드롭존이 조회 모드에서도 표시 또는 학생 글로벌 status를 변경

**수정:** `canEdit && onWithdrawalDrop` 가드 추가, enrollment doc만 업데이트

### Step 17: 스케줄 변경 자동 적용 패턴 검증

**파일:** `components/Timetable/TimetableManager.tsx`, `hooks/useClassMutations.ts`

**검사:** (1) TimetableManager 마운트 시 pendingScheduleDate가 도래한 클래스의 스케줄을 자동 적용하고, (2) useClassMutations에서 pendingSchedule 저장/삭제가 올바른지 확인합니다.

```bash
grep -n "pendingScheduleDate.*todayStr\|자동적용\|applyPending" components/Timetable/TimetableManager.tsx | head -5
grep -n "pendingSchedule\|clearPending\|deleteField" hooks/useClassMutations.ts | head -10
```

**PASS 기준:**
- TimetableManager에 마운트 시 `pendingScheduleDate <= todayStr` 체크 + class doc/enrollments 업데이트 + pending 필드 삭제
- useClassMutations에 `pendingSchedule`, `pendingScheduleDate`, `clearPending` 필드 지원
- `clearPending: true` 시 `deleteField()` 사용

**FAIL 기준:** 자동 적용 useEffect 누락 또는 pending 필드 삭제 없이 무한 적용 반복

**수정:** useEffect 추가 (마운트 시 1회), clearPending에서 deleteField() 호출

## Output Format

| # | 검사 항목 | 파일 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | React.memo ClassCard | ClassCard.tsx | PASS/FAIL | |
| 2 | React.memo TimetableGrid | TimetableGrid.tsx | PASS/FAIL | |
| 3 | 커스텀 비교함수 ClassCard | ClassCard.tsx | PASS/FAIL | |
| 4 | useRef stale closure 방지 | useStudentDragDrop.ts | PASS/FAIL | |
| 5 | createPortal ClassCard | ClassCard.tsx | PASS/FAIL | |
| 6 | createPortal IntegrationClassCard | IntegrationClassCard.tsx | PASS/FAIL | |
| 7 | writeBatch 시퀀스 | useStudentDragDrop.ts | PASS/FAIL | |
| 8 | sanitizeForFirestore | SimulationContext.tsx | PASS/FAIL | |
| 9 | 테스트 파일 존재 | tests/ | PASS/FAIL | |
| 10 | invalidateMathCaches 일관성 | useClassOperations.ts | PASS/FAIL | |
| 11 | effectiveClasses 패턴 | useStudentDragDrop.ts | PASS/FAIL | |
| 12 | scheduledDate 처리 | useStudentDragDrop.ts | PASS/FAIL | |
| 13 | getWeekReferenceDate 일관성 | 시간표 전체 | PASS/FAIL | |
| 14 | 퇴원예정 가로줄 패턴 | ClassCard.tsx | PASS/FAIL | |
| 15 | memo referenceDate 비교 | ClassCard.tsx | PASS/FAIL | |
| 16 | 고스트 카드 렌더링 | ClassCard.tsx + TimetableManager.tsx | PASS/FAIL | |
| 17 | 퇴원 드롭존 | ClassCard.tsx + TimetableManager.tsx | PASS/FAIL | |
| 18 | 스케줄 자동 적용 | TimetableManager.tsx + useClassMutations.ts | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **TimetableHeader가 React.memo를 사용하지 않음** - TimetableHeader는 모드 전환, 검색 등 자주 변경되는 props를 받으며 부모(TimetableManager)가 리렌더될 때 같이 리렌더되는 것이 자연스러움
2. **ScheduledDateModal이 React.memo를 사용하지 않음** - 모달은 열릴 때만 렌더되므로 memo 불필요
3. **SimpleViewSettingsModal이 React.memo를 사용하지 않음** - 위와 동일 (모달 컴포넌트)
4. **useClassOperations가 writeBatch를 사용하지 않음** - 단일 문서 CRUD는 setDoc/updateDoc이 적절
5. **useMathConfig/useMathSettings에 useRef가 없음** - 설정 훅은 stale closure 문제가 발생하지 않는 단순한 구조
6. **IntegrationMiniGridRow에 createPortal이 없음** - 미니 그리드 행은 툴팁이 없는 간략 표시 컴포넌트로 createPortal 불필요
7. **고스트 카드에 드래그/드롭이 비활성** - 고스트 카드는 예정 스케줄 미리보기이므로 학생 이동 기능이 없는 것이 정상
8. **TimetableManager에서 직접 Firestore 쓰기 (자동 적용)** - mutation 훅이 아닌 직접 updateDoc 사용은 마운트 시 1회 실행되는 자동 적용 로직의 특수 케이스로 정상
