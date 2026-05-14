---
name: open-show
description: 将 Markdown、Word (.docx)、PDF、Text (.txt)、本地 HTML 或任意网址转换为单个可全屏播放的 HTML 幻灯片。触发词：「幻灯片」「转幻灯片」「生成演示稿」「做 deck」「文档转 html 播放」。
---

# OpenShow 技能

## 触发条件

用户提及以下任意关键词时激活：
- 「幻灯片」「转幻灯片」「生成演示稿」「做 deck」
- 「把这个文档转成可播放的 html」
- 「把这篇文章做成 PPT 一样的网页」
- 「这个网页能不能全屏播放」

## 支持的输入

| 类型 | 识别方式 | 处理方式 | 依赖 |
|------|---------|---------|------|
| Markdown | `.md` / `.markdown` 后缀 | `markdown` 库解析 | `markdown` |
| Word | `.docx` 后缀 | `python-docx` 提取标题/段落 | `python-docx` |
| 本地 HTML | `.html` / `.htm` 后缀 | `BeautifulSoup` 解析 DOM | `beautifulsoup4` |
| 网址 | `http://` / `https://` 前缀 | `requests` 抓取 + 正文提取 | `requests`, `beautifulsoup4` |
| PDF | `.pdf` 后缀 | `PyMuPDF` 逐页转图片嵌入 | `pymupdf` |
| Text | `.txt` 后缀 | 按空行/标题分块解析 | 无 |

## 执行流程（严格按顺序）

### 第一步：依赖检查
首次使用或不确定时，检查依赖：
```bash
python3 -c "import markdown, docx, requests, bs4, fitz; print('ok')"
```
若失败，安装：
```bash
python3 -m pip install markdown python-docx requests beautifulsoup4 pymupdf
```

### 第二步：判断输入并调用脚本
基础用法：
```bash
python3 ~/.hermes/skills/open-show/scripts/openshow.py -i "<输入>" -o ~/openshow_outputs
```

生成后自动用系统默认浏览器打开：
```bash
python3 ~/.hermes/skills/open-show/scripts/openshow.py -i "<输入>" -o ~/openshow_outputs --open
```

生成后用 openclaw browser 打开：
```bash
python3 ~/.hermes/skills/open-show/scripts/openshow.py -i "<输入>" -o ~/openshow_outputs --openclaw
```

- 输入可以是文件绝对路径或 URL
- 输出目录固定为 `~/openshow_outputs`（不存在则自动创建）
- 生成文件命名规则：`openshow_<标题>_<时间戳>.html`

### 第三步：返回结果并告知交互方式

> 已生成可播放 HTML：`{path}`
>
> 操作方式：
> - `←` / `→` 翻页
> - `空格` / `PageDown` 下一页
> - `F` 键切换全屏
> - `T` 键显示/隐藏计时器
> - 手机支持左右滑动翻页
> - 点击屏幕右侧 2/3 下一页，左侧 1/3 上一页
> - 左上角计时器点击可暂停/继续
>
> 适配场景：手机、电脑、大屏幕投影全屏播放

## 核心机制（内部实现要点）

### 内容解析
- 所有输入统一转换为 `Block` 列表（heading, paragraph, image, list, code, quote）
- HTML/URL 输入会启发式提取正文容器（最大文本密度的 `article/main/div/section`）
- 自动清理导航栏、广告、脚本、样式表
- 本地/远程图片自动内联为 `data URI`，确保单文件离线可用

### 分页算法
1. 以 `h1/h2/h3` 为天然章节边界分 `Section`
2. 单节内按容量拆页：文字 > 300 字、图片 > 3 张、块数 > 6 时自动拆分
3. 超长段落（>300 字）先按句子拆分为多个 block，避免一页文字爆炸
4. 自动避免标题独占一页：若某页只有 heading，从下一页借一个 block

### 布局模板
根据内容自动匹配：
- `cover`：H1 大标题页，居中
- `text`：纯文字内容页，左对齐
- `list`：bullet points 页，字体放大
- `split`：左图右文（1 张图）或上图下文（多张图）
- `image`：单图全屏居中
- `closing`：最后一页，居中总结风格

### 幻灯片引擎
- 零外部 CDN，CSS + JS 全部内联
- 每页 `100vw × 100vh` 绝对定位
- 翻页动画：`transform: translateX()` + `cubic-bezier(0.22, 1, 0.36, 1)`，0.5s
- 性能优化：`will-change` + `backface-visibility: hidden` + `touch-action: none`
- 响应式：`clamp()` 字体 + `@media` 适配手机

### 计时器
- 页面加载 1 秒后自动开始
- 左上角显示 `MM:SS`
- 点击暂停/继续，暂停时变橙色
- `T` 键切换显示/隐藏

### 品牌水印
- 每页右下角内置 OpenShow logo（极简几何线条风格）
- 低透明度（`rgba(255,255,255,0.04~0.07)`），不影响阅读
- 切换到活动页时透明度微增，高端大气

## 常见错误与限制

- ❌ 不支持 `.pptx` 输入
- ❌ 不支持 `.doc`（老版本 Word），必须先转换为 `.docx`
- ⚠️ PDF 转换为图片嵌入，文件较大时可能产生较大的 HTML
- ⚠️ 某些复杂网页的 DOM 结构可能提取不完全，可建议用户先保存为本地 HTML 再转换
- ⚠️ 远程图片下载失败时会保留原 URL，离线播放可能缺失

## 文件位置

- Skill 配置：`~/.hermes/skills/open-show/SKILL.md`
- 核心脚本：`~/.hermes/skills/open-show/scripts/openshow.py`
- Logo 资源：`~/.hermes/skills/open-show/assets/logo.svg`
- 输出目录：`~/openshow_outputs/`
