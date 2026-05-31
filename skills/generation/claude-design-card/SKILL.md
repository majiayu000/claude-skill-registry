---
name: claude-design-card
description: |
  将任意文本、网页或 URL 生成符合 Claude/Anthropic 设计语言的 HTML 信息卡片，通过 Playwright 截图为 PNG。
  支持 14 种格式：平台封面（公众号、视频号、B站、抖音）、图文内容卡（小红书、教程、对比分析）、
  社交分享卡（金句、数据、方形）、长文编辑排版（Broadsheet、Feature、Reader、Digest）。
  当用户提到「信息卡、卡片、封面、图文笔记、排版、截图、生成图、内容卡」时使用本技能。
---

# claude-design-card

将内容转成符合 Claude/Anthropic 设计语言的 HTML 卡片，并通过 Playwright 截图为 PNG。
核心目标：用统一的设计系统让每种格式都有专属的排版气质，而不是换色皮肤。

## Claude 设计语言

所有卡片必须**只使用**以下 token，不引入任何外部颜色：

### 颜色 Token

| Token | 值 | 用途 |
|---|---|---|
| \`--pg\` Parchment | \`#f5f4ed\` | 主背景色 |
| \`--iv\` Ivory | \`#faf9f5\` | 卡面/次背景 |
| \`--nk\` Near-Black | \`#141413\` | 正文、标题 |
| \`--ds\` Dark-Surface | \`#30302e\` | 深色区块背景 |
| \`--tc\` Terracotta | \`#c96442\` | 强调色、CTA、装饰 |
| \`--og\` Olive-Gray | \`#5e5d59\` | 副文本、说明 |
| \`--sg\` Stone-Gray | \`#87867f\` | 元信息、占位 |
| \`--bc\` Border-Cream | \`#f0eee6\` | 细分隔线 |
| \`--bw\` Border-Warm | \`#e8e6dc\` | 暖色分隔 |
| \`--ws\` Warm-Silver | \`#b0aea5\` | 深色背景上的副文本 |

### 字体规则

\`\`\`css
/* 标题：衬线，中等粗细，绝不使用 font-weight: 700 */
font-family: Georgia, 'Times New Roman', serif;
font-weight: 500;

/* 正文/UI：系统无衬线 */
font-family: -apple-system, system-ui, sans-serif;

/* 正文行高：书籍级 */
line-height: 1.60;

/* Kicker/标签：全大写，小字号，字间距 */
font-size: 9px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase;
\`\`\`

### 字号参考（按格式和平台缩放）

\`\`\`css
/* 格式族 A — 平台封面 */
/* 公众号首图 900×383: 主标题 44-64px，标题视觉占比 28-36% */
/* B站/YouTube 1280×720: 主标题 64-92px，标题视觉占比 32-42% */
/* 视频号 1080×1440: 主标题 76-108px，标题视觉占比 30-40% */
/* 抖音/故事 1080×1920: 主标题 76-104px，标题视觉占比 28-34% */

/* 格式族 B — 图文内容卡 1080×1440 */
/* 主标题: 64-96px, 承接句: 26-34px, 正文块: 24-30px, 元信息: 16-20px */

/* 格式族 C — 社交分享卡 1080×1080 */
/* 主标题: 48-72px, 正文: 18-24px */

/* 格式族 D — 长文编辑排版 800px 以下 */
/* 主标题: 32-40px, 正文: 17px, 副文本: 13px */
\`\`\`

### 阴影规则

\`\`\`css
/* 只用环形阴影，不用传统投影 */
box-shadow: 0px 0px 0px 1px rgba(0,0,0,0.08);

/* 卡片外容器 */
box-shadow: rgba(0,0,0,0.08) 0 4px 24px;
\`\`\`

**禁止**：任何冷色调蓝灰（如 \`#64748b\`）、纯白背景（用 \`#faf9f5\`）、\`font-weight: 700\`。

---

## 格式族与尺寸

选格式的逻辑是：**内容类型 → 平台 → 尺寸**，不是「好看不好看」。

### 格式族 A — 平台封面

平台封面是「点击前承诺」，不是文章摘要。只允许三层信息：主判断标题、一句承接承诺、一个证据点。

| 格式 | 尺寸 px | 比例 | 平台场景 | 构图逻辑 |
|---|---|---|---|---|
| 公众号首图 | 900 × 383 | 2.35:1 | 微信公众号题图 | 横向秒读：左标题，右证据/装饰 |
| 视频号竖封面 | 1080 × 1440 | 3:4 | 微信视频号封面 | 竖版海报：中心标题，上下节奏 |
| B站/YouTube 横封面 | 1280 × 720 | 16:9 | B站/YouTube 封面 | 缩略图路牌：大关键词 + 单视觉钩子 |
| 抖音全屏竖版 | 1080 × 1920 | 9:16 | 抖音/快手/故事 | 全屏停顿：安全区内一个判断 |

### 格式族 B — 图文内容卡

图文内容卡是「可保存的知识物件」，不是摘要 PPT。首图负责停留，内页负责理解，工具页负责收藏。

| 格式 | 尺寸 px | 比例 | 场景 | 默认美学模式 |
|---|---|---|---|---|
| 小红书图文笔记 | 1080 × 1440 | 3:4 | 小红书主图/轮播 | Editorial Artifact + Dark Magazine Cover |
| 步骤教程卡 | 1080 × 1440 | 3:4 | 教程类内容 | Practical Toolkit |
| 对比分析卡 | 1080 × 1440 | 3:4 | 对比/竞品分析 | Editorial Artifact |

### 格式族 C — 社交分享卡

| 格式 | 尺寸 px | 比例 | 场景 | 气质关键词 |
|---|---|---|---|---|
| 金句分享卡 | 1080 × 1080 | 1:1 | 语录/引文传播 | 大号引言符 + 极简 |
| 数据大字卡 | 1080 × 1080 | 1:1 | 数字/统计突出 | 超大数字 + 说明 |
| 方形通用卡 | 1080 × 1080 | 1:1 | 通用社交分享 | 标准单栏，灵活 |

### 格式族 D — 长文编辑排版

| 格式 | 宽度 px | 高度 | 气质 | 适合内容 |
|---|---|---|---|---|
| The Broadsheet | 800 | auto | 三栏报纸 + 版刻装饰 | 时事评论、周报 |
| The Feature | 760 | auto | 暗头 + 非对称双栏 | 深度报道、特稿 |
| The Reader | 720 | auto | 单栏 + 边注 Marginalia | 随笔、书评、文化评论 |
| The Digest | 760 | auto | 摘要框 + 数据列 | 研究报告、行业分析 |

长文编辑排版截图时使用自动高度模式（\`--full-page\`）。

---

## 格式选择决策表

| 内容类型 | 首选格式 | 备选格式 | 关键确认点 |
|---|---|---|---|
| 金句 / 语录 | 金句分享卡 | 方形通用卡 | 有没有来源要标注 |
| 教程 / 步骤 | 步骤教程卡 | 小红书图文笔记 | 几个步骤，是否要截图 |
| 数据 / 统计突出 | 数据大字卡 | The Digest | 数字多还是文字多 |
| 对比 / 竞品 | 对比分析卡 | The Feature | 几组对比，单双列 |
| 长文摘要 / 观点 | The Feature | 小红书图文笔记 | 读者还是传播 |
| 新闻 / 评论 | The Broadsheet | The Feature | 字数多不多 |
| 随笔 / 散文 | The Reader | The Feature | 有没有注释需要 |
| 研究 / 分析报告 | The Digest | 对比分析卡 | 数据量 |
| 视频内容 | 视频号竖封面（默认） | B站/YouTube 横封面 | 先问平台：微信 or B站/YouTube |
| 公众号配图 | 公众号首图 | 视频号竖封面 | 是否作为题图 |
| 抖音/故事 | 抖音全屏竖版 | — | 是否要保留品牌 |

---

## 先问再做

先分析内容，再给用户 **1 个主推荐 + 2 个备选格式建议**，不要一上来就生成 HTML。

### 触发问答的规则

- 只要存在明显不确定性，就先问，不要猜。
- 只要用户偏好会改变格式、构图或节奏，就先问。
- 只要输入信息不足以稳定选主推荐，就先问。
- 不要把问答理解成阻塞，而要理解成降低试错成本。

### 默认交互顺序

1. 判断内容类型、信息密度和目标平台。
2. 给出 1 个主推荐 + 2 个备选，说明每个适合的原因。
3. 问最多 3 个会改变结果的关键问题（优先 1-2 个）：
   - 目标平台（微信 / 小红书 / B站 / 通用）
   - 希望阅读型还是传播型
   - 是否有品牌色要求
4. 用户确认后，进入 HTML 生成。
5. 如果用户说「按你判断」或场景已足够明确，直接生成。

### 风格建议格式

每次先给：
- 推荐格式 + 尺寸 + 适用理由（一句话说明为什么）
- 备选一 + 适用理由
- 备选二 + 适用理由
- 默认分支：如不选则按主推荐

---

## A/B 族生成契约

### A 族平台封面

生成 A 族时，先把内容压缩为：

\`\`\`text
主判断标题：一个结论 / 冲突 / 反差 / 收益
承接承诺：点进去能获得什么
证据点：数字 / 来源 / 对象 / 场景 / 对比（只能一个）
\`\`\`

禁止把 4-6 个要点放在封面上。封面负责点击，不负责讲完。

#### 抖音 / 故事安全区

抖音 / 故事不是竖版海报，而是全屏停顿设计：

- 顶部 14%：弱信息区，只放品牌、栏目、轻 kicker。
- 中部 44-52%：主阅读区，放标题和承接承诺。
- 底部 20%：弱信息区，不放关键信息。
- 右侧：避让互动按钮，不放主标题和证据点。

### B 族内容卡

B 族必须先选择美学模式：

| 模式 | 用途 | 视觉语言 |
|---|---|---|
| Editorial Artifact | 默认主模式 | 网格、编号、规则线、边注、留白，像高级编辑手册 |
| Dark Magazine Cover | 强传播首图 | 深色 surface、大标题、单个 coral 关键词、少量几何编辑标记 |
| Practical Toolkit | 教程/清单内页 | 动作标题、2-4 个步骤块、强间距、弱装饰 |

小红书轮播建议角色顺序：封面 → 背景/问题 → 框架 → 示例 → 清单 → 收束。

---

## 输入处理

| 输入类型 | 处理方式 |
|---|---|
| 纯文本 | 直接进入内容提炼 |
| URL（通用网页） | 用 \`r.jina.ai/[url]\` 抓取为 Markdown |
| \`arxiv.org/abs/\` | 先尝试 HTML 版全文，回退 PDF |
| \`mp.weixin.qq.com\` | 用 r.jina.ai 抓取，保留原文结构 |
| \`x.com\` / \`twitter.com\` | 用 \`r.jina.ai/[url]\` 抓取 |

---

## 异常处理

**每个步骤失败时的回退路径，必须遵守：**

| 异常情况 | 处理方式 |
|---|---|
| `r.jina.ai` 抓取失败（超时/403） | 告知用户并请求：「请将正文内容粘贴到对话中」，不要捏造内容 |
| 截图脚本报错（Chromium 找不到） | 提示：`bunx playwright install chromium` 后重试；同时告知 HTML 已保存路径 |
| 字体文件不存在（`assets/` 路径缺失） | HTML 降级到 `Georgia, 'Times New Roman', serif`，提示用户字体文件路径有误 |
| 内容过长（原文 > 3000 字） | 先自动压缩：只保留核心论点 + 数据 + 反转点，要点上限 6 条，不询问用户 |
| 内容过短（< 50 字） | 直接询问用户：「内容较少，是否补充背景或希望我补全创作？」 |
| 用户未回答格式确认问题（3 轮内无回应） | 直接按主推荐格式生成，在 HTML 注释中写明「按默认主推荐生成」 |

---

## 内容提炼规则

### 只保留「删掉就会损失信息」的内容

- 找核心判断，不找表面描述。
- 找具体数字、倍率、年份、金额、对比关系。
- 找因果链：A 导致 B，B 导致 C。
- 找反转点：最意外、最反直觉、最能转述的一句话。
- 控制在 4-6 个要点，超过就压缩。

### 标题规则

- 标题必须是结论，不是背景介绍。
- 标题优先用动词、数字、冲突、反差。
- 避免日记式、主题式、名词堆砌式标题。

### 封面标题规则（A/B 族优先）

- 标题必须先给判断，不给主题名。
- 优先使用：旧/新、错/对、失效/有效、隐藏/显性、为什么/怎么做。
- A 族标题只服务点击承诺；B 族首图标题服务停留和收藏。
- 标题过长时先改写，不要一味缩小字号。
- 如果标题只有 2-4 个汉字，可以放大；如果超过 14 个汉字，必须拆分或重写。

### 金句规则

- 金句必须来自原文事实或原文句子。
- 不允许为了排版好看而捏造。

### 数据规则

- 所有数字必须忠实原文。
- 不混淆 ARR、月收入、估值、样本数等不同量纲。

---

## 图表规则

只有当图比纯文本能多传递信息时才加图。

| 内容特征 | 建议图形 |
|---|---|
| 因果链 | Mermaid 流程图 |
| 步骤流程 | Mermaid 流程图 |
| 概念关系 | Mermaid 关系图 |
| 数据、趋势、比例 | 内联 SVG（见 SVG 设计系统） |
| 排版装饰、节奏分割 | 内联 SVG（见 SVG 设计系统） |
| 纯观点或纯列表 | 不加图 |

图表放在标题之后、要点之前，作为结构总览，不要抢正文。

## SVG 设计系统

SVG 不是装饰工具，是**印刷工艺的数字实现**。每个 SVG 元素必须对应一种具体的排版传统或信息功能，能清楚回答「它在这里的工作是什么」。

### 核心原则：CSS 优先

**只有当 SVG 能做 CSS 做不到的事，才使用 SVG。**

| CSS 能做到的（用 CSS） | SVG 应该做的 |
|---|---|
| 直线分隔线（border） | 带节点/菱形/圆的装饰规则线 |
| 颜色填充背景 | 网点/交叉线图案（\`<pattern>\`） |
| Unicode 引号（"…"） | 70px+ 的精确大引号（字体渲染在大尺寸时失真） |
| 箭头文字（→） | 有收笔的印刷风格指示符 |
| 纯色矩形 | 有数据意义的进度条 / 折线图 / 柱状图 |

### SVG 元素分类

按**功能**分类，而不是固定清单。Agent 可在每类中自由发挥构图，但须遵守每类的设计约束。

#### 类型 A — 排版装饰器（Typographic Ornament）

**功能**：分割视觉节奏，替代平庸的 CSS 分隔线  
**传统来源**：活字印刷版刻装饰规则（column rule, ornamental rule）  
**适用场景**：分节符、段落过渡、页眉页脚装饰

设计约束：
- 构图必须轴对称（左右或点对称）
- 中心元素颜色：terracotta \`#c96442\`；规则线颜色：warm-silver \`#b0aea5\`
- 规则线线宽 ≤ 0.8px（细如发丝，才有印刷质感）
- 中心元素形状限：菱形、圆、双圆、花边节点（fleuron）
- 整体尺寸：宽 ≤ 240px，高 ≤ 20px

禁止：箭头、星形、爆炸形、自由曲线形状

---

#### 类型 B — 大号引言符（Display Quote Mark）

**功能**：在 Pull Quote 下层置入半透明大引号，增加排版层次  
**传统来源**：出版社排版，19 世纪对开印刷传统  
**适用场景**：任何 pull quote / blockquote 区块

设计约束：
- 必须用 SVG \`<text>\` + Georgia 字体渲染（利用字体字形精度，不用手绘路径）
- 字号 70–100px，透明度 0.07–0.12
- 颜色：terracotta（内容型）或 near-black（文学型）
- 位置：\`position: absolute\` 置于引文区块左上角，\`z-index: 0\`，不遮挡正文

禁止：自定义贝塞尔路径引号（字体字形比手绘更精准）

---

#### 类型 C — 编辑插图（Editorial Illustration）

**功能**：替代空白占位图或摄影，用几何构成传达文章核心隐喻  
**传统来源**：Bauhaus、De Stijl、20 世纪杂志封面插图  
**适用场景**：长文头图、Feature 风格杂志开头的视觉「钩」

设计约束：
- 只使用基本几何形：\`circle\`、\`rect\`、\`line\`、\`polygon\`、\`polyline\`
- 颜色只用 Claude 设计 token：terracotta、near-black、stone-gray、parchment
- 透明度梯度：最深 0.6，最浅 0.06（保持轻薄层次感）
- 必须有叙事意图：构图能够解释文章核心隐喻，不能是随机几何拼接
- 必须有视觉重心（通常是一个尺寸最大或颜色最深的元素）
- 建议尺寸：宽 280–480px，高度适配内容区域

禁止：文字标签嵌入插图、写实风格、icon 库拼合

---

#### 类型 D — 数据可视化（Embedded Data Viz）

**功能**：用视觉语言替代纯数字，让量级和趋势感直觉化  
**传统来源**：编辑信息图，W Magazine 数据版式  
**适用场景**：统计型卡片数据列、分析报告数据区

设计约束：
- **折线图**：\`<polyline>\` + \`stroke-dasharray\` 动画（让数据被「读出来」，不只是展示）
- **进度条**：\`<line>\` + \`stroke-dasharray\` 动画（比 \`<rect>\` 动画流畅）
- **柱状图**：\`<rect>\` 元素，\`rx="1"\`（轻微圆角，保持温和感）
- 图例：\`font-size: 7px\`，\`font-family: system-ui\`
- 正向数据：terracotta；负向 / 对比数据：stone-gray
- 动画延迟 0.5–1.5s（让页面先稳定，再播数据动画）

禁止：饼图（视觉感知误差大）、3D 效果、渐变填充

---

#### 类型 E — 图案底纹（Pattern Texture）

**功能**：用 \`<pattern>\` 在区块背景制造印刷质感，区分内容层次  
**传统来源**：报纸印刷网点（halftone）、档案交叉线纹  
**适用场景**：侧边栏背景、摘要区块、数据列背景

设计约束：
- 只用两种基本图案：**网点**（\`<circle>\`）或**交叉线**（两条正交 \`<line>\`）
- 图案颜色只用 terracotta \`#c96442\`
- 透明度：0.05–0.08（只是「有纹理感」，绝不喧宾夺主）
- \`pattern\` 单元格：6–10px 正方形

禁止：复杂图案、多色图案、含文字的图案

---

### 约束总表

| 约束维度 | 规则 |
|---|---|
| **数量上限** | 每张卡片最多使用 3 种 SVG 类型，同类型可重复 |
| **颜色** | 只用 Claude 设计 token，不引入任何新颜色 |
| **视觉权重** | 装饰性 SVG 不超过内容区 15% 的视觉面积 |
| **动画** | 只允许 \`stroke-dasharray\` 和 \`opacity\` 动画，不用 \`transform\` 动画 |
| **无障碍** | 所有装饰性 SVG 必须加 \`aria-hidden="true"\` |
| **CSS 优先** | 凡 CSS 能做到的，不用 SVG |
| **叙事性** | 每个 SVG 元素必须能回答「它在这里的工作是什么」 |

### 使用决策流程

\`\`\`
内容有数据 / 比例 / 趋势？
  → 是：使用类型 D（数据可视化）
内容有 Pull Quote？
  → 是：使用类型 B（大号引言符）
需要视觉节奏分割点？
  → 是：使用类型 A（排版装饰器）
需要区块背景区分？
  → 是：使用类型 E（图案底纹）
Feature 风格，需要头图区域？
  → 是：使用类型 C（编辑插图）
以上都不是
  → 不加 SVG
\`\`\`

### 生成前自检

每个 SVG 元素生成前先问：
1. **CSS 能做到吗？** — 不确定就不加 SVG
2. **它的工作是什么？** — 说不清楚就删掉
3. **会喧宾夺主吗？** — 会就降低透明度或缩小尺寸
4. **颜色在 Claude token 范围内吗？** — 不在就换回 token 颜色

---

## 生成流程

### Step 1：内容提炼

输出：主标题、副标题、4-6 个要点、1 句金句、来源信息。

**QR 检测**：若用户消息中包含 URL（如 `https://...`）或明确说「附带二维码 / 扫码跳转」，
提取该 URL 记为 `QR_URL`，后续步骤中使用。否则 `QR_URL` 为空，跳过所有 QR 相关步骤。

