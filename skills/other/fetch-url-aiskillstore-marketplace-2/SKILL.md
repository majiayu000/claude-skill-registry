---
name: fetch-url
description: 渲染网页 URL，去噪提取正文并输出为 Markdown（默认）或其他格式/原始 HTML，以减少 Token。
---

在当前文件所在目录运行：`./scripts/fetch_url.py URL`（仅支持 `http` / `https`）。  
说明：必须直接当作可执行文件执行。

默认自动探测本地 Chromium 系浏览器路径；未探测到时需安装 Playwright 浏览器：

```bash
uv run playwright install chromium
```

参数：
- `--output`：将输出写入文件（默认 stdout）。
- `--timeout-ms`：Playwright 导航超时（毫秒，默认 60000）。
- `--browser-path`：指定本地 Chromium 系浏览器路径（默认自动探测）。
- `--output-format`：输出格式（默认 `markdown`），支持 `csv`、`html`、`json`、`markdown`、`raw-html`、`txt`、`xml`、`xmltei`；`raw-html` 直接输出渲染后的 HTML（不经 trafilatura）。

示例：

```bash
./scripts/fetch_url.py https://example.com --output ./page.md --timeout-ms 60000
```

Reference：[`scripts/fetch_url.py`](scripts/fetch_url.py)
