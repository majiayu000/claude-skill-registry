---
name: jeecg-aiflow
description: >
  JeecgBoot AI 编排流程（AIFlow）全生命周期管理——通过自然语言描述需求，自动创建、编辑、查询、删除、调试、发布 AI 编排流程。
  只要用户意图涉及「AI编排」「AIFlow」就必须使用本技能，包括但不限于：
  创建 AI 编排流程（"做一个AI流程"、"创建aiflow"、"新建编排"、"做一个知识库问答流程"、"创建一个大模型对话流程"），
  修改已有流程（"给流程加个节点"、"改一下LLM的提示词"、"修改流程"），
  查询流程（"查看流程列表"、"有哪些AI流程"），
  删除流程（"删除流程"、"移除XX流程"），
  调试运行流程（"调试流程"、"运行流程"、"测试流程"），
  发布管理（"发布流程"、"取消发布"），
  复制流程（"复制流程"、"克隆流程"）。
  关键词触发：aiflow、ai-flow、AI编排、AI流程、编排流程、大模型流程、知识库流程、LLM流程。
  注意：本技能仅处理 AI 编排流程（AIFlow），不处理 BPMN 工作流（使用 jeecg-bpmn）、
  不处理简流（使用 jeecg-lowcode-miniflow）。
---

# JeecgBoot AIFlow — AI 编排流程管理

## 设计原则

本 skill 的核心架构是**模板驱动**：AI 不直接生成节点 JSON，而是选择节点类型后由脚本从权威模板生成完整结构，AI 只负责填写业务配置。这样做的原因是 AIFlow 的节点配置字段非常多且结构严格，让 AI 从零生成容易产生格式错误。chain（LiteFlow EL 表达式）也由 Python 脚本自动生成，AI 不需要关心。

修改已有流程时，先查询再修改——因为流程的 design JSON 包含所有节点状态，凭记忆操作容易丢失配置。

## 前置条件

用户需提供两个信息：
1. **API 地址**（默认 `http://localhost:3100/jeecgboot`）
2. **X-Access-Token**（从浏览器 F12 → Network → Request Headers 复制）

## 工作目录机制

所有操作基于「工作目录」。首先通过 `init-work` 创建工作目录，后续所有命令只需传 `-w`，脚本自动从工作目录中的 `meta.json` 读取 API 凭证和流程信息，design.json 也存放在工作目录中。

```
工作目录结构：
  {临时目录}/jeecg-aiflow/{workId}/
    ├── meta.json      ← name, descr, apiBase, token, flowId
    └── design.json    ← 节点和连线的完整 JSON
```

---

## 创建流程（核心流程）

### 1. 初始化工作目录

```bash
python "<skill目录>/scripts/aiflow_creator.py" init-work \
  --name "流程名称" \
  --descr "流程描述" \
  --api-base "<api_base>" \
  --token "<token>"
```

返回 `workId`，后续所有命令都用这个 ID。

### 2. 理解需求，选择节点

根据用户描述，从下方「节点类型速查表」选择节点。每个流程必须包含 1 个 `start` 和至少 1 个 `end`。

### 3. 展示摘要，等待用户确认（强制）

生成之前必须展示完整摘要并等待用户明确确认。除非用户事先说过"不用确认直接生成"，否则不要跳过这一步。

摘要需要包含**三部分**：节点列表、节点关系（连线）、关键配置：

```
流程名称：知识库问答助手

节点列表：
  1. start — 开始（接收用户问题）
  2. knowledge — 知识库检索
  3. llm — 大模型（根据检索结果回答）
  4. end — 结束（返回回答文本）

节点关系：
  start → knowledge → llm → end

关键配置：
  - knowledge: 知识库待选择（需要您提供知识库ID或让我查询列表）
  - llm: 模型待选择，系统提示词="你是一个知识库问答助手..."
  - end: 输出类型=text，内容引用 llm 的回复
```

等待用户回复确认后再继续下一步。如果用户提出修改意见，调整后重新展示摘要。

