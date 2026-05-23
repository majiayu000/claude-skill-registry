---
name: jeecg-onlchart
description: Use when user asks to create/edit Online graph charts, data visualization, or says "创建图表", "生成图表", "新建图表", "做一个图表", "online图表", "数据图表", "柱状图", "折线图", "饼图", "统计图", "可视化", "chart", "graph", "create chart", "generate chart", "bar chart", "line chart", "pie chart". Also triggers when user describes chart requirements like "做一个销售柱状图" or mentions data visualization like "用图表展示男女比例".
---

# JeecgBoot Online 图表 AI 自动生成器

将自然语言的图表需求描述转换为 Online 图表配置，并通过 API 在 JeecgBoot 系统中自动创建/编辑图表。

> **重要：本 skill 处理「Online 图表」（SQL 驱动的数据可视化图表），不涉及「Online 报表」（cgreport 数据列表）或「Online 表单」（cgform）。**

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

---

## 交互流程

### Step 0: 判断操作类型

| 用户意图关键词 | 操作类型 |
|---------------|---------|
| 创建/新建/做一个/生成图表 | **新增图表** → Step 1A |
| 修改图表/改字段/换图表类型 | **编辑图表** → Step 1B |

### Step 1A: 新增图表 — 解析需求

从用户描述中提取：

| 信息 | 必填 | 默认值 | 示例 |
|------|------|--------|------|
| 图表编码 (code) | 是 | 自动生成 snake_case | `tj_user_sex` |
| 图表名称 (name) | 是 | 用户指定 | "统计男女比例" |
| SQL 语句 (cgrSql) | 是 | 从需求推导或用户提供 | `select count(*) cout, sex from sys_user group by sex` |
| X 轴字段 (xaxisField) | 是 | 从 SQL 推导 | `sex` |
| Y 轴字段 (yaxisField) | 是 | 从 SQL 推导 | `cout` |
| 图表类型 (graphType) | 是 | `bar` | `bar`、`line`、`pie`、`line,bar` |
| 展示模板 (displayTemplate) | 否 | `tab` | `tab`、`single`、`double` |
| 数据源 (dbSource) | 否 | 空（默认数据源） | `second_db` |
| 数据类型 (dataType) | 否 | `sql` | `sql` |

**X/Y 轴推导规则：**
- **X 轴 (xaxisField)**：通常是分类/维度字段（如 sex、dept、month、category）
- **Y 轴 (yaxisField)**：通常是度量/聚合字段（如 count、sum、avg 的结果）

### Step 1B: 编辑图表 — 查询现有配置

1. 用户提供图表 ID 或编码
2. 通过 API 查询现有图表配置（参考 API 列表）
3. 展示现有配置，根据用户需求进行修改

### Step 2: 解析字段（根据 dataType 选择接口）

#### 2A. SQL 类型 — 复用 parseSql 接口

```
GET /online/cgreport/head/parseSql?sql={urlEncodedSql}&dbKey={dbKey}
```

- `sql`：URL 编码后的 SQL 语句
- `dbKey`：数据源编码，默认数据源可不传

**返回结构：**
```json
{
  "success": true,
  "result": {
    "fields": [
      { "fieldName": "cout", "fieldTxt": "cout", "fieldType": "String", "isShow": 1, "orderNum": 1 }
    ],
    "params": []
  }
}
```

> **注意**：parseSql 返回的 `isShow` 是数字 (0/1)，但图表接口需要字符串 `"Y"/"N"`，需要转换。

#### 2B. JSON/API 类型 — 使用 parseField 接口

```
POST /online/graphreport/head/parseField?type=JSON
POST /online/graphreport/head/parseField?type=API
```

请求体（JSON 类型传 JSON 字符串，API 类型传接口 URL）：
```json
{ "data": "[{\"month\":\"01\",\"amount\":1000}]" }
```

**返回结构**（与 parseSql 相同格式）：
```json
{
  "success": true,
  "result": {
    "fields": [
      { "fieldName": "month", "fieldTxt": "month", "fieldType": "String", "isShow": 1 },
      { "fieldName": "amount", "fieldTxt": "amount", "fieldType": "Integer", "isShow": 1 }
    ],
    "params": []
  }
}
```

> JSON/API 类型无需配置 `dbSource`，`cgrSql` 字段存放 JSON 字符串或 API URL。

#### API 数据格式要求

API 接口返回的数据**必须**包裹在 `{"data": [...]}` 结构中，否则图表无法解析：

```json
// ✓ 正确
{"data": [{"name": "一月", "value": 120}, {"name": "二月", "value": 200}]}

// ✗ 错误（裸数组，图表无法识别）
[{"name": "一月", "value": 120}]
```

#### parseField 失败时的处理

`parseField?type=API` 要求 JeecgBoot 服务端能访问该 URL。若服务端无法访问外网导致失败，**跳过 parseField，手动构造 items**（字段已知时可直接定义）。

#### 使用 YApi Mock 创建 API 数据源

项目内置 YApi Mock 平台（https://api.jeecg.com），可快速创建 mock 接口作为 API 数据源。
使用 `scripts/yapi_mock.py` 脚本操作，凭证获取规则，**禁止硬编码**：

- 优先从当前上下文（系统提示、memory、全局配置等任意来源）中查找 YApi 邮箱和密码
- 上下文中找不到时，**必须询问用户**：
  > 需要使用 YApi Mock 创建数据源，请提供登录邮箱和密码（平台地址：https://api.jeecg.com）。

> `yapi_mock.py` 内部使用 `http.cookiejar.CookieJar + build_opener` 管理会话，兼容 Python 3.6 / 3.9 / 3.12 及以上所有版本，直接调用 `init_yapi(email, password)` 即可。

