---
name: frontend-svelte
description: 现代前端开发综合技能，涵盖 Svelte、SvelteKit、shadcn-svelte 和 Bun 生态系统。使用此技能构建现代 Web 应用、创建 UI 组件、实现状态管理、处理表单，或使用基于 TypeScript 的前端架构时使用。适用于需要响应式框架、服务端渲染或类型安全组件开发的项目。
---

# 前端开发技能

现代前端开发的综合技能，包含 Svelte、SvelteKit、shadcn-svelte 和 Bun 生态系统。

## 技术栈

### 核心框架：Svelte + SvelteKit

#### Svelte 基础
- **响应式框架**：编译时框架，将组件转换为高效的命令式代码
- **真正的响应式**：自动依赖跟踪，无需虚拟 DOM
- **小包体积**：最小的运行时开销
- **内置动画**：过渡和动画指令
- **作用域样式**：组件样式默认作用域

#### SvelteKit 特性
- **全栈框架**：服务端渲染（SSR）、静态站点生成（SSG）和客户端渲染（CSR）
- **基于文件的路由**：路由由文件系统结构定义
- **API 路由**：在前端代码旁构建 API 端点
- **表单操作**：服务端表单处理，渐进式增强
- **钩子**：拦截和修改请求/响应
- **适配器**：部署到任何平台（Node、Vercel、Netlify、Cloudflare 等）

### UI 组件库：shadcn-svelte

#### 概览
- shadcn/ui 的 Svelte 版本
- 基于 Radix Svelte（Melt UI）构建的可访问、可定制组件
- 复制粘贴组件方式（不是 npm 包）
- 使用 Tailwind CSS 构建
- TypeScript 支持

#### 关键组件
- **表单**：Input、Textarea、Select、Checkbox、Radio、Switch
- **反馈**：Alert、Toast（Sonner）、Dialog、Alert Dialog
- **导航**：Button、Dropdown Menu、Tabs、Command Menu
- **布局**：Card、Separator、Accordion、Collapsible
- **数据展示**：Table、Badge、Avatar、Skeleton
- **覆盖层**：Popover、Tooltip、Sheet、Drawer

#### 安装和使用
```bash
# 初始化 shadcn-svelte
bunx shadcn-svelte@latest init

# 按需添加组件
bunx shadcn-svelte@latest add button
bunx shadcn-svelte@latest add card
bunx shadcn-svelte@latest add form
```

### 包管理器：Bun

#### 为什么选择 Bun？
- **性能**：比 npm 快 25 倍，比 pnpm 快 4 倍
- **一体化**：运行时、打包器、测试运行器、包管理器
- **直接替换**：兼容 npm/Node.js 生态系统
- **内置测试**：兼容 Vitest 的测试运行器
- **原生 TypeScript**：原生 TypeScript 支持，无需编译

#### npm 兼容性
- 读取 package.json 和 package-lock.json/bun.lockb
- 与大多数 npm 包兼容
- 可以通过 `bun run` 运行 npm 脚本
- 特定包需要时可回退到 npm

## 项目架构

### 推荐的目录结构

