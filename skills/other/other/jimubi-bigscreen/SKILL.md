---
name: jimubi-bigscreen
description: Use when user asks to create/design a big screen (大屏), full-screen data visualization, or says "创建大屏", "生成大屏", "新建大屏", "设计大屏", "做一个大屏", "BI大屏", "数据大屏", "可视化大屏", "监控大屏", "create big screen", "design big screen", "BI visualization big screen". Also triggers when user describes big screen requirements like "做一个销售数据大屏" or mentions full-screen display like "展厅展示", "监控室大屏". Make sure to use this skill for big screens (大屏) — NOT dashboards (仪表盘/看板), which use a completely different layout and styling system.
---

# JeecgBoot 大屏 AI 自动生成器

将自然语言的大屏需求转换为 drag page 配置，并通过 API 自动创建。

> **本 skill 专门处理大屏（bigScreen）模式**：全屏展示，绝对定位（像素坐标），深色主题，适用于监控室/展厅/展示墙。
> 仪表盘（看板）请使用 `jimubi-dashboard` skill。

## ⚠️ 强制规则：所有大屏相关操作必须优先通过本 skill 处理（无任何例外）

**触发范围**：凡涉及大屏的任何操作，包括但不限于：
- 创建/删除/修改大屏页面
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
1. 用户提出大屏相关需求
2. **第一步必须调用本 skill**（`Skill jimubi-bigscreen`）
3. 在 skill 上下文中读取凭据、选择脚本、执行操作

## 按需加载指南

本 skill 采用分层加载：核心规则始终在上下文中，专题文档按需读取。

| 场景 | 读取文件 |
|------|---------|
| 需要示例/演示数据（用户未提供数据源）| `references/api-dataset-examples.md`（92条公开 mock API，按行业分类：饮料零售/快消品/电商运营/库存管理/物业消防/AI产品/企业OA，直接用 `dataset_ops.py create-api` 创建，无需鉴权） |
| 创建/绑定/修改数据集（SQL/API/文件） | `references/dataset-guide.md`（**仅自定义脚本时需要**；使用 `dataset_ops.py` / `comp_ops.py --dataset-name` / `comp_ops.py --create-sql` / `comp_ops.py --sql-params` 预置脚本时**无需读取**，脚本已封装全部逻辑，含 FreeMarker 查询参数支持） |
| **多文件数据集（FILES）+ 图表** | 直接用 `files_ops.py create-bind`（**无需 Write 脚本**，无需读文档）。封装：创建空数据集→上传多文件→自动探查列名→推断 JOIN SQL→绑定图表。详见下方「快捷操作：files_ops.py」章节。**⚠️ 执行前必须先确认 Excel 列名**：JOIN 模式需要 `--group-by`、`--agg`、`--join-on` 三个参数，列名未知时禁止盲目执行，必须先询问用户 |
| 创建 WebSocket 数据集 | `references/dataset-guide.md`「创建 WebSocket 数据集」章节（**预置脚本不支持 WebSocket 类型**，必须自定义脚本：`dataType='websocket'`，`querySql` 存 ws:// 地址，无需 dbSource。绑定组件后通过 `/drag/websocket/sendData?chartId=xxx` 推送数据） |
| SQL 数据集使用存储过程（CALL） | 直接用 `proc_ops.py bindcomp`，**无需读任何文档**（一键完成：pymysql 创建存储过程 + 创建数据集 + 绑定组件；自动从数据源 API 获取数据库连接信息） |
| **多图表+联动批量生成**（≥2个图表且需要联动） | 直接用 `multi_chart_linkage.py`，**无需 Write 脚本**（单脚本：1次query + N次并发dataset创建 + 批量add_component + 内存linkageConfig + 1次save，比逐个调用 comp_ops.py+linkage_ops.py 节省约80%耗时）。**禁止**多图表+联动场景逐个调用 comp_ops.py |
| **生成全组件大屏**（含全部 99 个业务组件） | 直接用 `gen_all_comps.py`（预置脚本，**无需 Write 脚本**，无需读任何文档） |
| 从模板复制创建大屏 | 直接用 `template_ops.py copy`，**无需读任何文档** |
| 模板复制遇到问题时 | `references/template-copy-guide.md` |
| 地图组件（JAreaMap 等）| `references/map-guide.md`（含各组件专属配置速查：JFlyLineMap `commonOption.effect` 飞线动效、JHeatMap `commonOption.heat` 热力点、JTotalFlyLineMap/JTotalBarMap `option.timeline`、JTotalBarMap 右侧数据面板、JBubbleMap 散点扩展字段） + **静态数据必须用 `references/map-static-data.md`**（省份GDP/城市散点/飞线/时间轴飞线/分组柱形，禁止自行设计简陋数据） |
| 创建数据源 + SQL数据集 + 图表（完整流程或分步） | 直接用 `datasource_ops.py create` + `comp_ops.py add --create-sql --db-source`，**无需读文档**。遇到参数错误或流程问题时读 `references/datasource-dataset-chart-guide.md` |
| 自写 Java API 接口 + API 数据集 + 批量图表 | 直接参考 `references/pitfalls.md`「完整工作流：自写API接口」章节（Step 1-6），**无需读其他文档**。关键点：`@JimuNoLoginRequired`、`String` 返回裸数组、`dataType='api'`、不同图表 slot_labels 不同、脚本末尾输出接口地址+重启提示 |
| **YApi Mock 系统 + API 数据集**（用户选择 mock 方式） | 直接用 `yapi_ops.py create-mock`（**无需读任何文档**，已封装登录+创建+URL拼接）。固定项目：**proj_id=57（claude AI），catid=1157，basepath=/claude**，禁止探测。Mock URL 格式：`YAPI_BASE/mock/57/claude/{path}`。内置模板：`--template single/multi/pie/gauge/table/bar_multi` |
| 签名接口 / 数据源管理 / NoSQL 数据源 | `references/signing-datasource-guide.md`（含 MongoDB/ES/Redis 创建流程、dbUrl 格式、SQL 前缀语法、已知问题） |
| 组件联动 / 钻取 | 直接用 `linkage_ops.py`，参数说明见下方「快捷操作：linkage_ops.py」章节。**联动**（跨组件）用 `add-linkage --source --target --mapping`；**钻取**（自刷新下钻）用 `add-drill --comp --mapping`（无 --target）。仅遇到复杂问题时读 `references/linkage-drill-guide.md` |
| 组件外部链接跳转 | 直接用 `link_ops.py`，**无需读任何文档** |
| 组件自定义JS脚本 | 直接用 `link_ops.py set-js` 或 `comp_ops.py edit --set "jsConfig=..."`，**无需读任何文档**（参数说明见下方「快捷操作：自定义JS脚本」章节） |
| **组件连线（connectLine）** | 直接用自定义脚本操作 `linesConfig.connectLine`，**无需读任何文档**（完整结构见下方「快捷操作：组件连线」章节）。**仅 JImg 支持，JCustomIcon 不支持** |
| **JCustomIcon（图标）配置** | 无需读文档，直接用 `config.type='01'~'36'` 选图标（iconfont，共 36 个）。**图库图片用 JImg 不是 JCustomIcon**。详见下方「JCustomIcon 图标组件说明」章节 |
| **弹窗（Popup Modal）** | `references/popup-guide.md`（**必读**，有大量踩坑；config 必须为 dict、子组件用局部坐标、groupStyle 公式特殊，与普通组件完全不同） |
| 组件组合（JGroup） | `references/group-guide.md` |
| 修改页面配置（背景/水印/宽高） | `references/page-config-guide.md` |
| 字典翻译（jimu_dict） | `references/dict-guide.md` |
| 组件右键操作（图层排序/复制/删除/锁定） | `references/rightclick-actions-guide.md` |
| 遇到奇怪问题时查阅 | `references/pitfalls.md` |
| 组件样式配置路径 | `references/bi-comp-option-config.md`（**仅当 SKILL.md 中未列出目标组件的配置路径时才读取**；JStatsSummary/JCapsuleChart/JGauge/JProgress/JColorBlock/JScrollBoard 等常用组件的配置路径已内联在 SKILL.md「常用组件配置路径速查」章节，无需读 600 行文档） |
| **JPermanentCalendar（日历）组件配置** | `references/permanent-calendar-option-config.md`（容器/月份/周/日期/数据字段/圆圈的全部 option 路径，来源于源码 PermanentCalendarOption.vue） |
| **JCardScroll（卡片滚动）组件配置** | `references/card-scroll-option-config.md`（基础/滚动/卡片样式/内容字段全部 option 路径，三变体差异对照，来源于 CardScrollOption.vue + CardScroll.vue + config.ts） |
| **JStatsSummary（统计概览）组件配置** | `references/stats-summary-option-config.md`（布局/字段映射/卡片样式/分区样式/高亮配置全部 option 路径，三变体共用，来源于 StatsSummaryOption.vue + StatsSummarySectionOption.vue） |
| **JListProgress（列表进度图）组件配置** | `references/list-progress-option-config.md`（行/进度条轨道+填充+边框+超出/左中右区域字段/滚动配置全部 option 路径，来源于 ListProgressOption.vue） |
| **JBreakRing（多色环形图）组件配置** | `references/break-ring-option-config.md`（基础/标题/标题位置/引导线/颜色配置全部 option 路径，来源于 BreakRingOption.vue） |
| **JSemiGauge（半圆仪表盘）组件配置** | `references/semi-gauge-option-config.md`（角度/指针/数值/标题/外刻度/外进度环/内圆/内阴影/内进度环全部 option 路径，颜色数组格式说明，来源于 SemiGaugeOption.vue） |
| **JScrollList（滚动列表）组件配置** | `references/scroll-list-option-config.md`（基础/滚动/容器/表头/行/字段映射全部 option 路径，三变体差异对照，来源于 ScrollListOption.vue） |
| **JGaoDeMap（高德地图）组件配置** | `references/gaode-map-option-config.md`（中心坐标/地图样式/显示要素/视图模式/缩放/旋转俯仰全部 option 路径，含常用城市坐标参考，来源于 GaoDeMapSettings.vue） |
| **JOrbitRing（轨道环形文字）组件配置** | `references/orbit-ring-option-config.md`（轨道参数/文字样式/中心点图片/行星项目配置/联动 compVals，图文模式差异，来源于 OrbitRingOption.vue） |
| **JTabToggle（导航切换）组件配置** | `references/tab-toggle-option-config.md`（自动轮播/通用样式/高亮样式/个性化模式/items 数组/联动 compVals，来源于 TabToggleOption.vue） |
| 完整组件类型清单 | `references/bi-component-types.md` |
| 新增组件默认尺寸/数据/option | `references/core-configs/component-defaults.md`（82+ 组件的 w/h/chartData/option 默认值速查） |
| 组件创建流程（addPageComp） | `references/core-configs/addPageComp-logic.md`（newItem 结构、位置计算、保存逻辑） |
| 组件菜单分类树 | `references/core-configs/menu-hierarchy.md`（完整 menuData 层级 + 统计）。**全组件批量生成时无需读取**，SKILL.md 组件速查表已包含全部 compType→中文名映射，脚本中直接硬编码 categories 列表即可 |
| Online表单/设计器表单生成图表（dataType:4）— **单图表** | `references/online-design-form-chart-guide.md`（完整流程、API接口、config结构、字段映射、脚本化方案）。**全组件批量生成时无需读取**，直接按下方「Online表单全组件快速路径」执行，config结构已内联 |

## 图表查询与推荐（用户询问或需求不明确时）

### 场景一：用户询问"可以使用什么图表"

**触发条件**：用户问"有哪些图表"、"支持什么图表"、"可以用什么图表"、"图表有哪些类型"、"列出所有图表"等。

**处理方式**：直接输出以下完整图表分类表格（无需读取任何文档，无需执行任何脚本）：

| 分类 | 图表名称 | compType |
|------|---------|----------|
| **柱形图** | 基础柱形图 | JBar |
| | 堆叠柱形图 | JStackBar |
| | 动态柱形图 | JDynamicBar |
| | 胶囊图 | JCapsuleChart |
| | 基础条形图 | JHorizontalBar |
| | 背景柱形图 | JBackgroundBar |
| | 对比柱形图 | JMultipleBar |
| | 正负条形图 | JNegativeBar |
| | 百分比条形图 | JPercentBar |
| | 折柱图 | JMixLineBar |
| **饼状图** | 饼图 | JPie |
| | 南丁格尔玫瑰图 | JRose |
| | 旋转饼图 | JRotatePie |
| **折线图** | 基础折线图 | JLine |
| | 平滑曲线图 | JSmoothLine |
| | 阶梯折线图 | JStepLine |
| | 面积图 | JArea |
| | 对比折线图 | JMultipleLine |
| | 双轴图 | DoubleLineBar |
| **进度图** | 基础进度图 | JCustomProgress |
| | 进度图 | JProgress |
| | 列表进度图 | JListProgress |
| | 圆形进度图 | JRoundProgress |
| | 水波图 | JLiquid |
| **仪表盘** | 基础仪表盘 | JGauge |
| | 多色仪表盘 | JColorGauge |
| | 渐变仪表盘 | JAntvGauge |
| | 半圆仪表盘 | JSemiGauge |
| **环形图** | 饼状环形图 | JRing |
| | 多色环形图 | JBreakRing |
| | 基础环形图 | JRingProgress |
| | 动态环形图 | JActiveRing |
| | 玉珏图 | JRadialBar |
| **散点图** | 普通散点图 | JScatter |
| | 象限图 | JQuadrant |
| | 气泡图 | JBubble |
| **漏斗图** | 普通漏斗图 | JFunnel |
| | 金字塔漏斗图 | JPyramidFunnel |
| | 3D金字塔 | JPyramid3D |
| **雷达图** | 普通雷达图 | JRadar |
| | 圆形雷达图 | JCircleRadar |
| **象形图** | 象形柱图 | JPictorialBar |
| | 象形图 | JPictorial |
| | 男女占比 | JGender |
| **矩形/3D** | 矩形图 | JRectangle |
| | 3D柱形图 | JBar3d |
| | 3D分组柱形图 | JBarGroup3d |
| **字符云** | 字符云 | JWordCloud |
| | 图层字符云 | JImgWordCloud |
| | 闪动字符云 | JFlashCloud |
| **地图** | 区域地图 | JAreaMap |
| | 散点地图 | JBubbleMap |
| | 飞线地图 | JFlyLineMap |
| | 柱形地图 | JBarMap |
| | 热力地图 | JHeatMap |
| | 时间轴飞线地图 | JTotalFlyLineMap |
| | 柱形排名地图 | JTotalBarMap |
| | 高德地图 | JGaoDeMap |
| **表格/列表** | 轮播表 | JScrollBoard |
| | 表格 | JScrollTable |
| | 数据表格 | JCommonTable |
| | 数据列表 | JList |
| | 排行榜 | JScrollRankingBoard |
| | 个性排名 | JFlashList |
| | 气泡排名 | JBubbleRank |
| | 滚动列表(单行) | JScrollList_1 |
| | 滚动列表(多行+序号) | JScrollList_2 |
| | 滚动列表(带表头) | JScrollList_3 |
| | 发展历程 | JDevHistory |
| | 透视表 | JPivotTable |
| **统计/轮播** | 统计概览(卡片) | JStatsSummary_1 |
| | 统计概览(背景) | JStatsSummary_2 |
| | 统计概览(高亮) | JStatsSummary_3 |
| | 翻牌器 | JCountTo |
| | 数值 | JNumber |
| | 卡片滚动(横向) | JCardScroll_1 |
| | 卡片滚动(竖向+序号) | JCardScroll_2 |
| | 卡片滚动(高亮) | JCardScroll_3 |
| | 卡片轮播 | JCardCarousel |
| | 日历 | JPermanentCalendar |
| **装饰/辅助** | 边框1~13 | JDragBorder |
| | 装饰1~12 | JDragDecoration |
| | 图片 | JImg |
| | 轮播图 | JCarousel |
| | 图标 | JCustomIcon |
| | 文本 | JText |
| | 颜色块 | JColorBlock |
| | 当前时间 | JCurrentTime |
| | 轨道环形文字 | JOrbitRing |
| | 选项卡 | JSelectRadio |
| | 导航切换 | JTabToggle |
| | 富文本 | JDragEditor |
| | Iframe | JIframe |
| | 按钮 | JRadioButton |
| | 统计进度图 | JTotalProgress |
| | 排行榜(自定义) | JRankingList |
| | 自定义图表 | JCustomEchart |
| **视频** | 播放器 | JVideoPlay |
| | RTMP播放器 | JVideoJs |
| **天气** | 天气预报(多种样式) | JWeatherForecast |

---

### 场景二：用户图表需求不明确时给出推荐

**触发条件**：用户说"加一个图表"、"加一个图"、"给我展示数据"、"可视化一下"、"用什么图表好"等，没有明确说要哪种图表类型。

**处理方式**：根据用户描述的数据类型/业务场景，从以下推荐表中给出 3-5 个建议，说明各自适用场景，让用户选择：