```python
import sys
sys.path.insert(0, '<skill目录>/scripts')
from yapi_mock import init_yapi, create_mock

# 凭证由 Claude 从 memory 读取后注入，不得硬编码
init_yapi(email='<email>', password='<password>')

# 创建 mock 接口并写入数据，返回完整 mock URL
mock_url = create_mock(
    path='/staff',        # 路径后缀，不含 basepath（/claude）
    title='职员信息',
    data=[
        {"name": "张三", "salary": 18000},
        {"name": "李四", "salary": 15000},
    ]
)
print(mock_url)  # https://api.jeecg.com/mock/57/claude/staff
```

**路径规则（重要）**：项目 basepath 为 `/claude`，接口路径只写后缀：

| 传入 path | 完整 mock URL |
|-----------|--------------|
| `/staff`  | `https://api.jeecg.com/mock/57/claude/staff` |
| `/line`   | `https://api.jeecg.com/mock/57/claude/line` |

### Step 3: 智能字段配置

#### 3.1 字段属性映射（图表 vs 报表的差异）

**关键差异：图表字段使用 `"Y"/"N"` 字符串，而非数字 0/1。**

| 属性 | 图表 (graphreport) | 报表 (cgreport) | 说明 |
|------|-------------------|-----------------|------|
| 关联头ID | `graphreportHeadId` | `cgrheadId` | 字段名不同 |
| 是否显示 | `isShow`: `"Y"/"N"` | `isShow`: 0/1 | 类型不同 |
| 是否合计 | `isTotal`: `"Y"/"N"` | `isTotal`: `"0"/"1"` 或 null | 类型不同 |
| 是否查询 | `searchFlag`: `"Y"/"N"` | `isSearch`: 0/1 | 字段名和类型都不同 |
| 查询模式 | `searchMode` | `searchMode` | 相同 |
| 字典 | `dictCode` | `dictCode` | 相同 |
| 排序 | `orderNum` | `orderNum` | 相同 |

#### 3.2 字段显示名称 (fieldTxt)

parseSql 返回的 fieldTxt 默认等于 fieldName，AI 需要根据语义翻译为中文：

| 字段名模式 | 推导中文名 |
|-----------|-----------|
| count / cout / cnt | 数量/人数/次数 |
| sum / total / amount | 合计/总额 |
| avg / average | 平均值 |
| sex | 性别 |
| dept / department | 部门 |
| status | 状态 |
| type / category | 类型/分类 |
| month / year / date | 月份/年份/日期 |
| name / title | 名称 |
| age | 年龄 |
| salary | 薪资 |

#### 3.3 是否显示 (isShow)

| 规则 | isShow |
|------|--------|
| 所有字段（默认） | `"Y"`（图表通常字段不多，全部显示） |
| id / 主键字段 | `"N"` |

#### 3.4 是否查询 (searchFlag) + 查询模式 (searchMode)

| 字段类型 | searchFlag | searchMode |
|---------|------------|------------|
| 分类/维度字段 | `"Y"` | `single` |
| 日期/时间字段 | `"Y"` | `group` |
| 度量/聚合字段 | `"N"` | null |

#### 3.5 是否合计 (isTotal)

| 规则 | isTotal |
|------|---------|
| 度量/聚合字段 | `"Y"` |
| 维度/分类字段 | `"N"` |

#### 3.6 字典配置 (dictCode) — 列表数据值替换显示

**作用**：列表（明细表格区域）中，将数据库存储的原始值替换为可读文本显示。

> 例：性别字段数据库存 `1`/`2`，配置字典后显示为"男"/"女"。

支持两种方式：

**方式一：系统字典编码**

填写系统字典的 `dictCode`，由系统字典表自动解析值 → 文本。

```json
"dictCode": "sex"
```

常用系统字典编码：

| dictCode | 说明 |
|----------|------|
| `sex` | 性别（1=男，2=女） |
| `priority` | 优先级 |
| `valid_status` | 有效状态 |
| `yn` | 是/否 |

**方式二：字典 SQL**

在 `dictCode` 处直接写一条 SELECT 语句，动态替换显示值。SQL 必须返回两列：`value`（数据库存的值）和 `text`（展示的文本）。

```json
"dictCode": "SELECT id as value, name as text FROM sys_category WHERE pid = '1'"
```

```json
"dictCode": "SELECT code as value, name as text FROM sys_depart ORDER BY depart_order"
```

> **注意**：字典 SQL 每次渲染都会执行查询，数据量大时建议加 `WHERE` 条件限制范围。

### Step 4: 图表类型选择

根据数据特征推荐图表类型：

| 数据场景 | 推荐 graphType | 说明 |
|---------|---------------|------|
| 分类对比（如男女人数） | `bar` | 柱状图 |
| 趋势变化（如月度销售） | `line` | 折线图 |
| 占比分布（如部门比例） | `pie` | 饼图 |
| 趋势+对比（如月度销售对比） | `line,bar` | 组合图表 |
| 纯数据明细 | `table` | 数据表格（只渲染在底部明细区，不占图表位） |

**graphType 支持逗号分隔多种类型**，如 `"bar,pie"` 会同时生成柱状图和饼图两个区域。

**组合图表配置（折线+柱状同坐标系）：**
- `graphType`: `"line,bar"`（逗号分隔多种类型）
- `isCombination`: `"combination"`（标记为组合图表）
- 非组合图表 `isCombination` 为 null 或不传

### Step 5: 展示摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

```
## Online 图表配置摘要

- 图表编码：tj_user_sex
- 图表名称：统计男女比例
- 图表类型：bar（柱状图）
- X 轴字段：sex（性别）
- Y 轴字段：cout（人数）
- 数据源：默认
- 目标环境：https://boot3.jeecg.com/jeecgboot

### SQL 语句
select count(*) cout, sex from sys_user group by sex

### 字段配置

| 序号 | 字段名 | 显示名称 | 类型 | 显示 | 查询 | 字典 | 合计 |
|------|--------|---------|------|------|------|------|------|
| 0 | cout | 人数 | String | Y | N | - | Y |
| 1 | sex | 性别 | String | Y | N | sex | N |

### 参数
（无）

确认以上配置？(y/n)
```