### 4. 生成模板 JSON

```bash
python "<skill目录>/scripts/aiflow_creator.py" generate \
  -w "<workId>" \
  --types "start,knowledge,llm,end"
```

脚本从权威模板生成 design.json 到工作目录。返回包含文件定位信息的结构：

```json
{
  "totalLines": 168,
  "nodes": [
    {"id": "start-node", "type": "start", "startLine": 3, "endLine": 50},
    {"id": "746...", "type": "llm", "startLine": 51, "endLine": 92},
    {"id": "746...", "type": "end", "startLine": 93, "endLine": 110}
  ],
  "edgesLines": {"startLine": 112, "endLine": 167}
}
```

- `totalLines` — design.json 的总行数。行数较少时可全量读取，较多时按节点行号精准定位
- `nodes[i].startLine / endLine` — 该节点在 design.json 中的起止行号（1-based），用于 Read 工具的 `offset`/`limit` 参数精准读取单个节点
- `edgesLines.startLine / endLine` — edges 数组的起止行号，修改连线时精准定位
- `generate`、`export`、`add-node`、`remove-node` 命令都返回以上信息

### 5. 读取 JSON，编辑业务配置

利用返回的行号，用 Read 工具按需读取目标节点或 edges 片段，再用 Edit 工具修改。需要关注两类内容：

**A. 业务配置**（根据用户需求填写）

每种节点需要配置的核心字段：

| 节点 | 需要填写 | 用户未指定时怎么办 |
|------|---------|-----------------|
| llm | `model.modeId`、`model.params.model`、系统提示词 | 查询模型列表让用户选择，modeId 取 value、params.model 取 text |
| knowledge | `knowIds` | 查询知识库列表让用户选择 |
| knowledgeWrite | `knowIds`、`content` | 查询知识库列表让用户选择 |
| switch | `if[].conditions`、`if[].next`、`else.next` | 向用户询问判断条件 |
| classifier | `model.modeId`、`model.params.model`、`categories[].category`、`categories[].next`、`else.next` | 查询模型列表，modeId 取 value、params.model 取 text |
| varExtract | `model.modeId`、`model.params.model`、`variables`、`success.next`、`fail.next` | 查询模型列表，modeId 取 value、params.model 取 text |
| loop | `type`、counted 时 `maxLoopTimes`、array 时 `loopItemsParam` | 向用户询问循环方式 |
| setLoopVar | `targetField`、`sourceVar` | 根据循环变量定义填写 |
| code | `code` 脚本内容 | 根据需求编写 |
| http | `http.url`、`http.method` | 向用户询问接口地址 |
| sql | `sql.dataSourceId`、`sql.outputSql` | 查询数据源列表让用户选择 |
| tools | `tools.pluginId`、`tools.toolName` | 向用户询问工具/MCP 选择 |
| braveSearch | inputParams（搜索关键词） | 根据需求绑定上游变量 |
| reply | `content` | 根据需求填写 |
| end | `outputType`、`outputContent` | 默认 `text` 类型即可 |
| subflow | `subflowId` | 查询子流程列表让用户选择 |

**查询系统资源**（不需要手动 init_api，通过 query 子命令自动从工作目录读取凭证）：

```bash
python "<skill目录>/scripts/aiflow_creator.py" query -w "<workId>" --resource models        # LLM 模型
python "<skill目录>/scripts/aiflow_creator.py" query -w "<workId>" --resource knowledge     # 知识库
python "<skill目录>/scripts/aiflow_creator.py" query -w "<workId>" --resource datasources   # 数据源
python "<skill目录>/scripts/aiflow_creator.py" query -w "<workId>" --resource subflows      # 子流程
```

**start 和 end 是每个流程必有的节点，完整配置参考如下（无需查索引）：**

### start — 开始节点

> 进阶配置见 `references/node-reference.md` 的 `start — 定时触发配置` 章节，包含：cronTrigger 开关与 cronType 选择（minute/hour/day/custom）、cronExp 表达式生成规则、custom 对象结构（时/天/周/月的精细控制）。

