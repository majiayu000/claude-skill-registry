---
name: gpt-image2-ppt
description: Generate visually striking PPT slides via OpenAI's gpt-image-2 -- 10 curated styles (Spatial Glass / Tech Blue / Editorial Mono / Dark Aurora / Risograph / Wabi / Swiss Grid / Hand Sketch / Y2K Chrome / Retro Vector) plus a template-clone mode that mimics any user-supplied .pptx; outputs high-res slide PNGs and a 16:9 .pptx. Use when the user asks to make a presentation, slides, deck, pitch deck, investor PPT, magazine-style PPT, or 做一份 PPT / 生成幻灯片 / 用 gpt-image 生成 PPT / 按这个模板生成 PPT.
---

# gpt-image2-ppt -- 用 gpt-image-2 生成 PPT

把一份 markdown 大纲（或 `slides_plan.json`）+ 一种视觉风格，直接喂给 OpenAI 官方 Images API（`gpt-image-2`），逐页出图，最后打包成 16:9 .pptx。

## 十种内置风格

| 风格 ID | 一句话定位 | 适用场景 |
| --- | --- | --- |
| `gradient-glass` | Apple Vision OS / Spatial Glass | AI 产品发布、技术分享、创意提案 |
| `clean-tech-blue` | Stripe / Linear 级蓝白 | 融资路演、商业计划书、企业战略 |
| `vector-illustration` | 复古矢量插画 + 黑描边 | 教育培训、品牌故事、社区分享 |
| `editorial-mono` | Kinfolk / Monocle 编辑设计 | 品牌发布、文化访谈、读书分享 |
| `dark-aurora` | Linear / Vercel 深色霓虹 | AI 产品、开发者工具、技术分享 |
| `risograph` | Riso 双套色印刷 + 网点纹理 | 创意工作室、文创品牌、独立 zine |
| `japanese-wabi` | 无印 / 原研哉式侘寂 | 茶道、生活方式、奢侈品、文化讲座 |
| `swiss-grid` | Bauhaus / Vignelli 国际主义网格 | 学术报告、博物馆展陈、严肃汇报 |
| `hand-sketch` | Sketchnote / 白板手绘 | 工作坊、产品 brainstorming、培训 |
| `y2k-chrome` | Y2K 千禧液态金属 + 蝴蝶贴纸 | 潮牌、文娱、品牌联名、Z 世代营销 |

> 风格选择原则：技术类首选 `dark-aurora` / `gradient-glass`，商务类首选 `clean-tech-blue` / `editorial-mono`，文化生活类首选 `japanese-wabi` / `vector-illustration`，潮文娱类首选 `risograph` / `y2k-chrome`，学术类首选 `swiss-grid`，工作坊与早期创意类首选 `hand-sketch`。

## 模板克隆模式

直接给 skill 一个 .pptx 模板，后续所有页都仿这个模板。

```bash
# 一行：自动渲染 + 模板分析 + 出图。需本机有可用 PPTX 渲染后端
python3 scripts/generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-strict
```

`--template-strict` 表示每页都把模板对应页作为 image reference 喂给 gpt-image-2，仿真度最高。

### 模板渲染：本机不需要操作 PowerPoint

skill 自带 `render_template.py`，把 .pptx 自动渲染成每页 PNG，存到 `<cwd>/template_renders/<stem>/page-NN.png`。

### Agent 前置检查（模板克隆时必须做）

**在跑任何 --template-pptx 命令之前，你必须先检查本机是否有可用 PPTX 渲染后端。**

检查方式：

- macOS：优先检查 `/Applications/Keynote.app`，否则检查 `which libreoffice || which soffice`
- Windows：优先检查本机 PowerPoint；否则 `where libreoffice 2>nul & where soffice 2>nul`
- Linux：`which libreoffice || which soffice`

如果都没有可用后端，先告知用户模板渲染需要安装 LibreOffice，或让用户手动把模板每页导出为 `page-01.png`、`page-02.png` 后通过 `--template-images` 传入。可选安装命令：