| 数据类型/业务场景 | 推荐图表 | 理由 |
|-----------------|---------|------|
| 占比/构成分析 | 饼图(JPie)、环形图(JRing)、玫瑰图(JRose) | 直观展示各部分在整体中的比例 |
| 趋势/时序变化 | 折线图(JLine)、平滑曲线图(JSmoothLine)、面积图(JArea) | 反映随时间变化的走势 |
| 分类对比 | 柱形图(JBar)、条形图(JHorizontalBar)、对比柱形图(JMultipleBar) | 比较不同类别的数值大小 |
| 多系列对比 | 对比折线图(JMultipleLine)、对比柱形图(JMultipleBar)、堆叠柱形图(JStackBar) | 同时展示多个维度的数据 |
| 完成率/进度 | 进度图(JProgress)、仪表盘(JGauge)、水波图(JLiquid)、环形进度图(JRingProgress) | 展示目标达成程度 |
| 排行/Top N | 排行榜(JScrollRankingBoard)、胶囊图(JCapsuleChart)、动态柱形图(JDynamicBar) | 突出排名先后顺序 |
| KPI/核心指标 | 统计概览(JStatsSummary)、翻牌器(JCountTo)、数值(JNumber) | 大字号展示关键数字 |
| 地理分布 | 区域地图(JAreaMap)、散点地图(JBubbleMap)、柱形地图(JBarMap) | 展示地理位置相关数据 |
| 转化漏斗 | 漏斗图(JFunnel)、金字塔(JPyramidFunnel) | 展示各环节转化率递减 |
| 多维综合评估 | 雷达图(JRadar)、气泡图(JBubble) | 多维度综合打分或分布 |
| 数据列表/明细 | 轮播表(JScrollBoard)、数据表格(JCommonTable)、滚动列表(JScrollList) | 展示多条明细数据 |
| 词频/热词 | 词云(JWordCloud) | 展示关键词频次分布 |

**推荐话术：** 列出3-5个图表名+compType+一句话原因，末尾"请选择，我将立即创建"。

---

## SQL数据集创建标准流程（强制）

> **触发条件**：用户说"使用SQL数据集"、"增加SQL数据集"、"统计 xxx 表"、"生成图表"等涉及 SQL 数据集的任何场景，必须严格按以下四步执行，**不得跳过第1步**。

### 第1步：确认数据源（必须询问，禁止擅自选择）

先列出数据源让用户选择，等用户选择后再继续：
```bash
py datasource_ops.py list "<api_base>" "TOKEN"
```

### 第2步：根据业务场景自行编写SQL
- 用户指定数据源后，根据用户描述的业务场景，自行设计并编写合适的 SQL 语句
- **🚨 严禁自行猜测或编造表名**：必须先通过 pymysql 直连（`datasource_ops.py detail` 获取连接信息 + 向用户索取密码）执行 `SHOW TABLES` 确认表存在，再写 SQL。常见错误案例：擅自使用 `jimu_drag_page`，实际表名是 `onl_drag_page`（2026-04-15 事故）
- **必须使用预置脚本创建 SQL 数据集，禁止直接调用 `/drag/onlDragDatasetHead/add` API**（直接调 API 报"数据源连接失败"；预置脚本封装了正确的请求体格式）
- 使用 `comp_ops.py add --create-sql --db-source <ID>` 或 `dataset_ops.py create-sql` 创建

### 第3步：创建SQL数据集
- 分组必须使用 **"示例数据集"**（`dataset_ops.py create-sql` 已内置 `--group "示例数据集"` 默认值，自动查询/创建，无需手写代码）
- **直接使用 `dataset_ops.py create-sql`**（已修复 `--db-source` 参数 bug，可正常使用）：
```bash
py dataset_ops.py create-sql $API_BASE $TOKEN \
  --name "数据集名称" --db-source "数据源ID" \
  --sql "SELECT name, value FROM table GROUP BY name" \
  --fields "name:String,value:Integer"
# --group 默认 "示例数据集"，无需额外传参
```
- 数据集创建完成后，**必须执行查询解析验证**确认数据正常返回

### 第4步：后续绑定操作（按需）
- 询问用户是否需要将数据集绑定到图表组件
- 如需要，使用 `comp_ops.py --dataset-name` 或 `comp_ops.py --create-sql` 执行绑定

---

## 文件数据集创建标准流程（多文件 FILES）

> **触发条件**：用户说"多文件数据集"、"FILES"、"上传多个Excel文件"、"JOIN多个文件"，或明确指定需要多个文件关联查询时使用。
> **注意**：用户只说"文件数据集"或提供一个文件时，应使用**单文件数据集（singleFile）**流程（见下一节）。

### 标准流程（5步）

> ⚠️ **实测可行顺序**：先创建空数据集 → 上传文件 → 获取表名 → 更新 SQL + 字段列表；也可先上传再创建（带 content 字段）。两种顺序均可，但先创建再上传更常见（数据集 ID 上传后立即可用）。

| 步骤 | 操作 | 接口地址 |
|------|------|----------|
| 第1步 | 创建空 FILES 数据集（querySql 可为空，后续更新） | `POST /drag/onlDragDatasetHead/add`（`dataType='FILES'`, `dbSource=页面ID`, `parentId=示例数据集分组ID`） |
| 第2步 | 上传所有文件（不传 isSingle，带 reportId） | `POST /jmreport/source/datasource/files/add`（参数：`{reportId: 大屏ID, file: 二进制}`，**不传** `isSingle`） |
| 第3步 | 获取文件列表，提取系统生成的真实表名 | `GET /jmreport/source/datasource/files/get?reportId=大屏ID`，**⚠️ `result` 是 dict**，真实表名在 `json.loads(result['dbUrl'])` 数组的 `name` 字段（格式：`jmf.Sheet1_orders_excel`） |
| 第4步 | 用真实表名编写 SQL，更新数据集（queryById + edit） | 先 `queryById` 取实体，再填入 `querySql` 和 `datasetItemList`，调 `edit` 保存 |
| 第5步 | 添加图表，绑定多文件数据集 | 组件绑定时 `dataSetType: 'FILES'`，`dataSetIzAgent: '1'`，dataMapping 用 SQL 字段别名 |

### 关键要点

- **上传文件自动加 HHMM 时间戳后缀**（避免 H2 表名冲突）
- **value 是 SQL 关键字**：用 `sales`/`amount`/`total` 等替代
- **上传必须带 `reportId` 参数**；`dbSource` 必须与 `reportId` 一致
- **files/get 的 result 是 dict**：`json.loads(result.get('dbUrl','[]'))` 取 `name` 字段
- **queryFileFieldBySql 需签名，bi_utils 不支持**：直接传 `datasetItemList` + `getAllChartData` 验证
- **SQL 别名不加单引号**：`SELECT col as type`（不是 `'type'`）
- **Excel 表名规律**：`xxx.xlsx` → `Sheet1_{xxx}_excel`（files/get 失败时用作 fallback）

### files/get 正确解析方式

```python
# ✅ 正确：result 是 dict，dbUrl 是 JSON 字符串
files_resp = bi_utils._request('GET', '/jmreport/source/datasource/files/get', params={'reportId': PAGE_ID})
result = files_resp.get('result') or {}
file_list = json.loads(result.get('dbUrl', '[]'))  # [{"fileName":"products.xlsx","name":"jmf.Sheet1_products_excel"}, ...]

# 按文件名关键词匹配
products_table = next((f['name'] for f in file_list if 'product' in f['name'].lower()), 'jmf.Sheet1_products_excel')
orders_table   = next((f['name'] for f in file_list if 'order'   in f['name'].lower()), 'jmf.Sheet1_orders_excel')

# ❌ 错误：不能把 result 当 list 迭代
# file_list = (files_resp.get('result') or [])  # result 是 dict 不是 list！
```

### SQL 字段别名与 dataMapping 对应

| SQL 字段别名 | dataMapping mapping | 说明 |
|-------------|---------------------|------|
| `as sales` | `'sales'` | 不能用 `'value'` |
| `as amount` | `'amount'` | 不能用 `'value'` |
| `as type` | `'type'` | 分组字段，**不能加单引号** |
| `as name` | `'name'` | 维度字段，**不能加单引号** |

**详细操作步骤和代码示例见** `references/dataset-guide.md` 的「多文件数据集（FILES）标准操作流程」章节。

---

## 单文件数据集创建标准流程（singleFile）

> **触发条件**：用户说"单文件数据集"、"使用单个Excel文件"、"singleFile"，或明确指定只上传一个文件时使用。

### 关键区别

| 特性 | 单文件 (singleFile) | 多文件 (FILES) |
|------|---------------------|---------------|
| dataType | `'singleFile'` | `'FILES'` |
| 文件数量 | 仅1个文件 | 支持多个文件，可JOIN |
| SQL查询 | `select * from {table_name}` 简单查询 | 支持复杂SQL和JOIN |
| 文件上传参数 | `isSingle=true` | 不传isSingle参数 |
| dbSource | 页面ID（reportId） | 页面ID（reportId） |
| code字段 | 必须等于实际表名 | 可自定义 |

### 标准流程（5步）

> ⚠️ **第5步必须在同一脚本内用 `bi_utils.add_component()` 完成，禁止拆成两个脚本，禁止用 `comp_ops.py --dataset-name`。**（`--dataset-name` 按索引顺序映射而非语义匹配，导致图表显示错误数据）

| 步骤 | 操作 | 关键点 |
|------|------|--------|
| 第1步 | 上传文件（带isSingle=true） | 必须传`isSingle=true`参数；**`bi_utils._request()` 不支持 `files` 参数，必须用 `requests.post(..., files=...)` 直接上传** |
| 第2步 | 预览获取字段 | 用preview API获取文件实际字段 |
| 第3步 | 创建数据集 | dataType='singleFile'，code=表名，content=文件列表JSON |
| 第4步 | 验证数据 | getAllChartData确认返回数据 |
| 第5步 | 在**同一脚本内**用 `bi_utils.add_component()` 添加图表 | 显式指定 `dataMapping`（语义映射），`dataSetType='singleFile'`，`dataSetIzAgent=''` |

### singleFile 快速路径（强制 3 轮完成）

```
轮次1: [并行] Read 凭据 + Bash openpyxl/xlrd 分析 Excel 列名
轮次2: [并行] Bash cp bi_utils.py + Write singlefile_chart.py（全流程一脚本）
轮次3: Bash PYTHONIOENCODING=utf-8 py singlefile_chart.py && rm 清理
```

**全流程一脚本模板：** 详见 `references/dataset-guide.md`「创建单文件数据集（singleFile）端到端」章节。关键结构：
```python
# 上传（必须用 requests.post，bi_utils._request 不支持 files 参数）
up = requests.post(f"{API_BASE}/jmreport/source/datasource/files/add",
    headers={"X-Access-Token": TOKEN}, params={"reportId": PAGE_ID, "isSingle": "true"},
    files={"file": (filename, file_data, "application/octet-stream")}).json()
table_name = (json.loads((up.get("result") or {}).get("dbUrl", "[]")) or [{}])[0].get("name")
# 建数据集（parentId="1516743332632494082"，code=table_name 含 jmf. 前缀）
# 查询页面缓存template，再 add_component（显式语义映射），再 save_page
page = bi_utils.query_page(PAGE_ID); bi_utils._page_components[PAGE_ID] = page.get('template', [])
```

### 关键要点

- **querySql**：`select * from jmf.{table_name}`（必须含 `jmf.` 前缀，不做聚合）
- **表名解析**：`json.loads(result.get("dbUrl","[]"))[0].get("name")`（不是 `result.tableName`）
- **code 字段**：保留 `jmf.` 前缀（缺前缀报 SQLException），禁止 `replace('jmf.','')`
- **dataSetIzAgent**：singleFile 设 `''`（FILES 才用 `'1'`）
- **parentId**：固定 id=`1516743332632494082`（示例数据集）
- **写脚本用 Write 工具**，禁止 bash heredoc（含单引号必报错）

**详细操作步骤和代码示例见** `references/dataset-guide.md` 的「创建单文件数据集（singleFile）端到端」章节。

---

## API数据集创建标准流程（强制）

> **触发条件**：用户说"使用API数据集创建图表"、"用API数据集"，且未明确指定接口地址或SQL数据集时，必须严格按以下五步执行。

### ⚡ 快捷路径：用户已给出 API 地址时（2轮完成，禁止任何探测步骤）

**触发条件**：用户需求中明确包含 API 接口地址（如 `https://...`）。

**强制流程（严格 2 轮，禁止多余步骤）：**
```
轮次1: cp dataset_ops.py + comp_ops.py + bi_utils.py + default_configs.json && ls验证
轮次2: dataset_ops.py create-api ... && comp_ops.py add --dataset-name ... && rm
```

**⚠️ 禁止行为（已观测违规 2026-04-10）：**
- 禁止先用 `--dataset-name` 查找不存在的数据集（查不到就添加静态组件，浪费 3 轮）
- 禁止先 `comp_ops.py add` 添加静态数据组件再删除重来
- 禁止询问数据来源（用户已给出地址，无需问 mock 还是自写接口）

---

### ⚡ 快捷路径：YApi Mock + 批量图表（2轮完成，强制规范）

**触发条件**：用户选择 YApi Mock 方式 + 需要生成同类型全部图表（如柱形图类全部10种）。

**强制流程（严格 2 轮）：**
```
轮次1: [并行] Bash: yapi list（查已有接口，复用勿重建）
               Write: 批量脚本（内嵌数据集创建+全部图表添加，直接填入最终凭据）
轮次2: Bash: cp "<skill_base_dir>/references/bi_utils.py" . && \
             cp "<skill_base_dir>/references/scripts/default_configs.json" . && \
             PYTHONIOENCODING=utf-8 py batch_script.py && \
             rm batch_script.py bi_utils.py default_configs.json
```

**五条强制规则：**
1. cp 必须与 py 在同一命令链（轮次间文件会丢失）
2. Write 脚本与 yapi list 必须同轮并行
3. 批量脚本内嵌数据集创建逻辑，禁止分轮执行
4. 脚本内置 mock 复用逻辑，禁止看 yapi list 结果后再 Edit 脚本
5. yapi 复用逻辑按路径精确匹配（如 `/claude/bar_multi`），禁止宽泛正则（如 `'bar' in line` 命中错误接口）

**批量脚本结构（query_page → 缓存 template → 创建数据集 → 批量 add_component → save_page）：**
```python
# 1. 查询页面并立即缓存（禁止省略缓存步骤，否则 save_page 清空已有组件）
page = bi_utils.query_page(PAGE_ID)
bi_utils._page_components[PAGE_ID] = page.get('template', [])
# 2. 创建数据集（/drag/onlDragDatasetHead/add，parentId 用示例数据集固定ID 1516743332632494082）
# 3. 循环 bi_utils.add_component() 批量添加（1次 query + N次内存add + 1次save）
# 4. bi_utils.save_page(PAGE_ID)
```

---

### 第1步：确认是否已有接口
- 用户**已指定**接口地址 → 走上方「快捷路径」，直接 `dataset_ops.py create-api` + `comp_ops.py add`
- 用户**未指定** → 执行第2步

### 第2步：询问数据来源方式（必须询问，禁止擅自决定）
向用户提问，选择：
1. 使用 **mock** 创建API接口（使用YApi Mock系统）
2. 使用**自定义接口**（在后端编写Java接口）

### 第3步：根据选择收集信息并创建接口

**选择1（mock接口）：**
- 询问：mock系统接口地址、账号密码、业务场景描述
- 参考按需加载表中「YApi Mock 系统 + API 数据集」章节（`references/pitfalls.md`）执行

**选择2（自定义接口）：**
- 询问：接口要编写到哪个Controller文件、业务场景描述
- **禁止自行搜索文件**，必须直接询问用户Controller路径
- 参考按需加载表中「自写 Java API 接口 + API 数据集 + 批量图表」章节（`references/pitfalls.md`）执行

### 第4步：创建API数据集（含字段列表）
- 分组用 **"示例数据集"**（固定 id=`1516743332632494082`，可直接硬编码）
- **【强制】`/add` 时直接传 `datasetItemList`**（字段名不是 `onlDragDatasetItemList`），无需 `queryFieldByApi`（常返回空）
- `/add` 返回的 `result` 是完整对象 dict，取 DS_ID：`(add_r.get('result') or {}).get('id')`

```python
ds_fields = [
    {'fieldName': 'name',  'fieldTxt': '名称', 'fieldType': 'String',  'izShow': 'Y', 'orderNum': 0},
    {'fieldName': 'value', 'fieldTxt': '数值', 'fieldType': 'Integer', 'izShow': 'Y', 'orderNum': 1},
    # 多系列图表额外加 type/group 字段
    {'fieldName': 'type',  'fieldTxt': '分组', 'fieldType': 'String',  'izShow': 'Y', 'orderNum': 2},
]
add_r = bi_utils._request('POST', '/drag/onlDragDatasetHead/add', data={
    'name': '数据集名', 'code': 'ds_xxx', 'dataType': 'api',
    'querySql': API_URL, 'apiMethod': 'get', 'parentId': parent_id,
    'datasetItemList': ds_fields,  # ⚠️ 直接传，无需解析接口
})
DS_ID = (add_r.get('result') or {}).get('id')  # ⚠️ result 是 dict，取 .id
```

### 第5步：绑定图表组件（dataMapping 必须按语义映射）
- **【强制】dataMapping 按字段语义显式指定，禁止按数组索引顺序映射**（索引 0→0 不等于语义对应）

```python
# ✅ 语义映射模板（单系列图表：JLine/JSmoothLine/JStepLine/JArea/JPie/JBar 等）
SINGLE_MAP = [
    {'filed': '维度', 'mapping': 'name'},
    {'filed': '数值', 'mapping': 'value'},
]
# ✅ 语义映射模板（多系列图表：JMultipleLine/DoubleLineBar/JStackBar/JMultipleBar 等）
MULTI_MAP = [
    {'filed': '分组', 'mapping': 'type'},   # 分组字段对应 type/group
    {'filed': '维度', 'mapping': 'name'},   # 维度对应 name（x轴标签）
    {'filed': '数值', 'mapping': 'value'},  # 数值对应 value
]
```

