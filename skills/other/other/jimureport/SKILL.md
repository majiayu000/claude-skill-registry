---
name: jimureport
description: 积木报表生成器 — 自然语言描述报表需求或提供截图，自动生成积木报表（支持数据报表、打印报表、分组报表、循环报表、数据填报等全类型）。Use when user says "积木报表", "jmreport", "Excel报表", "数据填报", "可视化报表", "打印报表", "分组报表", "循环报表", "按照截图生成报表", "创建积木报表", "做一个可视化报表", "积木设计器", "create jimureport", "visual report". Also triggers when user describes report requirements involving Excel-like layouts, data binding with #{}, or multi-sheet reports, or provides a screenshot to generate a report.
---

# 积木报表 AI 生成器

> 不涉及「Online 报表」（cgreport）或「Online 表单」（cgform）。

## 一键脚本（必看，覆盖三类全场景）

写自定义 JSON / Python 之前，先看用户需求是否命中下表现成脚本，命中则**直接调用，禁止重新组装 JSON 或 Python**：

| 用户描述（关键词） | 直接调用 | 默认覆盖 |
|------|---------|---------|
| 「全图表」「所有图表」「图表大全」「测试所有数据集类型」「SQL+API+JSON」「图表展示」 | `python scripts/generate_all_reports.py --base-url ... --token ... --name "..." --mysql-host ... --mysql-port ... --mysql-db ... --mysql-user ... --mysql-pwd ...` | 25 个图表（SQL 12 + API 2 + JSON 4 + 不绑 7），自动建 `chart_demo_all` 表插数据 + 自动创建 YApi mock + 一次保存 |

### 命中规则与禁止事项

- **关键词命中即用**：用户说「生成全部图表」「全图表测试」「演示所有图表」「测试 SQL/API/JSON 三种数据集」时，**第一反应**就是 `generate_all_reports.py`，**不要**回头自己写 chart_entry/echarts 模板
- **3 秒能跑完**：实测 ~3.1s 端到端创建。脚本启动后**不要分块等待、不要发 AskUser 求确认**，直接 `Bash` 等结果
- **Mock 已存在自动复用**：`yapi_mock.py:create_mock` 已修复重复 path 报错，存在则复用 id
- **saveDb 串行**：脚本已改为串行调用 `save_db`，避免 `jimu_report_db_field` INSERT 并发引发 MySQL deadlock
- **新增图表类型时**：在 `CHARTS` 列表加一行，写一个 `tpl_xxx` 函数即可，无需重写主流程

## 执行流程

**第一步（必须）：检查 examples/ 目录**

开始写脚本前，先 Glob `examples/**` 找是否有匹配的示例文件（如 `master-sub-table.md`、`horizontal-group.md` 等）。**找到就必须先 Read，以示例结构为基础生成，不能只看 references/ 规范描述。** 示例文件才是可直接复用的布局模板，规范文件只是参数说明。

> **场景匹配优先于文件名匹配**：`multi-level-header.md` 主要是**交叉表 groupRight/dynamic**，纵向分组+静态多级表头不要读它（浪费 ~30s 读不适用示例）。判断：含 `groupRight()` / `dynamic()` 是交叉表；纯 `group()` + 固定多级表头是本地构造，无需读该示例。

读完本文件后直接 Write JSON 配置 → 执行 CLI 命令 → 输出预览链接。**两步完成，禁止多余动作。**

> **报表名称规则**：用户明确指定名称时直接使用；未指定时 AI 自动生成名称，生成后须调 `GET /jmreport/query/report/folder?pageNo=1&pageSize=10&reportType=&name={name}&token={token}` 检查是否重复，有同名则追加后缀（如 `_2`、`_20260415`）。