#### inputParams 结构

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `field` | string | — | 字段名（编程用） |
| `name` | string | — | 显示名称 |
| `type` | string | — | 参数类型（见下表） |
| `required` | boolean | `false` | 是否必填 |

**固定的默认 inputParams（3 个）：**

| field | name | type | required |
|-------|------|------|----------|
| `content` | 用户问题 | `string` | false |
| `history` | 历史记录 | `string[]` | false |
| `images` | 图片 | `picture` | false |

**type 枚举值（开始节点支持 4 种）：**

| type 值 | 含义 | 对应 UI 控件 |
|---------|------|-------------|
| `string` | 文本 | Input 输入框 |
| `number` | 数值 | InputNumber 数字框 |
| `picture` | 图片 | 图片上传 |
| `file` | 文件 | 文件上传 |

> 注意：图片字段的 field 必须命名为 `images`，否则 LLM 节点无法接收图片。

> **禁止使用数组类型**：start 节点的 inputParams **只支持以上 4 种类型**，不支持 `string[]`、`object[]` 等数组类型。如果流程需要数组输入（如 loop 的 array 迭代模式），应通过前置的 code 节点构造数组，而不是在 start 节点定义数组字段。

其他节点的 inputParams/outputParams 还可能使用 `string[]`、`number[]`、`object[]`、`object`、`text`、`boolean` 等扩展类型。

#### outputParams

无（开始节点没有输出参数）。

#### 校验规则

| 条件 | 错误消息 |
|------|---------|
| cronTrigger.enabled=true 且存在 required 的 inputParam 未配置默认值 | `定时触发器：存在必填参数未配置默认值` |

#### 特殊行为

- 固定 ID: `start-node`，不可修改
- 只有右侧锚点（无左侧输入）
- 不允许删除

### end — 结束节点

#### options 字段

| 参数 | 类型 | 默认值 | 可选值 | 说明 |
|------|------|--------|--------|------|
| `outputType` | string | `'text'` | `'default'` / `'text'` / `'card'` | 输出类型 |
| `outputContent` | string | `''` | 支持变量引用 | outputType='text' 时的返回文本 |
| `cardConfig` | object\|null | `null` | 卡片配置对象 | outputType='card' 时的卡片绑定 |

**outputType 三种模式区别：**

| outputType | 返回内容 | 使用场景 |
|-----------|---------|---------|
| `'default'` | outputParams 中选择的变量（JSON 格式） | API 调用、子流程等需要结构化数据 |
| `'text'` | outputContent 中配置的文本（支持 `{{变量name}}` 引用，需先在 outputParams 中绑定） | 对话场景，返回自然语言文本 |
| `'card'` | cardConfig 绑定的卡片 | 需要富文本/结构化卡片展示 |

#### 校验规则

| 条件 | 错误消息 |
|------|---------|
| outputType='default' 且 outputParams 为空 | `输出变量: 必填` |
| outputType='text' 且 outputContent 为空 | `返回文本不能为空` |
| outputType='card' 且 cardConfig 为 null | `需要绑定卡片` |

> 进阶配置见 `references/node-reference.md` 的 `end — 进阶配置` 章节，包含：cardConfig 卡片结构（outputType='card' 时的字段绑定）、作为子流程时各 outputType 的输出行为差异。

#### 特殊行为

- 只有左侧锚点（无右侧输出）
- 一个流程至少需要 1 个 end 节点

#### 使用要点：end 与 reply 的区别

end 是流程的**最终输出**，流程结束后只保留 end 节点的内容作为最终返回结果。需要给用户返回内容并结束流程时，必须用 end。

**常见错误**：用 reply 节点代替 end 节点来结束某个分支（如"商务问题直接回复请联系销售团队"）。reply 在流式传输时能看到内容，但流程最终结果中不会保留。正确做法是用 end 节点。

其他节点的完整字段说明在 `references/node-reference.md` — 修改具体字段前按下方索引表 `Read` 对应片段（只读该片段，不要全量读）：

