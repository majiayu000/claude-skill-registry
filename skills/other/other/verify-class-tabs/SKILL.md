---
name: verify-class-tabs
description: 수업 그룹(시간표/출석부/출결관리/수업관리/강의실/강의실배정/숙제관리/시험관리/교재관리) 탭의 핵심 기능을 검증합니다. 수업 관련 컴포넌트 수정 후 사용.
---

## Purpose

1. **시간표 Math/English 분리** - 수학/영어 시간표가 독립적으로 동작하고 각각의 시뮬레이션 컨텍스트를 가지는지 검증
2. **출석부 데이터 흐름** - useAttendance → AttendanceManager → StudentRow 데이터 흐름이 올바른지 검증
3. **출결 관리 상태 전환** - 출석/결석/지각/조퇴 등 상태 전환이 정상적인지 검증
4. **수업 관리 CRUD** - 수업 생성/수정/삭제 및 학생 배정 기능이 올바른지 검증
5. **강의실 배정 알고리즘** - 자동 배정 알고리즘과 수동 배정 기능이 정상 동작하는지 검증
6. **교재 요청서 시스템** - 요청서 작성/이력/PNG 다운로드/수납 자동 매칭이 올바르게 동작하는지 검증

## When to Run

- `components/Timetable/` 하위 컴포넌트를 수정한 후
- `components/Attendance/` 또는 `components/DailyAttendance/` 수정 후
- `components/ClassManagement/` 수정 후
- `components/Classroom/` 또는 `components/ClassroomAssignment/` 수정 후
- `hooks/useAttendance.ts`, `hooks/useClassMutations.ts`, `hooks/useDailyAttendance.ts` 수정 후
- `components/Textbooks/` 또는 `hooks/useTextbooks.ts`, `hooks/useTextbookRequests.ts` 수정 후

## Related Files

| File | Purpose |
|------|---------|
| `components/Timetable/TimetableManager.tsx` | 시간표 메인 (Math/English 분기) |
| `components/Timetable/English/EnglishTimetable.tsx` | 영어 시간표 (lazy-loaded) |
| `components/Timetable/Math/MathClassTab.tsx` | 수학 시간표 탭 |
| `components/Timetable/English/context/SimulationContext.tsx` | 영어 시뮬레이션 컨텍스트 |
| `components/Timetable/Math/context/SimulationContext.tsx` | 수학 시뮬레이션 컨텍스트 |
| `components/Attendance/AttendanceManager.tsx` | 출석부 메인 |
| `components/Attendance/components/StudentRow.tsx` | 학생 행 컴포넌트 |
| `components/Attendance/components/SalarySettings.tsx` | 급여 설정 컴포넌트 |
| `components/Attendance/components/SalarySettingsTab.tsx` | 급여 설정 탭 |
| `components/DailyAttendance/DailyAttendanceManager.tsx` | 출결 관리 메인 |
| `components/ClassManagement/ClassManagementTab.tsx` | 수업 관리 메인 |
| `components/ClassManagement/ClassDetailModal.tsx` | 수업 상세 모달 |
| `components/Classroom/ClassroomTab.tsx` | 강의실 메인 |
| `components/ClassroomAssignment/ClassroomAssignmentTab.tsx` | 강의실 배정 메인 |
| `components/ClassroomAssignment/hooks/useAutoAssignAlgorithm.ts` | 자동 배정 알고리즘 |
| `hooks/useAttendance.ts` | 출결 데이터 및 mutation (11 mutations) |
| `hooks/useDailyAttendance.ts` | 일일 출결 (5 mutations) |
| `hooks/useClassMutations.ts` | 수업 CRUD (5 mutations) |
| `hooks/useClasses.ts` | 수업 목록 쿼리 |
| `hooks/useClassDetail.ts` | 수업 상세 쿼리 |
| `hooks/useClassStats.ts` | 수업 통계 |
| `hooks/useEnglishClassUpdater.ts` | 영어 수업명 업데이트 |
| `hooks/useVisibleAttendanceStudents.ts` | 출석부 표시 학생 필터 |
| `components/Homework/HomeworkTab.tsx` | 숙제 관리 메인 |
| `components/Exams/ExamsTab.tsx` | 시험 관리 메인 |
| `components/Textbooks/TextbooksTab.tsx` | 교재 관리 메인 (4개 뷰: list/distribution/billing/request) |
| `components/Textbooks/TextbookRequestView.tsx` | 교재 요청서 뷰 (작성/이력 탭, PNG 다운로드) |
| `components/Textbooks/TextbookPreviewCard.tsx` | 요청서 미리보기 카드 (forwardRef + html-to-image) |
| `components/Textbooks/TextbookBookSelector.tsx` | 교재 선택 모달 (카탈로그 검색) |
| `hooks/useHomework.ts` | 숙제 데이터 + mutation (4 mutations) |
| `hooks/useExams.ts` | 시험 데이터 + mutation (4 mutations) |
| `hooks/useTextbooks.ts` | 교재 수납 데이터 + mutation (5 mutations, 자동 매칭 포함) |
| `hooks/useTextbookRequests.ts` | 교재 요청서 CRUD + 계좌설정 + 카탈로그 (6 mutations) |
| `data/textbookCatalog.ts` | 157개 교재 카탈로그 정적 데이터 |
| `hooks/useSubjectClassStudents.ts` | 통합 과목별 수업 학생 데이터 훅 (수학/영어/Generic 공통) |
| `utils/enrollment.ts` | 수강종료 판정 유틸리티 (getEndedSubjects 단일 소스) |
| `utils/firestoreConverters.ts` | Firestore Timestamp → 날짜 변환 유틸리티 |

