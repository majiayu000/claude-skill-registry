---
name: jeecg-onlreport
description: Use when user asks to create/edit/query Online reports, SQL reports, data reports, or says "创建报表", "生成报表", "新建报表", "查询报表", "online报表", "SQL报表", "数据报表", "统计报表", "create report", "generate report", "data report". Also triggers when user describes report requirements like "做一个销售统计报表", mentions JeecgBoot cgreport/online report, or says "查看现有报表" / "列出所有报表". This skill handles Online 报表 (SQL-driven data display/reports), not Online forms (cgform) or designer forms (desform).
---

# JeecgBoot Online 报表 AI 自动生成器

将自然语言描述的报表需求，转换为 Online 报表配置，并通过 API 自动创建/编辑/查询。

> **重要**：本 skill 处理「Online 报表」（SQL 驱动的只读数据报表），不涉及 Online 表单（cgform）或设计器表单（desform）。

## 核心能力

| 操作 | 说明 |
|------|------|
| **查询报表** | 列出系统中所有 Online 报表，查看字段和参数配置 |
| **新增报表** | 从自然语言需求或 SQL 创建报表 |
| **编辑报表** | 修改现有报表的字段、参数、SQL |

---

## Step 0: 收集凭证

**每次操作前必须收集以下信息**（如果用户已提供则跳过）：

1. **API 地址** — JeecgBoot 后端地址，如 `https://boot3.jeecg.com/jeecgboot`
2. **X-Access-Token** — JWT 令牌，从浏览器 F12 → Network → 任意请求的 Request Headers 中复制

用户未提供时提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token。

---

## Step 1: 判断操作类型

根据用户意图判断操作类型：

| 用户意图关键词 | 操作 |
|---------------|------|
| 列出报表 / 查询报表 / 查看所有报表 / 有哪些报表 | **查询报表** → Step 2 |
| 创建 / 新建 / 做一个 / 生成报表 | **新增报表** → Step 3 |
| 修改 / 编辑 / 改字段 / 加字段 / 删除字段 | **编辑报表** → Step 4 |

> ⚠️ **菜单挂载与角色授权为可选操作，不得默认执行：**
> - 用户只说"创建报表"→ 仅执行 `create_report` + `validate_report`，**不挂载菜单，不授权角色**
> - 用户明确说"挂载到菜单"、"绑定菜单"、"授权给 xxx 角色"等关键词 → 才调用 `publish_report` 或 `create_and_publish`
> - 违反此规则会导致：超出用户意图、产生不必要的菜单记录、因全量拉取权限列表而显著增加耗时

---

## Step 2: 查询报表

> **API 初始化（统一入口）**：所有 Python 操作前必须先调用 `init_api`，与 `desform_utils` 保持一致：
> ```python
> import sys
> sys.path.insert(0, r'<skill目录>/scripts')
> from onlreport_api import init_api
> init_api('<api_base>', '<token>')
> ```
> 后续按需导入：`list_all_reports_table`, `list_fields_by_code_table`, `list_reports`, `query_report`, `list_fields`, `list_params`, `parse_sql`, `create_report`, `edit_report`, `gen_id`, `create_menu`, `get_role_id_by_code`, `grant_menu_to_role`, `add_data_rule`, `query_data_rules`

### 2.1 快速列表（语法糖）

**首选方式**，调用 `list_all_reports_table()` 一次返回所有报表的名称/编码/SQL 表格，自动分页遍历：

```python
from onlreport_api import init_api, list_all_reports_table
init_api('<api_base>', '<token>')
list_all_reports_table()
```

返回 Markdown 表格，仅含三个字段（报表名称、报表编码、报表 SQL），方便 AI 直接使用：

```
| 报表名称 | 报表编码 | 报表 SQL |
|----------|----------|----------|
| 关联报表查询 | fz_sql | SELECT u.id, u.username ... |
| ... | ... | ... |
```

或通过 CLI：
```bash
python "<skill目录>/scripts/onlreport_api.py" \
    --api-base <URL> --token <TOKEN> -a list-table
```

### 2.2 按编码查字段（语法糖）

**首选方式**，调用 `list_fields_by_code_table(code)` 直接通过报表编码查字段：

```python
from onlreport_api import init_api, list_fields_by_code_table
init_api('<api_base>', '<token>')
list_fields_by_code_table('fz_sql')
```

返回 Markdown 表格，仅含三个字段（字段编码、字段文本、字段类型），自动分页：

