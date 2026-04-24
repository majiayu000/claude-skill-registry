---
name: jimubi-dashboard
description: Use when user asks to create/design a dashboard (仪表盘/看板), data kanban, or says "创建仪表盘", "生成仪表盘", "做一个仪表盘", "数据看板", "做一个看板", "创建看板", "数据面板", "统计看板", "运营看板", "create dashboard", "generate dashboard", "design dashboard", "data kanban", "KPI dashboard". Also triggers for QQY/敲敲云 mode dashboards: "敲敲云仪表盘", "低代码应用仪表盘", "应用内仪表盘", "给应用添加图表", mentions appId+tenantId in dashboard context. Also triggers when user describes dashboard/kanban requirements like "做一个运营数据看板" or mentions grid-layout data display like "统计系统数据". Make sure to use this skill for dashboards (仪表盘/看板) — NOT big screens (大屏), which use completely different positioning, styling, and component configurations.
---

# JeecgBoot 仪表盘 AI 自动生成器

将自然语言的仪表盘需求转换为 drag page 配置，并通过 API 自动创建。

> **本 skill 专门处理仪表盘（default）模式**：网格布局（24列栅格），亮色主题，带卡片头，适用于日常数据看板。
> 大屏请使用 `jimubi-bigscreen` skill。

## ⚠️ 强制规则：所有仪表盘相关操作必须优先通过本 skill 处理（无任何例外）

**触发范围**：凡涉及仪表盘的任何操作，包括但不限于：
- 创建/删除/修改仪表盘页面
- 添加/编辑/删除组件
- 数据集（SQL/API/文件/WebSocket）的创建与绑定
- 数据源的创建、编辑、测试（包括修改用户名、密码、连接参数等）
- 模板复制、页面配置修改
- 组件联动、钻取、外部链接

**禁止行为**：
- 未调用本 skill，直接读 memory 找凭据自行执行
- 未调用本 skill，自己探索 API 路径后直接调用
- 以"操作太简单不需要 skill"为由跳过

**正确执行顺序**：
1. 用户提出仪表盘相关需求
2. **第一步必须调用本 skill**（`Skill jimubi-dashboard`）
3. 在 skill 上下文中读取凭据、选择脚本、执行操作

## 按需加载指南

本 skill 采用分层加载：核心规则始终在上下文中，专题文档按需读取。

| 场景 | 读取文件 |
|------|---------|
| **敲敲云（QQY）低代码应用仪表盘** | 核心规则已内联（识别条件/初始化/必填字段/工作流）；完整 config 模板/UI组件配置/批量生成/按钮操作 → 读取 `references/qqy-guide.md` |
| **QQY全组件仪表盘（30统计图表+7UI，一次生成）** | 直接用 `gen_qqy_all_comps.py`（**无需 Write 脚本**）：`PYTHONIOENCODING=utf-8 py gen_qqy_all_comps.py API_BASE TOKEN --page-id PAGE_ID --app-id APP_ID --tenant-id TENANT_ID --form-code FORM_CODE [--form-name 表单名称] [--form-type design\|online]` |
| 需要示例/演示数据（用户未提供数据源）| `references/api-dataset-examples.md`（92条公开 mock API，按行业分类，直接用 `dataset_ops.py create-api` 创建） |
| 创建/绑定/修改数据集（SQL/API/文件）| `references/dataset-guide.md`（**仅自定义脚本时需要**；使用预置脚本时**无需读取**） |
| **多文件数据集（FILES）+ 图表** | 直接用 `files_ops.py create-bind`（**无需 Write 脚本**） |
| 创建 WebSocket 数据集 | `references/dataset-guide.md`「创建 WebSocket 数据集」章节 |
| **多图表+联动批量生成**（≥2个图表且需要联动） | 直接用 `multi_chart_linkage.py` |
| 从模板复制创建仪表盘 | 直接用 `template_ops.py copy` |
| 模板复制遇到问题时 | `references/template-copy-guide.md` |
| 地图组件（JAreaMap 等）| `references/map-guide.md` + 静态数据用 `references/map-static-data.md` |
| 创建数据源 + SQL数据集 + 图表 | `datasource_ops.py create` 创建数据源 → `dataset_ops.py create-sql` 创建数据集 → `comp_ops.py batch-add --specs` 绑定图表（在每个 spec 的 `"config"` 中传入 `dataType:2/dataSetId/dataMapping` 即可，视觉配置由 `default_configs.json` 自动提供）。**仅当 SQL 含 FreeMarker / 需要 queryFieldBySql 回写时，才需写全流程自定义脚本。** |
| 自写 Java API 接口 + API 数据集 + 批量图表 | 参考 `references/pitfalls.md`「完整工作流：自写API接口」章节 |
| **YApi Mock 系统 + API 数据集** | 直接用 `yapi_ops.py create-mock`（固定项目：**proj_id=57，catid=1157，basepath=/claude**） |
| 签名接口 / 数据源管理 / NoSQL 数据源 | `references/signing-datasource-guide.md` |
| 组件联动 / 钻取 | 直接用 `linkage_ops.py` |
| 组件外部链接跳转 | 直接用 `link_ops.py` |
| 字典翻译（jimu_dict） | `references/dict-guide.md` |
| 修改页面配置（背景色/背景图/风格/组件主题）| `references/page-config-guide.md`（**仪表盘无水印功能**，水印仅大屏专有） |
| 遇到奇怪问题时查阅 | `references/pitfalls.md` |
| 组件样式配置路径 | `references/bi-comp-option-config.md`（**仅当 skill.md 中未列出目标组件时才读取**；JStatsSummary/JCapsuleChart/JGauge/JProgress/JScrollBoard/JNumber 已内联在「常用组件配置路径速查」章节） |
| 完整组件类型清单 | `references/bi-component-types.md`（已内联在「图表查询与推荐」章节，一般无需再读取） |
| 新增组件默认尺寸/数据/option | `references/core-configs/component-defaults.md` |
| Online表单/设计器表单生成图表（dataType:4）| `references/online-design-form-chart-guide.md` |
| **bi_utils 初始化 / 字段访问规则** | 已内联在「bi_utils 使用规则（强制）」章节，**无需读取外部文件** |
| **comp_ops.py 参数与数据绑定格式** | 已内联在「快捷操作：comp_ops.py」章节，**无需读取外部文件** |
| **linkage_ops.py 联动/钻取命令** | 已内联在「快捷操作：linkage_ops.py」章节，**无需读取外部文件** |
| **link_ops.py 外部链接 + 自定义JS** | 已内联在「快捷操作：link_ops.py」章节，**无需读取外部文件** |
| 踩坑速查 | 已内联在「核心踩坑速查」章节（~45条），**优先查此处**；极端复杂场景再读 `references/pitfalls.md` |
| 图库（图标/图片）管理 | 已内联在「图库管理」章节，**无需读取外部文件** |

## SQL数据集创建标准流程（强制）

> **触发条件**：用户说"使用SQL数据集"、"增加SQL数据集"、"统计 xxx 表"、"生成图表"等涉及 SQL 数据集的任何场景，必须严格按以下四步执行，**不得跳过第1步**。

### 第1步：确认数据源（必须询问，禁止擅自选择，无任何例外）

> ⚠️ **无论使用任何方式创建 SQL 数据集，都必须先询问数据源，禁止直接执行。**

**执行步骤（强制）：**
1. 先运行 `py datasource_ops.py list API_BASE TOKEN` 列出所有可用数据源
2. 向用户展示列表，询问"请问使用哪个数据源？"
3. 等待用户选择后，用选定的数据源 ID 继续执行

```bash
py datasource_ops.py list "<api_base>" "TOKEN"
```

### 第2步：根据业务场景自行编写SQL
- 用户指定数据源后，根据用户描述的业务场景，自行设计并编写合适的 SQL 语句
- **🚨 comp_ops.py add/batch-add 不支持 `--create-sql`/`--sql-file`/`--ds-name`/`--db-source`**，这些参数不存在，使用会报 `unrecognized arguments`
- **推荐方式（普通SQL，无 FreeMarker 动态条件）**：`dataset_ops.py create-sql` 创建数据集，再用 `comp_ops.py batch-add --specs` 绑定图表；每个 spec 的 `"config"` 字段只需传 `dataType/dataSetId/dataMapping` 等数据绑定字段，视觉配置自动从 `default_configs.json` 取
- **全流程自定义脚本（仅限以下场景）**：SQL 含 FreeMarker 动态参数（`<#if>`/`${}`）、需要 queryFieldBySql 自动回写字段、或需要在同一脚本内串联复杂逻辑时，才用 Write 工具写入 Python 脚本执行（详见下方"全流程自定义脚本模板"章节）
- **⚠️ "singleFile" 是文件数据集的 dataType 值**（`dataType: 'singleFile'`，上传 Excel/CSV），与 SQL 数据集脚本模式无关，禁止把 SQL 场景的自定义脚本称为"singleFile 脚本"

### 第3步：创建SQL数据集
- 分组必须使用 **"示例数据集"**（`dataset_ops.py create-sql` 已内置 `--group "示例数据集"` 默认值）
```bash
py dataset_ops.py create-sql $API_BASE $TOKEN \
  --name "数据集名称" --db-source "数据源ID" \
  --sql "SELECT name, value FROM table GROUP BY name" \
  --fields "name:String,value:Integer"
```
- 数据集创建完成后，**必须执行查询解析验证**确认数据正常返回

### 第4步：后续绑定操作（按需）
- 询问用户是否需要将数据集绑定到图表组件
- 如需要，优先使用 `dataset_ops.py create-sql` + `comp_ops.py batch-add --specs` 组合；仅当场景复杂（FreeMarker/需字段回写）时才写全流程自定义脚本

---

## 执行效率规则（强制）

### 简单操作直接执行，禁止多余探索

**对所有仪表盘操作，必须跳过以下步骤直接执行：**
- 禁止启动 Explore 子代理去探索源码
- 禁止启动子代理去读 data.ts 默认配置（skill 文档已包含完整信息）
- 禁止读取 template-copy-guide.md（template_ops.py copy 已实现全部流程）
- 禁止使用预置脚本时读取 dataset-guide.md（`dataset_ops.py`/`comp_ops.py --dataset-name` 已封装全部逻辑）
- 禁止执行预置脚本前先 `--help` 查看用法（skill 文档已包含完整参数说明）
- 禁止展示设计摘要等待确认（除非用户明确要求确认）

**耗时目标：**

| 操作类型 | 目标耗时 | 做法 |
|---------|---------|------|
| 单组件增/删/改/查 | ≤30s | comp_ops.py 一条命令（cp + 执行 + rm，共 2 轮） |
| 数据集 + 单组件 | ≤60s | singleFile 脚本（7步完整流程：/add → queryFieldBySql → /edit → getAllChartData → config → append → save_page） |
| 复合操作（数据集 + 多组件） | ≤60s | 并行 Bash 调用 |
| 模板复制创建仪表盘 | ≤60s | template_ops.py copy |
| 多图表+联动（≥2图+联动） | ≤10s | `multi_chart_linkage.py` 单脚本 |

### 反模式检查清单（出现任何一条就说明在浪费时间）

- **🚨 添加≥2个组件时用单独的 `add` 并行执行**（并行导致乐观锁冲突丢失组件！必须用 `batch-add --specs '[...]'` 一次保存）
- **🚨 `add` 命令后 chartData 为 `[]`**（comp_ops.py 已从 default_configs.json 加载完整默认数据，出现空数据说明 default_configs.json 未被复制到工作目录）
- **🚨 静态 chartData 禁止使用 comp_ops.py 兜底数据**（default_configs.json 为空时 comp_ops.py 回落到内置占位数据：JBar→A/B/C/D/E、JStackBar→收入/支出，这些是虚构数据。必须从前端源码 `data.ts`（位于 `packages/dragEngine/components/jeecgComponents/data.ts`）中读取各组件 `compConfig.chartData` 的真实值，通过每个 spec 加 `"config":{"chartData":[...]}` 字段，或 singleFile 脚本中调用 `comp_ops._build_comp_config(comp_type, title, {"chartData": json.dumps(real_data)})` 覆盖）
- **⚠️ 创建 SQL 数据集时跳过询问数据源直接执行**（无论使用哪种脚本，执行前必须先 `datasource_ops.py list` 列出数据源，询问用户）
- **⚠️ 用户已给出 API 地址时先用 `--dataset-name` 探测或先添加静态组件**（直接 `dataset_ops.py create-api` → `comp_ops.py add --dataset-name`，2 轮完成）
- **⚠️ singleFile 全流程脚本第4步（add_component）前漏写 query_page + 缓存 template**（漏掉两行缓存代码时，`save_page` 将仪表盘**所有已有组件永久清空**）
- **⚠️ singleFile 场景将"建数据集脚本"和"添加图表脚本"拆成两个**（必须一个脚本完成全部流程）
- **⚠️ singleFile 场景用 `comp_ops.py --dataset-name` 绑定图表**（按字段数组顺序自动映射，导致图表显示错误数据）
- **⚠️ 执行 `py script.py` 时不加 `PYTHONIOENCODING=utf-8`**（Windows 默认 GBK 编码，中文必定乱码）
- **⚠️ cp 依赖文件放在轮次1，py 执行在轮次2**（cp 后文件可能丢失。**必须把 cp 与 py 放在同一命令链**）
- **⚠️ cp 目标路径用 `.` 或 `C:/Users/` 格式**（`.` 不可靠、`C:/Users/` 在 Git Bash 静默失败。**必须用完整 Unix 格式** `/c/Users/<用户名>/bi_utils.py`，含文件名）
- **⚠️ cp 后用 `py -c` 或读取文件来验证文件内容**（多余！直接 Write 脚本并执行即可，中途检查浪费1轮。仅需 `ls` 验证文件存在）
- **⚠️ Write 脚本时写占位符 TOKEN/API_BASE 再单独 Edit 更新**（凭据已在上下文中，必须 Write 时直接填入最终值）
- **⚠️ 多图表+联动场景逐个调用 comp_ops.py + linkage_ops.py**（用 `multi_chart_linkage.py` 单脚本，节省约80%耗时）
- **⚠️ 直接调用 bi_utils.add_xxx() + save_page() 添加组件到已有页面**（会覆盖已有组件！必须先 query_page + 缓存 template）
- **⚠️ 写自定义脚本用 bash heredoc 而非 Write 工具**（heredoc 含单引号必报错）
- **⚠️ 脚本中用拼音/英文替代中文字段名、组件名**（如把"基础柱形图"写成 `JiChu-ZhuXingTu`，用户无法识别）
- **⚠️ 用户未指定数据来源时擅自使用公开 mock API**（必须先执行 Step 0.1 询问数据来源）
- **⚠️ 批量绑定数据集时 dataMapping.filed 写成字段名**（`filed` 是语义槽位标签"维度"/"数值"/"分组"，`mapping` 才是字段名）
- **⚠️ dataMapping 按数组索引顺序映射而非语义映射**（必须按语义显式指定：单系列 `[{维度→name},{数值→value}]`，多系列 `[{分组→type},{维度→name},{数值→value}]`）
- **⚠️ 仪表盘 size 字段用栅格单位**（`config.size.width/height` 必须是像素：`width = w×75, height = h×11`）
- **🚨 QQY全组件仪表盘需要从头 Write 脚本**（直接用 `gen_qqy_all_comps.py` 预置脚本，参数：`--page-id --app-id --tenant-id --form-code`，1轮完成，耗时<2s）
- **🚨 QQY全组件生成前跳过字段确认直接执行脚本**（禁止！必须先查询表单字段，以表格列出并给出推荐配置（维度/数值/分组），等用户确认后再执行 gen_qqy_all_comps.py）
- **⚠️ QQY dataType=4 组件缺少 compStyleConfig 或 analysis**（前端 `useChartBiz.ts` 读取这两个字段，缺少任意一个则 TypeError 白屏；必须包含 `compStyleConfig: {'summary': {'showTotal': False, 'showY': False, 'decimals': 0}}` + `analysis: {}`）
- **⚠️ QQY filter 缺少 conditionFields 字段**（`filter` 对象必须包含 `conditionFields: []`，否则前端"设置"弹窗报错）
- **🚨 QQY seriesType 作用域：只有 JPivotTable + 4个地图 需要非空数组，其余26个统计图表必须是 `[]`**（✅正确：非分组图表 `seriesType:[]`；JPivotTable/JAreaMap/JBubbleMap/JHeatMap/JBarMap 用 `[{"series":"1","type":"bar"},...]`；❌错误：所有图表统一填非空数组，会导致前端 `.map is not a function` 崩溃）
- **⚠️ QQY 仪表盘类（JGauge/JColorGauge/JAntvGauge）nameFields 放了字符串字段**（仪表盘类 nameFields 必须为 `[]`，只有 valueFields）
- **⚠️ QQY 散点图 nameFields 用字符串维度字段**（JScatter/JBubble 的 nameFields 必须是数值类型字段，否则散点图坐标轴无法渲染）
- **🚨 QQY commonOption 作用域：只有 4 个地图类型需要，其余26个统计图表禁止包含**（✅正确：JAreaMap/JBubbleMap/JHeatMap/JBarMap 加 commonOption；❌错误：所有统计图表都加 commonOption，会引入不必要字段干扰渲染）
- **🚨 QQY JHeatMap commonOption 正确值（来自参考JSON）**：`heat:{blurSize:20,pointSize:15,maxOpacity:1}`，`breadcrumb.textColor:'#000000'`，`areaColor:{color1:'#f7f7f7',color2:'#fcc02e'}`，`barColor:'#fff176'`，`barColor2:'#fcc02e'`，`inRange:{color:['#04387b','#467bc0']}`；❌错误：blurSize:13/pointSize:6/textColor:'#ffffff'/不同inRange配色
- **🚨 QQY JHeatMap 四项强制要求**（① `visualMap.show:true`——false 时报 `Heatmap must use with visualMap`；② `visualMap.seriesIndex:[1]`——不是 [0]；③ `commonOption` 必须含 `heat` 字段，`blurSize:20,pointSize:15`；④ `geo.roam:true`）
- **⚠️ QQY 地图 visualMap.seriesIndex 搞错**（JAreaMap→[0]show:false；JBubbleMap→[1]show:false；**JHeatMap→[1]show:TRUE**；JBarMap→[0]show:false）
- **🚨 QQY option 坐标轴颜色禁用 #EEF1FA**（大屏暗色在白底仪表盘看不清；禁止写 axisLabel.color/textStyle.color 覆盖，用默认色）
- **🚨 QQY JWordCloud/JTotalProgress option 必须为 `{title,card}` 只需 title+card，无坐标轴**（加坐标轴/series 反而崩溃）；**JRankingList 需要完整横向条形图 option**（`yAxis:{data:[],type:'category'}` + `xAxis:{type:'value'}` + `series:[{type:'bar'}]` + `grid:{containLabel:true}`，不能是 `{}`）
- **🚨 QQY DoubleLineBar yAxis 必须是双数组**（`yAxis:[{type:'value'},{type:'value'}]`，单对象则第二轴缺失）
- **🚨 QQY HorizontalBar 系 category 必须是 'HorizontalBar'**（JHorizontalBar/JRankingList/JTotalProgress 的 category 写 'Bar' 则方向/样式全错）
- **🚨 QQY JPivotTable isGroup 必须为 True**（False 时透视表不渲染行列分组）
- **🚨 QQY compStyleConfig showField 取值**：`'all'`=全部字段（用户选"全部"时），`'fieldName'`=指定字段，`''`=默认未选；**columnFreeze 必须为 False**（参考JSON权威）；headerFreeze/unilineShow/lineFreeze 为 True
- **🚨 QQY option.card 必须含 headColor:'#FFFFFF'；option.title.text 必须设为组件显示名称**（缺 headColor 导致卡片头色异常；title.text 为空则图表无标题）
- **🚨 QQY assistYFields/assistTypeFields 作用域：只有 JPivotTable + 4个地图 需要填充，其余26个统计图表必须是 `[]`**（✅正确：普通图表 `assistYFields:[]`；❌错误：所有图表统一填 [数值字段]）
- **🚨 QQY JGauge 与 JColorGauge/JAntvGauge option 结构不同**：JGauge 需要 `series:[{min:0,data:[],max:100,axisTick:{lineStyle:{color:'#eee'},show:true},detail:{formatter:'{value}'},type:'gauge'}]`；JColorGauge/JAntvGauge 只需 `{title, card}`（无 series）
- **🚨 QQY JBarMap geo 必须含 aspectScale:0.96 + areaColor:'#37805B' + roam:true**（来自参考JSON；其余地图 areaColor 为空字符串，JHeatMap/JBarMap roam:true，JAreaMap/JBubbleMap roam:false）
- **🚨 QQY JPivotTable pivotTable 子配置必须动态包含所有 num_fields**（`controlList`/`unitList` 必须对每个数值字段建一个条目；只用 VAL[0] 则多值字段的汇总列缺失）
- **🚨 QQY filterField 必须在表单字段前预置5个系统字段**（create_by/update_by/update_time/create_time/bpm_status，缺失则筛选面板不完整）

