---
name: design-to-code
description: Lanhu to Code workflow for Claude Code. Convert Lanhu design URLs into Vue/React frontend code with component reuse, design token mapping, TODO-safe business logic, and optional code review.
---

# design-to-code

三阶段工作流：code-gen → code-format → code-review

## 入参收集（开始前必须确认）

**第一步：蓝湖页面信息**

未提供时必须先问：
```
请提供要转换的蓝湖页面地址（URL）或页面名称，例如：
- https://lanhuapp.com/web/#/item/project/stage?pid=xxx&id=yyy（指定页面）
- https://lanhuapp.com/web/#/item/project/stage?pid=xxx（项目级，需从列表中选页面）
- 或直接告诉我页面名称，我来查
```

不能假设或猜测页面，必须等用户明确给出后再继续。

**第二步：判断意图（新建 vs 改造）**

运行前置检查后，根据 `TECH_SPEC` 是否存在：

| 情况 | 操作 |
|------|------|
| 有 tech-spec | 在 tech-spec 中查找设计页面名对应的已有路由/文件 |
| → 找到匹配 | 自动判定"改造旧页面"，记录现有文件路径 |
| → 未找到匹配 | 自动判定"新建页面" |
| 无 tech-spec（NEEDS_DECISION） | 向用户询问（见下方话术） |

**无 tech-spec 时的询问话术：**
```
docs/tech-spec.md 不存在，无法自动判断这是新页面还是改造。

请告诉我：
1. 新建页面（根据设计稿生成新文件）
2. 改造现有页面（请同时告诉我现有文件路径，如 src/pages/home/index.vue）
```

## 前置检查

运行 `scripts/check-prerequisites.sh <项目根目录>`，按 exit code 处理：

| exit | STATUS | 行为 |
|------|--------|------|
| 1 | BLOCKED | 告知原因，**停止** |
| 2 | NEEDS_DECISION | 显示缺失文档列表，按对应话术询问用户后继续 |
| 0 | OK | 读取 CONTEXT_FILES，进入意图判断，然后阶段 1 |

脚本 stdout 包含 `CONTEXT_FILES` 块：
```
CONTEXT_FILES:
  TECH_STACK=CLAUDE.md
  COMPONENT_DOC=docs/开发规范与组件文档.md
  DEV_SPEC=docs/开发规范与组件文档.md
  TECH_SPEC=docs/tech-spec.md
```
将这些路径 + 意图（新建/改造+文件路径）一并传给 code-format。

**component-doc 缺失时的询问话术：**
```
docs/ 中没有找到组件文档，有三个选项：
1. 立即运行 component-doc-gen 生成初稿，审阅后再继续（推荐）
2. 以降级模式继续（扫描 src/ 推断可用组件，生成后请重点 review 组件使用部分）
3. 取消
```

## 阶段 1：code-gen

使用 Skill 工具调用 `/code-gen`，传入蓝湖页面 URL 作为参数。

code-gen 以隔离的 subagent 运行（`context: fork`），完成后返回路径 + 元素摘要，不会污染主会话上下文。

**URL 无具体页面 ID 时**（如只有 pid 没有 id）：code-gen 会展示该项目的所有设计图列表，等用户选择后才继续，不自动选第一个。

## 阶段 2：code-format

### ⚠️ 强制检查点：CSS 值对照表（必须执行）

在写任何样式代码之前，必须先完成以下步骤：

1. 读取蓝湖产物中的 HTML+CSS 代码
2. 提取所有 CSS 属性值（渐变、颜色、间距、字体、圆角等）
3. 输出 **CSS 值对照表**，格式如下：

```
## CSS 值对照表

| 选择器 | 属性 | 设计稿值 | 代码值 |
|--------|------|----------|--------|
| .income-stats-card | background | linear-gradient(135deg, #FFF5F0 0%, #FFFFFF 100%) | (待填写) |
| .debt-item | border-radius | 24rpx | (待填写) |
| ... | ... | ... | ... |
```

4. 填写"代码值"列时，必须与"设计稿值"完全一致
5. 对照表输出后，等待确认再继续

### 禁止事项

- 禁止简化渐变为纯色
- 禁止自作主张添加条件判断（如 v-if 权限控制）
- 禁止"改进"设计稿的值
- 禁止跳过对照表直接写代码

**只有输出完整的对照表后，才能开始写代码。**

### 传递给 code-format 的信息

将以下信息传给 code-format：
- CONTEXT_FILES（技术栈、组件文档、规范文档路径）
- 蓝湖产物路径（`.claude/lanhu-output/<页面名称>/`）
- 意图：`新建` 或 `改造:src/pages/xxx/index.vue`

## 阶段 3：code-review（可选）

阶段 2 完成后询问用户是否 code review，确认后调用 `/code-review-expert`。

## 进度反馈

```
[前置检查] 通过 / 需要决策...
[意图判断] 新建页面 / 改造 src/pages/xxx/index.vue
阶段 1/3：正在从蓝湖获取设计稿数据...
✓ 阶段 1 完成 → 阶段 2/3：正在生成框架代码...
✓ 阶段 2 完成 → 是否进行 code review？(y/n)
```

完整失败模式见 → `workflow-guide.md#失败模式`
