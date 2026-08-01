---
name: css-design-tokens
description: 'CSS design tokens and color system for vehicle insurance platform. Use
  when defining colors, spacing, typography, or design variables. Keywords: eye-care
  colors #5B8DEF/#8B95A5/#C5CAD3, CSS variables,'
---

---
name: css-design-tokens
description: CSS design tokens and color system for vehicle insurance platform. Use when defining colors, spacing, typography, or design variables. Keywords: eye-care colors #5B8DEF/#8B95A5/#C5CAD3, CSS variables, spacing system, color palette, typography scale, design tokens, variables.css, theme colors.
allowed-tools: Read, Edit, Grep, Glob
---

# CSS Design Tokens - 设计规范变量

车险签单数据分析平台的CSS设计规范和变量系统。

---

## 🎨 护眼配色体系

### 图表主色 (Chart Primary Colors)

**核心色板** - 护眼蓝灰系:

```css
--chart-primary-blue: #5B8DEF;    /* D (最新周期) - 主蓝色 */
--chart-secondary-gray: #8B95A5;  /* D-7 (上周) - 次灰色 */
--chart-light-gray: #C5CAD3;      /* D-14 (前周) - 浅灰色 */
```

**使用场景**:
- **周对比图表**: 3条折线分别使用这3种颜色
  - `#5B8DEF` (主蓝): 最新7天数据(D)
  - `#8B95A5` (次灰): 上一个7天(D-7)
  - `#C5CAD3` (浅灰): 前一个7天(D-14)

**ECharts使用示例**:
```javascript
const chartOption = {
  color: ['#5B8DEF', '#8B95A5', '#C5CAD3'],  // 护眼配色
  // ... other options
}
```

---

### 状态色 (Status Colors)

```css
--status-success: #52C41A;   /* 上升 ↑ - 成功绿 */
--status-warning: #F5222D;   /* 下降 ↓ - 警示红 */
--status-neutral: #8B95A5;   /* 持平 — - 中性灰 */
```

**使用场景**:
- KPI趋势指示 (↑ ↓ —)
- Toast通知 (成功/错误/信息)
- 数据变化高亮

---

### 主色 (Primary Palette)

```css
--primary-50: #f3e8ff;
--primary-100: #e9d5ff;
--primary-500: #a855f7;   /* 主按钮、链接 */
--primary-600: #9333ea;
--primary-700: #7e22ce;
```

**使用场景**:
- 主按钮背景: `--primary-500`
- 主按钮悬停: `--primary-600`
- 链接文字: `--primary-500`

---

### 中性色 (Neutral Colors)

```css
--gray-50: #f9fafb;    /* 浅背景 */
--gray-100: #f3f4f6;   /* 卡片背景 */
--gray-300: #d1d5db;   /* 边框 */
--gray-500: #6b7280;   /* 次要文字 */
--gray-700: #374151;   /* 辅助文字 */
--gray-900: #111827;   /* 主要文字 */
```

**文字颜色映射**:
```css
--text-primary: var(--gray-900);
--text-secondary: var(--gray-500);
--text-muted: rgba(17, 24, 39, 0.7);
```

---

### 表面与阴影 (Surface & Shadows)

```css
--surface-default: #ffffff;
--surface-elevated: #ffffff;
--surface-primary-tint: rgba(168, 85, 247, 0.08);

--shadow-soft: 0 10px 30px rgba(15, 23, 42, 0.08);
--shadow-md: 0 10px 30px rgba(15, 23, 42, 0.08);
```

---

## 📏 CSS 变量规范

### 间距系统 (Spacing)