- `fieldOption` 必须同步传入（前端字段面板显示用）：
```python
field_option = [
    {'label': 'name',  'text': '名称', 'type': 'String',  'value': 'name',  'show': 'Y'},
    {'label': 'value', 'text': '数值', 'type': 'Integer', 'value': 'value', 'show': 'Y'},
    {'label': 'type',  'text': '分组', 'type': 'String',  'value': 'type',  'show': 'Y'},
]
```

---

## 大屏特征

- **布局**：绝对定位，坐标和尺寸单位为**像素**（如 x=50, y=280, w=860, h=380）
- **主题**：默认 `dark`，深色背景，亮色/霓虹文字
- **背景图**：默认 `/img/bg/bg4.png`，支持自定义
- **装饰元素**：常用 JDragBorder（边框）、JDragDecoration（装饰条）增强视觉效果
- **典型分辨率**：1920×1080

> **⚠️ 以下为大屏固定默认值，用户未说明时无需重复声明，脚本中直接使用：**
> - 分辨率：`1920×1080`（desJson.height=1080，宽度由前端固定）
> - 背景图：`/img/bg/bg4.png`（深空星空，极暗底色，文字必须用亮色）
> - 主题：`dark`，style：`bigScreen`，designType：`100`
> - 只有用户明确要求更换分辨率或背景图时才修改

### 默认背景图 bg4.png 配色指引（强制）

> **bg4.png 是深空星空渐变图**：四角纯黑（`#000000`），中心深海蓝（`#021533`～`#03234d`），整体极暗。文字/标签颜色必须足够亮才能保证可读性。

**适合在 bg4.png 上使用的颜色（亮色系）：**

| 用途 | 推荐色 | 说明 |
|------|--------|------|
| 主标题 | `#f0c040`（金色）、`#ffffff` | 高亮，确保醒目 |
| 小节标题 / 标签文字 | `#00d4ff`（青色）、`#e0f0ff` | 亮蓝，与背景蓝形成冷暖对比 |
| 普通数值 / 说明文字 | `#d4e8ff`、`#8ab8d0` | 淡蓝白，清晰但不刺眼 |
| 辅助/次要文字 | `#5a8ab0` | 暗蓝，用于 ticker/备注 |
| 图表轴标签 / 图例 | `#8ab8d0` | 不能用深色，否则被背景淹没 |
| 进度条/高亮强调 | `#f0c040`、`#2ed573`、`#ff4757` | 金/绿/红，高对比强调色 |

**严禁在 bg4.png 上使用的颜色（深色系，会被背景吞没）：**
- `#333333`、`#464646`、`#666666` 等深灰 — ECharts 默认轴色，**必须覆盖**
- `#000000`、`#0a1628`、`#021533` — 与背景融为一体，完全不可见
- `rgba(0,0,0,x)` — 任何黑色半透明

**ECharts 组件必须显式覆盖的默认暗色字段（强制）：**
```python
opt_patch = {
    'xAxis': {'axisLabel': {'color': '#8ab8d0'}, 'axisLine': {'lineStyle': {'color': '#1a3a5a'}}},
    'yAxis': {'axisLabel': {'color': '#8ab8d0'}, 'splitLine': {'lineStyle': {'color': '#1a3a5a55'}}},
    'legend': {'textStyle': {'color': '#8ab8d0'}},
    'tooltip': {'backgroundColor': '#0b1e3acc', 'textStyle': {'color': '#e0f0ff'}},
}
```

### 图层背景色规则（强制）

> **严禁将图层背景色设为红色或任何非透明颜色（除非用户明确指定）。** 用户未指定背景色时，`config.background` 和 `config.borderColor` 必须设为 `#FFFFFF00`（透明）。

| 规则 | 说明 |
|------|------|
| **默认值** | `config.background = '#FFFFFF00'`，`config.borderColor = '#FFFFFF00'` |
| **严禁使用 `rgba(0,0,0,0)`** | Ant Design 颜色选择器将其解析为**红色**（色相 0°=红色） |
| **唯一正确的透明写法** | `#FFFFFF00`（带 alpha 通道的十六进制透明白色） |
| **何时设为非透明** | 仅当用户明确指定了具体背景颜色时 |

### 图表配色规范（强制）

> 以下规范适用于所有使用 `option.customColor` 的图表组件（JPie/JRose/JLine/JArea/JMixLineBar/JMultipleLine/JStackBar/JMultipleBar/JCapsuleChart 等 20 种）。

| 场景 | 正确做法 |
|------|---------|
| 用户指定具体颜色 | 将颜色写入 `option.customColor`，格式 `[{"color1":"#FF0000","color":"#FF0000"},...]` |
| 用户要求"系统自定义配色" | 填入系统默认9色（见下方），**禁止设为 `[]`** |
| 用户要求"自定义配色" | 同上，填入完整色组数组 |
| `option.color` | 对这类组件无效，禁止使用 |

**系统默认9色（"系统自定义配色"的正确值，2026-04-20 实测）：**

```python
SYSTEM_CUSTOM_COLORS = [
    {"color1": "#1e90ff", "color": "#1e90ff"},
    {"color1": "#90ee90", "color": "#90ee90"},
    {"color1": "#00ced1", "color": "#00ced1"},
    {"color1": "#e2bd84", "color": "#e2bd84"},
    {"color1": "#7a90e0", "color": "#7a90e0"},
    {"color1": "#3ba272", "color": "#3ba272"},
    {"color1": "#2be7ff", "color": "#2be7ff"},
    {"color1": "#0a8ada", "color": "#0a8ada"},
    {"color1": "#ffd700", "color": "#ffd700"},
]
```

> **为什么不是 `[]`**：界面选择"系统自定义配色"时，前端会将系统色板中的9个颜色逐一写入该字段，而非清空。`[]` 与界面行为不一致，会导致图表使用 ECharts 内置配色而非系统配色。

## 前置条件

用户必须提供 API 地址和 X-Access-Token。


## 执行效率规则（强制）

### 简单操作直接执行，禁止多余探索

**禁止：** brainstorming、Explore子代理探源码、Read模板JSON（92KB+）、读 dataset-guide.md（预置脚本已封装）、展示摘要等确认、预置脚本前 `--help`、存储过程手写 pymysql（用 `proc_ops.py bindcomp`）

**正确做法：直接使用预置脚本（`template_ops.py`、`comp_ops.py`、`dataset_ops.py`）完成，1-2 轮工具调用。**

### 模板创建快速路径（强制，token 节省 90%+）

**创建整个大屏时，必须走以下快速路径，禁止自定义脚本：**

```
轮次1: cp template_ops.py + bi_utils.py（1 条 Bash 命令）
轮次2: py template_ops.py copy ... --replace '{...}' --board-data '{...}' && echo URL | clip.exe && rm（1 条 Bash 命令）
```

**替换字典构建规则：** 根据用户行业需求，直接构建 `--replace` JSON，无需分析模板内容。各模板中的占位文本是固定的：

**模板1：大数据可视化展示平台（通用/销售/综合类）**

| 占位文本 | 替换为行业术语 |
|---------|--------------|
| 大数据可视化展示平台 | 行业大屏标题 |
| 总金额 | 行业核心指标1名称 |
| 数量 | 行业核心指标2名称 |
| 数量结算率 / 金额结算率 等 | 行业百分比指标 |
| 2017年 / 2018年 | 近两年年份 |
| 结算率 | 行业趋势指标 |
| 年度数据 / 图例数据 | 行业分组标签 |
| 图例1/2/3/4 | 行业分类项 |
| 行1列1~行5列3 | 轮播表业务数据 |

**模板2：北京科技数字化云平台（科技/能源/电力/IoT/设备监控类）**

| 占位文本 | 替换为行业术语 |
|---------|--------------|
| 北京科技数字化云平台 | 行业大屏标题 |
| 网关管理/云组态/设备管理/动态数据/人员管理/监控管理/人员定位/能源管理 | 顶部8个导航菜单项 |
| 功耗总量 | 核心指标标题 |
| 电能耗 / 水能耗 | 双翻牌器标签 |
| 17563 / 11163 | 双翻牌器数值 |
| kw/h | 翻牌器单位 |
| 近七日电能耗 / 近七日水能耗 | 左侧双柱状图标题 |
| 一号~五号机房功率 | 5个仪表盘标题 |
| 设备功率信息 | 中间仪表盘区域标题 |
| 设备列表 / 信息 | 右侧面板标题 |
| 站点号：0001 / 设备状态：正常 / 环境温度：36摄氏度 / 在线设备：20 台 | 右侧4行信息文本 |
| 近七日设备在线数 | 右下折线图标题 |
| 基础折线图 | 折线图标题 |
| 1号~5号机房 / 0374~0378 / 正常 | 滚动表格数据 |
| 功率 / 编号 / 设备名 / 设备状态 | 数据字段名 |

**示例（风力发电行业，使用北京科技数字化云平台模板）：**
```bash
py template_ops.py copy $API_BASE $TOKEN \
  --template "北京科技数字化云平台_1014376428645961728.json" \
  --name "风力发电智慧监控平台" \
  --bg-image "/img/bg/bg4.png" \
  --replace '{"北京科技数字化云平台":"风力发电智慧监控平台","网关管理":"风机管理","云组态":"SCADA系统","设备管理":"机组管理","动态数据":"实时数据","人员管理":"运维管理","监控管理":"故障监控","人员定位":"风场巡检","能源管理":"发电管理","功耗总量":"发电总量","电能耗":"发电量","水能耗":"上网电量","17563":"58260","11163":"42850","kw/h":"万kWh","设备列表":"风机列表","信息":"风场信息","站点号：0001":"风场编号：WF-001","设备状态：正常":"风机状态：正常运行","环境温度：36摄氏度":"平均风速：8.5m/s","在线设备：20 台":"在线风机：126 台","近七日设备在线数":"近七日风机在线数","设备功率信息":"风机功率信息","近七日电能耗":"近七日发电量","近七日水能耗":"近七日弃风量","一号机房功率":"A区风机功率","二号机房功率":"B区风机功率","三号机房功率":"C区风机功率","四号机房功率":"D区风机功率","五号机房功率":"E区风机功率","基础折线图":"风机在线趋势","1号机房":"A区-01号风机","2号机房":"B区-03号风机","3号机房":"C区-07号风机","4号机房":"D区-12号风机","5号机房":"E区-05号风机","0374":"WF-A01","0375":"WF-B03","0376":"WF-C07","0377":"WF-D12","0378":"WF-E05","正常":"运行中","功率":"功率(MW)","编号":"风机编号","设备名":"风机名称","设备状态":"运行状态"}'
```

### Online表单全组件快速路径（强制，3 轮完成）

**用户要求"使用Online表单创建全组件"时，直接按以下流程执行，禁止读取 `online-design-form-chart-guide.md`。**

**⚠️ 凭据已在 MEMORY.md 上下文中，无需 Read 凭据文件（节省1轮）。**

```
轮次1: 列出表单（固定端点，**禁止盲猜其他路径**）：
       Online 表单：  GET /online/cgform/head/list
       设计器表单：   GET /desform/api/list/options  ← 返回 [{value:tableName, label:formName}]
       用户选定后，立即查询字段：
       Online 表单：  GET /online/cgform/field/listByHeadId?headId=xxx
       设计器表单：   GET /desform/api/fields/{tableName}?subTable=true  ← result.id=formId, result.fields[]
       展示字段列表，询问：维度字段（nameFields）、数值字段（valueFields）、分组字段（typeFields）
轮次2: 用户确认字段后 → cp bi_utils.py + Write 全组件脚本（并行）
轮次3: PYTHONIOENCODING=utf-8 py online_all_comps.py && rm bi_utils.py online_all_comps.py
```

**允许的48个 Online 表单图表类型（按顺序硬编码，禁止自行扩充）：**

> **⚠️ 第4个元素是中文名，必须直接用作 `componentName`，严禁用 `ct`（英文代码）作图层名！**
> 正确写法：`ct, cat, is_group, cn_name = chart_tuple`，然后 `'componentName': cn_name`

```python
ALL_CHARTS = [
    # (compType, category, isGroup, 中文名)
    ('JBar','Bar',False,'基础柱形图'), ('JStackBar','Bar',True,'堆叠柱形图'),
    ('JMultipleBar','Bar',True,'对比柱形图'), ('JNegativeBar','Bar',True,'正负柱形图'),
    ('JDynamicBar','Bar',False,'动态柱形图'), ('JMixLineBar','Bar',True,'折柱图'),
    ('JCapsuleChart','Bar',False,'胶囊图'), ('JPercentBar','Bar',True,'百分比条形图'),
    ('JHorizontalBar','HorizontalBar',False,'基础条形图'),
    ('JRankingList','HorizontalBar',False,'排行榜'),
    ('JTotalProgress','HorizontalBar',False,'进度图'),   # onlyValueChart，nameFields=[]
    ('JLine','Line',False,'基础折线图'), ('JArea','Line',False,'面积图'),
    ('JMultipleLine','Line',True,'对比折线图'),
    ('DoubleLineBar','Line',True,'双轴图'),               # nameFields=[]，typeFields=[维度]
    ('JStepLine','Line',False,'阶梯折线图'),
    ('JCustomProgress','Progress',False,'基础进度图'),
    ('JProgress','Progress',False,'进度图'),
    ('JLiquid','Progress',False,'水波图'),                # onlyValueChart，nameFields=[]
    ('JPictorialBar','Pictorial',False,'象形柱图'), ('JPictorial','Pictorial',False,'象形柱'),
    ('JPie','Pie',False,'基础饼状图'), ('JRing','Pie',False,'基础环形图'),
    ('JRose','Pie',False,'南丁格尔玫瑰'), ('JRotatePie','Pie',False,'旋转饼图'),
    ('JFunnel','Funnel',False,'基础漏斗图'), ('JPyramidFunnel','Funnel',False,'金字漏斗图'),
    ('JRadar','Radar',True,'基础雷达图'), ('JCircleRadar','Radar',True,'圆形雷达图'),
    ('JRingProgress','Ring',False,'基本环形图'), ('JActiveRing','Ring',False,'动态环形图'),
    ('JRadialBar','Ring',False,'玉珏图'),
    ('JRectangle','Rectangle',False,'矩形图'),
    ('JBar3d','threeD',False,'3D柱形图'), ('JBarGroup3d','threeD',True,'3D分组柱形图'),
    ('JColorGauge','Gauge',False,'多色仪表盘'), ('JGauge','Gauge',False,'基础仪表盘'),
    ('JAntvGauge','Gauge',False,'渐变仪表盘'),  # onlyValueChart（Gauge），nameFields=[]
    ('JNumber','Number',False,'数值图'),         # onlyValueChart（Number），nameFields=[]
    ('JScatter','Scatter',False,'基础散点图'),
    ('JBubble','Scatter',True,'气泡图'), ('JQuadrant','Scatter',True,'象限图'),
    ('JPivotTable','Table',True,'表格'),
    ('JAreaMap','Map',False,'区域地图'), ('JBubbleMap','Map',False,'散点地图'),
    ('JHeatMap','Map',False,'热力地图'), ('JBarMap','Map',False,'柱形地图'),
    ('JWordCloud','WordCloud',False,'词云'),
]
```

**onlyValueChart 判断规则（nameFields/typeFields 必须为 []）：**
- `category in {'Gauge','Number'}` → nameFields=[], typeFields=[]
- `compType in {'JTotalProgress','JLiquid'}` → nameFields=[], typeFields=[]
- Ring/Progress 分类其他组件（JCustomProgress/JProgress/JRingProgress 等）**不是** onlyValueChart，需要 nameFields

**DoubleLineBar 特殊字段规则：**
- nameFields=[], typeFields=[维度字段(name)], valueFields=[数值字段], assistYFields=[数值字段], assistTypeFields=[分组字段(sex)], seriesType=[]

**chart.isGroup 设置规则（JGauge/JColorGauge/JAntvGauge/DoubleLineBar 不设此字段，其余按实际 isGroup 值设）：**
```python
no_isg = {'JGauge','JColorGauge','JAntvGauge','DoubleLineBar'}
chart_cfg = {'category': cat, 'subclass': ct}
if ct not in no_isg:
    chart_cfg['isGroup'] = is_group
```

**compStyleConfig 必须包含完整 summary（否则前端报 showTotal 错误）：**
```python
'compStyleConfig': {
    'summary': {'showY':True,'showTotal':False,'showField':'all','totalType':'sum','showName':'总计'},
    'showUnit': {'numberLevel':'','decimal':None,'position':'suffix','unit':''},
    'assist': {'summary':{'showY':True,'showField':'all','totalType':'sum','showName':'总计'},
               'showUnit':{'numberLevel':'','decimal':None,'position':'suffix','unit':''}},
    'headerFreeze':False,'unilineShow':False,'izPage':False,
    'columnFreeze':False,'lineFreeze':False,
    'showProgressText':True,'progress':{'show':True,'name':'进度'},'target':{'show':True,'name':'目标'},
}
```

**filter 必须包含 conditionFields:[] 和 customTime:[]（否则 forEach 报错）：**
```python
'filter': {'queryField':'create_time','queryRange':'all','conditionMode':'AND','conditionFields':[],'customTime':[]}
```

**⚠️ 必填字段清单：**
- `dataType: 4`（**最易漏！** 漏写则 dataType=0 静态数据，读不到表单数据）
- `formType: 'online'`（漏掉表单未绑定）
- `formId: HEAD_ID`（**必须用 formId 不是 headId**）
- `formName`, `tableName`（缺失接口无法定位表）
- `option`：必须是图表专属 ECharts 配置，禁止传 `{}`（空 option 导致"加载中"）
- `commonOption`：地图类专用，必须单独设置