| 平台 | 安装命令 |
| --- | --- |
| Windows | `winget install LibreOffice.LibreOffice` |
| macOS | `brew install --cask libreoffice` |
| Linux (Debian/Ubuntu) | `sudo apt-get install -y libreoffice` |
| Linux (Fedora/RHEL) | `sudo dnf install -y libreoffice` |
| Linux (Arch) | `sudo pacman -S --noconfirm libreoffice-fresh` |

装完再次检查，确认存在可用渲染后端再继续后续流程。

> 注意：Windows 上 `winget` 是 Win10/11 自带，会弹 UAC 确认框，需要用户点确认；macOS 上 `brew` 需要先安装 Homebrew。

`render_template.py` 的渲染后端按优先级自动挑：
1. **Windows**：PowerPoint COM（本机有 Office 时优先，直出 PNG，跳过 PDF 步骤）> LibreOffice
2. **macOS**：Keynote AppleScript（本机有 Keynote 时优先，直出 PNG）> LibreOffice
3. **Linux**：LibreOffice / soffice 命令
4. PDF -> PNG 走 `pymupdf`（已在 requirements）；没装就用 `pdf2image` + poppler

跑 `generate_ppt.py --template-pptx ...` 时如果省略 `--template-images` 会自动调一次渲染；也可以手动先跑一次：

```bash
python3 scripts/render_template.py company-template.pptx
# -> <cwd>/template_renders/company_template/page-01.png ... page-NN.png
```

### 仿模板的两层缓存

| 资料 | 路径 | 用途 |
| --- | --- | --- |
| 模板每页 PNG | `<cwd>/template_renders/<stem>/page-NN.png` | LibreOffice 一次渲染长期复用 |
| 模板风格分析 | `<cwd>/template_cache/<sha256>.json` 或手写 `template_profile.json` | 多模态 agent 自己看图生成；纯文本 agent 才需要外挂 vision |
| 生成产物 | `<cwd>/outputs/<timestamp>/` | 每次新跑都新目录 |

三者都在调用者 cwd 下，与项目自然同进退；建议把 `template_renders/`、`template_cache/`、`outputs/` 加进项目的 `.gitignore`。

**模板看图分析（让 agent 自己判断要不要配 `VISION_*`）**：

- **当前 code agent 本身是多模态模型**（例如 Claude Code 的多模态 Claude、Codex 的多模态 GPT）：不需要额外配置 `VISION_*`。agent 直接读取 `template_renders/<stem>/page-*.png`，按 `template_analyzer.py` 的 `TemplateProfile` 结构生成 `template_profile.json`，再用 `--template-profile template_profile.json` 传给 `generate_ppt.py`。如果要配合 `--template-strict`，每个 layout 里要写 `reference_image`（模板 PNG 的绝对路径或可访问路径）。
- **当前 code agent 是纯文本模型**（例如只接入 DeepSeek 文本模型）：它看不了模板截图，需要额外配置 `VISION_BASE_URL` / `VISION_API_KEY` / `VISION_MODEL_NAME`，让 `template_analyzer.py` 调一个独立的 OpenAI 兼容多模态端点做模板分析。

vision 分析与图片生成的 `gpt-image-2` 永远解耦——换 vision provider 不影响出图路径。

## 安装

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh --target claude   # Claude Code
# 或
bash install_as_skill.sh --target codex    # Codex
# API 直连所需密钥优先通过 agent 配置 / 系统环境变量注入
```

## 环境变量注入（API 直连时）

不要把本 skill 的密钥写进调用者业务项目根目录的 `.env`，也不要为了出图去读取用户项目里的通用 `.env`。环境变量建议按 agent 框架的标准方式注入：

- **通用 / CI / 服务器**：用系统环境变量、Docker Compose `environment` / `env_file`、Kubernetes Secret、CI Secret 等注入。
- **Claude Code**：用用户级 `~/.claude/settings.json` 或项目级 `.claude/settings.local.json` 注入环境变量；命令行环境变量优先级最高。
- **OpenClaw / 自定义 Agent**：用框架配置里的 `apiKey` / env reference 引用系统环境变量，避免把 key 明文写进项目配置。
- **本地 standalone CLI fallback**：可以设置 `GPT_IMAGE2_PPT_ENV=/path/to/private.env`，或使用 skill 安装目录下的 `.env`；这只是备用方式，不是业务项目 `.env`。

API 直连需要这些变量：

```bash
OPENAI_BASE_URL=https://api.openai.com    # 或任意 OpenAI 兼容中转站
OPENAI_API_KEY=sk-...
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_QUALITY=high                     # low / medium / high / auto

