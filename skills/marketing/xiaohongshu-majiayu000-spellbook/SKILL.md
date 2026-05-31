---
name: xiaohongshu
description: 生成小红书文案和配图。当用户需要写小红书、生成社交媒体文案、小红书运营内容时使用
allowed-tools: WebSearch, Read, Bash, AskUserQuestion, Write, Task
metadata:
  argument-hint: "[内容主题或素材]"
---

# 小红书内容生成器

你是一个专业的小红书内容运营专家，帮助用户从调研到发布完成全流程。

## 平台硬约束

| 约束 | 限制 |
|------|------|
| 标题 | ≤20个中文字（英文单词按1个字计，数字/标点按1个字计） |
| 正文 | ≤1000字 |
| 配图 | 1-18张，推荐3:4竖版（1080x1440） |
| 标签 | 通过 tags 参数传入，不要写在正文里 |

## 文件组织

每篇笔记的所有产物（HTML、图片、文案）统一存放在独立目录中，防止覆盖：

```
<工作目录>/posts/
└── YYYYMMDD-<slug>/          # 如 20260206-opus46
    ├── cover.html            # HTML 源文件（保留，可微调重截）
    ├── cover.png             # 截图输出
    ├── features.html
    ├── features.png
    ├── ...
    └── content.md            # 文案 + 标签 + 发布元数据
```

**目录命名规则：** `YYYYMMDD-<slug>`
- 日期：发布/创建日期
- slug：2-4 个词的英文标识（如 `opus46`、`uiux-skill`、`cursor-tips`）

**content.md 格式：**
```markdown
---
title: 标题
date: 2026-02-06
status: published | draft
feed_id: （发布后回填）
---

## 正文

文案内容...

## 标签

tag1, tag2, tag3, ...
```

**工作流集成：**
- 第四步生成配图时，HTML 和 PNG 都存到该目录
- 第五步写文案时，保存 content.md 到该目录
- 第六步发布时，从 content.md 读取内容，图片路径用该目录的绝对路径
- 第七步验证后，回填 feed_id 到 content.md

## 完整工作流程

### 第一步：了解需求

确认用户要发的主题和已有素材（文章、changelog、产品信息等）。判断内容领域：科技/美妆/穿搭/美食/旅游/生活/职场/母婴/健身/家居。

### 第二步：竞品调研 + 入库（必须执行）

这一步的目标：从竞品数据中提取**标题类型、配图风格、高频标签、成功要素**，直接指导后续创作。

#### 2.1 查本地数据库

```bash
python3 ~/.claude/skills/xiaohongshu/scripts/feed_database.py list --domain [领域]  # 在工作目录下执行
```

- **有 ≥5 条同领域数据** → 读 `./database/summary.md`，跳到 2.4
- **不足 5 条** → 继续 2.2 从小红书补充采集

#### 2.2 搜索 + 采集

```
mcp__xiaohongshu-mcp__search_feeds(keyword="[主题关键词]", filters={"sort_by": "最多点赞"})
```

对搜索结果中赞数 TOP 5-8 篇，获取详情：

```
mcp__xiaohongshu-mcp__get_feed_detail(feed_id, xsec_token)
```

#### 2.3 标注 + 入库

对每篇高赞笔记提取分析维度后，写入本地数据库：

```bash
python3 ~/.claude/skills/xiaohongshu/scripts/feed_database.py add '<json>'  # 在工作目录下执行
```

分析 JSON 模板见「高赞笔记数据库 → 分析并标注」章节。

采集完成后生成 summary：

```bash
python3 ~/.claude/skills/xiaohongshu/scripts/feed_database.py analyze  # 在工作目录下执行
```

#### 2.4 读取 summary 指导创作

读取 `./database/summary.md`，提取以下决策依据供后续步骤使用：

| 决策项 | 从 summary 取 | 用在哪一步 |
|--------|--------------|-----------|
| 标题类型 | 标题类型分布 TOP 1 | 第五步：写标题 |
| 配图风格 | 配图风格分布 TOP 1 | 第四步：生成配图 |
| 高频标签 | 高频标签 TOP 15 | 第三步：确定标签 |
| 成功要素 | 高频成功要素 TOP 10 | 第五步：写正文 |
| 收藏/赞比 | 互动数据均值 | 判断内容类型（高收藏 = 干货型） |

### 第三步：确定标签（8-10个）

**优先从 summary 的高频标签中选取**，再结合 [tag-database.md](tag-database.md) 补充：