### Step 6: 校验编码可用性（仅新增时）

用户确认后，**新增图表前必须先校验 code 是否已被占用**：

```
GET /sys/duplicate/check?tableName=onl_graphreport_head&fieldName=code&fieldVal={code}
```

**返回结构：**
```json
{ "success": true, "result": true }   // true = 可用（未重复）
{ "success": true, "result": false }  // false = 已存在，需换一个 code
```

若 `result` 为 `false`，提示用户更换编码，不继续执行创建。

Python 示例：
```python
encoded_code = urllib.parse.quote(report_code)
check = api_request(f'/sys/duplicate/check?tableName=onl_graphreport_head&fieldName=code&fieldVal={encoded_code}')
if not check.get('result'):
    print(f'图表编码 "{report_code}" 已存在，请换一个编码')
    exit(1)
print(f'编码 "{report_code}" 可用，继续创建...')
```

### Step 7: 调用 API 创建/编辑图表

用户确认且编码校验通过后执行。

#### 6.1 新增图表 — 请求结构

**`POST /online/graphreport/head/add`**

```json
{
    "dbSource": "",
    "name": "统计男女比例",
    "code": "tj_user_sex",
    "displayTemplate": "tab",
    "xaxisField": "sex",
    "yaxisField": "cout",
    "dataType": "sql",
    "graphType": "bar",
    "cgrSql": "select count(*) cout, sex from sys_user group by sex",
    "onlGraphreportItemList": [
        {
            "id": "前端生成的长数字ID",
            "cgrheadId": null,
            "fieldName": "cout",
            "fieldTxt": "人数",
            "fieldWidth": null,
            "fieldType": "String",
            "searchMode": null,
            "isOrder": null,
            "isSearch": null,
            "dictCode": null,
            "fieldHref": null,
            "isShow": "Y",
            "orderNum": 0,
            "replaceVal": null,
            "isTotal": null,
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "groupTitle": null
        }
    ],
    "paramsList": []
}
```

> **注意（add 接口）**：add 时 items 中的关联ID字段名为 `cgrheadId`（值为 null），虽然查询/编辑时返回的是 `graphreportHeadId`。

#### 6.2 编辑图表 — 请求结构

**`PUT /online/graphreport/head/edit`**

```json
{
    "id": "1290934362649460737",
    "name": "统计男女比例",
    "code": "tj_user_bysex",
    "cgrSql": "select count(*) cout, sex from sys_user group by sex",
    "xaxisField": "sex",
    "yaxisField": "cout",
    "yaxisText": "yaxis_text",
    "content": null,
    "extendJs": null,
    "graphType": "line,bar",
    "isCombination": "combination",
    "displayTemplate": "tab",
    "dataType": "sql",
    "dbSource": "",
    "tenantId": 0,
    "lowAppId": null,
    "onlGraphreportItemList": [
        {
            "id": "1290934166687383554",
            "graphreportHeadId": "1290934362649460737",
            "fieldName": "cout",
            "fieldTxt": "人数",
            "isShow": "Y",
            "isTotal": "N",
            "searchFlag": "N",
            "searchMode": null,
            "dictCode": "",
            "fieldHref": null,
            "fieldType": "String",
            "orderNum": 0,
            "replaceVal": null,
            "createBy": "admin",
            "createTime": "2020-08-05 17:03:06",
            "updateBy": null,
            "updateTime": null
        }
    ],
    "paramsList": []
}
```

**add 与 edit 字段差异：**

| 字段 | add | edit | 说明 |
|------|-----|------|------|
| `id` (head) | 不传 | 必传 | 图表头ID |
| `yaxisText` | 不传 | 可选 | Y轴标签文字 |
| `content` | 不传 | 可选 | 自定义内容 |
| `extendJs` | 不传 | 可选 | 扩展JS |
| `isCombination` | 不传 | 可选 | 组合图表标记 |
| `tenantId` | 不传 | 传回原值 | 租户ID |
| Item 关联ID字段 | `cgrheadId`: null | `graphreportHeadId`: headId | 字段名不同 |
| Item `isShow` | `"Y"/"N"` | `"Y"/"N"` | 一致 |
| Item `searchFlag` | 不存在，用 `isSearch` | `searchFlag`: `"Y"/"N"` | add 和 edit 可能不同 |

#### 6.3 字段 ID 生成规则

- add 时使用**雪花ID格式**（19位数字字符串），如 `"2033369959277633538"`
- 可用 Python 的 `str(int(time.time() * 1000) * 1000000 + random.randint(100000, 999999))` 近似生成

#### 6.4 使用 Python 调用 API

**重要限制：**
1. **Windows 环境下 curl 发送中文/长 JSON 会出错**，必须使用 Python
2. **禁止使用 `python3 -c "..."` 内联方式**
3. **必须先用 Write 工具写入 `.py` 临时文件，再用 Bash 执行，最后删除临时文件**

**推荐方式：使用 `onlchart_api.py` 封装脚本（与 jeecg-onlreport 的 onlreport_api.py 同模式）**

**脚本路径：** skill 加载时开头已提供 `Base directory for this skill: <skill_base_dir>`，scripts 目录即 `<skill_base_dir>\scripts`。

```python
import sys
sys.path.insert(0, r'<skill_base_dir>\scripts')
from onlchart_api import init_api, build_item, build_param, create_chart

init_api('<api_base>', '<token>')

items = [
    build_item('sex',    '性别',  search_flag='Y', search_mode='single', dict_code='sex', order_num=0),
    build_item('cout',   '人数',  is_total='Y', order_num=1),
]

# 默认只创建图表，不挂菜单、不授权
# 如需发布，改用 create_and_publish() 或单独调用 publish_chart()
result = create_chart(
    code='tj_user_sex',
    name='用户性别分布',
    sql='SELECT sex, count(*) cout FROM sys_user GROUP BY sex',
    x='sex', y='cout',
    graph_type='bar',
    items=items,
)
```

