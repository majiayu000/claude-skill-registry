---
name: verify-student-tabs
description: 학생 그룹(학생관리/등록상담/학생상담/성적관리/퇴원관리/계약관리/성적표) 탭의 핵심 기능을 검증합니다. 학생 관련 컴포넌트 수정 후 사용.
---

## Purpose

1. **학생 CRUD 무결성** - 학생 등록/수정/삭제/병합 기능이 올바르게 동작하는지 검증
2. **상담 데이터 흐름** - 등록 상담과 학생 상담의 데이터 흐름이 분리되고 일관적인지 검증
3. **성적 관리 구조** - 시험 생성/점수 입력/성적 프로필 흐름이 올바른지 검증
4. **퇴원 관리** - 퇴원 처리/통계/필터링 기능이 정상 동작하는지 검증
5. **학생 상세 서브탭** - 학생 상세 모달의 6개 서브탭이 모두 연결되어 있는지 검증

## When to Run

- `components/StudentManagement/` 하위 파일을 수정한 후
- `components/RegistrationConsultation/` 또는 `components/StudentConsultation/` 수정 후
- `components/Grades/` 또는 `components/WithdrawalManagement/` 수정 후
- `hooks/useStudents.ts`, `hooks/useConsultations.ts`, `hooks/useGradeProfile.ts` 수정 후
- 학생 관련 mutation 훅을 변경한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/StudentManagement/StudentManagementTab.tsx` | 학생 관리 메인 (5개 lazy import) |
| `components/StudentManagement/StudentDetailModal.tsx` | 학생 상세 모달 |
| `components/StudentManagement/tabs/BasicInfoTab.tsx` | 기본 정보 서브탭 |
| `components/StudentManagement/tabs/AttendanceTab.tsx` | 출결 서브탭 |
| `components/StudentManagement/tabs/CoursesTab.tsx` | 수강 서브탭 |
| `components/StudentManagement/tabs/GradesTab.tsx` | 성적 서브탭 |
| `components/StudentManagement/tabs/ConsultationsTab.tsx` | 상담 서브탭 |
| `components/StudentManagement/tabs/BillingTab.tsx` | 수납 서브탭 |
| `components/RegistrationConsultation/ConsultationManager.tsx` | 등록 상담 메인 (2개 lazy import) |
| `components/RegistrationConsultation/ConsultationForm.tsx` | 상담 폼 |
| `components/StudentConsultation/ConsultationManagementTab.tsx` | 학생 상담 메인 (2개 lazy import) |
| `components/Grades/GradesManager.tsx` | 성적 관리 메인 |
| `components/Grades/ExamCreateModal.tsx` | 시험 생성 모달 |
| `components/Grades/ScoreInputView.tsx` | 점수 입력 뷰 |
| `components/WithdrawalManagement/WithdrawalManagementTab.tsx` | 퇴원 관리 메인 |
| `hooks/useStudents.ts` | 학생 데이터 쿼리 + mutation |
| `hooks/useStudentFilters.ts` | 학생 필터링 |
| `hooks/useStudentGrades.ts` | 학생 성적 (4 mutations) |
| `hooks/useConsultations.ts` | 상담 조회/수정 |
| `hooks/useConsultationMutations.ts` | 상담 CRUD (5 mutations) |
| `hooks/useConsultationStats.ts` | 상담 통계 |
| `hooks/useGradeProfile.ts` | 성적 프로필 (10 mutations) |
| `hooks/useWithdrawalStats.ts` | 퇴원 통계 |
| `hooks/useWithdrawalFilters.ts` | 퇴원 필터링 |
| `hooks/useEnrollments.ts` | 수강 등록 관리 |
| `components/Contracts/ContractsTab.tsx` | 계약 관리 메인 |
| `components/Reports/ReportsTab.tsx` | 성적표 메인 |
| `hooks/useContracts.ts` | 계약 데이터 + mutation (4 mutations) |
| `utils/enrollment.ts` | 수강종료 판정 유틸리티 (퇴원/미래배정 필터링) |
| `utils/firestoreConverters.ts` | Firestore Timestamp → 날짜 변환 유틸리티 |

## Workflow

### Step 1: 학생 그룹 탭 lazy import 검증

**검사:** 7개 탭 컴포넌트가 모두 TabContent에서 lazy import되는지 확인합니다.

```bash
grep -n "StudentManagementTab\|ConsultationManager\|ConsultationManagementTab\|GradesManager\|WithdrawalManagementTab\|ContractsTab\|ReportsTab" components/Layout/TabContent.tsx
```

**PASS 기준:** 7개 컴포넌트가 모두 React.lazy로 import됨
**FAIL 기준:** 하나 이상의 탭 컴포넌트 누락

### Step 2: 학생 상세 서브탭 존재 검증

**검사:** StudentDetailModal에서 6개 서브탭이 모두 참조되는지 확인합니다.

```bash
grep -n "BasicInfoTab\|AttendanceTab\|CoursesTab\|GradesTab\|ConsultationsTab\|BillingTab" components/StudentManagement/StudentDetailModal.tsx
```

**PASS 기준:** 6개 서브탭 모두 참조됨
**FAIL 기준:** 서브탭 참조 누락

**수정:** 누락된 서브탭 import 및 렌더링 추가

### Step 3: 학생 관련 mutation 훅 검증

**검사:** 학생 관련 핵심 mutation 훅들이 존재하고 useMutation을 사용하는지 확인합니다.

```bash
for f in hooks/useStudents.ts hooks/useConsultationMutations.ts hooks/useGradeProfile.ts hooks/useStudentGrades.ts; do
  count=$(grep -c "useMutation" "$f" 2>/dev/null);
  echo "$f: $count mutations";
