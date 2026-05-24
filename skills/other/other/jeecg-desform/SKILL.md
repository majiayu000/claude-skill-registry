---
name: jeecg-desform
description: JeecgBoot 表单设计器（desform）全生命周期管理——通过对话的方式创建、更新、复制、删除表单设计器，管理表单数据（CRUD），生成 PC/移动端表单视图，以及一键创建 OA 审批应用（表单+流程+授权）。只要用户意图涉及「表单设计器」就必须使用本技能，包括但不限于：创建或生成表单（"做一个请假表单"、"AI设计表单"、"desform"）、修改已有表单或字段（"加个字段"、"改一下表单"）、复制/删除表单、录入或查询表单数据、创建表单视图（含移动端）、以及咨询设计器功能（控件类型、字典配置、校验规则、关联记录、子表、公式计算、JS/CSS增强、默认值、外链等）。当用户想要创建带审批流程的 OA 应用时也应触发（"创建OA应用"、"创建审批单"、"创建报销单"、"创建请假单"、"做一个OA表单带流程"、"一键创建表单和流程"、"面试申请"、"出差申请"等）。即使用户只是描述字段需求（如"需要姓名、手机号字段"）而未明确说"表单"，只要语境指向表单设计器也应触发。注意：本技能仅处理表单设计器（desform），不处理 Online 表单——如果用户明确提到"Online表单"或"online表"，应使用 jeecg-onlform 技能。
---

# JeecgBoot 表单设计器 AI 自动生成器

使用自然语言（或图片）生成表单设计器配置。

> **重要：本 skill 只处理「表单设计器」（desform），不涉及 Online 表单。两者是完全独立的表单体系。**

---

## 执行准则（必读）

本技能的所有强制规则，都在对抗同一个 AI 倾向：**用"我大概知道"替代"我确认知道"**。

**跳步**：校验、确认、读文档看似多余——AI 倾向于省略。但每个步骤都是防错设计，省略后出错时代价是数据损坏或 API 异常，且无法回头。

**猜测**：系统特定的编码、API 参数格式、控件配置细节，训练知识不够用，但 AI 会用"看起来合理"的值填补——配置看似正确，运行时才报错。

本系统有大量与通用认知冲突的特殊行为（API 接口不可靠、参数大小写有严格要求、控件结构非直觉、部分值只存在于用户自己的系统中）。**你对这个系统的了解程度，不如这份文档和用户本身。**

遇到任何操作，遵守以下三条：

1. **步骤不可跳** — 感觉没必要时仍要执行，这是防错机制而不是形式
2. **有专属文档的功能先读文档** — 通用知识在本系统大概率是错的，文档记录的是实测验证的行为
3. **系统特定的值必须问** — 无法从当前上下文确认的参数（规则 Code、报表编码、业务 ID 等），直接告知用户"需要您提供 X"，不要猜测

**第 2 条的执行方式（强制）：** 遇到不确定某功能在哪里配置时，先在 SKILL.md 末尾的参考文档列表中找到对应的 `references/` 文件并读取，再执行任何 API 操作。参考文档列表覆盖了所有专属功能，是权威索引。

---

## 临时配置文件规则（强制）

所有传给脚本的 `--config <xxx.json>` 必须放在 **`{系统临时目录}/jeecg-desform/`** 下，由操作系统自动清理；skill 与脚本均不主动删除该目录或文件。

`tempfile.gettempdir()` 自动适配各平台：Windows `%TEMP%`、Linux `/tmp`、macOS `/var/folders/.../T`（注意 macOS 并非 `/tmp`）。文件名建议使用 **`<表名>_<步骤>.json`**（如 `sk_audit_create.json`），路径已含技能名称无需重复前缀。

### 场景一：Claude 用 `Write` 工具写文件后调脚本（最常见）

`Write` 工具需要绝对路径，所以**必须先**通过公共脚本拿到路径。脚本一次完成「定位系统临时目录 → 创建技能子目录 → 返回路径」：

```bash
# 取目录
python "<skill目录>/scripts/skill_temp_path.py"
# → C:\Users\xxx\AppData\Local\Temp\jeecg-desform

# 直接拿完整文件路径（推荐）
python "<skill目录>/scripts/skill_temp_path.py" -f sk_audit_create.json
# → C:\Users\xxx\AppData\Local\Temp\jeecg-desform\sk_audit_create.json
```