```
| 字段编码 | 字段文本(显示名) | 字段类型 |
|----------|-----------------|----------|
| id | ID | String |
| username | username | String |
| realname | realname | String |
```

或通过 CLI：
```bash
python "<skill目录>/scripts/onlreport_api.py" \
    --api-base <URL> --token <TOKEN> -a fields-table --code fz_sql
```

底层 API：`GET /online/cgreport/item/listByHeadCode?headCode={code}`

### 2.3 查询报表详情

用户指定报表 ID 或编码后，依次查询：

```
GET /online/cgreport/head/queryById?id={headId}        # 报表头配置
GET /online/cgreport/item/listByHeadId?headId={headId}  # 字段列表
GET /online/cgreport/param/listByHeadId?headId={headId}  # 参数列表
```

展示完整配置供用户参考，询问是否需要修改。

---

## Step 3: 新增报表

### 3.1 收集需求

从用户描述中提取：

| 信息 | 来源 | 示例 |
|------|------|------|
| 报表编码 (code) | 自动生成 snake_case | `sales_report` |
| 报表名称 (name) | 用户指定 | "销售统计报表" |
| SQL 语句 (cgrSql) | 用户提供 SQL 或描述需求 | `SELECT ... FROM ...` |
| 数据源 (dbSource) | 用户指定，空=默认 | `second_db` |

**创建前必须校验报表编码唯一性**，调用 `check_code_available(code)` 或直接调用接口：
```
GET /sys/duplicate/check?tableName=onl_cgreport_head&fieldName=code&fieldVal={code}
```
返回 `success: true` 表示编码可用，`false` 表示已被占用，需换一个。`create_report()` 内部已自动调用此校验。

**SQL 有两种来源：**
1. **用户直接提供 SQL** → 直接使用
2. **用户描述需求** → 需要用户确认表名和字段（调用 parseSql 验证）

### 3.2 调用 parseSql 解析字段

**必须先调用 parseSql 获取字段和参数列表：**

```
GET /online/cgreport/head/parseSql?sql={urlEncodedSql}&dbKey={dbKey}
```

返回结构：字段列表 `fields[]` 和参数列表 `params[]`。

> **为什么必须先调用 parseSql？** 因为 SQL 中的 `${paramName}` 会被解析为参数列表，字段列表是后续构造 items 配置的依据。

#### parseSql 失败处理

SQL 包含复杂函数（如 `name like concat('%','${username}','%')`）时会解析失败。解决方案：

1. 先将问题条件去掉，用简化 SQL 解析
2. 解析成功后，在 SQL 参数 tab 手工新增参数名（如 `username`，对应 `${username}`）
3. 最终保存时 cgrSql 使用完整的原始 SQL

### 3.3 智能字段配置

根据字段名语义，自动推导每个字段的配置。

#### 字段通用属性

> **searchMode 说明**：有效值只有 `single`（单值查询）和 `group`（范围查询）两种。String 类型的 `single` 查询在后端会自动执行 LIKE 模糊匹配；Date/Datetime 类型用 `group` 实现范围选择。有字典配置时下拉选择自动生效。

| 字段名模式 | fieldTxt（中文名） | fieldType | isShow | isSearch | searchMode | isOrder | isTotal |
|-----------|------------------|-----------|--------|----------|------------|---------|---------|
| id / 主键 | ID | String | **0**（隐藏） | null | - | null | - |
| name / title | 名称/标题 | String | 1 | 1 | `single` | null | - |
| code / no | 编码/编号 | String | 1 | 1 | `single` | null | - |
| status | 状态 | String | 1 | 1 | `single` | null | - |
| type / category | 类型/分类 | String | 1 | 1 | `single` | null | - |
| amount / money / price / fee | 金额/费用/价格 | BigDecimal | 1 | null | - | 1 | **"1"** |
| count / qty / num / number | 数量 | Integer | 1 | null | - | 1 | **"1"** |
| date / sale_date | 日期 | Date | 1 | 1 | `group` | 1 | - |
| time / datetime | 时间 | Datetime | 1 | 1 | `group` | 1 | - |
| create_by / update_by | 创建人/更新人 | String | **0**（隐藏） | null | - | null | - |
| create_time / update_time | 创建时间/更新时间 | Datetime | 1 | null | - | 1 | - |
| sex | 性别 | String | 1 | 1 | `single` | null | - |
| age | 年龄 | Integer | 1 | null | - | null | - |
| email | 邮箱 | String | 1 | null | - | null | - |
| phone / mobile / tel | 电话/手机号 | String | 1 | null | - | null | - |
| address | 地址 | String | 1 | null | - | null | - |
| remark / description / content | 备注/描述 | String | 1 | null | - | null | - |
| dept / org | 部门/组织 | String | 1 | 1 | `single` | null | - |
| sys_org_code / tenant_id | 系统字段 | String | **0**（隐藏） | null | - | null | - |
| 图片/附件字段 | 图片 | Image | 1 | null | - | null | - |