## Workflow

### Step 1: 수업 그룹 탭 lazy import 검증

**검사:** 9개 탭 컴포넌트가 모두 TabContent에서 lazy import되는지 확인합니다.

```bash
grep -n "TimetableManager\|AttendanceManager\|DailyAttendanceManager\|ClassManagementTab\|ClassroomTab\|ClassroomAssignmentTab\|HomeworkTab\|ExamsTab\|TextbooksTab" components/Layout/TabContent.tsx
```

**PASS 기준:** 9개 컴포넌트가 모두 React.lazy로 import됨
**FAIL 기준:** 하나 이상의 탭 컴포넌트가 누락되거나 직접 import됨

### Step 2: 시간표 Math/English 시뮬레이션 컨텍스트 분리 검증

**검사:** Math와 English 시뮬레이션 컨텍스트가 독립적으로 존재하는지 확인합니다.

```bash
ls components/Timetable/English/context/SimulationContext.tsx 2>/dev/null || echo "MISSING: English SimulationContext"
ls components/Timetable/Math/context/SimulationContext.tsx 2>/dev/null || echo "MISSING: Math SimulationContext"
```

**PASS 기준:** 양쪽 모두 SimulationContext 파일 존재
**FAIL 기준:** 하나 이상의 SimulationContext 누락

### Step 3: 출석부 mutation 훅 연결 검증

**검사:** AttendanceManager가 useAttendance 훅을 사용하고 핵심 mutation이 존재하는지 확인합니다.

```bash
grep -n "useAttendance" components/Attendance/AttendanceManager.tsx | head -5
grep -c "useMutation" hooks/useAttendance.ts
```

**PASS 기준:** AttendanceManager에서 useAttendance 사용 + 11개 이상의 mutation 존재
**FAIL 기준:** 훅 연결 누락 또는 mutation 수 감소

### Step 4: 수업 관리 CRUD 모달 검증

**검사:** 수업 관리 탭에서 추가/수정/삭제 모달이 모두 연결되어 있는지 확인합니다.

```bash
grep -n "AddClassModal\|EditClassModal\|ClassDetailModal" components/ClassManagement/ClassManagementTab.tsx | head -10
```

**PASS 기준:** 3개 모달이 모두 참조됨
**FAIL 기준:** CRUD 모달 연결 누락

### Step 5: 강의실 배정 알고리즘 훅 존재 검증

**검사:** 자동 배정 알고리즘 훅이 존재하고 ClassroomAssignmentTab에서 사용되는지 확인합니다.

```bash
ls components/ClassroomAssignment/hooks/useAutoAssignAlgorithm.ts 2>/dev/null || echo "MISSING"
grep -n "useAutoAssignAlgorithm\|useClassroomAssignment" components/ClassroomAssignment/ClassroomAssignmentTab.tsx | head -5
```

**PASS 기준:** 알고리즘 훅 존재 + 탭에서 사용
**FAIL 기준:** 알고리즘 훅 누락

### Step 6: 출결 상태 타입 일관성 검증

**검사:** 출결 상태값(출석/결석/지각/조퇴 등)이 Attendance 타입과 DailyAttendance에서 일관적으로 사용되는지 확인합니다.

