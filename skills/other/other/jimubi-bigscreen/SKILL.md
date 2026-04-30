---
name: jimubi-bigscreen
description: Use when user asks to create/design a big screen (大屏), full-screen data visualization, or says "创建大屏", "生成大屏", "新建大屏", "设计大屏", "做一个大屏", "BI大屏", "数据大屏", "可视化大屏", "监控大屏", "create big screen", "design big screen", "BI visualization big screen". Also triggers when user describes big screen requirements like "做一个销售数据大屏" or mentions full-screen display like "展厅展示", "监控室大屏". Make sure to use this skill for big screens (大屏) — NOT dashboards (仪表盘/看板), which use a completely different layout and styling system.
---

# JeecgBoot 大屏 AI 自动生成器

> 本 skill 处理大屏（bigScreen）。仪表盘（看板）请用 `jimubi-dashboard` skill。

## ⚠️ 核心强制规则（9条）

1. 所有大屏操作必须通过本 skill（禁止未调用 skill 直接读 memory 凭据自行执行）
2. **入口即分叉**：按场景决策树选路径，禁止默认走 spec_builder。spec_builder 仅用于"整屏生成（含组件）"场景。禁止逐组件拼 Python 脚本
3. 🚨 删除/重写/清空前必须询问用户确认（除非用户明确说"删除/去掉/移除/清空/清除"）
4. 🚨 编写 SQL 前必须 SHOW TABLES 确认表名（onl_drag_page ≠ jimu_drag_page）
5. `dataMapping.filed` 拼写：少一个 d（不是 field）
6. Windows：用 `py` 不是 `python`；所有脚本加 `PYTHONIOENCODING=utf-8`
7. 🚨 **用户未指定数据来源时必须先问**（纯静态布局/纯装饰除外）。可选项：静态 mock / YApi 接口 / SQL 数据集 / Excel-CSV 文件 / 存储过程 / 自写 Java API / **BI 直连 Online 表/设计器表单/Online 报表（`dataType=4`）**。⚠️ 用户说"用某 Online 表 / cgform / jeecg 表 / Online 报表 / desform 作为数据源"时**优先 BI 模式**而非 SQL 数据集（详见 `references/bi-mode-online.md`）。禁止默认编造静态数据
8. **真相源优先级（写组件配置 / 数据集绑定都遵循）**：
   - **数据集绑定字段映射** → `references/data-binding-mapping.md`（唯一真相源，描述冲突以此为准；按 §0 检测算法对照 `defaults/<CompType>.json` 判定 A/B/无映射 三型，别猜）
   - **组件 option 字段名（passthrough 自定义组件 JScrollList / JScrollBoard / JScrollTable / JText / JCurrentTime / JStatsSummary / JDragDecoration / JDragBorder / JFlashList / JRectangle / JLiquid / JSemiGauge / JCustomProgress / JListProgress 等，非穷举）**，按以下四级顺序查，找到即止：
     - ① `references/scripts/defaults/<CompType>.json`（初始加载真相源，`--schema <CompType> --full` 调取）
     - ② `references/<comp>-option-config.md`（组件专项文档）
     - ③ `references/bi-comp-option-config.md`（兜底）
     - ④ **以上三级仍找不到 → 说明该字段是 UI 运行时动态写入的**（不在 defaults 里）。正确做法：在页面上手动操作一次该属性，再 `query_page` 观察实际写入了哪些字段，以观察结果为准。典型案例：`JRing` 的环形尺寸，defaults 只有 `series[0].radius`（百分比），但 UI 实际写的是 `option.outRadius` / `option.innerRadius`（像素整数），不查 ④ 直接写百分比字段会被 Vue 渲染器忽略（实测 2026-04-28）
   - 错字段不报错只会被默认值覆盖（看似"有效"实则无效）。禁止按 Vue/React/Bootstrap 习惯拍脑袋写 `bgColor`/`fontColor`/`borderColor`——实际可能是 `backgroundColor`/`alternateBackgroundColor`/`BGC` 等平台自定义名
   - ECharts 标准字段（`series[*].itemStyle.color` / `xAxis.axisLabel.color` 等）可凭记忆写，不受此规则限制
9. **配色禁止 AI 自编色值**——用户说"复古/商务/科技/红涨绿跌"等命名色板，必走 `style_ops.py set-palette --name <名称>`（或 spec 顶层 `palette`）。查色值用 `style_ops.py list-palettes`，不调 API 不耗 token

## ⚡ 写/改任何组件 option 字段前——强制预检（不可跳过）

在编写任何组件 config 脚本、`comp_ops.py edit --set`、或手写 Python patch 之前，**必须先确认字段名，不允许凭 ECharts 文档或经验直接写**。按以下优先级判断：

| 情况 | 做什么 |
|------|--------|
| 当前上下文已有该组件 config（刚 query_page / dump 过） | **直接看它**，从中确认字段名和现有结构 |
| Config 中没有目标字段、或字段名不确定 | **查 `bi-comp-option-config.md`** 对应 CompType section（平台缩写字段如 `legend.t` 只在这里，defaults JSON 里没有） |
| 从零建组件、需要确认初始字段结构 | 先查 `defaults/<CompType>.json`（`--schema <CompType> --full`），再查 `bi-comp-option-config.md` 补充 |
| 以上三处均无 | 在 UI 手动操作一次，`query_page` 观察实际写入字段，以观察结果为准 |

**找到即止，立即执行，禁止从多个来源重复确认同一字段**。任一来源确认字段名后直接跑命令，不再查第二个来源。`comp_ops.py edit` 的 `true/false/数字` 自动类型转换是固定行为，无需每次验证源码。

**错字段不报错不报 warning，只会被默认值静默覆盖**（典型案例：`option.legend.top` 无效，正确字段是 `option.legend.t`；`option.outRadius/innerRadius` 与 `series[0].radius` 同理）。

