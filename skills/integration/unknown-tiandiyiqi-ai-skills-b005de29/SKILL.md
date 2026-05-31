---
name: youtube-downloader
description: 下载 YouTube 视频，支持自定义质量和格式选项。当用户要求下载、保存或获取 YouTube 视频时使用此技能。支持多种质量设置（最佳、1080p、720p、480p、360p）、多种格式（mp4、webm、mkv）以及仅音频下载为 MP3。
---

# YouTube 视频下载器

完全控制质量和格式设置下载 YouTube 视频。

## 快速开始

下载视频的最简单方法：

```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

这会将视频以最佳可用质量下载为 MP4 到 `/mnt/user-data/outputs/`。

## 选项

### 质量设置

使用 `-q` 或 `--quality` 指定视频质量：

- `best`（默认）：最高可用质量
- `1080p`：全高清
- `720p`：高清
- `480p`：标清
- `360p`：较低质量
- `worst`：最低可用质量

示例：
```bash
python scripts/download_video.py "URL" -q 720p
```

### 格式选项

使用 `-f` 或 `--format` 指定输出格式（仅视频下载）：

- `mp4`（默认）：兼容性最好
- `webm`：现代格式
- `mkv`：Matroska 容器

示例：
```bash
python scripts/download_video.py "URL" -f webm
```

### 仅音频

使用 `-a` 或 `--audio-only` 仅下载音频为 MP3：

```bash
python scripts/download_video.py "URL" -a
```

### 自定义输出目录

使用 `-o` 或 `--output` 指定不同的输出目录：

```bash
python scripts/download_video.py "URL" -o /path/to/directory
```

## 完整示例

1. 以 1080p 下载视频为 MP4：
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 1080p
```

2. 仅下载音频为 MP3：
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a
```

3. 以 720p 下载为 WebM 到自定义目录：
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 720p -f webm -o /custom/path
```

## 工作原理

该技能使用 `yt-dlp`，这是一个强大的 YouTube 下载器，它：
- 如果不存在自动安装自身
- 在下载前获取视频信息
- 选择符合你标准的最佳可用流
- 在需要时合并视频和音频流
- 支持广泛的 YouTube 视频格式

## 重要说明

- 默认情况下下载保存到 `/mnt/user-data/outputs/`
- 视频文件名根据视频标题自动生成
- 脚本自动处理 yt-dlp 的安装
- 仅下载单个视频（默认跳过播放列表）
- 较高质量的视频可能需要更长时间下载并使用更多磁盘空间
