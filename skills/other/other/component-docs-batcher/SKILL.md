---
name: component-docs-batcher
description: 批量生成和维护前端组件库文档的自动化工具。专为 Monorepo 组件库设计（如 atom-ui-mobile），通过对比组件文件和文档的修改时间，自动生成任务清单并批量生成符合规范的完整组件文档。支持以下场景：(1) 定期批量更新组件文档，(2) 单个组件文档维护，(3) 新组件文档初始化。自动识别主要组件文件，跳过 index.ts、store、hooks 等辅助文件，文档路径为组件目录下的 index.zh-CN.md。
---

# Component Docs Batcher

## 概述

Component Docs Batcher 是一个自动化批量生成和维护前端组件库文档的工具。专为 Monorepo 架构的组件库设计，通过智能扫描主要组件文件，对比文档更新状态，生成规范化的组件文档，确保文档与代码保持同步。

## 核心功能

- **智能组件识别**: 自动识别组件目录中的主要组件文件（如 button/button.tsx），跳过 index.ts、store、hooks 等辅助文件
- **Git时间对比**: 通过对比组件文件和文档的git最后提交时间，确定文档状态（比文件系统时间更准确）
- **任务清单生成**: 自动生成结构化的todos.md任务清单
- **批量文档生成**: 按照规范批量生成完整的组件文档
- **组件库优化**: 针对 Monorepo 组件库结构优化，文档位于组件目录下的 index.zh-CN.md

## 工作流程

### 步骤1: 扫描组件

使用 `scan-components.ts` 脚本扫描组件库，识别需要处理的组件：

```bash
# 扫描指定组件库目录
npx ts-node .claude/skills/component-docs-batcher/scripts/scan-components.ts /path/to/packages/atom-ui-mobile/src/components

# 输出JSON格式（用于程序化处理）
npx ts-node .claude/skills/component-docs-batcher/scripts/scan-components.ts /path/to/components --json
```

**组件识别规则**:
- 扫描组件目录下的一级子目录（如 `button/`, `alert/`）
- 识别主要组件文件：与目录名同名的 `.tsx` 或 `.jsx` 文件（如 `button/button.tsx`）
- 自动跳过辅助文件：`index.ts`, `*.store.ts`, `use*.ts` 等
- 自动跳过辅助目录：`styles/`, `__tests__/` 等

**扫描结果分类**:
- ❌ **文档缺失**: 组件目录下没有 `index.zh-CN.md` 文档
- ⚠️ **文档过时**: 组件文件的git最后提交时间晚于文档
- ✅ **文档最新**: 组件和文档的git最后提交时间一致（不输出）

**时间对比说明**:
- 使用 `git log -1 --format=%ct` 获取文件的最后提交时间
- 如果文件没有git历史（新文件），则使用文件系统时间作为备选
- git时间比文件系统修改时间更准确，不受checkout、pull等操作影响

### 步骤2: 生成任务清单

使用 `generate-todos.ts` 生成详细的任务清单：

```bash
# 在当前目录生成todos.md
npx ts-node .claude/skills/component-docs-batcher/scripts/generate-todos.ts

# 在指定目录生成
npx ts-node .claude/skills/component-docs-batcher/scripts/generate-todos.ts /path/to/components /output/path/todos.md
```

生成的 `todos.md` 包含：
- 📊 统计信息（新增/更新数量）
- ✅ 任务列表（每个组件的详细任务）
- 📝 使用说明
- 📚 文档规范参考

### 步骤3: 分析组件结构

对于每个需要处理的组件，使用 `analyze-component.ts` 分析组件结构：

```bash
# 分析单个组件
npx ts-node .claude/skills/component-docs-batcher/scripts/analyze-component.ts /path/to/Component.tsx

# 输出JSON格式
npx ts-node .claude/skills/component-docs-batcher/scripts/analyze-component.ts /path/to/Component.tsx --json
```

**分析内容包括**:
- 组件类型（component/hook/util/type）
- Props接口（属性名、类型、默认值、必填性）
- TypeScript类型定义
- 导入依赖
- 代码示例（从注释提取）

### 步骤4: 批量生成文档

根据组件分析结果，为每个组件生成符合规范的文档：

1. **读取组件源码**: 使用 Read 工具读取完整的组件文件
2. **理解组件逻辑**: 不要依赖代码注释，独立理解组件实现
3. **提取关键信息**:
   - Props接口及其所有属性
   - TypeScript类型定义
   - 组件的使用场景和交互逻辑
   - 依赖的第三方组件API（如 Ant Design Mobile）