done
```

**PASS 기준:** useStudents(4+), useConsultationMutations(5+), useGradeProfile(10+), useStudentGrades(4+)
**FAIL 기준:** mutation 수가 예상보다 적음

### Step 4: 등록 상담 vs 학생 상담 분리 검증

**검사:** 등록 상담(RegistrationConsultation)과 학생 상담(StudentConsultation)이 독립적인 컴포넌트와 훅을 사용하는지 확인합니다.

```bash
grep -l "ConsultationManager" components/RegistrationConsultation/*.tsx 2>/dev/null
grep -l "ConsultationManagementTab" components/StudentConsultation/*.tsx 2>/dev/null
```

**PASS 기준:** 각 디렉토리에 독립적인 메인 컴포넌트 존재
**FAIL 기준:** 한쪽 디렉토리에서 다른 쪽의 메인 컴포넌트를 사용

### Step 5: 성적 관리 CRUD 흐름 검증

**검사:** 시험 생성 → 점수 입력 → 조회 흐름이 연결되어 있는지 확인합니다.

```bash
grep -n "ExamCreateModal\|ScoreInputView\|ExamListView" components/Grades/GradesManager.tsx | head -10
```

**PASS 기준:** 3개 뷰/모달이 GradesManager에서 참조됨
**FAIL 기준:** 성적 관리 흐름 단절

### Step 6: 퇴원 관리 필터 훅 연결 검증

**검사:** WithdrawalManagementTab에서 필터링 훅이 사용되는지 확인합니다.

```bash
grep -n "useWithdrawalFilters" components/WithdrawalManagement/WithdrawalManagementTab.tsx | head -5
```

**PASS 기준:** useWithdrawalFilters 훅 사용 확인
**FAIL 기준:** 필터 훅 연결 누락

### Step 7: 학생 필터링 훅 연결 검증

**검사:** StudentManagementTab에서 useStudentFilters 훅이 사용되는지 확인합니다.

```bash
grep -n "useStudentFilters" components/StudentManagement/StudentManagementTab.tsx | head -5
```

**PASS 기준:** 학생 필터링 훅 연결 확인
**FAIL 기준:** 필터링 기능이 UI에서 분리됨

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | 7개 탭 lazy import | TabContent.tsx | PASS/FAIL | |
| 2 | 학생 상세 6개 서브탭 | StudentDetailModal | PASS/FAIL | |
| 3 | 학생 mutation 훅 | hooks/ | PASS/FAIL | 훅별 mutation 수 |
| 4 | 상담 컴포넌트 분리 | Registration/Student | PASS/FAIL | |
| 5 | 성적 CRUD 흐름 | GradesManager | PASS/FAIL | |
| 6 | 퇴원 통계/필터 | WithdrawalManagement | PASS/FAIL | |
| 7 | 학생 필터링 연결 | StudentManagement | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **StudentManagementTab 내부의 5개 lazy import** - 서브탭과 모달을 lazy load하는 것은 코드 스플리팅을 위한 정상 패턴
2. **ConsultationDrafts의 onSnapshot 사용** - 임시저장은 실시간 동기화가 필요하므로 onSnapshot 사용이 정상
3. **WithdrawalManagementTab의 간소한 구조** - 3개 파일로 구성된 단순한 탭으로 별도 hooks 디렉토리 없이 직접 hooks/ 사용
4. **grades/GoalSettingModal, LevelTestModal의 중첩 구조** - 학생 상세 > 성적 탭 > 목표/레벨 모달의 3단 중첩은 도메인 복잡성에 따른 정상 구조
5. **useConsultationStats의 App.tsx 레벨 사용** - 상담 통계는 대시보드에서도 사용되므로 탭 외부에서의 import는 정상