```
project-root/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ui/              # shadcn-svelte 组件
│   │   │   │   ├── button/
│   │   │   │   ├── card/
│   │   │   │   └── ...
│   │   │   ├── layout/          # 布局组件
│   │   │   │   ├── Header.svelte
│   │   │   │   ├── Footer.svelte
│   │   │   │   └── Sidebar.svelte
│   │   │   └── features/        # 功能特定组件
│   │   │       ├── auth/
│   │   │       ├── dashboard/
│   │   │       └── ...
│   │   ├── stores/              # Svelte stores
│   │   │   ├── user.ts
│   │   │   ├── theme.ts
│   │   │   └── notifications.ts
│   │   ├── utils/               # 工具函数
│   │   │   ├── api.ts
│   │   │   ├── validation.ts
│   │   │   └── formatting.ts
│   │   ├── types/               # TypeScript 类型
│   │   │   ├── api.ts
│   │   │   └── models.ts
│   │   ├── server/              # 服务端工具
│   │   │   ├── db.ts
│   │   │   └── auth.ts
│   │   └── config/              # 配置
│   │       ├── constants.ts
│   │       └── env.ts
│   ├── routes/                  # SvelteKit 路由
│   │   ├── +page.svelte         # 首页
│   │   ├── +layout.svelte       # 根布局
│   │   ├── +error.svelte        # 错误页面
│   │   ├── api/                 # API 路由
│   │   │   └── users/
│   │   │       └── +server.ts
│   │   ├── (auth)/              # 路由组
│   │   │   ├── login/
│   │   │   └── register/
│   │   └── dashboard/
│   │       ├── +page.svelte
│   │       └── +page.server.ts
│   ├── app.html                 # HTML 模板
│   ├── app.css                  # 全局样式
│   └── hooks.server.ts          # 服务器钩子
├── static/                      # 静态资源
│   ├── images/
│   └── fonts/
├── tests/                       # 测试
│   ├── unit/
│   └── integration/
├── bun.lockb                    # Bun 锁文件
├── package.json
├── svelte.config.js
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## 核心模式和最佳实践

### 1. 组件开发

#### 组件结构最佳实践
```svelte
<script lang="ts">
  // 1. 导入（外部，然后内部）
  import { onMount, createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  import type { User } from '$lib/types';
  import { Button } from '$lib/components/ui/button';

  // 2. 类型定义（如果不在单独文件中）
  interface $$Props {
    user: User;
    variant?: 'default' | 'compact';
  }

  // 3. 带默认值的 Props
  export let user: User;
  export let variant: $$Props['variant'] = 'default';

  // 4. 事件调度器
  const dispatch = createEventDispatcher<{
    edit: { userId: string };
    delete: { userId: string };
  }>();

  // 5. 本地状态
  let isEditing = false;
  let formData = { ...user };

  // 6. 响应式声明
  $: fullName = `${user.firstName} ${user.lastName}`;
  $: hasChanges = JSON.stringify(formData) !== JSON.stringify(user);

  // 7. 函数
  function handleEdit() {
    isEditing = true;
  }

  function handleSave() {
    dispatch('edit', { userId: user.id });
    isEditing = false;
  }

  // 8. 生命周期钩子
  onMount(() => {
    console.log('组件已挂载');

    return () => {
      console.log('组件将卸载');
    };
  });
</script>

<!-- 具有清晰层次结构的模板 -->
<div class="user-card" class:compact={variant === 'compact'}>
  {#if isEditing}
    <form on:submit|preventDefault={handleSave}>
      <!-- 编辑模式 -->
    </form>
  {:else}
    <!-- 查看模式 -->
    <div class="user-info" transition:fade>
      <h3>{fullName}</h3>
      <p>{user.email}</p>
    </div>
    <Button on:click={handleEdit}>编辑</Button>
  {/if}
</div>

<!-- 作用域样式 -->
<style lang="postcss">
  .user-card {
    @apply rounded-lg border p-4;

    &.compact {
      @apply p-2;
    }
  }

  .user-info {
    @apply space-y-2;
  }
</style>
```

#### TypeScript Props 模式
```typescript
// 对于复杂的 props，使用 interface
interface $$Props {
  items: Item[];
  selectedId?: string;
  onSelect?: (item: Item) => void;
  class?: string;
}

export let items: $$Props['items'];
export let selectedId: $$Props['selectedId'] = undefined;
export let onSelect: $$Props['onSelect'] = undefined;

// 用于 class prop 转发
let className: $$Props['class'] = '';
export { className as class };
```

### 2. 状态管理

#### Svelte Stores

**可写 Store**
```typescript
// stores/user.ts
import { writable } from 'svelte/store';
import type { User } from '$lib/types';

function createUserStore() {
  const { subscribe, set, update } = writable<User | null>(null);

  return {
    subscribe,
    set,
    login: (user: User) => set(user),
    logout: () => set(null),
    updateProfile: (updates: Partial<User>) =>
      update(user => user ? { ...user, ...updates } : null)
  };
}

export const user = createUserStore();
```

**派生 Store**
```typescript
// stores/user.ts (续)
import { derived } from 'svelte/store';

export const isAuthenticated = derived(
  user,
  $user => $user !== null
);

export const userPermissions = derived(
  user,
  $user => $user?.roles.flatMap(role => role.permissions) ?? []
);
```

**可读 Store（用于外部数据）**
```typescript
import { readable } from 'svelte/store';

export const time = readable(new Date(), (set) => {
  const interval = setInterval(() => {
    set(new Date());
  }, 1000);

  return () => clearInterval(interval);
});
```

**带持久化的自定义 Store**
```typescript
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export function persistedStore<T>(key: string, initialValue: T) {
  const stored = browser ? localStorage.getItem(key) : null;
  const initial = stored ? JSON.parse(stored) : initialValue;

  const store = writable<T>(initial);

  if (browser) {
    store.subscribe(value => {
      localStorage.setItem(key, JSON.stringify(value));
    });
  }

  return store;
}

// 使用
export const theme = persistedStore<'light' | 'dark'>('theme', 'light');
```

#### Context API（组件树状态）
```svelte
<!-- Parent.svelte -->
<script lang="ts">
  import { setContext } from 'svelte';
  import type { Writable } from 'svelte/store';
  import { writable } from 'svelte/store';

  const formData = writable({ name: '', email: '' });
  setContext('form', formData);
</script>

<!-- Child.svelte -->
<script lang="ts">
  import { getContext } from 'svelte';
  import type { Writable } from 'svelte/store';

  const formData = getContext<Writable<FormData>>('form');
</script>

<input bind:value={$formData.name} />
```

### 3. SvelteKit 路由和数据加载

#### 页面结构
```typescript
// routes/blog/[slug]/+page.ts
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch, parent }) => {
  // 访问父布局数据
  const parentData = await parent();

  // 获取数据
  const response = await fetch(`/api/posts/${params.slug}`);
  const post = await response.json();

  return {
    post,
    meta: {
      title: post.title,
      description: post.excerpt
    }
  };
};
```

```svelte
<!-- routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.meta.title}</title>
  <meta name="description" content={data.meta.description} />
