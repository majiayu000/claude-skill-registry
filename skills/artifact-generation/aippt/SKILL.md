---
name: aippt
description: AIPPT - 基于模板定制化生成 PPT。垫图约束风格 → 提示词替换内容 → AI 生图 → 打包 PPTX。
---

<!--
input: 文章/内容 + PPT模板
output: 完整的 .pptx 文件
pos: 核心 skill，PPT 自动化生成

架构守护者：一旦我被修改，请同步更新：
1. 本文件的头部注释
2. README.md 索引表
-->

# AIPPT - AI PPT 生成工作流

> **核心理念**：用垫图约束风格，用提示词替换内容，AI 生成每一页。

## 什么时候用

- 有现成 PPT 模板，想快速生成新内容
- 需要批量生成多页 PPT
- 希望每页风格一致但内容不同

---

## 工作流程

```
导出图片 → 分析模板 → 内容分段 → 表达形式设计 → 内容映射 → 上传图床 → 调用API → 下载保存 → 打包PPTX
    ↓          ↓          ↓            ↓            ↓          ↓         ↓          ↓          ↓
  垫图      布局库      页面规划    最佳表达形式    提示词      URL      生成图片    PNG文件    .pptx
```

---

## 快速开始

### Step 1: 准备垫图
读 `01_导出方法.md` — PPT 导出为图片

### Step 2: 分析模板
读 `02_PPT模板分析方法.md` — 输出布局库

### Step 3: 规划内容
读 `03_内容分段方法.md` — 确定每页放什么

### Step 3.5: 表达形式设计（关键）
对每页内容问：**最佳表达形式是什么？**
- 模板有合适布局 → 用模板
- 模板没有 → 用创意页面（风格不变，表达自由）

详见 `04_内容映射方法.md` 的"表达形式设计"章节

### Step 4: 映射+提示词
读 `04_内容映射方法.md` — 内容匹配布局，生成提示词

> **提示词规范**见 `02_PPT模板分析方法.md` 第六章

### Step 5: 生成图片
上传垫图 → 调用 API → 下载保存

### Step 6: 打包 PPT
```bash
node scripts/images2pptx.js <图片目录> output.pptx
```

---

## 文件索引

| 文件 | 地位 | 功能 |
|------|------|------|
| `01_导出方法.md` | 阶段1 | PPT 导出为图片（垫图） |
| `02_PPT模板分析方法.md` | 阶段2 | 分析模板，输出布局库 |
| `03_内容分段方法.md` | 阶段3 | 内容拆分为页面 |
| `04_内容映射方法.md` | 阶段4 | 内容匹配布局，生成提示词 |
| `05_图床上传方法.md` | 工具 | 图床上传获取 URL |
| `config/secrets.md` | 配置 | API Key |
| `scripts/images2pptx.js` | 工具 | 图片打包成 PPTX |

---

## API 调用

### 读取配置

从 `config/secrets.md` 获取 API Key

### 调用生图 API

```bash
curl -s -X POST "https://api.apicore.ai/v1/images/generations" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-3-pro-image-preview-4k", "prompt": "提示词", "size": "16:9", "n": 1}'
```

### 模型选择

| 模型 | 说明 |
|-----|------|
| `gemini-3-pro-image-preview` | 标准版 |
| `gemini-3-pro-image-preview-2k` | 2K 高清 |
| `gemini-3-pro-image-preview-4k` | 4K 超清（默认） |

### 下载图片

```bash
curl -s -o "输出.png" "图片URL"
```

---

## 打包 PPTX

```bash
# 首次使用安装依赖
npm install pptxgenjs

# 打包
node scripts/images2pptx.js <图片目录> [输出文件名]
```

- 自动识别 jpg/png/gif/webp
- 按文件名数字排序
- 输出 16:9 比例

---

## 目录结构

```
AIPPT2/
├── SKILL.md              # 入口（本文件）
├── README.md             # 总览
├── 01_导出方法.md
├── 02_PPT模板分析方法.md
├── 03_内容分段方法.md
├── 04_内容映射方法.md
├── 05_图床上传方法.md
├── config/
│   └── secrets.md        # API Key
└── scripts/
    └── images2pptx.js    # 打包脚本
```