# 可选：模板克隆模式的 vision 分析 backend。
# 多模态 agent / 原生 Codex 可自己看图生成 --template-profile，不需要下面这组。
# 只有纯文本 agent（如 DeepSeek 文本模型）才需要外挂下面这组。
# 不内置默认 endpoint，请填你自己信任的服务，否则就别填。
# VISION_BASE_URL=https://your-openai-compatible-relay.example.com/v1
# VISION_API_KEY=sk-...
# VISION_MODEL_NAME=gemini-3.1-pro-preview   # 或 gpt-4o / claude-3.5-sonnet 等任意多模态 SKU
```

> **安全提示**：脚本只读取当前进程环境、平台注入的 `gpt-image2-ppt_*` 变量、显式 `GPT_IMAGE2_PPT_ENV`，以及 skill 安装目录下的 `.env` fallback。脚本**不会**向上递归读取调用者项目目录里的 `.env`，避免误吃业务项目密钥。

## 如果你就是 Codex agent（原生 image_generation 出图 — 推荐）

**如果你自己就是 Codex**（正在运行本 skill 的 agent 就是 Codex CLI / Codex TUI），并且当前环境提供 `image_generation` tool 和 ChatGPT 登录态，此时**不要用 `generate_ppt.py` 或 `--backend codex` 负责出图**，直接用原生工具生成图片，最后只复用本仓库的 md 转换 / PPTX 打包逻辑即可。

### 如何判断

你能访问 `image_generation` tool，并且不需要手动配 `OPENAI_API_KEY` 就能出图——满足这两个条件就走原生路径。若当前 Codex 会话没有这个 tool，就按普通 agent 处理：走 API 直连、`--backend codex` 备用后端，或让用户补齐环境。

### 出图流程（Codex 原生路径）

**1. 准备 slides 数据**

如果还没有 `slides_plan.json`，先按下面「生成流程」第 2-3 步写 `slides_plan.md` → `python3 scripts/md_to_plan.py ...` 转 json。

**2. 读风格模板**

读 `styles/<id>.md`，取 `## 基础提示词模板` section 作为 base prompt。

**3. 构造每页 prompt**

参考 `generate_ppt.py` 的 `generate_prompt()` 逻辑，核心规则：

- 封面（cover/slide 1）：标题/副标题为视觉焦点
- 数据页（data/最后一页）：突出关键数字、对比或结论
- 内容页（content/其余页）：按层级、对齐、留白结构化呈现
- **所有文字必须简体中文**，字体用思源黑体/苹方，严禁草书/艺术字
- **16:9 横版宽屏**（landscape, widescreen），prompt 里明确说"宽度明显大于高度、绝对不要方图"

```text
{style 基础提示词模板}

---

现在请生成本组中的【{封面页/内容页/数据页}】，{对应 hint}
本页要呈现的内容如下（请按本风格美学重新设计版式）：

{slide content}

【强制语言与字体要求】
1. 所有文字必须使用简体中文，严禁英文（专有名词除外）
2. 中文字体使用思源黑体或苹方，严禁草书、艺术字
3. 标题粗体，正文常规，字号对比清晰

【画面比例 — 强制】16:9 横版宽屏 (landscape, widescreen)，宽度明显大于高度，绝对不要方图或竖图。
```

**4. 调 image_generation tool 出图**

对每页调你的 `image_generation` tool：

- `prompt`: 上面拼好的完整 prompt
- `output_format`: `png`
- 将返回的图片保存到 `outputs/<timestamp>/images/slide-NN.png`（NN 为两位页码）

可以并发（建议 ≤4 并发，避免限流）。