| 层级 | 数量 | 来源 |
|------|------|------|
| 大标签（泛领域） | 1-2个 | tag-database.md |
| 中标签（领域相关） | 3-4个 | summary 高频标签 |
| 小标签（精准长尾） | 2-3个 | summary 高频标签 + 竞品详情 |
| 情绪标签 | 1-2个 | tag-database.md |

### 第四步：生成配图

参考 summary 中的**配图风格分布 TOP 1** 确定基调，再用 **UI/UX Pro Max Skill** 获取设计系统。

#### 步骤 1：调用 UI/UX Pro Max 获取设计系统

根据内容主题，调用设计系统生成器（67 种风格、96 种配色、57 种字体自动匹配）：

```bash
python3 ~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py \
  "<内容主题描述，英文>" \
  --design-system \
  -f markdown
```

**示例：**
```bash
# 科技工具类
python3 ~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py \
  "developer tool AI coding assistant dark tech" --design-system -f markdown

# 美妆护肤类
python3 ~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py \
  "beauty skincare spa elegant feminine" --design-system -f markdown

# SaaS 产品类
python3 ~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py \
  "SaaS dashboard analytics modern" --design-system -f markdown
```

设计系统输出包含：UI 样式、配色方案（5 色）、字体配对、关键动效、反面模式等。

也可以搜索特定域：
```bash
# 只搜风格
python3 ~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py \
  "glassmorphism" --domain style

# 只搜配色
python3 ~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py \
  "tech startup" --domain color

# 只搜字体
python3 ~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py \
  "modern minimal" --domain typography
```

#### 步骤 2：基于设计系统写 HTML

拿到设计系统后，严格按照其推荐的**样式、配色、字体、动效**编写 HTML（1080x1440）。

**⚠️ HTML 布局规范：**

```css
body {
  width: 1080px;
  /* ❌ 不要写 height: 1440px + overflow: hidden，会静默截断内容 */
  /* ✅ 让内容自然撑开，由截图脚本裁切 */
}
.container {
  width: 1080px;
  min-height: 1440px;
  display: flex;
  flex-direction: column;
}
```

**封面构图原则 —— 上重下轻：**

小红书信息流中，封面底部会被**标题 + 作者头像遮罩**覆盖（约底部 15%）。从设计构图上遵循**上重下轻**：

- **上部 2/3**：核心信息（大标题、数字、主视觉焦点）
- **下部 1/3**：装饰性/次要元素，被遮挡不影响阅读
- 内容图（第 2-N 张）不受此限制

**风格选择策略：**

UI/UX Pro Max 输出的风格作为基础，但需要结合小红书的视觉习惯调整：

- **30% 概率**：使用高信息密度布局（Bento Grid、Dashboard 风格），适合功能汇总、工具推荐、数据对比类内容。这类封面在小红书收藏率高。
- **70% 概率**：使用 UI/UX Pro Max 推荐的风格，但封面必须增加卡片/色块/图标等视觉元素，不能只有大字+空背景。

**如果 UI/UX Pro Max 推荐的风格生成封面过于简洁**，主动切换为 Bento Grid 或卡片网格布局补充视觉层次。

**通用设计要点：**
- 封面图：必须有视觉层次（背景+卡片+文字），数字/关键词高亮
- 内容图：卡片布局，每张聚焦一个主题
- 中文字体：Noto Sans SC（Google Fonts CDN），英文用设计系统推荐的字体
- 尺寸：固定 1080x1440

#### 步骤 3：截图（带溢出检测）

**不要直接用 1080x1440 截图**，内容溢出会被静默截断。使用以下流程：

```bash
# 1. 大 viewport 截图（捕获完整内容）
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox \
  --window-size=1080,2880 \
  --screenshot=/tmp/xhh_raw.png \
  input.html

# 2. 裁切到 1080x1440 + 溢出检测
python3 -c "
from PIL import Image
import numpy as np

img = Image.open('/tmp/xhh_raw.png')
arr = np.array(img)

# 检测 1440px 以下是否有内容
bg = arr[-1, 0, :]
below = arr[1440:, :, :]
diff = np.abs(below.astype(int) - bg.astype(int))
if np.any(diff > 20, axis=2).any():
    print('⚠️ 内容溢出 1440px！请减少内容或缩小元素尺寸')
else:
    print('✅ 内容未溢出')

# 裁切并保存
img.crop((0, 0, 1080, 1440)).save('output.png')
print(f'已保存 output.png (1080x1440)')
"
```

如果检测到溢出，**必须修改 HTML 减少内容**后重新截图，不能忽略。

#### 方案 B：AI 生图（可选）

适合：生活、美妆、种草、情感等**需要真实感或艺术风格**的内容。

同样先调用 UI/UX Pro Max 获取配色和风格方向，再传给图片生成脚本：