---

## 仪表盘特征

- **布局**：24 列栅格，坐标和尺寸单位为**栅格单位**（如 x=0, y=0, w=6, h=17）
- **背景色**：支持，字段 `backgroundColor`（`DragEngineDef.vue` 第68行）
- **背景图**：支持，字段 `backgroundImage`
- **风格（style）**：支持 `transparent`/`light`/`dark`/`default`（`DragEngineDef.vue` 第50行）
- **组件主题（theme）**：支持 `default`/`gray`/`green`/`red`/`blue`/`dark`（`DragEngineDef.vue` 第58行）
- **水印**：❌ 不支持（水印仅大屏专有，仪表盘无此功能）
- **卡片头**：图表组件的 `card.title` 应留空（标题由 ECharts `option.title` 显示），避免标题重复
- **颜色体系**：白底 `#FFFFFF`、深灰标题 `#464646`、浅灰轴标签 `#909198`、浅灰网格 `#F3F3F3`

## 仪表盘栅格布局规则

| 组件类型 | 推荐 w | 推荐 h | 说明 |
|---------|--------|--------|------|
| JNumber | 6 | 17 | 数字卡片，4 个一行正好 24 列 |
| JGrowCard/JSimpleCard | 6-8 | 17-22 | 统计增长卡片 |
| JLine/JBar/JSmoothLine | 12-14 | 28-35 | 图表，通常半宽或更宽 |
| JPie/JRing/JRose | 10-12 | 28-35 | 饼图/环形图 |
| JHorizontalBar | 12 | 28-35 | 横向柱状图 |
| JCommonTable | 12 | 30-40 | 数据表格 |
| JList | 12 | 30-40 | 数据列表 |
| JGauge | 6-8 | 25-30 | 仪表盘表盘 |
| JProgress/JCustomProgress | 8-12 | 20-28 | 进度条/进度图 |

**布局原则：**
- 总宽度 24 列，组件 w 之和不要超过 24
- 第一行通常放 4 个 JNumber（w=6×4=24）
- 第二行放图表组合（如 JLine w=14 + JPie w=10 = 24）
- 第三行放表格/排行等

## 前置条件

用户必须提供：
1. **API 地址**：JeecgBoot 后端地址（如 `https://api3.boot.jeecg.com`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

---

## 敲敲云（QQY）仪表盘模式专题

> **本章节专门处理低代码应用（敲敲云）模式下的仪表盘。** 如果用户只是做普通仪表盘，跳过本章节。

### 识别条件（满足任一即进入 QQY 模式）

- 用户提及"敲敲云"、"低代码应用"、"应用仪表盘"、"应用内仪表盘"
- 用户提供了 `appId`（低代码应用 ID）和 `tenantId`（租户 ID）
- 操作上下文是在低代码应用（`/myapp/{appId}/...` 路由）内的仪表盘
- 用户说"给某应用创建仪表盘"、"在应用里加一个图表"

### QQY 模式 vs 标准仪表盘核心区别

| 特性 | 标准仪表盘 | QQY 仪表盘 |
|------|-----------|-----------|
| `isLowApp` | 前端标识，不存库 | 前端标识，不存库（**禁止写入数据库**，仅前端引擎据此切换至 DragEngineQqyun） |
| 组件库来源 | `menuData` | `qqyMenuData`（不含 JBreakRing 等） |
| 主要数据来源 | SQL/API 数据集（dataType=2） | 设计器/Online 表单（dataType=4） |
| 额外前置条件 | 无 | **appId**（应用ID）+ **tenantId**（租户ID） |
| HTTP 附加头 | 无 | `X-Low-App-ID: {appId}` + `X-Tenant-Id: {tenantId}` |
| 仪表盘归属 | 系统级，无应用关联 | 应用级，`lowAppId` 字段关联到具体应用 |
| 数据查询接口 | `getAllChartData` | `getTotalData`（QQY 统计表单数据）|
| 数据集管理 | 前端可见 | 隐藏，用户不感知 |
| 按钮操作 | 无特殊绑定 | 支持创建记录/打开视图/调用业务流程等 5 种 |

### QQY 模式额外前置条件

用户在标准前置条件基础上，**还必须提供**：
3. **appId**（低代码应用 ID）：从页面 URL `/myapp/{appId}/...` 或应用管理中获取
4. **tenantId**（租户 ID）：从系统设置→租户管理中获取，或询问用户

> 若用户未提供 appId/tenantId，**必须先询问**，不得用占位符代替。

### QQY 模式脚本初始化（强制）

QQY 模式下所有脚本必须在 `init_api` 后立即设置额外请求头，**同时创建页面时必须在 body 中显式传入 `lowAppId`**，确保应用归属正确保存到数据库：

```python
import json, time
import bi_utils

API_BASE = '<api_base>'
TOKEN = 'your-token'
APP_ID = '应用ID'          # 低代码应用ID（必填）
TENANT_ID = '1'            # 租户ID（必填）
PAGE_ID = '已有页面ID'     # 或稍后调用 create_page 获取

# QQY 模式初始化（必须设置 extra_headers）
bi_utils.init_api(API_BASE, TOKEN, extra_headers={
    'X-Low-App-ID': APP_ID,
    'X-Tenant-Id': str(TENANT_ID),
})
```

> **⚠️ 创建页面时必须在 body 中传 `lowAppId`（强制）：**
> ```python
> page_resp = bi_utils._request('POST', '/drag/page/add', data={
>     'name': '仪表盘名称',
>     'style': 'default',
>     'lowAppId': APP_ID,   # 必须显式传入，确保存库
>     # ❌ 禁止传 isLowApp：这是前端标识，不存数据库
> })
> ```
> **标准仪表盘**创建时不传 `lowAppId`。

> **证据**：`DragEngine.vue` onMounted 中执行 `localStorage.setItem(ConfigEnum.DRAG_APP_ID, props.lowAppId)`，请求拦截器 `request.js` 中：
> `config.headers[ConfigEnum.LOW_APP_ID] = localStorage.getItem(ConfigEnum.DRAG_APP_ID)`
> 后端 `OnlDragPageController.java`：`String lowAppId = TokenUtils.getLowAppIdByRequest(request)` → 写入 `onlDragPage.setLowAppId(lowAppId)`

### QQY 仪表盘列表查询

QQY 模式下查询应用内的仪表盘列表时，`X-Low-App-ID` 头会自动过滤出该应用的仪表盘。也可以直接用 `lowAppId` 参数过滤：

```python
# 查询指定低代码应用的仪表盘列表
result = bi_utils._request('GET', '/drag/page/list', params={
    'lowAppId': APP_ID,
    'pageNo': 1,
    'pageSize': 50
})
pages = result.get('result', {}).get('records', [])
for p in pages:
    print(p['id'], p['name'])
```

### QQY 可用组件（快速参考）

**统计图表（30个）**：JBar, JStackBar, JMultipleBar, JNegativeBar, JHorizontalBar, JRankingList, JTotalProgress, JLine, JArea, JMultipleLine, DoubleLineBar, JWordCloud, JPie, JRing, JRose, JFunnel, JPyramidFunnel, JRadar, JCircleRadar, JColorGauge, JGauge, JAntvGauge, JNumber, JScatter, JBubble, JPivotTable, JAreaMap, JBubbleMap, JHeatMap, JBarMap

❌ 禁止添加：JDynamicBar, JMixLineBar, JSmoothLine, JProgress, JCommonTable, JList, JGrowCard, JFlyLineMap 等（不在 qqyMenuData 中）

**UI/功能组件（7个）**：JCustomButton（按钮）, JText（文本）, JFilterQuery（查询条件）, JCarousel（轮播图，需绑定imgupload字段）, JDragEditor（富文本）, JIframe（嵌入URL）, JCurrentTime（实时日期）

❌ 禁止添加：JTabs, JGrid, JImg, JCalendar, JWaitMatter, JRadioButton 等

### dataType=4 必填字段（QQY 统计图表核心）

每个 QQY 统计图表 config 必须包含：
1. `dataType: 4` + `formType/formId/formName/tableName/appId/appType`
2. `nameFields/valueFields/typeFields/sorts/filter/filterField`（含 `filter.conditionMode:"and"` + `filter.conditionFields:[]`）
3. `compStyleConfig`（含 `summary/showUnit/assist` 完整结构）
4. `analysis`（含 `showData:1, isRawData:True, showMode:1, trendType:'1'`）
5. 笛卡尔坐标图：`option.series:[{type:'bar/line/scatter'}]` + xAxis/yAxis + grid
6. `chart:{category,subclass,isGroup}` + `seriesType:[]`（JPivotTable/地图除外）

> **完整 config 模板、UI组件配置、批量生成流程、按钮操作类型**：见 `references/qqy-guide.md`

### QQY 仪表盘创建完整工作流

```
Step 1: 确认 appId + tenantId（必须询问用户）
Step 2: 确认仪表盘名称
Step 3: 在 bi_utils.init_api 中设置 extra_headers
Step 4: 调用 /drag/page/add 创建页面，body 中必须显式传 lowAppId: APP_ID（不传 isLowApp）
Step 5: 添加每个统计图表前，必须执行【三步询问流程】（见下方）
Step 6: 将仪表盘菜单归入目标分组（见下方「QQY 仪表盘菜单归组」章节）
Step 7: 创建完成后输出仪表盘 ID 和分享地址（格式：{前端域名}:{端口}/drag/share/{appId}/{pageId}）
```

### QQY 仪表盘菜单归组（创建后必须执行）

QQY 仪表盘页面创建后，其对应的应用菜单项 `parentId` 默认为空（不在任何分组下），**必须手动调用接口将其归入目标分组**，否则在低代码应用侧边栏中无法在分组下看到该仪表盘。

**Step 1：查询应用菜单，找到目标分组 ID**

> ⚠️ 必须用 `appId` 参数过滤，用 `lowAppId` 参数无效（会返回所有应用的菜单）

```python
r = requests.get(f'{API_BASE}/online/lowAppMenu/list', headers=HEADERS,
    params={'appId': APP_ID, 'pageSize': 100})
records = r.json().get('result', {}).get('records', []) or []
# 找 type='group' 的分组，以及 type='drag' 的仪表盘菜单项（parentId 为空即是待归组的）
for m in records:
    if m.get('appId') == APP_ID:
        print(m['id'], m['type'], m['menuName'], m.get('parentId'))
```

**Step 2：调用 edit 接口设置 parentId**

```python
body = {
    'id': MENU_ID,            # 仪表盘菜单项 ID（type='drag' 的那条）
    'parentId': GROUP_ID,     # 目标分组 ID（type='group'）
    'menuName': '仪表盘名称',
    'type': 'drag',
    'menuUrl': PAGE_ID,       # 仪表盘页面 ID
    'appId': APP_ID,
    'orderNum': 4,
}
r = requests.put(f'{API_BASE}/online/lowAppMenu/edit', headers=HEADERS, json=body)
# {"success":true,"message":"编辑成功!"} 即为成功
```

> 注意：请求头必须包含 `X-Low-App-ID` 和 `X-Tenant-Id`，否则鉴权失败。

---

### 🚨 QQY 统计图表三步询问流程（强制，每个统计图表都必须执行）

每次在 QQY 仪表盘中添加**任意一个统计图表**（30个范围内），必须严格执行以下三步，**禁止自行假设表单或字段**：

**Step A：查询并展示可用表单 → 询问用户选择**
```python
# 调用接口
GET /desform/api/list/options?appId={APP_ID}
# 向用户展示：
# | formCode | 表单名称 |
# 询问："请问使用哪个表单？"
# 等待用户选择后继续
```

**Step B：查询并展示字段 → 询问用户选择维度/数值字段**
```python
# 调用接口
GET /desform/api/fields/{formCode}
# 向用户展示字段列表（字段名 + 显示名 + 控件类型），询问：
# "请选择要显示的字段：
#  - 维度字段（nameFields，文字/选项类）
#  - 数值字段（valueFields，数字/金额类）"
# 等待用户确认后继续
```

**Step C：按用户选定的表单 + 字段，构建 dataType=4 完整 config 创建图表**

**禁止行为：**
- ❌ 禁止自行推断"复用页面已有组件的表单"
- ❌ 禁止跳过询问、直接用某个表单或字段
- ❌ 即使应用只有一个表单，也要展示让用户确认
- ❌ 禁止使用 dataType=1 静态数据兜底


**QQY 也支持 dataType=2（SQL/API 数据集），只需额外携带 appId/tenantId 头。**

### QQY 模式不支持的功能

- ❌ **水印**（仅大屏专有）
- ❌ **JBreakRing、JPyramid3D 等大屏专属组件**（不在 qqyMenuData 中）

---

## 交互流程

### Step 0: 解析用户需求

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 页面名称 | 用户指定 | "运营数据看板" |
| 主题 | default | default |
| 组件列表 | 从描述中解析 | 用户总数(数字)、增长趋势(折线)、来源分布(饼图) |

### Step 0.1: 数据来源确认（强制，用户未明确指定时必须询问）

**触发条件：** 用户没有明确说明数据来自哪里（没有给出接口地址、没有指定数据集、没有说用 SQL/mock/自己写代码），则**必须先问用户以下两个问题，不得擅自假设或跳过**：

> **问题一：接口来源**
> 使用 **mock 系统** 还是 **自己编写代码**？
> - **mock 系统**：请提供 mock 服务地址 + 账号密码（如 YApi）
> - **自己编写代码**：请提供代码存放路径（Java Controller 文件全路径）
>
> **问题二：接口需要实现什么业务需求？**
> 描述各组件要展示的数据内容

**可跳过询问、直接执行的情况：**
- 用户已明确说"使用 mock 系统"并提供了地址和账号
- 用户已明确说"写接口"并提供了文件路径
- 用户指定了已有数据集名称或 SQL 数据源
- 任务不涉及数据集创建（如纯样式修改、组件位移、删除等）

### Step 0.5: 模板匹配（优先使用模板布局）

**生成整个仪表盘时，必须先匹配模板，复用已有布局。** 这是最优先的步骤，能确保生成的仪表盘布局专业、美观。

**模板目录**：`references/templates/default/`（29 个仪表盘模板 JSON）

**匹配流程：**

1. **根据用户需求关键词搜索模板**：将用户描述的行业/场景与模板名称进行语义匹配

| 用户需求关键词 | 推荐模板 |
|---------------|---------|
| 销售/订单/电商/运营 | 产品销售数据、某电商公司销售运营看板、某连锁饮品销售看板 |
| 招聘/HR/人事 | 公司年度招聘看板 |
| 金融/银行/封控 | 金融封控数据展示、示例_乡村振兴普惠金融服务 |
| 仓储/库存/物料 | 库存管理可视化大屏 |
| 医院/医疗/医美 | 示例_医院综合数据统计、医美行业网络关注度 |
| 旅游/景区/客流 | 示例_旅游数据监控 |
| 社区/物业/消防 | 示例_智慧社区、物业消防巡检状态 |
| 生产/制造/车间 | 车间生产管理 |
| 门户/首页/工作台 | 企业门户、流程门户、示例_首页 |
| 消费者/权益/投诉 | 消费者权益保护 |
| 数据分析/统计/报表 | 示例_数据分析、示例_数据表格、示例_统计近十日的登陆次数 |
| 查询/联动/筛选 | 示例_查询_联动、示例_日期范围查询、示例_钻取 |
| 通用/综合/看板 | 示例_智能大数据、示例_全组件、示例_首页 |

2. **找到匹配模板** → 使用「模板复制方式」创建仪表盘（参见下方"备选方式：从模板复制创建仪表盘"章节），保留模板的布局和装饰，仅替换业务数据和标题文字

3. **找不到匹配模板** → 随机选择一个通用模板作为布局基础（推荐选择：`示例_智能大数据`、`示例_首页`、`示例_全组件`），同样保留布局和装饰，替换业务数据

> **重要**：只有在用户明确要求"不使用模板"或"从零创建"时，才跳过模板匹配，直接使用 bi_utils 默认组件函数逐个添加。

