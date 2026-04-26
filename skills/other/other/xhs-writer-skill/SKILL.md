---
name: xhs-writer
description: >-
  生成小红书(RedNote)笔记：把主题或用户提供的素材(文字/图片/视频)做成一套竖版卡片(图文)
  或一段带分镜脚本的视频稿(视频)，配 caption + hashtags，落盘到 output/小红书/。
  使用时机：用户说 写小红书 / 做小红书笔记 / 小红书图文 / 小红书种草 / 出一套 xhs 卡片 /
  小红书视频 / write a Xiaohongshu note / make a RedNote post。
---

# xhs-writer — 小红书笔记生成

把一个主题 + (可选)用户素材，生成**图文卡片组**或**短视频脚本**，按规范落盘到 `output/小红书/`。

## 核心理念

小红书读者看的不是长文，是**卡片组**或**短视频**。长文原稿只是中间产物；caption 只是发布配文。

- **图文帖(image post)**：3-9 张 9:16 竖版卡片(cover + content × N + ending)，每张 ≤80 字中文。
- **视频帖(video post)**：一段 15-90 秒竖屏视频脚本 + 封面卡，分镜写在 `meta.json.shots` 里，视频合成本 skill 不做。

### 爆款方法论（通用原则）

**5大核心原则**：
1. **真实素材优先**：项目截图、对比图、演示图 > 纯 AI 生图
2. **聚焦核心卖点**：用公式判断优先级（见 Step 0.5）
3. **素人感设计**：纯色背景 + 大 emoji + 口语化 > 品牌宣传风格
4. **痛点导向**：说"能解决什么问题" > 堆砌功能列表
5. **快速迭代**：V1(60分) → 用户反馈 → V2(70分) → 持续优化

**详细方法论**：见 `references/xiaohongshu-viral-methodology.md`

## 工作流

按顺序执行。**不要跳步**。

### Step 0 — Intake(必问，一次问完)

收到请求后不要动手，先向用户确认以下要点，尽量一条消息问完：

1. **主题 / 目标读者 / 核心观点**
2. **输出形态**：图文 or 视频？(默认图文)
3. **素材**：有没有已有的文字/图片/视频要用？贴路径或拖文件
4. **风格**：简约清新 / 科技感 / ins 风 / 商务 / 文艺复古 / 可爱卡通(默认"简约清新")
5. **卡片数量 / 视频时长**：图文默认 5-7 张；视频默认 30-60 秒

### Step 0.5 — 卖点/亮点分析（推荐执行）

**触发条件**：
- 推广类：产品、项目、工具、服务
- 分享类：好物推荐、经验总结、知识科普
- 测评类：产品对比、使用体验

**执行**：
1. 列出所有功能/特性/亮点
2. 用 AskUserQuestion 让用户打分（每个点）：
   - 稀缺性（1-5）：别人有吗？独特吗？
   - 实用性（1-5）：能解决多大问题？
   - 可感知（1-5）：用户能直接看到/感受到吗？
3. 计算得分 = 稀缺性 × 实用性 × 可感知
4. 排序，选择 Top 1-2 作为核心卖点/亮点

**输出**：
```markdown
## 卖点/亮点分析结果

| 点 | 稀缺性 | 实用性 | 可感知 | 得分 | 优先级 |
|---|---|---|---|---|---|
| 亮点A | 5 | 5 | 5 | 125 | 🥇 核心 |
| 亮点B | 2 | 3 | 3 | 18 | 🥉 辅助 |

**核心卖点/亮点**：亮点A（聚焦这个，其他作为辅助）
```

**参考**：`references/xiaohongshu-viral-methodology.md` 第2节

### Step 1 — 素材清点(有素材才做)

如果用户提供了素材路径，**先跑脚本生成清单**，再由 AI 用多模态能力填描述：

```bash
python3 scripts/analyze_material.py <path>... \
  --out <work-dir>/reference/materials.json \
  --frames-dir <work-dir>/reference/frames
```

脚本只做确定性预处理(分类、取分辨率/时长、抽帧)。AI 随后用视觉能力 **打开** `materials.json` 里每条 image/frame，填 `caption` 和 `usage`(cover / content-N / ending / reference)。详见 [`references/material-intake.md`](references/material-intake.md)。