| 禁止 | 替代 |
|------|------|
| 读 .py 源码 | CLI 接受 JSON 配置，不用写 Python |
| 找 DB 凭证 | 用 memory 中的配置或问用户 |
| Windows 下 Bash tool 跑 python | **改用 PowerShell tool 跑 `python xxx.py` / `python -c "..."`**，同步返回（详见下方「Windows 执行环境」） |
| 调外部 API 验证字段 | 直接按用户提供的字段写脚本，不预调 API |
| `sleep` + `cat` 轮询输出 | Bash 命令在 Windows 始终被后台化；若仍要走 Bash，**必须用 `TaskOutput(task_id, block=true)` 等待结果**，禁止用 sleep/cat 轮询 |

### Windows 执行环境（强制规则，违反会让用户吐槽"执行太慢"）

**现象**：Windows 的 Bash tool 会把 `python` / `python -c` / skill 脚本当作长命令自动 `run_in_background`，tool 立即返回 background ID，真正输出要等完成通知——把毫秒级调用放大到数秒。

**规则**：
- **Windows（platform=win32）** → 所有 python 调用（脚本 + `python -c` 探测）都用 **PowerShell tool**，同步返回。
- **Linux / macOS** → 用 Bash tool 即可。
- 任何平台都不用 `curl`：跨平台不一致，Windows Bash 下同样被后台化。

**Windows 正确示例**：
```
PowerShell: python <skill_base_dir>/scripts/generate_all_reports.py --base-url ... --token ...
PowerShell: python -c "import urllib.request as u, json; r=u.urlopen(...); print(r.read().decode())"
```

**Windows 错误示例**（会被后台化，用户立即感知到"卡"）：
```
Bash: python generate_all_reports.py ...    ← 返回 "Command running in background with ID: xxx"
Bash: python -c "..."                        ← 同上
Bash: curl -X POST ...                       ← 同上
```

> **历史教训**：曾因默认走 Bash + python 被用户连续吐槽"执行太慢了 / 生成这么慢"。根因是 Bash tool 在 Windows 对 python 也会后台化，不限于 curl。

## 前置条件

用户须提供 **X-Access-Token**。SQL 数据集还需确认数据源（默认留空用服务自带数据源）。

### API 数据集前置询问（用户未提供 API 地址时必须先问）

用户未给出 API 地址时，**必须先询问**：

> 请问接口用哪种方式创建？
> - **mock 接口**：通过 YApi 创建 mock 接口（参见下方「YApi Mock 数据源」章节）
> - **本地代码**：请提供本地 JeecgBoot 项目路径，我直接把 Controller 写入项目

**收到答复后的处理规则：**

| 用户选择 | 处理方式 |
|---------|---------|
| mock 接口 | 按「YApi Mock 数据源」章节流程，用 `yapi_mock.py` 创建 mock 接口，返回 mock URL 填入数据集 |
| 本地代码 | 询问项目路径（如 `D:\path\to\jeecg-boot`），只生成 Controller 写入项目，返回静态数据（`{"data": [...]}`），**不生成** Entity / Mapper / Service / SQL |

## 🚀 CLI 创建（一条命令）

```bash
python /scripts/jimureport_creator.py \
  --api-base http://BASE_URL --token TOKEN --config /path/to/config.json
```

### 配置 A：SQL 普通/分组报表

```json
{
  "action": "create", "reportName": "报表名称", "theme": "blue",
  "datasets": [{"dbCode":"ds1","dbChName":"数据集","dbDynSql":"SELECT col1,col2 FROM t ORDER BY col1","dbSource":"","isPage":"0"}],
  "table": {"datasetCode":"ds1","title":"报表名称","columns":[
    {"field":"col1","title":"列1","width":120,"group":true},
    {"field":"col2","title":"列2","width":100,"funcname":"SUM"}
  ]}
}
```
> columns 可选属性：`group:true`(分组) / `funcname:"SUM"`(聚合) / `subtotalText:"小计"`

### 配置 B：SQL + 图表

