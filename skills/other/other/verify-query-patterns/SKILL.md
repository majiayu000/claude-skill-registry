---
name: verify-query-patterns
description: React Query 캐시키/enabled/staleTime 일관성과 쿼리 패턴을 검증합니다. React Query 훅 수정 후 사용.
---

## Purpose

1. **캐시 키 일관성** - queryKey 네이밍 규칙이 프로젝트 전반에서 일관적인지 검증
2. **enabled 조건** - 의존성이 있는 쿼리에 enabled 옵션이 올바르게 설정되어 있는지 검증
3. **staleTime/gcTime 설정** - queryClient 기본값과 개별 쿼리의 캐시 설정이 적절한지 검증
4. **QueryClientProvider 설정** - 앱 진입점에서 QueryClient가 올바르게 제공되는지 검증

## When to Run

- `hooks/` 디렉토리에서 useQuery/useMutation을 사용하는 훅을 추가/수정한 후
- `queryClient.ts` 설정을 변경한 후
- React Query 관련 캐시 이슈가 발생했을 때
- 새로운 데이터 패칭 훅을 생성한 후

## Related Files

| File | Purpose |
|------|---------|
| `queryClient.ts` | QueryClient 설정 (staleTime: 5분, gcTime: 30분, retry: 1) |
| `index.tsx` | QueryClientProvider 래핑 |
| `hooks/useStudents.ts` | 학생 쿼리 (queryKey 패턴 참조) |
| `hooks/useClasses.ts` | 수업 쿼리 |
| `hooks/useStaff.ts` | 직원 쿼리 |
| `hooks/useConsultations.ts` | 상담 쿼리 |
| `hooks/useBilling.ts` | 수납 쿼리 |
| `hooks/useFirebaseQueries.ts` | Firebase 공통 쿼리 |
| `hooks/useEnrollments.ts` | 수강 등록 쿼리 |
| `hooks/useGradeProfile.ts` | 성적 프로필 쿼리 |
| `hooks/useTextbookRequests.ts` | 교재 요청서 쿼리 (textbookRequests, textbookAccountSettings, textbookCatalog) |

## Workflow

### Step 1: QueryClient 설정 검증

**검사:** queryClient.ts에서 기본 설정이 올바르게 정의되어 있는지 확인합니다.

```bash
grep -n "staleTime\|gcTime\|retry\|refetchOnWindowFocus" queryClient.ts | head -10
```

**PASS 기준:** staleTime, gcTime, retry 설정이 존재
**FAIL 기준:** QueryClient 기본 설정 누락

### Step 2: QueryClientProvider 래핑 검증

**검사:** index.tsx에서 QueryClientProvider가 앱을 감싸는지 확인합니다.

```bash
grep -n "QueryClientProvider" index.tsx | head -5
```

**PASS 기준:** QueryClientProvider로 앱 래핑됨
**FAIL 기준:** QueryClientProvider 누락 (모든 쿼리 실패)

### Step 3: useQuery enabled 옵션 검증

**검사:** 의존성이 있는 쿼리에서 enabled 옵션을 사용하는지 확인합니다 (departmentId, userId 등이 필요한 쿼리).

```bash
for f in $(grep -l "useQuery" hooks/*.ts 2>/dev/null); do
  has_enabled=$(grep -c "enabled" "$f");
  has_dep=$(grep -c "departmentId\|userId\|classId\|studentId" "$f");
  if [ "$has_dep" -gt 0 ] && [ "$has_enabled" -eq 0 ]; then
    echo "WARNING: $f has dependencies but no enabled option";
  fi;
done
```

**PASS 기준:** 의존성이 있는 모든 쿼리에 enabled 옵션 존재
**FAIL 기준:** 의존성이 undefined일 수 있는데 enabled 체크 없음

**수정:** `enabled: !!departmentId` 또는 `enabled: Boolean(userId)` 추가

### Step 4: queryKey 네이밍 패턴 검증

**검사:** queryKey가 일관된 배열 패턴을 사용하는지 확인합니다.

```bash
grep -rn "queryKey" hooks/*.ts 2>/dev/null | grep -v "invalidateQueries\|node_modules" | head -20
```

**PASS 기준:** queryKey가 배열 형태 `['category', ...params]`로 일관되게 사용됨
**FAIL 기준:** 문자열 키 또는 불일치하는 키 패턴 발견

### Step 5: invalidateQueries와 queryKey 매칭 검증

**검사:** mutation의 invalidateQueries에서 사용하는 키가 실제 useQuery의 queryKey와 매칭되는지 확인합니다.

```bash
grep -rn "invalidateQueries" hooks/*.ts 2>/dev/null | grep "queryKey" | head -20
```

**PASS 기준:** invalidateQueries의 키가 해당 쿼리의 queryKey 접두사와 일치
**FAIL 기준:** 잘못된 키로 캐시 무효화 시도 (캐시 갱신 실패)

### Step 6: onSnapshot vs useQuery 분리 검증

**검사:** onSnapshot(실시간)과 useQuery(폴링)가 혼용되지 않는지 확인합니다.

```bash
for f in $(grep -l "onSnapshot" hooks/*.ts 2>/dev/null); do
  has_usequery=$(grep -c "useQuery" "$f");
  if [ "$has_usequery" -gt 0 ]; then
    echo "MIXED: $f uses both onSnapshot and useQuery";
  fi;
done
```

**PASS 기준:** 각 훅이 onSnapshot 또는 useQuery 중 하나만 사용
**FAIL 기준:** 같은 데이터에 대해 두 패턴 혼용 (중복 요청, 데이터 불일치 가능)

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | QueryClient 설정 | queryClient.ts | PASS/FAIL | |
| 2 | QueryClientProvider | index.tsx | PASS/FAIL | |
| 3 | enabled 옵션 | hooks/ (의존성 쿼리) | PASS/FAIL | N개 경고 |
| 4 | queryKey 패턴 | hooks/ | PASS/FAIL | |
| 5 | invalidateQueries 매칭 | hooks/ (mutation) | PASS/FAIL | |
| 6 | onSnapshot/useQuery 분리 | hooks/ | PASS/FAIL | N개 혼용 |

## Exceptions

다음은 **위반이 아닙니다**:

1. **useFirebaseQueries의 다중 useQuery** - 여러 Firebase 컬렉션을 한 훅에서 조회하는 것은 편의를 위한 패턴
2. **useAppState의 queryKey 부재** - Zustand/useState 기반 상태 관리 훅은 React Query를 사용하지 않음
3. **useEventCrud의 useQuery 부재** - 이벤트는 App.tsx의 onSnapshot으로 실시간 동기화되므로 별도 useQuery 불필요
4. **useConsultationDrafts의 onSnapshot + invalidateQueries** - 임시저장은 실시간 동기화 + 다른 관련 쿼리 캐시 무효화가 동시에 필요한 특수 케이스
5. **enabled: false인 쿼리의 fetchStatus: 'idle'** - React Query v5에서 enabled: false면 쿼리가 idle 상태이며, 이는 정상 동작