**可用函数一览：**

| 函数 | 说明 |
|------|------|
| `init_api(api_base, token)` | 初始化连接（必须最先调用） |
| `build_item(field_name, ...)` | 构建字段配置 |
| `build_param(param_name, ...)` | 构建自定义参数 |
| `parse_sql(sql, db_key)` | 解析 SQL 字段 |
| `check_code_available(code)` | 校验编码是否可用 |
| `create_chart(code, name, sql, x, y, items, ...)` | 创建图表 |
| `edit_chart(head_id, ...)` | 编辑图表 |
| `publish_chart(head_id, name, role_code)` | 挂载菜单 + 授权角色 |
| `create_and_publish(code, name, sql, x, y, items, ...)` | **一键全流程** |
| `list_charts()` | 查询图表列表 |
| `query_chart(head_id)` | 查询图表详情 |
| `get_chart_id_by_code(code)` | 按编码查 head_id |

---

**低级手写脚本模板（不推荐，优先使用上方封装）：**

```python
import urllib.request
import json
import time
import random
import ssl
import urllib.parse

API_BASE = '{用户提供的后端地址}'
TOKEN = '{用户提供的 X-Access-Token}'

# 忽略SSL验证（开发环境）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def api_request(path, data=None, method=None):
    """发送 API 请求"""
    url = f'{API_BASE}{path}'
    headers = {
        'X-Access-Token': TOKEN,
        'Content-Type': 'application/json; charset=UTF-8'
    }
    if data is not None:
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        if method is None:
            method = 'POST'
        req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    else:
        if method is None:
            method = 'GET'
        req = urllib.request.Request(url, headers=headers, method=method)
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read().decode('utf-8'))

def gen_id():
    """生成雪花ID格式的字符串（19位数字）"""
    return str(int(time.time() * 1000) * 1000000 + random.randint(100000, 999999))

# ====== Step 1: 调用 parseSql 解析字段 ======
sql = "select count(*) cout, sex from sys_user group by sex"
encoded_sql = urllib.parse.quote(sql, safe='')
parse_result = api_request(f'/online/cgreport/head/parseSql?sql={encoded_sql}')
print('解析结果:', json.dumps(parse_result, ensure_ascii=False, indent=2))

if not parse_result.get('success'):
    print('SQL 解析失败:', parse_result.get('message'))
    exit(1)

# ====== Step 2: 构造字段配置 ======
items = [
    {
        "id": gen_id(), "cgrheadId": None,
        "fieldName": "cout", "fieldTxt": "人数",
        "fieldWidth": None, "fieldType": "String",
        "searchMode": None, "isOrder": None, "isSearch": None,
        "dictCode": None, "fieldHref": None,
        "isShow": "Y", "orderNum": 0,
        "replaceVal": None, "isTotal": None,
        "createBy": None, "createTime": None,
        "updateBy": None, "updateTime": None, "groupTitle": None
    },
    {
        "id": gen_id(), "cgrheadId": None,
        "fieldName": "sex", "fieldTxt": "性别",
        "fieldWidth": None, "fieldType": "String",
        "searchMode": None, "isOrder": None, "isSearch": None,
        "dictCode": "sex", "fieldHref": None,
        "isShow": "Y", "orderNum": 1,
        "replaceVal": None, "isTotal": None,
        "createBy": None, "createTime": None,
        "updateBy": None, "updateTime": None, "groupTitle": None
    }
]

# ====== Step 3: 构造请求 ======
graph_data = {
    "dbSource": "",
    "name": "统计男女比例",
    "code": "tj_user_sex",
    "displayTemplate": "tab",
    "xaxisField": "sex",
    "yaxisField": "cout",
    "dataType": "sql",
    "graphType": "bar",
    "cgrSql": sql,
    "onlGraphreportItemList": items,
    "paramsList": []
}

# ====== Step 4: 调用 add API 创建图表 ======
result = api_request('/online/graphreport/head/add', graph_data)
print('创建结果:', json.dumps(result, ensure_ascii=False, indent=2))

if result.get('success'):
    print('\n图表创建成功！')
else:
    print('\n创建失败:', result.get('message'))
```

**编辑图表脚本差异：**

```python
# 编辑时用 PUT 方法，且 items 使用 graphreportHeadId
graph_data = {
    "id": "existing_head_id",
    "name": "统计男女比例",
    "code": "tj_user_bysex",
    "cgrSql": sql,
    "xaxisField": "sex",
    "yaxisField": "cout",
    "yaxisText": "",
    "content": None,
    "extendJs": None,
    "graphType": "line,bar",
    "isCombination": "combination",
    "displayTemplate": "tab",
    "dataType": "sql",
    "dbSource": "",
    "tenantId": 0,
    "lowAppId": None,
    "onlGraphreportItemList": [
        {
            "id": "existing_item_id",
            "graphreportHeadId": "existing_head_id",
            "fieldName": "cout", "fieldTxt": "人数",
            "isShow": "Y", "isTotal": "N",
            "searchFlag": "N", "searchMode": None,
            "dictCode": "", "fieldHref": None,
            "fieldType": "String", "orderNum": 0,
            "replaceVal": None
        }
    ],
    "paramsList": []
}
result = api_request('/online/graphreport/head/edit', graph_data, method='PUT')
```

### Step 8: 生成菜单 SQL（可选）

> **默认不创建菜单、不授权。** 只有用户明确说「挂菜单」「授权」「发布」时才执行此步骤。

图表创建成功后，可生成菜单 SQL：

> **重要**：菜单 URL 使用图表的 **head_id**，不是 code。
> 路由格式：`/online/graphreport/chart/{head_id}`