得到路径后：
1. 用 `Write` 工具将 JSON 写入该路径
2. 调脚本 `--config <该路径>`

**会话内目录可复用**——首次取到后缓存到上下文，后续临时文件直接拼接同一前缀，不必每次重新调用脚本。

### 场景二：技能内的 Python 脚本自行写中间文件

skill 自己的脚本（`desform_creator.py` 等）在脚本进程内写文件时，**不要**通过 `Write` 工具，直接用 `tempfile`：

```python
import tempfile, os, json

skill_dir = os.path.join(tempfile.gettempdir(), "jeecg-desform")
os.makedirs(skill_dir, exist_ok=True)          # 确保目录存在，不主动检查

config_path = os.path.join(skill_dir, 'sk_audit_create.json')
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
```

### ❌ 禁止

- 写到 `<skill>/tmp/` 或当前工作目录（污染 skill / 用户项目）
- 硬编码 `/tmp`、`C:\Temp` 或任何固定路径（不跨平台）
- 每步完成后主动 `rm` / `Remove-Item`（操作系统会清理，属多余 tool call）
- 主动 `os.path.exists()` 检查（其本身即为一次 tool call）
  （`os.makedirs(…, exist_ok=True)` 与 `skill_temp_path.py` 都已隐式建目录，无需另外检查）

### 文件丢失补救

**临时文件可能被操作系统异步清理**，但仍遵循 **乐观调用 + 报错补救**：仅当脚本返回 `FileNotFoundError` 或 `配置文件不存在` 时，使用相同内容、**在相同的 `{系统临时目录}/jeecg-desform/` 路径下重写**（重写前重新调一次 `skill_temp_path.py` 或 `os.makedirs(skill_dir, exist_ok=True)` 确保目录存在），切勿更换路径或回退至 skill 目录。

---

## lowApp 模式（敲敲云 / 零代码模式）

当用户提及以下任一场景时，**必须先阅读 `references/desform-lowapp.md`，再执行任何操作**：

- 用户说「工作表」（而非「表单」）
- 用户说「在 xxx 应用下」「应用里」「某个应用中」
- 用户说「敲敲云」「零代码」「lowApp」
- 用户提到「组织」「租户」（作为操作对象，而非系统权限配置）

lowApp 模式下：
- 表单设计器表单 = **工作表**（概念同，名称不同）
- 需要「组织（租户）+ 应用」两级上下文
- 初始化用 `init_lowapp`，**不是** `init_api`
- 初始化后，`create_form`、`add_widget` 等所有表单操作函数**无需修改**，自动生效
- 详细说明见 `references/desform-lowapp.md`（概念+流程）和 `references/desform-lowapp-utils.md`（函数导入方式与完整说明）

---

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

### API 初始化（统一入口）

所有 Python 操作前都需要先初始化 API 连接。`init_api` 只存在于 `desform_utils.py` 中，其他模块（如 `desform_data_utils.py`）不包含此函数——错误导入会导致 ImportError。

```python
import sys
sys.path.insert(0, r'<skill目录>/scripts')
from desform_utils import init_api
init_api('<api_base>', '<token>')
```

后续按需从各模块导入函数，查阅函数详细说明时：
**先 grep 函数名定位行号，再用 offset+limit 读取对应章节，不要全量阅读文档。**

```bash
# 示例：查 update_design_config 的用法
grep -n "## update_design_config" references/desform-python-utils.md
# 得到行号后：Read 该文件，offset=<行号-1>, limit=40
```

### desform_utils 函数速查表

完整函数列表见 `references/desform-python-utils.md`；列表视图函数见 `references/desform-list-view.md`。