4. **确定正确的导出名称**: ⚠️ **重要！** 在生成文档前，必须检查 `/packages/atom-ui-mobile/src/index.ts` 确认组件的实际导出名称
   - 例如：`qr-code` 组件导出为 `QrCode`（不是 `QRCode`）
   - 例如：`message` 组件导出为小写的 `message`
   - 例如：`time-select` 直接导出为 `TimeSelect`（没有 `default as`）
5. **生成文档**: 按照 [文档格式规范](references/docs-format.md) 生成完整文档
6. **质量验证**: 对照质量检查清单验证文档完整性

**重要规则**:
- 文档路径：组件目录下的 `index.zh-CN.md`（如 `button/index.zh-CN.md`）
- 独立理解组件，不复制代码注释
- 完整列出所有API，特别是继承的第三方组件API（如 Ant Design Mobile Button 的所有属性）
- 提供真实可用的代码示例
- **导出名称必须与 `src/index.ts` 中的定义完全一致**（包括大小写）
- 引用方式示例：`import { Button } from '@evanfang/atom-ui-mobile';`

### 步骤5: 更新任务状态

完成每个组件文档后，在 `todos.md` 中标记任务为已完成：

```markdown
1. [x] 读取组件源码
2. [x] 分析组件结构
3. [x] 创建/更新文档
4. [x] 验证文档格式
5. [x] 检查文档完整性
```

所有任务完成后，删除 `todos.md` 文件。

## 文档格式规范

所有组件文档必须遵循标准格式。详见 [文档格式规范](references/docs-format.md)。

**关键要求**:
- 完整的API表格（属性名、类型、说明、默认值）
- TypeScript类型定义表格
- 真实可用的代码示例
- 主题变量列表或"无"的明确说明

## 使用场景

### 场景1: 定期批量更新

在项目迭代过程中，定期执行批量文档更新：

```bash
# 1. 扫描组件库
cd /Users/arwen/Desktop/Arwen/Demo/cc-system
npx ts-node .claude/skills/component-docs-batcher/scripts/scan-components.ts \
  /Users/arwen/Desktop/Arwen/evanfang/dp-design/packages/atom-ui-mobile/src/components

# 2. 生成任务清单
npx ts-node .claude/skills/component-docs-batcher/scripts/generate-todos.ts \
  /Users/arwen/Desktop/Arwen/evanfang/dp-design/packages/atom-ui-mobile/src/components

# 3. 按照生成的todos.md批量处理每个组件
# 4. 完成后删除todos.md
```

### 场景2: 单个组件维护

针对特定组件快速更新文档：

```bash
# 1. 分析组件结构
npx ts-node .claude/skills/component-docs-batcher/scripts/analyze-component.ts \
  /Users/arwen/Desktop/Arwen/evanfang/dp-design/packages/atom-ui-mobile/src/components/button/button.tsx

# 2. 根据分析结果生成/更新文档
# 文档位置: button/index.zh-CN.md
```

### 场景3: 新组件文档初始化

为新创建的组件快速生成文档：

```bash
# 1. 检查组件是否需要文档
npx ts-node .claude/skills/component-docs-batcher/scripts/scan-components.ts \
  /Users/arwen/Desktop/Arwen/evanfang/dp-design/packages/atom-ui-mobile/src/components

# 2. 新组件会在"文档缺失"列表中显示
# 3. 为新组件生成 index.zh-CN.md 文档
```

## 资源

### scripts/

可执行的TypeScript脚本，提供扫描、分析和文档生成功能。

**scan-components.ts**: 组件文件扫描器
- 扫描指定目录下的组件文件
- 对比组件和文档的修改时间
- 输出需要更新或新增的组件列表
- 支持JSON格式输出

**generate-todos.ts**: 任务清单生成器
- 基于扫描结果生成todos.md
- 包含详细的任务步骤和统计信息
- 提供文档规范引用

**analyze-component.ts**: 组件结构分析器
- 分析组件源代码结构
- 提取Props、类型、依赖等信息
- 输出结构化的组件分析结果

### references/

文档和参考资料，指导文档生成过程。

**docs-format.md**: 组件文档格式规范
- 标准文档模板
- 编写规则和质量检查清单
- 不同组件类型的特殊要求