**option 分发规则（按 ct 选择，详见 `references/online-design-form-chart-guide.md` 第八节 `_get_default_chart_option()`）：**
- 地图类（MAP_TYPES）：必须同时设 `option`（含 drillDown/area/geo/visualMap）+ `commonOption`（必含 breadcrumb）
- 仪表盘（JGauge/JColorGauge/JAntvGauge/JSemiGauge）：无 xAxis/yAxis，series type='gauge'
- 水波图（JLiquid）：series type='liquidFill'
- 漏斗图（JFunnel/JPyramidFunnel）：series type='funnel'，tooltip trigger='item'
- 饼图系列（JPie/JRose/JActiveRing/JRotatePie）：**禁用含 xAxis/yAxis 的柱形 option**，series:[], tooltip trigger='item'
- JRing：series 必须预填充完整含 radius:['40%','70%']
- 雷达图（JRadar/JCircleRadar）：**禁用柱形 option**，必须含 radar:{indicator:[]}
- JProgress：专属双 series 结构（前景+背景），无 xAxis，title.show=False
- 条形图（JHorizontalBar/JRankingList/JTotalProgress）：yAxis=category，xAxis=value（轴对调）
- 词云图（JWordCloud/JImgWordCloud/JFlashCloud）：**禁用含 xAxis/yAxis 的柱形 option**
- DoubleLineBar：yAxis 必须是两元素数组，config 根层必须加 `seriesType:[]`
- JBar：series 必须含 `type:'bar'`（禁止传空数组 `[]`）
- 其他（JLine/JStackBar 等坐标轴类）：通用 xAxis/yAxis 对象格式（禁止数组格式）

- `analysis`：**必须是完整结构，禁止传 `{}`**（空 analysis 导致前端访问属性时 TypeError）
```python
'analysis': {'isRawData': True, 'showMode': 1, 'showData': 1, 'showFields': [],
             'isCompare': False, 'compareType': '', 'trendType': '1',
             'compareValue': None, 'izTimeOut': False, 'timeOut': 0}
```
- `sorts: {'name': '', 'type': ''}`（必须含 `type` 键，否则前端排序逻辑报错）
- `actionConfig: {'operateType': 'modal', 'modalName': '', 'url': ''}`（缺失前端崩溃）
- `dataNum: ''`、`filterField: [...]`（从 `/online/cgform/field/listByHeadId` 过滤后的字段列表）

**正确保存方式：** `query_page` → 缓存 `_page_components` → 循环 `add_component` → `queryById+edit` 合并保存 template 和 `desJson.height`（禁止 `save_page` 后再单独更新高度）。代码结构同"核心代码结构"章节。

**Online 表单字段对象格式（online formType，用于 nameFields/valueFields/typeFields）：**
```python
{'fieldName': 'xxx', 'fieldTxt': '显示名', 'fieldType': 'string'|'double'|'int',
 'widgetType': 'text', 'dictCode': '', 'dictField': '', 'dictTable': '', 'dictText': '', 'fieldExtendJson': ''}
```

**设计器表单字段对象格式（design formType，用于 nameFields/valueFields/typeFields）：**
```python
# ⚠️ 必须包含 options（完整原始 options）和 fieldShow:True
# 来源：ChartSetModal.vue 第572-579行（设计器 loadField 分支）
{'fieldName': item['model'], 'fieldTxt': item['name'],
 'fieldType': 'string'|'number'|'date',   # 归一化类型
 'widgetType': item['type'],               # 原始控件类型
 'options': item.get('options', {}),       # ⚠️ 必须：原始 options 含 remote/dictCode 等
 'fieldShow': True}                        # ⚠️ 必须：False 时被 allFields.filter() 过滤
```

**设计器表单 filterField 格式（包含系统字段，与 nameFields 格式相同但有额外字段）：**
```python
# ⚠️ filterField 必须包含 5 个系统公共字段（来自 constant.ts publicFields 常量）
# 前端 loadField() 第606-615行硬编码追加，和表单本身无关，所有设计器表单都要有
# Online 表单的 filterField 只有 {fieldName, fieldTxt, fieldType, widgetType, dictField}，无 options
PUBLIC_FIELDS_DESIGN = [
    {'fieldName': 'create_by',   'fieldTxt': '创建人',   'fieldType': 'select-user', 'widgetType': 'select-user', 'options': {},                                        'customDateType': '3'},
    {'fieldName': 'update_by',   'fieldTxt': '修改人',   'fieldType': 'select-user', 'widgetType': 'select-user', 'options': {},                                        'customDateType': '3'},
    {'fieldName': 'update_time', 'fieldTxt': '修改时间', 'fieldType': 'date',        'widgetType': 'date',        'options': {},                                        'customDateType': '3'},
    {'fieldName': 'create_time', 'fieldTxt': '创建时间', 'fieldType': 'date',        'widgetType': 'date',        'options': {},                                        'customDateType': '3'},
    {'fieldName': 'bpm_status',  'fieldTxt': '流程状态', 'fieldType': 'select',      'widgetType': 'select',      'options': {'remote': 'dict', 'dictCode': 'bpm_status'}, 'customDateType': '3'},
]
# filterField = [业务字段列表(含options+fieldShow)] + PUBLIC_FIELDS_DESIGN
```

### 存储过程快速路径（强制，2 轮完成）

**存储过程任务必须走 `proc_ops.py bindcomp`，禁止手动 pymysql + comp_ops.py 分步执行：**

```
轮次1: Read 凭据 + Bash: cp proc_ops.py comp_ops.py bi_utils.py default_configs.json（并行）
轮次2: py proc_ops.py bindcomp ... && rm proc_ops.py comp_ops.py bi_utils.py default_configs.json && echo URL | clip.exe
```

**示例：**
```bash
py proc_ops.py bindcomp "<api_base>" "$TOKEN" \
  --page "PAGE_ID" --comp "JCommonTable" --title "Demo数据表格" \
  --x 50 --y 280 --w 900 --h 450 \
  --proc-name "sp_query_demo" \
  --proc-sql "SELECT id, name, sex, age FROM demo ORDER BY create_time DESC" \
  --fields "id:String,name:String,sex:String,age:String" \
  --dict "sex=sex"
# 带参数：追加 --proc-params "IN p_sex varchar(10)" 并在 SQL 中引用 p_sex
```

`proc_ops.py bindcomp` 自动完成：获取 DB 连接 → pymysql 创建存储过程 → 验证 CALL → 创建数据集+绑定组件。

**执行方式**：直接在本 skill 的 `references/scripts/` 目录下运行，无需 cp。`bi_utils.py` 位于上级目录，脚本会自动找到。Claude 执行时根据当前平台构建完整路径（macOS/Linux 用 `python3`，Windows 用 `py`）。

### 多字段页面配置修改必须合并（强制）

修改 2 个及以上页面属性时，禁止逐个调用 page_ops.py，必须编写合并脚本（1 次 query + 修改所有字段 + 1 次 edit）。详见 `references/page-config-guide.md`。

### 所有大屏操作以耗时最少为第一优先级（强制）

直接执行；优先预置脚本；并行独立操作；复杂组件从 `default_configs.json` 加载；理想 2 轮；凭据已知时不重复读取。

**耗时目标：**

| 操作类型 | 目标耗时 | 做法 |
|---------|---------|------|
| 单组件增/删/改/查 | ≤30s | comp_ops.py 一条命令（cp + 执行 + rm，共 2 轮） |
| 数据集 + 单组件 | ≤45s | comp_ops.py --create-sql 或 dataset_ops.py + comp_ops.py --dataset-name |
| 复合操作（数据集 + 多组件） | ≤60s | 并行 Bash 调用 |
| SQL数据集 + 批量图表（同类型全部） | ≤30s | dataset_ops.py 内嵌于批量脚本，Write+cp 并行，共 3 轮（询问数据源→Write脚本+cp→py执行+rm） |
| 模板复制创建大屏 | ≤60s | template_ops.py copy --replace |
| 存储过程 + 单组件 | ≤45s | proc_ops.py bindcomp 一条命令（cp + 执行 + rm，共 2 轮） |
| 页面配置修改（≥2项） | ≤30s | 合并脚本一次完成 |
| 全组件批量生成（99个） | ≤5s | **预置脚本 `gen_all_comps.py`**，无需 Write 脚本。严格 2 轮：轮次1 Read凭据（已知时跳过），轮次2 `cp 3个文件 && ls && py gen_all_comps.py API TOKEN && rm`（一条命令） |
| 多图表+联动（≥2图+联动） | ≤10s | **预置脚本 `multi_chart_linkage.py`**：1次query + N并发dataset + 内存add+linkage + 1次save。禁止逐个调 comp_ops.py（17次API≈35s）。严格 2 轮：轮次1 cp 3个文件，轮次2 py执行+rm |

### 全组件批量生成快速路径（强制）

**用户要求"生成全组件大屏"时，直接调用预置脚本 `gen_all_comps.py`，禁止每次重新 Write 脚本。**

**预置脚本方式（最优，严格 2 轮）：**

```
凭据已知时：仅1轮
轮次1: cp 3个文件 && ls验证 && py gen_all_comps.py API_BASE TOKEN [页面名] && rm（一条命令）
凭据未知时：2轮
轮次1: Read 凭据
轮次2: cp 3个文件 && ls验证 && py gen_all_comps.py API_BASE TOKEN [页面名] && rm（一条命令）
```

**完整命令**：直接在本 skill 的 `references/scripts/` 目录下运行，Claude 根据平台自动构建路径和 Python 命令：
```
python gen_all_comps.py "<api_base>" "TOKEN值" "全组件大屏"
```

> 脚本已内置 subprocess clip，URL 自动复制到剪贴板，无需外部 `| clip.exe`

**脚本特性：**
- 99 个业务组件（排除 JDragBorder/JDragDecoration/JWeatherForecast）
- 4 列网格布局（440×300，间距 20px），自动计算页面高度（约 8150px）
- 全静态演示数据（从 default_configs.json 加载），无需数据集；传 `--ds-id` 时绑定指定数据集
- 接受命令行参数（2026-04-09 更新，**禁止再 Read 源文件**）：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `API_BASE` | API地址（必填） | — |
| `TOKEN` | Token（必填） | — |
| `[页面名]` | 新建页面时用的名称 | `全组件大屏` |
| `--page-id PAGE_ID` | 使用已有页面（跳过创建，组件追加在已有组件下方） | 新建页面 |
| `--ds-id DS_ID` | 绑定数据集ID（所有可绑定组件均绑此集） | 不绑定 |
| `--ds-type TYPE` | 数据集类型（api/FILES/singleFile） | `api` |
| `--ds-name NAME` | 数据集名称（显示用） | 从数据集自动取 |
| `--ds-fields FIELDS` | 字段列表，格式 `f1:T1,f2:T2`（如 `name:String,type:String,sales:Integer`） | 从数据集自动查 |

**FILES + 已有页面全组件标准命令（3轮完成）：**
```bash
# <skill_base_dir> = skill 加载时显示的 Base directory for this skill（Windows 路径，Git Bash 下需转为 /c/Users/... 格式）
# 轮次1: 分析Excel列名（openpyxl）+ Read凭据
# 轮次2: cp 4个文件 + ls验证 + 创建数据集（--no-chart）+ 生成全组件 + rm
cp "<skill_base_dir>/references/scripts/files_ops.py" . && \
cp "<skill_base_dir>/references/scripts/gen_all_comps.py" . && \
cp "<skill_base_dir>/references/bi_utils.py" . && \
cp "<skill_base_dir>/references/scripts/default_configs.json" . && \
ls files_ops.py gen_all_comps.py bi_utils.py default_configs.json && \
PYTHONIOENCODING=utf-8 py files_ops.py create-bind API_BASE TOKEN PAGE_ID \
    --files file1.xlsx file2.xlsx --join-on 关联列 --group-by 字段1,字段2 --agg 聚合列 \
    --col-name name --col-type type --col-sales sales --no-chart 2>&1 | tee /tmp/fo.txt && \
DS_ID=$(PYTHONIOENCODING=utf-8 py -c "import re,sys; m=re.search(r'数据集已创建: (\S+)', open('/tmp/fo.txt').read()); print(m.group(1) if m else sys.exit(1))") && \
echo "DS_ID=$DS_ID" && \
PYTHONIOENCODING=utf-8 py gen_all_comps.py API_BASE TOKEN "页面名" \
    --page-id PAGE_ID --ds-id "$DS_ID" --ds-type FILES \
    --ds-name "数据集名称" --ds-fields "name:String,type:String,sales:Integer" && \
rm files_ops.py gen_all_comps.py bi_utils.py default_configs.json
```

**字段映射规则（自动推断，无需手动指定）：**
- `str_fields[0]`（第1个字符串字段）→ 单系列维度 / 表格名称 / 起点名称
- `str_fields[-1]`（最后一个字符串字段）→ 多系列分组 / 终点名称（与 files_ops.py 的 col_type 一致）
- `num_fields[0]`（第1个数字字段）→ 数值

**核心原则（仅自定义修改脚本时参考）：**
1. 必须用 `bi_utils.add_component()` — 自动处理 config 结构（flat dict → JSON string）、size/chart/turnConfig 等字段
2. `_page_components[page_id] = []` 清空缓存 → 批量 add_component → queryById+edit 合并保存
3. `chartData` 在传入前序列化为 JSON 字符串
4. `option.title` 可能是 str 类型，需检查后再赋值
5. `desJson.height` 存页面高度（不是 pageConfig），创建后必须同步更新

**关键代码结构（gen_all_comps.py 已封装，自定义时参考）：**
```python
# SLOT_CONFIGS: 每种 compType 的槽位标签（严禁自行创建不存在的标签）
# 单系列: ['维度','数值']；多系列: ['分组','维度','数值']；仪表盘: ['总计','已用']
# 表格: ['名称','数值']；飞线: ['起点名称','终点名称']；卡片: ['内容']
# 详细映射见下方 SLOT_CONFIGS 表

# UI-only 不绑数据集
NO_BIND = {'JImg','JCarousel','JCustomIcon','JText','JCurrentTime','JIframe',
           'JDragEditor','JRadioButton','JForm','JPermanentCalendar','JSelectRadio',
           'JTabToggle','JCommon','JVideoPlay','JVideoJs'}

# 批量添加后保存（禁止 save_page，必须 queryById+edit 合并保存 template+desJson）
raw = bi_utils._request('GET', '/drag/page/queryById', params={'id': page_id})
p = raw.get('result') or {}
des = json.loads(p['desJson']) if isinstance(p.get('desJson'), str) else (p.get('desJson') or {})
des['height'] = total_height
bi_utils._request('POST', '/drag/page/edit', data={
    'id': page_id, 'name': p.get('name',''),
    'template': json.dumps(bi_utils._page_components[page_id], ensure_ascii=False),
    'updateCount': p.get('updateCount', 1), 'style': p.get('style','bigScreen'),
    'theme': p.get('theme','dark'), 'backgroundImage': p.get('backgroundImage',''),
    'designType': p.get('designType',100), 'desJson': json.dumps(des, ensure_ascii=False),
})
```

**⚠️ 严禁在批量场景下自行构造 comp dict 并 insert 到 template**（必须用 `bi_utils.add_component()` 处理结构转换）

**反模式检查清单（关键禁止项）：**

**效率违规：**
- cp 放在轮次1 而非与 py 同一命令链（轮次2）
- cp 目标路径用 `C:/Users/` 格式（Git Bash 静默失败，必须用 `/c/Users/...` Unix 格式）
- cp 依赖文件和 Write 脚本串行执行（必须同轮并行）
- Bash 中用 shell 变量传参给 py 脚本（变量可能为空，必须内联字面值）
- 写自定义脚本用 bash heredoc（含单引号必报错，必须用 Write 工具）
- 脚本中用拼音替代中文字段名/组件名（显示乱码，必须直接写 Unicode）
- 执行 py 不加 `PYTHONIOENCODING=utf-8`（Windows GBK 中文必报错）
- `comp_ops.py` 子命令写在 API_BASE 后面（正确：子命令在最前）
- Python subprocess 用 `/c/Users/...` 路径（Windows 下无效，提前 cp 到当前目录）
- 多图表+联动场景逐个调 comp_ops.py（应用 multi_chart_linkage.py，节省80%）
- 全组件批量生成超过 2 轮（凭据已知 1 轮：cp+py+rm）
- 生成全组件大屏 Write 脚本（直接 cp gen_all_comps.py 执行）
- 询问数据源后才开始 Write 批量脚本（应在用户确认后同轮并行 Write+cp）
- SQL数据集创建单独一轮，批量图表再一轮（内嵌到批量脚本里）
- save_page() 后再 queryById+edit 更新高度（合并为1次edit，共3次API）
- Read 大型Controller文件直接全文（先 Grep 定位结构，再针对性 Read）
- 凭据已知时 Read 凭据文件（凭据在 MEMORY.md 上下文中）
- 使用预置脚本时读取 dataset-guide.md（已封装，无需读）
- 执行预置脚本前 --help 查看用法