| 函数 | 适用场景 |
|------|---------|
| **表单生命周期** | |
| `check_code_available(code)` | 新建前校验编码唯一性 |
| `create_form(name, code, widgets, ...)` | 一站式创建表单（查找/创建→保存设计→同步权限） |
| `update_form(code, widgets, ...)` | 整体重设计已有表单 |
| `update_design_config(code, config_updates)` | 只改配置不改控件（发布/通知/打印/业务规则等） |
| `query_form(code)` | 查询表单完整信息（含设计JSON） |
| `get_form_fields(form_code)` | 获取所有字段的 model/key/type 映射 |
| **字段级操作** | |
| `add_widget(code, widget_or_widgets)` | 追加字段到已有表单末尾 |
| `update_widget(code, changes, *, key=None, model=None)` | 修改字段属性（优先传 key=） |
| `delete_widget(code, *, key=None, model=None)` | 删除字段（优先传 key=） |
| **设计JSON预处理** | |
| `export_design_json(code, output_path)` | 导出设计JSON到文件（用于手动修改场景） |
| `save_design_from_file(code, file_path)` | 将修改后的文件保存回后台 |
| `extract_field_table_from_design(design_json)` | 从设计JSON提取字段参照表（不调用API） |
| **工具** | |
| `query_dict(dict_code)` | 查询字典项列表 |
| `search_dict(keyword)` | 按名称/编码模糊搜索字典 |
| `gen_menu_sql(parent_name, children, ...)` | 生成菜单和角色授权SQL |

## 主数据复用规则

表单字段配置字典、选人、选部门等数据源时，遵循"先查后建"原则——先查系统是否已有该字典/角色/部门，避免重复创建。

> 使用 `jeecg-system` skill 的 `system_utils.py` 查询和管理主数据，详见  `jeecg-system` 技能。

---

## 创建表单

### 1. 解析用户需求

从用户描述中提取：表单名称、表单编码（英文命名，模块名前缀）、字段列表、字段属性。

**布局选择规则：** 默认使用普通布局（`auto`/`half`/`full`），不要主动使用 Word 风格。只有当用户明确要求时才使用 `layout: "word"`——例如用户说"Word风格"、"表格边框样式"、"像Word文档那样"等。即使表单是审批单、申请表等看起来适合 Word 风格的场景，也不要自行判断使用 Word 风格，而是让用户来决定。

**编码唯一性校验（新建表单时）：**

创建新表单时，生成 `desformCode` 后立即执行编码校验，在校验通过前不要展示摘要让用户确认。原因：用户确认摘要后会期望直接执行成功，如果执行时才发现编码冲突，体验很差，且可能意外覆盖已有表单数据。

```python
from desform_utils import init_api, check_code_available
init_api('<api_base>', '<token>')
result = check_code_available('<code>')  # 只接受 1 个参数
# True → 编码可用  |  False → 已占用，自动换一个编码重试
```

### 2. 识别字段并选择控件类型

根据用户描述的关键词（也可能是图片），匹配对应的控件 type。

> 详见 `references/desform-widget-types.md` — 完整的关键词到控件类型映射表。

对于 radio/select/checkbox 控件，支持静态选项（默认）和系统字典两种数据源。

> 详见 `references/desform-dict-config.md` — 字典配置方式、常用字典编码、Python 快捷函数用法。

对于 table-dict (表字典) 组件时必须阅读 `references/desform-widget-options.md`（搜索 `table-dict`），了解用法和限制后再使用，**强制前提（不可跳过，不可替代）**

**⚠️ 选项颜色强制约束（radio / select / checkbox 的 `itemColor`）：**
系统前端硬编码了 20 个合法颜色值，设置 `itemColor` 时必须严格从这 20 个值中选取，禁止使用任何范围外的颜色（包括视觉上接近的近似色，如 `#FF9800` ≠ `#FF9300`，`#9C27B0` ≠ `#7500EA`，`#F44336` ≠ `#F52222`）。同时必须将 `useColor` 设为 `true`，否则颜色在甘特图/看板视图中不生效。
> 完整颜色表见 `references/desform-widget-options.md` 顶部「选项颜色合法值约束」章节（强制查阅，不可凭记忆填写颜色值）。

对于 select-tree (下拉树) 组件：用户未指定 `categoryCode` 时，直接使用默认值 `"B02"`，**禁止**查询系统分类 API 或向用户询问。

### 3. 展示表单摘要并确认

展示以下内容，等待用户确认后再执行：

```
## 表单摘要
- 表单名称：{name}
- 表单编码：{code}（已通过校验）
- 目标环境：{API_BASE}

### 字段列表
| 序号 | 字段名称 | 控件类型 | 必填 | 说明 |
|------|---------|---------|------|------|
| 1 | ... | ... | ... | ... |

确认以上信息正确？(y/n)
```