**素材分类（按价值排序）**：
1. **对比图**（最有价值）：before/after、input/output、不同版本对比
2. **功能演示**：界面截图、操作流程图、效果展示
3. **数据图表**：性能对比、用户增长、功能覆盖
4. **品牌素材**：Logo、配色方案、官方截图

**素材使用策略**：
- ✅ **优先级**：真实素材 > 图生图 > 代码叠加 > 纯 AI 生图
- ✅ **对比图**：用图生图（保留真实感 + 叠加小红书风格文字）
- ✅ **纯文字卡片**：用 AI 生图（素人感设计）
- ❌ **避免**：所有卡片都用纯 AI 生图（缺少真实感）

**参考**：`references/xiaohongshu-viral-methodology.md` 第3节

### Step 2 — 采集外部参考(观点类 / 资讯类必做；纯素材驱动可跳过)

按 [`references/reference-search.md`](references/reference-search.md) 执行，结果写入同一 `reference/` 目录。核心数据 ≥2 个来源交叉验证。

### Step 3 — 写长文原稿(2000-4000 字)

从 H2 开始(**不写 H1**；标题入 `meta.json.title`)。写完**先给用户看**，确认主旨再继续，不要直接跳到卡片/分镜。反模式清单以 [`references/humanizer-zh.md`](references/humanizer-zh.md) 为准。

### Step 4 — 去 AI 化

读 [`references/humanizer-zh.md`](references/humanizer-zh.md) 五层原则，完整扫描重写原稿，给出质量评分(满分 50)。

### Step 4.5 — 图生图处理（有真实素材时必做）

**触发条件**：Step 1 发现了对比图、功能演示等高价值素材

**工具**：gpt-image-2 图生图（需要 OpenAI API key）

**执行**：
```python
# 使用本项目的 image_generator
import sys
sys.path.insert(0, '~/.claude/skills/xhs-writer-skill/scripts')
from image_generator import GptImage2Generator

generator = GptImage2Generator(aspect_ratio="9:16")

# 图生图：保留真实素材 + 叠加小红书风格文字
generator.generate_scene_image(
    scene_data={
        'index': 1,
        'image_prompt': """Based on the reference image, create a Xiaohongshu style card, 9:16 vertical.

Keep the original image visible.

Add overlays:
- Top: "{标题}"
- Bottom: "{引导文字}"

Style:
- Keep original clear
- Casual Xiaohongshu style
- Authentic feel"""
    },
    output_path='output.jpg',
    size='auto',
    reference_image_path='material.jpg'
)
```

**Prompt 模板**：见 `references/xiaohongshu-viral-methodology.md` 附录C

**失败处理**：
1. 重试 1 次
2. 降低图片分辨率（max 1024px）
3. 改用代码叠加文字（`scripts/text_on_image.py`）

### Step 5 — 分发：图文 or 视频

#### 5A. 图文帖：拆成 3-9 张卡片

- 结构：`cover`(第 1 张) + `content`(中间若干) + `ending`(最后 1 张)
- 每张 ≤80 字(`title` + `content` 合计，代码点计数)
- 一张卡只讲一个论点；数字 / 对比 / 金句优先上卡
- 全套卡片 emoji 风格与配色保持一致

每张卡选一种 **合成策略**(写入 `cards[i].synthesis_strategy`)，五选一。详见 [`references/material-intake.md`](references/material-intake.md)：

| strategy | 适用 | 工具 | 优先级 |
|---|---|---|---|
| `img2img` | 有真实素材（对比图/演示图） | gpt-image-2 图生图 | 🥇 最佳 |
| `text_on_photo` | 有 1 张合适照片 + 一句钩子 | `scripts/text_on_image.py` | 🥈 次选 |
| `collage` | 有 2-4 张互补照片 | `scripts/collage_3x4.py` | 🥉 可用 |
| `pure_text` | 无素材，纯文字卡 | AI 生图（素人感） | ✅ 常用 |
| `ai_generated` | 概念图 / 数据图 | 用户自备 t2i 服务 | ⚠️ 慎用 |

**策略选择原则**：
- ✅ 有真实素材 → 优先 `img2img`（保留真实感）
- ✅ 纯文字卡片 → 用 `pure_text`（素人感设计）
- ❌ 避免所有卡片都用 `ai_generated`（广告感强）

