---
name: jeecg-onlform
description: >-
  JeecgBoot Online表单（cgform）全生命周期管理——通过API自动创建/编辑数据库表和表单配置，
  支持单表、主子表、树表，26种控件类型，以及JS/Java/SQL增强、权限配置、数据CRUD、积木报表集成。
  只要用户意图涉及「Online表单」就必须使用本技能，包括但不限于：
  创建或配置数据库表（"建一张请假表"、"创建online表"、"做一个带下拉选择的表"、"低代码表单"、"在线表单"、"配置表"）、
  修改已有Online表字段（"加个字段"、"改字段类型"、"加子表"、"删除字段"）、
  配置表单增强（"JS增强"、"自定义按钮"、"表单联动"、"Java增强"、"SQL增强"）、
  配置权限（"字段权限"、"按钮权限"、"数据权限"、"授权给角色"）、
  管理表单数据（"插入数据"、"查询记录"、"导出CSV"、"造测试数据"）、
  以及关联积木报表（"给这个表加报表"、"集成打印"）。
  即使用户只描述了业务需求而没说"online"（如"做一个员工信息管理功能，包含姓名、部门下拉、入职日期"），
  只要涉及元数据驱动的表单配置，也应触发本技能。
  注意：不要与「设计器表单」(desform)混淆——desform是拖拽式表单设计器，用skill jeecg-desform处理；
  也不要与「Online报表」(cgreport)或「Online图表」(onlchart)混淆——它们是SQL驱动的只读展示。
---

# JeecgBoot Online 表单 AI 自动生成器

将自然语言的表单需求描述转换为 Online 表单配置 JSON，并通过 API 在 JeecgBoot 系统中自动创建/编辑表单。

> **重要：本 skill 处理「Online 表单」（元数据驱动，运行时 CRUD），不涉及「设计器表单」（desform）。两者是完全独立的表单体系。**

## 选择正确的技能

| 用户需求 | 应使用的技能 |
|---------|------------|
| 元数据驱动的表/表单配置（字段定义、控件类型、数据库建表） | **本技能 (jeecg-onlform)** |
| 拖拽式可视化表单设计（自由布局、表单设计器） | jeecg-desform |
| SQL查询结果以**列表**展示 | jeecg-onlreport |
| SQL查询结果以**图形**展示（柱状图/饼图/折线图） | jeecg-onlchart |
| 复杂Excel样式报表（打印、分组、循环） | jimureport |

## 目录结构

```
scripts/
├── onlform_creator.py      # 表单创建/编辑（单表/主子表/树表）
├── onlform_jimureport.py   # 积木报表集成（创建/删除报表并关联）
├── onlform_enhance.py      # JS/Java/SQL增强 + 自定义按钮
├── onlform_auth.py         # 权限配置（字段/按钮/数据权限）
├── onlform_data.py         # 数据 CRUD（增删改查/树数据/导出CSV）
└── onlform_menu.py         # 菜单挂载 + 路由缓存 + 角色授权

references/
├── onlform-field-types.md  # 字段类型/控件/字典/校验/默认值/扩展配置
├── onlform-enhance.md      # JS/Java/SQL增强参考 + 自定义按钮
├── onlform-auth.md         # 权限配置（字段/按钮/数据权限 API）
├── onlform-data-crud.md    # 数据 CRUD API + 存储格式
├── onlform-jimureport.md   # 积木报表集成 8 步流程
├── onlform-misc.md         # 杂项：表类型/布局/BPM/视图/错误处理
├── onlform-api-reference.md # 完整 JSON 数据结构和字段枚举
└── onlform-route-cache.md  # 路由缓存配置（动态/静态路由、组件名称映射）
```

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

## 执行效率规则（减少无谓等待）

所有 HTTP 调用必须遵循，否则用户会感到响应明显变慢。**本节为强制要求，违反会直接被用户吐槽"太慢了"。**

### 0. Windows 环境下**必须**用 PowerShell tool 跑 python（最容易踩的坑）

**现象**：Windows 的 Bash tool 会把 `python` / `python -c` / skill 脚本当作长命令自动 `run_in_background`，tool 立即返回一个 background ID，真正的执行输出要等系统通知才到——把毫秒级调用放大到数秒，用户会立即感到"卡"。