### Step 2：选格式

根据内容类型和目标平台，选定格式族和具体格式，确认尺寸。

### Step 3：决定 SVG 元素

按 SVG 决策流程逐项判断，记录每个 SVG 元素「在这里的工作是什么」。

### Step 4：生成 HTML

生成**完整自包含** HTML 文件：
- 所有样式内联，不依赖外部 CSS / JS
- 使用本地字体（`TsangerJinKai02-W04.ttf`、`NotoSerifSC-Regular.ttf`），通过 `@font-face` 加载
- 卡片宽度与格式尺寸匹配
- 底部包含一键保存 PNG 按鈕（浏览器直接打开可用）

**字体路径规则（重要）**：`@font-face` 中的 `src: url()` 必须使用 **`file://` 绝对路径**。
相对路径在 Playwright 截图时无效（Chromium 沙笼阻止加载）。

```css
/* ✅ 正确：截图和浏览器均可用 */
@font-face {
  font-family: 'TsangerJinKai02';
  src: url('file:///绝对路径/assets/TsangerJinKai02-W04.ttf');
}
/* ❌ 错误：浏览器可用，截图时字体失效 */
@font-face {
  font-family: 'TsangerJinKai02';
  src: url('assets/TsangerJinKai02-W04.ttf');
}
```

