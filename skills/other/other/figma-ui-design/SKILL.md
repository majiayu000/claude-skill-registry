---
name: figma-ui-design
description: 自动化 Figma UI 设计。当用户需要创建设计稿、生成组件、导出资源或自动化设计流程时使用此技能。
allowed-tools: Bash, Read, Write, Edit, WebFetch
---

# Figma UI 设计自动化

## 功能说明
此技能专门用于自动化 Figma 设计工作流，包括：
- 设计系统和组件库创建
- 自动化设计稿生成
- 设计资源导出
- 设计规范文档生成
- Figma API 集成
- 设计到代码的转换

## 使用场景
- "创建一个登录页面的 Figma 设计"
- "生成设计系统组件库"
- "从 Figma 导出所有图标"
- "将 Figma 设计转换为 React 组件"
- "自动化设计审查流程"
- "生成设计规范文档"

## 核心功能模块

### 1. 设计系统
- **颜色系统**：定义品牌色、语义色、中性色
- **字体系统**：字体家族、字号、行高、字重
- **间距系统**：统一的间距规范（4px、8px、16px 等）
- **组件库**：按钮、表单、卡片等可复用组件
- **图标库**：统一的图标集合

### 2. 页面设计
- **布局设计**：响应式布局、栅格系统
- **交互设计**：原型和交互流程
- **动效设计**：过渡动画和微交互
- **适配设计**：多端适配（Web、移动端）

### 3. 资源导出
- **图片导出**：PNG、JPG、SVG 格式
- **图标导出**：SVG 图标和图标字体
- **切图导出**：@1x、@2x、@3x 倍图
- **样式导出**：CSS、SCSS 变量

### 4. 设计到代码
- **组件生成**：React、Vue、Angular 组件
- **样式生成**：CSS、Tailwind、Styled Components
- **代码规范**：遵循团队代码规范
- **类型定义**：TypeScript 类型

## 设计工作流程

### 标准设计流程
1. **需求分析**：理解产品需求和用户场景
2. **信息架构**：规划页面结构和导航
3. **线框图**：绘制低保真原型
4. **视觉设计**：应用设计系统创建高保真稿
5. **交互原型**：添加交互和动效
6. **设计评审**：团队审查和反馈
7. **开发交付**：导出资源和标注

### 组件库建设流程
1. **组件规划**：确定需要的组件类型
2. **设计规范**：定义组件的设计规则
3. **组件设计**：创建基础组件
4. **变体管理**：定义组件的不同状态
5. **文档编写**：使用说明和示例
6. **发布更新**：版本管理和更新日志

## 最佳实践

### 设计规范
- **命名规范**：使用清晰的图层命名
- **组织结构**：合理的页面和图层组织
- **组件化**：最大化组件复用
- **自动布局**：使用 Auto Layout 提高效率
- **约束设置**：正确设置响应式约束

### 协作规范
- **文件组织**：项目、页面、组件分类清晰
- **版本管理**：使用 Figma 版本历史
- **评论反馈**：使用评论功能沟通
- **权限管理**：合理设置查看和编辑权限
- **团队库**：共享设计系统和组件

### 性能优化
- **图层优化**：减少不必要的图层
- **效果使用**：谨慎使用阴影和模糊
- **图片优化**：压缩大图片
- **组件实例**：使用组件实例而非复制

## 设计系统示例

### 颜色系统
```javascript
const colors = {
  // 品牌色
  primary: {
    50: '#E3F2FD',
    100: '#BBDEFB',
    500: '#2196F3',  // 主色
    700: '#1976D2',
    900: '#0D47A1'
  },
  // 功能色
  success: '#4CAF50',
  warning: '#FF9800',
  error: '#F44336',
  info: '#2196F3',
  // 中性色
  gray: {
    50: '#FAFAFA',
    100: '#F5F5F5',
    500: '#9E9E9E',
    900: '#212121'
  }
};
```

### 字体系统
```javascript
const typography = {
  fontFamily: {
    sans: 'Inter, system-ui, sans-serif',
    mono: 'Fira Code, monospace'
  },
  fontSize: {
    xs: '12px',
    sm: '14px',
    base: '16px',
    lg: '18px',
    xl: '20px',
    '2xl': '24px',
    '3xl': '30px',
    '4xl': '36px'
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700
  },
  lineHeight: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75
  }
};
```

### 间距系统
```javascript
const spacing = {
  0: '0',
  1: '4px',
  2: '8px',
  3: '12px',
  4: '16px',
  5: '20px',
  6: '24px',
  8: '32px',
  10: '40px',
  12: '48px',
  16: '64px',
  20: '80px'
};
```

## Figma API 使用

### 获取文件内容
```javascript
const response = await fetch(
  'https://api.figma.com/v1/files/FILE_KEY',
  {
    headers: {
      'X-Figma-Token': 'YOUR_TOKEN'
    }
  }
);
const data = await response.json();
```

### 导出图片
```javascript
const response = await fetch(
  'https://api.figma.com/v1/images/FILE_KEY?ids=NODE_ID&format=png&scale=2',
  {
    headers: {
      'X-Figma-Token': 'YOUR_TOKEN'
    }
  }
);
const { images } = await response.json();
```

### 获取样式
```javascript
const response = await fetch(
  'https://api.figma.com/v1/files/FILE_KEY/styles',
  {
    headers: {
      'X-Figma-Token': 'YOUR_TOKEN'
    }
  }
);
const { meta } = await response.json();
```

## 设计到代码转换

### React 组件生成
```jsx
// 从 Figma 设计生成的按钮组件
import React from 'react';
import styled from 'styled-components';

const StyledButton = styled.button`
  padding: 12px 24px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #1976D2;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    background: #BDBDBD;
    cursor: not-allowed;
  }
`;

export const Button = ({ children, ...props }) => {
  return <StyledButton {...props}>{children}</StyledButton>;
};
```

### CSS 变量生成
```css
:root {
  /* Colors */
  --color-primary: #2196F3;
  --color-primary-dark: #1976D2;
  --color-success: #4CAF50;
  --color-error: #F44336;

  /* Typography */
  --font-sans: Inter, system-ui, sans-serif;
  --font-size-base: 16px;
  --font-weight-normal: 400;
  --font-weight-bold: 700;

  /* Spacing */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-4: 16px;
  --spacing-8: 32px;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

## 常用插件推荐

### 设计效率
- **Autoflow**：自动生成流程图连线
- **Content Reel**：快速填充文本和图片
- **Unsplash**：免费高质量图片
- **Iconify**：海量图标库

### 开发协作
- **Figma to Code**：设计转代码
- **Anima**：导出 React/Vue 代码
- **Zeplin**：设计标注和切图
- **Avocode**：设计交付平台

### 设计系统
- **Design System Manager**：管理设计系统
- **Stark**：无障碍设计检查
- **Contrast**：对比度检查

## 集成场景

### 1. 自动化设计审查
- 检查设计规范遵循情况
- 验证颜色和字体使用
- 检查组件一致性
- 生成审查报告

### 2. 设计资源同步
- 自动导出设计资源
- 同步到代码仓库
- 更新组件库
- 通知开发团队

### 3. 设计文档生成
- 提取设计规范
- 生成组件文档
- 创建使用指南
- 发布到文档站点

### 4. 原型测试
- 生成可交互原型
- 收集用户反馈
- 分析交互数据
- 迭代设计方案

## 注意事项
- 保持设计文件整洁有序
- 定期清理未使用的组件和样式
- 使用版本控制管理重要变更
- 与开发团队保持密切沟通
- 遵循无障碍设计原则
- 考虑性能和加载速度
