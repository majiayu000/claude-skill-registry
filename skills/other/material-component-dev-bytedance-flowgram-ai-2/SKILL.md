---
skill_name: material-component-dev
description: FlowGram 物料组件开发指南 - 用于在 form-materials 包中创建新的物料组件
version: 1.0.0
tags: [flowgram, material, component, development]
---

# FlowGram Material Component Development

## 概述

本 SKILL 用于指导在 FlowGram 项目的 `@flowgram.ai/form-materials` 包中创建新的物料组件。

## 核心原则

### 1. 组件位置
- ✅ **在现有包中创建**：直接在 `packages/materials/form-materials/src/components/` 下创建组件目录
- ❌ **不要单独拆包**：不创建新的 npm 包，保持简洁

### 2. 代码质量
- ✅ **使用 named export**：所有导出使用 named export 提高 tree shake 性能
- ❌ **不写单元测试**：通过 Storybook 进行手动测试
- ✅ **通过类型检查**：必须通过 `yarn ts-check`
- ✅ **符合代码规范**：遵循项目 ESLint 规则

### 3. 物料设计
- ✅ **保持精简**：只保留必要的 props，不添加非核心功能配置项
- ✅ **功能单一**：一个物料只做一件事
- ✅ **使用内部依赖**：优先使用 FlowGram 内部的组件和类型

### 4. 技术栈
- **UI 组件库**：`@douyinfe/semi-ui`
- **代码编辑器**：`JsonCodeEditor`, `CodeEditor` 等来自 `../code-editor`
- **类型定义**：`IJsonSchema` 来自 `@flowgram.ai/json-schema`（不使用外部的 `json-schema` 包）
- **React**：必须显式 `import React` 避免 UMD 全局引用错误

## 开发流程

### Step 1: 规划组件结构

确定组件的：
- **功能**：组件要解决什么问题
- **Props 接口**：只保留核心必需的 props
- **命名**：使用 PascalCase，清晰描述功能

### Step 2: 创建目录结构

```bash
mkdir -p packages/materials/form-materials/src/components/{组件名}/utils
```

典型结构：
```
packages/materials/form-materials/src/components/{组件名}/
├── index.tsx                 # 导出文件 (named export)
├── {组件名}.tsx              # 主组件
├── {辅助组件}.tsx            # 可选的辅助组件
└── utils/                    # 可选的工具函数
    └── *.ts
```

### Step 3: 实现组件

#### 3.1 工具函数（如需要）

```typescript
// utils/helper.ts
/**
 * Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
 * SPDX-License-Identifier: MIT
 */

export function helperFunction(input: string): Output {
  // 实现逻辑
}
```

#### 3.2 辅助组件（如需要）

```typescript
// modal.tsx
/**
 * Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
 * SPDX-License-Identifier: MIT
 */

import React, { useState } from 'react';
import { Modal, Typography } from '@douyinfe/semi-ui';

interface ModalProps {
  visible: boolean;
  onClose: () => void;
  onConfirm: (data: SomeType) => void;
}

export function MyModal({ visible, onClose, onConfirm }: ModalProps) {
  // 实现
}
```

#### 3.3 主组件

```typescript
// my-component.tsx
/**
 * Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
 * SPDX-License-Identifier: MIT
 */

import React, { useState } from 'react';
import { Button } from '@douyinfe/semi-ui';
import type { IJsonSchema } from '@flowgram.ai/json-schema';

export interface MyComponentProps {
  /** 核心功能的回调 */
  onSomething?: (data: SomeType) => void;
}

// 使用 named export，不使用 default export
export function MyComponent({ onSomething }: MyComponentProps) {
  const [visible, setVisible] = useState(false);

  return (
    <>
      <Button onClick={() => setVisible(true)}>
        操作文本
      </Button>
      {/* 其他组件 */}
    </>
  );
}
```

**关键点**：
- ✅ 显式 `import React`
- ✅ 使用 Semi UI 组件
- ✅ 使用 function 声明而非 React.FC
- ✅ Props 精简，只保留核心功能
- ✅ Named export

#### 3.4 导出文件

```typescript
// index.tsx
/**
 * Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
 * SPDX-License-Identifier: MIT
 */

export { MyComponent } from './my-component';
export type { MyComponentProps } from './my-component';
```

### Step 4: 在 form-materials 主入口导出

编辑 `packages/materials/form-materials/src/components/index.ts`：