---

## 大屏平台默认值

- 分辨率 1920×1080（后端默认，spec_builder 不写）| style bigScreen | designType 100
- 主题 dark（spec_builder L797）| 背景 `/img/bg/bg4.png` 深空星空（spec_builder L798）| 图层 bg/border 透明 `#FFFFFF00`
- bg4 色板（spec_builder 内置）：主标题 `#f0c040`，副标题 `#00d4ff`，数值 `#d4e8ff`，轴 `#8ab8d0`，分割线 `#1a3a5a55`
- A股红涨绿跌：`#ff4d4f` / `#52c41a`

---

## 入口判断（先做这一步）

**1. 新建 vs 已有大屏？**

| 用户语境 | 走哪 |
|---------|------|
| 含 page_id / 提到"当前大屏 / 刚才那个屏 / 这个大屏" | **C 组件操作**（已有屏） |
| 说"做一个 / 创建 / 新建 / 设计 XX 大屏" | **B 整屏生成**（新建） |
| 仅说"删除 / 改名 / 换背景 / 克隆" | **A 页面级** |
| 仅说"换数据源 / 绑数据集 / 接 SQL/API" | **D 数据绑定** |
| 模糊（"帮我做大屏"，无 page_id 也无具体诉求） | **必须先问用户**：新建还是修改已有？数据来源？组件清单？ |

**2. 模糊需求兜底（用户没指定组件、数据、布局）**

禁止默认 spec_builder 编造一通。优先动作：
- 问 1-2 个关键问题（业务主题 / 大致 5-8 个图想看什么 / 数据从哪来）
- 或者直接命中 B-Step1 模板时，向用户确认"我用 XX 模板复制后再改"

**3. 高频意图 → 脚本/组件 速查**

| 用户说 | 路径 |
|-------|------|
| "排行 / TOP N / 排名" | 组件首选 `JScrollRankingBoard`，动画版 `JDynamicBar` |
| "KPI / 核心数字 / 大数字" | **≥3 个一组并排** → `JStatsSummary`（一个组件容纳 4-6 项 KPI，自带 label/value/unit/环比，是大屏顶部 KPI 行**首选**）；单个突出大数字 → `JCountTo`（翻牌动画）/ `JNumber`（静态）。⛔ 禁止 N 个 JNumber/JCountTo 横排凑 KPI 行 |
| "完成率 / 达标率" | `JGauge`（指针）/ `JLiquid`（液位）/ `JRingProgress`（环形），value 是 **0-100** 整数 |
| "占比 / 比例 / 分布" | `JPie` / `JRing` / `JRose` |
| "趋势 / 走势 / 时序" | `JLine` / `JSmoothLine` / `JArea` |
| "对比 / 多组数据" | `JBar` / `JMultipleBar` / `JStackBar` |
| "转化 / 漏斗" | `JFunnel` |
| "地图 / 区域 / 飞线 / 热力" | `JAreaMap` / `JFlyLineMap` / `JHeatMap` |
| "装饰 / 好看点" | `JDragDecoration`（12 套预设，禁止与 JDragBorder 混） |
| "边框 / 框一下" | `JDragBorder`（13 套预设，选哪种看 `references/border-style-guide.md`） |
| "标题 / 文字 / 标语" | `JText` |
| "时钟 / 实时时间" | `JCurrentTime` |
| "日历" | `JPermanentCalendar` |
| "换配色 / 复古 / 商务 / 科技色" | `style_ops.py set-palette --name <名称>` |
| "联动 / 点饼图筛柱图" | `linkage_ops.py`（已有屏加联动） |
| "新建多图带联动" | `multi_chart_linkage.py`（一次建多图+联动） |
| "弹窗 / Modal" | `references/popup-guide.md` |
| "外链 / 跳转 / 自定义 JS" | `link_ops.py` |
| "克隆 / 备份 / 恢复" | `backup_ops.py` |
| "看现在有哪些组件" | `comp_ops.py list` |
| "通用组件 / 自由写 ECharts JS / customOption / 写个 JS option 串 / 桑基/树图/自定义图" | **`JCommon`**（菜单"通用组件"） — 写 `config.customOption`（**JS 字符串**，须 `option = {...}; return option;` 结尾），可写 function 等动态逻辑。spec_builder 不会自动写此字段，需 spec 建壳后用 bi_utils patch |
| "自定义组件 / 自定义 echarts / 直接写 echarts JSON" | **`JCustomEchart`**（菜单"自定义组件"） — 写 `config.definitionOption`（**JSON 对象**，纯静态，不能含 function）。spec_builder 不会自动写此字段，需 spec 建壳后用 bi_utils patch |
| "用 Online 表 / cgform / jeecg 表 / Online 报表 / desform 作为数据源" | **BI 模式 (`dataType=4`)** — 见 `references/bi-mode-online.md`，禁止默认套 SQL 数据集 |

> ⚠️ **JCommon ≠ ECharts 内置组件（JBar/JLine/JPie 等）**。"通用组件"是平台菜单分类，专指 JCommon；用户说"通用组件"时**默认指 JCommon**，禁止误映射到 builtin handler 图表。区别看 `references/data-binding-mapping.md` §3。

---

## ⭐ 模糊需求 → 快速好看大屏 SOP（核心）

> **目标**：用户没指定组件/布局/数据时，AI 也能 1 次往返产出"快 + 好看 + 不丑"的大屏。

### 速度铁律（HTTP 越少越快）