> **parseSql 返回的 fieldType 通常是 String**，AI 必须根据字段名语义修正为正确的类型（Date/Datetime/BigDecimal/Integer/Long/Image 等）。
>
> **isOrder/isSearch 为 null 表示"否"**，不要用 `0`，否则可能影响前端展示。

#### 字典配置 (dictCode)

**普通字典**（输入字典 code）：
- 常用系统字典：`sex`、`priority`、`valid_status`、`urgent_level`、`yn`

**SQL 字典**（查另一张表）：格式固定为 `SELECT id 'value', name 'text' FROM table_name`，字段别名必须是 `value` 和 `text`：
```sql
SELECT username AS value, realname AS text FROM sys_user
```

**replaceVal 格式**（导出时文本替换）：`显示文本_数据库值` 逗号分隔，例如 `男_1,女_2`

#### 分组表头 (groupTitle)

同一分组的多个字段设置相同的 groupTitle，可实现多级表头：
```json
{"fieldName": "q1_amount", "groupTitle": "第一季度"}
{"fieldName": "q1_count",  "groupTitle": "第一季度"}
```

#### 字段跳转 (fieldHref)

支持以下语法：

| 用法 | 示例 |
|------|------|
| 跳转到菜单路径 | `/system/user` 或 `/system/user?sex=1` |
| 跳转到 Vue 组件 | `/jeecg/helloworld.vue?id=${id}` |
| 跳转到外部链接 | `http://jeecg.com?id=${id}` |
| 动态参数（当前行字段值） | `http://jeecg.com?sex=${sex}` |
| JS 表达式（双花括号） | `/account/center?name=${name}&age={{${age} + 100}}` |
| 获取当前登录 Token | `http://api.example.com?token={{ACCESS_TOKEN}}` |

---

## Step 4: 编辑报表

### 4.1 查询现有配置

1. 用户提供报表 ID 或编码
2. 依次调用 queryById、listByHeadId（字段）、listByHeadId（参数）
3. 展示现有配置

### 4.2 确认修改需求

根据用户需求，确定：
- 哪些字段需要修改 isShow/isSearch/orderNum 等
- 哪些字段需要新增或删除
- SQL 是否需要调整

### 4.3 构造 editAll 请求

editAll 使用 **PUT** 方法（非 POST）。

与新增类似，但需注意：
- `head.id` = 现有报表 ID（必填）
- `deleteItemIds` = 要删除的字段 ID 逗号拼接
- `deleteParamIds` = 要删除的参数 ID 逗号拼接

#### 替换参数的完整流程

编辑时若需要**替换参数**（如从无参改为有参，或修改参数配置），步骤：

1. 查询旧参数列表，收集所有旧参数 ID
2. 新参数对象必须包含 `id`（`gen_id()` 生成）和 `headId`（报表 ID）
3. 在 payload 中设置 `deleteParamIds` 删除旧参数，`params` 传入新参数

```python
old_params = api_request(f'/online/cgreport/param/listByHeadId?headId={head_id}')['result']
delete_param_ids = ','.join(p['id'] for p in old_params) if old_params else None

new_params = [
    {"id": gen_id(), "headId": head_id, "paramName": "log_type", "paramTxt": "日志类型", "paramValue": "1", "orderNum": 1}
]

payload = {
    "head": {...},
    "items": items,
    "params": new_params,
    "deleteParamIds": delete_param_ids   # 有旧参数时必传，否则会重复
}
```

> **注意**：editAll 的 params 中每条记录必须有 `id` 和 `headId`，否则保存后参数不生效。新增时（`create_report`）的 params 可以不带这两个字段。

---

## Step 5: 展示摘要并确认

**在执行 API 前必须展示以下摘要，等待用户确认：**

