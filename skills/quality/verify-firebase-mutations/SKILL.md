---
name: verify-firebase-mutations
description: Firebase mutation 훅의 invalidateQueries/에러처리/writeBatch 패턴을 검증합니다. mutation 훅 수정 후 사용.
---

## Purpose

1. **useMutation + invalidateQueries 쌍** - useMutation을 사용하는 훅이 onSuccess에서 invalidateQueries를 호출하는지 검증
2. **writeBatch 패턴** - 다중 문서 수정 시 writeBatch를 사용하는지 검증
3. **에러 처리** - mutation 함수에 try/catch 또는 onError 핸들러가 있는지 검증
4. **useQueryClient 사용** - mutation 훅이 queryClient를 올바르게 가져오는지 검증

## When to Run

- `hooks/` 디렉토리의 mutation 훅을 추가하거나 수정한 후
- Firebase 쓰기 작업(setDoc, updateDoc, writeBatch)을 변경한 후
- React Query 캐시 무효화 로직을 수정한 후
- 새로운 CRUD 훅을 생성한 후

## Related Files

| File | Purpose |
|------|---------|
| `hooks/useAttendance.ts` | 출결 관리 (11 mutations, 9 invalidations) |
| `hooks/useClassMutations.ts` | 수업 CRUD (5 mutations, 20 invalidations) |
| `hooks/useConsultationMutations.ts` | 상담 CRUD (5 mutations, 4 invalidations) |
| `hooks/useGradeProfile.ts` | 성적 관리 (10 mutations, 9 invalidations) |
| `hooks/useStaff.ts` | 직원 관리 (4 mutations, 6 invalidations) |
| `hooks/useStudents.ts` | 학생 관리 (4 mutations, 3 invalidations) |
| `hooks/useStudentGrades.ts` | 학생 성적 (4 mutations, 11 invalidations) |
| `hooks/useStaffLeaves.ts` | 휴가 관리 (5 mutations, 4 invalidations) |
| `hooks/useDailyAttendance.ts` | 일일 출결 (5 mutations, 4 invalidations) |
| `hooks/useBilling.ts` | 청구 관리 (5 mutations, 5 invalidations) |
| `hooks/useResources.ts` | 자료 관리 (4 mutations, 3 invalidations) |
| `hooks/useSessionPeriods.ts` | 교시 관리 (4 mutations, 6 invalidations) |
| `hooks/useEnrollmentTerms.ts` | 등록 학기 (4 mutations, 3 invalidations) |
| `hooks/useExams.ts` | 시험 관리 (4 mutations, 4 invalidations) |
| `hooks/useExamSeries.ts` | 시험 시리즈 (2 mutations, 1 invalidation) |
| `hooks/useGanttProjects.ts` | 간트 프로젝트 (4 mutations, 3 invalidations) |
| `hooks/useGanttTemplates.ts` | 간트 템플릿 (4 mutations, 3 invalidations) |
| `hooks/useConsultations.ts` | 상담 조회/수정 (4 mutations, 3 invalidations) |
| `hooks/useConsultationDrafts.ts` | 상담 임시저장 (3 mutations, onSnapshot 기반) |
| `hooks/useGradePromotion.ts` | 진급 관리 (2 mutations, 1 invalidation) |
| `hooks/useBatchAttendanceUpdate.ts` | 일괄 출결 (2 mutations, 2 invalidations) |
| `hooks/useContracts.ts` | 계약 관리 (4 mutations, 3 invalidations) |
| `hooks/useHomework.ts` | 숙제 관리 (4 mutations, 3 invalidations) |
| `hooks/useMarketing.ts` | 마케팅 관리 (4 mutations, 3 invalidations) |
| `hooks/useNotices.ts` | 공지사항 (4 mutations, 3 invalidations) |
| `hooks/useNotifications.ts` | 알림 관리 (4 mutations, 3 invalidations) |
| `hooks/useParentLinks.ts` | 학부모 연동 (3 mutations, 2 invalidations) |
| `hooks/useParentMessages.ts` | 학부모 메시지 (3 mutations, 2 invalidations) |
| `hooks/usePayroll.ts` | 급여 관리 (4 mutations, 3 invalidations) |
| `hooks/useShuttle.ts` | 셔틀 관리 (4 mutations, 3 invalidations) |
| `hooks/useTextbooks.ts` | 교재 수납 관리 (5 mutations, 5 invalidations, 자동 매칭 포함) |
| `hooks/useTextbookRequests.ts` | 교재 요청서 CRUD + 계좌설정 + 카탈로그 (6 mutations, 6 invalidations) |

## Workflow

### Step 1: useMutation 훅 목록 확인

**검사:** useMutation을 사용하는 모든 훅 파일을 식별합니다.

```bash
grep -l "useMutation" hooks/*.ts hooks/*.tsx 2>/dev/null | sort
```

**정보:** 현재 32개 훅이 useMutation을 사용합니다.

### Step 2: invalidateQueries 존재 검증

**검사:** useMutation을 사용하는 훅이 invalidateQueries도 호출하는지 확인합니다. onSnapshot 기반 훅은 면제입니다.

```bash
for f in $(grep -l "useMutation" hooks/*.ts hooks/*.tsx 2>/dev/null); do
  has_invalidate=$(grep -c "invalidateQueries" "$f");
  has_snapshot=$(grep -c "onSnapshot" "$f");
  if [ "$has_invalidate" -eq 0 ] && [ "$has_snapshot" -eq 0 ]; then
    echo "WARNING: $f has useMutation but no invalidateQueries and no onSnapshot";
  fi;
done
```