```typescript
export {
  // ... 其他组件按字母序
  MyComponent,
  // ... 继续其他组件
  type MyComponentProps,
  // ... 继续其他类型
} from './components';
```

然后编辑 `packages/materials/form-materials/src/index.ts`，确保新组件在主导出列表中：

```typescript
export {
  // ... 其他组件按字母序
  MyComponent,
  // ...
  type MyComponentProps,
  // ...
} from './components';
```

### Step 5: 创建 Storybook Story

在 `apps/demo-materials/src/stories/components/` 创建 Story：

```typescript
// my-component.stories.tsx
/**
 * Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
 * SPDX-License-Identifier: MIT
 */

import React, { useState } from 'react';
import type { Meta, StoryObj } from 'storybook-react-rsbuild';
import { MyComponent } from '@flowgram.ai/form-materials';
import type { SomeType } from '@flowgram.ai/json-schema';

const MyComponentDemo: React.FC = () => {
  const [result, setResult] = useState<SomeType | null>(null);

  return (
    <div style={{ padding: '20px' }}>
      <h2>My Component Demo</h2>
      <MyComponent
        onSomething={(data) => {
          console.log('Generated data:', data);
          setResult(data);
        }}
      />

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>结果:</h3>
          <pre style={{
            background: '#f5f5f5',
            padding: '16px',
            borderRadius: '4px',
            overflow: 'auto'
          }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

const meta: Meta<typeof MyComponentDemo> = {
  title: 'Form Components/MyComponent',
  component: MyComponentDemo,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: '组件功能描述',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
```

### Step 6: 运行类型检查

```bash
cd packages/materials/form-materials
yarn ts-check
```

确保通过所有类型检查。

### Step 7: 启动开发环境测试

开启两个 Terminal：

**Terminal 1 - 监听包编译：**
```bash
rush build:watch
```

**Terminal 2 - 启动 Storybook：**
```bash
cd apps/demo-materials
yarn dev
```

访问 http://localhost:6006/，找到你的组件进行测试。

## 常见问题

### Q1: React 引用错误

**错误信息**：
```
error TS2686: 'React' refers to a UMD global, but the current file is a module.
```

**解决方案**：
在文件顶部添加：
```typescript
import React from 'react';
```

### Q2: 组件未导出

**错误信息**：
```
Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) but got: undefined.
```

**解决方案**：
检查以下文件的导出：
1. `components/{组件名}/index.tsx`
2. `components/index.ts`
3. `src/index.ts`

### Q3: 类型找不到

**错误信息**：
```
Cannot find module '@flowgram.ai/json-schema' or its corresponding type declarations.
```

**解决方案**：
- 使用 `type IJsonSchema` 而非 `type JSONSchema7`
- 从 `@flowgram.ai/json-schema` 导入而非 `json-schema`

### Q4: CodeEditor 没有 height 属性

**错误信息**：
```
Property 'height' does not exist on type 'CodeEditorPropsType'.
```

**解决方案**：
使用外层 div 设置高度：
```tsx
<div style={{ minHeight: 300 }}>
  <JsonCodeEditor value={value} onChange={onChange} />
</div>
```

## 验收标准

- [ ] 组件在 `packages/materials/form-materials/src/components/` 下创建
- [ ] 使用 named export
- [ ] 通过 `yarn ts-check` 类型检查
- [ ] Props 精简，只保留核心功能
- [ ] 在 Storybook 中可以正常显示和使用
- [ ] 功能正常，无明显 bug
- [ ] 代码符合 FlowGram 代码规范

## 最佳实践

### 1. 组件设计

- **单一职责**：一个组件只做一件事
- **Props 精简**：避免过度配置
- **命名清晰**：组件名和 Props 名要清晰易懂

### 2. 代码风格

- **使用 TypeScript**：充分利用类型系统
- **显式导入**：明确导入所需的依赖
- **注释适度**：关键逻辑添加注释

### 3. UI 一致性

- **使用 Semi UI**：保持 UI 风格一致
- **响应式设计**：考虑不同屏幕尺寸
- **错误处理**：友好的错误提示

### 4. 性能优化

- **Named export**：支持 tree shaking
- **按需加载**：避免不必要的依赖
- **合理使用 memo**：必要时使用 React.memo

## 示例参考

完整示例请参考：
- `packages/materials/form-materials/src/components/json-schema-creator/`
- `apps/demo-materials/src/stories/components/json-schema-creator.stories.tsx`