## 图表查询与推荐（用户询问或需求不明确时）

### 场景一：用户询问"可以使用什么图表"

**触发条件**：用户问"有哪些图表"、"支持什么图表"、"可以用什么图表"、"图表有哪些类型"等。

**处理方式**：直接输出以下完整图表分类表格（无需读取任何文档，无需执行任何脚本）：

| 分类 | 图表名称 | compType |
|------|---------|----------|
| **柱形图** | 基础柱形图 | JBar |
| | 堆叠柱形图 | JStackBar |
| | 动态柱形图 | JDynamicBar |
| | 象形图 | JPictorialBar |
| | 基础条形图 | JHorizontalBar |
| | 背景柱形图 | JBackgroundBar |
| | 对比柱形图 | JMultipleBar |
| | 正负条形图 | JNegativeBar |
| | 折柱图 | JMixLineBar |
| | 双轴图 | DoubleLineBar |
| **饼状图** | 饼图 | JPie |
| | 南丁格尔玫瑰图 | JRose |
| **折线图** | 基础折线图 | JLine |
| | 平滑曲线图 | JSmoothLine |
| | 阶梯折线图 | JStepLine |
| | 面积图 | JArea |
| | 对比折线图 | JMultipleLine |
| **进度图** | 基础进度图 | JCustomProgress |
| | 进度图 | JProgress |
| **仪表盘** | 基础仪表盘 | JGauge |
| | 多色仪表盘 | JColorGauge |
| **环形图** | 饼状环形图 | JRing |
| **散点图** | 普通散点图 | JScatter |
| | 气泡图 | JBubble |
| **漏斗图** | 普通漏斗图 | JFunnel |
| | 金字塔漏斗图 | JPyramidFunnel |
| **雷达图** | 普通雷达图 | JRadar |
| | 圆形雷达图 | JCircleRadar |
| **地图** | 区域地图 | JAreaMap |
| | 散点地图 | JBubbleMap |
| | 飞线地图 | JFlyLineMap |
| | 柱形地图 | JBarMap |
| | 热力地图 | JHeatMap |
| | 柱形排名地图 | JTotalBarMap |
| | 时间轴飞线地图 | JTotalFlyLineMap |
| **表格/列表** | 数据表格 | JCommonTable |
| | 透视表 | JPivotTable |
| | 数据列表 | JList |
| **统计/数字** | 数值 | JNumber |
| | 统计卡片（增长） | JGrowCard |
| | 简洁卡片 | JSimpleCard |
| **首页功能** | 待办事项 | JWaitMatter |
| | 项目列表 | JProjectCard |
| | 快捷导航 | JQuickNav |
| | 最新动态 | JDynamicInfo |
| **交互** | 查询条件 | JFilterQuery |
| | 自定义按钮 | JCustomButton |
| | 选项卡切换 | JTabs |
| | 按钮组 | JRadioButton |
| **辅助** | 图片 | JImg |
| | 文本 | JText |
| | 轮播图 | JCarousel |
| | 富文本 | JDragEditor |
| | Iframe | JIframe |
| | 日历 | JCalendar |
| | 多视图日历 | JMultiViewCalendar |
| | 当前时间 | JCurrentTime |
| | 栅格布局 | JGrid |
| | 自定义ECharts | JCustomEchart |
| **Online/表单** | Online表单 | online |
| | 设计器表单 | design |

### 场景二：用户图表需求不明确时给出推荐

**处理方式**：根据用户数据类型/业务场景，给出 3-5 个建议：

| 数据类型/业务场景 | 推荐图表 | 理由 |
|-----------------|---------|------|
| 占比/构成分析 | JPie、JRing、JRose | 直观展示各部分在整体中的比例 |
| 趋势/时序变化 | JLine、JSmoothLine、JArea | 反映随时间变化的走势 |
| 分类对比 | JBar、JHorizontalBar、JMultipleBar | 比较不同类别的数值大小 |
| 多系列对比 | JMultipleLine、JMultipleBar、JStackBar | 同时展示多个维度的数据 |
| 完成率/进度 | JProgress、JGauge、JLiquid、JRingProgress | 展示目标达成程度 |
| 排行/Top N | JScrollRankingBoard、JCapsuleChart、JDynamicBar | 突出排名先后顺序 |
| KPI/核心指标 | JNumber、JStatsSummary、JCountTo | 大字号展示关键数字 |
| 地理分布 | JAreaMap、JBubbleMap、JBarMap | 展示地理位置相关数据 |
| 转化漏斗 | JFunnel、JPyramidFunnel | 展示各环节转化率递减 |
| 多维综合评估 | JRadar、JBubble | 多维度综合打分或分布 |
| 数据列表/明细 | JScrollBoard、JCommonTable、JScrollTable | 展示多条明细数据 |

**推荐话术：** 列出3-5个图表名+compType+一句话原因，末尾"请选择，我将立即创建"。

---

### Step 1: 识别组件并选择类型

用户说组件名时直接查上方「图表查询与推荐」章节的表格获取 compType，**禁止 Grep 搜索源码**。

**常用仪表盘组件速查：**

| 用户描述关键词 | 组件 component | 说明 |
|---------------|---------------|------|
| 数字/KPI/指标/总数 | `JNumber` | 数字指标卡（带卡片头） |
| 统计卡片/增长卡片 | `JGrowCard` | 带增长率的统计卡片 |
| 柱状图 | `JBar` | 基础柱状图 |
| 横向柱状图 | `JHorizontalBar` | 水平柱状图 |
| 折线图/趋势 | `JLine` | 折线图 |
| 曲线图 | `JSmoothLine` | 平滑曲线 |
| 柱线混合 | `JMixLineBar` | 柱状+折线混合 |
| 饼图 | `JPie` | 饼图 |
| 环形图 | `JRing` | 环形图 |
| 玫瑰图 | `JRose` | 南丁格尔玫瑰图 |
| 表盘 | `JGauge` | 仪表盘表盘 |
| 进度条 | `JProgress` | 进度条 |
| 雷达图 | `JRadar` | 雷达图 |
| 漏斗图 | `JFunnel` | 漏斗图 |
| 地图 | `JAreaMap` | 区域地图 |
| 数据表格 | `JCommonTable` | 数据表格 |
| 数据列表 | `JList` | 数据列表 |
| 日历 | `JCalendar` | 日历组件 |
| 待办/工作台 | `JWaitMatter` | 待办事项列表 |
| 查询/筛选 | `JFilterQuery` | 查询条件组件 |

### Step 2: 展示设计摘要并确认

**跳过确认：** 用户说「直接生成」/「不用确认」，或模板精确匹配，或同会话中已确认过。

**需要确认时，展示如下摘要：**

```
## 仪表盘设计摘要

- 页面名称：运营数据看板
- 主题：default

### 组件列表

| 序号 | 组件名称 | 组件类型 | 位置(x,y) | 尺寸(w×h) | 数据源 |
|------|---------|---------|-----------|----------|--------|
| 1 | 总用户数 | JNumber | (0,0) | 6×17 | 静态数据 |
| 2 | 今日活跃 | JNumber | (6,0) | 6×17 | 静态数据 |
| 3 | 用户增长趋势 | JLine | (0,17) | 14×35 | 静态数据 |
| 4 | 用户来源 | JPie | (14,17) | 10×35 | 静态数据 |

确认以上信息正确？(y/n)
```

### 快捷操作：全部预置脚本一览

脚本目录：`<skill_base_dir>\references\scripts\`（`<skill_base_dir>` 为 skill 加载时显示的 `Base directory for this skill` 路径）

| 脚本 | 功能 | 常用命令 |
|------|------|---------|
| `comp_ops.py` | 组件增删改查 | `list`, `delete`, `edit`, `add`, `batch-add`, `move` |
| `page_ops.py` | 页面配置（背景/主题）| `info`, `set-bg`, `set-bgimg`, `set-theme`, `rename`。**rename 参数格式：** `py page_ops.py rename API_BASE TOKEN PAGE_ID --name "新名称"`（`--name` 是命名参数）。**delete：** `bi_utils._request('DELETE','/drag/page/delete',params={'id':PAGE_ID})`。**⚠️ 水印仅大屏有，仪表盘无此命令** |
| `dataset_ops.py` | 数据集管理 | `list`, `create-sql`, `create-api`, `test`, `delete`, `bind` |
| `template_ops.py` | 模板操作 | `list`, `preview`, `search`, `copy` |
| `linkage_ops.py` | 联动/钻取配置 | `show`, `add-linkage`, `remove-linkage`, `add-drill`, `remove-drill` |
| `map_ops.py` | 地图数据管理 | `list`, `check`, `upload`, `add-map` |
| `style_ops.py` | 批量样式修改 | `show-colors`, `set-title-color`, `set-palette`, `batch-edit` |
| `datasource_ops.py` | 数据源管理（含签名） | `list`, `detail`, `create`, `test`, `delete`, `parse-sql`。**create 参数：** `--db`（非 --db-name）、`--user`（非 --username）；**test 支持 `--id` 或 `--name`** |
| `dict_ops.py` | 字典管理 | `list`, `items`, `create`, `add-item`, `delete`, `bind` |
| `files_ops.py` | 多文件数据集 | `create-bind`（上传→建数据集→绑图表一体化）。JOIN 模式必须传 `--group-by <列名> --join-on <关联列> --agg <聚合列>`；列名未知时先问用户 |
| `link_ops.py` | 外部链接/自定义JS | `set`（外部链接）, `set-js`（自定义JS）, `show`（查看）, `remove`（删除链接）, `remove-js`（删除JS） |
| `yapi_ops.py` | YApi Mock 管理 | `create-mock`（**必填 `--title`，不是 `--name`**；`--template single/multi/pie/gauge/table/bar_multi`），`list`，`delete`。**⚠️ 创建前必须先 `list` 查已有接口，复用勿重建** |
| `multi_chart_linkage.py` | 批量图表+联动 | 单脚本完成多图+联动，节省80%耗时 |
| `proc_ops.py` | 存储过程绑定 | `bindcomp`（创建SP+数据集+绑组件一体化）。**前置：`py -m pip install pymysql`** |
| `default_configs.json` | 组件默认配置 | 所有组件默认 w/h/chartData/option，自定义脚本时加载 |

**使用前准备（所有脚本通用）：**
```bash
# <skill_base_dir> = skill 加载时显示的 Base directory for this skill（Windows 路径，Git Bash 下需转为 /c/Users/... 格式）
cp "<skill_base_dir>/references/scripts/脚本名.py" .
cp "<skill_base_dir>/references/bi_utils.py" .
# 执行完后清理: rm 脚本名.py bi_utils.py
```

### 快捷操作：comp_ops.py（增删改查）

> **⚠️ 添加/编辑/删除组件必须使用 comp_ops.py，严禁直接调用 bi_utils.add_xxx() + save_page()。**
> 原因：bi_utils.add_component() 内部将 `_page_components[page_id]` 初始化为空列表，save_page 时会用空列表覆盖页面已有的全部组件，造成不可恢复的数据丢失。

**使用前准备（add 命令需额外复制 default_configs.json）：**
```bash
cp "<skill_base_dir>/references/scripts/comp_ops.py" .
cp "<skill_base_dir>/references/bi_utils.py" .
cp "<skill_base_dir>/references/scripts/default_configs.json" .
# 执行完后清理
rm comp_ops.py bi_utils.py default_configs.json
```

**核心命令（坐标为栅格单位，w 之和≤24）：**
```bash
# 查看组件
py comp_ops.py list $API_BASE $TOKEN $PAGE_ID

# 删除组件
py comp_ops.py delete $API_BASE $TOKEN $PAGE_ID --name "组件名"

# 编辑组件属性（单属性）
py comp_ops.py edit $API_BASE $TOKEN $PAGE_ID --name "组件名" --set "option.title.text=新标题"

# 编辑组件属性（多属性：每个属性一个 --set）
py comp_ops.py edit $API_BASE $TOKEN $PAGE_ID --name "组件名" --set "option.showValue=true" --set "option.unit=个"

# 添加单个组件（静态数据，栅格坐标）⚠️ 严禁并行调用多个 add，会因乐观锁丢失组件
py comp_ops.py add $API_BASE $TOKEN $PAGE_ID --comp "JBar" --title "柱形图" --x 0 --y 0 --w 12 --h 30

# 批量添加多个组件（一次 save，彻底消除并发锁冲突）——添加≥2个组件时必须用此命令
py comp_ops.py batch-add $API_BASE $TOKEN $PAGE_ID --specs '[
  {"comp":"JBar","title":"柱形图","x":0,"y":0,"w":12,"h":30},
  {"comp":"JPie","title":"饼图","x":12,"y":0,"w":12,"h":30},
  {"comp":"JProgress","title":"进度图","x":0,"y":30,"w":12,"h":28},
  {"comp":"JCustomProgress","title":"自定义进度图","x":12,"y":30,"w":12,"h":28}
]'

# 创建SQL数据集+绑定图表：comp_ops.py add/batch-add 不支持直接创建数据集
# 推荐：先 dataset_ops.py create-sql，再 batch-add 传 "config" 绑定；复杂场景用全流程自定义脚本

# 移动/缩放组件
py comp_ops.py move $API_BASE $TOKEN $PAGE_ID --name "组件名" --x 0 --y 17
```

**四种数据模式：**

| 模式 | 参数 | 说明 |
|------|------|------|
| 静态数据（默认） | 无额外参数 | 从 `default_configs.json` 加载默认配置 |
| 绑定已有数据集 | `--config '{"dataType":2,"dataSetId":"...","dataMapping":[...]}'` | 手动传完整 config JSON |
| 创建SQL数据集+绑定 | **不支持**，先 `dataset_ops.py create-sql` 建集，再 batch-add 的 spec `"config"` 中传绑定字段 | `--create-sql` 等参数均不存在 |

### SQL数据集 + 批量图表推荐工作流（dataset_ops + batch-add）

> **适用场景**：普通 SQL（无 FreeMarker 动态参数），字段手动已知。视觉配置由 `default_configs.json` 自动提供，**无需手写 option**。

```bash
# Step 1: 创建 SQL 数据集（获取 DS_ID）
py dataset_ops.py create-sql $API_BASE $TOKEN \
  --name "每年大屏创建数量" --code "yearly_bigscreen_count" \
  --db-source "数据源ID" \
  --sql "SELECT YEAR(create_time) AS name, COUNT(*) AS value FROM onl_drag_page WHERE del_flag=0 GROUP BY YEAR(create_time)" \
  --fields "name:String,value:Integer"

# Step 2: 验证数据集
py dataset_ops.py test $API_BASE $TOKEN --id "DS_ID"

# Step 3: 批量绑定图表（视觉配置自动取 default_configs.json，只需传数据绑定字段）
cp "<skill_base_dir>/references/scripts/comp_ops.py" . && \
cp "<skill_base_dir>/references/bi_utils.py" . && \
cp "<skill_base_dir>/references/scripts/default_configs.json" . && \
PYTHONIOENCODING=utf-8 py comp_ops.py batch-add $API_BASE $TOKEN $PAGE_ID --specs '[
  {"comp":"JBar","title":"基础柱形图","x":0,"y":0,"w":12,"h":35,
   "config":{"dataType":2,"dataSetId":"DS_ID","dataSetName":"每年大屏创建数量",
             "dataSetType":"sql","dataSetApi":"SELECT ...","dataSetMethod":"GET","dataSetIzAgent":"1",
             "dataMapping":[{"filed":"维度","mapping":"name"},{"filed":"数值","mapping":"value"}],
             "fieldOption":[{"fieldName":"name","fieldTxt":"年份","fieldType":"String"},{"fieldName":"value","fieldTxt":"数量","fieldType":"Integer"}],
             "dictOptions":{},"paramOption":[],"chartData":"[]"}},
  {"comp":"JPie","title":"饼图","x":12,"y":0,"w":12,"h":35,
   "config":{"dataType":2,"dataSetId":"DS_ID",...}}
]' && \
rm comp_ops.py bi_utils.py default_configs.json
```

> **config 只需传数据绑定字段**：`dataType/dataSetId/dataSetName/dataSetType/dataSetApi/dataSetMethod/dataSetIzAgent/dataMapping/fieldOption/dictOptions/paramOption/chartData`。`option/background/borderColor/size/w/h` 等视觉字段**全部**由 `default_configs.json` 自动补全，不要手写。

---

### 全流程自定义脚本模板（仅限复杂场景：FreeMarker SQL / 需 queryFieldBySql 自动回写）

> **⚠️ "singleFile" 是文件数据集的 dataType 值，SQL 场景的自定义脚本不要用此名称。**
> **SQL 含特殊字符（`%`、`<`、`>`、`${}`）时必须通过 Write 工具写入 Python 脚本，禁止 bash 命令行传递。**

```python
# 全流程自定义脚本（SQL数据集 + 图表绑定，适用于含 FreeMarker 的复杂 SQL）
import json, time, random, hashlib, urllib.request
import bi_utils, copy

t0 = time.time()
API_BASE = '<api_base>'
TOKEN = '...'
PAGE_ID = '...'
DB_SOURCE_ID = '...'
bi_utils.API_BASE = API_BASE
bi_utils.TOKEN = TOKEN

# ===== Step 1: 缓存已有组件（防止覆盖） =====
page = bi_utils.query_page(PAGE_ID)
tmpl = page.get('template', [])
if isinstance(tmpl, str): tmpl = json.loads(tmpl)
bi_utils._page_components[PAGE_ID] = tmpl

# ===== Step 2: 获取或创建"示例数据集"分组 =====
groups_resp = bi_utils._request('GET', '/drag/onlDragDatasetHead/getAllGroup')
parent_id = '0'
for g in groups_resp.get('result', []):
    if g.get('name') == '示例数据集' and g.get('dataType') is None:
        parent_id = g.get('id', '0'); break
if parent_id == '0':
    bi_utils._request('POST', '/drag/onlDragDatasetHead/addGroup', data={'groupName': '示例数据集'})
    groups2 = bi_utils._request('GET', '/drag/onlDragDatasetHead/getAllGroup')
    for g in groups2.get('result', []):
        if g.get('name') == '示例数据集' and g.get('dataType') is None:
            parent_id = g.get('id', '0'); break