```
## Online 报表配置摘要

- 报表编码：sales_report
- 报表名称：销售统计报表
- 数据源：默认
- 目标环境：https://boot3.jeecg.com/jeecgboot

### SQL 语句
SELECT s.id, s.name, s.amount, s.sale_date, s.status
FROM biz_sales s WHERE 1=1

### 字段配置

| 序号 | 字段名 | 显示名称 | 类型 | 显示 | 查询 | 排序 | 合计 |
|------|--------|---------|------|------|------|------|------|
| 0 | id | ID | String | 否 | 否 | 否 | - |
| 1 | name | 名称 | String | 是 | 单值 | 否 | - |
| 2 | amount | 金额 | BigDecimal | 是 | 否 | 是 | 是 |
| 3 | sale_date | 销售日期 | Date | 是 | 范围 | 是 | - |
| 4 | status | 状态 | String | 是 | 单值 | 否 | - |

### 参数
| 参数名 | 显示名称 | 默认值 |
|--------|---------|--------|
| (无) | | |

确认以上配置？(y/n)
```

---

## Step 6: 调用 API

用户确认后执行。使用 Python 调用 API（Windows 环境下 curl 中文会出错）：

### Windows 执行环境（强制规则，违反会让用户吐槽"执行太慢"）

**现象**：Windows 的 Bash tool 会把 `python` / `python -c` / skill 脚本当作长命令自动 `run_in_background`，tool 立即返回 background ID，真正输出要等完成通知——把毫秒级调用放大到数秒。

**规则**：
- **Windows（platform=win32）** → 用 Bash tool 调用 `powershell -Command "python xxx.py"`，同步返回。
- **Linux / macOS** → 用 Bash tool 直接调用 `python xxx.py`。
- 任何平台都不用 `curl`：跨平台不一致，Windows Bash 下同样被后台化。

**脚本执行前强制检查（3 项，缺一不可）**：
1. ✅ Windows 下用 `powershell -Command "python xxx.py"`，不是直接 `python xxx.py`
2. ✅ 脚本已写入 `.py` 文件（禁止 `python -c` 内联代码）
3. ✅ 脚本第一行已加编码声明：`import sys; sys.stdout.reconfigure(encoding='utf-8')`（防 GBK 崩溃重试）

**Windows 正确示例**：
```
Bash: powershell -Command "python <skill_base_dir>/scripts/onlreport_api.py --api-base ... --token ..."
```
> `<skill_base_dir>` 是本 SKILL.md 所在目录，运行时用实际路径替换。

**Windows 错误示例**（会被后台化，用户立即感知到"卡"）：
```
Bash: python onlreport_api.py ...     ← 返回 "Command running in background with ID: xxx"
Bash: python -c "..."                  ← 同上
Bash: curl -X POST ...                 ← 同上
```

---

**调用方式**：import `onlreport_api`，调用 `init_api` 初始化后直接使用封装函数，无需修改脚本文件。

```python
import sys
sys.path.insert(0, r'<skill目录>/scripts')
from onlreport_api import init_api, parse_sql, create_report, gen_id
init_api('<api_base>', '<token>')
```

脚本中封装了以下操作：

**查询类**
- `list_reports()` — 查询报表列表
- `list_all_reports_table()` — 查询所有报表（Markdown 表格，自动分页）
- `list_fields_by_code_table(code)` — 按编码查字段（Markdown 表格）
- `query_report(head_id)` — 查询报表头
- `list_fields(head_id)` — 查询字段列表
- `list_params(head_id)` — 查询参数列表
- `get_report_id_by_code(code)` — 按编码获取报表 ID
- `parse_sql(sql, db_key)` — 解析 SQL 字段

**创建 / 编辑**
- `create_report(code, name, sql, db_source, items, params)` — 创建报表，返回含 `head_id` 的 dict
- `edit_report(...)` — 编辑报表（PUT editAll）

**发布流程（高级语法糖，推荐优先使用）**
- `validate_report(head_id)` — 验证 SQL 是否可执行，返回 True/False
- `publish_report(head_id, name, role_code='admin', parent_id='')` — 验证 SQL + 创建菜单 + 授权角色，三步合一
- `create_and_publish(code, name, sql, items, params=[], db_source='', role_code='admin', parent_id='')` — **全流程一键完成**：创建报表 + 验证 + 建菜单 + 授权

**字段构建辅助**
- `build_item(field_name, field_txt, ...)` — 按字段名语义自动推断类型/查询/显示，支持手动覆盖任意属性

**菜单 & 权限**
- `create_menu(head_id, name, parent_id='')` — 创建报表菜单
- `get_role_id_by_code(role_code)` — 按角色编码获取角色 ID
- `grant_menu_to_role(role_id, menu_id)` — 追加授权菜单给角色
- `add_data_rule(menu_id, role_id, rule_name, rule_column, rule_conditions, rule_value)` — 完整四步数据规则配置