```python
# 查询刚创建的图表，获取 head_id
list_result = api_request(f'/online/graphreport/head/list?code={urllib.parse.quote(report_code)}')
if list_result.get('success') and list_result['result']['records']:
    head_id = list_result['result']['records'][0]['id']
    report_name = list_result['result']['records'][0]['name']
    print(f'\n图表 ID: {head_id}')
    print(f'\n### 菜单 SQL（可选执行）')
    print(f"""
INSERT INTO sys_permission (
  id, parent_id, name, url, component, component_name,
  is_route, is_leaf, keep_alive, hidden, hide_tab, description,
  del_flag, rule_flag, status, internal_or_external,
  perms_type, sort_no, menu_type, route_redirect
) VALUES (
  '{head_id}', NULL, '{report_name}',
  '/online/graphreport/chart/{head_id}',
  'super/online/graphreport/auto/GraphreportAutoChart',
  NULL,
  1, 1, 0, 0, 0, NULL,
  0, 0, '1', 0,
  '0', 1.0, 1, NULL
);
""")
```

### Step 9: 输出结果

**本地环境自动执行菜单 SQL 规则：**
如果 API_BASE 以 `http://127.0.0.1` 或 `http://localhost` 开头（不区分大小写），在生成菜单 SQL 后，自动通过 Bash 工具执行 MySQL 命令插入菜单：

```bash
# 先检查是否已存在，避免重复插入
mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3 -e "SELECT id FROM sys_permission WHERE id='{head_id}'"
# 不存在则执行插入
mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3 -e "INSERT INTO sys_permission (...) VALUES (...);"
```

- 如果 MySQL 执行失败，回退为输出 SQL 让用户手动执行，不中断整体流程
- 数据库连接参数默认 `mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3`，与 jeecg-codegen 保持一致

```
## Online 图表创建成功

- 图表编码：{code}
- 图表名称：{name}
- 图表类型：{graphType}
- X 轴：{xaxisField}
- Y 轴：{yaxisField}
- 字段数量：{N} 个
- 目标环境：{API_BASE}
- 菜单 SQL：{已自动执行 ✓ / 需手动执行}

### 菜单 SQL
INSERT INTO sys_permission (...) VALUES (...);

### 后续操作
1. 打开 JeecgBoot 后台 → Online图表
2. 找到该图表，点击「功能测试」预览效果
3. 如菜单未自动执行，手动执行上方 SQL 或在后台手动添加
4. 可在「编辑」中调整图表类型、字段等配置
```

---

## 高级功能

### 组合图表

支持在同一图表中展示多种图表类型：

```json
{
    "graphType": "line,bar",
    "isCombination": "combination"
}
```

组合图表会在同一坐标系中同时展示折线和柱状图。

### Y 轴标签 (yaxisText)

自定义 Y 轴显示文字：
```json
{
    "yaxisText": "人数（单位：人）"
}
```

### JS 增强 (extendJs)

#### 全局变量

| 变量 | 说明 |
|------|------|
| `headId` | 当前图表的 ID |
| `onClick` | 用于添加点击事件的全局对象 |

#### 添加点击事件

通过 `onClick.图表类型 = function(event) {}` 的方式挂载，**不同图表类型分别定义**：

```javascript
// 柱状图点击
onClick.bar = function(event) {
    this.$message.success('点击了柱状图！')
}

// 折线图点击
onClick.line = function(event) {
    this.$message.info('点击了折线图！')
}

// 饼图点击
onClick.pie = function(event) {
    this.$message.info('点击了饼图！')
}
```

#### `this` 上下文（可用 API）

extendJs 中函数体的 `this` 指向一个固定对象（源码 `onClickThis`），包含以下可用属性：

| 属性 | 类型 | 说明 |
|------|------|------|
| `this.$message` | Ant Design Message | **轻提示**（顶部小条，自动消失） |
| `this.$confirm` | Modal confirm | **确认对话框**（需传入 options 对象） |
| `this.$info` | Modal.info | **信息对话框** |
| `this.$success` | Modal.success | **成功对话框** |
| `this.$error` | Modal.error | **错误对话框** |
| `this.$warning` | Modal.warning | **警告对话框** |
| `this.$router` | Vue Router | **路由跳转** |
| `this.$http` | defHttp (Axios) | **HTTP 请求** |

**`$message` — 轻提示（最常用）：**
```javascript
this.$message.success('操作成功')   // 绿色
this.$message.info('提示信息')      // 蓝色
this.$message.warning('注意！')     // 黄色
this.$message.error('发生错误')     // 红色
this.$message.loading('加载中...')  // 转圈
```

**`$confirm` / `$info` / `$success` / `$error` / `$warning` — 模态对话框：**
```javascript
// $confirm：带确认/取消按钮的对话框
this.$confirm({
    iconType: 'warning',
    title: '确认操作',
    content: '职业：' + event.name + '，确认查看详情？',
    onOk: () => {
        this.$router.push('/detail?occupation=' + event.name)
    },
    onCancel: () => {}
})

// $info / $success / $error / $warning：纯展示对话框（只有关闭按钮）
this.$success({ title: '成功', content: '数值：' + event.value })
this.$info({ title: '信息', content: event.name + ' 的平均薪资：' + event.value })
```

**`$router` — 路由跳转：**
```javascript
// 跳转到系统内部页面
this.$router.push('/system/user')
// 带参数跳转
this.$router.push({ path: '/online/cgreport/xxx', query: { occupation: event.name } })
```

**`$http` — HTTP 请求（defHttp，Axios 封装）：**
```javascript
onClick.bar = function(event) {
    var self = this  // 保存 this 引用，供回调中使用
    self.$message.loading('查询中...')
    self.$http.get({
        url: '/sys/user/list',
        params: { occupation: event.name }
    }).then(function(res) {
        self.$message.success('查到 ' + res.total + ' 条记录')
    })
}
```