# ===== Step 3: 创建SQL数据集 =====
SQL = "SELECT ... FROM ... GROUP BY ..."
FIELD_LIST = [
    {'fieldName': 'name', 'fieldTxt': '维度', 'fieldType': 'String', 'izShow': 'Y', 'orderNum': 0},
    {'fieldName': 'value', 'fieldTxt': '数值', 'fieldType': 'Integer', 'izShow': 'Y', 'orderNum': 1},
]
ds_resp = bi_utils._request('POST', '/drag/onlDragDatasetHead/add', data={
    'name': '数据集名称', 'code': 'dataset_code',
    'dataType': 'sql', 'dbSource': DB_SOURCE_ID,
    'querySql': SQL, 'apiMethod': 'GET',
    'parentId': parent_id,
    'datasetItemList': FIELD_LIST, 'datasetParamList': []  # ⚠️ datasetItemList，不是 onlDragDatasetItemList
})
result = ds_resp.get('result', {})
DS_ID = result.get('id') if isinstance(result, dict) else result

# ===== Step 4: queryFieldBySql 解析字段并 edit 回写（需签名）=====
SECRET = 'dd05f1c54d63749eda95f9fa6d49v442a'

def get_sign(path):
    """X-Sign：URL参数 + SECRET（不含时间戳）"""
    json_obj = {}
    if '?' in path:
        for kv in path.split('?', 1)[1].split('&'):
            if '=' in kv: k, v = kv.split('=', 1); json_obj[k] = v
    json_obj.pop('_t', None)
    s = json.dumps(dict(sorted(json_obj.items())), ensure_ascii=False, separators=(',', ':')) + SECRET
    return hashlib.md5(s.encode('utf-8')).hexdigest().upper()

def get_vsign(data, sign):
    """V-Sign：Body中的String字段 + sign + SECRET（不含时间戳）"""
    j = dict(data) if data else {}; j['sign'] = sign
    sp = {k: v for k, v in j.items() if v and isinstance(v, str)}
    s = json.dumps(dict(sorted(sp.items())), ensure_ascii=False, separators=(',', ':')) + SECRET
    return hashlib.md5(s.encode('utf-8')).hexdigest().upper()

def signed_post(path, data):
    ts = str(int(time.time() * 1000))
    xsign = get_sign(path); vsign = get_vsign(data, xsign)
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(API_BASE + path, data=body, headers={
        'Content-Type': 'application/json;charset=UTF-8', 'X-Access-Token': TOKEN,
        'X-TIMESTAMP': ts, 'X-Sign': xsign, 'V-Sign': vsign,
    }, method='POST')
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))

fields_resp = signed_post('/drag/onlDragDatasetHead/queryFieldBySql',
    {'sql': SQL, 'dbCode': DB_SOURCE_ID, 'paramArray': []})
# ⚠️ result 是 dict({fieldList:[...], paramList:[...]})，不是直接的列表
raw_fields = (fields_resp.get('result') or {})
if isinstance(raw_fields, dict): raw_fields = raw_fields.get('fieldList', [])
parsed_fields = [
    {'fieldName': f['fieldName'], 'fieldTxt': f.get('fieldTxt', f['fieldName']),
     'fieldType': f.get('fieldType', 'String'), 'izShow': 'Y', 'izWhere': 'N', 'izTotal': 'N', 'orderNum': i}
    for i, f in enumerate(raw_fields)
]
if parsed_fields:
    ds_full = bi_utils._request('GET', '/drag/onlDragDatasetHead/queryById', params={'id': DS_ID})
    ds_obj = ds_full.get('result', {})
    ds_obj['datasetItemList'] = parsed_fields
    bi_utils._request('POST', '/drag/onlDragDatasetHead/edit', data=ds_obj)

# ===== Step 5: getAllChartData 验证 + 取 dictOptions =====
chart_data_resp = bi_utils._request('POST', '/drag/onlDragDatasetHead/getAllChartData', data={'id': DS_ID})
data_list = chart_data_resp.get('result', {}).get('data', [])
dict_options = chart_data_resp.get('result', {}).get('dictOptions', {})
print(f'数据集返回 {len(data_list)} 条，示例: {data_list[:2]}')

field_option = [{'fieldName': f['fieldName'], 'fieldTxt': f['fieldTxt'], 'fieldType': f['fieldType']}
                for f in (parsed_fields or FIELD_LIST)]

# ===== Step 6: 加载 default_configs.json，用业务数据覆盖（禁止手写 option）=====
import os
_cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_configs.json')
if not os.path.exists(_cfg_path): _cfg_path = os.path.join(os.getcwd(), 'default_configs.json')
with open(_cfg_path, encoding='utf-8') as f: defaults = json.load(f)

def build_chart_config(comp_type, ds_id, mapping, field_opt, dict_opts, sql):
    cfg = copy.deepcopy(defaults.get(comp_type, {}))
    cfg.update({
        'dataType': 2, 'dataSetId': ds_id, 'dataSetName': '数据集名称',
        'dataSetType': 'sql', 'dataSetApi': sql, 'dataSetMethod': 'GET', 'dataSetIzAgent': '1',
        'dataMapping': mapping, 'fieldOption': field_opt,
        'dictOptions': dict_opts, 'paramOption': [], 'chartData': '[]',
    })
    return cfg

single_mapping = [{'filed': '维度', 'mapping': 'name'}, {'filed': '数值', 'mapping': 'value'}]
cfg = build_chart_config('JBar', DS_ID, single_mapping, field_option, dict_options, SQL)
comp = {
    'component': 'JBar', 'componentName': '基础柱形图',
    'visible': True, 'i': f'{int(time.time()*1000)}_{random.randint(100000,999999)}',
    'x': 0, 'y': 0, 'w': 12, 'h': 35, 'orderNum': 10, 'config': cfg
}

# ===== Step 7: 追加并保存 =====
bi_utils._page_components[PAGE_ID].append(comp)
bi_utils.save_page(PAGE_ID)
print(f'完成！耗时: {time.time()-t0:.1f}s')
print(f'预览: {API_BASE}/drag/page/view/{PAGE_ID}')
```

**FreeMarker 语法规则（强制）：**

| 规则 | 正确写法 | 错误写法 |
|------|---------|---------|
| 参数判空 | `<#if isNotEmpty(age)>` | ~~`<#if age?? && age?length gt 0>`~~ |
| 参数占位 | `'${age}'` | ~~`#{age}`~~（`#{}` 是系统变量专用） |
| 系统变量 | `#{sys.login_user}` | ~~`${sys.login_user}`~~ |

**`--sql-params` 格式**：`paramName:paramTxt:defaultValue:dictCode`（后三项可省略，多个逗号分隔）

**自定义脚本添加图表的强制规则：**
1. **图表 config 必须从 `default_configs.json` 深拷贝**：`json.loads(json.dumps(defaults['JBar']))`，再覆盖动态数据字段
2. **字典翻译用 jimu_dict**：`/jmreport/dict/*` API，不是 `/sys/dict/*`
3. **dictOptions 从 `getAllChartData` 获取**：创建数据集后调 `getAllChartData`，将返回的 `dictOptions` 写入组件 config

### 快捷操作：linkage_ops.py（组件联动/钻取）

> **组件联动 = 点击源组件，将参数传递给目标组件的数据集查询参数，目标组件自动刷新数据。**

**使用前准备：**
```bash
cp "<skill_base_dir>/references/scripts/linkage_ops.py" .
cp "<skill_base_dir>/references/bi_utils.py" .
```

**核心命令：**
```bash
# 查看页面所有联动配置
py linkage_ops.py show $API_BASE $TOKEN $PAGE_ID

# 添加联动（--mapping 格式：src=tgt，多个逗号分隔）
py linkage_ops.py add-linkage $API_BASE $TOKEN $PAGE_ID --source "源组件名" --target "目标组件名" --mapping "value=age"
py linkage_ops.py add-linkage $API_BASE $TOKEN $PAGE_ID --source "柱形图" --target "饼图" --mapping "name=name,value=keyword"

# 删除联动
py linkage_ops.py remove-linkage $API_BASE $TOKEN $PAGE_ID --source "源组件名" --target "目标组件名"

# 添加钻取（自刷新下钻，--comp 为源组件，无 --target）
py linkage_ops.py add-drill $API_BASE $TOKEN $PAGE_ID --comp "组件名" --mapping "name=year"

# 删除钻取
py linkage_ops.py remove-drill $API_BASE $TOKEN $PAGE_ID --comp "组件名"
```

**联动 vs 钻取核心区别：**

| 特性 | 联动（add-linkage） | 钻取（add-drill） |
|------|---------------------|-------------------|
| 刷新对象 | **其他**组件 | **自身**（递归查询） |
| 参数 | `--source + --target` | `--comp`（只有自己） |
| 支持回退 | 不支持 | 支持（图表左上角回退按钮） |

**⚠️ 易错点（强制记忆）：**

| 错误写法 | 正确写法 | 说明 |
|---------|---------|------|
| `add-drill --source "A" --target "B"` | `add-drill --comp "A"` | 钻取无 `--target`，是自刷新不是跨组件 |
| `--mapping "value:age"` | `--mapping "value=age"` | 映射用 `=` 分隔，不是 `:` |
| `--mapping "a=b c=d"` | `--mapping "a=b,c=d"` | 多个映射用逗号分隔 |

### QQY dataType=4 图表钻取配置（标准流程，1轮完成）

> **触发场景**：用户说"给敲敲云/应用仪表盘中的某图表增加钻取配置"

**核心结论（验证来源：2026-04-17 实操）：**
- QQY dataType=4 图表**同样使用 `drillData` 存钻取映射**，与 dataType=2 机制一致
- `--mapping` 的 target 必须是 **nameFields[].fieldName**（表单字段的 model 值），不是 SQL 参数名
- 点击图表后，前端用 `params.name`（ECharts 点击事件的 name）匹配 drillData，过滤到只显示对应 nameField 值的数据

**标准执行步骤（共2轮）：**

```
步骤1：查询图表配置，取 nameFields[0].fieldName
  py comp_ops.py list API_BASE TOKEN PAGE_ID
  # 再用 py -c 取 config 中的 nameFields，读取 fieldName

步骤2：写入钻取配置
  py linkage_ops.py add-drill API_BASE TOKEN PAGE_ID \
    --comp "图表名" --mapping "name=<nameFields[0].fieldName>"
```

**快速参考（直接取 nameFields[0].fieldName 写入 mapping 的命令）：**

```bash
# 一次性取 nameFields 字段名 + 写入钻取（推荐：合并为同一命令链）
PYTHONIOENCODING=utf-8 py -c "
import sys, json
sys.path.insert(0, '.')
import bi_utils
bi_utils.init_api('API_BASE', 'TOKEN')
page = bi_utils.query_page('PAGE_ID')
tmpl = page.get('template', [])
if isinstance(tmpl, str): tmpl = json.loads(tmpl)
for comp in tmpl:
    if comp.get('componentName') == '目标图表名':
        cfg = comp.get('config', {})
        if isinstance(cfg, str): cfg = json.loads(cfg)
        nf = cfg.get('nameFields', [])
        if nf: print('nameField:', nf[0]['fieldName'])
        break
"
# 输出 nameField: input_xxxx_xxxx 后，直接执行：
py linkage_ops.py add-drill API_BASE TOKEN PAGE_ID --comp "目标图表名" --mapping "name=input_xxxx_xxxx"
```

**⚠️ QQY 钻取的 mapping target 是表单字段名（不是语义名）：**

| 图表数据类型 | mapping target 填什么 | 示例 |
|------------|----------------------|------|
| dataType=2（SQL数据集）| SQL FreeMarker 参数名（如 `year`、`category`）| `name=year` |
| dataType=4（QQY表单）| nameFields[0].fieldName（表单字段 model）| `name=input_1772159072450_604010` |

### 快捷操作：link_ops.py（外部链接/自定义JS）

**核心命令：**
```bash
# 查看页面所有链接配置
py link_ops.py show $API_BASE $TOKEN $PAGE_ID

# 设置外部链接（按名称/类型/ID 定位组件）
py link_ops.py set $API_BASE $TOKEN $PAGE_ID --name "饼图名" --url "https://example.com/detail?category=\${name}"
py link_ops.py set $API_BASE $TOKEN $PAGE_ID --type "JPie" --url "https://www.baidu.com/s?wd=\${name}&value=\${value}"

# 删除外部链接
py link_ops.py remove $API_BASE $TOKEN $PAGE_ID --name "饼图名"

# 设置自定义JS脚本
py link_ops.py set-js $API_BASE $TOKEN $PAGE_ID --name "基础柱形图" --js 'window.open("http://example.com");return false;'

# 从文件读取复杂脚本
py link_ops.py set-js $API_BASE $TOKEN $PAGE_ID --type "JBar" --js-file script.js

# 删除自定义JS脚本
py link_ops.py remove-js $API_BASE $TOKEN $PAGE_ID --name "基础柱形图"
```

**URL 参数占位符（来自 ECharts 点击事件 params）：**

| 占位符 | 含义 |
|--------|------|
| `${name}` | 维度名称（饼图扇区名、柱子x轴标签） |
| `${value}` | 数值（饼图扇区值、柱子高度） |
| `${type}` | 系列名称（多系列图表标识） |

**打开方式（--target）：** `_blank`（新窗口，默认）、`_self`（当前窗口）

### 快捷操作：自定义JS脚本（config.jsConfig）

> 自定义JS脚本存储在 `config.jsConfig`（字符串）。执行顺序：jsConfig → (return true?) → 外部链接 → 联动 → 钻取。return false 阻断后续。

**脚本参数 `params` 常用属性（ECharts 图表）：**

| 属性 | 含义 |
|------|------|
| `params.name` | 维度名称（柱子x轴标签、饼图扇区名） |
| `params.value` | 数值 |
| `params.data` | 原始数据对象 `{name:'北京', value:100}` |
| `params.dataIndex` | 数据索引 |
| `params.seriesName` | 系列名称 |

**常用脚本示例：**
```javascript
// 跳转到外部网站（带点击参数）
window.open("https://example.com/detail?name=" + params.name + "&value=" + params.value);
return false;

// 条件跳转
if (params.value > 100) {
  window.open("https://example.com/high?name=" + params.name);
} else {
  window.open("https://example.com/low?name=" + params.name);
}
return false;
```

**也可用 comp_ops.py edit 快速设置：**
```bash
py comp_ops.py edit $API_BASE $TOKEN $PAGE_ID --name "基础柱形图" --set "jsConfig=window.open(\"http://example.com\");return false;"
```

### 组件 dataMapping 槽位配置（SLOT_CONFIGS）速查

绑定数据集时 `dataMapping.filed` 必须使用以下语义槽位标签（源自 `data.ts` 定义，禁止自行创造不存在的槽位）：

```python
SLOT_CONFIGS = {
    # 单系列图表（2槽位：维度+数值）
    'JBar': ['维度', '数值'], 'JDynamicBar': ['维度', '数值'], 'JCapsuleChart': ['维度', '数值'],
    'JHorizontalBar': ['维度', '数值'], 'JBackgroundBar': ['维度', '数值'],
    'JPie': ['维度', '数值'], 'JRose': ['维度', '数值'], 'JRotatePie': ['维度', '数值'],
    'JLine': ['维度', '数值'], 'JSmoothLine': ['维度', '数值'], 'JStepLine': ['维度', '数值'], 'JArea': ['维度', '数值'],
    'JCustomProgress': ['维度', '数值'], 'JProgress': ['维度', '数值'], 'JListProgress': ['维度', '数值'],
    'JPictorialBar': ['维度', '数值'], 'JPictorial': ['维度', '数值'],
    'JScatter': ['维度', '数值'], 'JFunnel': ['维度', '数值'], 'JPyramidFunnel': ['维度', '数值'],
    'JRadar': ['维度', '数值'], 'JRing': ['维度', '数值'], 'JRingProgress': ['维度', '数值'],
    'JActiveRing': ['维度', '数值'], 'JRadialBar': ['维度', '数值'],
    'JWordCloud': ['维度', '数值'], 'JAreaMap': ['维度', '数值'], 'JBubbleMap': ['维度', '数值'],
    'JBarMap': ['维度', '数值'], 'JHeatMap': ['维度', '数值'],
    # 仪表盘（总计+已用）
    'JGauge': ['总计', '已用'], 'JColorGauge': ['总计', '已用'], 'JAntvGauge': ['总计', '已用'],
    # 多系列图表（3槽位：分组+维度+数值）
    'JStackBar': ['分组', '维度', '数值'], 'JMultipleBar': ['分组', '维度', '数值'],
    'JNegativeBar': ['分组', '维度', '数值'], 'JPercentBar': ['分组', '维度', '数值'],
    'JMixLineBar': ['分组', '维度', '数值'], 'JMultipleLine': ['分组', '维度', '数值'],
    'DoubleLineBar': ['分组', '维度', '数值'],
    # 表格/列表（名称+数值）
    'JTable': ['名称', '数值'], 'JCommonTable': ['名称', '数值'],
    'JScrollTable': ['名称', '数值'], 'JScrollRankingBoard': ['名称', '数值'],
    # 数字指标（数值）
    'JNumber': ['数值'],
    # 水波图（总量+当前）
    'JLiquid': ['总量', '当前'],
}
# UI-only 组件不绑数据集
NO_BIND = {'JImg', 'JText', 'JCurrentTime', 'JIframe', 'JDragEditor',
           'JRadioButton', 'JForm', 'JSelectRadio', 'JTabToggle'}
```

### Step 3: 调用 API 创建仪表盘

**优先使用共通工具库 `bi_utils.py`**（从 Skills 目录复制到后端项目根目录使用）：
- Skills 目录（权威副本）：`<skill_base_dir>\references\bi_utils.py`

> 如果后端项目根目录没有 `bi_utils.py`，先从 skills 目录复制过去再使用。

**执行步骤：**
```
1. 确认后端项目根目录有 bi_utils.py（没有则从 skills 复制）
2. Write 工具 → 写入业务脚本 create_xxx_dashboard.py（项目根目录）
3. Bash 工具 → cd <项目根目录> && python create_xxx_dashboard.py
4. Bash 工具 → rm create_xxx_dashboard.py（清理临时脚本）
```

**仪表盘创建示例：**
```python
from bi_utils import *

init_api('<api_base>', '<token>')

# 创建仪表盘（style='default'，栅格坐标）
page_id = create_page('运营数据看板', style='default', theme='default')

# 第一行：4 个数字卡片（w=6×4=24，h=17）
add_number(page_id, '总用户数', x=0, y=0, w=6, h=17, value=15890, suffix='人')
add_number(page_id, '今日活跃', x=6, y=0, w=6, h=17, value=3256, suffix='人')
add_number(page_id, '今日收入', x=12, y=0, w=6, h=17, value=89600, prefix='¥')
add_number(page_id, '转化率', x=18, y=0, w=6, h=17, value=23.5, suffix='%')

# 第二行：折线图 + 饼图
add_chart(page_id, 'JLine', '用户增长趋势', x=0, y=17, w=14, h=35,
          categories=['周一','周二','周三','周四','周五','周六','周日'],
          series=[{'name':'新增用户', 'data':[120,200,150,80,70,110,130]}])

add_chart(page_id, 'JPie', '用户来源', x=14, y=17, w=10, h=35,
          pie_data=[
              {'name':'微信','value':40},
              {'name':'APP','value':30},
              {'name':'网页','value':20},
              {'name':'其他','value':10},
          ])

save_page(page_id)
print(f'仪表盘创建成功！ID: {page_id}')
```