### 4. 防覆盖检查

用户确认后、执行创建前，通过 `get_form_id(code)` 检查编码是否已存在。这是防止误覆盖的最后一道安全网——编码校验只检查当前时刻，而从校验到执行之间可能有其他人创建了同编码表单。

如果表单已存在：
1. 告知用户：`表单 {code} 已存在 (ID={id})，是否要覆盖更新？`
2. 用户确认后才执行覆盖（调用 `update_form`）
3. 用户拒绝覆盖时，基于原编码生成 3~5 个新编码供选择

### 5. 生成 JSON 并调用 API

使用 `scripts/desform_creator.py` + JSON 配置文件创建表单。这个脚本封装了完整的 JSON 构造逻辑（控件包裹、key/model 生成、跨控件引用等），比手动拼 JSON 更可靠，也更不容易出错。

**⚡ 预处理优先原则（存在创建后需要修改的属性时）：**

执行创建前，先判断是否存在 JSON config **无法直接配置**、但需要创建后额外操作的属性，常见场景包括：

- 字段默认隐藏（`hidden: true`）—— JSON config 不支持此参数
- 业务规则（`bizRuleConfig`）
- JS / CSS 增强代码
- 控件深层嵌套属性的精确修改

如果存在以上任一需求，**优先使用 `--preprocess` 模式**，在一次创建流程内完成所有修改，避免创建后再调用 `update_widget` / `update_design_config` 等额外步骤。

> 详见本文档「设计 JSON 预处理 → 场景一：创建表单时预处理」章节。

⛔ **执行前必须判断字段数量，选择正确方式——禁止在字段数 ≤50 时使用临时文件：**

**默认方式：常规表单（≤50 个字段）** → stdin 管道，一条命令完成，无需临时文件：
```bash
echo '<json_config>' | python "<skill目录>/scripts/desform_creator.py" --api-base <URL> --token <TOKEN> --config -
```

**仅当字段 >50 时** → 临时文件方式，避免管道传输大量数据时的稳定性问题：
1. 根据「临时配置文件规则（强制）」章节，将 JSON 配置写到 `{系统临时目录}/jeecg-desform/<表名>_create.json`
2. 执行脚本：`python "<skill目录>/scripts/desform_creator.py" --api-base <URL> --token <TOKEN> --config <config.json>`
3. **不要**主动删除该文件，操作系统会自动清理

> 详见 `references/desform-json-config.md` — JSON 配置格式、字段定义、子表说明、完整示例。

**脚本自动处理的跨控件引用：**
- **capital-money（大写金额）**：优先通过 JSON 中的 `moneyField`（字段中文名）解析关联目标，未指定时兜底查找前面最近的 `money`/`formula`/`summary` 控件。当大写金额与目标字段不相邻时，必须显式传入 `moneyField`
- **summary（汇总）**：`linkTable`（子表中文名）和 `field`（子表列中文名）自动解析为实际 model；`filter.rules` 中的 `field` 也支持中文名自动解析
- **formula（公式）表达式**：支持使用字段中文名作为占位符（如 `$预算总额$`），自动解析为实际 model
- **Word 布局下的 divider（分隔符）**：自动包裹在 `span=24`、`isWordStyle=true` 的 grid 容器中

> 脚本已自动处理 JSON 结构规则（card 容器、key/model 生成、className/icon、控件跨引用等）。如需排查或手动构造，详见 `references/desform-design-json-schema.md`。

> **多表互相关联场景**（2+ 个表单通过 link-record 互相引用）：阅读 `references/desform-cross-form-binding.md`，采用"先建表后关联"策略。

**降级方案：** 如果脚本执行失败，先向用户说明失败原因，经用户确认后可降级为手动构造 JSON。
> 详见 `references/desform-fallback-manual-json.md` — 手动构造 desformDesignJson 的完整指南。

### 6. 检查结果与权限

- `success: true` → 表单创建成功，脚本会自动创建字段权限
- `success: false` → 输出错误信息，参见 `references/desform-api-notes.md` 错误处理表
- 权限创建失败不会阻断主流程（仅输出警告），可用 `scripts/desform_auth_retry.py --api-base <URL> --token <TOKEN> --code <form_code>` 重试

### 7. 输出结果