**逻辑违规：**
- 🚨 singleFile 全流程脚本 add_component 前漏写 `query_page + 缓存 _page_components`（清空大屏所有组件）
- 🚨 地图组件手工构造 option/commonOption（必须从 default_configs.json 深拷贝）
- 🚨 地图 chartData 格式跨组件套用（各组件格式完全不同，详见 map-guide.md）
- 🚨 设计器表单端点盲猜（固定端点：`/desform/api/list/options`、`/desform/api/fields/{tableName}`）
- 🚨 Online表单全组件场景漏写 `dataType=4`（默认 dataType=0 静态数据，完全不读表单）
- 🚨 批量生成时用 compType 英文代码作 componentName（必须用中文名）
- singleFile 场景用 `comp_ops.py --dataset-name` 绑定（按索引映射导致字段错乱）
- singleFile 上传后用 `result.tableName` 提取表名（无此字段，从 `result.dbUrl` 的 `name` 取）
- singleFile `code` 字段去掉 `jmf.` 前缀（系统拼 SQL 时报错）
- singleFile 文件上传用 `bi_utils._request()`（不支持 files 参数，必须用 requests.post）
- 直接调用 bi_utils.add_xxx() + save_page() 添加组件（覆盖已有组件，必须用 comp_ops.py add）
- 批量生成 95 个组件逐个调 comp_ops.py（190 次 API vs 2 次，差 95 倍）
- 全局统一 dataMapping（每个组件必须用自己的 SLOT_CONFIGS[comp_type]）
- 批量绑定时用 `GET /drag/view/getAllChartData`（result 格式不同报 None 错误）
- 批量绑定时 `dataMapping.filed` 写字段名（filed 是槽位标签，mapping 才是字段名）
- 创建自定义API/Mock数据集后调 queryFieldByApi（字段已知直接传 datasetItemList）
- 全组件生成时为分类生成 JText 标题组件
- 全组件生成时包含 JDragBorder/JDragDecoration/JWeatherForecast
- Online表单全组件场景读取 online-design-form-chart-guide.md（已内联）
- YApi批量：Write脚本后看 yapi list 结果再 Edit（yapi复用逻辑必须内嵌到脚本，按路径完整匹配）
- 🚨 API_BASE 未知时用 curl 探测路径（直接询问用户）
- 用户已给出 API 地址时先探测已有数据集（直接 create-api → add）
- 创建 SQL 数据集时跳过询问数据源
- dataset_ops.py create-api 漏 --code 参数（必填4项：--name/--code/--url/--fields）
- 缺少 fieldOption（前端字段选项面板为空）
- 缺少 dataSetName/dataSetType/dataSetApi/dataSetMethod/dataSetIzAgent/paramOption/viewLoading

## 交互流程

### Step 0: 解析用户需求

| 信息 | 默认值 |
|------|--------|
| 页面名称 | 用户指定 |
| 主题 | dark |
| 背景图 | `/img/bg/bg4.png` |
| 组件列表 | 从描述中解析 |

### Step 0.1: 数据来源确认（强制，用户未明确指定时必须询问）

**触发条件：** 用户没有明确说明数据来自哪里（没有给出接口地址、没有指定数据集、没有说用 SQL/mock/自己写代码），则**必须先问用户以下两个问题，不得擅自假设或跳过**：

> **问题一：接口来源**
> 使用 **mock 系统** 还是 **自己编写代码**？
> - **mock 系统**：请提供 mock 服务地址 + 账号密码（如 YApi：`https://xxx.com/login`）
> - **自己编写代码**：请提供代码存放路径（Java Controller 文件全路径）
>
> **问题二：接口需要实现什么业务需求？**
> 描述各组件要展示的数据内容（参考大屏中的静态数据格式设计接口）

**跳过询问：** 用户已给出 mock 地址/接口路径/数据集名/数据源，或任务不涉及数据集创建。

### Step 0.5: 模板匹配（优先使用模板布局）

**生成整个大屏时，必须先匹配模板，复用已有布局。**

**模板目录**：`references/templates/bigScreen/`（10 个经典大屏模板 JSON）

**模板名→文件名索引（直接使用，禁止 Glob 搜索）：**

| 模板名称 | 文件名 |
|---------|--------|
| 乡村振兴普惠金融服务平台 | `乡村振兴普惠金融服务平台_1024608431274250240.json` |
| 北京市污水排放总量 | `北京市污水排放总量_1022392593179791360.json` |
| 北京科技数字化云平台 | `北京科技数字化云平台_1014376428645961728.json` |
| 医院实时数据监控 | `医院实时数据监控_1011800681234354176.json` |
| 旅游数据分析中心大屏 | `旅游数据分析中心大屏_1016994272231608320.json` |
| 杭州房地产市场宏观监控 | `杭州房地产市场宏观监控_1024545852833189888.json` |
| 警务监控系统 | `警务监控系统_1024545264544305152.json` |
| 车辆分布图 | `车辆分布图_1017325669831987200.json` |
| 集团综合数据大屏 | `集团综合数据大屏_1151069555267260416.json` |
| 香山公园客流大数据 | `香山公园客流大数据_1027085484978388992.json` |

| 用户需求关键词 | 推荐模板 |
|---------------|---------|
| 销售/订单/交易/通用/综合/驾驶舱 | 集团综合数据大屏 |
| 医院/医疗/医药/机构/校园/人员管理 | 医院实时数据监控 |
| 监控/安防/警务 | 警务监控系统 |
| 旅游/公园/客流 | 旅游数据分析中心大屏、香山公园客流大数据 |
| 房地产/城市/环境 | 杭州房地产市场宏观监控、北京市污水排放总量 |
| 科技/数字化/IoT/能源/电力/风电/光伏 | 北京科技数字化云平台 |
| 金融/银行/乡村 | 乡村振兴普惠金融服务平台 |
| 车辆/交通/地图 | 车辆分布图 |

**模板选择优先级（强制，按顺序匹配）：**

1. **精确匹配** → 从上方关键词表找到直接对应的模板，使用「模板复制方式」创建大屏，保留布局和装饰，仅替换业务数据和标题文字
2. **备选三模板** → 没有精确匹配时，从以下三个模板中选最合适的：
   - `北京科技数字化云平台`（科技/工业/设备/IoT/能源类）
   - `北京市污水排放总量`（环境/城市/数据监测类）
   - `医院实时数据监控`（机构/人员/综合管理类）
3. **兜底模板** → 以上都不合适时，才选择 `集团综合数据大屏`

模板复制的详细流程（ID 映射、JTabToggle/JGroup 引用更新、边界检查等）见 `references/template-copy-guide.md`。

> **重要**：只有在用户明确要求"不使用模板"或"从零创建"时，才跳过模板匹配，直接使用 bi_utils 默认组件函数逐个添加。

### Step 1: 识别组件并选择类型

> 用户说组件名时直接查上方「图表查询与推荐」章节的表格获取 compType，**禁止 Grep 搜索源码**。所有组件均用 `comp_ops.py add --comp <compType>` 添加，变体组件加数字后缀（如 JStatsSummary_1/2/3、JScrollList_1/2/3、JCardScroll_1/2/3）。

**特殊组件：**

| 组件 | compType | 说明 |
|------|---------|------|
| 选项卡 | `JSelectRadio` | 需自定义脚本配置 `compShowConfig`（见下方专节） |
| 天气预报 | `JWeatherForecast` | 需自定义脚本，template=11/34/21/12/27/94 |
| 区域地图 | `JAreaMap` | 读 `references/map-guide.md` |

### JWeatherForecast 天气预报组件（特殊组件，需自定义脚本）

> **comp_ops.py 不支持 JWeatherForecast**，必须用自定义脚本直接操作 template 数组添加。
> **dataType 必须为 1**（自动获取天气数据），不是 0。chartData 为 `"[]"`。

| 版本 | template 值 | 默认尺寸 (w×h) | fontColor | bgColor |
|------|------------|----------------|-----------|---------|
| 滚动版 | 11 | 311×47 | #fff | #ffffff00 |
| 横线版 | 34 | 300×30 | #fff | #ffffff00 |
| 带背景 | 21 | 415×131 | #000 | #ffffff00 |
| 好123版 | 12 | 318×61 | #fff | #ffffff00 |
| 温度计版 | 27 | 400×266 | #fff | #ffffff |
| 列表文字版 | 94 | 257×47 | #fff | #ffffff00 |

完整脚本见 `references/weather-forecast-guide.md`

### JSelectRadio 选项卡组件（需自定义脚本实现组件关联）

> **选项卡的核心功能是「组件可见性控制」**：点击不同选项卡，显示/隐藏关联的组件。
> comp_ops.py 可以添加基础选项卡，但**无法配置 `compShowConfig`（组件关联）**，需自定义脚本。
> 参考文档：https://help.jimureport.com/biScreen/componentconfig/other/tab/

**两种显示风格**：选项卡样式（默认）、下拉菜单样式

**chartData 格式**（定义选项卡标签）：
```json
[
  {"label": "折线图", "value": "1"},
  {"label": "柱形图", "value": "2"}
]
```

**核心配置：`config.compShowConfig`**（控制组件显示/隐藏）：
```json
[
  {"selectVal": "1", "compVals": ["目标组件ID_1"]},
  {"selectVal": "2", "compVals": ["目标组件ID_2", "目标组件ID_3"]}
]
```

| 字段 | 说明 |
|------|------|
| `selectVal` | 对应 chartData 中某项的 `value` |
| `compVals` | 组件 ID 数组（`comp['i']`），选中该选项时这些组件显示，其余隐藏 |

**显隐逻辑（源码 `SelectRadio.vue`）**：
- 遍历 `compShowConfig`，对每条规则中 `compVals` 引用的组件设置 `visible = (selectVal == 当前选中值)`
- 支持组合组件（JGroup）内部的子组件查找
- 每个选项可关联**多个组件**同时显示

**option 常用配置路径：**

| 说明 | 配置路径 | 示例值 |
|------|---------|--------|
| 类型（选项卡/下拉） | `option.type` | `radio` / `select` |
| 字体颜色（未选中） | `option.fontColor` | `#ffffff` |
| 字体大小 | `option.fontSize` | `14` |
| 选项卡间距 | `option.tabGap` | `10` |
| 未选中背景色 | `option.bgColor` | `#FFFFFF00` |
| 未选中边框颜色 | `option.borderColor` | `#0f66ff` |
| 未选中边框宽度 | `option.borderWidth` | `1` |
| 选中文字颜色 | `option.activeFontColor` | `#ffffff` |
| 选中背景色 | `option.activeBgColor` | `#0f66ff` |
| 选中边框颜色 | `option.activeBorderColor` | `#0f66ff` |
| 背景图片（未选中） | `option.bgImgUrl` | URL |
| 背景图片（选中） | `option.activeBgImgUrl` | URL |

完整脚本见 `references/select-radio-guide.md`（新增关联组件 + 为已有组件添加关联两种场景）

**⚠️ 易错点：**

| 错误 | 正确做法 |
|------|---------|
| `compShowConfig` 放在 `option` 内 | `compShowConfig` 与 `option` 同级，在 `config` 顶层 |
| `compVals` 用组件名称 | `compVals` 必须用组件 `i` 字段（UUID），不是 `componentName` |
| 关联组件和选项卡位置不重叠 | 被关联组件应放在**相同坐标区域**（x/y/w/h 一致），由选项卡控制显隐切换 |
| 忘记设置 config 为 JSON 字符串 | `config` 必须是 `json.dumps()` 后的字符串 |
| `size` 字段为空 `{}` | config 内部和顶层都必须设置 `size: {width, height}`，否则组件初始不渲染（需手动拖拽才显示）。同理 `chart`/`turnConfig`/`linkageConfig` 也要设置 |

### Step 2: 展示设计摘要并确认

**跳过确认：** 用户说「直接生成」/「不用确认」，或模板精确匹配，或同会话中已确认过。

### 快捷操作：comp_ops.py（增删改查）

> **⚠️ 添加/编辑/删除组件必须使用 comp_ops.py，严禁直接调用 bi_utils.add_xxx() + save_page()。**
> 原因：bi_utils.add_component() 内部将 `_page_components[page_id]` 初始化为空列表，save_page 时会用空列表覆盖页面已有的全部组件，造成不可恢复的数据丢失。comp_ops.py 会先加载已有模板再操作，安全无损。

**脚本位置**：`<skill_base_dir>/references/scripts/comp_ops.py`

**执行方式**：直接在本 skill 的 `references/scripts/` 目录下运行，无需 cp。`bi_utils.py` 位于上级目录，脚本会自动找到。Claude 执行时根据当前平台构建完整路径（macOS/Linux 用 `python3`，Windows 用 `py`）。

**核心命令：**
```bash
# 查看组件
py comp_ops.py list $API_BASE $TOKEN $PAGE_ID

# 删除组件
py comp_ops.py delete $API_BASE $TOKEN $PAGE_ID --name "组件名"

# 编辑组件属性（单属性）
py comp_ops.py edit $API_BASE $TOKEN $PAGE_ID --name "组件名" --set "option.title.text=新标题"

# 编辑组件属性（多属性：每个属性一个 --set）
py comp_ops.py edit $API_BASE $TOKEN $PAGE_ID --name "胶囊图" --set "option.showValue=true" --set "option.unit=333"

# 添加组件（静态数据）
py comp_ops.py add $API_BASE $TOKEN $PAGE_ID --comp "JBar" --title "柱形图" --x 50 --y 500 --w 450 --h 300

# 一键：创建SQL数据集 + 字典翻译 + 添加图表
py comp_ops.py add $API_BASE $TOKEN $PAGE_ID --comp "JPie" --title "男女比例" --x 735 --y 365 --w 450 --h 350 --create-sql "SELECT sex as name, COUNT(*) AS value FROM demo WHERE sex IS NOT NULL GROUP BY sex" --ds-name "男女比例统计" --fields "name:String,value:String" --dict "name=sex"

# 移动/缩放组件
py comp_ops.py move $API_BASE $TOKEN $PAGE_ID --name "组件名" --x 100 --y 200
```

**⚠️ 数据集默认规则（强制）：用户添加图表时未指明数据集，必须使用静态数据（无额外参数），禁止自动绑定或创建数据集。**

**⚠️ 标题默认隐藏（强制）：添加图表时，`option.title.show` 必须设为 `false`，禁止默认展示标题。**

**四种数据模式：**

| 模式 | 参数 | 说明 |
|------|------|------|
| 静态数据（默认） | 无额外参数 | 从 `default_configs.json` 加载默认配置 |
| 绑定已有数据集 | `--dataset-name "名称"` | 内置自动查询数据集、设 dataType=2，**无需单独调 dataset_ops.py 查询** |
| 一键创建SQL+绑定 | `--create-sql "SQL"` | 创建数据集+绑定+字典，支持 `--dict`、`--fields` |
| 带查询参数的SQL | `--create-sql` + `--sql-params` | `comp_ops.py add --sql-file sql.txt --sql-params "age:年龄::"` 或自定义 Python 脚本 |

**⚠️ 带 FreeMarker 动态参数的 SQL 必须用 `--sql-file`，禁止通过 bash 命令行传递。** 原因：`${age}` 会被 shell 解释为变量（值为空），`<#if>` 中的 `>` 会被解释为重定向，导致 SQL 被截断或参数丢失。

**动态SQL查询参数完整示例（强制规范）：**

```bash
# Step 1: 将含 FreeMarker 语法的 SQL 写入文件
cat > sql.txt << 'SQLEOF'
SELECT sex as name, COUNT(*) AS value FROM demo WHERE sex IS NOT NULL
<#if isNotEmpty(age)>
  AND age = '${age}'
</#if>
GROUP BY sex
SQLEOF

# Step 2: 用 --sql-file + --sql-params 创建
py comp_ops.py add $API_BASE $TOKEN $PAGE_ID \
  --comp "JPie" --title "男女比例" --x 735 --y 365 --w 450 --h 350 \
  --sql-file sql.txt --ds-name "男女比例统计" \
  --fields "name:String,value:String" --dict "name=sex" \
  --sql-params "age:年龄::"

# Step 3: 清理
rm sql.txt
```

**FreeMarker 动态条件语法规则（强制）：**

| 规则 | 正确写法 | 错误写法 |
|------|---------|---------|
| 参数判空 | `<#if isNotEmpty(age)>` | ~~`<#if age?? && age?length gt 0>`~~ |
| 参数占位 | `'${age}'` | ~~`#{age}`~~（`#{}` 是系统变量专用） |
| 条件结束 | `</#if>` | - |
| 系统变量 | `#{sys_user_code}` | ~~`${sys_user_code}`~~（`${}` 和 `#{}` 不可混用） |

**`--sql-params` 格式**：`paramName:paramTxt:defaultValue:dictCode`（后三项可省略，多个逗号分隔）

| 示例 | 说明 |
|------|------|
| `"age:年龄::"` | 年龄参数，无默认值，无字典 |
| `"sex:性别:1:sex"` | 性别参数，默认值 1，字典编码 sex |
| `"age:年龄::,sex:性别:1:sex"` | 多参数逗号分隔 |

**SQL 含 `!=` 等特殊字符时**：同样禁止通过 bash 传递，必须用 `--sql-file` 或写 Python 脚本在内部定义 SQL。

## 🚨 组件编写核心原则（等同于人在界面操作，强制）

> **组件的创建、数据、配置三件事必须按以下方式处理，禁止凭感觉和想象构造任何字段。**

### 原则一：创建组件 = 使用默认配置（先拷贝后定制）

人在界面拖出一个组件，得到的是系统默认配置。脚本中等价操作是：
```python
d = copy.deepcopy(defaults[compType])   # 相当于从面板拖出
```
**禁止跳过这一步直接手写 option dict。**

### 原则二：动态数据格式必须与静态数据格式一致

`default_configs.json` 中的 `chartData` 就是该组件的静态数据格式。动态数据（API/SQL 返回的数据）必须与这个格式完全一致，否则组件无法渲染：
```python
# 先看 defaults 里的静态格式
# JBreakRing: [{"value": 1048, "name": "oppo"}, ...]
# 动态数据也必须返回同样的字段名和结构
```

### 原则三：修改配置必须先查该组件支持的字段

不能凭感觉猜测字段名。修改任何组件的 option 字段前，必须先找到该组件的配置文档，按以下优先级查找：

1. **有独立配置文档的组件** → 查对应的 `references/*-option-config.md`（按需加载，上方「按需加载指南」表格中列出）
   - 例：JBreakRing → `references/break-ring-option-config.md`
   - 例：JStatsSummary → `references/stats-summary-option-config.md`
   - 例：JScrollList → `references/scroll-list-option-config.md`
   - 例：JTabToggle → `references/tab-toggle-option-config.md` 等