**仪表盘样式特点（bi_utils.py 自动应用）：**
- 背景：白色 `#FFFFFF`
- 边框：浅灰 `#E8E8E8`
- 标题颜色：深灰 `#464646`
- 轴标签：`#909198`
- 网格线：`#F3F3F3`
- 卡片头：白色背景 + 深灰粗体标题（`headColor: '#FFFFFF'`）
- 图例：深灰色文字

## 仪表盘标题规则（重要）

### 图表组件：card.title 留空，用 option.title 显示

根据真实模板验证，**图表组件**（JBar/JLine/JPie/JRing 等）在仪表盘模式下 `card.title` 应为空字符串，标题通过 ECharts `option.title.text` 显示。如果两者都设置，标题会重复出现（卡片头一次 + 图表内部一次）。

`bi_utils.py` 的 `add_chart()` 已自动处理：调用 `_make_card(mode, '')` 传入空标题。

**JNumber 等非图表组件**可以使用 `card.title` 显示标题。

### 大屏 vs 仪表盘标题对比

| 特征 | 大屏（bigScreen） | 仪表盘（default） |
|------|-------------------|-------------------|
| 图表标题 | `option.title.text`（ECharts 内部） | `option.title.text`（ECharts 内部） |
| card.title（图表） | 必须为空 `''` | 必须为空 `''`（避免重复） |
| card.title（JNumber等） | 为空 `''` | 可填标题 |
| 页面主标题 | JText 组件（fontSize 40+） | 不需要 |

### JText 正确的 config 格式

如果仪表盘中需要使用 JText（少见），config 结构为：
```python
config = {
    'dataType': 1,
    'chartData': {'value': '显示文本'},  # dict 格式，不是字符串
    'option': {
        'body': {
            'color': '#464646',
            'fontSize': 16,
            'fontWeight': 'normal',
            'letterSpacing': 0,
            'text': '',
            'marginTop': 0,
            'marginLeft': 0,
        },
        'textAlign': 'left',
        'card': {'title': '', ...},
    },
}
```

**手动构建组件（用于高级定制，需直接操作 config）：**

当 `add_chart` 等快捷函数无法满足需求时（如需要多系列 chartData、自定义 customColor），可直接构建组件 config：

```python
import json, time, random
import bi_utils

def _key():
    return f'{int(time.time()*1000)}_{random.randint(100000,999999)}'

# 仪表盘亮色主题通用样式
CARD = {
    'size': 'default',
    'headColor': '#FFFFFF',
    'textStyle': {'color': '#464646', 'fontSize': 16, 'fontWeight': 'bold'},
    'extra': '', 'rightHref': ''
}

# 直接构建折线图组件
line_data = [
    {'name': '1月', 'value': 120, 'type': '新增'},
    {'name': '1月', 'value': 80, 'type': '流失'},
    # ...
]
comp = {
    'component': 'JLine',
    'x': 0, 'y': 17, 'w': 14, 'h': 35,
    'i': _key(),
    'config': json.dumps({
        'dataType': 1,
        'chartData': json.dumps(line_data, ensure_ascii=False),
        'background': '#FFFFFF',
        'borderColor': '#E8E8E8',
        'size': {'width': 700, 'height': 375},
        'option': {
            'customColor': [
                {'color': '#1890FF', 'color1': '#1890FF'},
                {'color': '#52C41A', 'color1': '#52C41A'},
            ],
            'title': {'show': True, 'text': '用户变化趋势',
                      'textStyle': {'color': '#464646'}},
            'tooltip': {'show': True},
            'legend': {'show': True, 'textStyle': {'fontSize': 12}},
            'xAxis': {
                'type': 'category',
                'axisLabel': {'color': '#909198'},
                'axisLine': {'lineStyle': {'color': '#F3F3F3'}},
            },
            'yAxis': {
                'axisLabel': {'color': '#909198'},
                'splitLine': {'lineStyle': {'color': '#F3F3F3'}},
            },
            'grid': {'top': 70, 'left': 60, 'right': 30, 'bottom': 40},
            'card': {**CARD, 'title': '用户变化趋势'},
        }
    }, ensure_ascii=False)
}
bi_utils._page_components[page_id].append(comp)
```

### Step 4: 输出结果

**必须将预览地址作为单独一行返回，并用 clip.exe 复制到剪贴板：**

**⚠️ 每次任务完成后必须输出总耗时（强制）：**
- **脚本中**：开头记录 `import time; t0 = time.time()`，末尾输出 `print(f'耗时: {time.time()-t0:.1f}s')`
- **多轮调用/纯API操作**：在最终回复文字末尾补充一行 `耗时：约 Xs`
- **禁止输出每个步骤的耗时**，只输出整个任务从开始到结束的总耗时

```
## 仪表盘创建成功

- 页面ID：{id}
- 页面名称：{name}
- 模式：仪表盘（default）
- 组件数量：{count} 个

预览地址（标准仪表盘）：
{API_BASE}/drag/page/view/{id}

分享地址（QQY 低代码应用仪表盘）：
http://{前端域名}:{端口}/drag/share/{appId}/{pageId}
```

```bash
echo -n "{完整URL}" | clip.exe
```

**⚠️ 写了 Java 接口时，脚本末尾必须额外输出（强制）：**
```python
print("\n" + "="*60)
print("仪表盘组件已生成完成！")
print("="*60)
print("\n【API 接口地址】（需重启后端后生效）：")
print(f"  {API_BASE}/drag/mock/xxxFlow")
print("\n【重要提示】请重启 Spring Boot 后端服务！")
print(f"\n【仪表盘预览地址】")
print(f"  {API_BASE}/drag/page/view/{PAGE_ID}")
print("="*60)
```

---

## 数据集管理（动态数据源）

`config.dataType`：`1`=静态数据（chartData直写）；`2`=动态数据（SQL/API/文件数据集）；`4`=表单数据（Online/设计器表单，无需数据集）

**推荐工作流（无需读此节）**：
- SQL 数据集：`dataset_ops.py create-sql` → `comp_ops.py batch-add --specs`（spec 的 config 传 dataType/dataSetId/dataMapping）
- API 数据集：`dataset_ops.py create-api` → `comp_ops.py add --dataset-name`（2轮完成）
- 文件数据集：`files_ops.py create-bind`（一体化）

### 数据集 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/drag/onlDragDatasetHead/add` | POST | 创建数据集 |
| `/drag/onlDragDatasetHead/edit` | POST | 编辑数据集 |
| `/drag/onlDragDatasetHead/delete?id=xxx` | DELETE | 删除 |
| `/drag/onlDragDatasetHead/list` | GET | 查询列表 |
| `/drag/onlDragDatasetHead/getAllChartData` | POST | 执行查询/取数据 |
| `/drag/onlDragDatasetHead/queryFieldBySql` | POST | 解析SQL字段（**需签名**） |
| `/drag/onlDragDatasetHead/queryFieldByApi` | POST | 解析API字段 |

### 组件绑定数据集（dataType=2）

```python
config = {
    'dataType': 2,
    'dataSetId': 'dataset_id',
    'dataSetName': '数据集名称',
    'dataSetType': 'sql',          # sql / api
    'dataSetApi': 'SELECT ...',    # SQL语句或API地址
    'dataSetMethod': 'GET',
    'dataSetIzAgent': '',          # SQL='', API直连='0', API代理='1'
    'dataMapping': [
        {'filed': '维度', 'mapping': 'name'},   # filed=语义槽位，mapping=字段名
        {'filed': '数值', 'mapping': 'value'},
    ],
    'fieldOption': [...],          # 字段列表（getAllChartData后可获取）
    'dictOptions': {},             # 字典翻译（getAllChartData返回）
    'paramOption': [],             # 参数列表（FreeMarker条件参数）
    'chartData': '[]',
}
```

**dataMapping 语义槽位**：单系列 `[维度, 数值]`；多系列 `[分组, 维度, 数值]`
**filed 拼写**：`filed`（少一个 d，不是 field）

> 完整 SQL/API 端到端流程、FreeMarker 语法、全流程自定义脚本 → 见 `references/datasource-dataset-chart-guide.md` 和 `references/dataset-guide.md`

---

## API 接口签名机制

`queryFieldBySql` 等接口带 `@SignatureValidation`，需要签名头。**`bi_utils` 的 `signed_request()` 函数已封装签名逻辑，直接调用即可。**

> 签名算法、Python 实现、需签名接口清单 → 见 `references/signing-datasource-guide.md`

---

## 数据源管理

使用 `datasource_ops.py` 管理数据源：`list`, `detail`, `create`, `test`, `delete`

```bash
py datasource_ops.py list "API_BASE" "TOKEN"
py datasource_ops.py create "API_BASE" "TOKEN" --name "名称" --db "MYSQL5.7" \
  --url "jdbc:mysql://..." --user "root" --password "root"
```

> 已适配 18 种数据库类型（MySQL5.7/8.0, PostgreSQL, Oracle, SQLServer, DM等）。NoSQL/签名数据源 → 见 `references/signing-datasource-guide.md`

---

## SQL 数据集动态查询条件（FreeMarker）

SQL 支持 FreeMarker 动态条件：`<#if isNotEmpty(sex)> AND sex = '${sex}' </#if>`

**参数配置**在 `datasetParamList`；组件 `config.paramOption` 中传参值。

> FreeMarker 语法规则、参数配置详情 → 见 `references/dataset-guide.md`

---

## SQL/API 数据集绑定图表完整端到端流程

**推荐方式（普通SQL，无FreeMarker）**：
```bash
# 1. 创建SQL数据集
PYTHONIOENCODING=utf-8 py dataset_ops.py create-sql $API_BASE $TOKEN \
  --name "数据集名" --db-source "数据源ID" \
  --sql "SELECT name, value FROM t GROUP BY name" \
  --fields "name:String,value:Integer"

# 2. 批量添加图表并绑定
PYTHONIOENCODING=utf-8 py comp_ops.py batch-add $API_BASE $TOKEN $PAGE_ID --specs '[
  {"comp":"JBar","title":"柱形图","x":0,"y":0,"w":12,"h":35,
   "config":{"dataType":2,"dataSetId":"<DS_ID>",
             "dataMapping":[{"filed":"维度","mapping":"name"},{"filed":"数值","mapping":"value"}]}}
]'
```

**全流程自定义脚本（含FreeMarker SQL / 需queryFieldBySql回写）**：见 `references/datasource-dataset-chart-guide.md`

**API 数据集**：`dataset_ops.py create-api` + `comp_ops.py add --dataset-name`（2轮完成）

### 文件数据集（单文件 singleFile / 多文件 FILES）

文件数据集通过上传 Excel/CSV/JSON 文件作为数据源，无需外部数据库连接。

#### 文件数据集 vs SQL/API 数据集的关键差异

| 项目 | 单文件 (singleFile) | 多文件 (FILES) | SQL 数据集 | API 数据集 |
|------|-------------------|---------------|-----------|-----------|
| `dataType`（数据集） | `'singleFile'` | `'FILES'` | `'sql'` | `'api'` |
| `dbSource` | **reportId**（页面 ID） | **reportId**（页面 ID） | 数据库源 ID | `None` |
| `querySql` | `select * from {tableName}` | 可跨表 SQL 查询 | SQL 语句 | API URL |
| 文件上传 | 1 个文件（`isSingle=true`） | 多个文件 | 不需要 | 不需要 |
| `content` | `JSON.stringify(fileList)` | 不需要 | 不需要 | 不需要 |
| 字段解析 API | 自动从文件解析 | `queryFileFieldBySql`（非 `queryFieldBySql`） | `queryFieldBySql` | `queryFieldByApi` |
| 支持格式 | `.csv .xls .xlsx .json` | `.csv .xls .xlsx .json` | — | — |

#### 文件上传 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/jmreport/source/datasource/files/add` | POST (multipart) | 上传文件 |
| `/jmreport/source/datasource/files/get` | GET | 获取文件列表 `?reportId=xxx` |
| `/jmreport/source/datasource/files/preview` | GET | 预览文件数据 |
| `/jmreport/source/datasource/files/del` | DELETE | 删除数据源 |
| `/jmreport/source/datasource/files/del/file` | DELETE | 删除单个文件 |

**上传参数（multipart/form-data）：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `file` | File | 上传的文件 |
| `reportId` | String | 页面 ID（大屏/仪表盘 ID） |
| `isSingle` | Boolean | 单文件数据集设为 `true`，多文件不传 |
| `X-Access-Token` | Header | JWT 令牌 |

**上传返回结构：**
```json
{
  "success": true,
  "message": "filesDataSet/PAGE_ID/default.xls",
  "result": {
    "id": "xxx",
    "dbUrl": "[{\"fileName\":\"default.xls\",\"name\":\"jmf.Sheet1_default_excel\"}]"
  }
}
```

> **表名命名规则**：`jmf.{SheetName}_{fileName}_{ext}`（XLS 取 Sheet 名）或 `jmf.{fileName}_{ext}`（CSV/JSON）。

#### Python 文件上传函数

```python
def upload_file(file_path, report_id, is_single=False):
    url = f'{API_BASE}/jmreport/source/datasource/files/add'
    boundary = f'----WebKitFormBoundary{int(time.time()*1000)}'
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    body_parts = []
    body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="reportId"\r\n\r\n{report_id}\r\n'.encode())
    if is_single:
        body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="isSingle"\r\n\r\ntrue\r\n'.encode())
    body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{file_name}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode())
    body_parts.append(file_data)
    body_parts.append(f'\r\n--{boundary}--\r\n'.encode())
    body = b''.join(body_parts)
    headers = {'Content-Type': f'multipart/form-data; boundary={boundary}', 'X-Access-Token': TOKEN}
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode('utf-8'))
```

#### 创建单文件数据集（singleFile）

```python
# 1. 上传文件（isSingle=True）
result = upload_file(FILE_PATH, PAGE_ID, is_single=True)
file_list = json.loads(result['result']['dbUrl'])
table_name = file_list[0]['name']  # 如 jmf.Sheet1_default_excel

# 2. 创建数据集
ds = bi_utils._request('POST', '/drag/onlDragDatasetHead/add', data={
    'name': '销售数据(单文件)', 'code': 'sales_single',
    'dataType': 'singleFile',        # 关键
    'dbSource': PAGE_ID,             # 关键：页面ID
    'querySql': f'select * from {table_name}',
    'content': json.dumps(file_list, ensure_ascii=False),  # 文件列表
    'datasetItemList': [...], 'datasetParamList': []
})

# 3. 组件 config 绑定
config = {'dataType': 2, 'dataSetType': 'singleFile', 'dataSetApi': f'select ...', ...}
```

#### 创建多文件数据集（FILES）

```python
# 1. 上传多个文件
upload_file(r'<file_path>', PAGE_ID)
upload_file(r'<file_path>', PAGE_ID)

# 2. 获取文件列表
files = bi_utils._request('GET', '/jmreport/source/datasource/files/get', params={'reportId': PAGE_ID})
file_list = json.loads(files['result']['dbUrl'])

# 3. 创建数据集（可跨文件表 SQL）
ds = bi_utils._request('POST', '/drag/onlDragDatasetHead/add', data={
    'name': '多文件数据集', 'code': 'multi_files',
    'dataType': 'FILES',             # 关键：大写 FILES
    'dbSource': PAGE_ID,             # 关键：页面ID
    'querySql': f'select name, value from {table_name} order by value desc',
    'datasetItemList': [...], 'datasetParamList': []
})

# 4. 组件 config 绑定
config = {'dataType': 2, 'dataSetType': 'FILES', 'dataSetApi': 'select ...', ...}
```

---

### 数据集踩坑记录

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| **"数据源不存在"** | SQL 数据集未设置 `dbSource` | 必须指定 `dbSource`（如 `707437208002265088`） |
| **字段列表不生效** | 用了 `onlDragDatasetItemList` | 正确字段名是 `datasetItemList` |
| **编辑数据集 510 权限错误** | 缺少 `sign` 字段 | 编辑时需传 `sign: 'E19D6243CB1945AB4F7202A1B00F77D5'` |
| **dataMapping 的 filed 拼写** | 系统中 `filed` 不是 `field` | 必须用 `filed`（少一个 d），这是系统设计 |
| **API 类型跨域** | 前端直连外部 API 遇到 CORS | 设置 `izAgent: '1'` 走后端代理 |
| **SQL 参数替换** | 需要动态参数 | SQL 中用 `#{paramName}`（系统变量）或 `${paramName}`（FreeMarker） |
| **SQL 最大返回 1000 条** | 后端限制 | `getChartData` 方法限制最大 1000 条记录 |
| **queryFieldBySql 签名验证失败** | 该接口带 `@SignatureValidation` | 必须用 `signed_request()` 携带 X-Sign/V-Sign/X-TIMESTAMP |
| **SQL 注入检测拦截** | 查询 information_schema 被拦截 | 后端 `SqlInjectionUtil` 会拦截敏感关键词，直接用已知表名 |
| **API 地址存在 querySql 字段** | API 数据集没有独立的 url 字段 | `querySql` 对 SQL 类型存 SQL，对 API 类型存 API URL |
| **API 数据集不需要 dbSource** | API 类型直接访问外部接口 | `dbSource` 设为 `None`，否则可能报错 |
| **漏斗图数据过多显示拥挤** | 漏斗图层级太多影响视觉效果 | 使用 `dataFilterNum` 限制前 N 条（建议 3-7 条） |
| **API 数据集 izAgent 选择** | mock API 无跨域问题，外部 API 可能有 | 同域/mock 用 `'0'`（直连），跨域用 `'1'`（后端代理） |
| **文件数据集 dbSource 不是数据库ID** | singleFile/FILES 的 `dbSource` 是页面 ID | `dbSource = reportId`（页面 ID），不是数据库连接 ID |
| **单文件数据集需要 content 字段** | 单文件的 `content` 存文件列表 JSON | `content = JSON.stringify([{fileName, name}])`，多文件不需要 |
| **多文件字段解析用 queryFileFieldBySql** | 多文件的字段解析 API 不同于 SQL 数据集 | 用 `queryFileFieldBySql`（非 `queryFieldBySql`），参数 `dbCode = reportId` |
| **XLS 文件表名含 Sheet 名** | 系统从 Excel 的 Sheet 名生成表名 | 表名格式 `jmf.{SheetName}_{fileName}_{ext}`，如 `jmf.Sheet1_default_excel` |
| **CSV 编码问题** | UTF-8 BOM 头导致字段名乱码 | 上传前确保文件为纯 UTF-8（无 BOM），或系统会自动处理 |
| **文件上传 isSingle 参数** | 单文件和多文件的区别标志 | 单文件上传传 `isSingle=true`，多文件不传此参数 |

