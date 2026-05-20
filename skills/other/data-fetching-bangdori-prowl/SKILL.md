---
name: data-fetching
description: TanStack Query 기반 데이터 페칭 패턴
---

# Data Fetching Patterns

TanStack Query (`@tanstack/react-query`)를 사용한 데이터 페칭 규칙.

## 구조

```
src/renderer/
├── queries/
│   ├── client.ts    # QueryClient 인스턴스 (staleTime: 30s)
│   └── keys.ts      # 쿼리 키 팩토리
└── hooks/
    ├── useLaunchdJobs.ts   # useQuery 예시
    ├── useJobActions.ts    # useMutation 예시
    ├── useSettings.ts      # 공유 상태 예시
    ├── useFocusMode.ts     # optimistic update 예시
    └── useCalendarData.ts  # 복합 훅 예시
```

## 쿼리 키

`src/renderer/queries/keys.ts`에 정의된 팩토리 사용:

```typescript
queryKeys.jobs.list()        // ["jobs", "list"]
queryKeys.calendar.events()  // ["calendar", "events"]
queryKeys.settings.get()     // ["settings", "get"]
```

**새 쿼리 추가 시 반드시 keys.ts에 키 정의.**

## 읽기 (useQuery)

```typescript
const { data: jobs = [], isLoading, error } = useQuery({
  queryKey: queryKeys.jobs.list(),
  queryFn: () => window.electronAPI.listJobs(),
  refetchInterval: JOB_POLLING_INTERVAL_MS,  // 폴링 (선택)
});
```

### 조건부 폴링

running job이 있을 때만 빠르게 폴링:

```typescript
refetchInterval: (query) =>
  (query.state.data?.length ?? 0) > 0 ? 1000 : false,
```

## 쓰기 (useMutation)

```typescript
const mutation = useMutation({
  mutationFn: (settings: AppSettings) =>
    window.electronAPI.setSettings(settings),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: queryKeys.settings.all });
  },
});
```

## 낙관적 업데이트

```typescript
const mutation = useMutation({
  mutationFn: (event: LocalEvent) => window.electronAPI.addLocalEvent(event),
  onMutate: async (event) => {
    await queryClient.cancelQueries({ queryKey: queryKeys.calendar.events() });
    const previous = queryClient.getQueryData(queryKeys.calendar.events());
    queryClient.setQueryData(queryKeys.calendar.events(), (old = []) =>
      [...old, toCalendarEvent(event)],
    );
    return { previous };
  },
  onError: (_err, _vars, context) => {
    if (context?.previous)
      queryClient.setQueryData(queryKeys.calendar.events(), context.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: queryKeys.calendar.events() });
  },
});
```

## 핵심 규칙

1. **컴포넌트에서 `window.electronAPI` 직접 호출 금지** — 반드시 hooks 사용
2. mutation 성공 시 관련 쿼리 `invalidateQueries` 필수
3. 낙관적 업데이트는 `onMutate` + `onError` + `onSettled` 세트
4. 새 도메인 추가 시 `queries/keys.ts`에 키 팩토리 추가
5. `window.electronAPI.onWindowShow` 이벤트 시 `invalidateQueries`로 새로고침
