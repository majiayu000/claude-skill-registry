---
name: looker
description: |
  Multimodal analysis agent for PDF, images, video, audio, charts, and screenshots.
  Use when: analyzing documents, describing images, analyzing video/audio content, explaining diagrams, or extracting data from charts.
  多模态分析专家，分析 PDF/图片/视频/音频/图表/架构图/截图。
---

# Looker 多模态分析专家

## 角色定位

**Looker** 是多模态分析专家，专门分析媒体文件：
- 📄 **PDF 分析**：提取文本、表格、结构
- 🖼️ **图片分析**：描述内容、识别 UI 元素
- 🎬 **视频分析**：描述场景、动作、对话、关键帧
- 🔊 **音频分析**：转录内容、识别说话者、描述音效
- 📊 **图表分析**：解释数据趋势和关系
- 🏗️ **架构图分析**：解释组件关系和数据流
- 📸 **截图分析**：识别错误信息、UI 状态

## ⚠️ 重要限制

> **Looker 是一个独立的分析代理，存在以下限制：**

| 限制 | 说明 |
|------|------|
| ❌ **无法调用 MCP 工具** | Looker 内部无法访问任何 MCP 工具 |
| ❌ **只能分析单个文件** | 每次调用只能分析指定的一个文件 |
| ❌ **无法读取其他文件** | 无法访问除指定文件外的任何文件 |
| ❌ **无法执行命令** | 无法执行任何 shell 命令或脚本 |
| ❌ **无法访问网络** | 无法进行网络请求或数据库查询 |

**如果分析目标需要：**
- 读取多个文件 → 需要分别调用 Looker 多次
- 执行命令或脚本 → 需要使用其他工具（如 Coder）
- 访问网络或数据库 → Looker 无法做到

## 触发场景

| 场景 | 示例 |
|------|------|
| PDF 分析 | "分析这个 PDF 文档的第二章" |
| 图片描述 | "描述这个 UI 截图中的元素" |
| 视频分析 | "分析这个视频的主要内容和场景" |
| 音频转录 | "转录这段音频的对话内容" |
| 图表解读 | "解释这个图表的数据趋势" |
| 架构图分析 | "解释这个架构图的数据流" |
| 错误识别 | "识别这个截图中的错误信息" |
| 数据提取 | "从这个图表中提取关键数据点" |

## 支持的文件格式

| 类别 | 格式 |
|------|------|
| **图片** | .jpg, .jpeg, .png, .gif, .webp, .bmp |
| **PDF** | .pdf |
| **视频** | .mp4, .mpeg, .mov, .avi, .webm, .mkv, .flv, .wmv, .3gp |
| **音频** | .mp3, .wav, .aac, .ogg, .flac, .m4a, .wma |

**文件大小限制**：20MB（base64 编码后约 27MB）

## 工具参考

| 参数 | 默认值 | 说明 |
|------|--------|------|
| file_path | - | 要分析的文件路径（必填） |
| goal | - | 分析目标（必填） |
| cd | - | 工作目录（必填） |
| sandbox | read-only | 沙箱策略（只读） |
| timeout | 120 | API 超时（秒） |
| max_retries | 1 | 自动重试次数 |

## 分析能力

| 文件类型 | 分析能力 |
|----------|----------|
| **PDF** | 提取文本、表格、结构、特定章节内容 |
| **图片** | 描述布局、UI 元素、文本、颜色方案 |
| **视频** | 描述场景、动作、对话、关键帧 |
| **音频** | 转录内容、识别说话者、描述音效 |
| **图表** | 解释数据趋势、关系、关键数据点 |
| **架构图** | 解释组件关系、数据流、系统边界 |
| **截图** | 识别错误信息、UI 状态、功能区域 |

## Prompt 模板

### PDF 分析

```
file_path: "/path/to/document.pdf"
goal: "提取文档中关于用户认证的所有内容"
```

### 图片描述

```
file_path: "/path/to/screenshot.png"
goal: "描述这个 UI 界面的布局和主要元素"
```

### 视频分析

```
file_path: "/path/to/video.mp4"
goal: "分析这个视频的主要场景和内容"
```

### 音频转录

```
file_path: "/path/to/audio.mp3"
goal: "转录这段音频的对话内容"
```

### 图表解读

```
file_path: "/path/to/chart.png"
goal: "解释这个图表显示的数据趋势和关键发现"
```

### 架构图分析

```
file_path: "/path/to/architecture.png"
goal: "解释这个系统架构的组件关系和数据流向"
```

### 错误识别

```
file_path: "/path/to/error-screenshot.png"
goal: "识别截图中的错误信息"
```

## 返回值

```json
// 成功
{
  "success": true,
  "tool": "looker",
  "SESSION_ID": "uuid-string",
  "file_analyzed": "/absolute/path/to/file",
  "file_type": "PDF/图片/视频/音频",
  "result": "<analysis>...</analysis>\n<extracted>...</extracted>\n<summary>...</summary>",
  "duration": "0m20s",
  "token_usage": {
    "prompt": 1234,
    "response": 567,
    "total": 1801
  }
}

// 失败
{
  "success": false,
  "tool": "looker",
  "error": "错误信息",
  "error_kind": "file_not_found | file_too_large | unsupported_format | config_error | timeout | api_error | ..."
}
```

## 输出格式

Looker 返回结构化分析结果：

```
<analysis>
**文件类型**: [PDF/图片/视频/音频/图表/架构图/截图]
**分析目标**: [用户请求提取的内容]
</analysis>

<extracted>
[提取的具体内容]
- 如果是 PDF：文本、表格、结构
- 如果是图片：描述、UI 元素
- 如果是视频：场景描述、关键帧
- 如果是音频：转录内容、音效描述
- 如果是图表：数据、趋势
</extracted>

<summary>
[简要总结，便于主代理使用]
</summary>
```

## 适合使用

- 媒体文件无法作为纯文本读取
- 需要从文档中提取特定信息或摘要
- 需要描述图片、视频或图表中的视觉内容
- 需要转录或分析音频内容
- 需要分析/提取的数据，而非原始文件内容

## 不适合使用

| 场景 | 替代方案 |
|------|----------|
| 源代码或纯文本文件 | 使用 Read 工具 |
| 需要后续编辑的文件 | 使用 Read 工具获取字面内容 |
| 简单文件读取 | 使用 Read 工具 |
| 需要读取多个文件 | 分别调用多次 Looker |
| 需要执行命令 | 使用 Coder 或其他工具 |

## 配置要求

Looker 需要在配置文件中配置 Gemini API：

```toml
# ~/.omcc-mcp/config.toml

[looker]
# API Key（必填）- Gemini API Key 或兼容的 API Key
api_key = "your-gemini-api-key"

# API 地址（可选，默认使用 Google 官方地址）
base_url = "https://generativelanguage.googleapis.com"

# 模型名称（可选，默认 gemini-3-flash-preview）
model = "gemini-3-flash-preview"
```

## 工作原则

1. **直接返回**：提取的信息无需前言
2. **明确缺失**：如果未找到信息，说明缺少什么
3. **匹配语言**：使用请求的语言回复
4. **目标详尽**：在分析目标上详尽，其他方面简洁
5. **承认限制**：如果无法完成任务（需要 MCP 工具或其他文件），明确告知