---

### build_item 用法示例（推荐，替代手写 dict）

```python
from onlreport_api import init_api, build_item, create_and_publish
init_api('<api_base>', '<token>')

items = [
    build_item('id',          'ID',       order_num=0),          # 自动隐藏
    build_item('username',    '用户名',   order_num=1),          # 自动单值查询
    build_item('status',      '状态',     order_num=2),          # 自动 dictCode=valid_status
    build_item('amount',      '金额',     order_num=3),          # 自动 BigDecimal + 合计
    build_item('create_time', '创建时间', order_num=4),          # 自动 Datetime + 可排序
    # 手动覆盖
    build_item('email', '邮箱', order_num=5, field_href='mailto:${email}'),
    build_item('sex',   '性别', order_num=6, dict_code='sex'),
]

# 一键：建报表 + 验证 SQL + 建菜单 + 授权 admin
head_id = create_and_publish('my_report', '我的报表', 'SELECT ... FROM ...', items)
```

### build_item 自动推断规则

| 字段名关键词 | 自动推断结果 |
|-------------|------------|
| `id` | 隐藏（isShow=0） |
| `create_by` / `update_by` / `sys_org_code` / `org_code` | 隐藏 |
| `avatar` / `photo` / `image` / `pic` / `img` | Image 类型 |
| `amount` / `money` / `price` / `fee` / `cost` | BigDecimal，isTotal='1' |
| `count` / `qty` / `num` / `quantity` | Integer，isTotal='1' |
| `birthday` / `*_date` | Date，范围查询(group) |
| `*_time` / `*_datetime` | Datetime，可排序 |
| `create_time` / `update_time` | Datetime，可排序，不查询 |
| `sex` | dictCode=sex |
| `status` | dictCode=valid_status |
| `name` / `title` / `code` / `no` | 单值查询(single) |

> 所有推断值均可通过参数覆盖，例：`build_item('status', '状态', dict_code='my_dict')`

---

```python
# 手动构造 items 原始写法（不推荐，优先使用 build_item）
items = [
    {
        "id": gen_id(),         # 雪花 ID，19位数字字符串
        "headId": None,
        "fieldName": "name",
        "fieldTxt": "名称",
        "fieldWidth": None,
        "fieldType": "String",
        "searchMode": "single",  # 单值查询；范围查询用 "group"
        "isOrder": None,         # 不排序用 null，排序用 1
        "isSearch": 1,
        "dictCode": None,
        "fieldHref": None,
        "isShow": 1,
        "orderNum": 1,
        "replaceVal": None,
        "isTotal": None,         # 不合计用 null，合计用 "1"（字符串）
        "groupTitle": None,
        "createBy": None,
        "createTime": None,
        "updateBy": None,
        "updateTime": None
    }
]
```

**关键约束**：
1. **Windows 必须用 `powershell -Command "python xxx.py"`**，不要用 `python xxx.py` 或 `curl`
2. 写临时 `.py` 脚本时用 `Write` 工具，脚本首行加 `import sys; sys.stdout.reconfigure(encoding='utf-8')`，执行后删除临时文件
3. 字段 ID 用 `gen_id()` 生成（雪花格式 19 位数字字符串）
4. parseSql 返回的 fieldType 全是 String，需根据上表语义修正（或直接用 `build_item` 自动推断）
5. `isOrder`/`isSearch` 的"否"值为 `null`，不要用 `0`
6. `isTotal` 的"是"值为字符串 `"1"`，不是数字 `1`
7. **合计行仅在表内有数据时才显示**；表内无数据时合计行不出现，属正常现象，录入数据后即可看到
8. 合计只统计数字值；字段含空值/null/非数字内容时会显示"包含非数字内容"提示

---

## Step 7: 验证报表 SQL 可用性

报表创建成功后，**必须立即调用以下接口验证 SQL 执行正常**，否则报表预览会出现 500 错误：

```
GET /online/cgreport/api/getColumnsAndData/{headId}
```

```python
url = f'{base}/online/cgreport/api/getColumnsAndData/{head_id}'
req = urllib.request.Request(url, headers={'X-Access-Token': token})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read())
    if data.get('success'):
        result = data.get('result', {})
        columns = result.get('columns', [])
        rows = result.get('rows', [])
        print(f'验证通过：{len(columns)} 个字段，{len(rows)} 行数据')
    else:
        print('验证失败：', data.get('message'))
```

**常见失败原因及修复：**

