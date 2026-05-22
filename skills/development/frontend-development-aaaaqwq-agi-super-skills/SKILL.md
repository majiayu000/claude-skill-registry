---
name: frontend-development
description: 前端页面开发。当用户需要开发 Web 应用、创建 UI 组件、实现交互功能或优化前端性能时使用此技能。
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 前端页面开发

## 功能说明
此技能专门用于前端 Web 开发，包括：
- 现代前端框架开发（React、Vue、Angular）
- 响应式页面布局
- 交互功能实现
- 状态管理
- 性能优化
- 前端工程化

## 使用场景
- "创建一个 React 登录页面"
- "实现一个响应式导航栏"
- "优化页面加载性能"
- "集成第三方 API"
- "实现深色模式切换"
- "创建可复用的 UI 组件库"

## 技术栈

### 核心框架
- **React**：组件化、Hooks、Context
- **Vue**：响应式、组合式 API、Pinia
- **Angular**：TypeScript、依赖注入、RxJS
- **Next.js**：SSR、SSG、API Routes
- **Nuxt.js**：Vue SSR 框架

### UI 框架
- **Tailwind CSS**：实用优先的 CSS 框架
- **Material-UI**：React Material Design
- **Ant Design**：企业级 UI 组件库
- **Element Plus**：Vue 3 组件库
- **Chakra UI**：可访问的组件系统

### 状态管理
- **Redux**：可预测的状态容器
- **Zustand**：轻量级状态管理
- **Pinia**：Vue 状态管理
- **MobX**：响应式状态管理
- **Jotai**：原子化状态管理

### 构建工具
- **Vite**：下一代前端构建工具
- **Webpack**：模块打包器
- **Turbopack**：Rust 驱动的打包器
- **esbuild**：极速 JavaScript 打包器

## 开发工作流程

### 项目初始化
1. **创建项目**：使用脚手架工具
2. **配置环境**：ESLint、Prettier、TypeScript
3. **目录结构**：组织代码文件
4. **依赖安装**：安装必要的包
5. **Git 初始化**：版本控制设置

### 开发流程
1. **需求分析**：理解功能需求
2. **组件设计**：拆分组件结构
3. **样式开发**：实现 UI 设计
4. **功能实现**：编写业务逻辑
5. **测试验证**：单元测试和集成测试
6. **代码审查**：团队 Code Review
7. **部署上线**：构建和发布

## 最佳实践

### 代码组织
```
src/
├── components/       # 可复用组件
│   ├── Button/
│   ├── Input/
│   └── Modal/
├── pages/           # 页面组件
│   ├── Home/
│   ├── Login/
│   └── Dashboard/
├── hooks/           # 自定义 Hooks
├── utils/           # 工具函数
├── services/        # API 服务
├── store/           # 状态管理
├── styles/          # 全局样式
├── types/           # TypeScript 类型
└── constants/       # 常量定义
```

### 组件设计原则
- **单一职责**：一个组件只做一件事
- **可复用性**：设计通用的组件
- **可组合性**：小组件组合成大组件
- **Props 验证**：使用 TypeScript 或 PropTypes
- **默认值**：提供合理的默认属性

### 性能优化
- **代码分割**：动态导入和懒加载
- **虚拟滚动**：处理大列表
- **防抖节流**：优化事件处理
- **Memo 化**：避免不必要的重渲染
- **图片优化**：懒加载、WebP 格式
- **缓存策略**：合理使用缓存

### 可访问性
- **语义化 HTML**：使用正确的标签
- **键盘导航**：支持键盘操作
- **ARIA 属性**：辅助技术支持
- **对比度**：确保文字可读性
- **焦点管理**：清晰的焦点指示

## 代码示例

### React 组件示例
```tsx
import React, { useState } from 'react';
import styled from 'styled-components';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

const StyledButton = styled.button<ButtonProps>`
  padding: ${props => {
    switch (props.size) {
      case 'small': return '8px 16px';
      case 'large': return '16px 32px';
      default: return '12px 24px';
    }
  }};
  background: ${props =>
    props.variant === 'primary' ? '#2196F3' : '#757575'
  };
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover:not(:disabled) {
    opacity: 0.9;
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  children
}) => {
  return (
    <StyledButton
      variant={variant}
      size={size}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </StyledButton>
  );
};
```

### Vue 组件示例
```vue
<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  variant?: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'medium',
  disabled: false
});

const emit = defineEmits<{
  click: [];
}>();

const buttonClasses = computed(() => [
  'btn',
  `btn-${props.variant}`,
  `btn-${props.size}`,
  { 'btn-disabled': props.disabled }
]);

const handleClick = () => {
  if (!props.disabled) {
    emit('click');
  }
};
</script>

<style scoped>
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #2196F3;
  color: white;
}

.btn-secondary {
  background: #757575;
  color: white;
}

.btn-small {
  padding: 8px 16px;
  font-size: 14px;
}

.btn-large {
  padding: 16px 32px;
  font-size: 18px;
}

.btn:hover:not(.btn-disabled) {
  opacity: 0.9;
  transform: translateY(-2px);
}

.btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```

### 自定义 Hook 示例
```typescript
import { useState, useEffect } from 'react';

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useFetch<T>(url: string): FetchState<T> {
  const [state, setState] = useState<FetchState<T>>({
    data: null,
    loading: true,
    error: null
  });

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      try {
        setState(prev => ({ ...prev, loading: true }));
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (!cancelled) {
          setState({ data, loading: false, error: null });
        }
      } catch (error) {
        if (!cancelled) {
          setState({
            data: null,
            loading: false,
            error: error as Error
          });
        }
      }
    };

    fetchData();

    return () => {
      cancelled = true;
    };
  }, [url]);

  return state;
}
```

### 状态管理示例（Zustand）
```typescript
import create from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) =>
        set({ user, token, isAuthenticated: true }),
      logout: () =>
        set({ user: null, token: null, isAuthenticated: false })
    }),
    {
      name: 'auth-storage'
    }
  )
);
```

## 响应式设计

### 断点系统
```css
/* Mobile First */
/* Mobile: 默认样式 */
.container {
  padding: 16px;
}

/* Tablet: >= 768px */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }
}

/* Desktop: >= 1024px */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Large Desktop: >= 1440px */
@media (min-width: 1440px) {
  .container {
    max-width: 1400px;
  }
}
```

### Flexbox 布局
```css
.flex-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .flex-container {
    flex-direction: column;
  }
}
```

### Grid 布局
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  padding: 24px;
}
```

## 测试策略

### 单元测试（Jest + React Testing Library）
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

### E2E 测试（Playwright）
```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('http://localhost:3000/login');

  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('http://localhost:3000/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

## 部署和优化

### 构建优化
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@mui/material']
        }
      }
    },
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true
      }
    }
  }
});
```

### 环境变量
```env
# .env.production
VITE_API_URL=https://api.production.com
VITE_APP_NAME=My App
```

## 注意事项
- 遵循团队代码规范
- 编写清晰的注释和文档
- 考虑浏览器兼容性
- 注意安全问题（XSS、CSRF）
- 优化首屏加载时间
- 实现错误边界和降级方案
- 使用 TypeScript 提高代码质量
