---
name: component-doc-gen
description: Scan frontend src directories and generate docs/components.md so Claude Code can reuse existing Vue/React components during design-to-code generation.
model: sonnet
disable-model-invocation: true
---

# component-doc-gen

**职责：** 扫描项目 `src/` 目录，提取组件 props/emits/用法，生成 `docs/components.md` 初稿。

**运行场景：** GitLab/Codeup 定时 CI Pipeline，不在 design-to-code 流程中内联调用。

**不做：** 生成 tech-spec.md（API 路径只有人知道）、修改现有组件代码。

## 执行步骤

### 1. 发现组件（确定性，脚本执行）

```bash
bash scripts/detect-components.sh <项目根目录>
```

输出每行格式：`<shared|page>:<components目录>:<组件文件路径>`

### 2. 按类型分组

- `shared` → 通用组件（跨页面可用）
- `page` → 页面级组件（仅所属页面使用）

### 3. 逐文件提取（AI 读取，每文件独立处理）

读取每个组件文件，提取：

| 提取项 | Vue 3 来源 | React/TSX 来源 |
|--------|-----------|----------------|
| 组件名 | 文件名 / `name` 选项 | 函数名 / export default |
| Props | `defineProps<T>()` 或 `withDefaults` | TypeScript interface / PropTypes |
| Emits | `defineEmits()` | 回调 props（`onXxx`） |
| 用法示例 | 从 props 推断基础用法 | 从 props 推断基础用法 |

**提取规则：**
- Props 名称和类型以源码为准，不推测语义
- 无法确定的标注 `⚠️ 需人工确认`
- 不读取组件内部实现逻辑（只看对外接口）

### 4. 生成 docs/components.md

格式见 → `output-format.md`

### 5. 输出变更摘要

```
生成完成：
  通用组件：N 个
  页面级组件：M 个（来自 K 个页面）
  需人工确认：P 项（已在文件中标注 ⚠️）

docs/components.md 已写入，请审阅后提交 MR。
```

## 关键约束

- 每次全量重新生成（不做增量 diff，避免过时信息残留）
- 文件顶部必须保留 `⚠️ 自动生成` 提示，合并后由开发者手动删除
- 同名组件（shared 和 page 各有一个）在文档中分开列出，不合并