素材有水印 → 先跑 `scripts/crop_watermark.py` 或按 [`references/image-sourcing.md`](references/image-sourcing.md) 处理。

#### 5B. 视频帖：写分镜脚本

- 写 6-12 个分镜，每镜 2-8 秒，累计时长对齐用户预期
- 每镜含：`narration`(口播，≤30 字)、`on_screen_text`(屏幕字，≤15 字)、`visual`(画面描述)、`material_ref`(若引用 `materials.json` 里某条素材)
- 仍要出一张 `cover` 卡(3:4)作为封面；视频本体由用户侧工具合成，本 skill 只产脚本

字段结构见 [`references/meta-schema.md`](references/meta-schema.md) 的 `shots[]` 定义。

### Step 6 — caption + hashtags + 标题

**标题生成（5种公式）**：
1. **痛点+解决方案**：`{具体痛点}？{解决方案}`
   - 适用：有明确痛点的工具/产品
2. **提问式**：`有没有那种{功能描述}的{产品类型}？`
   - 适用：新工具推荐、功能发现
3. **发现式**：`我发现了个宝藏！{核心价值}`
   - 适用：兴奋分享、好物推荐
4. **热点词**：`{热点词}爆火后，我用它做了{场景}`
   - 适用：蹭热点、技术类产品
5. **身份共鸣**：`{身份标签}必备！{核心功能}`
   - 适用：有明确目标人群的产品

**参考**：`references/xiaohongshu-viral-methodology.md` 附录F

**caption**：
- 100-300 字，hook 开头(数字/提问/惊叹) → 关键信息 → 行动号召(点赞/收藏/关注)
- 带 emoji，闺蜜语气
- **结构**：痛点共鸣 → 解决方案 → 具体功能 → 真实案例 → CTA
- **避免**：堆砌功能、正式文案、广告感

**hashtags**：
- 5-8 个，与主题强相关
- **核心标签**（4个）：热点词 + 核心功能 + 差异化卖点 + 目标人群
- **辅助标签**（4个）：场景词 + 品类词
- 避免 `#生活` 等过度泛化标签

只写进 `meta.json`，**不**粘进卡片或正文

### Step 7 — 落盘

目录与命名规则见 [`references/output-spec.md`](references/output-spec.md)。

```
output/小红书/{YYYY-MM-DD}/{短标题}_{YYYYMMDDHHmm}/
├── {完整标题}.md        # 长文原稿
├── meta.json            # 元数据(卡片 / 分镜 / caption / hashtags / materials)
├── images/              # (图文)最终卡图 / (视频)封面
└── reference/           # materials.json / 搜索结果 / summary / 思考过程
```

目录短标题与时间戳**必须**走脚本标准化，别手写：

```bash
python3 scripts/normalize_slug.py "原始长标题" --with-ts
```

`meta.json` 完整字段定义见 [`references/meta-schema.md`](references/meta-schema.md)。

### Step 8 — 校验(强制)

写完 `meta.json` 后必须跑：

```bash
python3 scripts/validate_meta.py <work-dir>/meta.json
```

非 0 退出 → 读报错修 `meta.json` 再跑，直到 clean。不要把未校验的产物交给用户。

## 不要做的事

- 不写 H1；标题只放 `meta.json.title`
- 不在正文末尾写"参考来源 / References"；只落到 `reference/`
- 不在 `.md` 里留 `【插入图片：...】` 占位符；图片同步下载 + 引用相对路径
- 不跳过 Step 4(去 AI 化)和 Step 8(validate)
- 不自己手算目录名 / 时间戳，一律走 `normalize_slug.py`

---

## 工具依赖

### 必需工具
- Python 3.8+
- PIL (Pillow)

### 可选工具
- OpenAI API key（用于图生图，推荐）
  - 配置：在 `~/.claude/skills/xhs-writer-skill/.env` 填入 `OPENAI_API_KEY`
  - 没有 API key 也能用，会生成纯文字卡片