---

## Online表单 / 设计器表单 生成图表（dataType=4）

`config.dataType=4` 直接绑定 Online表单（cgform）或设计器表单（desform），无需创建数据集。

| 类型 | formType | 查询API |
|------|---------|---------|
| Online表单（cgform） | `'online'` | `GET /online/cgform/head/list` |
| 设计器表单（desform）| `'design'` | `GET /desform/api/list/options` |

字段角色：`nameFields`=维度（String类型）；`valueFields`=指标（数值类型或 record_count）；`typeFields`=分组

> 完整字段查询、config 构建模板、字段类型映射 → 见 `references/online-design-form-chart-guide.md`

---

## 编辑已有仪表盘

```python
from bi_utils import *
init_api('<api_base>', '<token>')

page = query_page(page_id)
print(page['name'], page['updateCount'])

add_chart(page_id, 'JBar', '新增图表', x=0, y=52, w=12, h=35,
          categories=['A','B','C'], series=[{'name':'值','data':[10,20,30]}])
save_page(page_id)
```

---

## 删除仪表盘

```python
from bi_utils import *
init_api('<api_base>', '<token>')

delete_page(page_id)                # 软删除
delete_page(page_id, physical=True) # 硬删除
```

---

## 修改组件样式

阅读 `references/bi-comp-option-config.md` 获取每种组件的完整配置项路径。

**仪表盘样式修改关键规则：**
- 颜色使用色值（`#000000`），不用英文单词
- customColor 格式：`[{color1:'#xxx',color:'#xxx'}]`
- 卡片头样式：`option.card.textStyle.color`、`option.card.headColor`
- 背景色：`config.background`（仪表盘默认 `#FFFFFF`，**禁止设置透明色 `#FFFFFF00` 或 `transparent`**）
- 边框色：`config.borderColor`（仪表盘默认 `#E8E8E8`）

```python
import json
from bi_utils import *
import bi_utils

init_api('<api_base>', '<token>')

page_id = 'xxx'
page = query_page(page_id)
tmpl = page.get('template', [])
if isinstance(tmpl, str):
    tmpl = json.loads(tmpl)

for comp in tmpl:
    config_str = comp.get('config', '{}')
    config = json.loads(config_str) if isinstance(config_str, str) else config_str
    if comp.get('component') == 'JBar':
        option = config.get('option', {})
        option['series'][0]['itemStyle'] = {'color': '#1890FF'}
        config['option'] = option
        comp['config'] = json.dumps(config, ensure_ascii=False)

bi_utils._page_components[page_id] = tmpl
save_page(page_id)
```

---

## bi_utils 使用规则（强制）

### 初始化方式

```python
# 正确：直接赋值模块级全局变量
import bi_utils
bi_utils.API_BASE = '<api_base>'
bi_utils.TOKEN = '...'

# 也可以用 init_api（封装了赋值）
from bi_utils import *
init_api('<api_base>', '<token>')

# 错误：没有 init() 方法
# bi_utils.init(API_BASE, TOKEN)  # ← AttributeError
```

### 页面数据与组件字段映射（query_page 返回值）

| 正确字段 | 常见误猜 | 说明 |
|---------|---------|------|
| `page['template']` | ~~`page['pageTemplate']`~~ | 组件列表，**已经是 list**，无需 `json.loads` |
| `comp['i']` | ~~`comp['id']`~~ | 组件唯一标识（UUID） |
| `comp['componentName']` | ~~`comp['label']`~~, ~~`comp['name']`~~ | 组件显示名称（中文） |
| `comp['component']` | - | 组件类型（JBar, JText 等） |
| `comp['pageCompId']` | - | 后端数据库 ID |
| `comp['isLock']` | - | 锁定状态（true/false） |

### 自定义脚本操作模板的正确模式

```python
import bi_utils
bi_utils.API_BASE = '...'
bi_utils.TOKEN = '...'
PAGE_ID = '...'

page = bi_utils.query_page(PAGE_ID)
tmpl = page.get('template', [])  # 已经是 list，不需要 json.loads

# 按组件名查找（字段是 componentName，不是 label/name）
target_idx = next(i for i, c in enumerate(tmpl) if c.get('componentName') == '目标名称')

# 修改后保存
bi_utils._page_components[PAGE_ID] = tmpl
bi_utils.save_page(PAGE_ID)
```

### Windows Python 命令

- 用 `py` 不是 `python`（Git Bash 下 `python` 找不到）
- **必须加 `PYTHONIOENCODING=utf-8` 前缀**（Windows 默认 GBK 编码，脚本中含中文输出时报 `UnicodeEncodeError`）
- 所有 `py script.py` 调用必须写成 `PYTHONIOENCODING=utf-8 py script.py`
- 脚本内部 `print` 禁止使用 emoji 字符

---

## 常用组件配置路径速查（内联）

> 以下组件的 option 路径已内联，修改时**直接使用，无需读取 `bi-comp-option-config.md`**。

### JStatsSummary（统计概览）

| 说明 | 配置路径 | 示例值 |
|------|---------|--------|
| 卡片最小宽度 | `option.card.minWidth` | 250 |
| 卡片圆角 | `option.card.borderRadius` | 16 |
| 卡片边框颜色 | `option.card.borderColor` | #1890FF59 |
| 卡片阴影 | `option.card.shadow` | 0 4px 12px #00000020 |
| 卡片填充颜色 | `option.card.fill.color` | #F7F7F7 |
| 数值字号 | `option.sections.top.value.fontSize` | 28 |
| 数值颜色 | `option.sections.top.value.fontColor` | #464646 |
| 单位字号 | `option.sections.top.value.unit.fontSize` | 14 |
| 标签字号 | `option.sections.bottom.label.fontSize` | 14 |
| 标签颜色 | `option.sections.bottom.label.fontColor` | #909198 |

### JCapsuleChart（胶囊图）

| 说明 | 配置路径 | 示例值 |
|------|---------|--------|
| 显示数值 | `option.showValue` | true/false |
| X轴名称/单位 | `option.unit` | 个 |

### JGauge（仪表盘表盘）

| 说明 | 配置路径 |
|------|---------|
| 刻度值显隐 | `option.series[0].axisLabel.show` |
| 刻度值颜色 | `option.series[0].axisLabel.color` |
| 刻度线显隐 | `option.series[0].axisTick.show` |
| 分割线显隐 | `option.series[0].splitLine.show` |
| 指标字号 | `option.series[0].detail.fontSize` |

### JProgress（进度条）

| 说明 | 配置路径 |
|------|---------|
| 显示标题 | `option.yAxis.axisLabel.show` |
| 标题字体颜色 | `option.yAxis.axisLabel.color` |

### JScrollBoard（轮播表）

| 说明 | 配置路径 |
|------|---------|
| 悬浮暂停 | `option.hoverPause` |
| 等待时间 | `option.waitTime` |

### JNumber（数字指标卡）

| 说明 | 配置路径 |
|------|---------|
| 数值字号 | `option.valueStyle.fontSize` |
| 数值颜色 | `option.valueStyle.color` |
| 前缀 | `option.prefix` |
| 后缀/单位 | `option.suffix` |
| 卡片头颜色 | `option.card.textStyle.color` |

---

## 布局组件使用指南（JTabs / JGrid）

> 证据来源：`Tabs.vue`、`Grid.vue`、`data.ts`（第3640-3687行）

### JTabs（选项卡）

**用途**：在同一空间内放多个 Tab，每个 Tab 内嵌一个图表/组件，切换显示。

**默认尺寸**：`w=12, h=40`

**数据结构（API创建时完整格式）：**

```python
jtabs_i = bi_utils._gen_uuid()

jtabs_comp = {
    'component': 'JTabs',
    'componentName': '选项卡',   # 必须中文
    'i': jtabs_i,
    'x': 0, 'y': 0, 'w': 24, 'h': 40,
    'orderNum': 10,
    'visible': True,
    'config': {
        'w': 1800, 'h': 440,
        'size': {'width': 1800, 'height': 440},
        'option': {
            'title': '选项卡',
            # 右上角文字按钮（可选）
            'rightText': '更多',          # 显示文字
            'rightHref': '/page/detail',  # 点击跳转链接
            'rightTextColor': '#4A90E2',  # 按钮颜色（默认#4A90E2）
        },
        'child': [
            {
                'title': 'Tab1',            # Tab 标签文字
                'i': bi_utils._gen_uuid(),  # 每个 tab 必须有独立 uuid
                'parentId': jtabs_i,        # 必须是 JTabs 的 i
                'component': 'JBar',        # 嵌套的组件类型
                'config': { ... }           # 嵌套组件的完整 config
            },
            {
                'title': 'Tab2',
                'i': bi_utils._gen_uuid(),
                'parentId': jtabs_i,
                'component': '',            # 空字符串 = 未放组件
                'config': {}
            }
        ]
    }
}
```

**关键规则（来源：Tabs.vue 第90-98行）：**
- `config.child` 读取的是 `props.config.child`（不是 `props.child`），必须放在 `config` 下
- 每个 Tab 只能嵌套 **一个** 组件
- **禁止**在 JTabs 内再嵌套 JTabs 或 customForm（`excludeComp = ['JTabs','customForm']`）
- Tab 内组件 resize 时会触发重新渲染（watch size → reloadKey++，解决组件尺寸失配问题）
- `rightText`/`rightHref` 不填时不显示右上角按钮

---

### JGrid（栅格布局）

**用途**：横向并排展示多个组件，可设置各列宽度比例，支持移动端自适应。

**默认尺寸**：`w=12, h=40`

**数据结构（API创建时完整格式）：**

```python
jgrid_i = bi_utils._gen_uuid()

jgrid_comp = {
    'component': 'JGrid',
    'componentName': '栅格布局',   # 必须中文
    'i': jgrid_i,
    'x': 0, 'y': 0, 'w': 24, 'h': 40,
    'orderNum': 10,
    'visible': True,
    'config': {
        'w': 1800, 'h': 440,
        'size': {'width': 1800, 'height': 440},
        'option': {
            'card': {
                'title': '',         # 整体卡片标题（留空则不显示）
                'extra': '',         # 卡片右侧附加文字
                'rightHref': '',     # 附加文字跳转链接
                'size': 'default',   # 卡片尺寸
            }
        },
        'child': [
            {
                'i': bi_utils._gen_uuid(),
                'parentId': jgrid_i,   # 必须是 JGrid 的 i
                'span': 12,            # 列宽（24列制，多列 span 之和 = 24）
                'component': 'JPie',   # 该列放置的组件类型
                'config': { ... }      # 该列组件的完整 config
            },
            {
                'i': bi_utils._gen_uuid(),
                'parentId': jgrid_i,
                'span': 12,
                'component': 'JBar',
                'config': { ... }
            }
        ]
    }
}
```

**关键规则（来源：Grid.vue 第146-151行）：**
- 子组件实际渲染宽度 = `(parent.size.width / 24) * item.span`（自动计算，不需手动传 size）
- `span` 之和推荐 = 24（等于总宽），否则最后一列会截断或留白
- **禁止**在 JGrid 内嵌套 layout 类或 customForm（`excludeComp = ['layout','customForm']`）
- **可以** JGrid 嵌套在 JTabs 内（支持 `pid` 参数传递父 Tab ID）
- 移动端响应式（来源：Grid.vue 第156-162行）：屏幕宽度 < 500px 时所有列 `span` 自动改为 24（全宽堆叠）
- `child` 默认为空数组，需在 API 创建时直接填充 `child` 才能预设内容

**常见 span 分配方案：**

| 列数 | span 分配 | 说明 |
|------|-----------|------|
| 2列 | 12 + 12 | 各半 |
| 3列 | 8 + 8 + 8 | 三等分 |
| 4列 | 6 + 6 + 6 + 6 | 四等分 |
| 左宽右窄 | 16 + 8 | 左图右说明 |
| 左窄右宽 | 8 + 16 | 左说明右图 |

---

### JTabs 嵌套 JGrid 示例

JTabs 的每个 Tab 内可放 JGrid（一个 Tab 内并排多列）：

```python
grid_i = bi_utils._gen_uuid()
tabs_i = bi_utils._gen_uuid()

jgrid_config = {
    'w': 1800, 'h': 440,
    'size': {'width': 1800, 'height': 440},
    'option': {'card': {'title': '', 'extra': '', 'rightHref': '', 'size': 'default'}},
    'child': [
        {'i': bi_utils._gen_uuid(), 'parentId': grid_i, 'span': 12, 'component': 'JBar', 'config': {...}},
        {'i': bi_utils._gen_uuid(), 'parentId': grid_i, 'span': 12, 'component': 'JPie', 'config': {...}},
    ]
}

jtabs_comp = {
    'component': 'JTabs',
    'componentName': '销售分析',
    'i': tabs_i, 'x': 0, 'y': 40, 'w': 24, 'h': 40,
    'orderNum': 20, 'visible': True,
    'config': {
        'w': 1800, 'h': 440,
        'size': {'width': 1800, 'height': 440},
        'option': {'title': '销售分析'},
        'child': [
            {'title': '柱图+饼图', 'i': grid_i, 'parentId': tabs_i,
             'component': 'JGrid', 'config': jgrid_config},
            {'title': 'Tab2', 'i': bi_utils._gen_uuid(), 'parentId': tabs_i,
             'component': '', 'config': {}},
        ]
    }
}
```

---

## 可用的快捷函数

**API 初始化：**
- `init_api(api_base, token)` — 初始化 API 地址和 Token

**页面管理：**
- `create_page(name, style='default', theme='default')` — 创建仪表盘
- `query_page(page_id)` — 查询页面详情
- `list_pages(style='default')` — 列表查询
- `save_page(page_id)` — 保存设计
- `delete_page(page_id, physical)` — 删除
- `copy_page(page_id)` — 复制

**添加组件（栅格坐标）：**
- `add_number(page_id, title, x, y, w, h, value, prefix, suffix)` — 数字指标
- `add_chart(page_id, chart_type, title, x, y, w, h, categories, series, pie_data)` — 图表
- `add_table(page_id, title, x, y, w, h, columns, data)` — 数据表格
- `add_scroll_table(page_id, title, x, y, w, h, columns, data)` — 滚动表格
- `add_ranking(page_id, title, x, y, w, h, data)` — 排行榜
- `add_text(page_id, title, x, y, w, h, content, font_size, color)` — 文本
- `add_image(page_id, title, x, y, w, h, src)` — 图片
- `add_gauge(page_id, title, x, y, w, h, value, max_val, unit, color)` — 仪表盘表盘
- `add_liquid(page_id, title, x, y, w, h, value, color)` — 水球图
- `add_component(page_id, component, title, x, y, w, h, config)` — 通用组件

---

## 核心踩坑速查

