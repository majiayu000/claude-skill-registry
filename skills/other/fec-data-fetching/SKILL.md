---
name: fec-data-fetching
description: 用于实现或审查前端服务端状态流程：类型化查询、请求缓存、失效、mutation、乐观更新、无限查询、预取、SSR hydration 或 API 层整合。不要用于本地 UI 状态或 Service Worker 缓存；中文触发词包括 数据获取、缓存、乐观更新。
---

# Server State 数据获取

## 用途

为前端 server state 建立清晰的数据获取、缓存、失效和提交边界，避免请求状态散落在页面组件中。

## 流程

1. 判断状态来源：来自服务端且需要缓存、去重、刷新、分页或 mutation 时使用请求缓存方案；纯本地 UI 状态用组件 state 或 store。
2. 先沿用项目已有数据获取库；新增依赖时 React/Vue/Solid/Svelte 可考虑 TanStack Query，也可沿用 SWR、Nuxt/Nitro 数据获取或项目封装。
3. 设计稳定 cache key/query key：结构包含实体、动作和所有影响结果的参数。
4. API 函数保持纯请求函数，数据 hook/composable 负责缓存、select、loading/error/empty 状态。
5. mutation 成功后 invalidation；需要即时反馈时使用 optimistic update 并在失败时回滚。

## React 快速开始

```tsx
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function UserList({ keyword }: { keyword: string }) {
  const query = useQuery({
    queryKey: ["users", "list", { keyword }],
    queryFn: () => getUserList({ keyword, page: 1, pageSize: 20 }),
    select: (response) => response.list,
  });

  if (query.isLoading) return <Skeleton />;
  if (query.isError) return <ErrorFallback onRetry={() => query.refetch()} />;
  if (!query.data?.length) return <EmptyState />;

  return query.data.map((user) => <UserRow key={user.id} user={user} />);
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createUser,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }),
  });
}
```

## 详细参考

涉及是否需要查询库、QueryClient 默认配置、Vue adapter、乐观更新、无限滚动查询、预取、SSR 水合和 API 层整合时，加载 [references/query-patterns.md](references/query-patterns.md)。

## 约束

- 相同数据必须复用相同 cache key/query key；参数缺失会造成缓存串读。
- `staleTime` 过长会显示旧数据，过短会造成频繁请求。
- 请求缓存库不管理本地 UI 状态；不要把 modal、输入框值放进 query cache。
- 乐观更新必须保存快照并在失败时回滚。
- SSR/SSG 场景必须使用框架支持的预取、水合或服务端数据边界。

## 预期输出

数据获取层具备 loading/error/empty/data 状态，重复请求自动去重，mutation 后缓存正确失效或回滚，API 层与 UI 层边界清晰。