**5. 打包 PPTX**

```bash
python3 -c "
from pptx import Presentation
from pptx.util import Inches
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
import os, glob
for p in sorted(glob.glob('outputs/<timestamp>/images/slide-*.png')):
    slide = prs.slides.add_slide(blank)
    slide.shapes.add_picture(p, 0, 0, width=prs.slide_width, height=prs.slide_height)
prs.save('outputs/<timestamp>/<title>.pptx')
print('done')
"
```

### 模板克隆模式（Codex 原生路径）

你自己就是多模态 agent——直接 `Read` 模板每页 PNG 抽取视觉风格，写成 `template_profile.json`（schema 见 `template_analyzer.py` 里的 `TemplateProfile`，每个 layout 写上 `reference_image`），然后按上面流程出图时把对应模板页作为 reference image 传给 `image_generation` tool。

**不需要配 `VISION_*`**——你就是 vision。

### 与下面「--backend codex」的区别

| | 原生路径（本节） | --backend codex |
|---|---|---|
| 适用场景 | **你就是** Codex agent | 你是 Claude Code / 其他 agent，借用本机 codex CLI |
| 调用方式 | 直接调 `image_generation` tool | spawn `codex exec --full-auto` 子进程 |
| 出图层数 | 1 层 | 2 层（agent → python → codex exec） |
| 速度 | 几秒/张 | 30-60s/张 |
| 可靠性 | tool 参数精确 | 自然语言 relay，偶发失败 |
| 需要 API Key | 不需要 | 不需要 |

---

## 可选：走 codex CLI 出图（--backend codex，非 Codex caller 用）

> **如果你就是 Codex agent，不要走这条路——用上一节的「原生路径」代替。**

当你用 Claude Code / OpenClaw / 其他 agent 运行本 skill，但本机装了 codex CLI 且已登录（`codex login`），可以借用它的凭据出图，省掉配 `OPENAI_API_KEY`：

```bash
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/editorial-mono.md --backend codex
```

默认后端仍是 `openai`（直调 API，快、并发稳、每页 3-10s）。`--backend codex` 是逃生口，适合"只跑 1-2 张图试水、不想配 key"的场景。

**Tradeoffs**：
- ✅ 不需要在本 skill 配 `OPENAI_API_KEY`
- ⚠️ 慢：每页多一层 agent loop，单页 30-60s+，10 页可能 5-10 分钟
- ⚠️ 计费不变：gpt-image-2 是按图计费，不在 ChatGPT 订阅内，codex 只是代你刷额度
- ⚠️ 可控性差：aspect_ratio / quality / reference_image 靠自然语言指令让 codex 转发，偶发失败

相关 env（都可选）：

```bash
CODEX_CMD="codex exec --full-auto"   # 覆盖 codex 调用方式（默认这串）
CODEX_IMAGE_MODEL=gpt-image-2        # 传给 codex 的目标模型
CODEX_TIMEOUT_SECS=900               # 单页超时
GPT_IMAGE_BACKEND=codex              # 不想每次敲 --backend 就设这个
```

模板克隆的 vision 分析同理——当 caller agent 自己是多模态时（Claude Code / 多模态 codex），可以直接 `Read` 模板 PNG 抽取风格，不用配 `VISION_*`；只有 caller agent 是纯文本模型时才需要外挂 vision provider。

## 生成流程（内置风格）

**先 md 后 json**：md 给人看、方便 diff / review / 改文案；json 由 md 派生，喂给 `generate_ppt.py`，标为 generated，不手改。

1. 用户给一份大纲 / 已有的 slides_plan.json
2. Agent 按下面 md 规范写一份 `slides_plan.md`，与用户确认文案：
   ````markdown
   ---
   title: MediWise Health Suite 商业计划书
   ---

   ## 1. [cover] MediWise Health Suite
   副标题：家庭健康管理智能平台
   年份：2026

   ## 2. [content] 市场痛点：健康管理的两类割裂
   痛点一：高频无深度
   ...

   ## 6. [data] 效率对比：使用 MediWise 前后
   ...
   ````
   - h2 格式：`## N. [page_type, layout=layout-05] 本页标题行`
   - `N.` 可省（按出现顺序自动编号）；`[page_type]` 可省（默认 `content`）；`layout=` 只在模板克隆模式需要
   - `page_type`: `cover` / `content` / `data`
   - h2 标题行 → json 里 `content` 的第一行；下面的正文 → 正文