**规则**：
- **Windows（platform=win32）** → 所有 python 调用（skill 脚本 + `python -c` 探测）都用 **PowerShell tool**，不要用 Bash tool。
- **Linux / macOS（platform=linux/darwin）** → 用 Bash tool 即可，python 不会被后台化。
- `curl` 在任何平台都不用——跨平台不一致，且 Windows Bash 下同样被后台化。

**Windows 正确示例**：
```
PowerShell: python C:/path/to/onlform_creator.py --api-base http://localhost:8080 --token xxx --config config.json
PowerShell: python -c "import urllib.request as u, json; r=u.urlopen(...); print(r.read().decode())"
```

**Windows 错误示例**（会被后台化）：
```
Bash: python onlform_creator.py ...       ← 会返回 "Command running in background"
Bash: python -c "..."                     ← 同上
Bash: curl -X POST ...                    ← 同上
```

> **历史教训**：本 skill 早期版本错误地声称"Python 在所有 shell 下都同步返回"——实测 Windows Bash tool 对 python 也会后台化。曾因此被用户连续吐槽"执行太慢了"。

### 1. 优先用 skill 自带的 Python 脚本，不要自己另起 HTTP 封装

skill 已提供 `onlform_creator.py` / `onlform_jimureport.py` 等脚本，它们封装了鉴权、重试、head 解析、主子表关联等细节。需要一次性 HTTP 探测再用 `python -c`。

### 2. 跳过非必要前置检查，直接跑脚本

- **表名查重**：仅在"用户暗示要复用已有表 / 表名看上去像已有资源"时才查。普通新建场景直接跑 `onlform_creator.py`——遇重名接口会返回明确错误，预查反而增加一次往返。
- **字典存在性**：`sex`/`yn`/`sys_status` 等内置字典直接用，不必查。仅在字典编码明显是业务自定义且不确定是否创建过时才 `sys/dict/list` 查。
- **link_table 引用表存在性**：这项仍然必须查（见 `references/onlform-field-types.md`），引用不存在的表会让创建成功但运行时报错，排查成本高。

### 3. 并行多个 GET 检查时，一个 Python 调用里顺序打完，不要拆成多条 shell

一次 tool call 拿到所有结果；拆成多条 shell 既有进程启动开销，在 Windows 下还会被后台化。
```python
# 用 PowerShell tool 跑
python -c "
import urllib.request as u, json
h = {'X-Access-Token':'<token>'}; base = 'http://host'
def g(p): return json.loads(u.urlopen(u.Request(base+p, headers=h), timeout=10).read())
dup = g('/sys/duplicate/check?tableName=onl_cgform_head&fieldName=table_name&fieldVal=xxx')
dct = g('/sys/dict/list?dictCode=xxx')
print('dup=', dup.get('result'), '; dict.total=', dct.get('result', {}).get('total'))
"
```

### 4. API base 确认（避免"路径不存在"返工）

JeecgBoot 后端的 context path 因部署而异：
- 较老版本 / 标准部署：`http://host:port/jeecg-boot`
- 较新版本 / 根路径部署：`http://host:port`（无 `/jeecg-boot` 后缀）

**首次不确定时**：直接按用户给的原样用。如果 `onlform_creator.py` 返回 `"路径不存在，请检查路径是否正确"`，去掉 `/jeecg-boot` 重试一次（或反之）——这个错误是确定性的，不要改别的参数。

### 5. 建表遇到「数据库表 [xxx] 已存在」时的处理

错误 `数据库表[xxx]已存在,请从数据库导入表单` 表示：**物理 DB 表残留，但 Online 配置不存在**（通常是之前创建后被手动删了 Online 头）。应对策略：

1. **首选：换表名**（如 `order_main` → `sale_order`）——最快，避免污染现有物理表和数据。
2. **次选：导入**：`GET /online/cgform/head/transTables/{tableName}` 把物理表导入为 Online 配置，再用 `action=edit` 调整字段。
3. **慎用：删除物理表**（通过 DB 直连 DROP TABLE）——只在确认无数据且用户明确要求时做。

> **主子表场景特别注意**：主表建失败后，子表如果已创建会成为"孤儿"（外键指向不存在的父表头）。此时必须先 `DELETE /online/cgform/head/delete?id={孤儿子表headId}` 删干净，再用新表名整体重建。不要在孤儿子表基础上继续操作。

## 主数据复用规则

