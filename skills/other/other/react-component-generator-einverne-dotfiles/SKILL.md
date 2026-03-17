---
name: react-component-generator
description: 生成符合项目规范的 React 组件。当用户要求创建组件、新建 React 组件或生成组件文件时使用
---

# React 组件生成器

## 组件规范

项目使用以下约定：
- TypeScript + React
- 函数式组件 + Hooks
- CSS Modules 样式
- 完整的 JSDoc 注释
- 配套的测试文件

## 生成流程

1. 确认组件信息
   - 组件名称（PascalCase）
   - 组件类型（基础组件、容器组件、页面组件）
   - 所需 props

2. 创建文件结构
   ```
   src/components/{ComponentName}/
   ├── index.tsx
   ├── {ComponentName}.module.css
   └── {ComponentName}.test.tsx
   ```

3. 生成组件文件

index.tsx 模板：
```typescript
import React from 'react';
import styles from './{ComponentName}.module.css';

interface {ComponentName}Props {
  // 定义 props 类型
}

/**
 * {组件描述}
 * @param props - 组件属性
 */
export const {ComponentName}: React.FC<{ComponentName}Props> = (props) => {
  return (
    <div className={styles.container}>
      {/* 组件内容 */}
    </div>
  );
};
```

4. 生成样式文件

{ComponentName}.module.css 模板：
```css
.container {
  /* 组件样式 */
}
```

5. 生成测试文件

{ComponentName}.test.tsx 模板：
```typescript
import { render, screen } from '@testing-library/react';
import { {ComponentName} } from './index';

describe('{ComponentName}', () => {
  it('renders correctly', () => {
    render(<{ComponentName} />);
    // 添加断言
  });
});
```

## 质量检查

生成后自动运行：
1. TypeScript 类型检查：`npm run type-check`
2. ESLint 检查：`npm run lint`
3. 测试：`npm test -- {ComponentName}`

如有错误，显示错误信息并提供修复建议。
