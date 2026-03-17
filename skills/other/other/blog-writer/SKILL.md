---
name: blog-writer
description: "技术博客写作专家，专注于 AI、编程、运维等技术领域的深度写作。自动抓取素材、生成配图、输出符合 Hugo 规范的博客文章。使用此 skill 当用户需要：(1) 撰写技术博客文章 (2) 整理技术资料成文章 (3) 介绍新工具/新技术"
---

# 技术博客写作专家

## 博客信息

- **博客地址**: https://www.heyuan110.com/
- **Hugo 版本**: v0.153.2+ (Extended)
- **主题**: hermit-V2
- **内容目录**: `content/posts/`

---

## 强制执行流程

⚠️ **每一步必须完成后才能进入下一步，不可跳过。**

---

### Step 0: 确认需求

在开始任何工作之前，**必须**向用户确认以下信息：

1. **主题**：您想写什么内容？
2. **素材**：有参考链接吗？（URL、文档、GitHub 仓库等）
3. **目标关键词**：希望用户搜索什么词找到文章？（可选）

如果用户已在指令中提供了这些信息，无需重复询问，直接进入 Step 1。

---

### Step 1: 确定分类和目录

#### 分类规范

根据文章内容选择分类，**只能使用以下预设值，禁止自创分类**：

| 分类 | 适用内容 |
|------|----------|
| **AI原理** | 概念、理论、访谈、思考、趋势分析 |
| **AI实战** | 教程、指南、工具使用、最佳实践、产品评测 |
| **Go** | Go 语言相关 |
| **Java** | Java 相关 |
| **Python** | Python 相关 |
| **Docker** | Docker 相关 |
| **Linux** | Linux 相关 |
| **MySQL** | MySQL 相关 |
| **macOS** | macOS 相关 |

❌ 错误示例：`Go实战`、`Docker教程`、`AI工具`（这些都是无效分类）
✅ 正确示例：写 Go 教程用 `categories = ['Go']`，写 AI 工具教程用 `categories = ['AI实战']`

#### 目录命名

使用 Page Bundle 结构，命名规范：`<日期>-<英文短标题>/`

```
content/posts/ai/2026-01-26-claude-code-guide/
├── index.md      # 文章内容
├── cover.webp    # 封面图（必须叫 cover.webp）
└── other.webp    # 其他配图
```

⚠️ **必须**用 `date` 命令获取当前日期，URL 目录名只用英文。

---

### Step 2: 收集素材

#### 2.1 读取用户提供的素材

如果用户提供了参考链接，**必须认真阅读链接内容**，不可仅凭标题猜测：

- **读取方式优先级**：
  1. 首选 `WebFetch` 工具
  2. 如遇反爬虫/403/访问限制，改用 Playwright MCP（`browser_navigate` + `browser_snapshot`）
  3. 如果是 GitHub 链接，可用 `gh` 命令或访问 raw 内容
- **特别关注**：核心观点、文章结构、配图含义、代码示例、技术细节

#### 2.2 主动研究补充

⚠️ **必须**执行以下主动研究，不能仅依赖用户提供的素材：

- 使用 `WebSearch` 搜索该主题的**最新进展和权威资料**
- 检查是否有该领域的**经典内容、官方文档、最佳实践**被遗漏
- 搜索**对比观点或争议点**，确保文章视角全面
- 如果涉及工具/框架，查找**官方文档和 GitHub 仓库**获取准确信息

#### 2.3 获取已有文章列表（为内链做准备）

⚠️ **必须**执行以下命令，获取博客已有文章目录：

```bash
ls content/posts/ai/
```

记录已有文章列表，在 Step 4 撰写时用于添加内链。

---

### Step 3: 生成封面图

⚠️ **必须**为每篇文章生成封面图。按以下优先级尝试：

#### 方案 A（首选）：Rube MCP + Gemini AI 生图

通过 Rube MCP 调用 `GEMINI_GENERATE_IMAGE` 生成封面图：

**第一步：搜索工具并获取 session_id**

调用 `RUBE_SEARCH_TOOLS` 搜索图像生成工具：
```
queries: [{use_case: "generate an AI image from a text prompt for a blog cover"}]
session: {generate_id: true}
```