```json
{
  "action":"create","reportName":"名称","layout":"chart_bottom",
  "datasets":[
    {"dbCode":"dt","dbChName":"表格","dbDynSql":"SELECT ...","isPage":"1"},
    {"dbCode":"dc","dbChName":"图表","dbDynSql":"SELECT x AS name,y AS value,'' AS type FROM ...","isPage":"0"}
  ],
  "table":{"datasetCode":"dt","title":"名称","columns":[...]},
  "chart":{"datasetCode":"dc","chartType":"bar.simple","title":"图表","width":"650","height":"380"}
}
```
> layout: `chart_bottom` / `chart_top` / `chart_right` / `chart_only`

### 配置 C：JSON 数据集（dbCode 必须字符串！）

```json
{
  "action":"create","reportName":"名称",
  "datasets":[{"dbCode":"my_data","dbChName":"数据","dbType":"3","isList":"1","isPage":"0",
    "jsonData":[{"name":"张三","age":"25"}],
    "fieldList":[["name","姓名"],["age","年龄"]]}],
  "table":{"datasetCode":"my_data","title":"名称","columns":[
    {"field":"name","title":"姓名","width":100},{"field":"age","title":"年龄","width":80}]}
}
```
> **禁止纯数字 dbCode**（如 gen_code()），JSON 数据集模板引擎无法解析。

> **f-string 写绑定字段时必须转义花括号**：`f"#{{{db_code}.{field}}}"` → 生成 `#{db_code.field}`。若写成 `f"#{db_code}.{field}#"` 则花括号被 Python 吃掉，变成 `#db_code.field#`（格式错误，末尾多 `#`，数据不渲染）。

### 配置 D：自定义 rows（复杂多级表头）

build_table_rows 无法满足时（如四级合并表头），传 `customRows` + `customMerges` 跳过自动构建：

```json
{
  "action":"create","reportName":"名称",
  "datasets":[{"dbCode":"ds1","dbType":"3","jsonData":[...],"fieldList":[...]}],
  "table":{"datasetCode":"ds1","columns":[{"field":"f1","title":"F1","width":100}]},
  "groupField":"ds1.group_field",
  "customRows":{"1":{"cells":{"1":{"text":"标题","style":0,"merge":[0,5]}},"height":40}},
  "customMerges":["B2:G2"],
  "customStyles":[{"align":"center","font":{"size":16,"bold":true}},{"align":"center","font":{"bold":true,"color":"#FFF"},"bgcolor":"#4472C4"},{"align":"center","valign":"middle"}],
  "customCols":{"0":{"width":27},"1":{"width":100},"len":100}
}
```

## 修改已有报表

```python
# get_report → 改 design → base_save(**design 展开，get_report 返回的 design 是安全的)
designer, design = get_report(session, report_id)
design["rows"]["3"]["cells"]["1"]["text"] = "新值"
design["chartList"] = filled_charts   # 如有图表回填，直接替换 chartList
session.request("/save", base_save(report_id, designer, **design))
# ↑ get_report 返回的 design 只含 base_save 接受的 key，**design 展开无冲突
# 注意：手动拼的 design dict 禁止 **展开，必须显式列出 rows/cols/styles/merges/chartList
```

## 报表大类

积木报表分为两大类，默认为数据报表：

| 大类 | 说明 | designerObj 关键字段 |
|------|------|-------------------|
| **数据报表**（默认） | 展示型报表，从数据集查询渲染 | `submitForm` 不设置或为 `0` |
| **填报报表** | 在报表上填写数据并提交到后端 | `submitForm: 1` |

## 数据报表类型判断

| 用户描述 | 数据绑定 | 数据集配置 |
|---------|---------|-----------|
| 明细/列表 | `#{db.field}` | isList:"1" isPage:"1" |
| 套打/单条 | `${db.field}` | isList:"0" isPage:"0" |
| 按XX分组 | `#{db.group(field)}` | isPage:"0" |
| 交叉表 | `#{db.groupRight(field)}` + `#{db.dynamic(field)}` | isPage:"0" |

## 单元格绑定字段名获取