```bash
grep -rn "출석\|결석\|지각\|조퇴\|present\|absent\|late\|early" components/Attendance/types.ts 2>/dev/null | head -10
grep -rn "출석\|결석\|지각\|조퇴\|present\|absent\|late\|early" components/DailyAttendance/DailyAttendanceManager.tsx 2>/dev/null | head -10
```

**PASS 기준:** 양쪽에서 동일한 상태값 사용
**FAIL 기준:** 상태값 불일치

### Step 7: useClassMutations invalidateQueries 검증

**검사:** 수업 mutation 후 관련 캐시가 올바르게 무효화되는지 확인합니다.

```bash
grep -c "invalidateQueries" hooks/useClassMutations.ts
```

**PASS 기준:** 20개 이상의 invalidateQueries 호출 (5 mutations × 평균 4+ invalidations, timetableClasses 포함)
**FAIL 기준:** invalidateQueries 수가 현저히 감소 (20 미만)

### Step 8: 교재 요청서 시스템 구조 검증

**검사:** TextbooksTab의 4번째 뷰 모드(request)가 TextbookRequestView를 lazy import하고, 요청서 훅과 컴포넌트가 올바르게 연결되는지 확인합니다.

```bash
grep -n "TextbookRequestView\|viewMode.*request" components/Textbooks/TextbooksTab.tsx | head -5
grep -n "useTextbookRequests" components/Textbooks/TextbookRequestView.tsx | head -3
ls components/Textbooks/TextbookPreviewCard.tsx components/Textbooks/TextbookBookSelector.tsx 2>/dev/null
grep -c "useMutation" hooks/useTextbookRequests.ts
```

**PASS 기준:** TextbooksTab에서 TextbookRequestView lazy import + viewMode 'request' 존재 + TextbookRequestView에서 useTextbookRequests 사용 + PreviewCard/BookSelector 파일 존재 + 6개 mutation
**FAIL 기준:** lazy import 누락, 훅 연결 누락, 컴포넌트 파일 누락

### Step 9: 수납 자동 매칭 로직 검증

**검사:** useTextbooks.ts의 importBillings mutation에 textbook_requests 자동 매칭 로직이 포함되어 있는지 확인합니다.

```bash
grep -n "textbook_requests\|autoMatch\|isPaid.*true" hooks/useTextbooks.ts | head -10
grep -n "textbookRequests" hooks/useTextbooks.ts | head -5
```

**PASS 기준:** importBillings 내에 textbook_requests 컬렉션 참조 + isPaid 자동 업데이트 + textbookRequests 캐시 invalidation 존재
**FAIL 기준:** 자동 매칭 로직 누락 (수납 가져오기 후 요청서 상태 미갱신)

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | 9개 탭 lazy import | TabContent.tsx | PASS/FAIL | |
| 2 | 시뮬레이션 컨텍스트 분리 | Timetable/Math,English | PASS/FAIL | |
| 3 | 출석부 mutation 연결 | useAttendance.ts | PASS/FAIL | N개 mutation |
| 4 | 수업 CRUD 모달 | ClassManagementTab | PASS/FAIL | |
| 5 | 강의실 배정 알고리즘 | ClassroomAssignment | PASS/FAIL | |
| 6 | 출결 상태 일관성 | Attendance + DailyAttendance | PASS/FAIL | |
| 7 | 수업 mutation 캐시 무효화 | useClassMutations.ts | PASS/FAIL | N개 invalidation |
| 8 | 교재 요청서 시스템 구조 | TextbooksTab + TextbookRequestView | PASS/FAIL | |
| 9 | 수납 자동 매칭 | useTextbooks.ts | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **TimetableManager 내부의 lazy import** - TimetableManager가 자체적으로 7개의 lazy import를 사용하는 것은 코드 스플리팅을 위한 정상 패턴 (verify-lazy-loading에서 별도 검증)
2. **AttendanceSettingsModal의 개별 lazy import** - 설정 모달은 AttendanceManager 내부에서 필요 시 로드
3. **ClassroomTab과 ClassroomAssignmentTab의 독립 동작** - 두 탭은 같은 강의실 데이터를 사용하지만 독립적인 상태를 가짐
4. **DailyAttendance의 간소한 구조** - ClassAttendanceList, AttendanceCalendar 등 하위 컴포넌트가 있지만 별도 hooks 디렉토리 없이 props로 데이터 전달하는 것은 정상
5. **English/Math 시간표의 다른 훅 구조** - 영어 시간표는 5개 훅, 수학 시간표는 6개 훅으로 구조가 다르지만 도메인 특성상 정상