<!-- NODE_OPTIONS_INDEX:START -->
!`python ${CLAUDE_SKILL_DIR}/scripts/gen_node_options_index.py 2>/dev/null || echo '> （节点选项索引自动生成失败，请用 Grep 搜索 "## <节点type>" 定位 references/node-reference.md 中的对应章节）'`
<!-- NODE_OPTIONS_INDEX:END -->

**B. 流程结构**（AI 自行填写）

1. **节点坐标** — 按以下常量布局：

| 常量 | 值 | 说明 |
|------|-----|------|
| 节点宽度 | 332px | 所有节点统一宽度 |
| 节点高度 | 62px | 基准高度（switch/classifier 按分支数动态增长） |
| 水平间距 X_GAP | 400px | 相邻节点左边缘间距 |
| 垂直间距 Y_GAP | 180px | 分支节点间垂直间距 |
| 起点坐标 | (200, 300) | start 节点位置 |

**线性流程**：所有节点在同一行（y=300），x 依次 +400。

**分支流程**（switch/classifier/varExtract 有多个下游）：分支下游节点竖向排列，以父节点 y 为中心上下分散，相邻分支间距 ≥ Y_GAP(180px)。示例（switch 有 3 个分支）：
```
分支1 y = 300 - 180 = 120
分支2 y = 300           （与 switch 同行）
分支3 y = 300 + 180 = 480
```

**防重叠规则**：放置节点时，检查同一 x 列上已有节点，确保任意两个节点的 y 差值 ≥ Y_GAP(180px)。如果分支后的节点再次汇合（多条路径合并到同一个节点），汇合节点 y 取所有入边来源节点 y 的平均值。

2. **连线 edges** — 描述节点间的连接关系

每条边**必须**包含 `sourceAnchorId` 和 `targetAnchorId`，否则前端渲染效果不一致。

**每条边必须包含 `id`、`pointsList` 和 `properties`**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 边的唯一标识，可用雪花ID或任意唯一字符串 |
| `pointsList` | array | 是 | 贝塞尔曲线控制点数组（见下方格式要求） |
| `properties` | object | 是 | 固定 `{"runStatus": ""}` |

**`pointsList` 格式（严格要求，违反会导致前端 `Cannot read properties of undefined (reading 'x')` 报错）：**

- **`base-edge`（贝塞尔曲线边）必须恰好 4 个点**：`[源锚点, 源控制点, 目标控制点, 目标锚点]`
  ```
  源锚点:    {x: 源节点.x + 332,       y: 源节点.y + 31}   // 节点右边缘中点
  源控制点:  {x: 源节点.x + 332 + 100,  y: 源节点.y + 31}   // 右偏移100px
  目标控制点: {x: 目标节点.x - 100,      y: 目标节点.y + 31}  // 左偏移100px
  目标锚点:  {x: 目标节点.x,            y: 目标节点.y + 31}   // 节点左边缘中点
  ```
  > 其中 332 = 节点宽度，31 = 节点高度(62) / 2。分支节点的源锚点 y 坐标需根据分支索引微调。

- **`base-line-edge`（直线边，loop↔loopBody 专用）必须为空数组 `[]`**，不能省略字段

**完整边示例**（`base-edge`）：
```json
{"id": "325590000000000001", "type": "base-edge", "sourceNodeId": "A", "targetNodeId": "B", "sourceAnchorId": "A_output", "targetAnchorId": "B_input", "pointsList": [{"x": 532, "y": 331}, {"x": 632, "y": 331}, {"x": 500, "y": 331}, {"x": 600, "y": 331}], "properties": {"runStatus": ""}}
```

**完整边示例**（`base-line-edge`）：
```json
{"id": "325590000000000002", "type": "base-line-edge", "sourceNodeId": "loop1", "targetNodeId": "loop1_loopBody", "sourceAnchorId": "loop1_link_body", "targetAnchorId": "loop1_loopBody_link_loop", "pointsList": [], "properties": {"runStatus": ""}}
```