```
## 表单创建成功
- 表单ID：{id}
- 表单名称：{desformName}
- 表单编码：{desformCode}
- 目标环境：{API_BASE}

请在表单设计器中查看：打开 JeecgBoot 后台 → 表单设计器 → 找到该表单
```

同时输出菜单 + 角色授权 SQL（用于将表单设计器加入系统菜单）。

> 详见 `references/desform-menu-sql.md` — gen_menu_sql 调用方式、输出格式、SQL 字段说明、本地自动执行规则。

当 `api_base` 以 `http://127.0.0.1` 或 `http://localhost` 开头时，通过 MySQL CLI 自动执行菜单 SQL。

---

## 更新已有表单

所有更新相关的函数详见 `references/desform-python-utils.md`。

### 更新流程

1. 获取现有表单信息：`get_form_fields(code)`
2. 分析用户需求，确定操作类型（添加/修改/删除/整体重设计）
3. 展示变更摘要（新增/修改/删除的字段列表），等待用户确认
4. 执行操作
5. 自动同步权限

### 整体重设计

如果用户要全面修改已有表单：
1. 查询现有表单设计 JSON：`query_form(code)` 或 `get_form_fields(code)`
2. 根据用户需求重新组装控件列表
3. 调用 `update_form(code, new_widgets)` 保存（自动获取 `updateCount`）

### 字段级操作

如果用户只是添加/修改/删除个别字段：
- **添加字段**：`add_widget(code, widget)` — 向已有表单追加控件
- **修改字段属性**：`update_widget(code, changes_dict, *, key=None, model=None)` — 修改指定控件属性，优先传 `key=`
- **删除字段**：`delete_widget(code, *, key=None, model=None)` — 删除指定控件，优先传 `key=`
- 操作后自动同步权限：`sync_auth(code, design_list, form_id)`

---

## 设计 JSON 预处理

当脚本能力不足以满足需求时（例如创建后还需要精确修改某个控件的嵌套属性），可以使用预处理模式——让脚本把生成的设计 JSON 输出到临时文件，AI 用文本工具手动修改后再统一保存。

### 场景一：创建表单时预处理

正常创建命令加 `--preprocess` 参数（管道符和临时文件方式均支持）：

```bash
echo '<json_config>' | python "<skill目录>/scripts/desform_creator.py" \
    --api-base <URL> --token <TOKEN> --config - --preprocess
```

脚本会：
1. 在后台创建表单实体（获得 form_id），但**跳过**保存设计 JSON
2. 将生成的设计 JSON 写入临时文件（格式化缩进）
3. 打印所有字段的标题 / key / model 参照表

AI 使用 Read/Edit/Write 工具修改临时文件，完成后调用保存：

```python
from desform_utils import init_api, save_design_from_file
init_api('<api_base>', '<token>')
save_design_from_file('<form_code>', r'<临时文件路径>')
```

### 场景二：修改已有表单时预处理

```python
from desform_utils import init_api, export_design_json, save_design_from_file
init_api('<api_base>', '<token>')

# 1. 导出当前设计 JSON，同时打印字段参照表
file_path, field_rows = export_design_json('<form_code>')

# 2. 使用 Read/Edit/Write 工具修改 file_path 中的内容

# 3. 保存修改后的设计 JSON
save_design_from_file('<form_code>', file_path)
```

---

## 复制表单

`copy_form(source_code, new_code)` 可快速复制已有表单的设计 JSON 创建新表单。适用于基于现有表单创建类似表单（如复制"请假申请"改造为"出差申请"）。

流程：
1. 用户提供源表单编码和新表单编码
2. 校验新编码可用性（`check_code_available(new_code)`）
3. 调用 `copy_form(source_code, new_code)` 完成复制
4. 如需修改，使用 `update_form` 或字段级操作调整

## 删除表单

`delete_form` 已封装完整的删除流程（查找 → 逻辑删除 → 物理删除），支持传 code 或 ID。

> 详见 `references/desform-api-notes.md` — 删除流程、注意事项。

## 视图类型说明（消歧）

desform 有两种完全独立的视图概念：