> ⚠️ **注意**：`$http` 回调（`.then`/`.catch`）中 `this` 已不是 `onClickThis`，必须提前用 `var self = this` 保存引用，或改用箭头函数。

#### 事件参数 (event)

> Online 图表底层使用 **ECharts**，`event` 是标准 ECharts 事件对象（不是自定义对象）。
> 直接打印 `event` 会看到 `[object Object]`，需要读取具体属性。

**通用参数（柱状图 / 折线图 / 饼图均有）：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `event.name` | string | **X 轴类目值**（柱/线）或**扇区名称**（饼） |
| `event.value` | number | **Y 轴数值**（柱/线）或**扇区数值**（饼） |
| `event.seriesName` | string | 系列名称（Y 轴字段的 fieldTxt） |
| `event.seriesType` | string | 系列类型：`'bar'`、`'line'`、`'pie'` |
| `event.dataIndex` | number | 数据在数组中的索引（从 0 开始） |
| `event.color` | string | 当前元素颜色（十六进制） |

**饼图额外参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `event.percent` | number | ECharts 自动计算的百分比（如 `66.7`），可直接使用 |

```javascript
onClick.bar = function(event) {
    // event.name = X轴类目，event.value = Y轴值，event.seriesName = 系列名
    this.$message.info('X轴: ' + event.name + '，值: ' + event.value)
}
```

```javascript
onClick.line = function(event) {
    // ECharts 折线图：只有点击数据点才触发，点击连接线不触发事件
    this.$router.push('/detail?name=' + event.name)
}
```

```javascript
onClick.pie = function(event) {
    // event.name = 扇区名称（字典翻译后的文本，如"男"/"女"）
    // event.percent = ECharts 自动计算的百分比
    this.$message.info(
        '点击了：' + event.name
        + '，值：' + event.value
        + '，占比：' + event.percent.toFixed(1) + '%'
    )
}
```

**组合图（line,bar）区分系列：**

```javascript
// 组合图注册两个事件，通过 event.seriesName 区分点击的是哪条系列
onClick.bar = function(event) {
    this.$message.success('[柱] ' + event.name + '：' + event.value)
}
onClick.line = function(event) {
    this.$message.info('[线] ' + event.name + '：' + event.value)
}
```

### 自定义内容 (content)

用于自定义渲染模板或说明内容。

### AIGC — AI 自动生成图表

系统内置 AI 生成能力，可基于已有的 Online 表单（cgform）表，通过自然语言描述需求自动生成图表配置：

```
POST /online/graphreport/head/api/aigc?cgformTableName={表名}&prompt={需求描述}
```

- `cgformTableName`：Online 表单的数据库表名（如 `oa_leave`）
- `prompt`：用自然语言描述图表需求（如 "统计各部门请假次数"）
- 超时建议设为 60000ms

**返回结构：**
```json
{
  "success": true,
  "result": {
    "code": "dept_leave_count",
    "name": "各部门请假次数",
    "cgrSql": "SELECT dept, COUNT(*) as cnt FROM oa_leave GROUP BY dept",
    "graphType": "bar",
    "xaxisField": "dept",
    "yaxisField": "cnt",
    "displayTemplate": "tab",
    "onlGraphreportItemList": [...]
  }
}
```

AIGC 返回的配置可直接作为 add 接口的请求体使用，通常无需修改即可创建。

### 参数化查询

图表支持两种参数语法，注意区分：

#### 自定义参数：`${参数名}`

在 SQL 中用 `${}` 拼接 WHERE 条件，`{}` 内的文本就是参数名，需与 paramsList 中配置的 `paramName` **完全一致**。

**文本类型参数必须加引号：**
```sql
-- 文本字段加引号
SELECT count(*) cnt, dept FROM sys_user
WHERE status = '${status}' AND dept = '${dept}'
GROUP BY dept

-- 数字字段不加引号
SELECT * FROM order WHERE amount > ${min_amount}
```

对应的 paramsList 配置：
```json
[
    {"paramName": "status",     "paramTxt": "状态",   "paramValue": "1",  "orderNum": 1},
    {"paramName": "dept",       "paramTxt": "部门",   "paramValue": "",   "orderNum": 2},
    {"paramName": "min_amount", "paramTxt": "最低金额", "paramValue": "0", "orderNum": 3}
]
```

**使用方式：**
- URL 传参：`/online/graphreport/chart/{head_id}?status=1&dept=研发部`
- 菜单配置时直接在 URL 上设置固定值
- 未传参则使用 `paramValue` 中配置的默认值

#### 系统变量：`#{变量名}`

系统变量用 `#{}` 语法（**不是** `${}`），由系统自动注入当前登录用户信息，无需配置到 paramsList：

```sql
SELECT * FROM sys_user
WHERE org_code = '#{sys_org_code}'
  AND create_by = '#{sys_user_code}'
  AND create_time >= '#{sys_date}'
```

**可用系统变量：**

| 变量名 | 说明 | 版本要求 |
|--------|------|---------|
| `sys_user_code` | 当前登录用户账号 | - |
| `sys_user_name` | 当前登录用户真实姓名 | - |
| `sys_date` | 当前系统日期 | - |
| `sys_time` | 当前系统时间 | - |
| `sys_org_code` | 当前登录用户部门编号 | - |
| `tenant_id` | 当前登录用户租户 ID | v3.4.5+ |
| `sys_base_path` | Java 服务 basePath（仅 API 模式支持） | v2.4.4+ |

> **混用示例**（自定义参数 + 系统变量）：
> ```sql
> SELECT dept, count(*) cnt FROM sys_user
> WHERE org_code = '#{sys_org_code}'
>   AND status = '${status}'
> GROUP BY dept
> ```

### 动态数据源

查询非默认数据源的数据：
```json
{
    "dbSource": "second_db"
}
```

---