| 优先级 | 路径 | HTTP 次数 | 适用 |
|-------|------|-----------|------|
| 🥇 最快 | `template_ops.py copy --replace` | **1** | B-Step1 模板触发词命中 |
| 🥈 次快 | `spec_builder.py` 单次生成全部组件 | **1** | 模板未命中 / 自定义布局 |
| ⛔ 禁止 | 循环 `comp_ops.py add` 逐个加 | N | 任何"建多个组件"的场景都禁止 |

**潜规则**：spec_builder 一个 spec 写 N 个组件 = 1 次 HTTP；逐个 add 一个组件 1 次 HTTP。建 8 个图，前者 1 次，后者 8 次，速度差 ~6-8 倍。

### 组件挑选原则：5 维结构（用户没指定组件时按这个组）

> 不靠行业专属清单，靠**通用结构**——每张大屏从下面 5-7 维选 4-6 项即可，AI 据用户业务描述映射到具体组件。

| 维度 | 用途 | 候选组件（按"高频意图→组件"速查决定具体选哪个） |
|------|------|------------------------------------------------|
| **KPI 数字** | 顶部 KPI 行 ≥3 项 → **JStatsSummary**（首选，一个组件多指标）；单大数字 → JCountTo / JNumber；色块强调 → JColorBlock | — |
| **趋势** | 时间维度变化 | JLine / JArea / JSmoothLine / JStepLine |
| **对比** | 多类目/多组对比 | JBar / JStackBar / JMultipleBar / JMixLineBar |
| **占比** | 部分/整体 | JPie / JRing / JRose / JFunnel |
| **排行** | TOP N | JScrollRankingBoard / JDynamicBar / JBubbleRank |
| **地理**（可选） | 业务含地理属性 | JAreaMap / JFlyLineMap / JBubbleMap / JHeatMap |
| **明细/告警**（可选） | 列表/动态信息 | JScrollList / JScrollBoard / JScrollTable / JFlashList |

**挑选流程**：
1. 读用户描述，提取"想看的指标关键词"
2. 用上方"高频意图→组件"速查表把每个指标映射到具体组件类型
3. 缺维度（如完全没说时间/对比）就**反问**而非自己脑补
4. 行业模板若 B-Step1 命中，**优先 copy 模板**再按需替换组件，比从 0 拼快

### 布局规则（按画布等比例算，不写死坐标）

> 画布尺寸由用户决定（默认 1920×1080；竖屏 1080×1920；4K 等比例放大）。AI 按下面比例规则算坐标，**不要硬背像素**。

**通用比例**（让"不丑"的最小约束）：
- 边距（画布外沿到组件） ≥ 短边 × 4%
- 组件间距 ≥ 短边 × 1.5%–2%
- 标题区高度 ≈ 短边 × 5%–7%
- 所有 x/y/w/h 对齐到 10 或 20 的倍数（防像素错位）
- 检查：组件不重叠（前一个 x+w + 间距 ≤ 后一个 x）、不贴边、不留大块孤儿空白

**三种推荐布局形态**（描述结构，不锁坐标）：
| 形态 | 结构 | 适合 |
|------|------|------|
| **A 顶 KPI 行 + 主图网格** | 顶部 1 行 4-5 个 KPI；下方 2-3 行 × 3 列主图网格 | 最通用驾驶舱 |
| **B 左侧栏 + 中央大图 + 右侧栏** | 两侧各 2-3 个小图；中央 1 大图占 ~50% 宽 | 突出核心趋势/地图 |
| **C 四角 KPI + 中央大图** | 中央大图占主视觉；四角各 1 个 KPI | 监控/指挥中心 |

**默认搭配**：主题 `dark` + 平台命名色板（用户说"复古/商务/科技"等走 `style_ops.py set-palette`）。

### 演示数据量原则（AI 编 mock 时必读）

> **总则**：用户没给真实数据让 AI 编演示数据时，**数据条数尽可能多**。默认值偏少（多数 5-7 条），照抄会让大屏空旷且滚动/分页/排行类组件不触发动效。

| 组件类型 | 推荐演示数据量 | 触发条件 |
|---------|---------------|---------|
| **滚动类**（JScrollList / JScrollTable / JScrollBoard / JFlashCloud / JCardScroll） | ≥ 可视行数 × 1.5（按容器 h / 行高估算可视行数） | 数据 ≤ 可视时不滚 |
| **排行类**（JScrollRankingBoard / JDynamicBar / JCapsuleChart / JBubbleRank / JFlashList） | 取上限 — JBubbleRank 5 / JFlashList 4 / **JScrollRankingBoard：data_count ≥ rowNum+3**（rowNum=floor(h/40)，≈ 10 时 h≈400；h=195 时 rowNum=4） | **data_count > rowNum 才滚动**；两者相等全部展示完毕→不滚动 |
| **类目对比**（JBar / JStackBar / JLine / JArea） | ≥ 8-12 类目（柱图）/ ≥ 12-24 时间点（折线） | 太少视觉空 |
| **占比类**（JPie / JRing / JRose / JFunnel） | 5-8 项（占比类反而忌过多） | — |
| **KPI / 单值类**（JNumber / JCountTo / JGauge / JLiquid） | 1 个值，数据量与该规则无关 | — |
| **地图类**（JAreaMap / JFlyLineMap / JBubbleMap / JHeatMap） | 全国铺满（≥ 25 省份）或 ≥ 30 飞线/热点 | 稀疏会显假 |
| **明细/告警**（JList / JCommonTable / JDevHistory） | ≥ 10-15 行 | 撑满容器才耐看 |

**自检 checklist**：
- 滚动组件保存后回查 `数据行数 vs (h / row.height + marginBottom)` 比值，低于 1.5 倍直接补数据
- spec_builder 默认 chartData 多数是 5-7 条，**禁止照抄默认 chartData 当成"演示数据已够"**
- 真实接口/数据集到位后此规则失效（取真实数据，量由业务定）

### AI 模糊需求处理 SOP（按顺序走）