**第二步：生成图片**

调用 `RUBE_MULTI_EXECUTE_TOOL` 执行生图：
```
tools: [{
  tool_slug: "GEMINI_GENERATE_IMAGE",
  arguments: {
    prompt: "基于文章主题的详细英文描述，描述画面内容、风格、色调",
    model: "gemini-2.5-flash-image",
    aspect_ratio: "16:9"
  }
}]
session_id: "上一步返回的 session_id"
sync_response_to_workbench: false
memory: {}
```

**提示词要求**：
- 用**英文**撰写提示词（Gemini 对英文效果更好）
- 描述具体的画面内容、风格、色调
- 风格要求：科技感、简洁、专业，适合技术博客封面
- 避免包含文字（AI 生成的文字通常不准确）

**第三步：下载并转换**

图片 URL 在返回结果的 `data.image.s3url` 中（URL 有时效，需尽快下载）：

```bash
# 下载 AI 生成的图片
curl -L -o cover_raw.png "<s3url>"

# 转换为 webp 并调整尺寸
cwebp -q 85 -resize 1200 630 cover_raw.png -o cover.webp

# 清理临时文件
rm cover_raw.png
```

如果 `cwebp` 不可用，使用 Python 转换：
```python
python3 -c "
from PIL import Image
img = Image.open('cover_raw.png').resize((1200, 630), Image.LANCZOS)
img.save('cover.webp', 'WEBP', quality=85)
import os; os.remove('cover_raw.png')
"
```

如果 AI 生图失败（连接不可用、安全过滤拦截等），使用方案 B。

#### 方案 B（兜底）：Python/Pillow 程序化生成

当 AI 生图不可用时，执行以下 Python 脚本生成封面图（根据文章主题调整标题和关键词）：

```python
python3 -c "
from PIL import Image, ImageDraw, ImageFont
import subprocess

# === 配置区：根据文章修改以下内容 ===
TITLE = '文章标题'           # 封面大标题
SUBTITLE = '副标题或简短描述'  # 副标题
TAGS = ['标签1', '标签2', '标签3']  # 关键词标签
OUTPUT_DIR = 'content/posts/ai/目录名'  # 文章目录路径
# === 配置区结束 ===

WIDTH, HEIGHT = 1200, 630
img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# 深色渐变背景
for y in range(HEIGHT):
    r = int(15 + (25 - 15) * y / HEIGHT)
    g = int(23 + (35 - 23) * y / HEIGHT)
    b = int(42 + (60 - 42) * y / HEIGHT)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# 装饰元素：顶部渐变线条
for x in range(WIDTH):
    alpha = int(255 * (1 - abs(x - WIDTH/2) / (WIDTH/2)))
    draw.line([(x, 0), (x, 3)], fill=(100, 149, 237, alpha))

# 加载中文字体（macOS 系统字体，按优先级尝试多个）
# ⚠️ 所有字体必须支持中文，否则会出现乱码
CJK_FONT_PATHS = [
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/Library/Fonts/Arial Unicode.ttf',
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/Supplemental/Songti.ttc',
]

def load_cjk_font(size):
    for path in CJK_FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    raise RuntimeError('未找到任何中文字体，无法生成封面图。请安装中文字体后重试。')

font_title = load_cjk_font(52)
font_subtitle = load_cjk_font(28)
font_tag = load_cjk_font(20)

# 绘制标题（自动换行）
max_width = WIDTH - 120
words = TITLE
lines = []
current_line = ''
for char in words:
    test_line = current_line + char
    bbox = draw.textbbox((0, 0), test_line, font=font_title)
    if bbox[2] - bbox[0] > max_width:
        lines.append(current_line)
        current_line = char
    else:
        current_line = test_line
if current_line:
    lines.append(current_line)

y_offset = 180 if len(lines) <= 2 else 140
for line in lines:
    bbox = draw.textbbox((0, 0), line, font=font_title)
    x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, y_offset), line, fill='white', font=font_title)
    y_offset += 70

# 绘制副标题
if SUBTITLE:
    bbox = draw.textbbox((0, 0), SUBTITLE, font=font_subtitle)
    x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, y_offset + 20), SUBTITLE, fill=(180, 180, 200), font=font_subtitle)

# 绘制标签
tag_y = HEIGHT - 80
total_width = sum(draw.textbbox((0, 0), f' {t} ', font=font_tag)[2] - draw.textbbox((0, 0), f' {t} ', font=font_tag)[0] + 24 for t in TAGS) + 12 * (len(TAGS) - 1)
tag_x = (WIDTH - total_width) // 2
for tag in TAGS:
    text = f' {tag} '
    bbox = draw.textbbox((0, 0), text, font=font_tag)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # 标签背景
    draw.rounded_rectangle(
        [(tag_x, tag_y), (tag_x + tw + 20, tag_y + th + 14)],
        radius=6, fill=(40, 60, 100), outline=(80, 120, 180)
    )
    draw.text((tag_x + 10, tag_y + 7), text, fill=(160, 200, 255), font=font_tag)
    tag_x += tw + 32

# 保存为 webp
png_path = f'{OUTPUT_DIR}/cover.png'
webp_path = f'{OUTPUT_DIR}/cover.webp'
img.save(png_path)
subprocess.run(['cwebp', '-q', '85', png_path, '-o', webp_path], check=True)
import os
os.remove(png_path)

# 验证文件大小
size_kb = os.path.getsize(webp_path) / 1024
print(f'封面图已生成: {webp_path} ({size_kb:.1f} KB)')
if size_kb > 200:
    print('⚠️ 警告：文件超过 200KB，请降低质量参数重新生成')
"
```

