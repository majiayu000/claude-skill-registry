---
name: jimureport
description: 积木报表生成器 — 自然语言描述报表需求或提供截图，自动生成积木报表（支持数据报表、打印报表、分组报表、循环报表、数据填报等全类型）。Use when user says "积木报表", "jmreport", "Excel报表", "数据填报", "可视化报表", "打印报表", "分组报表", "循环报表", "按照截图生成报表", "创建积木报表", "做一个可视化报表", "积木设计器", "create jimureport", "visual report". Also triggers when user describes report requirements involving Excel-like layouts, data binding with #{}, or multi-sheet reports, or provides a screenshot to generate a report.
---

# 积木报表 AI 生成器

> 不涉及「Online 报表」（cgreport）或「Online 表单」（cgform）。

## 临时配置文件规则（强制）

所有传给脚本的 `--config <xxx.json>` 必须写到 **`{系统临时目录}/{SKILL_NAME}/`** 下，由操作系统自动清理；skill 与脚本均不主动删除该目录或文件。

```python
import tempfile, os, json

SKILL_NAME = "<SKILL_NAME>"               # 请替换为实际的技能名称
skill_dir = os.path.join(tempfile.gettempdir(), SKILL_NAME)
os.makedirs(skill_dir, exist_ok=True)          # 确保目录存在，不主动检查

config_path = os.path.join(skill_dir, 'sk_audit_create.json')   # 示例文件名
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
```

`tempfile.gettempdir()` 自动适配：Windows `%TEMP%`、Linux `/tmp`、macOS `/var/folders/.../T`（注意 macOS 并非 `/tmp`）。  
文件名建议使用 **`<表名>_<步骤>.json`**（如 `sk_audit_create.json`），无需重复技能前缀，因路径已包含技能名称，便于排错。

**❌ 禁止：**

- 写到 `<skill>/tmp/` 或当前工作目录（污染 skill / 用户项目）
- 硬编码 `/tmp`、`C:\Temp` 或任何固定路径（不跨平台）
- 每步完成后主动 `rm` / `Remove-Item`（操作系统会清理，属多余 tool call）
- 主动 `os.path.exists()` 检查（其本身即为一次 tool call）  
  （使用 `os.makedirs(…, exist_ok=True)` 满足需求，不算主动检查）

**临时文件可能被操作系统异步清理**，但仍遵循 **乐观调用 + 报错补救**：仅当脚本返回 `FileNotFoundError` 或 `配置文件不存在` 时，使用相同内容、**在相同的 `{系统临时目录}/{SKILL名称}/` 路径下重写**（重写前仍需 `os.makedirs(skill_dir, exist_ok=True)` 确保目录存在），切勿更换路径或回退至 skill 目录。

## 一键脚本（必看，覆盖三类全场景）

写自定义 JSON / Python 之前，先看用户需求是否命中下表现成脚本，命中则**直接调用，禁止重新组装 JSON 或 Python**：

| 用户描述（关键词） | 直接调用 | 默认覆盖 |
|------|---------|---------|
| 「全图表」「所有图表」「图表大全」「测试所有数据集类型」「SQL+API+JSON」「图表展示」 | `python scripts/generate_all_reports.py --base-url ... --token ... --name "..." --mysql-host ... --mysql-port ... --mysql-db ... --mysql-user ... --mysql-pwd ...` | 25 个图表（SQL 12 + API 2 + JSON 4 + 不绑 7），自动建 `chart_demo_all` 表插数据 + 自动创建 YApi mock + 一次保存 |

### 命中规则与禁止事项

- **关键词命中即用**：用户说「生成全部图表」「全图表测试」「演示所有图表」「测试 SQL/API/JSON 三种数据集」时，**第一反应**就是 `generate_all_reports.py`，**不要**回头自己写 chart_entry/echarts 模板
- **3 秒能跑完**：实测 ~3.1s 端到端创建。脚本启动后**不要分块等待、不要发 AskUser 求确认**，直接 `Bash` 等结果
- **Mock 新建必须用唯一路径**：`create_mock` 遇到同路径会**静默覆盖已有接口数据**，污染他人接口。创建新接口时必须在路径末尾追加时间戳或序号（如 `/sales_20260427`），只有用户明确说"修改/更新已有接口"时才可复用原路径
- **saveDb 串行**：脚本已改为串行调用 `save_db`，避免 `jimu_report_db_field` INSERT 并发引发 MySQL deadlock
- **新增图表类型时**：在 `CHARTS` 列表加一行，写一个 `tpl_xxx` 函数即可，无需重写主流程

## 执行流程

**第零步（必须）：Token 优先**

用户消息里没有 X-Access-Token 时，**立刻询问**，拿到 token 后再读任何文件。等待回复期间不要预读文件——等待时间不计入 3 分钟，文件读取时间计入。

> **⚠️ 凭证禁止读记忆，直接问用户**：需要数据库密码、账号密码等任何凭证时，**禁止**读取 memory 文件获取，必须直接在对话中问用户。

**第一步（必须）：按「执行速度规范」表选最小文件集**