写 `#{dbCode.fieldName}` 绑定前，**不得**凭 SQL 别名手写字段名。

**直接用 `parse_sql` 返回的 `fieldName`**（推荐，最快）：

```python
fl = parse_sql(session, sql)
fields = [f["fieldName"] for f in fl]
# MySQL 将所有别名转小写，AS totalAmount → totalamount，直接用即可
```

> `/field/tree/{reportId}` 是备用方案（需报表先 `/save` 存在才能调），`parse_sql` 已返回同样的真实字段名，无需多一次调用。

## 性能优化（单报表推荐模板）

**单报表单数据集场景，以下 3-step 流程总 HTTP ≤ 5 次（含数据源已存在的 1 次）。实测端到端 ~0.8s。**

```python
from jimureport_utils import (
    Session, gen_id, make_designer, make_styles, base_save, report_urls,
    ensure_datasource, parse_and_save_dataset,   # ← 推荐新路径
)

session = Session(BASE_URL, TOKEN)

# ① 确保数据源存在（1-2 HTTP，已存在时只 1 次）
ds_id = ensure_datasource(
    session, name="mongodb", db_type="mongodb",
    db_url="<db_host>:27017/<db_name>",
    db_username="qqyun", db_password="qqyun188"
)

# ② 预生成 report_id（客户端，0 HTTP）
report_id = gen_id()

# ③ parse_sql + saveDb 组合（2 HTTP，report_id 允许尚不存在）
sql = f"select * from mongo.{COLLECTION}"
field_list, db_id = parse_and_save_dataset(
    session, report_id, DB_CODE, "中文名", sql,
    db_source=ds_id, is_list="1", is_page="1"
)

# ④ 构建 rows/cols/styles 后，首次 /save —— 一步创建报表 + 写入布局（1 HTTP）
designer = make_designer(report_id, REPORT_NAME)
session.request("/save", base_save(report_id, designer,
    rows=rows, cols=cols, styles=styles, merges=merges, chartList=[]))
```

| 阶段 | 原来 HTTP | 现在 HTTP | 说明 |
|------|----------|----------|------|
| 数据源 | 3（查+存+再查） | 1-2 | `ensure_datasource` 合并 |
| 首次占位 /save | 1 | **0** | `parse_and_save_dataset` 直接对 orphan report_id 调 saveDb |
| 解析 SQL | 1 | 1 | — |
| 保存数据集 | 1 | （合并在 ③） | — |
| 最终 /save | 1 | 1 | 首次创建 + 写入布局 |
| **合计（已存在数据源）** | **7** | **4** | **省 3 次 HTTP** |

> **关键原理**：saveDb 接受尚不存在于服务端的 `report_id`（orphan），后续 /save 以此 id 首次创建报表时，数据集会正确绑定。实测验证通过。
> `addDataSource` 返回 `result: true`（不返回 id），新建后必须再查一次；`/initDataSource` 无签名比 `/getDataSourceByPage` 快。

### 仍可用的旧路径（保留兼容）

`parallel_init_and_parse` 已不推荐但保留 —— 旧脚本无需修改。新脚本一律用 `parse_and_save_dataset`。

### MongoDB / NoSQL 数据源特别说明

- `testConnection` 仅检测 **TCP 连通**，不验证账号密码。它返回 success 不代表凭证正确。
- 真实鉴权发生在 `queryFieldBySql` / 预览时。凭证错会在这两步报 `Exception authenticating`。
- **禁止**在创建脚本里尝试多种格式（标准分离 / 连接串 / 多 authSource）的试错循环 —— 白白浪费 3-6 秒。只试用户给的一种，失败立刻报错让用户检查 MongoDB 服务端 `db.getUsers()`。

## 性能优化（多数据集 / 多报表场景）

**核心原则：能并行的全部并行，消灭串行等待。**

