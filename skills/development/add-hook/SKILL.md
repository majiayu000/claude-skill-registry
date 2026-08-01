---
name: add-hook
description: '새 커스텀 훅을 생성합니다. TanStack Query 패턴을 적용합니다. 사용법: /add-hook useXxx [--mutation]'
---

---
name: add-hook
description: 새 커스텀 훅을 생성합니다. TanStack Query 패턴을 적용합니다. 사용법: /add-hook useXxx [--mutation]
---

# Add Hook

TanStack Query 패턴을 적용한 커스텀 훅을 생성합니다.

## Instructions

1. 사용자로부터 훅 이름(use 접두사 + camelCase)을 받습니다
2. `--mutation` 플래그가 있으면 mutation 훅도 포함합니다
3. 파일 위치: `src/hooks/useXxx.ts`
4. 해당 서비스 파일이 존재하는지 확인합니다

## Template

```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { xxxService } from "@/services/xxxService";

// Query Keys
export const xxxKeys = {
  all: ["xxx"] as const,
  lists: () => [...xxxKeys.all, "list"] as const,
  list: (filters: Record<string, unknown>) =>
    [...xxxKeys.lists(), filters] as const,
  details: () => [...xxxKeys.all, "detail"] as const,
  detail: (id: string) => [...xxxKeys.details(), id] as const,
};

export function useXxxList(options?: { enabled?: boolean }) {
  return useQuery({
    queryKey: xxxKeys.lists(),
    queryFn: () => xxxService.getAll(),
    enabled: options?.enabled !== false,
    staleTime: 1000 * 60 * 5,
  });
}

export function useXxx(id: string, options?: { enabled?: boolean }) {
  return useQuery({
    queryKey: xxxKeys.detail(id),
    queryFn: () => xxxService.getById(id),
    enabled: !!id && options?.enabled !== false,
  });
}
```

## Mutation Template (--mutation)

```typescript
export function useCreateXxx() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateXxxInput) => xxxService.create(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: xxxKeys.lists() });
    },
  });
}
```

## Checklist

- queryKey 상수 정의
- staleTime 설정
- enabled 옵션 지원
- invalidateQueries on mutation success

## Examples

```
/add-hook useItems --mutation
```

→ `src/hooks/useItems.ts` 생성 (query + mutation)