### 图生图使用
```python
# 添加路径
import sys
sys.path.insert(0, '~/.claude/skills/xhs-writer-skill/scripts')
from image_generator import GptImage2Generator

# 初始化
generator = GptImage2Generator(aspect_ratio="9:16")

# 生成
generator.generate_scene_image(
    scene_data={'index': 1, 'image_prompt': '...'},
    output_path='output.jpg',
    size='auto',
    reference_image_path='material.jpg'  # 图生图模式
)
```

---

## 参考资料

### 核心方法论
- **`references/xiaohongshu-viral-methodology.md`**：完整爆款方法论
  - 卖点优先级判断公式
  - 素材使用策略（优先级排序）
  - 爆款卡片结构（标准6-7张）
  - 文案公式库（5种标题公式）
  - 视觉风格指南（素人感 vs 精美设计）
  - 图生图 Prompt 模板（3种场景）
  - 常见错误清单（5大错误 + 解决方案）
  - 工具使用指南

### 其他参考
- `references/humanizer-zh.md`：去 AI 化原则
- `references/material-intake.md`：素材处理流程
- `references/image-sourcing.md`：图片来源处理
- `references/meta-schema.md`：元数据字段定义
- `references/output-spec.md`：输出目录规范

---

## 快速开始

### 场景1：推广产品/项目

```bash
# 用户说："帮我推广这个项目 /path/to/project"

# Step 0.5: 卖点分析
# → 列出功能，让用户打分（稀缺性×实用性×可感知）
# → 选出核心卖点

# Step 1: 素材盘点
# → 扫描项目截图、对比图、演示图
# → 分类：对比图（最有价值）> 功能演示 > 其他

# Step 4.5: 图生图
# → 对比图用图生图（保留真实感 + 小红书风格）
# → 纯文字卡片用 AI 生图（素人感）

# Step 6: 生成标题（5个选项）
# → 痛点式、提问式、发现式、热点词、身份共鸣

# 输出：6-7张卡片 + caption + hashtags
```

### 场景2：好物分享/经验总结

```bash
# 用户说："写一条关于 XX 好物推荐的小红书笔记"

# Step 0: Intake
# → 确认主题、目标读者、输出形态

# Step 0.5: 亮点分析
# → 这个好物的核心亮点是什么？

# Step 1: 素材盘点
# → 产品图、使用场景图、效果对比图

# Step 3-4: 写长文 + 去 AI 化

# Step 5: 拆成卡片
# → 封面（提问/发现式）+ 亮点展示 + 使用场景 + 真实体验 + CTA

# 输出：5-7张卡片 + caption + hashtags
```

### 场景3：知识科普/教程

```bash
# 用户说："写一条关于 XX 知识的小红书笔记"

# Step 0: Intake
# → 确认主题、目标读者、知识点

# Step 2: 采集外部参考
# → 搜索相关资料，交叉验证

# Step 3-4: 写长文 + 去 AI 化

# Step 5: 拆成卡片（纯文字）
# → 用 AI 生图（素人感设计）
# → 结构：封面 + 核心概念 + 步骤/要点 + 注意事项 + CTA

# Step 6: caption + hashtags

# 输出：5-7张卡片 + caption + hashtags
```

---

## 常见问题

### Q1：什么时候用图生图？
**A**：有真实素材（对比图、演示图、截图）时优先用图生图。效果：真实感 > 代码叠加 > 纯 AI 生图。

### Q2：如何判断卖点优先级？
**A**：用公式 `优先级 = 稀缺性(1-5) × 实用性(1-5) × 可感知(1-5)`，选择得分最高的 1-2 个作为核心卖点。

### Q3：封面选哪种风格？
**A**：
- 有明确痛点 → 痛点式
- 新工具推荐 → 提问式
- 好物分享 → 发现式
- 蹭热点 → 热点词式
- 明确人群 → 身份共鸣式

### Q4：图生图失败怎么办？
**A**：三级降级策略
1. 重试 1 次
2. 降低图片分辨率（max 1024px）
3. 改用代码叠加文字（`scripts/text_on_image.py`）

### Q5：需要多少张卡片？
**A**：
- 最少：3张（封面 + 核心卖点 + CTA）
- 标准：6张（封面 + 卖点 + 功能 + 人群 + 案例 + CTA）
- 完整：7张（+ 开源地址/官方链接）

---

**更新时间**：2026-04-25
**适用场景**：产品推广、好物分享、知识科普、经验总结、测评对比等各类小红书内容
