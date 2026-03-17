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



### Windows下Vite进程管理（重要！）

**问题**：Windows环境下Vite开发服务器退出时，chokidar文件监听器可能不会正确清理，导致僵尸进程占用端口。

**解决方案**：

1. **优化vite.config.js配置**
```javascript
export default defineConfig({
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: false,
    watch: { usePolling: false, interval: 1000 }
  },
  optimizeDeps: { exclude: ['@vueup/vue-quill'] }
})
```

2. **创建清理脚本 stop-dev.bat**
```batch
@echo off
echo Killing Vite processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 2^>nul ^| findstr LISTENING') do (
  taskkill /F /PID %%a 2>nul
)
echo Done!
```

3. **创建智能启动脚本 dev.bat**
```batch
@echo off
echo Starting Vite dev server...
cmd /c npm run dev
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 2^>nul ^| findstr LISTENING') do (
  taskkill /F /PID %%a 2>nul
)
echo Vite stopped
```

**使用方法**：使用`dev.bat`启动，`stop-dev.bat`清理，避免后台运行。

## 注意事项
- 遵循团队代码规范
- 编写清晰的注释和文档
- 考虑浏览器兼容性
- 注意安全问题（XSS、CSRF）
- 优化首屏加载时间
- 实现错误边界和降级方案
- 使用 TypeScript 提高代码质量

---

## ⚠️ 文档同步规范（非常重要！）

前端开发完成后，**必须同步更新相关文档**，保持代码与文档一致！

### 必须维护的文档

#### 1. 进度文档 (`docs/frontend/progress.md`)
记录开发进度、已完成功能、待办事项。

**更新时机**：
- 完成新页面/组件时
- 修改技术栈时
- 完成里程碑时

**文档格式参考**：
```markdown
# 前端开发进度

> 最后更新：YYYY-MM-DD
> 状态：开发中 (X%完成)

## 已完成功能
### 核心架构
| 模块 | 状态 | 说明 |
|------|------|------|
| 项目初始化 | ✅ | Vite + Vue3 + Pinia |

## 待完成功能
### 优先级 P1
- [ ] 深色模式

## 代码统计
| 类型 | 数量 |
|------|------|
| 页面组件 | 8 |
```

#### 2. API对接文档 (`docs/frontend/api-reference.md`)
记录后端API接口、请求格式、响应格式。

**更新时机**：
- 后端新增/修改API时
- 前端调用新API时
- API字段变化时

**必须包含**：
- 服务地址配置
- 通用响应格式
- 每个API的详细说明（方法、路径、参数、响应示例）
- 前端调用示例代码

#### 3. README.md (`frontend/README.md`)
项目入口文档，快速上手指南。

**必须包含**：
- 项目简介
- 技术栈版本
- 快速启动命令
- 目录结构
- 开发注意事项
- 与后端的对接说明

### 文档同步检查清单

前端开发完成后，问自己：

- [ ] 我更新了 `docs/frontend/progress.md` 吗？
- [ ] 新API调用记录在 `docs/frontend/api-reference.md` 了吗？
- [ ] README.md 里的技术栈版本是最新的吗？
- [ ] 如果有环境变量变化，更新文档了吗？
- [ ] 代码结构变化后，更新目录结构了吗？

### 文档与代码同步原则

1. **先更新文档再提交代码** - 确保文档反映最新状态
2. **API变化立即同步** - 后端API变了，前端文档也要更新
3. **配置变化记录在案** - 环境变量、端口等配置变化要写进文档
4. **定期Review文档** - 每周检查一次文档是否过时
5. **删除死链接** - 不存在的功能从文档中移除

### 文档命名规范

| 文档类型 | 路径 | 命名格式 |
|----------|------|----------|
| 前端进度 | `docs/frontend/progress.md` | 固定文件名 |
| API参考 | `docs/frontend/api-reference.md` | 固定文件名 |
| 后端进度 | `docs/backend/progress.md` | 固定文件名 |
| 后端API参考 | `docs/backend/api-reference.md` | 固定文件名 |
| 技术设计 | `docs/plans/YYYY-MM-DD-*.md` | 按日期命名 |

---