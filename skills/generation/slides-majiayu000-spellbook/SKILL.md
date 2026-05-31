---
name: slides
description: 生成口播视频背景 PPT 幻灯片（16:9 横版 PNG 序列）。当用户需要做 PPT、生成幻灯片、做演示背景图时使用
allowed-tools: WebSearch, Read, Bash, Write, Edit, Glob, Grep, Task, AskUserQuestion
metadata:
  argument-hint: '[主题或讲稿文件路径]'
---

# PPT 幻灯片生成器

你是一个演示文稿设计专家，支持两种模式：

| 模式 | 用途 | 页数 | 复杂度 |
|------|------|------|--------|
| **口播模式**（默认） | 口播视频背景 | 20-40 页 | 极简（纯文字居中） |
| **演示模式** | 独立 PPT 展示 | 5-8 页 | 复杂（卡片+装饰+图标） |

**判断逻辑**：
- 用户提到"口播""视频背景""讲稿""script""视频 PPT" → 口播模式
- 用户提到"演示""presentation""展示""信息图" → 演示模式
- 不确定时 → 口播模式（更常用）

---

# 口播模式（Voiceover）

一页一观点，颜色即层级，零装饰。配合口播视频使用。

## 内容类型（决定封面和前 3 页策略）

口播视频分 4 种类型，**类型不同，封面和开头页的视觉策略完全不同**：

| 类型 | 判断依据 | 封面理性钩重点 | slide_01-02 策略 |
|------|---------|--------------|-----------------|
| **人物型** | 围绕某人的观点/经历/访谈 | 必须包含人物最知名身份 | 专门一页展示身份标签（大字） |
| **教程型** | 教用户怎么做某件事 | 突出方法/配方 | 展示痛点场景 |
| **新闻型** | 报道产品/事件更新 | 突出产品名+核心变化 | 展示核心数字/事实 |
| **观点型** | 输出个人看法/总结 | 突出金句/观点 | 展示引发思考的问题 |

### 人物型的「身份优先」规则（极其重要）

人物型视频的核心卖点是**「谁说的」而非「说了什么」**。观众因为这个人的身份才点进来。

**身份标签选择 —— 用目标受众最有辨识度的称呼：**

| ❌ 正式但没人认识 | ✅ 圈内都知道的 |
|------------------|---------------|
| PSPDFKit 创始人 | 龙虾作者 |
| Segment 联合创始人 | 32亿美金被收购那哥们 |
| Anthropic Research | Claude 背后的团队 |
| Peter Steinberger | 龙虾作者 Peter |

**判断方法**：这个称呼发到目标受众的群里，大部分人能不能立刻知道是谁？如果不能，换一个更通俗的。

**硬规则：**
1. **封面理性钩**必须包含人物身份标签（最知名的那个）
2. **slide_01 或 slide_02** 必须有专门一页展示身份（用 `vo-stat` 或 `vo-big` + `vo-tech` 高亮）
3. 如果人物有多个身份，选**目标受众最熟悉**的那个，其他身份可以在后续页补充
4. 讲稿里提到的人物别称/昵称**原样保留**到幻灯片，不要替换成正式名称

## 设计系统

CSS 文件：`/Users/lifcc/Desktop/code/work/life/xhh/design-system-voiceover.css`

每页 HTML 只引用这一个 CSS：

```html
<link rel="stylesheet" href="file:///Users/lifcc/Desktop/code/work/life/xhh/design-system-voiceover.css">
```

### 背景主题（13 种，自动选择）

**暗色渐变系（白字）：**

| 主题 | body class | 视觉 | 适用 |
|------|-----------|------|------|
| warm（默认） | `vo-warm` | 暖黑渐变 | 大多数内容 |
| cool | `vo-cool` | 冷蓝渐变 | 技术/理性内容 |
| aurora | `vo-aurora` | 极光紫绿渐变 | AI/前沿内容 |

**纯色浸染系（白字，适合系列化内容）：**

| 主题 | body class | 视觉 | 适用 |
|------|-----------|------|------|
| indigo | `vo-indigo` | 深靛蓝 | 深度分析、蓝调 |
| wine | `vo-wine` | 暗酒红 | 情感、争议话题 |
| teal | `vo-teal` | 深松绿 | 效率、方法论 |
| forest | `vo-forest` | 深森林 | 自然、成长话题 |

**彩色渐变系（白字，高视觉能量）：**

| 主题 | body class | 视觉 | 适用 |
|------|-----------|------|------|
| ocean | `vo-ocean` | 紫→蓝→青 | 产品发布、激励 |
| sunset | `vo-sunset` | 暗红→深橙→棕 | 热点事件 |
| violet | `vo-violet` | 蓝→紫→品红 | 创意、前沿 |

**浅色系（黑字）：**

| 主题 | body class | 视觉 | 适用 |
|------|-----------|------|------|
| paper | `vo-paper` | 米白底 + 顶部品牌色条 | 观点输出、生活、非技术 |