</svelte:head>

<article>
  <h1>{data.post.title}</h1>
  <div>{@html data.post.content}</div>
</article>
```

#### 服务端数据加载
```typescript
// routes/dashboard/+page.server.ts
import type { PageServerLoad, Actions } from './$types';
import { error, fail, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals, depends }) => {
  // depends() 为失效创建依赖
  depends('app:dashboard');

  if (!locals.user) {
    throw redirect(307, '/login');
  }

  try {
    const stats = await fetchUserStats(locals.user.id);
    return { stats };
  } catch (err) {
    throw error(500, '加载仪表板数据失败');
  }
};

export const actions: Actions = {
  updateProfile: async ({ request, locals }) => {
    const formData = await request.formData();
    const name = formData.get('name');

    if (!name) {
      return fail(400, { name, missing: true });
    }

    await updateUser(locals.user.id, { name });
    return { success: true };
  }
};
```

#### 渐进式增强的表单操作
```svelte
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';

  export let form: ActionData;

  let loading = false;
</script>

<form
  method="POST"
  action="?/updateProfile"
  use:enhance={() => {
    loading = true;

    return async ({ result, update }) => {
      await update();
      loading = false;

      if (result.type === 'success') {
        // 处理成功
      }
    };
  }}
>
  <input
    name="name"
    value={form?.name ?? ''}
    aria-invalid={form?.missing}
  />

  {#if form?.missing}
    <p class="error">姓名是必填项</p>
  {/if}

  <button disabled={loading}>
    {loading ? '保存中...' : '保存'}
  </button>
</form>
```

### 4-10. API、表单、样式、测试、性能、无障碍、部署

> **REST API 端点**（GET/POST 处理器、分页）和**类型安全的 API 客户端**：参见 [references/api-patterns.md](references/api-patterns.md)

> **表单处理和验证**（shadcn-svelte 表单、sveltekit-superforms、Zod）和 **Tailwind CSS 配置**：参见 [references/forms-styling.md](references/forms-styling.md)

> **测试**（Vitest、集成测试）、**性能**（代码分割、懒加载）、**无障碍**（Melt UI、ARIA）：参见 [references/testing-performance-a11y.md](references/testing-performance-a11y.md)

> **部署**（Bun 构建、环境变量）、**常见模式**（暗色模式、Toast、认证、SSE）、**故障排除**和**资源**：参见 [references/deployment-patterns.md](references/deployment-patterns.md)