anchorId 规则：
- 普通出边：`sourceAnchorId = "{sourceNodeId}_output"`
- 普通入边：`targetAnchorId = "{targetNodeId}_input"`

**分支节点的出边**用专用 sourceAnchorId 替代 `_output`：
- **switch**: `{id}_source_if`（IF）、`{id}_case_{n}`（ELIF n≥2）、`{id}_source_else`（ELSE）
- **classifier**: `{id}_case_{n}`（分类 n≥1）、`{id}_case_else`
- **varExtract**: `{id}_success`、`{id}_fail`

**并行分支**：普通节点（非 switch/classifier）也可以有多条出边连接到不同下游，形成并行执行路径。多条出边都使用同一个 `sourceAnchorId = "{nodeId}_output"`，连到不同的 targetNodeId。并行路径可以汇合到同一个下游节点。

**分支流程关键规则（必须遵守）：**

1. **每个分支出口都必须有独立的边**：switch 的 IF/ELIF/ELSE、classifier 的每个 category + ELSE、varExtract 的 success/fail，每个分支都必须有一条带对应 `sourceAnchorId` 的边连接到下游节点。不能遗漏任何分支（尤其是 ELSE），即使多个分支指向同一个目标节点也需要各自独立的边。
2. **分支出口的 `next` 字段必须和 edges 一致**：switch 的 `if[i].next`/`else.next`、classifier 的 `categories[i].next`/`else.next`、varExtract 的 `success.next`/`fail.next` 必须填写，且值与 edges 中的 `targetNodeId` 一致。
3. **互斥分支汇合时用 varMerge**：当 switch/classifier 的多个分支各自产出结果后需要汇合到同一个下游节点时，**不要**让下游节点直接分别引用各分支的输出变量（运行时只有一个分支执行，其他变量为空）。正确做法是在汇合处插入 `varMerge` 节点，将各分支的同类输出聚合为一个变量，下游节点引用聚合后的变量。

### 6. 提交保存

```bash
python "<skill目录>/scripts/aiflow_creator.py" submit -w "<workId>"
```

脚本自动从工作目录读取 meta.json（name, descr, apiBase, token）和 design.json，完成：校验 → 生成 chain → 创建/保存流程。

校验不通过时会返回具体错误列表，修改 design.json 后重新提交即可。

**编辑已有流程时的校验错误处理**：用户提供的原始流程可能本身就有校验问题（不是 AI 编辑造成的）。submit 失败时，AI 应分析错误列表，区分哪些是自己编辑引入的、哪些是原始流程就有的。如果全部是原始问题，告知用户"当前流程存在 N 个原有问题"并列出，询问是否需要修复。如果用户确认不修复，使用 `--skip-validate` 跳过校验直接保存：

```bash
python "<skill目录>/scripts/aiflow_creator.py" submit -w "<workId>" --skip-validate
```

> `--skip-validate` 仅允许编辑已有流程（有 flowId）时使用，新建流程不允许跳过。

---

> 完整的端到端示例见 `references/aiflow-operations.md` 的「端到端示例」章节。

---

## 其他操作（查询、编辑、删除、复制、发布、调试）

创建以外的所有操作，阅读 `references/aiflow-operations.md` 获取完整指南。

**编辑已有流程**时 `init-work` 带 `--flow-id` 即可自动导出 design，无需单独 `export`：
```bash
python "<skill目录>/scripts/aiflow_creator.py" init-work \
  --name "流程名" --api-base "<url>" --token "<tk>" --flow-id "<id>"
# 返回 workId + nodes（含 startLine/endLine），用 Read/Edit 修改 design.json ...
python "<skill目录>/scripts/aiflow_creator.py" submit -w "<workId>"
```

该文档涵盖：流程列表查询、详情查询、编辑已有流程（含添加/删除/修改节点）、删除流程、复制流程、发布/取消发布、调试运行、子流程查询。

---

## 节点类型速查表