| 问题 | 核心规则 |
|------|---------|
| **🚨 严禁 bi_utils.add_xxx + save_page** | add_component 初始化空列表，save_page 覆盖已有组件。必须用 comp_ops.py add |
| **🚨 添加≥2个组件时严禁并行 add** | 并行两个 `add` 进程读到相同 updateCount，第二个保存必被后端拒绝，组件永久丢失。必须用 `batch-add --specs '[...]'` 一次保存 |
| **🚨 add 命令后 chartData 为 []** | comp_ops.py 已改为从 default_configs.json 加载完整默认数据；出现空数据说明 default_configs.json 未 cp 到工作目录，cp 时必须一并复制 default_configs.json |
| **🚨 静态 chartData 禁止使用兜底数据** | default_configs.json 为空时 comp_ops.py 回落到内置占位数据（JBar→A/B/C/D/E）。必须从 data.ts 读取真实 chartData，通过 spec `"config":{"chartData":[...]}` 或 singleFile 脚本 `_build_comp_config(comp_type, title, {"chartData": json.dumps(real_data)})` 覆盖 |
| **🚨 add_component 前必须缓存 template** | 任何场景调用 add_component 前，必须先：`page=bi_utils.query_page(PAGE_ID)` → `tmpl=page.get('template') or []`（**必须用 `or []`，不能用 `.get('template',[])`——空页面时 key 存在但值为 None，`.get` 默认值失效**）→ `bi_utils._page_components[PAGE_ID]=tmpl` → 再调 add_component。漏写则所有已有组件被永久清空 |
| **🚨 删除前必须询问用户确认** | 除非用户明确说"删除/去掉/移除"，禁止自行执行任何 delete 操作。删除不可逆 |
| **POST /drag/page/edit 乐观锁** | 必须传 `updateCount` |
| **chartData 必须是 JSON 字符串** | `json.dumps(...)` 后传入，不能是原生 list/dict |
| **dataMapping 的 filed 拼写** | `filed`（不是 `field`，少一个 d） |
| **图表标题去重** | 图表组件 `card.title=''`，只用 `option.title.text` |
| **size 字段必须是像素** | `config.size.width/height` 是像素值。栅格转像素：`w*75`, `h*11` |
| **组件 ID/名称字段** | ID 是 `i`（不是 `id`），名称是 `componentName`（不是 `label`/`name`） |
| **template 字段** | `query_page` 返回组件列表在 `template`（已是 list），不是 `pageTemplate`。**空页面时 `template` 为 `None`（非缺失键），必须用 `page.get('template') or []`，禁止 `.get('template',[])`** |
| **bi_utils 初始化** | 直接赋值 `bi_utils.API_BASE/TOKEN`，无 init() 方法（有 init_api 封装） |
| **Windows 命令** | 用 `py` 不是 `python`；所有脚本必须加 `PYTHONIOENCODING=utf-8`；脚本 print 禁用 emoji |
| **cp 目标路径格式** | Git Bash 必须用 Unix 格式 `/c/Users/<用户名>/`，不能用 `C:/Users/` |
| **cp 后必须 ls 验证** | cp 可能静默失败，必须 `&& ls *.py *.json` 验证，否则 ModuleNotFoundError |
| **cp 与 py 必须同轮** | cp 依赖文件和 py 执行必须在同一命令链，不能拆成两轮 |
| **写脚本用 Write 工具** | 禁止 bash heredoc（含单引号必报错） |
| **FreeMarker SQL 禁止 bash 传递** | `${age}` 被 shell 消费，`</#if>` 中的 `>` 被解释为重定向，必须用 `--sql-file` |
| **带 FreeMarker 的参数判空** | `<#if isNotEmpty(age)>`，禁止 `age?? && age?length gt 0` |
| **🚨 comp_ops.py add 不支持 --create-sql** | `--create-sql`/`--sql-file`/`--ds-name`/`--db-source` 均不存在，报 `unrecognized arguments`。应先 `dataset_ops.py create-sql`，再 `batch-add --specs` 传 `"config"` 绑定 |
| **🚨 SQL+批量图表禁止手写 option** | 图表 option/background/size 等视觉配置必须来自 `default_configs.json`（深拷贝），禁止在 config 里手写 option。只需传 dataType/dataSetId/dataMapping/fieldOption 等数据绑定字段 |
| **🚨 queryFieldBySql result 是 dict 不是 list** | `fields_resp.get('result', [])` 会得到 None 或 dict，报 `TypeError: 'NoneType' object is not iterable`。正确写法：`(fields_resp.get('result') or {}).get('fieldList', [])` |
| **🚨 签名算法不含时间戳** | X-Sign/V-Sign 的 MD5 字符串 = `json_str + SECRET`（无 `+ ts`）。加了时间戳必报"签名不匹配"。时间戳只放在请求头 `X-TIMESTAMP`，不参与 MD5 计算 |
| **🚨 getAllGroup 字段是 name 不是 groupName** | `item.get('groupName')` 永远 None → 无限触发 addGroup。必须用 `item.get('name')`；addGroup 返回 null，必须重查取 `id` 作 `parentId` |
| **🚨 SQL数据集创建后必须: queryFieldBySql+edit+getAllChartData+dictOptions** | 图表不渲染的根本原因：①缺少字段解析回写（fieldOption空）；②config缺dictOptions。全流程自定义脚本4步不可少；推荐方式(dataset_ops+batch-add)手动指定字段可跳过queryFieldBySql |
| **🚨 "singleFile脚本"术语禁用于SQL场景** | `singleFile` 是文件数据集的 dataType 值（`dataType:'singleFile'`，上传 Excel/CSV）。SQL 场景的自定义脚本应称为"全流程自定义脚本"，以免混淆 |
| **SQL 数据集无 dbSource** | SQL 类型数据集必须指定 `dbSource`（数据库源 ID），否则报"数据源不存在" |
| **datasetItemList 字段名** | 创建数据集用 `datasetItemList`，不是 `onlDragDatasetItemList` |
| **API 数据集不需要 dbSource** | API 类型 `dbSource` 设为 `None`，否则可能报错 |
| **dataSetIzAgent 取值** | SQL 类型设 `''`（留空）；API 直连 `'0'`；API 代理 `'1'` |
| **多系列 chartData 格式** | 需 `type` 字段区分系列：`[{"name":"1月","value":10,"type":"系列A"}]` |
| **字典翻译用 jimu_dict** | 必须用 `/jmreport/dict/*`，禁止 `/sys/dict/*` |
| **SQL 注入检测拦截** | information_schema/SHOW TABLES 会被后端 SqlInjectionUtil 拦截 |
| **SQL 最大返回 1000 条** | `getChartData` 方法限制最大 1000 条记录 |
| **queryFieldBySql 需签名** | 该接口带 `@SignatureValidation`，需要 X-Sign/V-Sign/X-TIMESTAMP |
| **API 数据集 /add 字段名** | `datasetItemList`（不是 onlDragDatasetItemList）；/add 后无需再 queryById+edit 回写 |
| **数据源 /add result 类型** | 数据源 /add 的 result 是字符串 ID；数据集 /add 的 result 是完整 dict（用 `.get('id')` 取） |
| **response null 处理** | `result=null` 时 `.get('result',{})` 返回 None，必须用 `(resp.get('result') or {})` |
| **componentName 必须用中文名** | 批量生成时图层名用中文（如"基础柱形图"），禁止用 compType（JBar/JPie） |
| **singleFile 场景禁止 comp_ops.py --dataset-name** | 按索引映射导致字段错乱，必须在同一脚本内用 `bi_utils.add_component()` 显式语义映射 |
| **singleFile code 字段保留 jmf. 前缀** | 缺前缀报 SQLException |
| **singleFile 文件上传用 requests.post** | `bi_utils._request()` 不支持 files 参数 |
| **FILES result 类型** | files/get 的 result 是 dict，`json.loads(result.get('dbUrl','[]'))` 取文件列表 |
| **yapi_ops.py create-mock 参数** | 接口标题参数是 `--title`，不是 `--name` |
| **subprocess 调用 yapi_ops.py** | 子命令必须在 YAPI_BASE 之前：`['py','yapi_ops.py', cmd, YAPI_BASE, EMAIL, PWD]` |
| **YApi mock 前先 list** | 直接创建会重复，先 `yapi_ops.py list` 查已有接口，复用已存在的 |
| **写 Java 接口** | 禁止自行 Grep 搜索 Controller 文件，必须问用户路径；完成后脚本末尾必须输出接口 URL + 重启提示 |
| **lockd/解锁组件** | 锁定字段是顶层 `disabled`，解锁必须用自定义脚本操作顶层：`comp['disabled']=False; comp['selected']=False` |
| **多图表+联动场景** | 必须用 `multi_chart_linkage.py`，禁止逐个调 comp_ops.py |
| **设计器表单端点** | 固定端点 `/desform/api/list/options`、`/desform/api/fields/{tableName}`，禁止盲猜 |
| **Online表单 dataType=4** | 最易漏！漏写则 dataType=0，读不到表单数据 |
| **🚨 X-Low-App-ID 必须是应用 ID，不是仪表盘页面 ID** | QQY URL 格式：`/myapp/{appId}/drag/{pageId}`，appId ≠ pageId！`X-Low-App-ID` 填 appId，`query_page` 传 pageId。用错后 `/desform/api/list/options` 返回空列表，极易误判为"无表单"。若用户只给一个 ID，必须问清是应用 ID 还是页面 ID，或请提供完整 URL |
| **🚨 表单列表返回空时第一反应是检查 appId，禁止从现有组件推断表单** | 表单接口返回 `[]` 最常见原因：X-Low-App-ID 用了页面 ID。排查：① 验证 appId 是否正确 → ② 确认无误后告知用户。任何情况禁止自行决定使用哪个表单 |
| **🚨 QQY dataType=4 必须包含 compStyleConfig + analysis** | 缺少或为 `{}` 时前端 `useEChartsNew.ts` 访问 `.summary.showTotal` / `.showUnit.position` 抛 TypeError 白屏。禁止写 `'compStyleConfig': {}`，必须用完整默认值对象（见"组件 config 结构（dataType=4）"章节） |
| **🚨 修复 compStyleConfig 时用 `not cfg.get()` 而非 `not in`** | 空对象 `{}` 是 truthy 的 key，`'compStyleConfig' not in cfg` 为 False（不覆盖）。必须用 `if not cfg.get('compStyleConfig'):` 检测空值 |
| **仪表盘组件颜色设置** | JPie/JRose/JLine/JArea/JMixLineBar 等组件颜色必须用 `option.customColor`，格式 `[{"color1":"#FF","color":"#FF"}]`，`option.color` 无效 |
| **api.jeecg.com 是 YApi 服务器** | 禁止对其尝试 JeecgBoot /sys/login，YApi 登录路径是 /api/user/login |
| **组件默认背景色** | `config.background` 必须为 `#FFFFFF`（白色），禁止使用 `#FFFFFF00`（透明）或 `transparent` |
| **坐标单位** | 仪表盘用**栅格**坐标（24列），不是像素 |
| **总宽度限制** | 同行组件 w 之和 ≤ 24 |
| **🚨 QQY dataType=4 filter 必须含 conditionFields** | 缺少 `filter.conditionFields` 导致 `common.ts:1657` 抛 `TypeError: Cannot read properties of undefined (reading 'forEach')`，同时设置弹窗无法打开。所有 dataType=4 组件 filter 必须写：`{'queryField': '', 'queryRange': 'all', 'conditionFields': []}` |
| **🚨 QQY JBar/折线/散点等笛卡尔坐标图必须在 option 显式写 series 类型** | QQY dataType=4 的柱形/折线/面积/散点/条形图，若 `option` 中没有 `series: [{type: 'bar/line/scatter'}]`，ECharts 报 `Unknown series undefined`，图表只显示坐标轴不渲染数据。必须补充：`'series': [{'type': 'bar'}]`（或 line/scatter）+ `xAxis` + `yAxis` + `grid` |
| **🚨 QQY isGroup 图表分组字段是 typeFields 而非 groupFields** | dataType=4 多系列/分组图表（JStackBar/JMultipleBar/JRadar/JPivotTable 等）的分组字段键名是 `typeFields`，不是 `groupFields`，写错则分组无效 |
| **🚨 isLowApp 禁止写入数据库** | `isLowApp: True` 是前端引擎切换标识（DragEngineQqyun.vue 判断），不存数据库，创建/保存页面的 body 中禁止传此字段。`lowAppId` 才是数据库字段，必须在 body 中传 |
| **🚨 QQY analysis 字段默认值错误** | 正确默认值：`{'showData': 1, 'isRawData': True, 'showMode': 1, 'isCompare': False, 'izTimeOut': False, 'showFields': [], 'trendType': '1', 'timeOut': 0}`。❌ 旧错误值：`isRawData=False, showMode=0, showData=0, trendType='mom'`——这些值会导致数据展示模式异常 |
| **🚨 QQY filter 必须含 conditionMode:"and"** | `filter` 缺少 `conditionMode` 字段会导致筛选条件模式未定义，设置弹窗行为异常。正确完整结构：`{'queryField': 'create_time', 'queryRange': 'all', 'conditionMode': 'and', 'conditionFields': [], 'customTime': []}` |
| **🚨 conditionFields 条目必须同时含 val + fieldValue + condition** | 通过 API 写入筛选条件时，conditionFields 每条必须包含：`val`（显示值）、`fieldValue`（后端实际查询值，缺少时条件不生效）、`condition`（条件类型枚举，如 `'4'`=包含/LIKE）。仅有 `val` 无 `fieldValue` 则查询不执行过滤。完整结构：`{'fieldName':'xxx','fieldTxt':'订单名称','fieldType':'string','widgetType':'input','rule':'LIKE','condition':'4','val':'华为','fieldValue':'华为','options':[],'fieldShow':True,'customDateType':''}` |
| **🚨 QQY JFilterQuery 添加前必须询问用户三项信息** | 禁止直接 `comp_ops.py add JFilterQuery` 后结束。必须先询问：①联动哪几个图表（列出当前页面图表供选择）；②添加几个查询条件；③每个条件关联哪个字段。收集完信息后一次性配置完整 config。详见 `references/qqy-guide.md` 「QQY 查询条件完整配置流程」 |
| **🚨 QQY JFilterQuery config 缺少 4 个必填字段** | `conditionFields`（顶层）/ `filter` / `linkageConfig` / `chartData`（JSON字符串）四个字段缺一不可。缺少任意一个：条件不显示 / 筛选面板报错 / 查询不触发刷新 / 前端解析失败。完整结构见 `references/qqy-guide.md` |
| **🚨 QQY JFilterQuery chartData 必须是 JSON 字符串** | `chartData` 存储的是 `json.dumps([...])` 的字符串，不能是 Python list。写成 list 则前端 `JSON.parse` 失败，查询条件无法渲染 |
| **🚨 QQY JFilterQuery conditionFields 必须在顶层和 filter 内各写一份** | `config.conditionFields` 和 `config.filter.conditionFields` 必须同时存在且内容相同。只写其中一处则另一处报 TypeError |
| **🚨 QQY JFilterQuery 禁止修改目标图表** | 联动完全由 JFilterQuery 自身的 `linkageConfig` 驱动，目标图表（JBar/JLine等）无需添加 drillData 或任何修改 |
| **🚨 QQY JFilterQuery relationChartList.options 需过滤类型 + 去除 dataType:null** | `/desform/api/fields` 返回的字段需过滤 `SKIP_TYPES`（file-upload/imgupload等），且删除 `options.dataType: null`（与前端参考JSON一致，否则字段对比异常） |
| **🚨 QQY filterField 不能为空数组** | `filterField: []` 导致图表设置面板无可选筛选字段。必须填入表单所有字段，每条包含 `fieldShow: True`、完整 `options` 对象；系统字段（create_by/update_by/create_time/update_time/bpm_status）也要包含；日期字段加 `customDateType: '1'`，人员字段加 `customDateType: '3'` |
| **🚨 QQY nameFields/typeFields 必须含 fieldShow:True** | 字段条目缺少 `fieldShow` 属性会导致字段在设置面板中不可见/不可操作。每个 nameFields/typeFields 条目必须加 `'fieldShow': True` |
| **🚨 QQY valueFields 必须含 fieldShow:True + groupField:""** | valueFields 条目除 `fieldShow: True` 外还必须含 `'groupField': ''`，缺少 groupField 导致聚合分组配置失效 |
| **🚨 QQY sorts 必须含 type:"" 字段** | `sorts: {'name': ''}` 不完整，必须写 `sorts: {'name': '', 'type': ''}`，缺少 type 字段导致排序设置面板异常 |
| **🚨 QQY JPivotTable 缺 pivotTable 子配置 → "暂无数据"** | JPivotTable 没有 `pivotTable` 顶层配置对象时，透视表始终显示"暂无数据"。必须在 config 顶层加：`'pivotTable': {'columnSummary': {'controlList': [{'showName':'','show':True,'totalType':'sum','position':'2','key':'<值字段名>'}], 'name':'列汇总','location':'right'}, 'lineSummary': {'controlList':[...],'name':'行汇总','location':'bottom'}, 'unitList':[{'showName':'','unit':'','key':'<值字段名>'}], 'showLineCount':0,'showColumnCount':0,'showColumnTotal':False,'showLineTotal':False}` |
| **🚨 QQY 地图组件缺 commonOption → 地图不加载** | JAreaMap/JBubbleMap/JHeatMap/JBarMap 的 config 顶层必须含 `commonOption`，缺失导致地图样式/颜色完全失效。必须加：`'commonOption': {'barSize':10,'gradientColor':False,'breadcrumb':{'drillDown':False,'textColor':'#000000'},'areaColor':{'color1':'#f7f7f7','color2':'#fcc02e'},'barColor':'#fff176','barColor2':'#fcc02e','inRange':{'color':['#04387b','#467bc0']}}` |
| **🚨 QQY 地图 option geo 必须用旧版 ECharts 格式** | `handleMapWarn`（useEChartsMap.ts:1145）处理 `itemStyle.normal/emphasis` 嵌套格式；使用新版 `itemStyle.areaColor` 直接写法样式失效。正确格式：`'geo':{'top':30,'zoom':1,'roam':False,'itemStyle':{'normal':{'areaColor':'#f7f7f7','borderColor':'#b0b5c1','borderWidth':0.5},'emphasis':{'areaColor':'#fcc02e'}},'label':{'emphasis':{'show':True,'color':'#000'}}}` |
| **🚨 QQY 地图 visualMap 必须含 seriesIndex** | ECharts 要求 heatmap series 必须有 visualMap 明确引用其 seriesIndex，否则报 `Heatmap must use with visualMap`。各类型 seriesIndex：JAreaMap→`[0]`(show:False)，JBubbleMap→`[1]`(show:False)，**JHeatMap→`[1]`(show:True)**，JBarMap→`[0]`(show:False)。缺 seriesIndex 或值错误→热力图崩溃 |
| **🚨 QQY 所有4种地图 option 都必须含 area 字段** | 不仅 JBubbleMap，全部4种地图的 `config.option?.area?.markerType` 都会被读取作为 series[0].type；缺失→type=undefined→`[ECharts] Unknown series undefined`。必须加：`'area':{'markerType':'effectScatter','markerColor':'#DDE330','shadowBlur':10,'markerCount':5,'markerOpacity':1,'scatterLabelShow':False,'value':['china'],'name':['中国']}` |
| **🚨 QQY 地图和表格 config 需要 seriesType/assistTypeFields/assistYFields** | JPivotTable、JAreaMap、JBubbleMap、JHeatMap、JBarMap 的 config 顶层缺少这3个字段会导致多系列/辅助轴配置失效。必须加：`seriesType:[{series:'1',type:'bar'},{series:'2',type:'bar'},{series:'',type:'bar'}]`；`assistTypeFields:[{fieldName:'create_time',fieldTxt:'创建时间',options:{},fieldType:'date',widgetType:'date',customDateType:'3'}]`；`assistYFields:[val_field_obj]` |
| **🚨 QQY 地图 valueFields 必须用表单实际数值字段，非固定 record_count** | record_count 只是"计数"的一种指标，不是地图 valueFields 的固定值。地图 valueFields 应使用用户表单中的数值类型字段（num_fields 中的字段）；仅在表单无数值字段时才以 record_count 兜底 |
| **🚨 QQY JPivotTable 透视表必须含 pivotTable 子配置** | 缺少 `pivotTable` 顶层配置时透视表始终"暂无数据"。必须动态从 valueFields 构建：`{'columnSummary':{'controlList':[{'showName':'','show':True,'totalType':'sum','position':'2','key':k}],'name':'列汇总','location':'right'},'lineSummary':{'controlList':[{'showName':'','show':True,'totalType':'sum','key':k}],'name':'行汇总','location':'bottom'},'unitList':[{'unit':'','numberLevel':'','position':'suffix','decimal':0,'key':k}],'showLineCount':0,'showColumnCount':0,'showColumnTotal':False,'showLineTotal':False}`；analysis 必须加 `compareType:''` |
| **🚨 QQY 地图 option 不能为空 {}** | 地图 option 必须包含完整 `geo`/`area`/`series`/`visualMap` 结构，否则地图不渲染。最小可用结构（以 JAreaMap 为例）：`{'drillDown':False,'area':{'name':['中国'],'value':['china'],'markerType':'effectScatter','markerColor':'#DDE330','shadowBlur':10,'markerCount':5,'markerOpacity':1,'scatterLabelShow':False,'shadowColor':'#DDE330'},'geo':{'top':30,'zoom':1,'roam':False,'itemStyle':{'normal':{'areaColor':'#f7f7f7','borderColor':'#b0b5c1','borderWidth':0.5},'emphasis':{'areaColor':'#fcc02e'}},'label':{'emphasis':{'show':True,'color':'#000'}}},'series':[{'type':'map','map':'china','geoIndex':0,'data':[]}],'visualMap':{'min':0,'max':200,'type':'continuous','show':False,'calculable':True,'top':'bottom','left':'5%','seriesIndex':[0]}}` |
| **🚨 QQY isGroup=true option 不能为空 {}** | `option: {}` 导致多系列图表不渲染柱体/线条。必须包含 `series: []`（空数组，非空对象）+ `grid`：`{'grid':{'top':90,'bottom':115},'series':[],'tooltip':{'trigger':'axis'}}`；JMultipleBar 的 series 可含样式提示：`[{'barWidth':15,'itemStyle':{'borderRadius':0}}]` |
| **🚨 QQY isGroup=true + xAxis.data:[] 阻止 X 轴渲染** | 笛卡尔坐标 isGroup 图表（JStackBar/JMultipleBar/JMixLineBar/JMultipleLine 等）option 中若含 `xAxis: {'type':'category','data':[]}` 或 `yAxis: {'type':'category','data':[]}`，前端无法动态填充分类轴，X 轴永远为空。必须去掉 `data: []` 只写 `type`，或完全省略 xAxis/yAxis |
| **🚨 QQY seriesType 作用域：只有 JPivotTable + 4个地图 填充非空数组** | 其余26个统计图表（包括 isGroup=True 的分组图表）`seriesType` 必须为 `[]`。只有 JPivotTable/JAreaMap/JBubbleMap/JHeatMap/JBarMap 用 `[{'series':'1','type':'bar'},{'series':'2','type':'bar'},{'series':'','type':'bar'}]` |
| **🚨 QQY formName 必须精确匹配表单显示名** | `formName` 是表单显示名称（如"测试表单"），不是 formCode（如 jeecg_1111_vjav），写错不影响数据查询但会导致配置面板显示混乱。必须先查询确认表单名：`GET /desform/api/list/options?appId={APP_ID}` 取 label 字段 |
| **🚨 /desform/api/fields result 是 dict 非 list** | `result` 结构：`{desformCode, titleField, desformName, id, fields:[...]}` —— 字段列表在 `result.get('fields', [])`，不可直接迭代 result。字段属性：`model`=字段名，`name`=显示名，`type`=控件类型（input/number/money/select/textarea/file-upload）。直接 `for f in fields_resp.get('result', []):` 会报 `AttributeError: 'str' object has no attribute 'get'` |
| **🚨 设计器表单字段类型映射（必须小写）** | 控件类型→BI fieldType：input/textarea/select/radio/checkbox→`string`，number/money→`number`，date/datetime→`string`；❌ 大写 `String`/`Integer`/`Double` 与手工配置不一致，导致字段类型判断异常；`file-upload` 必须跳过（不能作维度/指标，强制加入 filterField 会导致前端解析报错） |
| **🚨 QQY 30个统计图表必须绑定表单（dataType=4），且必须先询问用户选表单和字段** | QQY（敲敲云）模式下添加**任意统计图表**，必须执行三步询问流程（见「QQY 统计图表三步询问流程」章节）：**① 调用 `/desform/api/list/options?appId={APP_ID}` 列出表单 → 展示给用户，询问"使用哪个表单" → ② 调用 `/desform/api/fields/{formCode}` 列出字段 → 展示给用户，询问"选哪些维度字段和数值字段" → ③ 用用户选定的表单+字段构建 dataType=4 完整 config 创建组件**。❌ 禁止自行复用已有组件的表单信息；❌ 禁止跳过询问直接执行；❌ 即使只有一个表单也要展示确认；❌ 禁止 dataType=1 静态数据兜底。**例外（dataType=1）：JCustomButton/JText/JFilterQuery/JCarousel/JDragEditor/JIframe/JCurrentTime 这7个UI功能组件** |
| **🚨 QQY 全组件不能用 dataType=1（静态数据）** | QQY 前端无论 dataType 是否为 4，`useEChartsNew.ts` 都会访问 `compStyleConfig.summary.showTotal`；`useDataSource.ts` 会访问 `filter.conditionFields`。用 dataType=1 但不加这些字段，同样报 TypeError 白屏。结论：QQY 仪表盘**统计图表**统一用 dataType=4；**JCustomButton 按钮组件例外，固定用 dataType=1** |
| **🚨 JCustomButton 按钮组件 dataType 必须为 1** | JCustomButton 不走表单数据接口，`dataType` 必须为 `1`，禁止设为 `4`。用户已明确验证。 |
| **🚨 operationType=3 的 customPage 必须是对象** | `customPage` 必须是 `{'label':'页面名','value':'pageId','key':'pageId'}`，禁止直接填 pageId 字符串，否则前端无法识别目标页面 |
| **🚨 operationType=1/2/3/6 的 appInfo 必须是 `{'type':'current'}`** | 不能为 `null`；**仅 op4（打开链接）才填 `null`**；op6（调用业务流程）同样必须填 `{'type':'current'}` |
| **🚨 bizParams/desformId 字段作用域** | `bizParams` 仅 op6 有；`desformId`（顶层）仅 op1/op2 有；op3/4 不要加这两个字段 |
| **🚨 QQY 重新生成全组件时直接覆盖，无需逐个删除** | `query_page(PAGE_ID)` → `bi_utils._page_components[PAGE_ID] = []` → 循环 append 30 个新组件 → `save_page(PAGE_ID)`，一次保存替换全部旧组件。不要逐个调 delete API（耗时且复杂） |
| **🚨 QQY option 坐标轴颜色禁用大屏暗色 #EEF1FA** | 仪表盘是白底亮色主题，`axisLabel.color:'#EEF1FA'` / `textStyle.color:'#EEF1FA'` 是大屏暗色，会导致坐标轴字体在白底上看不清。仪表盘 option 中**禁止写任何 axisLabel.color / textStyle.color 颜色覆盖**，使用默认色即可 |
| **🚨 QQY JWordCloud/JTotalProgress option 只需 `{title, card}`，JRankingList 需要完整横向条形图 option** | JWordCloud/JTotalProgress 前端自渲染，只要 title+card，加坐标轴会报错。JRankingList 必须有：`yAxis:{data:[],type:'category'}` + `xAxis:{type:'value'}` + `series:[{type:'bar'}]` + `grid:{containLabel:true}`；option 不能为 `{}` |
| **🚨 QQY DoubleLineBar yAxis 必须是双数组格式** | 双轴图需要两个 Y 轴，`yAxis` 必须写成数组：`[{"type":"value"},{"type":"value"}]`，不能是单对象。写成单对象则第二轴缺失，图表渲染失败 |
| **🚨 compStyleConfig.summary.showField 取值：'all'=全部字段，字段名=指定字段，''=未选（默认）** | 源码（CompStyleConfig.vue:438）`options.unshift({label:'全部', value:'all'})`，确认 `'all'` 是合法值，表示"显示全部字段"。用户请求"总计显示全部字段"时必须写 `'all'`，不能写 `''`。`''` 表示未选中状态（默认初始值），`'fieldName'` 表示仅显示指定字段。原规则"必须是 ''" 已废弃 |
| **🚨 修改 JBar 柱体颜色必须同时更新 customColor 和 series[0].itemStyle.color** | 只设置 `option.customColor[0].color/color1` 不够——`option.series[0].itemStyle.color` 仍保留原色（如 `#64b5f6`），实际渲染以 itemStyle 为准导致颜色不变。必须同时更新两处：`option.customColor=[{color:'#FFD700',color1:'#FFD700'}]` + `option.series[0].itemStyle.color='#FFD700'` |
| **🚨 QQY compStyleConfig freeze：headerFreeze/unilineShow/lineFreeze=True，columnFreeze=False** | 参考JSON权威值：`headerFreeze:True, unilineShow:True, lineFreeze:True, columnFreeze:False`。写 `columnFreeze:True` 与参考数据不符 |
| **🚨 compStyleConfig.summary.totalType 取值：平均值必须是 'average' 非 'avg'** | 前端 `a-radio-button` 枚举：`'sum'`=求和、`'max'`=最大值、`'min'`=最小值、`'average'`=平均值。❌ 常见错误：写 `'avg'` 导致汇总方式无法生效（前端选中态丢失，实际计算仍走默认求和）。完整枚举：`totalType: 'sum' | 'max' | 'min' | 'average'` |
| **🚨 QQY seriesType 禁止字符串，只有 JPivotTable+地图 用非空数组** | 禁止 `seriesType:'bar'/'line'` 字符串（`.map is not a function`）；其余26个统计图表必须是 `seriesType:[]`；只有 JPivotTable/JAreaMap/JBubbleMap/JHeatMap/JBarMap 用 `[{series:'1',type:'bar'},{series:'2',type:'bar'},{series:'',type:'bar'}]` |
| **🚨 QQY commonOption 只有4个地图类型需要，其余统计图表禁止包含** | 26个非地图统计图表不应包含 `commonOption`；只有 JAreaMap/JBubbleMap/JHeatMap/JBarMap 在 config 顶层加 `commonOption` |
| **🚨 QQY 地图 commonOption 各类型不同（来自参考JSON）** | JAreaMap/JBubbleMap：`{barSize:10,gradientColor:False,breadcrumb:{textColor:'#000000'},areaColor:{color1:'#f7f7f7',color2:'#fcc02e'},barColor:'#fff176',barColor2:'#fcc02e',inRange:{color:['#04387b','#467bc0']}}`；**JHeatMap** 加 `heat:{blurSize:20,pointSize:15,maxOpacity:1}`（blurSize:13/pointSize:6 是错误值）；JBarMap barSize=12 |
| **🚨 QQY JHeatMap 四项强制要求（每次必查）** | ①`visualMap.show:True`（False→双重崩溃：`Heatmap must use with visualMap` + `a11.map is not a function`）；②`visualMap.seriesIndex:[1]`；③`geo.roam:True`；④`commonOption` 含 `heat:{blurSize:20,pointSize:15,maxOpacity:1}` |
| **🚨 QQY JBarMap geo 必须含 aspectScale:0.96 + areaColor:'#37805B' + roam:True** | 参考JSON权威：`geo:{top:30,aspectScale:0.96,zoom:1,roam:True,itemStyle:{normal:{areaColor:'#37805B',...}},...}`；其余地图 areaColor 为 `''`（空字符串） |
| **🚨 QQY HorizontalBar 系图表 category 必须是 'HorizontalBar'** | `JHorizontalBar` / `JRankingList` / `JTotalProgress` 的 `chart.category` 必须是 `'HorizontalBar'`，写 `'Bar'` 导致方向/样式完全错误 |
| **🚨 QQY JPivotTable isGroup 必须为 True；option.title.text 固定写 '表格'** | isGroup=False 时行列分组不渲染；option 只需 `{title:{show:True,text:'表格'},card:{...}}`，text 不用组件名 |
| **🚨 QQY assistYFields/assistTypeFields 只有 JPivotTable+4地图 填充，其余 `[]`** | 26个普通统计图表必须是 `assistYFields:[]`，`assistTypeFields:[]`；只有 JPivotTable/JAreaMap/JBubbleMap/JHeatMap/JBarMap 填充 `[val_field]` / `[create_time字段]` |
| **🚨 QQY option.card 必须含 headColor:'#FFFFFF'；title.text 传组件显示名称** | 缺 `headColor` 导致卡片头颜色异常；`title.text:''` 空字符串则图表无标题 |
| **🚨 QQY JGauge 与 JColorGauge/JAntvGauge option 结构不同** | JGauge 需要完整 `series:[{min:0,data:[],max:100,axisTick:{lineStyle:{color:'#eee'},show:True},detail:{formatter:'{value}'},type:'gauge'}]`；JColorGauge/JAntvGauge 只需 `{title,card}`（无series） |
| **🚨 QQY JPivotTable pivotTable 必须包含所有 num_fields** | `columnSummary.controlList` / `lineSummary.controlList` / `unitList` 对每个数值字段建一个条目（用 `key:fieldName`），只用第一个值字段导致多值字段汇总列缺失 |
| **🚨 QQY filterField 必须在表单字段前预置5个系统字段** | filterField 数组**开头必须先放5个系统字段**：`create_by(select-user)` / `update_by(select-user)` / `update_time(date)` / `create_time(date)` / `bpm_status(select,dictCode:bpm_status)`，再拼表单字段。缺少系统字段导致筛选面板看不到这些维度，联动过滤不完整 |