2. **无独立文档的组件** → 查 `references/bi-comp-option-config.md`（通用配置速查）
3. **以上都没有** → 在界面操作该配置项，再用 `comp_ops.py list` 查看实际存储的字段名，或直接读组件的 `*Option.vue` 源文件确认

**禁止**：在不知道字段名的情况下凭感觉构造 option，这是导致配置无效或组件不显示的根本原因。

**自定义脚本添加图表的强制规则：**
1. **🚨 图表 config 必须先从 `default_configs.json` 深拷贝，再进行定制（强制两步顺序，不可颠倒）**：
   ```python
   # 第一步：深拷贝完整默认配置（option/chartData/dataMapping 全部来自此处）
   d = copy.deepcopy(defaults['JBreakRing'])
   opt = d['option']
   # 第二步：在默认结构基础上覆盖需要定制的字段
   opt['customColor'] = [...]
   opt['title']['show'] = False
   cfg['option'] = opt
   cfg['dataMapping'] = d['dataMapping']
   ```
   **严禁跳过第一步直接手写 option dict**（手写必然遗漏 series/tooltip/grid 等渲染必需字段，导致组件空白或报错）。`default_configs.json` 中存有所有组件的完整默认结构，必须以它为基础进行修改，而不是从零构建。
2. **字典翻译用 jimu_dict**：`/jmreport/dict/*` API，不是 `/sys/dict/*`（系统字典需签名且表不同）
3. **dictOptions 从 `getAllChartData` 获取**：创建数据集后调 `getAllChartData`，将返回的 `dictOptions` 写入组件 config，禁止手动构建
4. **datasetItemList 中绑定 dictCode**：如 `{'fieldName': 'name', ..., 'dictCode': 'sex'}` 实现字段级字典翻译

### 全部预置脚本一览

脚本目录：`<skill_base_dir>\references\scripts\`（`<skill_base_dir>` 为 skill 加载时显示的 `Base directory for this skill` 路径）

| 脚本 | 功能 | 常用命令 |
|------|------|---------|
| `yapi_ops.py` | YApi Mock 接口管理（固定 claude AI 项目） | `create-mock`（**必填 `--title`，不是 `--name`**；`--template single/multi/pie/gauge/table/bar_multi` 或 `--body JSON`），`list`，`delete`，`update`。Mock URL 自动含 basepath `/claude`。**⚠️ 创建前必须先 `list` 查看已有接口，已存在同类接口时直接复用** |
| `comp_ops.py` | 组件增删改查 | `list`, `delete`, `edit`, `add`, `move` |
| `page_ops.py` | 页面配置 | `info`, `set-bg`, `set-bgimg`, `set-theme`, `watermark`, `rename`, `delete`。**rename 参数格式：** `py page_ops.py rename API_BASE TOKEN PAGE_ID --name "新名称"`（`--name` 是命名参数，不是位置参数）。**delete 用法：** `py page_ops.py delete API_BASE TOKEN PAGE_ID` |
| `dataset_ops.py` | 数据集管理 | `list`, `create-sql`, `create-api`, `edit`, `test`, `delete`, `bind` |
| `template_ops.py` | 模板操作 | `list`, `preview`, `search`, `copy` |
| `linkage_ops.py` | 联动/钻取 | `show`, `add-linkage`, `remove-linkage`, `add-drill` |
| `link_ops.py` | 外部链接跳转 | `show`, `set`, `remove` |
| `map_ops.py` | 地图数据 | `list`, `check`, `upload`, `add-map` |
| `style_ops.py` | 批量样式 | `show-colors`, `set-title-color`, `set-palette`, `batch-edit` |
| `backup_ops.py` | 备份恢复 | `export`, `import`, `clone`, `diff` |
| `datasource_ops.py` | 数据源管理（JDBC + NoSQL） | `list`, `detail`, `create`, `edit`, `test`, `delete`, `parse-sql`。**create 参数：** `--db`（非 --db-name）、`--user`（非 --username）；**test 支持 `--id` 或 `--name`**（按名称自动查找后测试）。**edit 参数：** `--name 数据源名称`（或 `--id`）定位，`--add-jdbc-param "key=value"` 追加/替换 JDBC 参数（如 `trustServerCertificate=true`），`--set-url` 替换完整 URL，`--user`/`--password` 修改凭据。**SQLSERVER create 已自动包含 `trustServerCertificate=true`**，旧数据源用 `edit --add-jdbc-param` 修复。**支持 NoSQL：** `--db-type mongodb/redis/es`，自动生成 `host:port/db` 格式的 dbUrl（不带协议前缀），dbDriver 自动置空。**NoSQL 数据集 SQL 语法：** MongoDB 表名加 `mongo.` 前缀（`select * from mongo.表名`），ES 加 `es.` 前缀。**API 接口（需签名）：** `GET /drag/onlDragDataSource/getOptions`（list，返回 `[{value:id,label:name,text:name}]`）、`GET /drag/onlDragDataSource/queryById`、`POST /drag/onlDragDataSource/add`、`POST /drag/onlDragDataSource/edit`（传完整对象）、`POST /drag/onlDragDataSource/testConnection`、`DELETE /drag/onlDragDataSource/delete` |
| `group_ops.py` | 组合管理 | `list`, `create`, `ungroup` |
| `dict_ops.py` | 字典管理 | `list`, `create`, `items`, `bind` |
| `files_ops.py` | 多文件数据集（FILES）| `create-bind`（建数据集+上传+推断SQL+加图表），`upload`，`list-tables`，`add-chart` |
| `proc_ops.py` | 存储过程管理 | `create`, `list`, `drop`, `bindcomp`（一键：创建存储过程+数据集+组件）。**前置条件：`py -m pip install pymysql`**，通过 pymysql 直连数据库执行 DDL |
| `multi_chart_linkage.py` | **多图表+联动批量生成**（单脚本，1次save） | `py multi_chart_linkage.py API TOKEN PAGE --db-source DS_ID [--config my.json]`。内置 demo 配置（jeecgbootsy统计库+demo表）。比逐个 comp_ops.py 节省约80%耗时 |
| `files_ops.py` | 多文件数据集（FILES）管理 | `create-bind`（一键：建数据集+上传文件+自动推断JOIN SQL+添加图表），`upload`（仅上传），`list-tables`（查表名），`add-chart`（单独绑图表）。**见下方「快捷操作：files_ops.py」章节**。`create-bind` JOIN 模式必须传 `--group-by <列名1,列名2> --join-on <关联列> --agg <聚合列>`；不传则脚本走 fallback 分支报 `UnboundLocalError`。**列名未知时先问用户，不要盲目执行** |

**通用使用流程**：直接在本 skill 的 `references/scripts/` 目录下运行，无需 cp。`bi_utils.py` 位于上级目录，脚本自动找到。Claude 执行时根据平台构建完整路径（macOS/Linux 用 `python3`，Windows 用 `py`）。

### Step 3: 调用 API 创建大屏

**方式一（最优）：** `template_ops.py copy`（cp+执行+rm，2轮）
**方式二（复杂）：** 自定义脚本，详见 `references/template-copy-guide.md`

## 大屏标题规则

- `option.card.title` 必须为空字符串（避免双重标题）
- 页面主标题用 `add_text()`，fontSize≥40，fontWeight='bold'，letterSpacing=5

## 组件字段映射机制三分类（必读，2026-04-21 实测）

> **判断规则**：绑定数据集前先查 `default_configs.json` 对应组件，根据有无 `dataMapping` 字段 + `option` 内容，确定属于哪类。

### 第一类：`dataMapping` 槽位机制（标准图表 + 部分列表）

`config.dataMapping` 是数组，每项 `{"filed":"槽位标签","mapping":"字段名"}`。槽位标签来自 `default_configs.json`，**禁止自行命名**。

| 组件 | 槽位标签（filed） |
|------|-----------------|
| JBar/JLine/JPie 等大多数图表 | 维度 / 数值 |
| 多系列图表（JStackBar/JMultipleBar 等） | 分组 / 维度 / 数值 |
| JList（数据列表） | 标题 / 描述 / 时间 / 封面 |
| JBreakRing（多色环形图） | 维度 / 数值 |
| JSemiGauge（半圆仪表盘） | 总计 / 已用（同时有 `option.titleMapping`/`option.valueMapping` 存实际字段名） |
| JOrbitRing（轨道环形文字） | 标题 / id(唯一标识) / 图片地址 |
| **JTabToggle（导航切换）** | 文本 / 数值 — ⚠️ **仅支持静态数据，禁止绑定数据集** |

### 第二类：`option` 内嵌字段映射（无 `dataMapping`）

这些组件**没有** `dataMapping`，字段映射配置在 `option` 内部专属字段：

| 组件 | option 字段映射路径 | 映射结构 |
|------|-------------------|---------|
| JPermanentCalendar（日历） | `option.field.dateField` / `option.field.valueField` | 字符串，填数据字段名 |
| JStatsSummary（统计概览 1/2/3） | `option.fieldMap` | dict：`{label:"name字段", value:"value字段", unit:"suffix字段", ...}` |
| JListProgress（列表进度图） | `option.beginFields[].key`、`option.centerTopFields[].key`、`option.endFields[].key` | 数组，每区域字段对象，`key` 指向数据字段名，`name` 为显示标签 |
| JScrollList（滚动列表 1/2/3） | `option.fieldMapping[].key` | 数组，每列一个对象，`key` 为数据字段名，`name` 为列标题 |
| JCardScroll（卡片滚动 1/2/3） | `option.contentFieldMapping[].key` | 数组，每项含 `key` 指向数据字段名 |

### 第三类：直接格式消费（无任何显式字段映射）

没有 `dataMapping` 也没有 `option` 级字段映射，数据格式由组件固定消费：

| 组件 | chartData 格式 | 说明 |
|------|---------------|------|
| JCommonTable（数据表格） | `[{"field1":"v","field2":"v",...}]` | 列由 `datasetItemList` 字段列表直接渲染，字段名即列名 |
| JScrollBoard（轮播表） | `[["行1列1","行1列2",...],...]` | 二维数组，列标题单独配置在 `option.header` |
| JGaoDeMap（高德地图） | `[{"name":"城市","value":[lng,lat,val]}]` | 固定地理坐标格式 |

---

## 常用组件配置路径速查（内联）

> 以下组件的 option 路径已内联，修改时**直接使用，无需读取 `bi-comp-option-config.md`**。

### JStatsSummary（统计概览）

| 说明 | 配置路径 | 示例值 |
|------|---------|--------|
| 卡片最小宽度 | `option.card.minWidth` | 250 |
| 卡片圆角 | `option.card.borderRadius` | 16 |
| 卡片边框宽度 | `option.card.borderWidth` | 1 |
| 卡片边框颜色 | `option.card.borderColor` | #0f66ff59 |
| 卡片阴影 | `option.card.shadow` | 0 16px 48px #0b76ff59 |
| 卡片模糊度 | `option.card.blur` | 24 |
| 卡片内边距(垂直) | `option.card.padding.vertical` | 24 |
| 卡片内边距(水平) | `option.card.padding.horizontal` | 24 |
| 卡片填充类型 | `option.card.fill.type` | none/color/gradient/image |
| 卡片填充颜色 | `option.card.fill.color` | #0b2b63 |
| 卡片填充渐变启用 | `option.card.fill.gradient.enabled` | true/false |
| 卡片填充渐变起始色 | `option.card.fill.gradient.startColor` | #05336a |
| 卡片填充渐变结束色 | `option.card.fill.gradient.endColor` | #0bb2ff |
| 卡片填充图片 | `option.card.fill.image.url` | /img/xxx.png |
| 外层间距 | `option.layout.gap` | 16 |
| 外层内边距 | `option.layout.padding.top/right/bottom/left` | 16 |
| 外层排列方式 | `option.layout.justify` | space-between |
| 外层圆角 | `option.layout.borderRadius` | 0 |
| 外层边框宽度 | `option.layout.borderWidth` | 0 |
| 外层填充类型 | `option.layout.fill.type` | none/color/gradient/image |
| 外层填充颜色 | `option.layout.fill.color` | #0b2b63 |
| 数值字号 | `option.sections.top.value.fontSize` | 34 |
| 数值字重 | `option.sections.top.value.fontWeight` | 600 |
| 数值颜色 | `option.sections.top.value.fontColor` | #d8f1ff |
| 单位字号 | `option.sections.top.value.unit.fontSize` | 18 |
| 标签字号 | `option.sections.bottom.label.fontSize` | 14 |
| 标签颜色 | `option.sections.bottom.label.fontColor` | #9ed3ff |

### JCapsuleChart（胶囊图）

| 说明 | 配置路径 | 示例值 |
|------|---------|--------|
| 显示数值 | `option.showValue` | true/false |
| X轴名称 | `option.unit` | 个 |

### JGauge（仪表盘）

| 说明 | 配置路径 |
|------|---------|
| 刻度值显隐 | `option.series[0].axisLabel.show` |
| 刻度值颜色 | `option.series[0].axisLabel.color` |
| 刻度线显隐 | `option.series[0].axisTick.show` |
| 分割线显隐 | `option.series[0].splitLine.show` |
| 分割线颜色 | `option.series[0].splitLine.lineStyle.color` |
| 指标字号 | `option.series[0].detail.fontSize` |

### JProgress（进度条-ECharts）

| 说明 | 配置路径 |
|------|---------|
| 显示标题 | `option.yAxis.axisLabel.show` |
| 标题字体颜色 | `option.yAxis.axisLabel.color` |

### JColorBlock（色块指标卡）

| 说明 | 配置路径 |
|------|---------|
| 行数 | `option.lineNum` |
| 边距 | `option.padding` |

### JScrollBoard（轮播表）

| 说明 | 配置路径 |
|------|---------|
| 悬浮暂停 | `option.hoverPause` |
| 等待时间 | `option.waitTime` |

## 图层顺序机制

**核心：`template` 数组索引决定 z-index，不是 orderNum。** 索引 0 = 最顶层。

### 新增组件必须置顶（强制）

> **新添加的组件必须插入到 `template` 数组的索引 0 位置（即最顶层），确保不会被已有组件遮挡。**
> `bi_utils.add_component()` 已使用 `insert(0, comp)` 实现自动置顶。自定义脚本操作模板时也必须用 `insert(0, comp)` 而非 `append(comp)`。

```python
# 置顶
element = tmpl.pop(target_idx)
tmpl.insert(0, element)
# 保存
bi_utils._page_components[PAGE_ID] = tmpl
save_page(PAGE_ID)
```

## 可用快捷函数（bi_utils.py）

**页面管理：** `create_page`, `query_page`, `list_pages`, `save_page`, `delete_page`, `recover_page`, `copy_page`

**添加组件：** `add_number`, `add_chart`(JBar/JLine/JPie/JRing/JRose/JFunnel/JRadar/JHorizontalBar/JSmoothLine/JStackBar/JMixLineBar), `add_table`, `add_scroll_table`, `add_ranking`, `add_text`, `add_image`, `add_gauge`, `add_liquid`, `add_countdown`, `add_border`, `add_decoration`, `add_current_time`, `add_word_cloud`, `add_color_block`, `add_progress`, `add_total_progress`, `add_component`

## Step 4: 输出结果

**必须将预览地址作为单独一行返回，并用 clip.exe 复制到剪贴板。**

**⚠️ 每次任务完成后必须输出总耗时（强制）：**

- **脚本中**：开头记录 `import time; t0 = time.time()`，末尾输出 `print(f'耗时: {time.time()-t0:.1f}s')`
- **多轮调用/纯API操作**：在最终回复文字末尾补充一行 `耗时：约 Xs`
- 可利用 API 响应中的 `timestamp` 字段估算（首尾两次响应时间戳之差）
- **禁止输出每个步骤的耗时**，只输出整个任务从开始到结束的总耗时

```
## 大屏创建成功

- 页面ID：{id}
- 页面名称：{name}
- 组件数量：{count} 个

预览地址：
{API_BASE}/drag/share/view/{id}?token={TOKEN}&tenantId=2
```

```bash
echo -n "{完整URL}" | clip.exe
```

**⚠️ 写了 Java 接口时，脚本末尾必须额外输出（强制）：**

```python
# 脚本末尾固定追加此段输出，让用户知道后续操作
print("\n" + "="*60)
print("大屏组件已生成完成！")
print("="*60)
print("\n【API 接口地址】（需重启后端后生效）：")
print(f"  {API_BASE}/drag/mock/xxxFlow")           # 根据实际接口路径替换
print(f"  {API_BASE}/drag/mock/xxxFlowMulti")       # 如有多个接口逐行列出
print("\n【重要提示】请重启 Spring Boot 后端服务！")
print("  重启后 API 数据集将自动拉取接口数据，图表即可显示。")
print("\n【大屏预览地址】")
print(f"  {API_BASE}/drag/share/view/{PAGE_ID}?token={TOKEN}&tenantId=2")
print("="*60)
```

## bi_utils 使用规则（强制）

### 初始化方式

```python
# 正确：直接赋值模块级全局变量
bi_utils.API_BASE = 'http://...'
bi_utils.TOKEN = '...'

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
- **必须加 `PYTHONIOENCODING=utf-8` 前缀**（Windows 默认 GBK 编码，脚本中含 emoji（✅⚠️等）或中文输出时报 `UnicodeEncodeError: 'gbk' codec can't encode character`。**所有 `py script.py` 调用必须写成 `PYTHONIOENCODING=utf-8 py script.py`**，且脚本内部 `print` 禁止使用 emoji 字符）

### 快捷操作：linkage_ops.py（组件联动/钻取）