如果 `cwebp` 不可用，使用 Pillow 直接保存 webp：
```python
img.save(f'{OUTPUT_DIR}/cover.webp', 'WEBP', quality=85)
```

⚠️ **方案 B 生成后必须验证**：用 Read 工具查看生成的封面图，确认中文标题、副标题、标签均正常显示，**不存在任何方框、问号、乱码字符**。如果出现乱码，说明字体不支持中文，必须排查字体路径后重新生成。

#### 封面图检查清单（无论哪种方案都必须满足）

- [ ] 文件名为 `cover.webp`
- [ ] 尺寸 1200×630px
- [ ] 大小 < 200KB
- [ ] 内容与文章主题相关
- [ ] **无乱码**：必须用 Read 工具查看生成的封面图，确认图片中不存在任何乱码、乱字符或不可读文字。如有乱码必须重新生成

---

### Step 4: 撰写文章

#### 4.1 Front Matter + 封面图引用（TOML 格式）

```toml
+++
date = '2026-01-26T10:00:00+08:00'
draft = false
title = '文章标题（20-60字符，核心关键词靠前）'
description = '文章描述，用于 SEO 和社交分享（120-160字符）'
toc = true
tags = ['标签1', '标签2', '标签3']
categories = ['AI实战']
keywords = ['搜索关键词1', '搜索关键词2']
+++

![封面图 ALT 文本，包含核心关键词的描述](cover.webp)
```

⚠️ **封面图必须在正文中引用**：在 Front Matter（`+++`）结束后的**第一行**，必须用 `![ALT 文本](cover.webp)` 引用封面图。不引用则封面图不会显示在文章中。ALT 文本应包含核心关键词，描述图片内容。

| 字段 | 必填 | 说明 |
|------|------|------|
| `date` | ✓ | ISO 8601 格式，含时区 `+08:00` |
| `title` | ✓ | 50-60 字符，关键词前置 |
| `description` | ✓ | 120-160 字符，包含核心关键词 |
| `categories` | ✓ | 只能使用 Step 1 中的预设值 |
| `tags` | ✓ | 3-5 个标签 |
| `toc` | 推荐 | 长文设为 `true` |
| `draft` | 可选 | 默认 `false` |

#### 4.2 写作规范检查项

撰写时必须逐项确保：

**开头三要素**（首段 100 字内必须出现核心关键词）：
- ✅ 为什么需要这个技术？（背景）
- ✅ 这个技术是什么？（定义）
- ✅ 读完能获得什么？（价值）