1. **B-Step1 行业模板命中？**
   - 是 → `template_ops.py copy` → 与用户确认改文案/数据 → 完成
   - 否 → 进入 2
2. **5 维结构 + 高频意图速查 = 选 4-6 个组件**，按形态 A 默认排版
   → `spec_builder.py` 单次生成 → 给用户预览
3. **数据来源未指定** → 必须先问（强制规则 #7）；用户允许 mock 时首选静态 mock 让效果最快出，后续再换真实数据集

---

## 场景决策树（入口即分叉，直达最短路径）

> 先判断操作类型，再判断子场景，**不要默认走 spec_builder**。

---

### A. 页面级操作

| 场景 | 脚本 | 备注 |
|------|------|------|
| **创建空白大屏** | 直接调 `bi_utils.create_page()`（见下方模板） | 禁止用 spec_builder；`page_ops.py` 无 create 子命令 |
| 删除大屏 | `page_ops.py delete` | 必须先确认 |
| 重命名/换背景/加水印 | `page_ops.py` | 读 `references/page-config-guide.md` |
| 标记/取消模板 | `page_ops.py set-template --flag 0\|1` | 单字段改 `izTemplate`，最小 payload |
| 克隆/导出/导入/对比 | `backup_ops.py`（子命令：`clone` / `export` / `import` / `diff`） | |

**创建空白大屏标准调用：**
```bash
cd <skill目录> && python3 - <<'EOF'
import sys, time; sys.path.insert(0, 'references')
import bi_utils
t0 = time.time()
bi_utils.init_api('<API>', '<TOKEN>')
page_id = bi_utils.create_page('<名称>', style='bigScreen', theme='dark', background_image='/img/bg/bg4.png')
wprint(f'预览: <API>/drag/share/view/{page_id}?token=<TOKEN>&tenantId=<TENANT_ID>')
print(f'耗时: {time.time()-t0:.2f}s')
EOF
```

---

### B. 整屏生成（从头新建含组件的大屏）

**Step 1：模板匹配**（用户说"从0开始"则跳过）

| 触发词（含近义） | 模板名 | 模板ID |
|--------|-------|--------|
| 金融/银行/普惠/乡村/信贷/财务/资产/贷款 | 乡村振兴普惠金融服务平台 | 1024608431274250240 |
| 环境/污水/排放/生态/水务/环保/碳排/双碳 | 北京市污水排放总量 | 1022392593179791360 |
| 科技/工业/IoT/能源/电力/制造/工厂/车间/产线/物联网 | 北京科技数字化云平台 | 1014376428645961728 |
| 医院/医疗/机构管理/卫生/诊疗/床位 | 医院实时数据监控 | 1011800681234354176 |
| 旅游/景区/客流/公园/展厅/展会 | 旅游数据分析中心大屏 | 1016994272231608320 |
| 房产/房地产/楼市/租房/物业 | 杭州房地产市场宏观监控 | 1024545852833189888 |
| 警务/安防/治安/监控室/指挥中心/应急 | 警务监控系统 | 1024545264544305152 |
| 交通/车辆/物流/配送/仓储/运输 | 车辆分布图 | 1017325669831987200 |
| 销售/订单/驾驶舱/营收/营销/电商/GMV/CRM | 集团综合数据大屏 | 1151069555267260416 |
| 公园/自然/景点/文旅/园区 | 香山公园客流大数据 | 1027085484978388992 |

**命中** → `template_ops.py copy --replace '{"旧文本":"新文本",...}'`（`--replace` 是 JSON 全局文本替换：对模板内 componentName / chartData / option 的所有匹配文本做 replace），完成，无需进入 Step 2。建议向用户确认"我先用 XX 模板复制再改文案/数据，可以吗？"  
**未命中** → 不许模糊套用（"教育/政务/HR/人力/营业厅/学校"等不在表里的领域，禁止硬塞最近的科技/金融模板）。直接进入 Step 2。  
**领域不在表 + 用户没给组件清单** → 必须先问业务主题与想看的核心指标，再走 Step 2。

**Step 2：数据来源决定路径**

```
数据来源？
├── 静态 mock 数据（用户给数据 / 让 AI 编造）
│     └── spec_builder（一次生成所有组件）
│           1. 读 references/spec-builder.md
│           2. 写 /tmp/<名称>.spec.json
│           3. 执行 spec_builder.py <API> <TOKEN> /tmp/<名称>.spec.json
│
├── YApi mock 接口
│     └── spec_builder 生成布局 → yapi_ops.py 绑定数据集
│
├── SQL 数据集（查数据库）
│     └── spec_builder 生成布局 → dataset_ops.py 绑定
│           注意：SQL 含 ${} 时用 --sql-file，禁止命令行传递
│           必须先 SHOW TABLES 确认表名
│
├── 文件数据集（Excel/CSV）
│     └── spec_builder 生成布局 → files_ops.py 绑定
│
├── 存储过程
│     └── spec_builder 生成布局 → proc_ops.py 绑定
│
└── BI 直连 Online 表 / 设计器表单 / Online 报表（dataType=4）
      触发：用户说"用 X 表 / cgform / jeecg 表 / Online 报表 / desform 作为数据源"
      特点：直接绑表字段，不创建独立数据集；自带字段级时间过滤(timeCondition)和字典翻译
      → 走 references/bi-mode-online.md 的脚本模板（spec_builder 当前不支持，需手写组件 config）
        已有参考大屏时优先 deepcopy 其组件 config（见 bi-mode-online.md §七）
```

**用户未指定数据来源时必须先问**（纯静态布局除外）。