> **组件联动 = 点击源组件，将参数传递给目标组件的数据集查询参数，目标组件自动刷新数据。**

**脚本位置**：`<skill_base_dir>/references/scripts/linkage_ops.py`

**执行方式**：直接在本 skill 的 `references/scripts/` 目录下运行，无需 cp。`bi_utils.py` 位于上级目录，脚本会自动找到。Claude 执行时根据当前平台构建完整路径（macOS/Linux 用 `python3`，Windows 用 `py`）。

**核心命令：**
```bash
# 查看页面所有联动配置
py linkage_ops.py show $API_BASE $TOKEN $PAGE_ID

# 添加联动（--mapping 格式：src=tgt，多个逗号分隔）
py linkage_ops.py add-linkage $API_BASE $TOKEN $PAGE_ID --source "源组件名" --target "目标组件名" --mapping "value=age"
py linkage_ops.py add-linkage $API_BASE $TOKEN $PAGE_ID --source "柱形图" --target "饼图" --mapping "name=name,value=keyword"

# 删除联动
py linkage_ops.py remove-linkage $API_BASE $TOKEN $PAGE_ID --source "源组件名" --target "目标组件名"

# 添加钻取（自刷新下钻，--comp 为源组件，无 --target；钻取是组件对自身的递归查询，不是跨组件）
py linkage_ops.py add-drill $API_BASE $TOKEN $PAGE_ID --comp "组件名" --mapping "name=year"
# 多级钻取（逗号分隔，第1级用 drillData[0]，第2级用 drillData[1]）
py linkage_ops.py add-drill $API_BASE $TOKEN $PAGE_ID --comp "组件名" --mapping "name=year,name=month"

# 删除钻取
py linkage_ops.py remove-drill $API_BASE $TOKEN $PAGE_ID --comp "组件名"
```

**联动 vs 钻取核心区别（务必记住）：**

| 特性 | 联动（add-linkage） | 钻取（add-drill） |
|------|---------------------|-------------------|
| 刷新对象 | **其他**组件 | **自身**（递归查询） |
| 参数 | `--source + --target` | `--comp`（只有自己） |
| 支持回退 | 不支持 | 支持（图表左上角回退按钮） |
| 数据集 | 目标组件各自有数据集 | 自身数据集接受参数重新查询 |

**三级钻取完整配置示例（年→月→日）：**
```python
# 1. API端点需根据参数返回不同层级数据：
#    无参数 → 年数据；?year=xxx → 月数据；?month=xxx → 日数据
# 2. 数据集 URL 含 FreeMarker 占位符
DRILL_API = f"{API_BASE}/drag/mock/drillYearMonthDay?year=${{year}}&month=${{month}}"
# 3. drillData 配置两级映射
cfg['drillData'] = [
    {'source': 'name', 'target': 'year'},   # 第1级：点击年份 → 传 year 参数
    {'source': 'name', 'target': 'month'},  # 第2级：点击月份 → 传 month 参数
]
# 4. paramOption 声明参数（供前端识别）
cfg['paramOption'] = [
    {'text': '年份', 'value': 'year',  'paramType': '3', 'paramTxt': '年份', 'paramValue': '', 'isRequired': '0'},
    {'text': '月份', 'value': 'month', 'paramType': '3', 'paramTxt': '月份', 'paramValue': '', 'isRequired': '0'},
]
```

> ⚠️ **上方多条 drillData 方案仅适用于 API 数据集**。SQL 数据集三级钻取必须用下方「单参数编码值」方案，原因见踩坑。

---

### 🚨 SQL 数据集多级钻取：必须用单参数编码值方案（实测 2026-04-17）

**根本原因：** 前端点击时会**同时触发所有 drillData 条目**，而非按层级逐条执行。  
配置 `name→year, name→month` 两条时，点击年份柱（如 2023）会同时设置 `year="2023"` 和 `month="2023"`，SQL 误判进入日级查询，`sale_month=2023` 无数据。

**正确方案：单参数 `drill_val` + 编码值**

| 层级 | `drill_val` 值 | FreeMarker 判断 | 返回数据 |
|------|--------------|----------------|---------|
| 年级（初始） | `""` 空 | `<#else>` | 年份汇总 |
| 月级 | `"2024"` | `isNotEmpty` 且不含 `-` | 该年各月 |
| 日级 | `"2024-06"` | `isNotEmpty` 且含 `-` | 该月各日 |

**SQL 模板（FreeMarker，实测可用）：**

> ⚠️ **禁止用 `drill_val?contains("-")` 判断层级**：日级值 `"2024-06-01"` 也含 `-`，点击日柱后 `SUBSTRING_INDEX(...,'-',-1)` 取到 "01"（日），被误当 `sale_month=1`，显示错误数据。**必须用 `drill_val?length` 精确区分**。

```sql
<#if isNotEmpty(drill_val) && drill_val?length gt 7>
-- 日级再点击（drill_val="2024-06-01"，length=10）→ 重新显示同月各日，停止下钻
SELECT CONCAT(SUBSTRING_INDEX('${drill_val}','-',2),'-',LPAD(sale_day,2,'0')) as name,
       ROUND(SUM(total_amount),0) as value
FROM sales_table
WHERE sale_year  = CAST(SUBSTRING_INDEX('${drill_val}','-',1) AS UNSIGNED)
  AND sale_month = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX('${drill_val}','-',2),'-',-1) AS UNSIGNED)
GROUP BY sale_day ORDER BY sale_day
<#elseif isNotEmpty(drill_val) && drill_val?length gt 4>
-- 月级（drill_val="2024-06"，length=7）→ 显示该月各日
SELECT CONCAT('${drill_val}','-',LPAD(sale_day,2,'0')) as name,
       ROUND(SUM(total_amount),0) as value
FROM sales_table
WHERE sale_year  = CAST(SUBSTRING_INDEX('${drill_val}','-',1) AS UNSIGNED)
  AND sale_month = CAST(SUBSTRING_INDEX('${drill_val}','-',-1) AS UNSIGNED)
GROUP BY sale_day ORDER BY sale_day
<#elseif isNotEmpty(drill_val)>
-- 年级（drill_val="2024"，length=4）→ 显示该年各月
SELECT CONCAT('${drill_val}','-',LPAD(sale_month,2,'0')) as name,
       ROUND(SUM(total_amount),0) as value
FROM sales_table
WHERE sale_year = ${drill_val}
GROUP BY sale_month ORDER BY sale_month
<#else>
-- 初始（drill_val=""）→ 显示各年汇总
SELECT sale_year as name,
       ROUND(SUM(total_amount),0) as value
FROM sales_table
GROUP BY sale_year ORDER BY sale_year
</#if>
```

**三个层级的 `drill_val` 长度规律（固定格式）：**

| 格式 | 示例 | 长度 | 层级 |
|------|------|------|------|
| `YYYY` | `"2024"` | 4 | 年级 → 显示月 |
| `YYYY-MM` | `"2024-06"` | 7 | 月级 → 显示日 |
| `YYYY-MM-DD` | `"2024-06-01"` | 10 | 日级（最细，停止下钻） |

**drillData + paramOption 配置（单条）：**
```python
cfg['drillData'] = [{'source': 'name', 'target': 'drill_val'}]
cfg['paramOption'] = [
    {'text':'下钻键','value':'drill_val','paramType':'3',
     'paramTxt':'下钻键','paramValue':'','isRequired':'0'}
]
```

**关键点：**
- `drill_val?contains("-")` 是标准 FreeMarker 字符串内建，JimuBI 支持 ✅
- CONCAT 中必须用 `'${drill_val}'`（加引号），不能用裸 `drill_val`（会被当 SQL 列名报错）
- 年份上下文编码在值中（`"2024-06"` 同时含年和月），无需多参数传递

---

**⚠️ 易错点（强制记忆）：**

| 错误写法 | 正确写法 | 说明 |
|---------|---------|------|
| `add-drill --source "A" --target "B"` | `add-drill --comp "A"` | 钻取无 `--target`，是自刷新不是跨组件 |
| `--param "value:age"` | `--mapping "value=age"` | 参数名是 `--mapping` 不是 `--param` |
| `--mapping "value:age"` | `--mapping "value=age"` | 映射用 `=` 分隔，不是 `:` |
| `--mapping "a=b c=d"` | `--mapping "a=b,c=d"` | 多个映射用逗号分隔 |
| SQL 多级钻取配置多条 drillData | SQL 多级钻取用单参数编码值方案 | 多条 drillData 同时触发，参数互相污染 |
| SQL CONCAT 中用裸 `drill_val` | `CONCAT('${drill_val}',...)` | 裸变量名被当 SQL 列名，报 Unknown column |

**联动前提：** 目标组件已绑定数据集且 SQL/URL 含对应查询参数。**钻取前提：** 自身数据集 URL 含 FreeMarker 参数，API 端点能返回不同层级数据。

### 快捷操作：组件连线（linesConfig.connectLine）

> **仅 JImg 支持连线**，JCustomIcon 不支持。`linesConfig` 在 `config` 顶层（与 `option` 同级）。
> 完整结构、枚举值、脚本见 `references/connect-line-guide.md`

**核心结构：** `config.linesConfig = {"connectLine": [{"sourceId","targetId","startPosition","endPosition","lineType","lineColor","lineWidth"}], "show": false}`

**默认值：** `startPosition/endPosition=AutoDefault`，`lineWidth=3`，`lineType=Straight`，`lineColor=#75cede`

**操作流程（2 轮）：**
```
轮次1: cp bi_utils.py + Write connect_line.py（并行）
轮次2: PYTHONIOENCODING=utf-8 py connect_line.py && rm connect_line.py bi_utils.py
```

**易错点：** `linesConfig` 不在 `option` 内；`config` 必须 `json.dumps()` 序列化；`targetId` 用 UUID 不用组件名；必须含 `"show": false`

---

### 快捷操作：link_ops.py（外部链接跳转）

> **组件外部链接 = 点击图表跳转到外部 URL，并将点击参数带到链接地址上。**

**脚本位置**：`<skill_base_dir>/references/scripts/link_ops.py`

**执行方式**：直接在本 skill 的 `references/scripts/` 目录下运行，无需 cp。`bi_utils.py` 位于上级目录，脚本会自动找到。Claude 执行时根据当前平台构建完整路径（macOS/Linux 用 `python3`，Windows 用 `py`）。

**核心命令：**
```bash
# 查看页面所有外部链接配置
py link_ops.py show $API_BASE $TOKEN $PAGE_ID

# 设置外部链接（按名称/类型/ID 三选一定位组件）
py link_ops.py set $API_BASE $TOKEN $PAGE_ID --name "饼图名" --url "https://www.baidu.com/s?wd=\${name}&value=\${value}"
py link_ops.py set $API_BASE $TOKEN $PAGE_ID --type "JPie" --url "https://example.com/detail?category=\${name}"
py link_ops.py set $API_BASE $TOKEN $PAGE_ID --id "538804ec..." --url "https://www.baidu.com/s?wd=\${name}" --target "_self"

# 删除外部链接
py link_ops.py remove $API_BASE $TOKEN $PAGE_ID --name "饼图名"
```

**URL 参数占位符（来自 ECharts 点击事件 params）：**

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `${name}` | 维度名称 | 饼图扇区名、柱子 x 轴标签 |
| `${value}` | 数值 | 饼图扇区值、柱子高度 |
| `${type}` | 系列名称 | 多系列图表的系列标识 |

**打开方式（--target）：** `_blank`（新窗口，默认）、`_self`（当前窗口）

**原理：** `config.linkType='url'` + `turnConfig={url,type}`，前端从 ECharts params 替换 `${...}` 后跳转。

### 快捷操作：自定义JS脚本（config.jsConfig）

> **自定义JS脚本 = 点击组件时执行 JS 代码，实现自定义跳转、弹窗等逻辑。**
> 参考文档：https://help.jimureport.com/biScreen/base/interactive/customJS

**存储字段**：`config.jsConfig`（字符串）。执行顺序：jsConfig → (return true?) → 外部链接 → 联动 → 钻取。return false 阻断后续。

**脚本参数 `params` 常用属性（ECharts 图表）：**

| 属性 | 含义 | 示例 |
|------|------|------|
| `params.name` | 维度名称 | 柱子 x 轴标签、饼图扇区名 |
| `params.value` | 数值 | 柱子高度、饼图扇区值 |
| `params.data` | 原始数据对象 | `{name:'北京', value:100}` |
| `params.dataIndex` | 数据索引 | 0, 1, 2... |
| `params.seriesName` | 系列名称 | 多系列图表的系列标识 |
| `params.seriesIndex` | 系列索引 | 0, 1, 2... |

