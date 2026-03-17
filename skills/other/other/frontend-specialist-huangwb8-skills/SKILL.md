---
name: frontend-specialist
description: 前端开发专家。精通 React/Vue/Next.js/Nuxt 等现代前端框架，专注于组件化开发、状态管理、响应式设计、性能优化和用户体验。用于前端应用开发、组件设计和 UI/UX 实现。
metadata:
  short-description: 前端开发与组件设计
  keywords:
    - frontend-specialist
    - 前端开发
    - React
    - Vue
    - Next.js
    - Nuxt.js
    - 组件化
    - 状态管理
    - 响应式设计
    - 性能优化
  category: 前端开发
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# Frontend Specialist - 前端开发专家

## 核心理念

**现代前端开发** 的最佳实践：

```
┌─────────────────────────────────────────────────────────┐
│  组件化 → 状态管理 → 性能优化 → 用户体验               │
└─────────────────────────────────────────────────────────┘
```

**核心原则**：
- ✅ **组件化设计**
- ✅ **声明式编程**
- ✅ **性能优先**
- ✅ **渐进增强**

---

## 何时使用本技能

在以下场景时激活：

- 开发前端应用或组件
- 提到 React、Vue、Next.js、Nuxt.js
- 需要 UI/UX 实现
- 前端性能优化
- 状态管理问题
- 响应式布局

---

## 框架选择指南

### React 生态

**适用场景**：
- 需要灵活性和大型生态系统
- 复杂的单页应用（SPA）
- 需要服务端渲染（SSR）

**推荐组合**：
| 需求 | 推荐技术 |
|------|----------|
| 框架 | Next.js 14+ (App Router) |
| 状态管理 | Zustand / Jotai / React Context |
| 样式 | Tailwind CSS / CSS Modules |
| 表单 | React Hook Form + Zod |
| 数据获取 | TanStack Query |
| 测试 | Vitest + React Testing Library |

### Vue 生态

**适用场景**：
- 快速开发和渐进增强
- 中小型应用
- 团队熟悉 Vue 生态

**推荐组合**：
| 需求 | 推荐技术 |
|------|----------|
| 框架 | Nuxt 3 |
| 状态管理 | Pinia |
| 样式 | Tailwind CSS / Scoped CSS |
| 表单 | VeeValidate |
| 数据获取 | useFetch / $fetch |
| 测试 | Vitest + Vue Test Utils |

---

## 组件化设计

### 组件设计原则

#### 1. 单一职责

```typescript
// ❌ 不好的做法：组件职责过多
function UserProfile() {
  // 获取数据
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch(`/api/users/${id}`).then(r => r.json()).then(setUser);
  }, []);

  // 格式化日期
  const formatDate = (date) => { /* ... */ };

  // UI 渲染
  return <div>...</div>;
}

// ✅ 好的做法：职责分离
// 数据层
function useUser(id: string) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch(`/api/users/${id}`).then(r => r.json()).then(setUser);
  }, [id]);
  return user;
}

// 工具函数
function formatDate(date: Date): string { /* ... */ }

// 组件：只负责渲染
function UserProfile({ userId }: { userId: string }) {
  const user = useUser(userId);
  if (!user) return <Loading />;
  return <ProfileCard user={user} />;
}
```

#### 2. 组合优于继承

```typescript
// ❌ 不好的做法：通过 props 控制多种模式
function Modal({ type, content }) {
  if (type === 'alert') return <AlertModal content={content} />;
  if (type === 'confirm') return <ConfirmModal content={content} />;
  if (type === 'prompt') return <PromptModal content={content} />;
}

// ✅ 好的做法：组合模式
function Modal({ children, footer }: ModalProps) {
  return (
    <Overlay>
      <Container>
        {children}
        {footer && <Footer>{footer}</Footer>}
      </Container>
    </Overlay>
  );
}

// 使用
<Modal footer={<Buttons><OK /><Cancel /></Buttons>}>
  <Alert>Are you sure?</Alert>
</Modal>
```

#### 3. Props 接口设计

