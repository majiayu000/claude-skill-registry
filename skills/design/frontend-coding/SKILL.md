---
name: frontend-coding
description: '前端编码规范与最佳实践。Use when writing React components, pages, or need guidance
  on TypeScript style, Tailwind CSS, or shadcn/ui usage. Triggers on: creating components,
  styling with Tailwind, using shadcn/ui,'
---

---
name: frontend-coding
description: 前端编码规范与最佳实践。Use when writing React components, pages, or need guidance on TypeScript style, Tailwind CSS, or shadcn/ui usage. Triggers on: creating components, styling with Tailwind, using shadcn/ui, TypeScript code style questions, responsive design, dark mode implementation.
---

# Frontend Coding Guide

前端开发编码规范，涵盖 Next.js、TypeScript、Tailwind CSS 和 shadcn/ui。

## Quick Reference

### Exports

```typescript
// ✅ named export
export const Button = () => {};

// ❌ default export（Next.js 约定文件除外）
export default Button;
```

### Parameters

```typescript
// ✅ 对象参数
function createUser({ name, email }: { name: string; email: string }) {}

// ❌ 位置参数
function createUser(name: string, email: string) {}
```

### Type Safety

```typescript
// ✅ 明确类型
const data: Record<string, string> = {};

// ❌ any
const data: any = {};
```

### Tailwind Design Tokens

```tsx
// ✅ 语义化 tokens
className = 'bg-background text-foreground';

// ❌ 硬编码
className = 'bg-[#0B0D10]';
```

### Responsive & Dark Mode

```tsx
// ✅ 移动优先 + 暗色模式
className = 'flex flex-col gap-4 md:flex-row bg-background text-foreground';

// ❌ 固定宽度 + 只有亮色
className = 'flex gap-8 w-[1200px] bg-white';
```

### shadcn/ui

```tsx
// ✅ 从 @/components/ui 导入
import { Button } from '@/components/ui/button';

// ❌ 直接导入 Radix
import * as Dialog from '@radix-ui/react-dialog';
```

### Icons

```tsx
// ✅ lucide-react
import { User, Settings } from 'lucide-react';

// ❌ 其他图标库
import { FaUser } from 'react-icons/fa';
```

## Detailed References

| Reference                        | Content                               |
| -------------------------------- | ------------------------------------- |
| `references/nextjs.md`           | Next.js + React best practices        |
| `references/typescript-style.md` | TypeScript code style                 |
| `references/tailwind-styling.md` | Tailwind CSS conventions              |
| `references/ui-components.md`    | shadcn/ui usage                       |
| `references/examples.md`         | 示例模板规范（`_examples/` 使用指南） |

## Core Principles

1. **Functional programming** - Use functions and hooks, avoid classes (except Service layer)
2. **Type safety** - No `any`, use explicit types
3. **Design tokens** - Use semantic colors, no hardcoding
4. **Responsive** - Mobile-first, support all screen sizes
5. **Dark mode** - All components must support
6. **Component reuse** - Prefer shadcn/ui, no reinventing wheels