**spec_builder 用法：**
> `--page-id <ID>` 追加组件到已有页面（保留原有组件）；不传则新建页面。
```bash
# 查组件 schema（字段不确定时）
python3 references/scripts/spec_builder.py --schema JStatsSummary        # L1 精简
python3 references/scripts/spec_builder.py --schema JColorGauge --full   # L2 完整
python3 references/scripts/spec_builder.py --schema --list               # L3 总览

# 生成
python3 \
  references/scripts/spec_builder.py <API> <TOKEN> /tmp/<名称>.spec.json
```
spec_builder 自动处理：chartData 序列化、透明 bg、dark 主题、ECharts 轴样式、gradient 展开、pie 无 xAxis/yAxis、compareState 转换、命名色板应用、布局约束预警。

**变体（variant）写法**：spec 中 `type` **不带后缀**（如 `"type":"JStatsSummary"`），变体通过同级 `"variant":"1"` 字段指定（生成 JStatsSummary_1）。直接写 `"type":"JStatsSummary_1"` 会找不到 handler。

**禁止直接 Read `references/scripts/defaults/*.json`**，统一经 `--schema --full` 调取。

---

### C. 组件操作（修改已有大屏）

```
组件操作？
├── 查看当前有哪些组件
│     → comp_ops.py list
│
├── ⭐ 迭代替换（删旧+加新+改色一把梭，单次 HTTP 往返）
│     触发：用户说"换别图表"、"把 XX 换成 YY"、"替换饼图为柱形图" 等
│     → spec_builder --page-id <ID>，spec 顶层同时写 delete + components + palette：
│       {
│         "page": {"name":"..."},
│         "palette": "科技",                              // 可选，自动应用命名色板
│         "delete": {"types": ["JPie","JRing","JAntvGauge"]},  // 按 types/names/ids 任一批量删
│         "components": [ ...仅新增组件... ]
│       }
│     优势：1 次 query_page → 过滤旧 → append 新 → 应用色板 → 1 次 save_page
│           （替代原 3 次 comp_ops delete + 1 次 spec_builder append + 2 次 set-palette = 6 HTTP）
│
├── 添加组件（纯布局 / 静态数据 / 1个或多个）
│     → spec_builder --page-id <ID> /tmp/x.spec.json
│       （spec 只写要新增的组件，自动追加，保留已有组件）
│
├── 添加单组件 + 同时绑定 SQL/文件数据集
│     → comp_ops.py add --comp <type> --create-sql / --sql-file / ...
│
├── 添加多组件 + 联动（≥2图）
│     → multi_chart_linkage.py（省 80% 步骤）
│
├── 删除单个/部分组件（必须先确认）
│     → 用户给了名称且唯一：直接 comp_ops.py delete ... --name <名称>（无需先 list）
│       用户给了类型且页面只有 1 个该类型：直接 comp_ops.py delete ... --type <类型>
│       ⚠️ 名称/类型不唯一（如说"删饼图"但页面有 3 个 JPie / 多个组件同名）：
│         必须先 comp_ops.py list 让用户指认 ID，再 --id 删；禁止盲删导致误删
│       批量多类型：comp_ops.py delete ... --types "JPie,JRing,JAntvGauge"（逗号分隔，1 次 HTTP）
│       批量多名称：comp_ops.py delete ... --names "饼图1,柱图2"
│       名称不确定时才先 list，再 comp_ops.py delete ... --id <组件ID>
│
├── 清空所有组件（必须先确认）
│     → bi_utils.query_page(page_id)                     # 加载元数据
│       bi_utils._page_components[page_id] = []
│       bi_utils.save_page(page_id)
│
├── 切换全屏配色（命名色板，与产品 UI "配色" 下拉一致）
│     → style_ops.py set-palette --name <名称>    # 独立操作
│       或 spec_builder spec 顶层 "palette":"<名称>"   # 建屏/迭代时内嵌
│       可选：默认/复古/淡雅/未来/渐变/简洁/商务/柔和/科技/明亮/经典/清新/活力/火红/轻快/灵动
│       自动处理：option.color + customColor + 清除 series 硬编码 color；
│       默认按 y/x 轮转色板起点，--no-rotate 则所有图从 color[0] 起
│       查色值：style_ops.py list-palettes（无需 API/token）
│
├── 批量修改所有组件属性（如隐藏标题/改颜色/改渐变）
│     ⚠️ Step 0 — 组件清单来源优先级（决定是否跳过 query_page）：
│       1. 本会话刚写的 spec JSON / 刚 query_page 的返回值 → 直接用，跳过 query
│       2. 否则 query_page 拿当前清单
│       3. 拿到 unique(c['component']) 集合后，对 references/bi-comp-option-config.md
│          或 references/<comp-group>-option-config.md 定点搜"<CompType>"
│       ⛔ 禁止对整个 references/ 广义 grep "渐变/gradient/color/字体" ——
│          会扫到 99 个无关组件的文档（如 JCurrentTime / JStatsSummary / JOrbitRing
│          / JListProgress / JScrollList / JTabToggle），浪费上下文且延迟决策。
│
│     → 正确修改模式（query_page 返回值取组件，不能从 _page_components 取）：
│       page = bi_utils.query_page(page_id)
│       comps = page.get('template', [])                  # 从返回值取，非 _page_components
│       if isinstance(comps, str): comps = json.loads(comps)
│       for comp in comps: <修改 comp['config']>
│       bi_utils._page_components[page_id] = comps       # 写回缓存
│       bi_utils.save_page(page_id)
│
├── 修改组件配置（标题/颜色/数据/位置）
│     🚨 Step 0 — 先确认字段名（强制预检）：
│       上下文已有该组件 config → 直接看；字段不确定 → 查 bi-comp-option-config.md 对应 section
│
│     Step 1 — 选执行方式（字段名确认后再选）：
│
│       ┌─ 纯赋值（1个或多个字段，无条件判断/计算/循环）
│       │    → comp_ops.py edit --set（支持嵌套路径和数组下标 series[0].top）
│       │    ⚠️ "上下文已有 config"不是写临时脚本的理由——有 config 也用 comp_ops.py edit
│       │    ⚠️ --set 路径从 config 起算，禁止加 config. 前缀；x/y/w/h/componentName 例外写顶层名
│       │
│       └─ 需要 Python 逻辑（条件判断 / 计算值 / 循环遍历）
│            → 临时脚本
│
├── 组件群组/解组
│     → group_ops.py
│
├── 添加联动/钻取
│     → linkage_ops.py（读 references/linkage-drill-guide.md）
│
├── 添加外链/自定义 JS
│     → link_ops.py
│
└── 批量修改样式
      → style_ops.py（10 个子命令）：
        show-colors（看当前色） / set-title-color / set-axis-color / set-grid-color / set-legend-color
        set-font-size / set-bg-all / set-palette / list-palettes
        batch-edit（任意 config 路径赋值，--path/--value/--type/--name 过滤）
```