### 基础节点

| 类型 | 标签 | 用户说 | 说明 |
|-----|------|-------|------|
| `start` | 开始 | 开始、入口 | 流程入口，固定 ID: `start-node` |
| `end` | 结束 | 结束、输出 | 流程出口，配置返回内容 |

### AI 节点

| 类型 | 标签 | 用户说 | 说明 |
|-----|------|-------|------|
| `llm` | 大模型 | 大模型、LLM、AI对话、GPT、Claude | 调用大语言模型 |
| `classifier` | 分类器 | 分类、意图识别 | AI 意图分类，多分支 |
| `varExtract` | 变量提取器 | 变量提取、实体提取 | LLM 提取结构化变量，双分支(success/fail) |

### 知识库 & 记忆

| 类型 | 标签 | 用户说 | 说明 |
|-----|------|-------|------|
| `knowledge` | 知识库 | 知识库、RAG、检索 | 向量检索 |
| `knowledgeWrite` | 知识库写入 | 写入知识库 | 写入文本/文件 |
| `chatMemoryGet` | 记忆检索 | 记忆、长期记忆 | 检索应用记忆库 |
| `chatMemorySet` | 记忆写入 | 记住、写入记忆 | 写入应用记忆库 |

### 变量

| 类型 | 标签 | 用户说 | 说明 |
|-----|------|-------|------|
| `chatVarGet` | 变量读取 | 读取变量 | 读取会话变量 |
| `chatVarSet` | 变量赋值 | 设置变量 | 设置会话变量 |
| `varMerge` | 变量聚合 | 合并变量 | 聚合多个变量值 |

### 控制流

| 类型 | 标签 | 用户说 | 说明 |
|-----|------|-------|------|
| `switch` | 条件分支 | 条件判断、分支、如果 | IF/ELIF/ELSE |
| `loop` | 循环 | 循环、遍历 | 计数/无限/数组循环 |
| `subflow` | 子流程 | 子流程、调用流程 | 嵌套流程 |

### 执行节点

| 类型 | 标签 | 用户说 | 说明 |
|-----|------|-------|------|
| `code` | 脚本执行 | 代码、脚本 | JS/Python/Groovy/Aviator |
| `http` | HTTP 请求 | HTTP、接口调用 | REST API 调用 |
| `sql` | SQL自定义 | SQL、数据库查询 | SQL 执行 |
| `enhanceJava` | Java 增强 | Java增强 | 调用 Java 类 |
| `tools` | 工具调用 | 工具、MCP | 外部工具/MCP |
| `braveSearch` | Brave搜索 | 搜索、网络搜索 | 网络搜索 |
| `reply` | 直接回复 | 直接回复、流式输出 | **仅用于流程执行过程中的中间输出**（如开启 LLM 流式输出），流程结束后 reply 的内容会被丢弃 |
| `sysGetUserinfo` | 用户信息 | 用户信息、当前用户 | 获取登录用户信息 |

### reply 与 end 的区别（重要）

- **end**：流程的最终输出，流程结束后保留为返回结果。
- **reply**：中间输出，流式传输时可见但流程结束后**被丢弃**。主要用于 LLM 流式输出和进度推送。
- **错误用法**：用 reply 代替 end 来结束分支——最终结果为空。

> 详见 `references/node-reference.md` 中 reply 和 end 节点的使用要点。

### 循环节点联动机制（重要）

- 创建 loop 节点时，脚本**自动创建** loopBody + 连接边，删除时**级联删除**。
- loopBody 是分组容器，循环体内子节点放在其中，`children` 数组记录子节点 ID。
- 循环体内最后一个子节点**不连回 loopBody**（否则 chain 死循环）。
- 如果下游节点引用循环变量，必须在 loop 的 `outputParams` 中声明（不引用则不需要）。
- 循环体内第一个子节点 x ≈ loop.x - 600，后续按 X_GAP 递增。

> 详见 `references/node-reference.md` 中 loop、loopBody、setLoopVar 节点的使用要点。