| 类型 | 控制内容 | 触发关键词 |
|------|---------|-----------|
| **列表视图** | 数据记录在列表页如何展示（表格/看板/日历/甘特图） | 用户直接说"视图"、"新建视图"、"看板"、"日历"、"甘特图"等 |
| **表单视图** | 填报表单时字段的布局和显示方式（PC/移动端） | 用户明确说"表单视图"、"移动端视图"、"移动视图" |

**默认规则：用户说"视图"时，默认理解为列表视图。只有明确提到"表单视图"或"移动视图/移动端视图"时，才处理表单视图。**

---

## 列表视图

列表视图控制数据记录在列表页的展示方式，支持四种类型：

| 类型 | 说明 | 必要配置 |
|------|------|---------|
| **表格** | Table 组件逐行显示，最常规 | 无 |
| **看板** | 按字段值分列展示卡片（也称卡片视图） | 分组字段（限单选/下拉/人员/表字典/关联记录单条） |
| **日历** | 数据挂载到日历显示 | 至少 1 个日期字段；可选开始+结束；可多组 |
| **甘特图** | 时间线任务展示 | 1 个开始日期 + 1 个结束日期（均必填） |

> **注意：创建表单时系统会自动生成一个默认的表格列表视图，无需主动调用视图创建方法。只有用户明确要求"创建看板"、"添加日历视图"、"新增甘特图"等时，才需要操作列表视图。**

> 详见 `references/desform-list-view.md` — 各视图类型字段规则、操作方式

---

## 表单视图

创建表单视图（PC 表单视图、移动端表单视图）时，优先使用 `scripts/desform_view_creator.py` 通用脚本，支持复制主表单视图或自定义字段两种模式。

> 详见 `references/desform-view-config.md` — 创建流程、JSON 配置格式、移动端优化规则、踩坑汇总。

## 自定义动作（自定义按钮 + 自定义规则）

> 当用户说"自定义按钮"、"添加按钮"、"视图按钮"、"自定义动作"、"zdyan"、"删除规则"、"控制删除"时触发本章节。

自定义动作包含两类：
- **自定义按钮**：通过独立的 `/desform/button/*` API 管理
- **自定义规则**：目前只有**删除规则**，通过 `PUT /desform/view/updateViewConfig` 的 `customRules` 字段配置，控制用户能否删除记录

> 详见 `references/desform-custom-button.md` — 删除规则完整结构与示例、自定义按钮数据结构、三种动作模式、显示条件、颜色预设、API 列表、Python 用法、工作流关联说明。

**操作流程：**

1. 查询已有按钮（`list_buttons`），了解当前配置
2. 展示变更摘要，等待用户确认
3. 调用相应函数执行（函数列表见 `references/desform-custom-button.md` 的"Python 工具函数"章节）

**关于工作流（重要）：**

- `clickThen='form'` + `flowStatus=False`：**完全可以纯 API 完成**，无需工作流
- `clickThen='execute'` 或 `'confirm'`（必须触发工作流）：创建按钮后会得到 `processId`，工作流节点内容需同时使用 **`jeecg-lowcode-miniflow` 技能**配置

---

## 功能开关（零代码应用专属）

> **触发场景**：当用户在零代码应用（工作表）语境下，说到以下任意情况时，立即阅读 `references/desform-switch-setting.md`：
>
> - **控制某功能是否显示/可用**：「不让用户创建记录」「隐藏创建按钮」「禁用导入」「关掉批量操作」「关闭批量删除」「关闭分享」「禁止下载附件」「隐藏评论」「禁用打印」
> - **限制使用范围**：「只有管理员才能 XX」「XX 功能只在某个视图显示」「限制某功能的可见范围」
> - **直接说功能开关**：「功能开关」「开关设置」「switchSetting」
>
> **注意**：功能开关仅在**零代码应用的工作表**中存在，普通表单设计器没有此功能。函数位于 `desform_lowapp_utils`，需 `init_lowapp` 初始化（非 `init_api`）。

**操作流程：**

1. 阅读 `references/desform-switch-setting.md`，确认目标 code 和配置值
2. 调用 `get_switch_settings(code)` 查看当前状态（可选，直接构造也可）
3. 构造配置对象，注意父子联动规则（`BATCH_ACTION` 变更时需同时传所有子级）
4. 调用 `save_switch_settings(code, items)` 保存（函数导入方式见 `references/desform-lowapp-utils.md`，需 `init_lowapp` 初始化）