```python
from jimureport_utils import parallel_parse_sqls, parallel_save_dbs, parallel_create_links
from concurrent.futures import ThreadPoolExecutor

# ① 并行解析所有 SQL（一轮完成）
fl_a, fl_b, fl_c = parallel_parse_sqls(session, [
    {"sql": sql_a}, {"sql": sql_b}, {"sql": sql_c},
])

# ② 并行保存所有数据集（一轮完成）
db_id_a, db_id_b, db_id_c = parallel_save_dbs(session, [
    {"report_id": rid, "db_code": "dsA", "sql": sql_a, "field_list": fl_a, ...},
    {"report_id": rid, "db_code": "dsB", "sql": sql_b, "field_list": fl_b, ...},
    {"report_id": rid, "db_code": "dsC", "sql": sql_c, "field_list": fl_c, ...},
])

# ③ 并行创建所有钻取/联动（一轮完成）
link1, link2, link3 = parallel_create_links(session, [
    {"report_id": rid, "link_name": "钻取1", "link_type": "0", ...},
    {"report_id": rid, "link_name": "钻取2", "link_type": "0", ...},
    {"report_id": rid, "link_name": "联动1", "link_type": "2", ...},
])

# ④ 多张报表最终 /save 并行
with ThreadPoolExecutor(max_workers=2) as ex:
    f1 = ex.submit(lambda: session.request("/save", base_save(rid1, d1, ...)))
    f2 = ex.submit(lambda: session.request("/save", base_save(rid2, d2, ...)))
    f1.result(); f2.result()
```

| 优化点 | 节省 |
|--------|------|
| `parse_sql` 直接取字段名，跳过 `first_save + field/tree` | 每张报表省 2 次请求 |
| `parallel_parse_sqls` | N 次串行 → 1 轮并行 |
| `parallel_save_dbs` | N 次串行 → 1 轮并行 |
| `parallel_create_links` | N 次串行 → 1 轮并行 |
| 多报表 `/save` 并行 | M 次串行 → 1 轮并行 |

## 行列索引规则

- 全部 0-indexed，A列(col0)留空，数据从 col1(B列)开始
- merge: `[extraRows, extraCols]`，0=只占自身
- merges 用 Excel 记法：`"B2:F2"`（UI行号 = code行号+1）

## 分组汇总

| 用户说法 | 实现 |
|---------|------|
| "合计行" | 数据行下方加 `=SUM(列号)` |
| "分组小计" | subtotal:"groupField" + funcname:"SUM" + subtotalText:"小计" |
| 只说"分组" | 只用 group() + aggregate:"group" |

### funcname 聚合函数值（⚠️ 必须严格使用以下字符串，写错则不生效）

| 用户需求 | funcname 值 |
|---------|------------|
| 合计 / 求和 | `"SUM"` |
| 平均 / 平均值 | `"AVERAGE"` （❌ 不是 `"AVG"`） |
| 最大值 | `"MAX"` |
| 最小值 | `"MIN"` |
| 计数 | `"COUNT"` |
| 不聚合（分组列占位） | `"-1"` |

### 分组列 vs 聚合列属性对比

| 属性 | 分组列（group） | 聚合列（select） |
|------|--------------|----------------|
| `aggregate` | `"group"` | `"select"` |
| `subtotal` | `"groupField"` | `"-1"` |
| `funcname` | `"-1"` | `"SUM"` / `"AVERAGE"` / `"MAX"` / `"MIN"` / `"COUNT"` |
| `subtotalText` | 小计行标签文字 | 小计行标签文字 |

## 查询参数（paramList）

**含查询控件时读** `references/query-params.md` § 0（含 SQL FreeMarker 条件、widgetType/searchMode 对照表、日期范围拆分规则）。

## 样式规范（必读约定，无需用户提醒）