> 更多属性参考 [ECharts 事件文档](https://echarts.apache.org/zh/api.html#events.%E9%BC%A0%E6%A0%87%E4%BA%8B%E4%BB%B6)

**设置方式（三种，按复杂度选择）：**

```bash
# 方式1：link_ops.py set-js（推荐，支持多行脚本）
py link_ops.py set-js $API_BASE $TOKEN $PAGE_ID --name "基础柱形图" --js 'window.open("http://jeecg.com");return false;'

# 方式1b：从文件读取复杂脚本
py link_ops.py set-js $API_BASE $TOKEN $PAGE_ID --type "JBar" --js-file script.js

# 方式2：comp_ops.py edit（简单单行脚本）
py comp_ops.py edit $API_BASE $TOKEN $PAGE_ID --name "基础柱形图" --set "jsConfig=window.open(\"http://jeecg.com\");return false;"

# 方式3：自定义 Python 脚本（需要精确控制换行符等）
# cfg['jsConfig'] = 'window.open("http://jeecg.com");\nreturn false;'
```

```bash
# 查看页面所有自定义JS脚本配置
py link_ops.py show $API_BASE $TOKEN $PAGE_ID    # show 命令同时展示外部链接和JS脚本

# 删除自定义JS脚本
py link_ops.py remove-js $API_BASE $TOKEN $PAGE_ID --name "基础柱形图"
```

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

## 核心踩坑速查

| 问题 | 核心规则 |
|------|---------|
| **锁定/解锁组件** | 锁定字段是顶层 `disabled`，不是 `isLock`。解锁禁止用 `--set "disabled=false"`（写入 config 内部无效），必须用自定义脚本操作顶层：`comp['disabled']=False; comp['selected']=False` |
| **🚨 删除前必须询问用户确认** | 除非用户明确说"删除/去掉/移除"，禁止自行执行任何 delete 操作。删除不可逆 |
| **🚨 严禁 bi_utils.add_xxx + save_page** | add_component 初始化空列表，save_page 覆盖已有组件。必须用 comp_ops.py add |
| **🚨 add_component 不加载静态数据（实测 2026-04-20）** | `bi_utils.add_component()` 固定 `dataType=1`、`chartData=[]`，不读 `default_configs.json`。批量添加静态图表时必须手动加载：`with open('default_configs.json') as f: defaults=json.load(f)`，再从 `defaults[comp_type]` 取 `chartData` 和 `option`，显式写入 config 后传给 `add_component`。否则图表一片空白 |
| **🚨 有 default_configs.json 对应项的组件，必须先拷贝再定制（两步顺序不可颠倒，实测 2026-04-22 多次违规）** | 编写任何自定义脚本时，凡是 `default_configs.json` 中有对应 key 的组件，**第一步必须 `d = copy.deepcopy(defaults[compType])`，第二步才在 `d['option']` 上覆盖定制字段**。直接手写 option dict 必然遗漏 `series`/`tooltip`/`grid`/`rowNum`/`carousel` 等渲染必需字段，导致组件空白（JScrollRankingBoard 缺 rowNum/sort/carousel，JBreakRing 缺 series/tooltip/innerRadius，均因此不显示）。**禁止先手写 option 再拷贝个别字段进去**——顺序必须是：拷贝完整默认 → 覆盖定制项。 |
| **🚨 add_component 前必须缓存 template（多次违规）** | 任何场景调用 add_component 前，必须先：`page=bi_utils.query_page(PAGE_ID)` → `bi_utils._page_components[PAGE_ID]=page.get('template',[])` → 再调 add_component。漏写两行则大屏所有已有组件被永久清空。适用：singleFile/dataType=4/YApi批量/所有自定义脚本 |
| **POST /drag/page/edit 乐观锁** | 必须传 `updateCount` |
| **chartData 必须是 JSON 字符串** | `json.dumps(...)` 后传入。**⚠️ default_configs.json 中 chartData 原始类型不一致**（list/dict/str 三种均有，如 JScrollList_1/2/3 是 list，JPivotTable 是 dict），从 defaults 读取后必须统一转换：`cd = d.get('chartData', []); cfg['chartData'] = cd if isinstance(cd, str) else json.dumps(cd, ensure_ascii=False)`。漏转或类型判断不全导致组件不显示或 TypeError（实测 2026-04-21） |
| **option 必须是 dict，禁止 json.dumps** | `cfg['option'] = {...}`（dict），`cfg['chartData'] = json.dumps(...)`（string）。两者相反：option 是对象，chartData 是字符串。json.dumps option 会导致前端 `TypeError: Cannot create property 'xxx' on string` |
| **dataMapping 的 filed 拼写** | `filed`（不是 `field`，少一个 d） |
| **🚨 dataMapping 只能用于 default_configs.json 中已有该字段的组件** | 绑定数据集前必须先查 `default_configs.json` 对应组件配置：有 `dataMapping` 字段才写，没有则禁止添加。无此字段的组件（JCommonTable/JScrollBoard 等）有各自的字段映射机制，详见下方「组件字段映射机制三分类」章节（2026-04-21 实测） |
| **🔍 组件显示异常时：先在 UI 拖出参考组件，再 queryById 对比 config** | 遇到组件不显示或布局异常，最有效的调试方法：①在界面拖出相同组件到新页面，②用 `queryById` 查两个页面，③对比 `config` 差异（重点关注 `chartData` 类型、`config.size` 结构、`option` 关键字段）。已通过此方法发现：JScrollList chartData 须为字符串、JBubbleRank config.size 须省略 width（实测 2026-04-21） |
| **🚨 JScrollList 变体 compType 必须是 `JScrollList`，禁止用 `JScrollList_1/2/3`（实测 2026-04-21）** | `JScrollList_1/2/3` 在前端不是有效 compType，用这些名称添加的组件完全不显示。三个变体的 compType 均为 `JScrollList`，variant 通过 option 区分：单行=`showHeader:false,showIndex:false,itemsPerRow:1`；多行+序号=`showHeader:false,showIndex:true,itemsPerRow:2`；带表头=`showHeader:true,showIndex:true,itemsPerRow:1`。default_configs.json 中 `JScrollList_1/2/3` 只是配置模板 key，不是 compType |
| **🚨 JStatsSummary/JCardScroll 变体后缀同理：`_1/_2/_3` 只是 default_configs.json 的模板 key，不是真实 compType（实测 2026-04-22）** | 用 `bi_utils.add_component('JStatsSummary_1',...)` 写入 template 的 `component` 字段为 `JStatsSummary_1`，前端找不到组件，完全不渲染。实际 compType 必须是 `JStatsSummary`/`JCardScroll`（无后缀）。**现已在 `bi_utils.add_component` 内置 `_resolve_comp_type` 自动剥离数字后缀**，`comp_ops.py add` 也已有此逻辑，两条路径均安全。自定义脚本手工构造 `comp` dict 时仍需注意：`'component': 'JStatsSummary'`（不是 `_1`）。 |
| **颜色格式只支持十六进制（实测 2026-04-20）** | 大屏所有颜色字段**只支持 `#RRGGBB` 或 `#RRGGBBAA` 十六进制格式**，禁止使用 `rgba(...)`。含透明度时用 8 位十六进制：`alpha=0→00, 0.15→26, 0.3→4d, 0.4→66, 0.5→80, 0.6→99, 0.8→cc, 1→ff`。示例：`rgba(6,18,50,0.6)` → `#06123299` |
| **透明色** | 用 `#FFFFFF00`，禁止 `rgba(0,0,0,0)`（被解析为红色） |
| **background 字段位置** | config 顶层，与 option 同级 |
| **图表标题去重** | `card.title=''`，只用 `option.title.text` |
| **🚨 JText 颜色/样式必须写在 option.body 内（实测 2026-04-22）** | JText 读取路径是 `option.body.color`，fallback 为 `#000000`。写在 `option.color` 顶层无效，显示黑色。完整字段路径见 `references/bi-comp-option-config.md`「文本设置 TextOption」章节 |
| **🚨 option.title 两种模式，禁止混用（实测 2026-04-21）** | ECharts 组件（JBar/JLine/JPie 等）：`option.title` 是 **dict**，隐藏用 `option.title.show=False`。非 ECharts 组件（JFlashList/JBubbleRank 等）：`option.title` 是**字符串**，显隐用单独的 `option.titleShow` 布尔字段。判断方法：defaults.json 中 `option` 里若有 `titleShow` 字段 → 字符串模式，禁止将 title 字符串转为 dict，否则渲染 `[object Object]`。目前已知字符串模式组件：`JFlashList`（`titleShow+title`）|
| **图层顺序** | 数组索引 0=最顶层，新增组件必须 `insert(0,...)`，`orderNum` 无效 |
| **组件 ID/名称字段** | ID 是 `i`（不是 `id`），名称是 `componentName`（不是 `label`/`name`） |
| **template 字段** | `query_page` 返回组件列表在 `template`（已是 list），不是 `pageTemplate` |
| **bi_utils 初始化** | 直接赋值 `bi_utils.API_BASE/TOKEN`，无 init() 方法 |
| **Windows 命令** | 用 `py` 不是 `python`；所有脚本必须加 `PYTHONIOENCODING=utf-8`；脚本 print 禁用 emoji |
| **存储过程 DDL** | JimuReport API 不能执行 DDL，必须 pymysql 直连创建存储过程 |
| **FreeMarker 判空** | `<#if isNotEmpty(age)>`，禁止 `age?? && age?length gt 0` |
| **带 FreeMarker 的 SQL** | 禁止 bash 命令行传递（`${}` 被 shell 消费），用 `--sql-file` |
| **`${}` 和 `#{}` 不混用** | `${param}` 是查询参数，`#{sys_user_code}` 是系统变量 |
| **JWeatherForecast** | comp_ops.py 不支持，用自定义脚本；dataType 必须为 1 |
| **🚨 JPermanentCalendar 静态 chartData 必须用当月日期** | 日历默认展示当月，static chartData 若用历史月份则数据点不可见。任何脚本添加日历时必须动态生成：`y,m=date.today().year,date.today().month`，dates 替换为 `f'{y}-{m:02d}-{d:02d}'`。`gen_all_comps.py` 已内置此逻辑；自定义脚本务必同步处理 |
| **WebSocket 数据集** | 预置脚本不支持，必须自定义脚本创建；querySql 填 ws:// 地址 |
| **WebSocket socketId** | `chartId + '_' + md5(token)`，Java 推送必须用完整 socketId |
| **WebSocket 推送格式** | `{"chartId":chartId,"result":dataJsonStr}`，data 在 result 字段 |
| **批量添加组件** | 必须用 bi_utils.add_component()，禁止手动构造 comp dict（会遗漏 size/chart/turnConfig） |
| **option.title 类型** | default_configs.json 中 title 可能是 str，直接 `['text']` 报错，先 `if isinstance(title,str): title={'text':title}` |
| **全组件排除装饰类** | 排除 JWeatherForecast/JDragBorder/JDragDecoration，不是业务组件 |
| **componentName 必须用中文名** | 批量生成时图层名用中文（如"基础柱形图"），禁止用 compType（JBar/JPie） |
| **全组件禁止为分类生成 JText 标题** | 分类只是代码注释，不生成 20 个文本图层 |
| **批量绑定数据集** | ①端点：POST /drag/onlDragDatasetHead/getAllChartData；②filed 是槽位标签；③必须设 fieldOption 及 dataSetName 等完整字段 |
| **linkage_ops.py 参数** | 映射用 `--mapping "src=tgt"`，等号分隔，多个逗号连接 |
| **add-drill 无 --source/--target** | 钻取只有 `--comp` 和 `--mapping`，是自刷新下钻而非跨组件 |
| **🚨 SQL 数据集多级钻取禁用多条 drillData** | 多条 drillData 前端同时触发，所有参数被设为同一点击值（如 year=2023 month=2023），SQL 误判层级返回空。**必须用单参数编码值方案**（见「快捷操作：linkage_ops.py」章节「SQL 数据集多级钻取」小节） |
| **🚨 API_BASE 未知禁止 curl 探测** | 直接问用户"请提供完整 API 地址"，禁止尝试 /sys/login 等路径 |
| **yapi_ops.py create-mock 参数** | 接口标题参数是 `--title`，不是 `--name` |
| **subprocess 调用 yapi_ops.py** | 子命令必须在 YAPI_BASE 之前：`['py','yapi_ops.py', cmd, YAPI_BASE, EMAIL, PWD]` |
| **YApi mock 前先 list** | 直接创建会重复，先 `yapi_ops.py list` 查已有接口，复用已存在的 |
| **YApi 凭据未知** | 用户说 Mock 但无 YApi 凭据时，直接走 Java 接口方案 |
| **弹窗/追加组件禁止 save_page** | query_page 可能返回空 template，追加场景必须用 `_request('GET',queryById)` + `_request('POST',edit)` 绕过 save_page |
| **componentName 匹配禁止 Unicode 转义** | 极易写错（柱→漱），优先按 `component`（英文 compType）匹配 |
| **写 Java 接口** | 禁止自行 Grep 搜索 Controller 文件，必须问用户路径；完成后脚本末尾必须输出接口 URL + 重启提示 |
| **多图表 slot_labels** | 单系列 `[维度,数值]`；多系列 `[维度,数值,分组]`；双轴 `[维度,数值,数值2]` |
| **subprocess 与脚本外重复调用** | 脚本只建数据集，组件添加统一在脚本外用 comp_ops.py add，禁止混用 |
| **cp 后必须 ls 验证** | cp 可能静默失败，必须 `&& ls *.py *.json` 验证，否则 ModuleNotFoundError |
| **response.get 接收 null** | `result=null` 时 `.get('result',{})` 返回 None，必须用 `(resp.get('result') or {})` |
| **嵌套 null 字段** | `{"data":null}` 时 `.get('data',[])` 返回 None，必须用 `.get('data') or []` |
| **自写接口 getAllChartData** | 重启前 404，必须 try/except 包裹，失败时 print 警告并继续，禁止阻断脚本 |
| **API 数据集 /add 字段名** | `datasetItemList`（不是 onlDragDatasetItemList）；/add 后无需再 queryById+edit 回写 |
| **API返回值可能是 list** | getAllGroup 等返回 list，调 `.get()` 报错，先判断类型 |
| **数据集创建时传字段列表** | /add 时同步传 `datasetItemList`，系统不自动解析 |
| **数据集分组字段** | 用 `parentId`（分组节点 id），不是 groupCode。示例数据集固定 id=1516743332632494082 |
| **getAllGroup 字段名** | 用 `item.get('name')`，不是 `groupName` |
| **SQL 注入防护** | information_schema/SHOW TABLES 会被 JeecgBoot API 拦截；但 pymysql 直连不受此限制，可用于查询真实表名 |
| **🚨 严禁猜测表名（2026-04-15 严重事故）** | 编写 SQL 前必须 pymysql 直连执行 `SHOW TABLES` 确认表存在。`jimu_drag_page` 不存在，大屏页面表实际是 `onl_drag_page` |
| **🚨 dataset_ops.py edit 不支持 --fields** | edit 命令只更新 SQL，不写字段列表，导致数据集字段为空、图表无数据。必须用自定义脚本：`queryById` 取实体 → 设置 `ds['datasetItemList']` → `edit` 保存 |
| **自定义脚本 SQL 数据集** | API 字段名是 `dbSource`（数据源 ID），不是 dbKey |
| **数据源 /add result 类型** | 数据源 /add 的 result 是字符串 ID；数据集 /add 的 result 是完整 dict（用 `.get('id')` 取） |
| **数据集 edit 字段名** | 必须用 `datasetItemList`，用 `onlDragDatasetItemList` 静默忽略 |
| **queryFieldByApi 空列表** | fallback：getAllChartData 推断字段类型再 edit 回写 |
| **queryAllById 需签名** | bi_utils 不兼容，用 queryById 替代 |
| **MySQL 版本 dbType** | MySQL 8 用 `MYSQL8`，MySQL 5.7 用 `MYSQL5.7` |
| **MongoDB 数据集 dataType** | 仍是 `'sql'`，不是 `'mongodb'`（无此枚举） |
| **py - heredoc** | stdin 模式 sys.path 绑定进程目录，import bi_utils 报错。必须 Write 脚本文件再 py 执行 |
| **执行脚本必须 cd 到 scripts 目录** | 所有脚本直接在 `<skill_base_dir>/references/scripts/` 下执行，`_find_bi_utils()` 自动从上级目录加载 `bi_utils.py`，无需 cp |
| **替换图表类型** | delete+add 时从旧 option 继承共通字段（title/xAxis/legend/color），series 专属禁止继承 |
| **JBar 颜色** | `option.color[0]` 不生效，必须同时设 `series[0].itemStyle.color` |
| **JLine 颜色** | 必须同时设 lineStyle.color + itemStyle.color + option.color[0] 三处 |
| **customColor 组件** | JPie/JRose/JLine/JArea/JMixLineBar 等 20 种组件颜色必须用 `option.customColor`，`option.color` 无效。配色规范见「图表配色规范」章节 |
| **Online表单 compStyleConfig** | 不能为 `{}`，必须含完整 summary 子对象 |
| **Online表单 filter** | 必须含 `conditionFields:[], conditionMode:'AND'` |
| **Online表单 chart.category** | JRing→Pie；JBar3d→threeD；JHorizontalBar→HorizontalBar |
| **onlyValueChart** | 仅 Gauge/Number 分类 + JTotalProgress/JLiquid：nameFields=[] |
| **isGroup 图表必须设 typeFields** | JStackBar/JMultipleBar/JRadar 等多系列组件，typeFields 空则无数据 |
| **DoubleLineBar** | nameFields=[]，typeFields=[维度]，assistYFields/assistTypeFields 必须设 |
| **record_count fieldType** | 必须是 `'count'`，用 `'int'` 报 SUM(*) SQL 错误 |
| **地图 commonOption** | 必须含 breadcrumb 字段 |
| **地图 option** | 必须含 drillDown 和 area 顶层字段 |
| **🚨 add_component 添加地图类组件必须显式传 commonOption（实测 2026-04-22）** | `bi_utils.add_component` 不会自动从 `default_configs.json` 加载地图专属字段，JAreaMap/JBubbleMap/JHeatMap 等直接用 comp() 函数添加时 `commonOption` 为空，前端访问 `commonOption.breadcrumb` 报 `TypeError: Cannot read properties of undefined`。**必须显式深拷贝**：`d=copy.deepcopy(DEFAULTS['JAreaMap']); cfg['option']=d['option']; cfg['commonOption']=d['commonOption']`，再传给 add_component。**简写**：`comp('JAreaMap', ..., opt=d['option'], extra={'commonOption': d['commonOption']})` 或在 config dict 中同级传入 commonOption |
| **饼图/雷达/词云/JProgress** | 禁用含 xAxis/yAxis 的柱形 option |
| **JBar series** | 必须含 `type:'bar'`，禁止空数组 |
| **DoubleLineBar yAxis** | 必须是两元素数组，config 根层必须有 seriesType:[] |
| **xAxis/yAxis 格式** | 对象格式（不是数组格式） |
| **isGroup/subclass/category** | 只能在 config.chart 内，放根层前端崩溃 |
| **设计器表单 formId** | 必须是 code 字符串，不能用数值 ID |
| **Online表单 config 辅助字段** | 必须含 assistYFields/calcFields/drillData/jsConfig/appId/actionConfig |
| **弹窗 config** | 必须为 dict，禁止 json.dumps() |
| **弹窗子组件坐标** | x/y 是 JGroup 内部局部坐标，不是屏幕绝对坐标 |
| **FILES 场景** | 直接用 files_ops.py create-bind，JOIN 模式必须传 --group-by/--join-on/--agg |
| **FILES SQL** | 别名不加单引号；禁用 value 关键字（用 sales/amount） |
| **files/get result** | 是 dict 不是 list，`json.loads(result.get('dbUrl','[]'))` |
| **queryFileFieldBySql** | 需签名，bi_utils 不支持，改用 getAllChartData |
| **api.jeecg.com** | 是 YApi mock 服务器，禁止尝试 JeecgBoot /sys/login |
| **page_ops.py rename** | `--name` 是命名参数不是位置参数 |
| **page_ops.py delete** | 不支持，用 `bi_utils._request('DELETE','/drag/page/delete',params={'id':PAGE_ID})` |

> 完整踩坑记录见 `references/pitfalls.md`

## JCustomIcon 图标组件说明

> **来源：** 源码 `customIcon.vue` + `constant.ts`（maxJCustomIconNum=36）实测确认，2026-04-21

设计器左侧面板「图标」区域分两个 Tab，对应**完全不同**的组件类型：

| Tab | compType | 数量 | 核心字段 | 渲染原理 |
|-----|----------|------|---------|---------|
| **图标**（系统图标） | `JCustomIcon` | 36 个（type 01~36） | `config.type` | iconfont class `icon-bigScreen-matter${type}` |
| **图库**（自定义图库） | `JImg` | 动态，从 API 加载 | 图片 URL | 图片组件渲染，与 JCustomIcon **无关** |

### JCustomIcon 正确配置方式

```python
cfg = {
    'type': '05',       # 核心字段：01~36，决定显示哪个系统 iconfont 图标
    'dataType': 1,
    'option': {
        'color': '#ffffff',   # 图标颜色
        'opacity': 1,         # 不透明度 0~1
        'filter': 0,          # 模糊 0~20
    }
}
```

**⚠️ 禁止在 JCustomIcon 上设置 `option.icon`/`option.iconId`/`option.imageUrl` 等字段** —— 这些字段在组件里完全不生效，组件只认 `config.type`。

**图库图片应用 `JImg` 组件添加**，不是 JCustomIcon。

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

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401） | 重新获取 X-Access-Token |
| `updateCount` 不匹配 | 重新查询页面获取最新值 |
| 组件不显示 | 检查 dataType、chartData、option 完整性 |
| 中文乱码 | 使用 Python（不要用 curl） |

## 参考文档

- `references/bi-component-types.md` — 完整组件类型清单
- `references/bi-comp-option-config.md` — 组件样式配置路径
- `references/bi_utils.py` — 工具库源码
- `references/core-configs/data.ts` — 组件面板菜单树 + 初始化 config（原始源码，353KB）
- `references/core-configs/optionData.ts` — 组件属性面板配置项列表（原始源码，57KB）
- `references/core-configs/component-defaults.md` — 82+ 组件默认配置速查（尺寸/chartData/option/dataMapping）
- `references/core-configs/addPageComp-logic.md` — 组件创建流程（addPageComp 函数、newItem 结构、位置计算）
- `references/core-configs/menu-hierarchy.md` — 组件菜单分类树（完整层级 + 统计）
- `references/templates/bigScreen/` — 10 个大屏模板 JSON
- `references/scripts/` — 12 个预置操作脚本 + default_configs.json