---

## 表单数据操作（CRUD）

对已有表单进行数据新增、查询、编辑、删除。

> 详见 `references/desform-data-utils.md` — 函数导入方式、完整函数列表和用法。

**数据新增流程：**
1. 先获取字段 model 映射：`get_form_fields(code)` 返回 `(titleField, {字段名: {model, key, type}, ...})`
2. 构造数据字典：key 为字段的 `model`（如 `input_1774607211242_327900`），value 为字段值
3. 调用 `add_data(code, data_dict)` 提交

## 错误处理

> 详见 `references/desform-api-notes.md` — 完整错误处理表。

---

## OA 审批应用一键生成（表单 + 流程 + 授权）

> 当用户说"创建审批单"、"创建报销单"、"做一个OA表单带流程"、"面试申请"、"请假申请"等，**立即阅读 `references/desform-oa-guide.md`**，其中包含完整的交互流程（Step 0–2）、JSON 配置格式、OA 专用字段类型、审批人类型、流程分支规则和常见模板。

---

## 参考文档

### OA 审批应用

- `references/desform-oa-guide.md` — OA 一键生成完整指南：交互步骤、JSON 配置格式、OA 专用字段类型、审批人类型、流程分支规则、常见模板（费用报销/请假/采购/出差）

### 脚本工具

| 脚本 | 用途 |
|------|------|
| `scripts/desform_creator.py` | 通用表单创建脚本，优先使用 |
| `scripts/desform_view_creator.py` | 通用表单视图创建脚本（PC/移动端） |
| `scripts/desform_utils.py` | 共通工具库（控件工厂、API 封装、布局引擎、字段权限） |
| `scripts/desform_data_utils.py` | 数据操作工具库（CRUD、批量、回收站） |
| `scripts/desform_auth_retry.py` | 字段权限重试（仅权限自动创建失败时使用） |
| `scripts/desform_button_utils.py` | 自定义按钮操作工具库（增删改查、视图绑定、排序） |
| `scripts/skill_temp_path.py` | 跨平台获取本技能临时目录/文件路径（写临时配置前必先调用，自动建目录） |

### 创建/更新表单时阅读

- `references/desform-json-config.md` — JSON 配置格式、字段定义、子表说明、完整示例
- `references/desform-widget-types.md` — 用户描述关键词 → 控件 type 映射表
- `references/desform-dict-config.md` — 字典数据源配置（静态选项、系统字典、Python 用法）
- `references/desform-python-utils.md` — desform_utils.py 使用指南、快捷函数、layout 参数
- `references/desform-api-notes.md` — API 踩坑记录、错误处理、命名规则
- `references/desform-menu-sql.md` — 菜单 SQL 生成、字段说明、本地自动执行

### 高级功能（按需阅读）