---

### D. 数据绑定（给已有组件换数据源）

> **📌 绑定前必读**：`references/data-binding-mapping.md`（两套映射机制：顶层 dataMapping vs 组件自带 option.fieldMap/header.key）——否则绑了也不显示数据。

> **🚨 一律走 `dataset_ops.py bind` / `bind-batch`，禁止手写临时 `.py` 直接改 `cfg['dataType']=2 / dataSetId / dataMapping`**。原因：脚本封装了 4 项**前端必读**的字段元信息回填（`option.columns` JCommonTable 列定义、`fieldOption` UI 字段下拉、`paramOption`、`dataSetIzAgent / dataSetMethod / dataSetApi`），靠 `getAllChartData` 拿真实 API 字段名 fallback。手写绑定漏写 → JCommonTable 表头/表体全空（`useTableBiz.ts:339` 直接读 `config.option.columns`，缺失时 `columns=[]`）。UI 复制组件能显示是因为 `dataSetCompService` 在保存时回填，**API 路径不会触发前端的回填逻辑**——这是 AI 最容易踩的"看似都改了实则缺关键字段"陷阱。

> **🚨 ≥2 个组件绑定一律用 `dataset_ops.py bind-batch`，禁止 shell 并行调多次 `bind`**。每次 `bind` 都是「query → 改 target → 整页 save」，并发会互相覆盖快照，导致**非 target 组件的 option 出现脏写**（实测：JRingProgress 的 `valueFontSize` 被改成 38、`lineHeight` 被改成 0，KPI 数值不显示）。`bind-batch` 一次 query → 内存改 N 个 target → 一次 save 彻底规避。

**易混脚本对照（防止选错）**：

| 脚本 | 作用 | 何时用 |
|------|------|--------|
| `dataset_ops.py` | 创建/绑定 **数据集**（SQL/API/JSON 等数据集对象） | 大屏组件取数主入口；自写 Java API 也走这里 `create-api`；多组件绑定走 `bind-batch` |
| `datasource_ops.py` | 配置 **数据源连接**（JDBC/NoSQL/Redis/ES/MongoDB） | 数据集底层缺 DB 连接时新建连接 |
| `linkage_ops.py` | 给**已有大屏**加联动/钻取（点 A 筛 B） | 大屏已存在，只想加交互 |
| `multi_chart_linkage.py` | **一次性建多图 + 联动**（省 80% 步骤） | 新建多图同时配联动 |
| `link_ops.py` | 组件外链跳转 + **自定义 JS 拦截器**（jsConfig） | 点击跳外部链接 / 前置 JS 逻辑 |
| `yapi_ops.py` | YApi mock 接口的创建 / 高级 mock 脚本（advmock） | 数据来源是 YApi |
| `files_ops.py` | Excel/CSV 文件数据集 | 用户上传文件做数据源 |
| `proc_ops.py` | 数据库存储过程作为数据集 | 数据来源是 SP |

| 数据源类型 | 脚本 | 参考文档 |
|----------|------|---------|
| YApi mock 接口 | `yapi_ops.py`（`create-mock` / `create-mock-batch` / `set-advmock`） | `references/api-dataset-examples.md` |
| YApi mock + 联动/钻取（按参数分支返参） | `yapi_ops.py create-mock --advmock-script/--advmock-file` 或 `set-advmock`；数据集用 `dataset_ops.py create-api --params` | `references/linkage-drill-guide.md` §API 数据集联动 |
| SQL 数据集 | `dataset_ops.py` | `references/dataset-guide.md` |
| 文件数据集（Excel/CSV） | `files_ops.py` | — |
| 存储过程 | `proc_ops.py` | — |
| 自写 Java API | `dataset_ops.py create-api`（接口注册）；底层连接由 `datasource_ops.py` | `references/pitfalls.md` §自写API |
| 绑定字段映射（单组件） | `dataset_ops.py bind`（类型 A `--mapping` / B.1 `--field-map` / B.7 `--header-keys`） | **`references/data-binding-mapping.md`** |
| 多组件批量绑定 | `dataset_ops.py bind-batch --batch-file <items.json>`（一次 save，避免并行 race） | 同上 |

---

### E. 其他操作

| 场景 | 脚本/文档 |
|------|---------|
| 弹窗 Modal | `references/popup-guide.md` |
| 地图数据（查省份/上传 GeoJSON/添加地图组件） | `map_ops.py`（子命令：`list` / `check` / `upload` / `edit` / `delete` / `add-map`） + `references/map-static-data.md`（数据格式速查） |
| 字典数据（CRUD + 绑数据集字段） | `dict_ops.py`（子命令：`list` / `items` / `create` / `add-item` / `delete` / `bind`） |
| 全 99 组件演示 | `gen_all_comps.py` |
| 遇到奇怪问题 | `references/pitfalls.md` |