> **重要：** 配置表单字段的字典、用户选择、部门选择等数据源时，必须遵循"先查后建"原则。
> 使用 `jeecg-system` skill 的 `system_utils.py` 查询和管理主数据。

## 交互流程

### Step 0: 判断操作类型

| 用户意图关键词 | 操作类型 | 使用脚本 |
|---------------|---------|---------|
| 创建/新建/做一个/生成 | 新增表单 → Step 1A | `onlform_creator.py` |
| 加字段/增加字段/修改字段/删除字段 | 编辑表单 → Step 1B | `onlform_creator.py` |
| 集成积木/关联打印/打印报表 | 积木报表集成 → Step 8 | `onlform_jimureport.py` |
| JS增强/按钮/增强功能 | 增强配置 → Step 9 | `onlform_enhance.py` |
| 权限/授权/数据规则 | 权限配置 → Step 10 | `onlform_auth.py` |
| 造数据/插入/查询/导出 | 数据操作 → Step 11 | `onlform_data.py` |
| 挂载菜单/加到菜单/预览地址/缓存路由 | 菜单挂载 → Step 12 | `onlform_menu.py` |

### Step 1A: 新增表单 — 解析需求

从用户描述中提取：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 表名 (tableName) | 自动生成 snake_case | `leave_application` |
| 表描述 (tableTxt) | 用户指定 | "请假申请" |
| 表类型 (tableType) | 1=单表 | 提到"主子表"→2/3，提到"树形"→1+isTree |
| 字段列表 | 从描述中解析 | 姓名(必填)、请假天数(数字)、日期(范围查询) |

**判断表类型：**
- 提到"分类/层级/树/上下级" → **树表** (tableType=1, isTree='Y')
- 提到"主子表/明细/一对多/订单+商品" → **主子表** (主表 tableType=2, 子表 tableType=3)，**默认使用 normal 风格**（不使用 erp），除非用户明确指定
- 默认 → **单表** (tableType=1)

> **创建前不要查重表名。** `addAll` 接口本身会校验并返回明确的重复提示，提前查重是多余的网络开销。
>
> **遇到重名错误（`数据库表[xxx]已存在`）时的处理规则：**
>
> | 当前操作 | 处理方式 |
> |---------|---------|
> | **新建表单**（用户意图是创建一个新表） | **自动加后缀重试**：`xxx` → `xxx_1` → `xxx_2` …，直到成功；执行成功后告知用户实际使用的表名 |
> | **修改/编辑表单**（用户意图是改已有表） | 切换到 editAll 流程 |
> | **导入数据库已有表** | 调用 `transTables/{tableName}` 导入 |
>
> ❌ **绝对不能删除已有表**（`DELETE /online/cgform/head/delete`）来"让位"给新建——这会丢失已有数据和配置。删除只能在用户**显式要求**删除时执行。

**字典字段配置易错点（必须注意）：**
- **下拉框/多选框/单选框/下拉多选/下拉搜索 这 5 种控件必须配置数据字典或表字典**，否则没有选项无法使用。生成字段配置时，遇到这 5 种控件必须同时配置 dictField（数据字典）或 dictTable+dictField+dictText（表字典）。
- 数据字典（系统字典/字典编码）：只填 `dictField`（字典编码，如 `sex`、`education`），`dictTable` 和 `dictText` 留空。**绝对不能**把 `dictTable` 设为 `sys_dict_item`。
- 表字典：`dictTable` 填业务表名（如 `sys_user`，也可以填 Online 创建的表），`dictField` 填存储值字段，`dictText` 填显示文本字段。
- 使用的字典编码不存在时，需先通过 `sys/dict/list?dictCode=xxx` 查询，不存在则通过 `sys/dict/add` + `sys/dictItem/add` 创建（先查后建）。

### Step 1B: 编辑表单 — 查询现有配置

1. 用户提供表单 ID 或表名
2. 查询表名获取 headId：`GET /online/cgform/head/list?tableName={表名}&pageNo=1&pageSize=1`
3. 查询现有字段列表展示给用户
4. 根据用户需求进行增/删/改字段

### Step 2-4: 智能字段推导

> **详细字段类型映射、字典配置、校验规则、默认值、扩展配置、特殊控件配置参见：**
> `references/onlform-field-types.md`