> **不要先 Glob examples/**，直接查下方「执行速度规范」表，按场景只读指定文件。禁止在表外额外读文件。
> **场景匹配优先于文件名匹配**：`multi-level-header.md` 主要是**交叉表 groupRight/dynamic**，纵向分组+静态多级表头不要读它（浪费 ~30s 读不适用示例）。

读完指定文件后直接 Write JSON 配置 → 执行 CLI 命令 → 输出预览链接。**两步完成，禁止多余动作。**

> **报表链接格式**（创建成功后直接输出，禁止调接口验证是否存在）：
> - 设计器：`http://{host}/jmreport/index/{report_id}?token={token}&tenantId=1`
> - 预览：`http://{host}/jmreport/view/{report_id}?token={token}&tenantId=1`

> **报表名称规则**：用户明确指定名称时直接使用；未指定时 AI 自动生成名称，生成后须调 `GET /jmreport/query/report/folder?pageNo=1&pageSize=10&reportType=&name={name}&token={token}` 检查是否重复，有同名则追加后缀（如 `_2`、`_20260415`）。

**utils 子模块速查**（需确认某函数签名时，Grep 对应小文件，禁止读全量 jimureport_utils.py）：

| 需要确认的函数 | 读哪个文件 |
|--------------|----------|
| Session、gen_id/code/layer、col_letter、_compute_sign | `jimureport_core.py` |
| parse_api、parse_sql、save_db、update_db、parse_and_save_dataset、parallel_parse/save/api | `jimureport_dataset.py` |
| make_designer、base_save、get_report、report_urls、print_summary | `jimureport_report.py` |
| make_styles、**STYLE_BASE/DATA/HEADER/TITLE/LINK**（命名常量，禁止用魔法数字） | `jimureport_styles.py` |
| chart_entry、virtual_row、build_chart_layout、update_chart_config、parallel_fill_charts、**pick_chart_axes** | `jimureport_chart.py` |
| create_link、parallel_create_links | `jimureport_link.py` |
| ensure_datasource、find_datasource、get_ds_connection、query_mysql、**execute_ds** | `jimureport_datasource.py` |

| 禁止 | 替代 |
|------|------|
| 读全量 jimureport_utils.py | 按上表 Grep/Read 对应子模块（各 25-175 行） |
| **Grep/Read `jimureport_gen.py`（任何原因）** | `api_dataset/group/standard` 等函数的签名和参数在 SKILL.md 调用示例中已完整给出（base_url 默认 http://192.168.1.6:8085/jmreport，无需传），"不确定参数"不构成读源码的理由，直接信任文档 |
| **Grep/Read `jimureport_creator.py` 确认是否支持某功能**（如 fieldList searchMode、paramList 等） | SKILL.md 的 JSON 配置模板和禁止表已覆盖所有场景，直接写 JSON 配置执行，禁止读源码验证 |
| **Grep/Read `jimureport_dataset.py` 查看 parse_sql 实现** | `parse_sql` 接受含 FreeMarker 条件的 SQL，服务端以空参评估后解析字段列表，直接调用即可，无需看源码 |
| 找 DB 凭证 | 用 memory 中的配置或问用户 |
| Windows 下 Bash tool 跑 python | **改用 PowerShell tool 跑 `python xxx.py` / `python -c "..."`**，同步返回（详见下方「Windows 执行环境」） |
| 调外部 API 验证字段 | 直接按用户提供的字段写脚本，不预调 API |
| 擅自调用 `create_mock()` 或 `init_yapi()` | **⛔ 用户已提供接口 URL 时，直接 `save_db(api_url=URL)`，严禁调用 `create_mock()` / `init_yapi()` / 任何 YApi 登录或验证操作**；只有用户明确说"帮我创建 mock 接口"或完全未提供 URL 时才调用；URL 已知 = 直接用，不验证、不询问、不登录 |
| `sleep` + `cat` 轮询输出 | Bash 命令在 Windows 始终被后台化；若仍要走 Bash，**必须用 `TaskOutput(task_id, block=true)` 等待结果**，禁止用 sleep/cat 轮询 |
| 报表创建后调接口验证是否存在 | `/save` 返回 `success:true` 即成功，直接输出设计/预览链接，无需查报表列表 |
| **手写 border 样式**（`{"style":1}` 或任何非数组格式） | **必须用 `make_styles()` 获取 styles 列表**，它已内置正确的 `["thin","#d8d8d8"]` 数组格式；手写 border 一律禁止，会导致整表渲染空白 |
| **`customRows` 配合空 `columns: []`** | creator 靠 `columns` 生成 `queryInfo.dbf`；`columns` 为空则不写入绑定元数据，报表预览**完全无数据**（即使数据集 `records=N`）。`customRows` 只控制视觉布局，`columns` 必须填数据集的实际字段（至少一个）|
| **用户未指定的可选参数自行填值**（如 `customEditConf.eventParams`、`freeze`、`rpbar`、`background` 等） | 只写用户明确给出的字段，其余可选参数一律省略，不得自造默认值 |
| 调 `report_urls()` 工具函数当作 dict 用（如 `urls['designer']`） | `report_urls(report_id, base_url, token, tenant)` 返回 **tuple `(preview_url, design_url)`**，不是 dict；且第一个参数是 report_id 不是 base_url。**直接按本节"报表链接格式"拼字符串**，不要调用此函数 |
| **报表创建走自定义 .py 脚本** | ⛔ **必须用 JSON 配置文件 + `jimureport_creator.py` CLI**：只写 `xxx.json` → `python jimureport_creator.py --api-base URL --token TOKEN --config xxx.json`。需要同时创建 YApi mock 的 API 数据集报表，用 `jimureport_gen.api_dataset(..., mock_data=[...], mock_path="/xxx_日期")` 一步完成，内部自动生成 JSON 并调 CLI，无需手写 Python 脚本。用户反馈（2026-05-22 再次确认）："以后只生成JSON"。**⚠️ 典型错误场景1**：用户要求自定义样式，AI 认为高级函数不支持样式就手写 `rows/cols/styles/save_db/base_save`——严重违规。**⚠️ 典型错误场景2**：场景复杂（含钻取+图表+建表），AI 直接写 `drill_demo.py` 等全流程 Python 脚本——严重违规。正确做法：报表结构部分始终写 JSON；建表/链接创建等 JSON 不支持的步骤写成最小独立 PowerShell inline；两部分分开，不混写。|
| **PowerShell `Out-File -Encoding utf8` 写 JSON** | 产生 UTF-8 BOM 导致 `json.load` 报 `Unexpected UTF-8 BOM`。**必须用**：`[System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding $false))` |

### Windows 执行环境（强制规则，违反会让用户吐槽"执行太慢"）

**现象**：Windows 的 Bash tool 会把 `python` / `python -c` / skill 脚本当作长命令自动 `run_in_background`，tool 立即返回 background ID，真正输出要等完成通知——把毫秒级调用放大到数秒，历史上多次让单报表从 1 分钟拖到 18 分钟。

**规则**：
- **Windows（platform=win32）** → 用 **PowerShell tool** 直接执行 `python xxx.py`，同步返回。禁止用 Bash tool 跑 python（会被后台化）。
- **Linux / macOS** → 用 Bash tool 直接调用 `python xxx.py`。
- 任何平台都不用 `curl`：跨平台不一致，Windows Bash 下同样被后台化。

**脚本执行前强制检查（2 项）**：
1. ✅ Windows 下用 **PowerShell tool** 执行 `python xxx.py`，**不是** Bash tool
2. ✅ 脚本第一行已加编码声明：`import sys; sys.stdout.reconfigure(encoding='utf-8')`（防 GBK 崩溃重试）

**Windows 正确示例**：
```
PowerShell: python <skill_base_dir>/scripts/xxx.py --base-url ... --token ...
```
> `<skill_base_dir>` 是本 SKILL.md 所在目录，运行时用实际路径替换，禁止写死 `C:/Users/...`。

**Windows 错误示例**：
```
Bash: python generate_all_reports.py ...    ← 返回 "Command running in background with ID: xxx"
Bash: curl -X POST ...                       ← 同上
```

> **历史教训**：曾因默认走 Bash + python 被用户连续吐槽"执行太慢了 / 生成这么慢"。根因是 Bash tool 在 Windows 对 python 会后台化，不限于 curl。另一常见重试原因：脚本缺编码声明导致 `UnicodeEncodeError: 'gbk' codec`，加第2项检查可消除。
> **典型症状**：报表生成完成后仍等待约 2 分钟才结束——这是 Bash 后台化的直接表现：脚本已跑完但 tool 在等 background 完成通知。遇到此现象立即确认是否误用了 Bash tool，改 PowerShell 即可消除。

## 前置条件

用户须提供 **X-Access-Token**。

### SQL 数据集数据源选取（用户未指定 `dbSource` 时必须执行）

**正确流程（必须每次执行，不可跳过）：**

1. 调 `GET /jmreport/initDataSource` 获取数据源列表
2. 按用户提供的数据库名（如 `jeecg-boot-cr`）**精确匹配** `name` 字段，取其 `id`
3. 找不到再询问用户

> **⚠️ 禁止用 memory 中存的数据源ID直接跳过查询**：memory 里的ID可能已过期或被重建，必须每次查询后按名字匹配拿到当前有效ID。memory 只用于记住数据库名，不用于记住ID。
> **⚠️ 禁止全量拉取后遍历猜测**：有明确数据库名时直接按名字匹配，不要靠含"积木"等模糊规则。

按以下规则处理：

| 返回结果 | 处理方式 |
|---------|---------|
| `result` 为空数组 | 告知用户需要先在积木报表中新增数据源，停止创建 |
| `result` 非空，存在 `name` 含"积木"的项 | 自动选该项，将其 `id` 作为 `db_source` 传入 `save_db` |
| `result` 非空，无含"积木"的项 | 列出所有数据源名称，询问用户选哪个，等待回复后再继续 |

接口返回字段：每项包含 `id`（传给 `db_source`）和 `name`（展示给用户）。

**脚本中直接调用**（禁止在脚本里重新手写此逻辑）：

```python
from jimureport_utils import resolve_db_source
# 用户未指定数据源时：
db_source = resolve_db_source(session)   # 自动选含「积木」的；无则抛 RuntimeError 列出清单
```

`RuntimeError` 消息已包含数据源列表，捕获后直接转告用户即可。

> **上下文优先**：本次对话中已经通过 `resolve_db_source` 或用户回复确定过 `db_source`，后续同一会话的报表直接复用，**不得重复调用 `initDataSource`**。
> **⚠️ 禁止全量拉取后遍历猜测**：不要拉取全部30+数据源再靠名字模糊匹配，应按用户提供的数据库名精确查找，或直接读 memory。全量拉取是浪费 + 容易选错。

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

> **⚠️ `table.columns` 与 `customRows` 同时存在时，`columns` 仍不可为空数组 `[]`**
> creator 依赖 `columns` 来生成 `designerObj` 中的 `queryInfo.dbf`（数据集绑定元数据）。
> 若 `columns: []`，`queryInfo.dbf` 不会写入，报表预览将**完全空白（无数据）**，即使数据集已保存成功（`records=N`）。
> **正确做法**：`columns` 填入数据集的实际字段（哪怕只有一个），`customRows` 再覆盖视觉布局；两者独立互不影响。

### 配置 E：含钻取（drilling）——**无需任何额外 Python 脚本**

`drilling` 和 `linkages` 键已**内置**于 creator：creator 自动调用 `/link/saveAndEdit` 并把 `linkIds` 回填到 cells / chart extData，全程只需一个 JSON 文件。

```json
{
  "action": "create",
  "reportName": "主报表（三种钻取演示）",
  "theme": "blue",
  "layout": "chart_bottom",
  "datasets": [
    {
      "dbCode": "sales", "dbChName": "学校汇总",
      "dbDynSql": "SELECT leibie AS name, SUM(jine) AS value, '' AS type, 'jeecg.com' AS website FROM school_demo GROUP BY leibie ORDER BY value DESC",
      "dbSource": "1161942757348524032", "isPage": "0"
    }
  ],
  "table": {
    "datasetCode": "sales", "title": "学校汇总报表",
    "columns": [
      {"field": "name",    "title": "类别（点击→子报表）", "width": 140},
      {"field": "value",   "title": "总金额",              "width": 120},
      {"field": "website", "title": "官网（点击→jeecg.com）","width": 180}
    ]
  },
  "chart": {
    "datasetCode": "sales", "chartType": "bar.simple",
    "title": "各类别总金额（点击柱子钻取）", "width": "560", "height": "360"
  },
  "drilling": [
    {
      "name": "钻取1-报表钻取报表",
      "linkType": "0",
      "targetReportId": "<detail_report_id>",
      "ejectType": "0",
      "source": {"type": "cell", "field": "name"},
      "params": [
        {"paramName": "leibie", "paramValue": "name", "fieldName": "name", "dbCode": "sales", "tableIndex": 0}
      ]
    },
    {
      "name": "钻取2-图表钻取报表",
      "linkType": "0",
      "targetReportId": "<detail_report_id>",
      "ejectType": "0",
      "source": {"type": "chart"},
      "params": [
        {"paramName": "leibie", "paramValue": "name", "fieldName": "", "dbCode": "sales", "tableIndex": 0}
      ]
    },
    {
      "name": "钻取3-网络钻取",
      "linkType": "1",
      "targetUrl": "http://jeecg.com",
      "ejectType": "0",
      "source": {"type": "cell", "field": "website"},
      "params": [
        {"paramName": "school", "paramValue": "name", "fieldName": "name", "dbCode": "sales", "tableIndex": 0}
      ]
    }
  ]
}
```

**drilling 字段说明：**

| 字段 | 说明 |
|------|------|
| `linkType` | `"0"` 报表钻取 / `"1"` 网络链接 |
| `targetReportId` | linkType=0 时填目标报表 ID；linkType=1 时留空 |
| `targetUrl` | linkType=1 时填外部 URL |
| `ejectType` | `"0"` 新窗口 / `"1"` 当前窗口 |
| `source.type` | `"cell"` 单元格触发 / `"chart"` 图表触发 |
| `source.field` | cell 时填数据集字段名（creator 自动匹配含该字段的数据行单元格并回填 `linkIds`） |
| `params[].paramValue` | 单元格钻取填字段名；图表钻取填 `name`（X轴）/ `value`（Y轴）/ `seriesName` |

> **跨报表钻取的顺序**：先创建子报表拿到 `detail_id`，再把 `detail_id` 填入主报表 JSON 的 `targetReportId`，两个 JSON 分别跑 CLI 即可，无需额外 Python 脚本。

### 配置 F：NoSQL 数据集（ES / MongoDB / Redis）

`dbType` 填 `"es"/"mongo"/"mongodb"/"redis"`，creator 自动补 Calcite schema 前缀；`dbSource` 必填数据源 ID。

```json
{"action":"create","reportName":"名称",
 "datasets":[
   {"dbCode":"esDs",    "dbChName":"ES员工",   "dbType":"es",    "esIndex":"jmreport_test_employee","dbSource":"<ES数据源ID>",    "isPage":"1"},
   {"dbCode":"mongoDs", "dbChName":"Mongo订单", "dbType":"mongo", "mongoCollection":"orders",        "dbSource":"<Mongo数据源ID>", "isPage":"1"},
   {"dbCode":"redisDs", "dbChName":"Redis缓存", "dbType":"redis", "dbDynSql":"SELECT * FROM cache",  "dbSource":"<Redis数据源ID>", "isPage":"0"}
 ],
 "table":{"datasetCode":"esDs","title":"员工列表","columns":[
   {"field":"emp_id","title":"工号","width":80},{"field":"emp_name","title":"姓名","width":100}
 ]}
}
```

| 字段 | 说明 |
|------|------|
| `esIndex` | ES 专用简写，自动生成 `SELECT * FROM es.{索引名}`；有它可省略 `dbDynSql` |
| `mongoCollection` | MongoDB 专用简写，自动生成 `SELECT * FROM mongo.{集合名}` |
| `dbDynSql` | 显式 SQL；ES/Mongo 缺 `es.`/`mongo.` 前缀时自动补全；Redis 原样传入 |

> ES 字段名若与 Calcite 保留字冲突（`position`/`date`/`type`/`value` 等），需反引号转义或改用 `esIndex` 简写（`SELECT *` 无需列出字段名，天然规避）。详见 pitfalls.md §数据库数据源。

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

> **⚠️ Bug 修复必须用 patch 脚本，禁止重跑创建脚本**
> 任何情况下发现已有报表存在问题（无论是用户反馈还是 AI 自己发现），正确做法是写一个独立 patch 脚本（`get_report` → 改局部字段 → `base_save` 回写；数据集错误用 `update_db`），**不得修改并重新执行创建脚本**。重跑创建脚本会生成新 ID 的报表，原报表（含已配置的权限、分享链接、引用关系）不会被修复，且产生垃圾报表。

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

### API 数据集快速路径（2 HTTP，实测 ~0.5s）

API 数据集无需 `queryFieldBySql`，字段手动定义，整个流程只需 **2 次 HTTP**：

```python
from jimureport_utils import Session, gen_id, make_designer, base_save, save_db

session = Session(BASE_URL, TOKEN)

# ① 客户端生成 report_id（0 HTTP）
report_id = gen_id()

# ② saveDb：orphan report_id 合法，直接绑定（1 HTTP）
field_list = [
    {"fieldName": "f1", "fieldText": "字段1", "widgetType": "String", "orderNum": 0, "tableIndex": 0, "extJson": "", "dictCode": ""},
    # ... 其余字段
]
save_db(session, report_id, DB_CODE, "数据集名称",
        API_URL, field_list,
        db_type="1", api_url=API_URL, api_method="0",
        is_list="1", is_page="0")

# ③ /save：首次创建报表 + 完整设计一步完成（1 HTTP）
designer = make_designer(report_id, REPORT_NAME)
session.request("/save", base_save(
    report_id, designer,
    rows=rows, cols=cols, styles=styles, merges=merges, chartList=[],
    isGroup=True, groupField=f"{DB_CODE}.group_field",   # 交叉/分组报表需要
))
```

| 旧流程（3 HTTP） | 新流程（2 HTTP） |
|----------------|----------------|
| POST /save 空报表 → 取 report_id | `gen_id()` 本地生成（0 HTTP） |
| POST /saveDb | POST /saveDb（同） |
| POST /save 完整设计 | POST /save 完整设计（同） |

> 实测：区域省份销售额交叉报表，3 步 ~3s → 2 步 ~0.5s（2026-04-22 验证）。
> 适用场景：所有 API 数据集报表（交叉表、分组表、明细表均可）。

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

> 🚨 **分组列开 `subtotal:"groupField"` 时，所有数值列必须默认 `aggregate:"select"` + `funcname:"SUM"`**——否则小计/合计行的数值单元格全部空白，UI 上"显示了合计标签 + 数值列空白"是绝对不允许的折中状态。要嘛不显示合计行（分组列改 `subtotal:"-1"`、`subtotalText:""`），要嘛数值列全部默认求和。AI 不得只搬模板里"分组列带 subtotal、数值列裸 text"的写法。

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

### 字段查询 vs 报表参数查询（必读规则）

| | 字段查询（fieldList searchFlag） | 报表参数查询（paramList） |
|---|---|---|
| SQL | 纯 `SELECT`，**不加 WHERE / FreeMarker 条件** | 必须加 `<#if isNotEmpty(x)>...` 条件 |
| fieldList | `searchFlag=1` + `searchMode` + `dictCode` 等 | 无需设置 searchFlag |
| paramList | **不需要** | 必须配置 paramList |
| querySetting | 无需设置 | 按需配置 izOpenQueryBar |

> **核心规则**：字段查询时 JimuReport 引擎自动处理过滤，SQL 保持纯净；只有使用报表参数时才在 SQL 中添加 FreeMarker WHERE 条件。两种方式**不能混用**。

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
- **⚠️ 凡是自定义 styles 数组或修改单元格配置，必须先读 `references/styling.md`**，不得凭经验猜属性层级（`color` 在顶层而非 `font` 内是高频踩坑点，引擎静默忽略错误写法）

完整规范 + col0 留白模板代码 → `references/styling.md`

## 图表类型速查

**含图表时读** `references/chart-types-quickref.md`（系统名称 → chartType 对照 + series 字段取值 + 地图数据语义规则）。
完整 ECharts 配置模板 → `references/chart-echarts-templates.md`。

## 执行速度规范（3分钟内完成）

**开始前强制检查（每次执行前过一遍）：**
1. ✅ 数据源ID已从 memory 读取，未调 `initDataSource`（除非 memory 确实没有）
2. ✅ 数据库驱动用 `pymysql`，不是 `mysql.connector`（该项目环境只有 pymysql）
3. ✅ 样式用 `customStyles` 时，border 格式从已读的示例文件中复用，不额外读 `styling.md`

文件读取按场景取最小集，**只读表中指定的文件，不得额外读其他文件**：

| 场景 | 读取文件（精确，不多读） |
|------|---------|
| 普通表格 / JSON数据集（无分组） | 只读 `references/pitfalls.md`（遇到报错按症状索引跳节，用 offset 只读对应节） |
| 纵向分组（含小计/聚合） | `references/pitfalls.md` §数据集保存（offset=15, limit=40）+ `examples/vertical-group-subtotal-example.md` |
| 纵向分组 + 自定义排序（textOrders） | 只读 `examples/vertical-group-custom-sort.md`；**API 数据集场景**见下方「已知坑点」中的 API+mock+textOrders 条目 |
| **customGroup（自定义横向分组，每条记录→一列）** | **只读 `references/horizontal-grouping.md`**（§5.3.2 已内嵌完整 JSON 模板 + 所有关键属性；无需再读 examples/horizontal-group.md） |
| groupRight + dynamic（交叉表，列头横向动态展开） | `references/horizontal-grouping.md` + `examples/horizontal-group.md` 示例1 |
| groupRight + dynamic + 跟随分组扩展统计行（rightFollowExten） | 只读 `references/horizontal-grouping.md` §「跟随分组扩展统计行」节 |
| 含条码/二维码 / 补全空白行 / 自定义编辑单元格 | 只读 `references/cell-config.md` |
| 含查询控件（paramList） | `references/query-params.md` § 0 + `examples/param-query.md` |
| 含图表（无联动/钻取） | `references/chart-types-quickref.md`（选 chartType）→ `references/chart-canonical-configs.md` + `references/chart-echarts-templates.md`；**图表显示条数/排序/数据过滤需求必须先查 `references/chart-echarts-props.md` §9，禁止改数据集类型或切片数据** |
| 含图表联动 | **只读 `examples/chart-linkage.md`**（已含完整 extData/linkType=2/paramValue="name"/parameter 结构，不需要再读 canonical-configs）；chartType 不确定时才额外读 `references/chart-types-quickref.md`（共 ≤2 个文件）。**严禁读 `pitfalls.md`：该文件 26742 tokens 必超限报错，联动场景也不需要它**。⚠️ API 数据集图表联动复用场景直接用 `scripts/create_chart_linkage.py`；`chart_linkage()` 的 linkages 参数**不生效**，必须 patch（见「已知坑点」） |
| 含报表钻取 | `references/report-drilling.md` + `examples/report-drilling.md` |
| 含表达式 | 只读 `references/expressions.md` |
| 数据填报报表 | 只读 `references/fillform.md` |
| **套打报表**（`${db.field}` 单条绑定，背景图覆盖整张表单） | 只读 `references/misc-config.md` §套打imgList配置（完整代码模板）；坑点摘要见 `references/pitfalls.md` §套打背景图（offset=292, limit=10） |
| 主子报表（套打式或循环块式，子表纵向展开，eri≥40） | `references/mastersub-report.md` + `examples/master-sub-table.md` |
| 分栏报表（loopTime 横向循环，eri=卡片实际行数，禁止缓冲行） | 只读 `references/loopblock-grouping.md` §5（offset=106） |
| 分版（并列独立展开，zonedEdition/zonedEditionList） | 只读 `references/loopblock-grouping.md` §5.5（offset=219，limit=60） |
| **多源报表**（多个数据集来自不同表且有共同关联字段；或用户要求同一行同时绑定主子两表字段） | 只读 `examples/multi-source-table.md` |
| 样式细节（边框/留白/优先级） | 只读 `references/styling.md` |
| **自定义 styles 数组（含 color / bgcolor / font 任意属性）** | **必读 `references/styling.md`**（color 文字色必须放 style 顶层，不能放 font 内；违反则静默失效） |
| **修改已有报表单元格配置（style / merge / text / direction 等）** | **必读 `references/styling.md`**，确认属性层级后再动手 |
| 文件数据集（Excel/CSV/JSON，含用户未提供文件需自动创建的场景） | 只读 `references/dataset-advanced-file.md`（§前置自动创建 + §4.0 上传流程） |
| 数据源管理（MongoDB/Redis/MySQL等 addDataSource） | 只读 `references/dataset-advanced.md` § 1 |
| 报表组合（创建/更新/删除） | 只读 `references/report-group.md` |
| 有参考报表 ID | `get_report` 照搬，跳过所有文件 |
| 需要示例数据/字段未确定 | 只读 `references/mock-apis.md` 选接口 |

> **pitfalls.md 读取规则**：仅「普通表格/无分组」行要求**全节**读取；其他场景遇到运行时报错时，按 pitfalls.md 顶部症状索引找对应节，用 `Read(offset=N, limit=40)` 只读该节（不要全读，9 个节每节约 20 行）。**⚠️ pitfalls.md 共 26742 tokens，任何场景都禁止整文件读取（必超 25000 token 限制报错）；联动/图表场景更是完全不需要读它。**

> **API 数据集 + customGroup 快速路径**（用户提供了 API URL + token 时，不超过 3 步）：
> 1. 读 `references/horizontal-grouping.md` §5.3.2 拿到模板
> 2. 在脚本里调 `parse_api(session, api_url)` 获取字段名（1 次 HTTP，合并进脚本，**不单独执行**）
> 3. 替换模板中的字段名 → PowerShell 执行脚本

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
# ⚠️ JSON数据集（db_type="3"）json_data 必须包裹 {"data":[...]}，不能传裸数组：
#    json_data=json.dumps({"data": raw_list}, ensure_ascii=False)

# ⑦ 图表回填：
#   SQL  → parallel_fill_charts(session, chart_list)
#   API  → parallel_fill_charts(session, chart_list)
#   JSON → parallel_fill_charts(session, chart_list, json_records_map={dbCode: records, ...})
#          JSON 数据集无服务端查询接口，必须通过 json_records_map 传入原始 records 本地填充。
#          不传 json_records_map 则 JSON 数据集图表 config 保持空 data:[]，预览显示空白。
# 完整代码见 references/chart-echarts-templates.md § SQL/API 图表数据回填

# ⑧ 最终保存：get_report 返回的 design 可直接 **展开
designer2, design2 = get_report(session, report_id)
design2["chartList"] = filled_charts
session.request("/save", base_save(report_id, designer2, **design2))

```

## 已知坑点（必读）

> **写脚本前先 Read `references/pitfalls.md`**，避免踩坑重试浪费时间。
> **写循环块报表前必须先 Read `references/loopblock-grouping.md`**，里面有完整配置模板，禁止从头自己写。
> **⚠️ API 数据集有 `paramList` 时，`apiUrl` 末尾必须加 `?paramName=${paramName}`**，否则联动/钻取参数传不进去。多参数用 `&` 连接。写完 `save_db` 后立即目视检查 `api_url` 字符串含占位符。
> **⚠️ 交叉表（groupRight+dynamic）底部跟随分组扩展统计行**：必须用**独立静态行 + `rightFollowExten:"follow"` + Excel公式**（如 `=MAX(G6)`），dynamic 单元格的 `funcname` 必须设为 `"-1"`，**禁止**设为 `"MAX"/"MIN"/"SUM"`——那不会生成跟随横向扩展的统计行。非分组维度字段（如姓名、性别）用 `aggregate:"select"`，不用 `group()`。详见 `references/horizontal-grouping.md` §「跟随分组扩展统计行」。
> **⚠️ 样式 patch 禁止跳过 col "0"**：creator 生成的分组/标准报表，标题格可能在 `rows["1"]["cells"]["0"]`（从 col 0 开始合并所有列）。patch 脚本遍历 cells 时**不得** `if ck == '0': continue`，否则标题样式永远不会被更新。正确做法：遍历所有 col，判断是否有 `merge` 且 text 不以 `#{` 开头即为标题格，直接更新 style。
> **⚠️ mock 路径冲突导致重试**：`create_mock()` 遇到路径已存在会报 RuntimeError。mock_path 末尾必须用**时间戳**（`import time; mock_path=f"/xxx_{int(time.time())}"`）而非固定日期，确保唯一。只有用户明确说"更新已有接口"时才可复用原路径。
> ✅ **API 数据集 dbType 修正与图表 dataType 已内置 creator（2026-05-23）**：`jimureport_creator.py` 现在在保存 API 数据集（`dbType:"1"`）后自动调用 `update_db` 修正 dbType/apiUrl，并在 `/save` 前按数据集实际类型（sql/api/json/javabean/files）自动设置图表 extData 的 `dataType`。**无需再手动 patch**，直接写 JSON config 即可。支持所有类型：SQL→"sql"、API→"api"、JSON→"json"、JavaBean→"javabean"、文件→"files"、共享→"sql"。
> **⚠️ 条码/二维码必须用 display 内联，禁止 displayConfig 浮层**：单元格只写 `"display":"barcode"` / `"display":"qrcode"`，**不加 `"config"` 字段，不在 payload 里传 `displayConfig`**。`displayConfig + config` 方式会创建 floating overlay 叠加层，覆盖表头和其他行，布局完全错乱（2026-05-22 实测）。
> **⚠️ create + patch 必须合并成一次 PowerShell 调用**：需要在创建报表后立即 patch（如添加条码/二维码）时，**不得分两次 PowerShell 调用**。正确做法是在同一个 Python 脚本中：调 `api_dataset()` → 解析 stdout 取 report_id → 立刻调 `get_report + base_save` 完成 patch。分两步会把秒级操作拖成分钟级，且中间报错需人工干预。
> **⚠️ report_id 解析正则用 `report_id=` 锚定，不要靠格式猜**：`jimureport_creator.py` stdout 固定输出 `report_id=<id>` 格式，直接用 `re.search(r'report_id[=:\s]+(\S+)', stdout)` 提取，比按 ID 长度/字符集猜格式更可靠。
> **⚠️ `api_dataset()` 可能返回 `CompletedProcess` 而非 report_id 字符串**：调用后必须做兼容判断，否则后续 `get_report(session, report_id)` 会把整个对象当 ID 发请求导致 400 报错，被迫拆成第二次 PowerShell 执行（秒级变分钟级）。标准写法：
> ```python
> result = api_dataset(...)
> if hasattr(result, 'stdout'):
>     import re
>     report_id = re.search(r'report_id[=:\s]+(\S+)', result.stdout).group(1)
> else:
>     report_id = result
> ```
> **⚠️ 禁止 grep 函数签名**：`api_dataset`、`run_config`、`DEFAULT_BASE_URL` 等参数格式在 SKILL.md 已有完整示例，不需要 grep/read jimureport_gen.py 确认。grep 函数签名每次浪费 3-5 次 tool call，直接信任文档。
> **⚠️ `chart_linkage()` 的 `linkages` 参数被静默忽略**：`jimureport_gen.chart_linkage()` 接受 `linkages` 参数但**不处理它**——函数只创建报表布局，不调用 `/link/saveAndEdit`，linkIds 也不会写入 cells/chartList。正确做法：`chart_linkage()` 创建报表后，必须补一个 patch 步骤：①调 `/link/saveAndEdit` 创建联动记录拿到 link_id；②`get_report` 取设计；③向 cell 写 `linkIds+display:"link"`、向触发图表 extData 写 `linkIds`；④`base_save` 回写。已封装为 `scripts/create_chart_linkage.py`，直接调用。`create_chart_linkage.py` 是提供的工具脚本，直接调用没问题；但若中途失败（如 `list_mocks()` 找不到新建接口），**禁止**重新写一个替代它的全流程 Python 脚本——正确做法是：用已知接口 ID 直接补调 `set_advmock` (最小 PowerShell inline)，报表结构改走 JSON config + creator CLI，联动 patch 另写最小 PowerShell inline，两部分严格分开。
> **⚠️ `chart_linkage()` 传给 creator 的数据集键必须 camelCase**：datasets 里的键用 `dbCode/apiUrl/fieldList/paramList`，table/charts 里的键用 `datasetCode/chartType`。用 `db_code/api_url/field_list` 等 snake_case 会导致 `KeyError: 'dbCode'`（creator 直接读 JSON 字段，不做转换）。
> **⚠️ yapi_mock 不暴露 session 对象，用 `list_mocks()` 获取接口 ID**：`_session`/`session` 等属性均不存在，不要花时间用 `inspect.getmembers` 找 session。正确做法：`init_yapi()` 登录后直接 `from yapi_mock import list_mocks; ifaces = list_mocks()` 获取接口列表，再按 path 匹配找 `_id`。
> **⚠️ `mastersub()` 正确签名是 `(token, name, master_sql, sub_sql, master_cols, sub_cols, *, link_field, sub_param, db_source)`**：`sub_sql` 在第4位，`master_cols` 在第5位，顺序不可对调。调换后 creator 会把 master_cols 列表当 SQL 传给 `queryFieldBySql`，报「签名校验失败」。
> **⚠️ `mastersub()` 只生成套打式布局，不支持循环块式（主子循环）**：调用后 creator 报「未配置 table 或 chart」是因为 mastersub 的 JSON 模板走 `${}` 单值绑定路径，无法生成 loopBlockList。**正确做法**：放弃 `mastersub()`，改用以下 3 步：①`parse_and_save_dataset` 保存主子两个数据集；②手动构建 rows（所有单元格加 `"loopBlock":1`，包括标题行的合并空单元格，缓冲行 eri≥40）；③`base_save` 传入 `loopBlockList=[{"sci":1,"eci":N,"sri":0,"eri":40,"index":1,"db":MAIN_CODE}]`，再调 `/link/saveAndEdit` linkType="4"。完整代码模板见 `references/mastersub-report.md` §二。
> **⚠️ 主子循环报表 JSON config 不支持 `loopBlockList`，creator 会报「未配置 table 或 chart」**：JSON config + creator CLI 路径对循环块式主子报表无效。正确做法分两步：①先跑 JSON config 让 creator 完成数据集保存（datasets 部分正常执行，layout 步骤报错可忽略，report_id 已生成）；②再用最小 PowerShell inline 调 `base_save`（含手动 rows + loopBlockList）+ `/link/saveAndEdit`。两步合并成一次 PowerShell 调用完成。
> **⚠️ 所有图表 config 的 `xAxis`/`yAxis` 必须是对象 `{...}`，禁止数组 `[{...}]`（即使只有一个轴）**：数组格式虽能正常渲染（ECharts 接受），但会让设计器「数据」面板的 `getChartDataList` 在读 `options['xAxis'].data` 时取到 `undefined` 抛 `Cannot read properties of undefined (reading 'length')`，导致 `selectChart` 在 `handleChartExtData` 之前崩溃 → 图表「数据类型」下拉框停留在默认值「Api数据集」，看起来像 JSON/SQL 数据集被当成了 API 数据集。`jimureport_creator.build_echarts_config` 已于 2026-05-26 修正为对象格式；手写 config 或 patch 时同样必须用对象。修复已有报表：`get_report` → 对每个 chart 把 `cfg['xAxis']=cfg['xAxis'][0]`（yAxis 同）→ `base_save` 回写。
> **⚠️ 图表联动中「触发图表」的 `xAxis` 必须是对象格式，否则点击无法触发联动**：`chart_entry()` 生成的柱状图 ECharts config 里 `xAxis` 是数组格式 `[{type:'category',data:[]}]`（标准多轴格式），但前端 `refreshChart()` 更新 X 轴标签时写的是 `chartOptions['xAxis']['data'] = names`——对数组执行此操作只是给数组对象加了个自定义属性，`xAxis[0].data` 仍为空。结果：点击柱子时 ECharts click event 的 `event.name = ""`，联动参数检查 `if(param["name"])` 为 false，目标图表永远不刷新。**修复方法**：报表创建完成后，对每个「充当联动触发源」的柱状图（extData 里有 `linkIds`），把 config 里的 `xAxis`/`yAxis` 从数组改为对象：
> ```python
> import json
> designer, design = get_report(session, report_id)
> for c in design.get("chartList", []):
>     ext = c.get("extData", {})
>     if ext.get("linkIds"):  # 该图表是联动触发源
>         cfg = json.loads(c["config"])
>         if isinstance(cfg.get("xAxis"), list) and cfg["xAxis"]:
>             cfg["xAxis"] = cfg["xAxis"][0]
>         if isinstance(cfg.get("yAxis"), list) and cfg["yAxis"]:
>             cfg["yAxis"] = cfg["yAxis"][0]
>         c["config"] = json.dumps(cfg, ensure_ascii=False)
> session.request("/save", base_save(report_id, designer, **design))
> ```
> 此 patch 应紧接 linkIds 回填步骤之后执行，合并在同一个 PowerShell inline 里。
> **⚠️ API 数据集 + mock + textOrders 自定义排序的正确流程**：报表结构必须在 JSON config，不得把 mock 创建 + 报表创建 + patch 包进同一个自定义 .py 脚本。正确四步（合并成一次 PowerShell 调用）：①最小 inline 脚本（只含 `init_yapi + create_mock`）→ 捕获 mockUrl；②写 JSON config（含 mockUrl，columns 用标准属性，不含 textOrders）；③运行 `jimureport_creator.py` CLI → 捕获 report_id；④最小 inline 脚本（`get_report` → 遍历 cells 加 `textOrders` → `base_save`）。②③④ 在同一次 PowerShell 调用内顺序执行，①可拆出或合并均可。
>
> **⚠️ 多文件数据集（dbType=5）必须拆成两步，禁止合并成一个自定义 Python 脚本**：文件上传 + `saveDb` 是 JSON config 无法表达的前置步骤，但报表布局（rows/cols/styles）仍必须走 JSON + creator CLI。正确拆分：
> - **Step 1（最小 PowerShell inline）**：逐个上传文件（`session.upload('/source/datasource/files/add', ...)`）→ `GET /source/datasource/files/get` 获取 `datasource_id` 和表名 → 构建 JOIN SQL → `queryFieldBySql` 解析字段 → `saveDb` 第一步（无 id）→ 拿 `db_id` → `saveDb` 第二步（带 id，fieldList 才真正持久化） → 输出 `report_id`、`dbCode`
> - **Step 2（JSON config + creator CLI）**：用 Step 1 的 `report_id` 和 `dbCode` 写 JSON layout → `python jimureport_creator.py --config xxx.json`
>
> **Calcite 保留字处理**：`type`、`count` 作为 Excel 列名时，SQL 中必须用反引号转义并起别名（如 `` b.`type` AS prod_type ``，`` a.`count` AS sales_count ``）；双引号（`b."type"`）在 Calcite 中会被解析为字符串字面量导致 `SQL语法错误`。
>
> **⚠️ 文件数据集 Excel/CSV 必须包含至少一行数据**：`/source/dataset/files/single/save` 需要解析文件推断字段类型，纯表头（只有 row1）会返回 `{"success":false,"message":"解析失败,请检查文件格式符合要求"}`。自动创建文件时，row1=表头，row2=一行合理的示例数据（可以是假数据），示例数据不影响报表展示。
>
> **⚠️ 建表脚本必须显式列名 INSERT，且先 DROP 再建**：`INSERT INTO t VALUES (...)` 不写列名时，若目标表已存在且列数/顺序不同，MySQL 报 `Column count doesn't match`，被迫再发一次 PowerShell 调用重试，直接多一个来回（理想 2 次 → 实际 3 次）。正确写法：始终用 `INSERT INTO t (col1, col2, ...) VALUES (...)` 显式列名，建表脚本开头先 `DROP TABLE IF EXISTS`，保证一次成功：
> ```python
> cur.execute("DROP TABLE IF EXISTS my_table")
> cur.execute("CREATE TABLE my_table (id VARCHAR(32) PRIMARY KEY, ...)")
> cur.execute("INSERT INTO my_table (id, name, ...) VALUES (%s, %s, ...)", row)
> ```
>
> **⚠️ 图表 extData 必须同时有 `id` 和 `chartId`，缺 `id` 会导致图表不渲染**：creator 生成的图表 extData 有时只写了 `chartId` 而漏掉 `id`，两者均须等于 `layer_id`。patch 已有报表时若发现 extData 没有 `id` 字段，必须补填：`ext['id'] = c['layer_id']`。症状：预览页图表区域空白，无报错或报 `Cannot read properties of undefined`。
>
> **⚠️ pie.simple 的 extData.series 必须为 `""`，错写 `"type"` 会报 TypeError**：单系列饼图 `series` 字段必须是空字符串，creator 偶尔会错误地设为 `"type"`。前端初始化时会按 series 字段名分组，数据里没有 `type` 列则 `undefined[0]` 报 `TypeError: Cannot read properties of undefined (reading '0')`。patch 时检查并修正：`ext['series'] = ''`。
>
> **⚠️ patch 图表背景色需同时设两处**：图表容器背景是 `chartList[n]['backgroud']`（框架源码拼写错误，实际字段名就是 `backgroud`，不是 `background`），ECharts 画布背景是 `config['backgroundColor']`。只设其中一处效果不完整。正确写法：
> ```python
> c['backgroud'] = {'enabled': True, 'color': '#e8f5e9', 'image': ''}
> cfg = json.loads(c['config'])
> cfg['backgroundColor'] = '#e8f5e9'
> c['config'] = json.dumps(cfg, ensure_ascii=False)
> ```

## 报表创建方式对比（必读）

积木报表有三种创建层级，**优先从上往下选**：

| 层级 | 方式 | 适用场景 |
|------|------|---------|
| ① JSON + CLI（**唯一推荐**） | 写 `xxx.json` → `python jimureport_creator.py --api-base URL --token TOKEN --config xxx.json` | **所有报表**，JSON 文件可见、可复现 |
| ② Python 封装函数 | `from jimureport_gen import group, api_dataset, ...` | 内部自动生成 JSON + 调 CLI，需要同时建 YApi mock 时用此方式 |

> ⛔ **禁止写自定义 Python 脚本创建报表**（用户 2026-05-22 再次明确：**以后只生成JSON**）。报表结构必须写 JSON 配置文件，API dataset + mock 走 `jimureport_gen.api_dataset()`（内部也是 JSON+CLI）。建表、`/link/saveAndEdit` 等 JSON 无法表达的步骤写成最小独立 PowerShell inline，**不得**把报表创建逻辑混进 Python 脚本。
> **⚠️ 典型错误场景3**：图表联动场景（table + 柱图 + 饼图），因 `list_mocks()` 中途失败，AI 把 mock 创建 + `chart_linkage()` 调用 + linkIds patch 全写进一个 `chart_linkage_patch.py` 自定义脚本——严重违规。正确做法：①mock 未设 advmock 时，单独一行 PowerShell inline 调 `set_advmock(已知ID)`；②报表结构写 JSON config → creator CLI；③联动 patch（`/link/saveAndEdit` + `get_report` + `base_save`）写成另一个最小 PowerShell inline；三步各自独立，不混入同一个大 Python 脚本。

### jimureport_gen.py 函数速查

`jimureport_gen.py` 是 `jimureport_creator.py` 的 Python 封装，内部自动写 JSON + 调 CLI。

```python
import sys
sys.path.insert(0, r'<skill_base_dir>/scripts')
from jimureport_gen import group, api_dataset, standard  # 按需 import
```

| 函数 | 报表类型 | 关键参数 |
|------|---------|---------|
| `standard(token, name, sql, columns)` | 普通明细表 | `db_source`, `is_page`, `chart` |
| `group(token, name, sql, columns)` | 纵向分组/小计 | 分组列加 `group=True, subtotalText="合计"` |
| `api_dataset(token, name, field_list, columns, *, api_url=...)` | API 数据集（已有URL） | `report_type="group"` 可改为分组模式 |
| `api_dataset(token, name, field_list, columns, *, mock_data=[...], mock_path=f"/xxx_{int(time.time())}")` | API 数据集（自动建 mock） | 自动创建 YApi mock 接口再建报表，一步完成；mock_path **必须用时间戳**，禁止固定日期 |
| `horizontal_group(token, name, sql, *, group_field, row_fields, value_fields)` | 交叉表 | `statistics_rows` 追加统计行 |
| `param_query(token, name, sql, columns, param_list)` | 带查询条件 | `param_list` 含 searchMode |
| `multilevel(token, name, sql, columns, header_groups)` | 多级表头 | `header_groups=[{"title":"分组","span":3}]` |
| `mastersub(token, name, master_sql, sub_sql, master_cols, sub_cols, *, link_field, sub_param, db_source)` | 主子表**套打**（`${}`单值翻页）| ⚠️ 仅限套打式；循环块式（主子循环）**禁止用此函数**，见「已知坑点」 |
| `loopblock(token, name, sql, columns, *, group_label)` | 循环块 | `group_label` 为分组字段名 |
| `fillform(token, name, sql, columns, *, key_field)` | 数据填报 | `enable_add/edit/delete` |
| `drilling(token, name, sql, columns, drilling_list)` | 报表钻取 | `drilling_list` 含 params |
| `chart_linkage(token, name, datasets, table, charts, linkages)` | 图表联动 | ⚠️ **`linkages` 参数被静默忽略**，函数只创建报表布局不处理联动；datasets 键必须 camelCase（`dbCode/apiUrl/fieldList`）；✅ API 数据集图表 `dataType` 已由 creator 自动修正，无需手动 patch。完整流程见 `scripts/create_chart_linkage.py` |
| `json_dataset(token, name, records, field_list, columns)` | JSON 静态数据集 | `field_list=[["field","名称"]]` |
| `template_print(token, name, sql, cells, bg_image)` | 套打 | `bg_image={"localPath":...,"cols":7,"rows":15}` |
| `file_dataset(token, name, file_path, columns)` | Excel/CSV 文件 | `columns` 的 field 用拼音；**Excel/CSV 必须有至少一行数据（纯表头报"解析失败"）**，自动创建文件时 row2 加一行示例数据 |
| `multisource(token, name, sections)` | 多源横向拼接 | `sections` 含多个数据集 + columns |
| `multisheet(token, name, sheets)` | 多 Sheet | `sheets` 对应 multisheet type 配置 |

**调用示例（API 数据集分组报表，自动建 mock）**：
```python
from jimureport_gen import api_dataset
api_dataset(
    token="xxx",
    name="学生信息统计表",
    field_list=[["grade","年级"],["class_name","班级"],["name","姓名"],
                ["gender","性别"],["age","年龄"],["total_score","总成绩"]],
    columns=[
        {"field":"grade",       "title":"年级",   "width":120, "group":True, "subtotalText":"合计"},
        {"field":"class_name",  "title":"班级",   "width":120, "group":True, "subtotalText":"小计"},
        {"field":"name",        "title":"姓名",   "width":100},
        {"field":"gender",      "title":"性别",   "width":80},
        {"field":"age",         "title":"年龄",   "width":80},
        {"field":"total_score", "title":"总成绩", "width":100, "funcname":"AVERAGE"},
    ],
    mock_data=[
        {"grade":"一年级","class_name":"一班","name":"张三","gender":"男","age":7,"total_score":285},
        # ...更多数据
    ],
    mock_path=f"/student_info_{int(time.time())}",   # 必须用时间戳，禁止固定日期
    report_type="group",
)
```

---

## 工具脚本（按需使用）

| 操作 | 命令 |
|------|------|
| 查询报表 | `python report_tools.py --base-url URL --token T list [-k 关键词]` |
| 报表详情 | `python report_tools.py --base-url URL --token T detail <id>` |
| 删除/复制 | `python report_tools.py --base-url URL --token T delete/copy <id>` |
| 查询报表组合列表 | `python report_tools.py --base-url URL --token T group-list [-k 关键词]` |
| 创建/更新报表组合 | `python report_tools.py --base-url URL --token T group-save --name "名称" --ids "id1,id2" [--names "报表1,报表2"] [--descr "描述"] [--group-id <id>]` |
| 删除报表组合 | `python report_tools.py --base-url URL --token T group-delete <组合ID>` |
| 分享 | `python report_export.py share --name 名称` |
| 导出 | `python report_export.py export <id> --format pdf` |
| 创建定时导出任务 | `python report_export.py schedule-export --name 任务名 --reports '[{"reportId":"id","exportType":"PDF","name":"报表名"}]' --cron "0 0 8 * * ?" [--email xxx@qq.com] [--begin "YYYY-MM-DD HH:mm:ss"] [--end "YYYY-MM-DD HH:mm:ss"]` |
| 修改定时导出任务 | 同上，追加 `--job-id <任务ID>`（创建与修改共用同一接口） |
| 查询定时导出任务列表 | `python report_export.py job-list [--name 关键词]`（接口为 `/auto/export/job/query`，`/list` 返回 404） |
| 删除定时导出任务 | `python report_export.py job-delete <job_id>` |
| 立即执行定时导出任务 | `python report_export.py job-run <job_id>`（返回执行批次号） |
| 启动定时导出任务 | `python report_export.py job-start <job_id>` |
| 停止定时导出任务 | `python report_export.py job-stop <job_id>` |
| 改图表类型 | `python chart_tools.py change-type <id> bar.multi` |
| 创建 YApi Mock | `python yapi_mock.py list` |
| **多文件数据集报表**（Excel/CSV JOIN） | `python multi_file_report.py --token T --files a.xlsx b.xlsx --name "名称" [--join-on product_id] [--db-code myds] [--base-url URL]` |

## YApi Mock 数据源

报表需要 API 数据源时，使用内置 YApi 平台（https://api.jeecg.com）创建 mock 接口。
**登录凭证处理流程（强制，违反导致执行失败重试）**：
1. **动手前必须先读 memory** 中的 YApi 凭证记录（`reference_yapi_credentials.md`），不得跳过
2. 有则直接写入脚本；**没有或 `init_yapi` 认证失败 → 向用户索取新密码，拿到后立即更新 memory**
3. 用户提供后，立即保存到 memory（reference 类型），下次直接读取，无需再问
4. **`init_yapi()` 必须显式传凭证**：`init_yapi(email=EMAIL, password=PWD)`，不传则报"email不能为空"失败
5. **`api_dataset()` 有 `mock_data` 时，必须把凭证直接传给 `api_dataset()`**：`api_dataset(..., yapi_email=EMAIL, yapi_password=PWD)`——内部会再次调用 `init_yapi`，单独提前调 `init_yapi()` 不生效，会报"email不能为空"

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

**⚠️ 新建 vs 修改（严格区分，防止污染他人数据）**：

| 用户意图 | 做法 |
|---------|------|
| 新建接口（默认） | 路径追加时间戳或序号，如 `/sales_20260427`，强制创建新接口 |
| 明确说"修改/更新已有接口" | 直接用原路径调 `create_mock()` 或 `update_mock()` |

> `create_mock()` 遇到同路径会**静默覆盖已有接口数据**，共享项目中会破坏他人接口。默认必须用唯一路径。

**分页规则**：自建 mock 接口**不需要分页**，`data` 直接返回完整数组，不加 pageNo / pageSize 参数。

积木报表中使用 mock URL 作为 API 数据集时，调用 `save_db(..., db_type="1", api_url=mock_url)` 即可，`dbCode` 是自定义编码（如 `sales_data`），与 URL 无关。

**API 数据集查询条件传参规则**：见「已知坑点」章节（含代码示例）及 `references/dataset-core.md` § 3.2.2。

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

### 高级 Mock 脚本（按参数动态返回不同数据）

**自动判断规则（AI 必须遵守）：**

> ⛔ **前提：用户未提供任何 API URL 时，以下规则才生效。用户已提供 URL → 直接 `parse_api` → `save_db`，全程禁止调用 `create_mock` / `init_yapi`，无论报表是否有联动/钻取。**

| 场景                                            | 做法 |
|-----------------------------------------------|------|
| **用户已提供 API URL**（无论是否有联动）                    | ⛔ 禁止创建 mock，直接 `parse_api(url)` → `save_db(api_url=url)` |
| 用户未提供 URL，报表有联动/钻取，数据集需按参数过滤（如 `?category=手机`） | `create_mock` 建接口 → **`set_advmock` 写脚本**，脚本里按 `params.xxx` 分支返回 |
| 用户未提供 URL，静态展示，不需要按参数过滤                      | 只用 `create_mock`，不调 `set_advmock` |

> **⚠️ 正确 API 是 `/api/plugin/advmock/save`，禁止用 `/api/interface/up` 的 `isOpen/script` 字段——那个字段不生效。**

```python
from yapi_mock import init_yapi, set_advmock

init_yapi(email='...', password='...')

# 先用 create_mock / list_mocks 拿到接口 ID，再调：
set_advmock(
    iface_id='5933',   # 接口 _id（字符串）
    script=r"""
if(params.leibie=='手机'){
    mockJson = {"data": [{"name":"苹果手机","value":25500}]}
}else if(params.leibie=='电脑'){
    mockJson = {"data": [{"name":"MacBook","value":47500}]}
}else{
    mockJson = {"data": [...]}   // 兜底默认值，无参数时返回
}
""",
    enable=True,
)
```

**脚本规则：**
- 用 `params.xxx` 读取 URL query 参数
- 用 `mockJson = {...}` 赋值返回体（不是 `return`）
- 必须写兜底 `else` 分支，确保无参数时有数据
- 字段名须与积木报表数据集的 `axisX/axisY`（或 `fieldName`）完全一致

## 常用配置速查

### 冻结行列（freeze）

```python
base_save(report_id, designer, ..., freeze="A3", freezeLineColor="red")
```

| freeze 值 | 效果 |
|-----------|------|
| `"A1"` | 不冻结（默认） |
| `"A2"` | 冻结第 1 行 |
| `"A3"` | 冻结前 2 行 |
| `"C1"` | 冻结前 2 列 |
| `"C3"` | 同时冻结前 2 行和前 2 列 |

### 报表背景色（background）

```python
# 启用背景色（在 base_save override 里传，或 patch 时改 design["background"]）
base_save(report_id, designer, ..., background={"enabled": True, "color": "#e8f5e9"})

# 禁用背景色
base_save(report_id, designer, ..., background=False)
```

> ⚠️ `bgColor` 写在 `make_designer(**extra)` 里**无效**；必须作为 `base_save` 的顶层 override 传递。
> patch 已有报表时：`design["background"] = {"enabled": True, "color": "#hex"}` → `base_save(id, designer, **design)`

### 预览页工具条（rpbar）

> `btnList` / `childrenBtnList` 存的是「**显示**」的按钮编号，从列表中删除编号即可隐藏，`[]` = 全部隐藏。
> `rpbar` 必须是 dict 对象，不能 `json.dumps()`。

```python
base_save(report_id, designer, ..., rpbar={
    "show": True, "pageSize": "",
    "btnList": [1,2,3,4,5,6,7,8,9],
    "childrenBtnList": [7.1,7.2,7.3,7.4,8.1,8.2,8.3,8.4,8.5,8.6]
})
```

| 主按钮 | | 子按钮 | |
|-------|---|-------|---|
| 1 首页 | 5 下一页 | 7.1 默认打印 | 8.1 导出 Excel |
| 2 上一页 | 6 末页 | 7.2 打印当前页 | 8.2 大数据 Excel |
| 3 当前/总页数 | 7 打印 | 7.3 分页缩放打印 | 8.3 导出 PDF |
| 4 分页显示数 | 8 导出 | 7.4 整体缩放打印 | 8.4 导出 PDF 图像 |
| 9 清晰度 | | | 8.5 导出图像 / 8.6 导出 WORD |

### 图表 extData 必填字段

| 字段 | 说明 |
|------|------|
| chartId / id | = layer_id（两个都要填） |
| chartType | bar.simple / pie.normal / line.simple 等 |
| dataType | "sql" / "api" / "json" / "files" / "javabean" |
| apiStatus | "1"=动态SQL / "0"=静态JSON |
| dataId | save_db() 返回值 |
| dbCode | 数据集编码 |
| axisX / axisY | X/Y 轴字段名 |
| series | 分组字段名，单系列传 `""` |

### 钻取/联动 linkType 对照

| linkType | 说明 | reportId | paramValue |
|---------|------|---------|-----------|
| "0" | 报表钻取 | 目标报表 ID | 字段名 |
| "1" | 网络链接 | 当前报表 ID | 字段名 |
| "2" 表格→图表 | 联动 | 当前报表 ID | 字段名 |
| "2" 图表→图表 | 联动 | 当前报表 ID | name/value/seriesName |
| "4" | 主子报表 | 当前报表 ID | — |

- 单元格触发：`cell["linkIds"] = link_id` + `cell["display"] = "link"`
- 图表触发：`extData["linkIds"] = link_id`（放 extData 内部，不在顶层）
- 联动必须有 `linkChartId`（目标图表 layer_id）；目标图表 paramList 必须设 paramValue 默认值

### 图片单元格（本地图片插入）

**⚠️ 禁止对大图（>20KB）用 `base64Img` 内嵌**：base64 编码使 JSON 膨胀到 MB 级，保存/加载极慢。

**正确做法**：先上传拿 URL，再用 `display:"img"` 引用：

```python
from report_tools import upload_image  # 封装好的上传函数
from jimureport_utils import Session

session = Session(BASE_URL, TOKEN)
msg, _ = upload_image(session, r"C:\path\to\image.png")
# OSS 场景 msg 已是完整 https URL；本地存储需拼前缀
img_url = msg if msg.startswith("http") else f"{BASE_URL}/img/{msg}"
```

单元格配置（customRows 或 patch 方式）：
```json
{"text": "http://...oss-url.../image.png", "display": "img", "merge": [extraRows, extraCols]}
```

> `base64Img` 仅限极小图标（< 20KB）。套打背景图同样走 `upload_image`，内部已修正为 `/upload` 端点（2026-05-25）。

### searchMode 映射

| searchMode | 控件 |
|-----------|------|
| 1 | 输入框 |
| 2 | 范围查询 |
| 3 | 下拉多选 |
| 4 | 下拉单选 |
| 5 | 模糊查询 |
| 6 | 下拉树 |
| 8 | 时间控件 |
