---
name: fec-state-management
description: 用于选择、实现、审查或重构 React、Vue、Next.js、Nuxt、URL 状态、服务端状态、表单状态、浏览器持久化或全局 store 的前端状态归属。TanStack Query 缓存细节、浏览器存储持久化或表单校验内部问题优先使用更窄的 skill；中文触发词包括 状态管理、状态归属、store 选型。
---

# 前端状态管理

## 用途

为前端状态确定清晰归属，避免全局 store 膨胀、重复缓存和派生状态同步错误。

## 流程

### 1. 先分类状态来源

不要先选 Redux、Zustand、Pinia 或 Context。先把每个状态标到唯一归属，再决定工具。

| 状态类型         | 典型例子                             | 默认归属                 |
| ---------------- | ------------------------------------ | ------------------------ |
| 本地 UI 状态     | 弹窗开关、tab、展开行、hover 编辑态  | 组件内 state / ref       |
| 表单状态         | 输入值、脏字段、校验错误、提交中     | 表单库或表单组件         |
| 服务端状态       | 列表、详情、分页结果、远程错误       | 请求缓存库               |
| URL 状态         | 搜索词、筛选、排序、页码、选中 tab   | 路由参数 / search params |
| 全局客户端状态   | 登录用户、主题、权限快照、购物车草稿 | 全局 store               |
| 浏览器持久化状态 | 跨刷新保留的草稿、偏好、离线队列     | 存储层 + 状态适配器      |

```tsx
type ReportsStateMap = {
  search: "url";
  selectedReportId: "url";
  reports: "server-state-cache";
  isFilterPanelOpen: "local-ui";
  draftColumns: "browser-persistence";
};
```

### 2. 保持最小状态

可从 props、server state、URL 或已有 state 推导出来的值，不要另存一份。

```tsx
interface Invoice {
  id: string;
  status: "draft" | "sent" | "paid";
}

function InvoiceList({ invoices }: { invoices: Invoice[] }) {
  const paidInvoices = invoices.filter((invoice) => invoice.status === "paid");

  return <span>{paidInvoices.length}</span>;
}
```

### 3. 选择 React 全局状态方案

React 中优先本地化和组合；只有跨页面、跨 feature 或需要统一动作时才引入全局 store。

```tsx
import { create } from "zustand";

interface WorkspaceState {
  activeWorkspaceId: string | null;
  setActiveWorkspaceId: (workspaceId: string) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  activeWorkspaceId: null,
  setActiveWorkspaceId: (activeWorkspaceId) => set({ activeWorkspaceId }),
}));
```

决策顺序：

1. 只在一个组件或一个小子树使用：`useState` / `useReducer`。
2. 低频全局配置或依赖注入：Context。
3. 中等复杂业务状态：Zustand 或 Jotai，按仓库现有选型优先。
4. 大型应用、严格动作流、审计或时间旅行调试：Redux Toolkit。
5. 远程数据：使用数据获取 skill 管理 query key、缓存和失效策略。

### 4. 选择 Vue 全局状态方案

Vue 3 中，局部跨层级传递使用 `provide/inject`；全局业务状态使用 Pinia 或项目既有 store。

```ts
import { computed, readonly, ref } from "vue";
import { defineStore } from "pinia";

export const useSessionStore = defineStore("session", () => {
  const userId = ref<string | null>(null);
  const isSignedIn = computed(() => userId.value !== null);

  function signIn(nextUserId: string) {
    userId.value = nextUserId;
  }

  return {
    userId: readonly(userId),
    isSignedIn,
    signIn,
  };
});
```

### 5. 明确状态边界和迁移步骤

重构状态时先做状态清单，再逐步移动读写入口。每一步都应保持行为可验证。

```ts
interface StateMigrationItem {
  name: string;
  currentOwner: "component" | "context" | "store" | "query-cache" | "url";
  targetOwner: "component" | "context" | "store" | "query-cache" | "url";
  verification: string;
}

const migrationPlan: StateMigrationItem[] = [
  {
    name: "dashboard filters",
    currentOwner: "store",
    targetOwner: "url",
    verification: "refreshing the page preserves filters through search params",
  },
];
```

## 详细参考

需要 Store 形状示例、选择器模式、URL 状态同步、持久化适配器、SSR 边界或审查清单时，加载 [references/state-patterns.md](references/state-patterns.md)。

## 约束

- 不把服务端响应复制到全局 store；缓存、失效和重试归数据获取层。
- 不把表单每个字段提升到全局 store；跨步骤共享也优先由表单上下文或提交草稿适配器处理。
- 不用 Context 承载高频变化的大对象；会扩大重渲染范围。
- 持久化状态必须明确字段白名单、版本号、过期策略和敏感数据排除。
- SSR 场景不要在模块顶层创建带用户数据的单例 store。

## 预期输出

产出状态归属清单、选型理由、store/API 边界和验证步骤。实现时应保留 loading/error/empty、刷新、回退、跨路由和权限变化等关键行为。