> **⚠️ link_table（关联记录）前置检查（必须执行）：**
> 配置 `link_table` 字段时，`dictTable` 只能引用 **Online 管理的业务表**，不能是系统表。
> 必须先调用 `GET /online/cgform/head/list?tableName={表名}&pageNo=1&pageSize=1` 验证被关联表是否存在。
> - 若不存在 → 先创建该 Online 表并同步数据库，再插入至少 3 条示例数据，然后再配置 link_table 字段。
> - 若已存在 → 直接配置。
> 详细说明见 `references/onlform-field-types.md` 的 `link_table` 小节。

核心映射速查：

| 关键词 | fieldShowType | dbType |
|--------|-------------|--------|
| 文本 | `text` | string |
| 备注 | `textarea` | string |
| 日期 | `date` | Date |
| 下拉 | `list` | string |
| 单选 | `radio` | string |
| 多选 | `checkbox` | string |
| 开关 | `switch` | string |
| 图片 | `image` | string |
| 文件 | `file` | string |
| 用户选择 | `sel_user` | string |
| 部门选择 | `sel_depart` | string |
| 省市区 | `pca` | string |
| 富文本 | `umeditor` | Text |

### Step 5: 展示摘要并确认

**必须展示配置摘要，等待用户确认后再执行。** 这一步至关重要——字段配置一旦创建后修改成本较高（需要逐个编辑），提前确认能避免返工。摘要需包含：
- 表名、表描述、表类型
- 6 个标准系统字段
- 所有业务字段（序号、字段名、标签、控件类型、DB类型、必填、查询、字典）
- 合计字段数

### Step 6-7: 生成配置 JSON 并调用脚本

**使用 `scripts/onlform_creator.py`（推荐方式）：**

```bash
python <skill目录>/scripts/onlform_creator.py --api-base <URL> --token <TOKEN> --config <config.json>
```

**单表创建 JSON 示例：**
```json
{
  "action": "create",
  "tables": [{
    "tableName": "leave_application",
    "tableTxt": "请假申请表",
    "tableType": 1,
    "fields": [
      {"dbFieldName": "name", "dbFieldTxt": "姓名", "fieldShowType": "text", "dbType": "string", "dbLength": 100, "fieldMustInput": "1", "isQuery": 1}
    ]
  }]
}
```

**编辑表单 JSON 示例：**
```json
{
  "action": "edit",
  "tableName": "test_demo",
  "addFields": [{"dbFieldName": "new_field", "dbFieldTxt": "新字段", "fieldShowType": "text", "dbType": "string", "dbLength": 100}],
  "deleteFields": ["old_field"],
  "modifyFields": [{"dbFieldName": "existing_field", "dbFieldTxt": "修改后标签", "dbLength": 200}]
}
```

> **主子表、树表的完整 JSON 配置示例参见：** `references/onlform-misc.md`

### Step 8: 积木报表集成

**使用 `scripts/onlform_jimureport.py`：**

```bash
python <skill目录>/scripts/onlform_jimureport.py --api-base <URL> --token <TOKEN> --config <config.json>
```

**配置 JSON 示例：**
```json
{
  "action": "create_report",
  "tableName": "customer",
  "reportName": "客户表打印",
  "fields": [
    {"fieldName": "customer_name", "fieldText": "客户名称"},
    {"fieldName": "phone", "fieldText": "联系电话"}
  ]
}
```

脚本自动完成 8 步：创建报表 → 保存空模板 → 解析字段 → 检查编码 → 保存数据源 → 获取模板 → 写入引用 → 关联表单。

> **前提条件**：Online 表中至少存在一条记录，否则字段解析不出来。
> **积木报表 API 详细说明参见：** `references/onlform-jimureport.md`

### Step 9: 增强配置

**使用 `scripts/onlform_enhance.py`：**

```bash
python <skill目录>/scripts/onlform_enhance.py --api-base <URL> --token <TOKEN> --config <config.json>
```

支持的操作：
- `create_buttons` — 创建自定义按钮（button/link/form 样式）
- `save_js` — 保存 JS 增强（form/list 类型）
- `save_java` — 保存 Java 增强（spring-key/java-class/http-api）
- `save_sql` — 保存 SQL 增强
- `query` — 查询所有增强配置

> **JS/Java/SQL 增强完整参考参见：** `references/onlform-enhance.md`

### Step 10: 权限配置

**使用 `scripts/onlform_auth.py`：**