> 完整设计规范参见 [`references/design-spec.md`](references/design-spec.md)（CSS 变量、格式尺寸、SVG 快查表）。

**QR Zone 插入（仅当 `QR_URL` 非空时）**

根据当前格式，在 HTML 正确位置插入 `#qr-zone` div。外层容器若为浮层方案需设 `position:relative`。

| 格式族 | 插入位置 | 尺寸 |
|:---|:---|:---|
| 方形卡 / 竖版卡 / 视频号 / 公众号封面 | 卡片容器内，最后一个子元素 | 80×80px |
| 小红书图文笔记 / 长图 | 卡片最底部（滚动内容之后） | 80×80px |
| The Feature 双栏 | 右侧栏内，内容最末 | 72×72px |
| The Vintage Broadsheet | article 底部 | 80×80px |

```html
<!-- 右下角浮层（方形卡 / 竖版卡 / 视频号 / 公众号）-->
<div style="display:none; position:absolute; right:12px; bottom:12px;
  flex-direction:column; align-items:center; gap:4px;" id="qr-wrapper">
  <div id="qr-zone" data-qr-size="72" data-qr-light="#F5F0E8" style="
    width:72px; height:72px; background:#141413;
    border-radius:4px; padding:4px; box-sizing:border-box;
  "></div>
  <span style="font-size:10px; color:#6B6B6B; letter-spacing:0.05em; white-space:nowrap;">扫码阅读全文</span>
</div>

<!-- 底部 footer 内嵌（footer 右侧，适合竖版卡 / 长图）-->
<div id="qr-zone" data-qr-size="72" data-qr-light="#F5F0E8" style="
  display:none; width:72px; height:72px;
  border-radius:4px; overflow:hidden;
"></div>
<!-- footer 内同时加文字标签 -->
<span style="font-size:11px; color:#6B6B6B; letter-spacing:0.05em;">扫码阅读全文</span>

<!-- 侧栏内嵌（The Feature 双栏）-->
<div id="qr-zone" data-qr-size="72" data-qr-light="#F5F0E8" style="
  display:none; margin-top:auto; padding-top:12px;
"></div>
<span style="font-size:10px; color:#888; margin-top:4px;">扫码阅读全文</span>

<!-- 底部浅色栏（The Vintage Broadsheet）-->
<div style="display:none; border-top:1px solid #c8bfa8; padding:12px 0; margin-top:16px;
  display:flex; align-items:center; gap:12px;" id="qr-wrapper-broadsheet">
  <div id="qr-zone" data-qr-size="64" data-qr-light="#F5F0E8" style="width:64px; height:64px;"></div>
  <span style="font-size:11px; color:#8B7355; letter-spacing:0.05em;">扫码阅读全文</span>
</div>
```