3. 用户 OK 后，转 json：
   ```bash
   python3 scripts/md_to_plan.py slides_plan.md -o slides_plan.json
   ```
4. 选风格：从上面 10 套里挑一个，对应 `styles/<id>.md`
5. **构造 slide_spec**（Agent 步骤）：读 `styles/<id>.md` 的视觉规范，为 `slides_plan.json` 每页构造 `slide_spec`（每个元素的 type、content、position、style），写入每页的 `slide_spec` 字段。格式见下方"指哪改哪"章节
6. 调脚本：
   ```bash
   python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/editorial-mono.md
   ```
7. 产物在 `<cwd>/outputs/<timestamp>/`：
   - `images/slide-XX.png` -- 每页 PNG（16:9，1536x864）
   - `prompts.json` -- 每页用到的完整 prompt（便于复盘 / 二次微调）
   - `metadata.json` -- slide_spec 版本历史（支持精确编辑和回滚）
   - `<title>.pptx` -- 16:9 整页填充图片的 .pptx，分享 / 投影直接用

## 生成流程（模板克隆）

1. **拿到模板 .pptx**（用户提供 / 内部模板库 / 网络下载）
2. **（可选）先单独渲染并人工挑选**----大模板（>15 页）建议先 `python3 scripts/render_template.py xxx.pptx`，再从 `template_renders/<stem>/` 里挑 8-12 张代表页复制到 `template_renders/<stem>_curated/`，供 vision 分析。页数越精，layout 命中越准
3. **生成 slides_plan.md → 转 slides_plan.json**（见内置风格流程第 2-3 步）。每页 `slide_number` / `page_type` (`cover` / `content` / `data` / 等) / `content`；想精准对位时在 h2 里加 `layout=layout-NN`（NN = 模板第 N 页 / 你期望对应的模板页编号）
4. **跑 generate_ppt.py**：
   ```bash
   python3 scripts/generate_ppt.py \
     --plan slides_plan.json \
     --template-pptx xxx.pptx \
     --template-images template_renders/xxx_curated \
     --template-strict --slides 1
   ```
   如果当前 agent 自己是多模态模型，也可以先看模板 PNG 写出 `template_profile.json`，再这样跑，完全不需要 `VISION_*`：
   ```bash
   python3 scripts/generate_ppt.py \
     --plan slides_plan.json \
     --template-profile template_profile.json \
     --template-strict --slides 1
   ```
   先 `--slides 1` 出封面冒烟，效果 OK 再跑全量
5. **告知用户产物路径**

### 模板页面挑选 / 复用原则

**核心原则：尽量做到 1 page : 1 layout**----同一份 deck 里每个 slide 用不同的模板页作 reference，观众会觉得每页都是新内容；如果同一个独特 layout 出现 2-3 次，观众下意识会想"为什么又是这页"。

vision 分析时会给每个 layout 标 `reuse_friendly`：

| reuse_friendly | 典型 layout | 多次使用的代价 |
| --- | --- | --- |
| `false`（不可复用，(!) 强警告） | 封面、3 个具名角色插画页、独特场景图（雪山/广播塔/复古收音机）、5 步骤 zigzag 各步独有图标、novelty 数据中央装置 | 视觉重复非常明显，观众会困惑 |
| `true`（可复用，但仍建议错开，(i) 弱提示） | 纯文字、卡片网格、通用列表、章节小节标题 | 不致命，但平白浪费模板里的其它好版式 |