**内容深度**：
- ✅ 每个核心概念都配实际案例，让读者能举一反三
- ✅ 复杂概念必须用类比或比喻解释（让小学生也能听懂）
- ✅ 不浮于表面，深入讲解原理和细节
- ✅ 代码示例完整可运行，有中文注释

**推荐的内容结构**：

```markdown
## 一、背景与问题（为什么需要）
## 二、核心概念（是什么）
## 三、基本用法（怎么用）
## 四、实战案例（真实场景）
## 五、进阶技巧（深入理解）
## 六、常见问题（避坑指南）
## 总结
```

**通俗化表达示例**：

```markdown
# ❌ 不好的写法
Docker 容器是一种轻量级虚拟化技术，通过 namespace 和 cgroup 实现资源隔离。

# ✅ 好的写法
Docker 容器就像一个"打包好的便当盒"。你把应用程序和它需要的所有东西都放进这个盒子里，
不管带到哪台电脑上打开，里面的东西都一模一样。
```

**SEO 要点**：
- 标题、描述、首段包含核心关键词
- 使用语义化标题层级（H2 > H3 > H4）
- 图片使用描述性 ALT 文本，包含关键词

**GEO（生成式引擎优化）要点**：
- 内容结构清晰，便于 AI 理解和引用
- 提供明确的定义和解释
- 使用列表、表格等结构化格式
- 给出具体数据和案例支撑观点

#### 4.3 链接策略

⚠️ **必须**基于 Step 2.3 获取的已有文章列表添加链接。

**内链（3-8 个）**：
- 在正文中自然引用已有相关文章
- 添加内链前确认目标文章确实存在（基于 Step 2.3 的文章列表）
- 文末添加「相关阅读」板块

```markdown
## 相关阅读

- [相关文章标题1](/posts/ai/2026-xx-xx-article-name/)
- [相关文章标题2](/posts/ai/2026-xx-xx-article-name/)
```

**外链（3-5 个）**：
- 优先链接权威来源：官方文档、GitHub 仓库、技术标准（RFC、W3C）
- 在正文中自然引用，为读者提供延伸阅读

#### 4.4 嵌套代码块处理

当需要在代码块中展示包含代码块的内容时，**必须使用不同数量的反引号**：

`````markdown
````markdown
```python
print("Hello World")
```
````
`````

规则：外层反引号数量必须**大于**内层。如外层 4 个，内层 3 个。

---

### Step 5: 发布前检查

⚠️ **以下所有检查项必须逐一确认**，任何不通过的项目必须修复后才能完成。

#### 格式检查

- [ ] 标题 ≤ 60 字符，关键词前置
- [ ] Description 120-160 字符，包含核心关键词
- [ ] Front Matter 使用 TOML 格式（`+++`）
- [ ] `categories` 使用预设值，未自创分类
- [ ] 目录名使用英文命名
- [ ] 日期使用 `date` 命令获取的真实日期
- [ ] 封面图为 `cover.webp`，尺寸 1200×630，大小 ≤ 200KB

#### 内容质量检查

- [ ] **封面图已在正文中引用**：Front Matter 后第一行为 `![ALT](cover.webp)`
- [ ] 开头三要素齐全：背景、定义、价值
- [ ] 每个核心概念都配了实际案例
- [ ] 复杂概念有通俗类比
- [ ] 代码示例完整可运行，有中文注释
- [ ] 内链数量 ≥ 3，且目标文章确实存在
- [ ] 外链数量 ≥ 3，指向权威来源
- [ ] 文末有「相关阅读」板块

#### Hugo 构建验证

⚠️ **必须**执行构建验证：

```bash
hugo --minify
```

确认无报错后，文章才算完成。

---

## 注意事项

1. **日期必须真实**：使用 `date` 命令获取当前日期
2. **URL 必须英文**：目录名使用英文或拼音
3. **Front Matter 用 TOML**：使用 `+++` 而非 `---`
4. **图片必须 webp**：封面图命名为 `cover.webp`
5. **素材必须实际阅读**：不可仅凭链接标题猜测内容
6. **分类只能用预设值**：禁止自创分类
