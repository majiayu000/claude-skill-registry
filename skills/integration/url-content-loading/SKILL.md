---
name: url-content-loading
description: A URL content loading tool that extracts text or metadata from URLs across multiple platforms (YouTube, PTT, Twitter/X, Truth Social, Reddit, GitHub, and more). Use this when you need to load and extract content from social posts, videos, documents, or code repositories for scraping, data extraction, or content analysis.
---

## How to load URL content

```shell
# Explicit loader selection
uvx kabigon --loader playwright https://example.com
uvx kabigon --loader httpx https://example.com
uvx kabigon --loader firecrawl https://example.com
uvx kabigon --loader youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ
uvx kabigon --loader youtube-ytdlp https://www.youtube.com/watch?v=dQw4w9WgXcQ
uvx kabigon --loader ytdlp https://www.youtube.com/watch?v=dQw4w9WgXcQ
uvx kabigon --loader twitter https://x.com/howie_serious/status/1917768568135115147
uvx kabigon --loader truthsocial https://truthsocial.com/@realDonaldTrump/posts/115830428767897167
uvx kabigon --loader reddit https://reddit.com/r/confession/comments/1q1mzej/im_a_developer_for_a_major_food_delivery_app_the/
uvx kabigon --loader ptt https://www.ptt.cc/bbs/Gossiping/M.1746078381.A.FFC.html
uvx kabigon --loader reel https://www.instagram.com/reel/CuA0XYZ1234/
uvx kabigon --loader github https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md
uvx kabigon --loader pdf https://example.com/document.pdf
```

```shell
# Compose loaders in order
# Example: try YouTube first, then fall back to `youtube-ytdlp` if captions are missing.
# `youtube-ytdlp` can download audio and transcribe it via Whisper.
uvx kabigon --loader youtube,youtube-ytdlp https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

```shell
# If you are not sure which loader to use, rely on the default pipeline.
uvx kabigon https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

```shell
# List supported loaders
uvx kabigon --list
```

## Troubleshooting

- Install `uv` if `uvx` is not found:
  ```text
  https://docs.astral.sh/uv/getting-started/installation/
  ```