- `references/desform-link-record.md` — 涉及关联记录 + 他表字段时阅读
- `references/desform-self-tree.md` — 涉及**表单数据树**（自关联树）时阅读：当用户说"自关联"、"数据树"、"自引用树"、"父子记录"、"关联自身"、"关联自己"、"上级记录"、"父节点字段"、"无限级分类"等，必须先阅读此文档再配置
- `references/desform-cross-form-binding.md` — 多表单互相关联时阅读（跨表 link-record/isSubTable/link-field/twoWayModel）
- `references/desform-sub-table-types.md` — 涉及子表时阅读（内部子表 vs 外部子表）
- `references/desform-formula-function.md` — 涉及公式计算时阅读（内置函数库、自定义 JS 函数、日期计算）
- `references/desform-default-value.md` — 涉及默认值时阅读（compose/function/javascript/linkage 四种类型）
- `references/desform-context-vars.md` — 涉及上下文变量（{{sysUserCode}} 等）时阅读（完整变量列表、支持位置、JSON/Python 用法）
- `references/desform-fill-rule.md` — 涉及填值规则（fillRuleCode）时阅读（触发时机、完全只读、动态触发 JS 写法；**规则 Code 必须用户提供，禁止猜测**）
- `references/desform-validation-rules.md` — 涉及校验规则时阅读（rules/defaultRules/pattern/unique）
- `references/desform-option-datasource.md` — 涉及选项数据源时阅读（静态/系统字典/关联表单/远程函数）
- `references/desform-remote-api.md` — 涉及远程API取值（remoteAPI）时阅读（动态参数语法、${字段model}传参、返回值规则、触发时机）
- `references/desform-js-enhance.md` — 涉及 JS 增强时阅读（自定义 JavaScript、API 方法、事件监听）
- `references/desform-layout.md` — 涉及布局模式时阅读（auto/half/full/word 四种模式的说明和适用场景）
- `references/desform-css-enhance.md` — 涉及 CSS 增强时阅读（自定义样式、Word 风格定制）
- `references/desform-layout-controls.md` — 涉及复杂布局时阅读（AutoGrid/Card/Grid/Tabs）
- `references/desform-linkage-query.md` — 涉及查询工作表时阅读（linkage 类型默认值）
- `references/desform-online-binding.md` — 涉及关联 Online 表单时阅读（字段映射/子表/数据同步）
- `references/desform-external-link.md` — 涉及外链表单时阅读（公共填报、免登录访问、外链授权管理）
- `references/desform-filter-rules.md` — **【强制】构建任何含 `rule` 字段的条件对象前必须阅读**（合法 rule 值列表、按字段类型分类、错误写法对照、conditionsGroup 完整字段说明）
- `references/desform-list-view.md` — 涉及列表视图时阅读（表格/看板/日历/甘特图类型说明、字段规则）
- `references/desform-api-docs/list-view.md` — 列表视图完整 API 文档（addView/updateViewConfig/排序/删除等所有接口）
- `references/desform-super-query.md` — 涉及筛选条件（高级查询）时阅读；触发关键词：「筛选条件」「高级查询」「superQuery」，**但需注意**：用户在创建/配置视图语境下说「筛选条件」「添加条件」时，应使用数据过滤（`config_view_data_filter`）而非本文档
- `references/desform-custom-button.md` — 涉及自定义按钮/自定义动作时阅读（数据结构、三种动作模式、显示条件、API、Python 用法、工作流关联）
- `references/desform-view-config.md` — 涉及表单视图时阅读（JSON 配置、移动端优化、踩坑汇总）
- `references/desform-custom-receive-url.md` — 涉及自定义接收URL时阅读（接口规则、事务控制、子表数据处理、Java示例）
- `references/desform-biz-rules.md` — 涉及业务规则时阅读（`bizRuleConfig` 完整结构、条件操作符枚举、动作类型枚举、原始属性联动陷阱、与 filter-rules 的差异）；触发关键词：「业务规则」「联动」「满足条件时」「显示隐藏条件」「必填条件」「锁定记录」`bizRuleConfig`
- `references/desform-release-setting.md` — 涉及发布设置/外部链接时阅读（字段说明、URL格式、`externalTitle` 特殊值处理）；触发关键词：「发布设置」「外部链接」「公开链接」「二维码」「allowExternalLink」「页眉图片」「headerImgUrl」
- `references/desform-notice-setting.md` — 涉及填报通知时阅读（`noticeType` 枚举值、`noticeReceiver` 格式、校验规则）；触发关键词：「填报通知」「新增通知」「提交通知」「enableNotice」「noticeType」「通知接收人」
- `references/desform-print-setting.md` — 涉及打印设置时阅读（字段联动关系、积木报表集成）；触发关键词：「打印」「打印设置」「allowPrint」「积木报表」「jmReport」「disabledAutoGrid」
- `references/desform-switch-setting.md` — **零代码应用专属**，涉及功能开关时阅读（14个开关的完整配置、父子联动规则、viewAuth 约束、Python 示例）；触发关键词：「功能开关」「显示创建按钮」「禁用批量操作」「导入功能」「记录分享」「记录讨论」「附件下载」「记录日志」；函数导入方式见 `references/desform-lowapp-utils.md`

### 降级/排障

- `references/desform-fallback-manual-json.md` — 脚本失败时手动构造 JSON 的完整指南
- `references/desform-design-json-schema.md` — JSON Schema 结构、控件类型清单、通用字段
- `references/desform-widget-options.md` — 每种控件的完整 options 配置

### 示例参考

- `references/desform-examples.md` — 常见表单模式示例 + Python 脚本模板
- `references/desform-real-samples.md` — 真实业务表单案例（字典、半行、分区、公式、关联）