---

## 按需加载文档（场景触发才读）

| 场景 | 文件 |
|------|------|
| **写 spec（默认）** | `references/spec-builder.md` |
| **数据集绑定字段映射**（接 API/SQL/文件到组件） | `references/data-binding-mapping.md` |
| **BI 直连 Online 表/设计器表单/Online 报表**（`dataType=4`） | `references/bi-mode-online.md` |
| 示例 mock API（92条） | `references/api-dataset-examples.md` |
| SQL 数据集详细流程 | `references/dataset-guide.md`（用脚本时无需读） |
| 自写 Java API 接口 | `references/pitfalls.md` §自写API |
| 地图静态数据（省份GDP/飞线） | `references/map-static-data.md` |
| 复杂联动/钻取 | `references/linkage-drill-guide.md` |
| 弹窗 Modal | `references/popup-guide.md` |
| 页面配置详细 | `references/page-config-guide.md` |
| spec-builder.md 不够细 | `references/comp-group-*.md`（分类文档） |
| 兜底组件 option 细节 | `references/bi-comp-option-config.md` |
| 遇到奇怪问题 | `references/pitfalls.md` |

---

## bi_utils 核心规则（仅手写 Python 时参考）

```python
bi_utils.API_BASE = 'http://...'
bi_utils.TOKEN    = '...'

PAGE_ID = bi_utils.create_page('名称', style='bigScreen', theme='dark',
                               background_image='/img/bg/bg4.png')   # 返回字符串，禁止 resp['id']
bi_utils._page_components[PAGE_ID] = []     # 必须缓存（否则 add 会覆盖）

bi_utils.add_component(PAGE_ID, 'JBar', '标题', x, y, w, h, config=cfg)
# 组件字段：comp['i']=UUID, ['componentName']=中文, ['component']=compType
# 图层：template[0]=最顶层，新增组件 insert(0, comp)

# query_page 返回 page 对象，组件在 page['template']，不在 _page_components
# 要修改已有组件必须从返回值取：page = bi_utils.query_page(ID); comps = page['template']
# 修改后写回：bi_utils._page_components[ID] = comps，再 save_page
bi_utils.query_page(PAGE_ID); bi_utils.save_page(PAGE_ID)
```

---

## 高频踩坑 Top 12（spec_builder 未覆盖 / 仅直调脚本时需留意）

| 问题 | 规则 |
|------|------|
| **猜测表名** | SQL 前必须 SHOW TABLES（onl_drag_page 不是 jimu_drag_page） |
| **create_page 返回值** | 字符串 page_id，禁止 `resp['id']`（TypeError） |
| **add_component 漏缓存 template** | `bi_utils._page_components[ID]=[]` 必须在 add 前（手写脚本时；spec_builder 已内置） |
| **dataMapping.filed 拼写** | 是 `filed`（少 d） |
| **SQL 含 FreeMarker `${}`** | 禁止 bash 命令行传递（被 shell 消费）→ 用 `--sql-file` |
| **SQL 多级钻取** | 禁用多条 drillData → 用单参数编码值方案（见 linkage-drill-guide.md） |
| **Windows 编码** | 所有 py 执行加 `PYTHONIOENCODING=utf-8`；脚本 print 禁用 emoji |
| **仪表/水球 value 语义** | JAntvGauge/JLiquid/JRingProgress/JColorGauge 的 value 均为 **0-100 数字**（78 = 78%）；传 0-1 小数会被当成 <1%，指针贴 0。速查 `references/spec-builder.md` §3.5 |
| **颜色字段统一用 16 进制** | 平台颜色选择器输入是 16 进制（`#RRGGBB` 或 `#RRGGBBAA`），写 `rgba()`/`hsla()` 会被识别为无效并 fallback 红色 `#FF0000`。透明用 `#FFFFFF00` |
| **JText 在 spec_builder 里写文字 / 样式 — 全用 spec 顶级字段** | 平台前端 text.vue:164-168 从 `config.option.body.*` 取值，**但 spec_builder 的 `handle_JText` 自己组装 `option.body`**——只读 spec **顶级**的 `text`（或 `title`）/ `color` / `fontSize` / `fontWeight` / `align` / `letterSpacing` / `fontStyle` / `fontFamily` / `marginLeft` / `marginTop`。spec 写 `option.body.color`/`option.color`/`data:[{"value":"标题"}]`/`option.body.text` 这些**仿前端直觉的位置 handler 全不读** → 渲染默认色板 + 14px + 空字符串（标题"看不见"）。spec_builder 已加双层防呆：检测 spec.option / spec.option.body 内的已知字段 + spec.data[0].value / spec.option.body.text 自动迁移到顶级并打印警告（实测 2026-04-28），但**正解还是直接写顶级**。bi_utils 直调时用 `add_text(page_id, text=..., color=..., fontSize=..., ...)` helper 而不是 `add_component('JText', config={...})`。同类规则适用 JNumber/JCountTo 的样式字段。规则 #8 一致：先看 `defaults/<CompType>.json` 再写字段路径 |
| **绑数据集禁止手写脚本绕过 `dataset_ops.bind` / `bind-batch`** | 实测 2026-04-27：JCommonTable 在 `dataType=2` 时**列定义完全来自 `config.option.columns`**（commonTable/hooks/useTableBiz.ts:336-358 — `let allCol = config?.option?.columns; let showCol = allCol.filter(izShow==='Y');` 缺失 → `columns=[]` → 表头/表体全空白）；同类需要"字段元信息回填"的还有 `fieldOption / paramOption / dataSetIzAgent / dataSetMethod / dataSetApi`。`dataset_ops.py _apply_binding`（dataset_ops.py:614-659）已封装：getAllChartData fallback 取字段 → 写 `option.columns` + `fieldOption` + 清空静态 chartData。手写脚本只改 `dataType/dataSetId/dataSetName/dataMapping` 看似全了实则缺 columns，**前端 UI 复制组件能显示是因为 `dataSetCompService` 在保存时回填，API 路径不会触发**。规则：≥1 个组件绑 API/SQL 数据集 → `dataset_ops.py bind` 单组件 / `bind-batch` 多组件，不要在临时 .py 里直接改 `cfg['dataType']=2` |
| **JScrollList 表头/单元格字段名易按 Vue/React 习惯写错** | 实测：列名字段是 **`fieldMapping[*].name`**（不是 `label`，写错→表头列名空白）；表头/单元格字色字段是 **`fontColor`**（不是 `color`，写错→字色失效用默认白）；单元格字色不在 `option.row` 而在每列 `fieldMapping[*].textStyle.fontColor`（`option.row` 只配背景色 `backgroundColor / alternateBackgroundColor / height / marginBottom`，没有字色字段）；表头底色 `option.header.backgroundColor` 加 `88` 等 alpha 会半透明，与 bg4 深空背景混叠后表头几乎看不见 → **想要稳定表头观感请用不透明 `#RRGGBB`**。spec_builder.handle_JScrollList 已加防呆：检测 `label` 自动改写 `name`、`option.header.color` 自动改写 `fontColor` 并打印警告。真相源 `references/scroll-list-option-config.md` + `defaults/JScrollList_3.json`，规则 #8 一致：先看 defaults 再写字段名 |