| 错误信息 | 原因 | 修复方式 |
|---------|------|---------|
| `Unknown column 'xxx' in 'field list'` | SQL 引用了表中不存在的字段（如多租户字段 `tenant_id` 在非多租户版本中不存在） | 从 SQL 和字段配置中删除该字段，用 `editAll` 更新 |
| `Table 'xxx' doesn't exist` | 表名错误或数据源配置有误 | 检查 SQL 中的表名和 dbSource |
| `syntax error` | SQL 语法错误 | 修正 SQL 语句 |

验证失败时，用 `editAll`（PUT）修复 SQL 和字段配置后，再次调用验证，直到返回 `success: true`。

---

## Step 8: 生成菜单 SQL

报表创建成功后，脚本会自动调用 `print_menu_sql(head_id, name)` 输出菜单 SQL。

**本地环境自动执行规则**：如果 API_BASE 以 `http://127.0.0.1` 或 `http://localhost` 开头（不区分大小写），自动执行 MySQL 插入菜单：

```bash
mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3 -e "INSERT INTO sys_permission (...) VALUES (...);"
```

- 如果 MySQL 失败，回退为输出 SQL 让用户手动执行
- 数据库参数默认 `mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3`

**菜单配置说明：**
- 前端组件固定为：`modules/online/cgreport/auto/OnlCgreportAutoMain`
- 报表访问路径：`/online/cgreport/{headId}`
- 也可在「系统管理 → 菜单管理」手工新增菜单，粘贴上述配置地址，「是否是路由菜单」设为否

---

## 输出结果模板

```
## Online 报表操作成功

- 报表编码：{code}
- 报表名称：{name}
- 字段数量：{N} 个
- 参数数量：{M} 个
- 目标环境：{API_BASE}
- 菜单 SQL：{已自动执行 ✓ / 需手动执行}

### 菜单 SQL
INSERT INTO sys_permission (...) VALUES (...);

### 后续操作
1. ✅ 调用 `/online/cgreport/api/getColumnsAndData/{headId}` 验证 SQL 执行正常
2. 打开 JeecgBoot 后台 → Online报表
3. 找到该报表，点击「功能测试」预览效果
4. 如菜单未自动执行，手动执行上方 SQL 或在后台手动添加
5. 可在「编辑」中调整字段显示/查询/排序等配置
```

---

## SQL 高级特性

### 参数化查询（Velocity 模板）

在 SQL 中使用 Velocity 模板语法定义参数（parseSql 会自动解析 `${paramName}` 为参数列表）：

```sql
SELECT * FROM biz_sales
WHERE 1=1
${#if($startDate != '')} AND sale_date >= '$startDate' ${#end}
${#if($endDate != '')} AND sale_date <= '$endDate' ${#end}
${#if($status != '')} AND status = '$status' ${#end}
```

对应的 params 配置（**新增**时可不带 id/headId，**editAll 编辑**时必须带）：

```json
[
  {"paramName": "startDate", "paramTxt": "开始日期", "paramValue": "", "orderNum": 1},
  {"paramName": "endDate",   "paramTxt": "结束日期", "paramValue": "", "orderNum": 2},
  {"paramName": "status",    "paramTxt": "状态",     "paramValue": "", "orderNum": 3}
]
```

editAll 编辑时的完整格式（需加 `id` 和 `headId`）：
```python
{"id": gen_id(), "headId": head_id, "paramName": "status", "paramTxt": "状态", "paramValue": "", "orderNum": 1}
```

**URL 带参访问**：获取报表配置地址后，将 `${sex}` 替换为实际值访问：
```
/online/cgreport/{headId}?sex=1
```

### 系统变量

在 SQL 中用 `#{变量名}` 引用当前登录用户信息，实现数据隔离：

```sql
SELECT * FROM sys_user WHERE username = '#{sys_user_code}'
```

| 变量 | 说明 |
|------|------|
| `#{sys_user_code}` | 当前登录用户账号 |
| `#{sys_user_name}` | 当前登录用户真实姓名 |
| `#{sys_date}` | 当前系统日期 |
| `#{sys_time}` | 当前系统时间 |
| `#{sys_org_code}` | 当前登录用户部门编号 |
| `#{sys_base_path}` | 当前 Java 服务 basePath |

### 排序配置

- **MySQL 及非 SQL Server 数据库**：直接在 SQL 中添加 `ORDER BY` 即可
- **SQL Server 数据库**：不允许 SQL 内含 `ORDER BY`，必须通过 URL 参数传递：

```
/online/cgreport/{headId}?column=age,name&order=desc
```