```typescript
// ✅ 好的 Props 设计
interface ButtonProps {
  // 必需的
  children: React.ReactNode;

  // 可选的，有合理默认值
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';

  // 事件处理
  onClick?: (e: React.MouseEvent) => void;

  // HTML 属性
  disabled?: boolean;
  type?: 'button' | 'submit';
}

function Button({ variant = 'primary', size = 'md', ...props }: ButtonProps) {
  return <button className={`btn btn-${variant} btn-${size}`} {...props} />;
}
```

---

## 状态管理

### 状态分类

```typescript
// 1. Local State - 组件内部状态
const [isOpen, setIsOpen] = useState(false);

// 2. URL State - URL 中的状态
const searchParams = useSearchParams();
const page = searchParams.get('page') || '1';

// 3. Server State - 服务器数据
const { data, isLoading } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId)
});

// 4. Global State - 全局共享状态
const { user, login, logout } = useAuthStore();
```

### 状态管理工具选择

| 工具 | 适用场景 | 示例 |
|------|----------|------|
| **React Context** | 简单的全局状态 | 主题、语言、认证 |
| **Zustand** | 中等复杂度状态 | 购物车、表单状态 |
| **Jotai** | 原子化状态 | 细粒度更新 |
| **TanStack Query** | 服务器状态 | API 数据缓存 |

```typescript
// Zustand 示例
import create from 'zustand';

interface AuthStore {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  login: async (credentials) => {
    const user = await api.login(credentials);
    set({ user });
  },
  logout: () => set({ user: null }),
}));
```

---

## 性能优化

### 1. Code Splitting

```typescript
// ❌ 不好的做法：一次性加载所有代码
import { HeavyComponent } from './HeavyComponent';

// ✅ 好的做法：动态导入
import { lazy } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### 2. Memoization

```typescript
// ✅ 合理使用 memo
export const ExpensiveComponent = memo(function ExpensiveComponent({
  data,
}: {
  data: ComplexData;
}) {
  return <div>{/* 复杂渲染 */}</div>;
});

// ✅ 缓存计算结果
import { useMemo } from 'react';

function List({ items }: { items: Item[] }) {
  const sorted = useMemo(
    () => items.sort((a, b) => a.id - b.id),
    [items]
  );
  return <ul>{sorted.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

### 3. 虚拟滚动

```typescript
// ✅ 大列表使用虚拟滚动
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {items[virtualItem.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 响应式设计

### Tailwind CSS 响应式断点

```typescript
// ✅ 移动优先设计
function Card() {
  return (
    <div className="
      p-4           /* 移动端默认 */
      md:p-6        /* md (768px+) */
      lg:p-8        /* lg (1024px+) */
    ">
      <h1 className="
        text-xl     /* 移动端 */
        md:text-2xl /* md (768px+) */
        lg:text-3xl /* lg (1024px+) */
      ">
        响应式标题
      </h1>
    </div>
  );
}
```

### 容器查询

```css
/* ✅ 使用容器查询 */
@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

---

## 表单处理

### React Hook Form + Zod

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema 定义
const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password too short'),
});

type LoginForm = z.infer<typeof loginSchema>;

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginForm) => {
    await api.login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```

---

## 测试

### 组件测试

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter', () => {
  it('should increment count when button is clicked', async () => {
    render(<Counter />);

    expect(screen.getByText('Count: 0')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: /increment/i }));

    await waitFor(() => {
      expect(screen.getByText('Count: 1')).toBeInTheDocument();
    });
  });
});
```

---

## 最佳实践清单

- [ ] 组件职责单一
- [ ] Props 接口清晰
- [ ] 使用 TypeScript 类型
- [ ] 合理拆分组件
- [ ] 状态分类管理
- [ ] 性能优化（懒加载、缓存）
- [ ] 响应式设计
- [ ] 无障碍访问（ARIA）
- [ ] 测试覆盖充分
- [ ] 代码格式统一（ESLint/Prettier）

---

## 相关参考

- [React Best Practices](https://react.dev/learn)
- [Next.js Documentation](https://nextjs.org/docs)
- [Vue 3 Guide](https://vuejs.org/guide/)