Agent 在搭 plan 时的执行策略：
1. **优先把模板里 N 个不同 layout 分配给 N 页 slide**（N 不够就在 SKILL 里看 reuse_friendly=true 的部分挑能复用的）
2. **如果 plan 里某页内容结构非常相似（比如多个"5 步骤流程"），先尝试改写内容用不同 layout 表达**（4 步骤 + 5 步骤分别用不同流程页），而不是同一个 zigzag 用两次
3. **冒烟跑完后，看 `Layout 复用检测` 那段输出**：(!) 必须改，(i) 看情况改；改 plan 里相应 slide 的 `layout_id` 即可
4. **看完 profile JSON 选 layout**：`cat <cwd>/template_cache/<sha256>.json | jq '.layouts[] | {id, page_type, reuse_friendly, summary}'`；如果是多模态 agent 自己生成的 `template_profile.json`，就读取那个文件。

`generate_ppt.py` 在派发任务前会自动跑一次复用检测，把警告打到终端，不阻塞执行。

## Skill 调用规范

当用户说"做一份 PPT" / "生成幻灯片"时：

1. **先问三件事**（不要直接动手）：
   - 内容 / 页数 / 观众是谁？
   - 风格偏好？按"十种内置风格"表的场景类目映射推荐 1-2 个；**或者用户上传自己的 .pptx 模板**（走 `--template-pptx`，自动渲染）
   - 是否需要单页测试一张图先看效果（`--slides 1`）
2. **先写 slides_plan.md** 给用户确认文案（md 是 source of truth，人审阅友好）
3. **转 slides_plan.json**：`python3 scripts/md_to_plan.py slides_plan.md -o slides_plan.json`（json 标为 generated，不手改；要改文案回到 md 改再转）
4. **构造 slide_spec**（Agent 步骤）：读 `styles/<id>.md` 了解视觉规范，然后为 `slides_plan.json` 每页构造 `slide_spec`，写入每页的 `slide_spec` 字段（格式见"指哪改哪"章节）。这一步让后续修改能精确到每个元素
5. **跑 generate_ppt.py**，先 `--slides 1` 出封面冒烟，效果 OK 再跑全量
6. **告知用户产物路径**，产物在 `outputs/<timestamp>/`，`<title>.pptx` 可直接打开

### 面向用户的表达规范

对普通用户汇报时，默认不要解释 `slide_spec`、`metadata.json`、`element-updates`、JSON Schema、pytest 命令等内部实现，除非用户明确问技术细节。

用户最关心的是：

1. 做出来的 PPT 是否好看、能不能直接用。
2. 哪些场景稳定，哪些场景需要人工验收。
3. 是否只改了指定页 / 指定内容。
4. 最终输出目录和 PPTX 文件在哪里。
5. 当前不足是什么，例如整页图片式 PPTX、数字小字需复核、真实 logo 需提供素材。

如果需要介绍修改能力，优先引用 `docs/edit_guide.md` 的场景分级、before / after 案例和当前不足，不要把实现链路放在用户前面。

当用户说"改第 X 页的 XX"时：

1. **找到 session**：先用 `--list-sessions` 列出现有 session，确定要编辑的是哪个
2. **读 metadata.json**：查看对应 slide 的 slide_spec，找到目标元素
3. **确认修改内容**：告知用户当前内容，询问新内容
4. **构造编辑指令**：用 `--element-updates` 指定要改的元素和新内容
5. **执行 --edit**：`python3 scripts/generate_ppt.py --edit X --session <ts> --element-updates '{"elem_id": {"content": "new"}}'`
6. **告知结果**：新版本已生成，PPTX 已更新

## 仅生成部分页

```bash
python3 scripts/generate_ppt.py --plan my_plan.json --style styles/dark-aurora.md --slides 1,3,5
```

跑过的页有同名 PNG 时会自动跳过，方便逐页迭代。

## "指哪改哪" PPT 编辑工作流

本节只保留 agent 执行所需信息；完整结构、版本链和数据安全细节见 `docs/workflow.md`。向普通用户解释能力时看 `docs/edit_guide.md`。

### 生成时的结构化要求

生成新 PPT 时，agent 应为每页写入简洁的 `slide_spec`，方便后续按标题、副标题、卡片、指标等元素精确修改。最低要求：