| URL 参数 | 说明 |
|----------|------|
| `column` | 排序字段，多个用逗号分隔 |
| `order` | 排序方式：`desc`（倒序）/ `asc`（正序） |

---

## 菜单创建与角色授权

报表创建后，通过 API 完成菜单注册和角色授权的完整流程：

### 1. 创建菜单
```
POST /sys/permission/add
```
```json
{
  "id": "{headId}",
  "name": "报表名称",
  "parentId": "",
  "url": "/online/cgreport/{headId}",
  "component": "modules/online/cgreport/auto/OnlCgreportAutoMain",
  "isRoute": 1,
  "isLeaf": "1",
  "keepAlive": 0,
  "hidden": 0,
  "hideTab": 0,
  "status": "1",
  "menuType": 1,
  "sortNo": 1.0,
  "alwaysShow": 0,
  "internalOrExternal": false,
  "permsType": "0",
  "ruleFlag": 0
}
```

### 2. 查找角色 ID
```
GET /sys/role/list?pageNo=1&pageSize=50
```
返回 `records[]`，找到目标角色的 `id`（管理员 `roleCode=admin`）。

### 3. 查询角色已有权限
```
GET /sys/permission/queryRolePermission?roleId={roleId}
```
返回权限 ID 数组（可能高达千条）。

### 4. 追加权限并保存
```
POST /sys/permission/saveRolePermission
Content-Type: application/json
```
```json
{
  "roleId": "{roleId}",
  "permissionIds": "id1,id2,...,{新菜单headId}",
  "lastPermissionIds": "id1,id2,..."
}
```

> **注意**：必须用 **JSON body**（`application/json`）发送，不支持 form 表单或 URL 参数。权限 ID 列表可能很长（>1000），不能放 URL。

---

## 数据权限配置

Online 报表支持通过「数据规则」过滤报表数据，仅展示符合条件的数据。

**配置路径**：菜单管理 → 找到报表菜单 → 更多 → 数据规则

**注意事项**：
- 规则字段不限于报表查询字段，表中任意字段均可使用
- 字符串参数必须用单引号引起来（例如：`'admin'`），否则视为数字
- 支持系统上下文变量，需加单引号（例如：`'#{sys_user_code}'`）
- **不支持带 `?` 参数的菜单配置数据规则**；如有需要，单独创建一个不带参数的隐藏菜单用于数据规则配置

### 通过 API 配置数据规则

**前提：角色必须先有该菜单的权限**，否则授权数据规则时会报"请先保存角色菜单权限!"。先调用 `grant_menu_to_role(role_id, menu_id)` 或手动授权菜单。

**Step 1：创建规则**（默认未启用）
```
POST /sys/permission/addPermissionRule
{"permissionId":"{menuId}","ruleName":"规则名称","ruleColumn":"sex","ruleConditions":"!=","ruleValue":"'1'"}
```

> ⚠️ **`addPermissionRule` 返回的 `result` 为 `null`，不含规则 ID！**
> 创建后必须调用以下接口查询刚创建的规则 ID：
> ```
> GET /sys/permission/queryPermissionRule?permissionId={menuId}
> ```
> 按 `ruleName` 匹配且 `status == null` 找到目标规则，取其 `id`。
> **`add_data_rule()` 函数已内置此逻辑，直接调用函数即可。**

**Step 2：启用规则**（`status:"1"` 才生效，缺少此步规则不生效）
```
POST /sys/permission/editPermissionRule
{"id":"{ruleId}","permissionId":"{menuId}","ruleName":"规则名称","ruleColumn":"sex","ruleConditions":"!=","ruleValue":"'1'","status":"1"}
```

**Step 3：将规则授权给指定角色**（此步骤才真正让规则对角色生效）
```
POST /sys/role/datarule
{"permissionId":"{menuId}","roleId":"{roleId}","dataRuleIds":"{ruleId1},{ruleId2}"}
```
多个规则 ID 用逗号分隔。**缺少此步骤，规则虽已创建并启用，但不会对任何角色生效。**

**Step 4：验证规则已对角色生效**
```
GET /sys/role/datarule/{menuId}/{roleId}
```
返回结构：
- `datarule[]`：该菜单下配置的所有数据规则列表
- `drChecked`：已授权给该角色的规则 ID，逗号分隔

`drChecked` 中包含规则 ID 说明授权成功。

### 完整流程小结