## API 完整列表

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| SQL 解析（复用报表） | GET | `/online/cgreport/head/parseSql?sql={encodedSql}&dbKey={dbKey}` | SQL 类型字段解析 |
| JSON/API 字段解析 | POST | `/online/graphreport/head/parseField?type=JSON\|API` | JSON 或 API URL 字段解析 |
| 编码重复校验 | GET | `/sys/duplicate/check?tableName=onl_graphreport_head&fieldName=code&fieldVal={code}` | result=true 可用，false 已存在 |
| 新增图表 | POST | `/online/graphreport/head/add` | 创建图表 |
| 编辑图表 | PUT | `/online/graphreport/head/edit` | 修改图表 |
| 查询列表 | GET | `/online/graphreport/head/list?code={code}` | 查询图表列表（分页） |
| 查询详情 | GET | `/online/graphreport/head/queryById?id={headId}` | 按 ID 查询图表头 |
| 查询字段列表 | GET | `/online/graphreport/head/queryOnlGraphreportItemByMainId?headId={headId}` | 查询图表关联字段 |
| 删除单个 | DELETE | `/online/graphreport/head/delete?id={id}` | 删除图表 |
| 批量删除 | DELETE | `/online/graphreport/head/deleteBatch?ids={id1,id2}` | 批量删除 |
| 获取图表数据 | GET | `/online/graphreport/api/getChartsData?id={id}&params={json}` | 图表展示时拉取渲染数据 |
| 获取参数配置 | GET | `/online/graphreport/params/listByHeadId?headId={id}` | 图表展示时拉取参数列表 |
| AI 生成图表 | POST | `/online/graphreport/head/api/aigc?cgformTableName={表名}&prompt={需求}` | AIGC 自动生成配置，超时 60s |
| 导出 Excel | GET | `/online/graphreport/head/exportXls` | 导出图表配置 |
| 导入 Excel | POST | `/online/graphreport/head/importExcel` | 导入图表配置 |

---

## 与其他 Skill 的区别

| Skill | 产出物 | 适用场景 |
|-------|--------|---------|
| `jeecg-graphreport` | Online 图表配置（SQL 驱动，数据可视化） | 柱状图、折线图、饼图等数据可视化 |
| `jeecg-onlreport` | Online 报表配置（SQL 驱动，数据列表） | 数据查询报表、统计列表、数据导出 |
| `jeecg-onlform` | Online 表单配置（元数据驱动，CRUD） | 数据录入管理表单 |
| `jeecg-codegen` | Java + Vue3 代码 + SQL | 需要自定义业务逻辑的模块 |
| `jeecg-desform` | 设计器表单 JSON | 数据采集、审批表单 |

---

## 常见问题

### Q1：Y 轴数据错乱 / 图表显示异常

**现象**：柱状图或折线图的 Y 轴数值顺序混乱，或显示不正确。

**原因**：Y 轴字段的 `fieldType` 不是数值类型。parseSql 默认将所有字段解析为 `String`，渲染时按字符串排序（如 `"10" < "9"`），导致显示错乱。

**解决方案**：将 Y 轴字段的 `fieldType` 改为对应的数值类型：

| 字段值特征 | 应设置的 fieldType |
|-----------|-------------------|
| 整数（count、人数、数量） | `Integer` |
| 小数 / 金额 / 均值 | `BigDecimal` |
| 长整数 | `Long` |

**示例**：

```python
# 错误：Y 轴字段 fieldType 是 String，图表会乱序
build_item('monthly_salary', '月薪', field_type='String', ...)

# 正确：数值字段必须用数值类型
build_item('monthly_salary', '月薪', field_type='BigDecimal', ...)
build_item('cnt',            '数量', field_type='Integer',    ...)
build_item('avg_age',        '平均年龄', field_type='BigDecimal', ...)
```

> **注意**：`build_item()` 默认 `field_type='String'`，对 Y 轴数值字段必须手动指定正确类型。

---

### Q2：YApi Mock 创建后续请求报「请登录」

**现象**：`init_yapi()` 调用成功，但紧接着的 `create_mock()` 报「请登录...」。

**原因**：旧版 `init_yapi()` 用 `resp.headers.get('Set-Cookie')` 手动解析响应头，Python 3.12 下该方法只返回第一个 Set-Cookie 值，YApi 登录需要 `_yapi_token` 和 `_yapi_uid` 两个 cookie，手动解析会丢失其中一个。

**解决方案**：`yapi_mock.py` 已重构为 `CookieJar + build_opener` 方式，由标准库自动处理所有 Set-Cookie 响应头，直接调用 `init_yapi(email, password)` 即可，无需任何额外处理。兼容 Python 3.6 / 3.9 / 3.12 及以上版本。

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401/认证失败） | 提示用户重新获取 X-Access-Token |
| `图表编码已存在` / duplicate check 返回 false | 换一个 code 或使用 edit 编辑 |
| parseSql 失败 | 检查 SQL 语法是否正确，表是否存在 |
| Y 轴数据错乱 | Y 轴字段 fieldType 必须为数值类型（Integer/BigDecimal/Long），不能是 String |
| `SQL注入风险` | 不要在 SQL 中使用 DROP/DELETE/UPDATE 等危险语句 |
| 中文乱码 | 确认使用 Python urllib（不要用 curl） |

---

## 实测记录

### 实测 1：新增图表（2026-03-16 验证通过）

**测试场景**：创建「系统登录用户统计分析」图表，按性别统计 sys_user 表用户数量

**配置参数**：
- 图表编码：`tj_login_user`
- 图表名称：系统登录用户统计分析
- 图表类型：`bar`（柱状图）
- X 轴：`sex`（性别）
- Y 轴：`cout`（人数）

**SQL**：
```sql
select count(*) cout, sex from sys_user group by sex
```

**Step 1 — parseSql 解析**：