---

## 变量引用

变量引用由**两部分**组成，缺一不可：

### A. 建立绑定（inputParams / outputParams）

在需要引用变量的节点的 `inputParams`（或 end 节点的 `outputParams`）中添加绑定条目，指明变量来自哪个节点的哪个字段：

```json
{
  "field": "content",
  "name": "用户问题",
  "nodeId": "start-node",
  "type": "string"
}
```

- `field` — 来源节点的输出字段名（如 start 的 `content`、llm 的 `text`）
- `name` — 为这个变量起的显示名称（后续在文本中用 `{{显示名称}}` 引用）
- `nodeId` — 来源节点的 ID
- `type` — 变量类型
- `isCustom`（可选）— 布尔值，默认 false。设为 true 时表示使用自定义值而非上游节点引用，此时 `nodeId` 和 `field` 可为空
- `customValue`（可选）— 自定义值，`isCustom=true` 时生效。变量值直接取 customValue 而非从上游节点获取。用于固定值或默认值场景

### B. 在文本中引用（用 name，不是 nodeId.field）

```
{{用户问题}}
{{回复内容}}
```

引用时使用的是绑定中定义的 **name**（显示名称），不是 `nodeId.field`。

### 完整示例

llm 节点引用 start 节点的用户输入：
```json
// llm 节点的 inputParams 中建立绑定
"inputParams": [
  {"field": "content", "name": "用户问题", "nodeId": "start-node", "type": "string"}
]

// llm 节点的 messages[1].content 中引用
"content": "{{用户问题}}"
```

end 节点引用 llm 节点的回复：
```json
// end 节点的 outputParams 中建立绑定
"outputParams": [
  {"field": "text", "name": "回复内容", "nodeId": "<llm节点ID>", "type": "string"}
]

// end 节点的 outputContent 中引用
"outputContent": "{{回复内容}}"
```

---

## 错误处理

| 错误 | 原因 | 解决 |
|------|------|------|
| Token 过期 (401) | 令牌失效 | 提示用户重新获取 |
| design 校验不通过 | 节点配置缺失或连线有误 | 根据错误列表修改后重新提交 |
| chain 生成失败 | edges 连线结构有误 | 检查 sourceNodeId/targetNodeId 和分支锚点 |

---

## 脚本速查

所有命令通过 `python "<skill目录>/scripts/aiflow_creator.py" <子命令>` 执行。

| 子命令 | 用途 | 关键参数 |
|--------|------|---------|
| `init-work` | 创建工作目录 | `--name --api-base --token [--flow-id] [--descr]` |
| `generate` | 生成模板 design.json | `-w <workId> --types` |
| `export` | 导出已有流程 design.json | `-w <workId> [--flow-id]` |
| `add-node` | 插入新节点 | `-w <workId> --type --after` |
| `remove-node` | 删除节点 | `-w <workId> --node-id` |
| `submit` | 校验 + chain + 保存 | `-w <workId> [--skip-validate]` |
| `query` | 查询系统资源 | `-w <workId> --resource (models/knowledge/datasources/subflows)` |

其他脚本（被 aiflow_creator.py 内部调用，一般不需要直接使用）：

| 脚本 | 用途 |
|------|------|
| `scripts/aiflow_apis.py` | API 封装层（Sign 签名 + HTTP 请求） |
| `scripts/aiflow_utils.py` | 核心工具（节点生成、插入、删除、校验） |
| `scripts/generate_chain.py` | chain 生成器（被 submit 自动调用） |

## 参考文档

| 文档 | 何时查阅 |
|------|---------|
| `references/aiflow-operations.md` | 执行创建以外的操作（查询、编辑、删除、复制、发布、调试）时 |
| `references/node-reference.md` | 修改节点配置时（options 字段、校验规则、特殊行为与使用要点） |
| `references/sync-guide.md` | **仅当用户要求同步节点配置/更新前后端变更时**。正常工作流程不需要阅读（含 chain 生成器源码映射表） |