> 完整踩坑见 `references/pitfalls.md`。被 spec_builder 自动消除的（chartData 序列化、透明 bg、颜色、pie xAxis、compareState、ECharts 轴样式、命名色板、布局约束预警）不再单列。变体写法见上方"变体（variant）写法"。

---

## 高频命令模板速查（写参数前抄这里）

> 决策树告诉你选哪个脚本，这里给完整命令模板。只挑参数最容易写错的 6 个高频场景。

**1. 迭代替换（删旧+加新+换色板，1 次 HTTP）**
```bash
cat > /tmp/iter.spec.json <<'EOF'
{
  "page": {"name": "<可选>"},
  "palette": "科技",
  "delete": {"types": ["JPie","JRing"]},
  "components": [ {...仅新增组件...} ]
}
EOF
python3 \
  references/scripts/spec_builder.py <API> <TOKEN> /tmp/iter.spec.json --page-id <PAGE_ID>
```

**2. 批量删多类型 / 多名称（1 次 HTTP）**
```bash
# 多类型（逗号分隔，禁止空格，禁止单引号包字符串）
python3 references/scripts/comp_ops.py delete \
  --api <API> --token <TOKEN> --page-id <PAGE_ID> \
  --types "JPie,JRing,JAntvGauge"

# 多名称（中文需用双引号包整个值）
python3 references/scripts/comp_ops.py delete \
  --api <API> --token <TOKEN> --page-id <PAGE_ID> \
  --names "饼图1,柱图2"
```

**3. 切换全屏命名色板（禁止 AI 自编色值）**
```bash
# 查可用色板（不调 API）
python3 references/scripts/style_ops.py list-palettes

# 切配色（默认按 y/x 轮转色板起点）
python3 references/scripts/style_ops.py set-palette \
  --api <API> --token <TOKEN> --page-id <PAGE_ID> --name 复古
# 加 --no-rotate 让所有图都从 color[0] 起
```

**4. SQL 数据集绑定（含 ${} FreeMarker 必走 --sql-file）**
```bash
# 先 SHOW TABLES 确认表名（强制规则 #4）
# SQL 含 ${var} 占位符时禁止命令行传，会被 shell 消费
cat > /tmp/q.sql <<'EOF'
SELECT name, value FROM onl_drag_page WHERE tenant_id = ${tenantId}
EOF

python3 references/scripts/dataset_ops.py create-sql \
  --api <API> --token <TOKEN> --name "我的数据集" --sql-file /tmp/q.sql \
  --db-source <DS_CODE>
```

**5. 多图新建+联动（一次完成）**
```bash
# multi_chart_linkage 适合：从 0 建 ≥2 张联动图
# linkage_ops 适合：已有屏的图加联动
python3 references/scripts/multi_chart_linkage.py \
  --api <API> --token <TOKEN> --page-id <PAGE_ID> \
  --spec /tmp/multi_linkage.spec.json
```

**6. YApi 高级 mock（按参数分支返参，支持联动/钻取）**
```bash
# 高级 mock 脚本走 --advmock-file（含 JS 逻辑，避免 shell 转义）
python3 references/scripts/yapi_ops.py create-mock \
  --project-id <PID> --path /api/sales/trend --method GET \
  --advmock-file /tmp/advmock.js
```

> **环境约定（按本机情况调整）**：
> - **Python 解释器**：示例统一写 `python3`（Unix 通用）。Windows 用户改为 `py`（或本机已配的 Python 3 路径）。脚本要求 Python ≥ 3.10（用了 `dict | None` 等语法）
> - **本地 API 走代理**：若本机 HTTP 代理拦截 `127.0.0.1`/`localhost` 导致 502，命令前加 `no_proxy="127.0.0.1,localhost"`（macOS/Linux）或 `set no_proxy=127.0.0.1,localhost &&`（Windows）
> - **Windows 中文输出乱码**：所有命令前加 `set PYTHONIOENCODING=utf-8 &&`

---

## Step 4：输出结果

```
预览地址：
{API_BASE}/drag/share/view/{id}?token={TOKEN}&tenantId=<TENANT_ID>
耗时：约 Xs
```
脚本开头 `t0=time.time()`，结尾 `print(f'耗时: {time.time()-t0:.1f}s')`。
