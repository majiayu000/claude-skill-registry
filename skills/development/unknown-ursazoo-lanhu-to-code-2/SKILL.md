---
name: code-format
description: Convert Lanhu HTML/CSS output into project frontend code for Vue, React, or the detected stack, with component reuse and design token mapping.
model: sonnet
---

# code-format

**核心原则：优先复用，禁止猜测。禁止省略代码。**

## 模式判断

调用方（design-to-code）会传入意图参数，根据意图选择模式：

| 意图参数 | 模式 |
|---------|------|
| `新建` | 模式 A：生成新文件 |
| `改造:src/pages/xxx/index.vue` | 模式 B：修改现有文件 |

## 执行步骤

### 1. 读取上下文（动代码前必须全部读完）

按以下优先级查找每类文档，找到第一个即用：

| 用途 | 优先 | 兜底顺序 |
|------|------|---------|
| 技术栈 | `README.md` | → `CLAUDE.md` → `package.json` |
| 组件文档 | `docs/components.md` | → `docs/` 下含 "Props"/"组件" 的 .md |
| 编码规范 | `docs/dev-spec.md` | → `docs/` 下含 "命名规范"/"开发规范" 的 .md → 扫描 `src/` 推断 |
| 交互逻辑 | `docs/tech-spec.md` | → 无则全部标 TODO |

**调用方（design-to-code）会传入 CONTEXT_FILES，直接使用传入路径，不必自己查找。**

文件缺失时的降级策略见 → `fallback-guide.md`

### 2. 分析蓝湖产物

读取 `.claude/lanhu-output/<页面名称>/index.html`，列出主要 UI 元素（不写代码）。

### 3. 组件映射

对每个 UI 元素查组件文档：
- 有完全匹配 → 直接用，传正确 props
- 有近似组件 → 用现有组件 + 自定义 class
- 确认没有 → 按 dev-spec 新建，标记为"新增组件"

常见映射失败案例见 → `failure-patterns.md`

### 4. 补全交互逻辑

从 `docs/tech-spec.md` 取：API 路径、状态处理、格式化规则。
找不到的用 `// TODO: 待确认` 标记，**不自行发明**。

---

## 模式 A：新建页面

按步骤 1-4 读取上下文后，生成完整新文件。

输出目录：`src/pages/<页面名>/` 或 `src/views/<页面名>/`（以 dev-spec 为准）。

**硬性约束：**
- 写完整代码，不允许 `// ... rest of component` 等占位
- 颜色/间距/字号精确匹配蓝湖数据
- 图片用 `assets/` 中的实际文件路径

---

## 模式 B：改造现有页面

按步骤 1-4 读取上下文后：

**额外步骤 B1：读取现有文件**

读取调用方传入的现有文件路径（如 `src/pages/home/index.vue`），完整理解现有代码。

**额外步骤 B2：列出变更范围**

对比设计稿与现有代码，明确列出（不写代码）：
```
变更项：
- [新增] 顶部渐变背景区域
- [修改] 余额显示区域：字号从 24px 改为 32px，颜色从 #333 改为 #fff
- [删除] 右上角设置入口
- [保留] 底部 TabBar（现有代码不动）
- [保留] 所有 API 调用逻辑（不动）
```

等用户确认变更范围后再写代码。

**额外步骤 B3：定向修改**

只修改变更项，保留：
- 现有业务逻辑（API 调用、事件处理、状态管理）
- 现有注释和 TODO
- 未变更的 UI 区域

每处修改标注原因，格式：`// [design-to-code] 按设计稿更新：xxx`

---

### 5. 输出摘要

```
✓ 生成/修改文件：[列表]
✓ 复用组件：[列表]
⚠ 新增组件：[列表]（需 review）
⚠ TODO 项：[列表]
```