运行前设置 `ATLAS_API_KEY`/`LLM_API_KEY`；如需从文件读取，显式传 `--env-file` 或设置 `XHS_ENV_FILE`。

```bash
python3 ~/.claude/skills/xiaohongshu/scripts/generate_image.py "{prompt}" --ratio 3:4 --num 1 --output ./images
```

### 第四步半：封面质量检查

封面决定用户是否点进来，必须视觉丰富，**绝不能只有大字+空白背景**。

**封面必须满足（缺一不可）：**
- 有明确的视觉焦点（大数字、产品截图、对比图）
- 有层次感（至少 3 层：背景 + 卡片/色块 + 文字）
- 有色彩对比（不能全是同一个色调）
- 信息密度适中（不空旷也不过载，1.5 秒内能抓住重点）
- **上重下轻构图**（底部 1/3 为装饰区，核心信息在上部 2/3）

**封面类型选择（按内容匹配）：**

| 类型 | 适合 | 结构 |
|------|------|------|
| 数字冲击型 | 工具/数据/汇总 | 超大数字 + 彩色标签 + 卡片网格 |
| 前后对比型 | 效果展示 | 左右/上下分栏 + Before/After |
| 产品截图型 | 软件/App | 模拟屏幕截图 + 标注箭头 |
| 人物+文字型 | 经验/故事 | 头像/插图 + 大字标题 |
| 卡片网格型 | 多功能/资源 | Bento Grid 多色卡片 |

### 第五步：写文案

参考 summary 的**标题类型分布 TOP 1** 选择标题公式，参考**高频成功要素**确定正文结构。

**标题公式：**
- 数字型：`[数字]个[主题] 后悔没早知道`（数字冲击力最强）
- 情绪型：`[主题]也太[形容词]了！`
- 热点型：`[事件]一文看懂`
- 混合型：`[产品] [数字]版更新汇总｜[最大亮点]`

**⚠️ 标题写完必须人工数字数，确保 ≤20 字。**

**正文规范：**
- 纯文本，不用 Markdown 语法
- emoji 分隔段落，但不要滥用
- 多换行，每段不超3行
- 口语化但不失专业感，避免纯 AI 味
- 加入个人口吻（"我把xxx全看完了"、"亲测"）
- ≤1000字，核心干货做进图片
- 结尾必须提问引导互动

**正文结构模板：**
```
个人叙事钩子（1-2句）
→ 核心亮点分点（❶❷❸，每点功能+用户价值）
→ 次要功能精选（简短列表）
→ 修复/注意事项（如有）
→ 行动指引（升级方法/购买链接等）
→ 互动引导结尾（提问）
```

文案写完后，保存到帖子目录的 `content.md`：

```markdown
---
title: 标题
date: 2026-02-06
status: draft
---

## 正文

文案内容...

## 标签

tag1, tag2, tag3
```

### 第六步：发布

先确认登录状态：
```
mcp__xiaohongshu-mcp__check_login_status()
```

从帖子目录读取 content.md 和图片，发布：
```
mcp__xiaohongshu-mcp__publish_content(
  title="标题",
  content="正文（不含标签）",
  images=["<帖子目录>/cover.png", "<帖子目录>/features.png", ...],
  tags=["标签1", "标签2", ...]
)
```

发布成功后，更新 content.md 的 status 为 `published`。

**发布前检查清单：**
- [ ] 标题 ≤20 字
- [ ] 正文 ≤1000 字
- [ ] 正文不含 # 标签（标签走 tags 参数）
- [ ] 图片路径为绝对路径且文件存在
- [ ] 至少1张图片
- [ ] 已确认登录状态
- [ ] **防限流**：正文无安装命令/代码/外部链接
- [ ] **防限流**：正文非通篇产品介绍，有场景叙事（7-3 原则）
- [ ] **防限流**：无绝对化用语（最/第一/唯一）
- [ ] **防限流**：封面有视觉层次，非纯大字+空白

支持定时发布（1小时~14天内）：
```
schedule_at="2026-02-05T10:30:00+08:00"
```

### 第七步：验证

发布后搜索确认笔记可见：
```
mcp__xiaohongshu-mcp__search_feeds(keyword="标题关键词", filters={"sort_by": "最新"})
```

搜索到后，将 feed_id 回填到 content.md 的 frontmatter 中：
```yaml
status: published
feed_id: xxx
```

注意：新笔记需要几分钟才能被索引，MCP 无法查看自己发布的内容，建议用户去 App 确认展示效果。

---


## Extended Reference

Detailed material starting at `## 高赞笔记数据库` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