- `layout`: 一句话描述版式
- `elements`: 语义化元素字典
- 常用元素 ID：`title`、`subtitle`、`card_1`、`card_2`、`metric_1`、`date_line`、`footer`
- 元素字段优先写 `type`、`content` 或 `heading/body`、`position`、`style`、`color`

不要为了追求完整而写很长的 spec；能让后续定位和编辑即可。

### 修改已有幻灯片

1. 用 `--list-sessions` 找到目标 session。
2. 读目标 session 的 `metadata.json`，定位页号和元素 ID。
3. 如果用户没给新内容，先问一句“当前是 X，要改成什么？”
4. 用 `--element-updates` 描述修改；需要更强约束时加 `--edit-instruction`，明确“其他内容、布局、配色不要动”。
5. 执行 `--edit` 后检查目标页图片，重建后的 PPTX 会同步更新。

常用命令：

```bash
python3 scripts/generate_ppt.py \
  --edit 3 \
  --session 20240523_143052 \
  --element-updates '{"subtitle": {"content": "医疗数据碎片化"}}' \
  --edit-instruction "将副标题从'健康管理的两类割裂'改为'医疗数据碎片化'"

python3 scripts/generate_ppt.py \
  --edit 3 \
  --session 20240523_143052 \
  --edit-prompt "在参考图基础上，只修改标题下方副标题的文字，从'健康管理的两类割裂'改为'医疗数据碎片化'，保持位置、字体、颜色、大小完全不变。" \
  --element-updates '{"subtitle": {"content": "医疗数据碎片化"}}'
```

### 外部 PPTX 摄取后修改

外部 PPTX 可先摄取为图片 session，再由多模态 agent 看图补齐每页的 `slide_spec`。没有补 spec 前，不要承诺“精确改某个对象”。

```bash
python3 scripts/generate_ppt.py --ingest-pptx path/to/deck.pptx
python3 scripts/generate_ppt.py --ingest-pptx path/to/deck.pptx --session my_deck_2024
```

### 回滚和 session 列表

```bash
python3 scripts/generate_ppt.py \
  --rollback 3 \
  --to-version 1 \
  --session 20240523_143052

python3 scripts/generate_ppt.py --list-sessions
```

## 文件结构

```
gpt-image2-ppt-skills/
|---- SKILL.md                # 本文件（Claude Code skill 入口）
|---- AGENTS.md               # codex / aider / cursor 等 agent 的薄索引，指向本文件
|---- README.md               # 项目说明
|---- scripts/                # 所有 Python 脚本
|   |---- generate_ppt.py         # 主入口（CLI）
|   |---- md_to_plan.py           # slides_plan.md -> slides_plan.json 转换器（CLI）
|   |---- render_template.py      # PPTX -> 每页 PNG 的辅助脚本（CLI + library）
|   |---- image_generator.py      # gpt-image-2 wrapper（支持 reference image，openai backend）
|   |---- codex_backend.py        # 可选：走 codex CLI 出图（--backend codex）
|   \---- template_analyzer.py    # PPT 模板剖析器（vision + 缓存）
|---- styles/                 # 10 套内置风格
|   |---- gradient-glass.md           dark-aurora.md
|   |---- clean-tech-blue.md          risograph.md
|   |---- vector-illustration.md      japanese-wabi.md
|   |---- editorial-mono.md           swiss-grid.md
|   |---- hand-sketch.md              y2k-chrome.md
|---- docs/README.en.md       # 英文 README
|---- install_as_skill.sh     # 一键安装到 agent skills 目录
|---- requirements.txt        # requests + python-dotenv + python-pptx + jsonschema + pymupdf
\---- .env.example
```

调用时产生的运行时目录都在 `<cwd>` 下：
```
<your-project>/
|---- template_renders/<stem>/page-NN.png   # PPTX 渲染（render_template.py）
|---- template_cache/<sha256>.json          # 外挂 vision 风格分析缓存（纯文本 agent 路径）
|---- template_profile.json                 # 多模态 agent 可手写/生成的模板 profile（可选）
\---- outputs/<timestamp>/                  # 每次生成产物
```

## License

Apache License 2.0.