**PASS 기준:** 모든 mutation 훅이 invalidateQueries 또는 onSnapshot 사용
**FAIL 기준:** mutation은 있지만 캐시 갱신 메커니즘이 없는 훅 발견

**수정:** `onSuccess` 콜백에 `queryClient.invalidateQueries({ queryKey: ['관련키'] })` 추가

### Step 3: useQueryClient import 검증

**검사:** invalidateQueries를 사용하는 훅이 useQueryClient를 올바르게 import하는지 확인합니다.

```bash
for f in $(grep -l "invalidateQueries" hooks/*.ts hooks/*.tsx 2>/dev/null); do
  has_client=$(grep -c "useQueryClient" "$f");
  if [ "$has_client" -eq 0 ]; then
    echo "MISSING useQueryClient: $f";
  fi;
done
```

**PASS 기준:** invalidateQueries를 사용하는 모든 훅에 useQueryClient 존재
**FAIL 기준:** useQueryClient 없이 invalidateQueries 사용 시도

**수정:** `const queryClient = useQueryClient()` 추가 및 `@tanstack/react-query`에서 import

### Step 4: writeBatch import 일관성 검증

**검사:** writeBatch를 사용하는 파일이 올바르게 import하는지 확인합니다.

```bash
grep -rn "writeBatch" hooks/*.ts hooks/*.tsx 2>/dev/null | grep -v "import" | head -20
grep -rn "import.*writeBatch" hooks/*.ts hooks/*.tsx 2>/dev/null
```

**PASS 기준:** writeBatch 사용하는 모든 파일에서 `import { writeBatch } from 'firebase/firestore'` 존재
**FAIL 기준:** writeBatch를 import 없이 사용

### Step 5: mutation 에러 처리 검증

**검사:** useMutation 훅이 에러 처리를 포함하는지 확인합니다 (onError 콜백 또는 mutationFn 내 try/catch).

```bash
for f in $(grep -l "useMutation" hooks/*.ts hooks/*.tsx 2>/dev/null); do
  has_onerror=$(grep -c "onError" "$f");
  has_trycatch=$(grep -c "try {" "$f");
  if [ "$has_onerror" -eq 0 ] && [ "$has_trycatch" -eq 0 ]; then
    echo "NO ERROR HANDLING: $f";
  fi;
done
```

**PASS 기준:** 모든 mutation 훅에 onError 또는 try/catch 존재
**FAIL 기준:** 에러 처리 없는 mutation 훅 발견

**수정:** `onError: (error) => { console.error(error); }` 또는 mutationFn 내 try/catch 추가

### Step 6: Firebase 쓰기 작업 카운트 요약

**검사:** 프로젝트 전체의 Firebase 쓰기 작업 분포를 보고합니다.

```bash
echo "writeBatch: $(grep -rl 'writeBatch' hooks/ --include='*.ts' 2>/dev/null | wc -l) files"
echo "setDoc: $(grep -rl 'setDoc' hooks/ --include='*.ts' 2>/dev/null | wc -l) files"
echo "updateDoc: $(grep -rl 'updateDoc' hooks/ --include='*.ts' 2>/dev/null | wc -l) files"
echo "deleteDoc: $(grep -rl 'deleteDoc' hooks/ --include='*.ts' 2>/dev/null | wc -l) files"
echo "useMutation: $(grep -rl 'useMutation' hooks/ --include='*.ts' 2>/dev/null | wc -l) files"
```

**정보:** 이 단계는 PASS/FAIL이 아닌 현황 보고입니다.

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | useMutation 목록 | hooks/ | INFO | N개 훅 |
| 2 | invalidateQueries 존재 | mutation 훅 | PASS/FAIL | N개 경고 |
| 3 | useQueryClient import | invalidation 훅 | PASS/FAIL | N개 누락 |
| 4 | writeBatch import | writeBatch 사용 훅 | PASS/FAIL | |
| 5 | 에러 처리 | mutation 훅 | PASS/FAIL | N개 미처리 |
| 6 | Firebase 쓰기 요약 | hooks/ | INFO | 분포 보고 |

## Exceptions

다음은 **위반이 아닙니다**:

1. **onSnapshot 기반 훅의 invalidateQueries 부재** - `useConsultationDrafts`, `useBucketItems`, `useTaskMemos`는 Firestore 실시간 리스너(onSnapshot)를 사용하여 자동으로 데이터가 갱신되므로 invalidateQueries가 불필요
2. **useEventCrud의 invalidateQueries 부재** - 이벤트는 App.tsx에서 전역 onSnapshot으로 실시간 동기화되므로 개별 invalidation 불필요
3. **컴포넌트 내부의 직접 Firebase 쓰기** - `components/` 내에서 직접 setDoc/updateDoc을 사용하는 경우는 이 스킬의 범위 밖 (마이그레이션 모달, 설정 탭 등의 일회성 작업)
4. **useEmbedTokens의 invalidateQueries 부재** - 토큰 생성 후 로컬 상태로 관리하며 React Query 캐시를 사용하지 않음
5. **hooks에서 alert() 사용** - happy-dom 환경에서 alert가 없지만, 이는 테스트 환경 이슈이며 프로덕션에서는 정상 동작