```bash
python <skill目录>/scripts/onlform_auth.py --api-base <URL> --token <TOKEN> --config <config.json>
```

支持的操作：
- `setup_field_auth` — 配置字段权限（列表可见/表单可见/表单可编辑）
- `setup_button_auth` — 配置按钮权限
- `setup_data_auth` — 配置数据权限规则
- `grant_role` — 授权给角色/部门/用户
- `query` — 查询所有权限配置

> **权限配置详细参考参见：** `references/onlform-auth.md` 和 `references/onlform-misc.md`

### Step 11: 数据操作

**使用 `scripts/onlform_data.py`：**

```bash
python <skill目录>/scripts/onlform_data.py --api-base <URL> --token <TOKEN> --config <config.json>
```

支持的操作：
- `insert` — 插入数据（单表/主子表）
- `insert_tree` — 插入树表数据（自动父先子后）
- `query` — 查询数据列表（带过滤）
- `query_tree` — 查询树表数据
- `get` — 查询单条记录
- `update` — 更新记录（自动全量合并）
- `delete` — 删除记录
- `export_csv` — 导出 CSV

> **数据 CRUD API 和存储格式详细参考参见：** `references/onlform-data-crud.md`

---

## 所有脚本通用参数

| 参数 | 说明 |
|------|------|
| `--api-base` | JeecgBoot 后端地址（如 `http://localhost:8080/jeecg-boot`） |
| `--token` | X-Access-Token |
| `--config` | JSON 配置文件路径 |

所有脚本支持 `tableName` 自动解析 `headId`，无需手动查询。

## 参考文档索引（按需读取）

| 文档 | 何时读取 |
|------|---------|
| [onlform-field-types.md](references/onlform-field-types.md) | 需要确定控件类型(fieldShowType)、字典配置、校验规则、默认值表达式、扩展配置(fieldExtendJson)时——创建/编辑表单字段必读 |
| [onlform-enhance.md](references/onlform-enhance.md) | 用户要求配置JS/Java/SQL增强、自定义按钮、表单联动、列表Hook时 |
| [onlform-auth.md](references/onlform-auth.md) | 用户要求配置字段权限、按钮权限、数据权限、或给角色授权时 |
| [onlform-data-crud.md](references/onlform-data-crud.md) | 需要插入/查询/更新/删除表单数据、导出CSV时——确认各控件的值格式必读 |
| [onlform-jimureport.md](references/onlform-jimureport.md) | 用户要求关联积木报表或集成打印功能时 |
| [onlform-misc.md](references/onlform-misc.md) | 处理head级配置(extConfigJson)、主子表/树表JSON结构、BPM集成、视图配置、表单布局(formTemplate)时 |
| [onlform-api-reference.md](references/onlform-api-reference.md) | 需要查看addAll完整请求体模板、head字段枚举、系统默认字段时 |
| [onlform-route-cache.md](references/onlform-route-cache.md) | 用户要求开启Online表单路由缓存(keepAlive)、配置菜单组件名称、或询问动态/静态路由配置时 |

### Step 12: 菜单挂载 + 路由缓存（**可选 · 不自动执行**）

> **本步骤非必须。** 表单/流程创建完成后**不要**默认执行菜单挂载。先用一句话询问用户："是否需要挂载到菜单？" 用户明确确认后再执行。
> 用户可以直接通过预览 URL 访问表单，或自行在系统设置中挂载。演示环境账号通常无菜单创建权限，强行执行会失败。

**使用 `scripts/onlform_menu.py`：**

```bash
python <skill目录>/scripts/onlform_menu.py --api-base <URL> --token <TOKEN> --config <config.json>
```

支持的操作：
- `mount` — 挂载单个 Online 表单到菜单（自动推导预览地址和组件名称，可选开启缓存、授权角色）
- `mount_batch` — 批量挂载多个表
- `enable_cache` — 为已有菜单开启路由缓存

**挂载菜单 JSON 示例：**
```json
{
  "action": "mount",
  "tableName": "test_order_main",
  "menuName": "测试订单主表",
  "keepAlive": false,
  "roleCode": "admin"
}
```

**开启缓存 JSON 示例：**
```json
{
  "action": "enable_cache",
  "menuId": "xxx"
}
```

> **默认不开启缓存路由**。仅当用户明确要求时才设置 `keepAlive: true`。
> **路由缓存详细参考参见：** `references/onlform-route-cache.md`