> 完整踩坑记录见 `references/pitfalls.md`

---

## 图库管理（Icon Library）

### 接口清单

| 操作 | 方法 | 路径 |
|------|------|------|
| 上传图片 | POST multipart | `/jmreport/upload` |
| 新增图标 | POST JSON | `/drag/jimuReportIconLib/add` |
| 查询列表 | GET | `/drag/jimuReportIconLib/list` |
| 编辑图标 | PUT JSON | `/drag/jimuReportIconLib/edit` |
| 删除图标 | DELETE | `/drag/jimuReportIconLib/delete?id=` |

### 新增图标完整流程

**⚠️ 必须用 `urllib.request` 直接调用，不能用 `bi_utils._request`（会 401）**

```python
import urllib.request, json
BASE = "<api_base>"; TOKEN = "<token>"
# Step 1: 上传图片（multipart）→ 取 result["message"] 得 image_url
boundary = "----FormBoundary7MA4YWxkTrZu0gW"
with open(r"图片路径.jpg", "rb") as f: file_data = f.read()
body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"img.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n").encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
req = urllib.request.Request(f"{BASE}/jmreport/upload", data=body, headers={"X-Access-Token": TOKEN, "Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
image_url = json.loads(urllib.request.urlopen(req).read())["message"]
# Step 2: 新增到图标库
data = json.dumps({"imageUrl": image_url, "name": "图标名称", "type": "common"}).encode()
req2 = urllib.request.Request(f"{BASE}/drag/jimuReportIconLib/add", data=data, headers={"Content-Type": "application/json", "X-Access-Token": TOKEN}, method="POST")
print(json.loads(urllib.request.urlopen(req2).read()))
```

**字段说明：** `imageUrl`=上传返回的 `message`；`name`=用户提供；`type`=固定 `"common"`

## 字典管理（jimu_dict / jimu_dict_item）

大屏/仪表盘字典使用 `jimu_dict`/`jimu_dict_item`（**不是** sys_dict）。API 前缀：`/jmreport/dict/*` 和 `/jmreport/dictItem/*`

使用 `dict_ops.py`：`list`, `items`, `create`, `add-item`, `delete`, `bind`

> 完整操作流程 → 见 `references/dict-guide.md`

---

## 从模板复制创建仪表盘

使用 `template_ops.py copy` 一键复制：
```bash
PYTHONIOENCODING=utf-8 py template_ops.py copy $API_BASE $TOKEN --template-name "模板名称" --new-name "新仪表盘名"
```

**原则**：只替换图表组件（JBar/JLine/JPie等）的 chartData 和标题，不修改图片/文本等其他组件的样式位置。

> 详细流程、JTabToggle ID映射踩坑 → 见 `references/template-copy-guide.md`

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401） | 重新获取 X-Access-Token |
| `updateCount` 不匹配 | 重新查询页面获取最新值 |
| 组件不显示 | 检查 dataType、chartData（必须是 JSON 字符串）、option 是否完整 |
| 图表缩成小点 | 检查 `config.size` 是否用了像素值（不是栅格单位），仪表盘需 `w*75` / `h*11` |
| 标题重复显示 | 图表组件的 `option.card.title` 设为空，仅用 `option.title.text` |
| 布局错乱 | 确认使用栅格坐标（不是像素），w 总和 ≤ 24 |
| 中文乱码 | 使用 Python（不要用 curl） |

## 参考文档

### 已内联到 skill.md 的章节（无需读取外部文件）

| 章节名 | 内容摘要 |
|--------|---------|
| 图表查询与推荐 | 60+ 组件类型表、按数据类型推荐 compType |
| bi_utils 使用规则（强制） | 初始化、字段访问（comp['i']/comp['componentName']）、Windows 命令 |
| 常用组件配置路径速查（内联） | JStatsSummary/JCapsuleChart/JGauge/JProgress/JScrollBoard/JNumber |
| 布局组件使用指南（JTabs/JGrid） | config.child 结构、span 分配、嵌套规则、移动端响应式、完整 API 示例 |
| 快捷操作：comp_ops.py | 完整参数说明、四种数据模式、FreeMarker SQL、SLOT_CONFIGS |
| 快捷操作：linkage_ops.py | 联动/钻取全命令、触发器/接收器配置、易错点 |
| 快捷操作：link_ops.py + 自定义JS | jsConfig 参数、常用 JS 示例 |
| 核心踩坑速查 | ~45 条 🚨 规则，覆盖 bi_utils/组件名/颜色/模板缓存/YApi/FILES 等 |
| 图库管理 | 图标/图片列表、上传、删除完整 API 表 + Python urllib 示例 |

### 按需读取的外部文件

- `references/qqy-guide.md` — QQY 仪表盘完整参考（组件配置模板/dataType=4结构/批量生成/按钮操作）
- `references/bi-comp-option-config.md` — 组件样式配置路径（上表未列出的组件时才读）
- `references/bi-component-types.md` — 完整组件类型清单（skill.md 内联已覆盖常见类型）
- `references/bi_utils.py` — 工具库源码
- `references/templates/default/` — 29 个仪表盘模板 JSON 参考
- `references/dataset-guide.md` — 数据集完整操作指南（自定义脚本时读；预置脚本无需读）
- `references/api-dataset-examples.md` — 92条公开 mock API 示例
- `references/pitfalls.md` — 极端复杂场景扩展踩坑（常见问题优先查 skill.md 内联章节）
- `references/online-design-form-chart-guide.md` — Online/设计器表单图表完整指南
- `references/linkage-drill-guide.md` — 联动/钻取详细配置（skill.md 内联已覆盖常见用法）
- `references/page-config-guide.md` — 页面配置（背景/水印/主题）
- `references/map-guide.md` + `references/map-static-data.md` — 地图组件配置
- `references/dict-guide.md` — 字典翻译操作
- `references/group-guide.md` — 组件组合操作
- `references/template-copy-guide.md` — 模板复制详细流程
- `references/signing-datasource-guide.md` — 签名接口与 NoSQL 数据源
- `references/datasource-dataset-chart-guide.md` — 数据源+数据集+图表完整流程
- `references/core-configs/` — 组件默认配置、addPageComp逻辑、菜单层级