**4px基准网格**:

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
```

**使用建议**:
- 组件内部间距: `--space-3` (12px) 或 `--space-4` (16px)
- 组件外部间距: `--space-6` (24px) 或 `--space-8` (32px)

---

### 圆角 (Border Radius)

```css
--radius-sm: 0.5rem;   /* 8px - 小按钮、标签 */
--radius-md: 0.75rem;  /* 12px - 卡片、输入框 */
--radius-lg: 1rem;     /* 16px - 对话框、大卡片 */
```

---

### 字体系统 (Typography)

```css
--text-xs: 0.75rem;   /* 12px - 辅助文字 */
--text-sm: 0.875rem;  /* 14px - 次要文字 */
--text-base: 1rem;    /* 16px - 正文(默认) */
--text-lg: 1.125rem;  /* 18px - 小标题 */
--text-xl: 1.25rem;   /* 20px - 标题 */
--text-2xl: 1.5rem;   /* 24px - 大标题 */
--text-3xl: 1.875rem; /* 30px - 数值展示 */
```

**字体族**:
```css
--font-family-base: 'Inter', 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

---

### 边框 (Borders)

```css
--border-accent-width: 0.25rem;  /* 4px - 强调边框(左侧装饰线) */
```

---

## 🌗 主题系统

### 护眼模式 (当前默认)

**设计理念**:
- 基于眼科医学研究,减少蓝光刺激
- 温暖的米白色背景 `#fefcf3`
- 降低对比度,避免强烈黑白对比

**颜色配置**:
```css
:root {
  --bg-primary: #fefcf3;      /* 温暖米白 */
  --bg-secondary: #f8f4e9;    /* 浅米色 */
  --bg-elevated: #ffffff;     /* 纯白 */
  --text-primary: #3a3a3a;    /* 深灰(降低对比度) */
  --text-secondary: #5a5a5a;
  --text-muted: #8a8a8a;
}
```

---

### 暗黑模式 (未来扩展)

**颜色配置**:
```css
[data-theme-mode="dark"] {
  --bg-primary: #0d0d0d;      /* 纯黑 */
  --bg-secondary: #1a1a1a;    /* 近黑 */
  --bg-elevated: #262626;     /* 深灰 */
  --text-primary: #f0f0f0;    /* 亮白 */
  --text-secondary: #c0c0c0;
  --text-muted: #909090;
}
```

---

## ✅ 使用最佳实践

### 规范 1: 使用CSS变量

```css
/* ✅ 正确 */
.text {
  color: var(--text-primary);
  font-size: var(--text-base);
  padding: var(--space-4);
}

/* ❌ 错误: 硬编码 */
.text {
  color: #111827;
  font-size: 16px;
  padding: 16px;
}
```

---

### 规范 2: 语义化颜色

```css
/* ✅ 正确: 使用语义化变量 */
.alert--success {
  color: var(--status-success);
}

/* ❌ 错误: 直接使用颜色值 */
.alert--success {
  color: #52C41A;
}
```

---

### 规范 3: 间距系统

```css
/* ✅ 正确: 使用间距变量 */
.card {
  padding: var(--space-6);
  margin-bottom: var(--space-4);
}

/* ❌ 错误: 随意间距 */
.card {
  padding: 23px;
  margin-bottom: 17px;
}
```

---

## 🔗 相关资源

### 关键文件位置
- [frontend/src/assets/styles/variables.css](../../frontend/src/assets/styles/variables.css) - CSS变量定义

### 相关 Skills
- [component-styling](../component-styling/SKILL.md) - 组件样式模板
- [vue-component-dev](../vue-component-dev/SKILL.md) - Vue组件开发

### 外部参考
- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

---

## ✅ 总结

### 核心要点

1. **护眼配色**: 蓝灰系 `#5B8DEF` / `#8B95A5` / `#C5CAD3`
2. **间距系统**: 4px基准网格 (space-1 到 space-8)
3. **字体系统**: 7级字体大小 (xs到3xl)
4. **圆角系统**: 3级圆角 (sm/md/lg)
5. **主题模式**: 护眼模式(当前) + 暗黑模式(未来)

### 适用场景

✅ **适用**:
- 定义新的设计变量
- 修改配色方案
- 调整间距/字体规范
- 实现主题切换

❌ **不适用**(请使用其他Skills):
- 组件样式实现 → `component-styling`
- Vue组件开发 → `vue-component-dev`

---

**文档维护者**: Claude Code AI Assistant
**创建日期**: 2025-11-09
**下次审查**: 2025-11-23