**特殊效果系：**

| 主题 | body class | 视觉 | 适用 |
|------|-----------|------|------|
| neon | `vo-neon` | 纯黑底，关键词霓虹发光 | 震撼数据、科技评测 |
| glass | `vo-glass` | 暗底 + 模糊光斑 + 毛玻璃卡片 | 产品介绍、高级感内容 |

**主题自动选择规则（不要每次都用 warm）：**
1. 检查最近 3 套幻灯片用了什么主题（`ls voiceover/*/slide_01.html | tail -3` 然后读 body class）
2. 不连续重复同一主题
3. 暗色和浅色交替出现（连续 3 套暗色后必须用 paper 或 neon）
4. 根据内容匹配：技术→cool/neon，AI→aurora/violet，观点→paper/wine，教程→teal/indigo

### 布局（2 种）

| 布局 | body class | 效果 | 适用 |
|------|-----------|------|------|
| 居中（默认） | 无需额外 class | 文字居中对齐 | 大多数内容 |
| 左对齐叙事 | `vo-left`（叠加） | 文字左对齐 + 左侧竖线 | 故事讲述、案例分析 |

布局与背景自由组合，如 `<body class="vo-paper vo-left">`。

### 文字层级

| CSS 类 | 效果 | 用途 |
|--------|------|------|
| `vo-main` | 76px 白色粗体（paper 下为黑色） | 主文字（每页至少 1 行） |
| `vo-sub` | 44px 灰色 | 次要文字/补充说明 |
| `vo-big` | 96px（叠加在 vo-main 上） | 封面/转场大标题 |
| `vo-small` | 34px（叠加在 vo-sub 上） | 备注小字 |
| `vo-gap` | margin-top: 28px | 主文字→灰色文字切换时加，拉开层次 |
| `vo-stat` | 220px 品牌色（Space Grotesk） | 大数字冲击（数据页用） |
| `vo-stat-unit` | 72px 半透明 | 数字单位（配合 vo-stat） |

### 6 种语义颜色（叠加在 vo-main 上，自动加粗）

| CSS 类 | 颜色 | 用途 | 使用时机 |
|--------|------|------|---------|
| `vo-pain` | #FF6B8A 粉红 | 痛点/情感/负面 | 开头铺垫 |
| `vo-solution` | #FFD666 黄色 | 方案/结论/惊叹 | 揭示方案时 |
| `vo-tech` | #5CC8FF 青蓝 | 工具名/技术名/产品名 | 提到具体工具时 |
| `vo-step` | #B088F9 紫色 | 步骤编号/分类标签 | "第一步""第二步" |
| `vo-positive` | #4AEABC 绿色 | 正面结论/成果 | 展示效果时 |
| `vo-cta` | #E6613E 橙色 | 互动引导/号召行动 | 结尾互动 |

注意：`vo-paper` 和 `vo-neon` 主题下语义色会自动调整（浅色主题用深色版本，霓虹主题加发光效果），无需手动处理。

### HTML 模板

每页 HTML 结构固定，只需替换 body class（主题+布局）和 vo-slide 内容：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="file:///Users/lifcc/Desktop/code/work/life/xhh/design-system-voiceover.css">
</head>
<body class="vo-warm">
  <div class="vo-slide">
    <p class="vo-main">主文字</p>
    <p class="vo-main vo-pain">彩色强调</p>
    <p class="vo-sub vo-gap">灰色补充</p>
    <p class="vo-sub">更多补充</p>
  </div>
</body>
</html>
```

## 拆页规则（核心）

| 规则 | 说明 |
|------|------|
| 每页最多 6 行 | 宁可多页也不要挤 |
| 每行最多 18 个中文字 | 超长必须换行 |
| 一个观点一页 | 不要把两个观点放一页 |
| 每页彩色最多 2 种 | 白+一种彩色，或灰+一种彩色 |
| 保持口语化 | 不要把讲稿书面化 |
| 总页数 20-40 页 | 对应 3-8 分钟视频 |

### 前 3 页策略（按内容类型）

前 3 页决定观众是否继续看。不同内容类型的前 3 页结构不同：

**人物型（必须在 slide_01-02 建立身份）：**

```
slide_01: 身份标签页（大字）
  例：vo-main vo-tech "龙虾作者" + vo-sub "Peter Steinberger"
  或：vo-stat "20+" vo-stat-unit "年" + vo-main vo-tech "iOS 老兵"
slide_02: 核心行为/观点（引出正题）
  例：vo-main "去年把工具全换成了" + vo-main vo-solution "AI驱动"