- **所有表格报表必须带 border**：优先用 `from jimureport_utils import make_styles` 的 5 种预置样式（索引 0-4）
- **col0 始终留白 30px 不加边框**：标题行从 col1 开始合并（merges 写 `B1:F1` 不含 A 列）。`make_styles()` 预置样式 0-4 均含边框，**col0 必须单独追加无边框样式**：
  ```python
  styles = make_styles()
  styles.append({"align": "center"})  # index 5：col0 专用，无边框
  # 所有行的 col0 统一用 style: 5
  "0": {"text": "", "style": 5}
  ```
- 自定义样式时 `border` 必须嵌套（不能 `**` 展开到顶层），`color`（文字色）与 `font` 平级放 style 顶层

完整规范 + col0 留白模板代码 → `references/styling.md`

## 图表类型速查

**含图表时读** `references/chart-types-quickref.md`（系统名称 → chartType 对照 + series 字段取值 + 地图数据语义规则）。
完整 ECharts 配置模板 → `references/chart-echarts-templates.md`。

## 执行速度规范（3分钟内完成）

文件读取按场景取最小集：

| 场景 | 读取文件 |
|------|---------|
| 普通表格 / JSON数据集（无分组） | 只读 `references/pitfalls.md`（任何场景必读，无豁免） |
| 纵向分组（含小计/聚合） | **必须先读** `references/pitfalls.md` + `examples/vertical-group-subtotal-example.md`，以示例结构为基础生成 |
| 纵向分组 + 自定义排序（textOrders） | 只读 `references/pitfalls.md` + `examples/vertical-group-custom-sort.md`（含完整布局 + json_data 坑） |
| 横向分组（groupRight/customGroup/横向自定义分组） | **必须先读** `references/horizontal-grouping.md` + `examples/horizontal-group.md`，确认绑定语法和布局模板后再写脚本 |
| 含条码/二维码 | 只读 `references/cell-config.md` |
| 含查询控件（paramList） | 只读 `references/query-params.md` § 0 |
| 含图表 | 先读 `references/chart-types-quickref.md`（选 chartType），再读 `references/chart-canonical-configs.md`（结构速查）和 `references/chart-echarts-templates.md`（完整模板） |
| 含表达式 | 只读 `references/expressions.md` |
| 数据填报报表 | 只读 `references/fillform.md` |
| 主子报表（套打式或循环块式） | 只读 `references/mastersub-report.md` |
| 样式细节（边框/留白/优先级） | 只读 `references/styling.md` |
| 数据源管理（MongoDB/Redis/MySQL等 addDataSource） | 只读 `references/dataset-advanced.md` § 1 |
| 有参考报表 ID | `get_report` 照搬，跳过所有文件 |
| 需要示例数据/字段未确定 | 只读 `references/mock-apis.md` 选接口 |

> `pitfalls.md` 常见坑已熟记，不需要每次都读。

## 自定义图表脚本规范（含 SQL/API 数据集）

> 写自定义图表脚本前必须先确认以下规范，杜绝反复调试。

```python
# ① BASE_URL 必须含 /jmreport
session = Session("http://host:port/jmreport", TOKEN)

# ② make_designer：首次 /save 时 report_id 传空字符串
designer = make_designer("", REPORT_NAME)
# !! 拿到 report_id 后，最终保存前必须重新构造 designer（带真实 id），否则单元格数据不会写入 !!
# designer = make_designer(report_id, REPORT_NAME)  ← 最终保存前用这个

# ③ rows 必须带 "len" key
rows = {"len": 200, "1": {"height": 25, "cells": {}}, ...}

# ④ base_save 前两个参数是位置参数，不可用关键字
resp = session.request("/save", base_save("", designer, rows=rows, cols=cols, styles=styles, merges=[], chartList=[]))

# ⑤ 首次 /save 返回的 result 是 dict，取 id
report_id = resp["result"]["id"]

# ⑥ save_db 位置参数顺序（第4个是 db_name，不是 db_ch_name）
db_id = save_db(session, report_id, "db_code", "中文名", sql_or_empty, field_list,
                db_type="1", api_url=mock_url, ...)   # API 数据集

# ⑦ 图表回填：SQL → /qurestSql (result 是 list)；API → /qurestApi (result["data"] 是 list)
# 完整代码见 references/chart-echarts-templates.md § SQL/API 图表数据回填

# ⑧ 最终保存：get_report 返回的 design 可直接 **展开
designer2, design2 = get_report(session, report_id)
design2["chartList"] = filled_charts
session.request("/save", base_save(report_id, designer2, **design2))
```