请求：
```
GET /online/cgreport/head/parseSql?sql=select%20count(*)%20cout%2C%20sex%20from%20sys_user%20group%20by%20sex
```

返回（成功）：
```json
{
  "success": true,
  "code": 200,
  "result": {
    "fields": [
      {
        "id": "2033372375880409089",
        "fieldName": "cout",
        "fieldTxt": "cout",
        "fieldType": "String",
        "isShow": 1,
        "orderNum": 1
      },
      {
        "id": "2033372375880409090",
        "fieldName": "sex",
        "fieldTxt": "sex",
        "fieldType": "String",
        "isShow": 1,
        "orderNum": 2
      }
    ],
    "params": []
  }
}
```

**Step 2 — add 创建图表**：

请求：
```
POST /online/graphreport/head/add
```

请求体：
```json
{
    "dbSource": "",
    "name": "系统登录用户统计分析",
    "code": "tj_login_user",
    "displayTemplate": "tab",
    "xaxisField": "sex",
    "yaxisField": "cout",
    "dataType": "sql",
    "graphType": "bar",
    "cgrSql": "select count(*) cout, sex from sys_user group by sex",
    "onlGraphreportItemList": [
        {
            "id": "1773628737000000123456",
            "cgrheadId": null,
            "fieldName": "cout",
            "fieldTxt": "人数",
            "fieldWidth": null,
            "fieldType": "String",
            "searchMode": null,
            "isOrder": null,
            "isSearch": null,
            "dictCode": null,
            "fieldHref": null,
            "isShow": "Y",
            "orderNum": 0,
            "replaceVal": null,
            "isTotal": null,
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "groupTitle": null
        },
        {
            "id": "1773628737000000654321",
            "cgrheadId": null,
            "fieldName": "sex",
            "fieldTxt": "性别",
            "fieldWidth": null,
            "fieldType": "String",
            "searchMode": null,
            "isOrder": null,
            "isSearch": null,
            "dictCode": "sex",
            "fieldHref": null,
            "isShow": "Y",
            "orderNum": 1,
            "replaceVal": null,
            "isTotal": null,
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "groupTitle": null
        }
    ],
    "paramsList": []
}
```

返回（成功）：
```json
{
  "success": true,
  "message": "添加成功！",
  "code": 200,
  "result": null,
  "timestamp": 1773628737956
}
```

**关键发现**：
1. parseSql 返回的 `fieldTxt` 默认等于 `fieldName`（如 `"cout"`），需 AI 翻译为中文（如 `"人数"`）
2. parseSql 返回的 `isShow` 是数字 `1`，add 时需转为字符串 `"Y"`
3. parseSql 返回的 `fieldType` 全部是 `"String"`，需根据语义修正
4. add 时 items 的 `orderNum` 从 0 开始正常工作
5. add 时 items 中关联 ID 字段名为 `cgrheadId`（值 null），而非 `graphreportHeadId`
6. gen_id() 生成的 19 位数字字符串被 API 正常接受
7. `dictCode: "sex"` 可正确关联系统字典实现值翻译
8. 不需要的字段值传 `null` 即可，不需要传空字符串

### 实测 2：编辑图表（用户提供的接口数据，已验证）

**测试场景**：修改已有图表，将单一柱状图改为组合图表（折线+柱状）

**请求**：
```
PUT /online/graphreport/head/edit
```

**关键字段变化**：
- `graphType` 从 `"bar"` 改为 `"line,bar"`
- 新增 `isCombination: "combination"`
- items 中关联 ID 字段名变为 `graphreportHeadId`（与 add 时的 `cgrheadId` 不同）
- items 中使用 `searchFlag`（`"Y"/"N"`）替代 `isSearch`

**返回**：
```json
{
  "success": true,
  "message": "修改成功!",
  "code": 200,
  "result": null,
  "timestamp": 1773628040311
}
```

**关键发现**：
1. edit 使用 `PUT` 方法（非 POST）
2. edit 时 items 关联字段名为 `graphreportHeadId`，add 时为 `cgrheadId` — **这是最容易踩的坑**
3. edit 时查询字段用 `searchFlag`（`"Y"/"N"`），add 时用 `isSearch`
4. 组合图表需同时设置 `graphType: "line,bar"` 和 `isCombination: "combination"`
5. edit 时需传回 `tenantId`、`createTime`、`createBy` 等系统字段原值


### 实测 3：API 类型图表 + YApi Mock 联合创建（2026-04-16 验证通过）

**测试场景**：创建「人物信息图表」，数据来源为 YApi Mock API，图表类型为 `bar,table`（柱状图 + 数据列表）

**完整流程**：
1. 调用 `init_yapi(email, password)` 登录 YApi（CookieJar 方式，所有 Python 版本通用）
2. 调用 `create_mock('/person_info', '人物信息', [...])` 创建 mock 接口，返回 mock URL
3. 调用 `create_chart(... data_type='api', sql=mock_url ...)` 创建图表

**关键配置**：
- `dataType`: `api`
- `cgrSql`: 填 mock URL（`https://api.jeecg.com/mock/57/claude/person_info`）
- `graphType`: `bar,table`（同时输出柱状图和数据列表）
- mock 数据格式必须包装为 `{"data": [...]}`，`yapi_mock.py` 的 `create_mock()` 已自动处理

**关键发现**：
1. `yapi_mock.py` 的 `init_yapi()` 已改为 CookieJar 方式，无需在调用脚本中自建 opener，直接 `from yapi_mock import init_yapi, create_mock` 即可
2. API 类型图表中 `cgrSql` 字段存放的是 API URL，不是 SQL 语句
3. `graphType: "bar,table"` 可同时展示图表区和数据列表区，满足「既要图又要表」的需求
4. `parseField?type=API` 可跳过——字段已知时直接用 `build_item()` 手动构建 items，同样有效
5. 凭证绝不能硬编码到脚本，从当前上下文中查找，找不到则询问用户，再以参数形式传入
