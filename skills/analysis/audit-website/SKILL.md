---
name: audit-website
description: "使用 squirrelscan CLI（squirrel）对网站进行审计，覆盖 SEO、技术、内容、性能、安全等 140+ 规则。当需要分析网站健康、排查技术 SEO、检查死链、校验 meta 与结构化数据、生成站点审计报告、对比改版前后，或提到「网站审计」「audit website」「squirrel」「站点健康检查」时使用。"
license: MIT
---

# 网站审计技能

使用 [squirrelscan](https://squirrelscan.com) 的 CLI 工具 `squirrel`，对网站进行 SEO、技术、内容、性能和安全性审计。

squirrel 支持 macOS、Windows、Linux，通过模拟浏览器与搜索爬虫，结合 140+ 条规则分析站点结构与内容，输出问题列表及修复建议。

## 链接

- 官网：<https://squirrelscan.com>
- 文档（含规则说明）：<https://docs.squirrelscan.com>

规则文档模板：`https://docs.squirrelscan.com/rules/{rule_category}/{rule_id}`  
示例：<https://docs.squirrelscan.com/rules/links/external-links>

---

## 本技能能做什么

支持 AI 智能体按 20+ 类别、140+ 条规则审计网站，包括：

- **SEO**：Meta 标签、title、description、canonical、Open Graph
- **技术**：死链、重定向链、页面速度、移动友好性
- **性能**：加载时间、资源使用、缓存
- **内容**：标题结构、图片 alt、内容分析
- **安全**：泄露密钥、HTTPS、安全头、混合内容
- **无障碍**：alt、色彩对比、键盘导航
- **可用性**：表单校验、错误处理、用户流程
- **链接**：内外链死链检测
- **E-E-A-T**：经验、专业、权威、可信度
- **移动端**：移动友好、响应式、触控元素
- **可抓取性**：robots.txt、sitemap.xml 等
- **Schema**：Schema.org、结构化数据、富摘要
- **法律**：隐私政策、服务条款等合规
- **社交**：Open Graph、Twitter 卡片及 schema 校验
- **URL 结构**：长度、连字符、关键词
- **关键词**：堆砌检测
- **图片**：alt、对比度、尺寸、格式
- **本地 SEO**：NAP 一致性、地理元数据
- **视频**：VideoObject schema、无障碍

审计会爬取站点、按规则分析页面，并生成报告，包含：

- 整体健康分（0–100）
- 按类别 breakdown（核心 SEO、技术 SEO、内容、安全等）
- 具体问题及受影响 URL
- 死链列表
- 可执行的改进建议

---

## 何时使用

在以下场景使用本技能：

- 分析网站健康度
- 排查技术 SEO 问题
- 修复上述各类问题
- 检查死链
- 校验 meta 与结构化数据
- 生成站点审计报告
- 对比改版前后健康度
- 提升性能、无障碍、SEO、安全等

---

## 前置条件

本技能依赖 **squirrel CLI**，需已安装并加入 PATH。

### 安装（macOS / Linux）

```bash
curl -fsSL https://squirrelscan.com/install | bash
```

将会：

- 下载最新二进制
- 安装到 `~/.local/share/squirrel/releases/{version}/`
- 在 `~/.local/bin/squirrel` 创建软链
- 在 `~/.squirrel/settings.json` 初始化配置

若 `~/.local/bin` 不在 PATH 中，在 shell 配置里添加：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Windows 安装

PowerShell：

```powershell
irm https://squirrelscan.com/install.ps1 | iex
```

将下载并安装到 `%LOCALAPPDATA%\squirrel\`，并加入 PATH。若用 CMD，可能需要重启终端使 PATH 生效。

### 验证安装

```bash
squirrel --version
```

---

## 配置

在项目目录执行 `squirrel init` 会生成 `squirrel.toml`。

每个项目应有唯一的 **project name**（默认可用被审计站点名），用于数据库区分多次审计：

```bash
squirrel init --project-name my-project
```

或：

```bash
squirrel config set project.name my-project
```

**若当前目录没有 `squirrel.toml`，必须先执行 `squirrel init`**，并用 `-n` 指定项目名（可推断）。  
项目名用于数据库标识，存储在 `~/.squirrel/projects/`。

---

## 使用方式

### 概述

有三个子命令，结果都会写入本地项目数据库：

- **crawl**：执行或继续爬取
- **analyze**：分析爬取结果
- **report**：按指定格式输出报告（llm、text、console、html 等）

`audit` 是上述三步的封装，按顺序执行：

```bash
squirrel audit https://example.com --format llm
```

**优先使用 `--format llm`**：为 LLM 设计的紧凑、完整输出格式。

### 审计目标选择

- 若用户未提供 URL：从当前目录、环境变量（如 Vercel 项目、记忆或代码中的引用）推断可能站点。
- 若当前目录能启动本地 dev 服务：可对本地站点做审计。
- 若发现多个可审计站点：让用户选择。
- 若无法推断任何站点：询问用户要审计的 URL。

**优先审计线上站点**，更能反映真实性能与渲染问题。若同时有本地与线上，提示用户选择，并**建议选线上**。可在线上审计发现问题后，在本地代码中修复。

### 实施修复时

- 可将大范围修复拆成可并行的子任务，用 subagent 加速。
- 修复完成后，如环境有 typecheck/format 工具（如 ruff、biome、tsc），对生成代码跑一遍。

### 基本流程

1. **执行审计**（写入数据库，并输出到终端）
2. **按格式导出报告**

```bash
# 1. 执行审计（默认 console 输出）
squirrel audit https://example.com

# 2. 导出为 LLM 格式
squirrel report <audit-id> --format llm
```

### 常用选项

爬取更多页面：

```bash
squirrel audit https://example.com --max-pages 200
```

忽略缓存、强制重新爬取：

```bash
squirrel audit https://example.com --refresh
```

恢复中断的爬取：

```bash
squirrel audit https://example.com --resume
```

调试时详细输出：

```bash
squirrel audit https://example.com --verbose
```

---

## 命令选项

### audit

| 选项 | 别名 | 说明 | 默认 |
|------|------|------|------|
| `--format <fmt>` | `-f` | 输出格式：console, text, json, html, markdown, llm | console |
| `--max-pages <n>` | `-m` | 最大爬取页数（最大 500） | 500 |
| `--refresh` | `-r` | 忽略缓存，全部重新抓取 | false |
| `--resume` | - | 恢复中断的爬取 | false |
| `--verbose` | `-v` | 详细输出 | false |
| `--debug` | - | 调试日志 | false |

### report

| 选项 | 别名 | 说明 |
|------|------|------|
| `--format <fmt>` | `-f` | console, text, json, html, markdown, xml, llm |

### 输出格式

- **console**（默认）：彩色、带进度的可读输出。
- **llm**：面向 LLM 的紧凑 XML/文本混合，token 更省（比冗长 XML 约小 40%），包含：
  - 摘要：健康分与核心指标
  - 按规则分类的问题（核心 SEO、技术、内容、安全等）
  - 死链列表（内链 + 外链）
  - 按优先级排列的改进建议

---

## 示例

### 1. 快速站点审计（LLM 输出）

```bash
squirrel audit https://squirrelscan.com --format llm
```

### 2. 大站深度审计

```bash
squirrel audit https://myblog.com --max-pages 500 --format llm
```

### 3. 改版后重新审计（忽略缓存）

```bash
squirrel audit https://example.com --refresh --format llm
```

### 4. 两步流程（复用已有审计）

```bash
squirrel audit https://example.com
# 记下输出的 audit-id，如 a1b2c3d4

squirrel report a1b2c3d4 --format llm
```

---

## 输出

审计与修复完成后，给用户一个**所有改动的摘要**。

---

## 故障排除

### `squirrel` 找不到

1. 安装：`curl -fsSL https://squirrelscan.com/install | bash`
2. 加入 PATH：`export PATH="$HOME/.local/bin:$PATH"`
3. 验证：`squirrel --version`

### 权限错误

```bash
chmod +x ~/.local/bin/squirrel
```

### 爬取超时或很慢

大站可能需较长时间，加 `--verbose` 查看进度：

```bash
squirrel audit https://example.com --format llm --verbose
```

### 无效 URL

务必包含协议（`http://` 或 `https://`）：

```bash
# ✗ 错误
squirrel audit example.com

# ✓ 正确
squirrel audit https://example.com
```

---

## 工作流程

1. **Crawl**：从基础 URL 发现并抓取页面  
2. **Analyze**：对每页执行审计规则  
3. **External Links**：检查外链可用性  
4. **Report**：生成 LLM 优化报告  

审计结果保存在本地数据库，之后可用 `squirrel report` 按不同格式导出。

---

## 延伸资源

- [squirrelscan 文档](https://docs.squirrelscan.com)
- CLI 帮助：`squirrel audit --help`