```
0. grant_menu_to_role(role_id, menu_id)            → 前提：确保角色有菜单权限
1. POST /sys/permission/addPermissionRule          → 创建规则（默认未启用，result 为 null）
   GET  /sys/permission/queryPermissionRule         → 查询列表获取真实规则 ID
2. POST /sys/permission/editPermissionRule         → 启用规则（status:"1"）
3. POST /sys/role/datarule                         → 授权给角色（才真正生效）
4. GET  /sys/role/datarule/{menuId}/{roleId}       → 验证授权结果
```

### 修改已有数据规则

使用 `editPermissionRule` 可修改规则名称、字段、条件、值（保持 `status:"1"`）：
```
POST /sys/permission/editPermissionRule
{"id":"{ruleId}","permissionId":"{menuId}","ruleName":"新名称","ruleColumn":"birthday","ruleConditions":"=","ruleValue":"'2024-04-11'","status":"1"}
```

### 删除数据规则

```
DELETE /sys/permission/deletePermissionRule?id={ruleId}
```

### ruleConditions 条件值

条件选项来自系统字典 `rule_conditions`，可通过 `GET /sys/dict/getDictItems/rule_conditions` 查询完整列表。

常用条件示例：

| 条件 | ruleValue 示例 | 说明 |
|------|---------------|------|
| `=` | `'2024-04-11'` | 等于（字符串必须加单引号） |
| `!=` | `'1'` | 不等于 |
| `>=` | `'2024-01-01'` | 大于等于 |
| `<=` | `'2024-12-31'` | 小于等于 |
| `like` | `'%admin%'` | 模糊匹配 |
| `in` | `'1','2','3'` | 包含多值 |
| `USE_SQL_RULES` | `username != 'admin'` | **自定义 SQL 表达式**，`ruleColumn` 无需填写，`ruleValue` 直接写 WHERE 子句（不含 WHERE 关键字） |

### ruleValue 系统变量

`ruleValue` 支持以下系统上下文变量（自动替换为当前登录用户信息）：

| 变量 | 说明 |
|------|------|
| `#{sys_user_code}` | 登录用户账号 |
| `#{sys_user_name}` | 登录用户名称 |
| `#{sys_date}` | 当前日期 |
| `#{sys_time}` | 当前时间 |
| `#{sys_org_code}` | 登录用户部门编码 |
| `#{sys_multi_org_code}` | 用户拥有的所有部门编码 |
| `#{tenant_id}` | 登录用户所属租户 |

> 字符串类型的系统变量需加单引号：`'#{sys_user_code}'`

---

## 数据导出

Online 报表支持导出功能，默认分 sheet 导出，每个 sheet 最多 1 万条数据。

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 401 / 认证失败 | Token 过期 | 重新从浏览器 F12 获取 X-Access-Token |
| 报表编码已存在 | code 重复 | 换一个 code，或用 editAll 编辑 |
| parseSql 失败 | SQL 含复杂函数或语法问题 | 去掉问题条件后解析，再手工添加参数 |
| SQL 注入风险 | 包含危险语句 | 不要在 SQL 中使用 DROP/DELETE/UPDATE |
| 禁止 select * | 系统开启了 disableSelectAll | 改为指定具体字段 |
| 中文乱码 | 用了 curl | 必须用 Python urllib |

---

## 与其他 Skill 的区别

| Skill | 产出物 | 适用场景 |
|-------|--------|---------|
| `jeecg-onlreport` | Online 报表（SQL 驱动，只读数据展示） | 数据查询、统计分析、数据导出 |
| `jeecg-onlform` | Online 表单（元数据驱动，CRUD） | 数据录入管理 |
| `jeecg-codegen` | Java + Vue3 代码 | 需要自定义业务逻辑的模块 |
| `jeecg-desform` | 设计器表单 JSON | 数据采集、审批表单 |

---

## API 快速参考

详细 API schema 参见 `references/api_schema.md`。

| 操作 | API |
|------|-----|
| 列出报表 | `GET /online/cgreport/head/list` |
| 查报表详情 | `GET /online/cgreport/head/queryById?id={id}` |
| 查字段列表 | `GET /online/cgreport/item/listByHeadId?headId={id}` |
| 按编码查字段 | `GET /online/cgreport/item/listByHeadCode?headCode={code}` |
| 查参数列表 | `GET /online/cgreport/param/listByHeadId?headId={headId}` |
| 解析 SQL | `GET /online/cgreport/head/parseSql?sql={sql}&dbKey={key}` |
| 创建报表 | `POST /online/cgreport/head/add` |
| 编辑报表 | `PUT /online/cgreport/head/editAll` |
