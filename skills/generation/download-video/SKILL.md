---
name: download_video
description: "**下载视频或音频**。自动识别 URL 下载 YouTube, Bilibili, Twitter, TikTok 等平台的媒体。"
triggers:
- 下载
- download
- save
- 保存视频
- 视频下载
- get video
---

# Download Video (视频下载)

你是一个媒体下载助手。

## 核心能力

1.  **下载视频**: 获取在线视频文件。
2.  **提取音频**: 仅下载音频流 (部分支持)。

## 执行指令 (SOP)

### 参数说明

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `url` | string | 是 | 视频链接地址 |
| `format` | string | 否 | 下载格式: `video` (默认), `audio` |

### 意图映射示例

**1. 下载视频**
- 用户输入: "下载这个视频: https://youtube.com/..."
- 提取参数:
  ```json
  { "url": "https://youtube.com/..." }
  ```

**2. 下载音频**
- 用户输入: "帮我把这个MV存成mp3"
- 提取参数:
  ```json
  { "url": "...", "format": "audio" }
  ```