> **重要**：`#qr-zone` 的 `display` 由 screenshot.ts 通过 `zone.style.display = 'block'` 控制显示，CSS 规则中不要设 display；初始隐藏用包裹层（`id="qr-wrapper"`）的 `display:none` 实现，或将 `#qr-zone` inline style 设为 `display:none`（screenshot.ts 会覆盖为 `block`）。QR 颜色：`colorDark: #141413`，`colorLight` 默认 `#F5F0E8`；若卡片底色不同，在 `#qr-zone` 上设置 `data-qr-light="#你的底色"`。

### Step 5：保存 HTML 并通知用户

\`\`\`
默认路径：/tmp/claude-card-[关键词].html
\`\`\`

**保存后必须输出预览提示，然后等用户确认：**

\`\`\`
✅ HTML 已生成：/tmp/claude-card-[关键词].html
可在浏览器中打开预览。确认布局 OK 后回复「截图」，我立即生成 PNG。
如需调整（字号 / 配色 / 内容），现在告诉我。
\`\`\`

> 若用户说「截图」「继续」「OK」或静默 1 轮，直接进入 Step 6，无需再次确认。

### Step 6：截图生成 PNG

\`\`\`bash
# 固定尺寸格式（封面类、分享卡类）：
bun scripts/screenshot.ts /tmp/claude-card-[关键词].html [output.png] [width] [height]

# 长文编辑排版（自动高度）：
bun scripts/screenshot.ts /tmp/claude-card-[关键词].html [output.png] [width] --full-page

# 附带二维码（QR_URL 非空时，在命令末尾追加）：
bun scripts/screenshot.ts /tmp/claude-card-[关键词].html [output.png] [width] [height] --url [QR_URL]
bun scripts/screenshot.ts /tmp/claude-card-[关键词].html [output.png] [width] --full-page --url [QR_URL]

# 脚本内部已设置 waitForTimeout(3000)，确保 SVG 动画在截图前完成
\`\`\`

默认输出：\`/tmp/claude-card-[关键词].png\`

---

## 质量门槛

生成前过以下检查：

1. 内容是否忠实原文。
2. 标题是否真的是结论、冲突或收益，而不是主题名。
3. A 族封面是否只保留「主判断 + 承接承诺 + 一个证据点」。
4. B 族是否选择了明确美学模式（Editorial Artifact / Dark Magazine Cover / Practical Toolkit）。
5. 是否有清晰的第一眼、第二眼、第三眼。
6. 平台裁切和安全区是否正确，尤其是抖音/故事顶部、底部、右侧避让。
7. 颜色是否全部使用 Claude 设计 token（无外来色）。
8. 手机屏幕上是否可读（A/B 族不得用 16-18px 作为核心正文块）。
9. 是否过度装饰（SVG 元素超过 3 种 / 视觉权重超过 15%）。
10. 每个 SVG 元素是否都能说清楚「它的工作是什么」。
11. 是否在大屏和手机上都能直接截图（没有外部资源依赖）。
12. 是否避免了 AI 味模板：同权圆角网格、摘要幻灯片、无意义标签、所有平台只换尺寸。