## 已知坑点（必读）

> **写脚本前先 Read `references/pitfalls.md`**，避免踩坑重试浪费时间。
> **写循环块报表前必须先 Read `references/loopblock-grouping.md`**，里面有完整配置模板，禁止从头自己写。

## 工具脚本（按需使用）

| 操作 | 命令 |
|------|------|
| 查询报表 | `python report_tools.py --base-url URL --token T list [-k 关键词]` |
| 报表详情 | `python report_tools.py --base-url URL --token T detail <id>` |
| 删除/复制 | `python report_tools.py --base-url URL --token T delete/copy <id>` |
| 分享 | `python report_export.py share --name 名称` |
| 导出 | `python report_export.py export <id> --format pdf` |
| 改图表类型 | `python chart_tools.py change-type <id> bar.multi` |
| 创建 YApi Mock | `python yapi_mock.py list` |

## YApi Mock 数据源

报表需要 API 数据源时，使用内置 YApi 平台（https://api.jeecg.com）创建 mock 接口。
**登录凭证处理流程**：
1. 先检查 memory 中是否已有 YApi 凭证记录
2. 有则直接使用；没有则询问用户：
   > 请提供 YApi 登录账号（邮箱）和密码，用于创建 mock 接口。
3. 用户提供后，立即保存到 memory（reference 类型），下次直接读取，无需再问

```python
import sys
sys.path.insert(0, '<skill目录>/scripts')
from yapi_mock import init_yapi, create_mock

init_yapi()  # 自动登录

mock_url = create_mock(
    path='/sales',       # 路径后缀，不含 basepath（/claude）
    title='销售数据',
    data=[
        {"month": "一月", "amount": 12000},
        {"month": "二月", "amount": 15000},
    ]
)
# mock_url = https://api.jeecg.com/mock/57/claude/sales
```

**固定参数**：project_id=57，catid=1157，basepath=/claude

**路径规则**：接口路径只写后缀（如 `/sales`），完整 URL = `https://api.jeecg.com/mock/57/claude/sales`

**分页规则**：自建 mock 接口**不需要分页**，`data` 直接返回完整数组，不加 pageNo / pageSize 参数。

积木报表中使用 mock URL 作为 API 数据集时，调用 `save_db(..., db_type="1", api_url=mock_url)` 即可，`dbCode` 是自定义编码（如 `sales_data`），与 URL 无关。

**fieldList 必须带 `orderNum`**（从 0 开始），否则数据集「排序」列为空，字段顺序不确定：
```python
{"fieldName": "col1", "fieldText": "列1", "fieldType": "String", "orderNum": 0},
{"fieldName": "col2", "fieldText": "列2", "fieldType": "String", "orderNum": 1},
```

### 查询 AI 已创建的接口列表

```python
init_yapi()  # 先登录，自动带上 Cookie

# 列出 project_id=57 下已创建的所有接口（需登录态）
# GET https://api.jeecg.com/api/interface/list?page=1&limit=20&project_id=57
# 返回字段：_id(接口ID), path(路径), title(名称), method, up_time
# 完整 mock URL = https://api.jeecg.com/mock/57{path}
```

命令行等效：`python yapi_mock.py list`（自动登录后分页列出所有接口）

> 冻结/rpbar/钻取联动/searchMode/完整参考文档索引 → 详见 `references/quick-ref.md`
> `references/chart-echarts-templates.md`（含图表时）
> 交叉报表 → `examples/multi-level-header.md`
> 钻取/联动 → `examples/report-drilling.md` / `examples/chart-linkage.md`