```

**教程型：**
```
slide_01: 痛点场景（引起共鸣）
slide_02: 解决方案预告（制造期待）
```

**新闻型：**
```
slide_01: 核心事实/数字（冲击力）
slide_02: 为什么重要（和观众的关系）
```

**观点型：**
```
slide_01: 引发思考的问题
slide_02: 反直觉的答案
```

### 颜色节奏（整套幻灯片的颜色分布）

```
开头 2-3 页  → vo-pain（铺垫痛点，引起共鸣）
引出方案     → vo-solution（转折，揭示答案）
工具/技术    → vo-tech（提到具体工具时）
步骤详解     → vo-step（"第一步""第二步"）
正面结论     → vo-positive（展示效果/成果）
结尾互动     → vo-cta（"你们学会了吗"）
其他补充     → vo-sub（灰色，不抢注意力）
```

## 封面系统（视频缩略图）

封面是视频在小红书信息流中的缩略图，直接决定点击率。**封面 ≠ slide_01**，封面是专门设计的标题卡。

### 封面三层结构（理性钩 → 感性钩 → 降门槛钩）

| 层级 | CSS 类 | 字号 | 作用 | 示例 |
|------|--------|------|------|------|
| L1 理性钩 | `vo-cover-title` | 52px | 说清楚是什么 | "用Claude Code实现一键生成PPT" |
| L2 感性钩 | `vo-cover-hook` | **160px** | 巨大情绪词，视觉焦点 | **"懒人配方"** |
| L3 降门槛 | `vo-cover-sub` | 38px | 暗示人人可用 | "普通人用CLAUDE CODE超神" |

**感性钩是封面的核心**，字号是理性钩的 3 倍，用渐变色。

### 封面钩子颜色

| 叠加类 | 渐变色 | 适用 |
|--------|--------|------|
| （默认，不加类） | 黄→橙→品牌色 | 方法论/配方/公式/万能 |
| `vo-cover-hook-tech` | 青→蓝→紫 | 技术/工具/产品 |
| `vo-cover-hook-positive` | 绿→青绿 | 效率/成果/正面 |
| `vo-cover-hook-pain` | 粉→红→品红 | 情感/争议/FOMO/焦虑 |

### 封面装饰

| 元素 | CSS 类 | 效果 |
|------|--------|------|
| 右上角 L 括号 | `vo-cover-deco-tl` | 淡金色角线 |
| 左下角 L 括号 | `vo-cover-deco-br` | 淡金色角线 |
| 底部装饰线 | `vo-cover-line` | 品牌色渐隐线 |
| 背景增强 | `vo-cover-bg-boost`（加在 body） | 中心微暖光晕 |

### 封面 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="file:///Users/lifcc/Desktop/code/work/life/xhh/design-system-voiceover.css">
</head>
<body class="vo-warm vo-cover-bg-boost">
  <div class="vo-slide vo-cover">
    <div class="vo-cover-deco-tl"></div>
    <div class="vo-cover-deco-br"></div>
    <p class="vo-cover-title">用Claude Code实现一键生成PPT</p>
    <p class="vo-cover-hook">懒人配方</p>
    <p class="vo-cover-sub">普通人用CLAUDE CODE超神</p>
    <div class="vo-cover-line"></div>
  </div>
</body>
</html>
```

### 感性钩的提取规则

从讲稿中提取封面三层文字（**按内容类型区分**）：

**通用规则：**

| 层级 | 提取方法 | ❌ 错误 | ✅ 正确 |
|------|---------|---------|--------|
| 理性钩 | 视频核心做了什么（一句话） | "Claude Code Skill教程" | "用Claude Code一键生成PPT" |
| 感性钩 | 2-4字情绪词（最好有比喻/夸张） | "PPT生成器" | "懒人配方" |
| 降门槛 | 暗示普通人也行的一句话 | "适合所有人" | "普通人用CLAUDE CODE超神" |

**人物型封面特殊规则：**

理性钩**必须包含人物身份**，感性钩聚焦观点/行为的情绪点：

| 层级 | ❌ 没有身份 = 没人点 | ✅ 身份前置 = 有点击 |
|------|---------------------|---------------------|
| L1 理性钩 | "一个iOS开发者的AI工作流" | "**龙虾作者**20年iOS老兵的AI工作流" |
| L2 感性钩 | "工作流分享" | "极简到离谱" |
| L3 降门槛 | "适合所有开发者" | "只用两样工具" |

**自检**：遮住感性钩和降门槛，只看理性钩 —— 能不能知道视频在讲谁？如果只看到"一个开发者""某位大佬"，就是不合格。

**感性钩常用词库（2-4字）**：

| 类型 | 词库 |
|------|------|
| 方法论 | 懒人配方、万能公式、一招搞定、降维打击 |
| 效率 | 效率拉爆、直接起飞、省一整天、十倍速 |
| 震撼 | 太猛了、真的炸、绝了、离谱 |
| FOMO | 别错过、快上车、还不知道？、落后了 |
| 情感 | 救命了、终于等到、爽到飞起、泪目 |


## Extended Reference

Detailed material starting at `## 工作流程` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
