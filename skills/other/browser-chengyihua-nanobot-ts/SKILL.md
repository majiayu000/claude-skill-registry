---
name: browser
description: 浏览器自动化技能。支持打开网页、网页截图、搜索、提取内容、填写表单、点击元素等。当用户要求“打开网页”、“搜索”、“爬取数据”、“点击按钮”、“截图”或“自动化操作浏览器”时使用。
metadata: {"nanobot":{"emoji":"🌐","requires":{"bins":["playwright"]},"install":[{"id":"pip","kind":"pip","package":"playwright","bins":["playwright"],"label":"Install Playwright (pip)"},{"id":"playwright-install","kind":"command","command":"playwright install chromium","label":"Install Chromium (playwright)"}]}}
---

# 浏览器自动化技能 (Browser Automation)

使用 Playwright 进行浏览器操作。模型应优先使用此技能执行任何与 Web 相关的任务。

## 核心指令 (Core Commands)

你必须通过 `runCommand` 调用以下脚本。**注意：脚本路径是相对于项目根目录的。**

### 1. 打开网页并截图 (Open & Screenshot)
**用法**: `python skills/browser/scripts/open_url.py --url "<URL>" [选项]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `--url` | **必填**。要访问的完整 URL。 | `https://example.com` |
| `--screenshot` | 截图保存的路径。 | `output/screenshot.png` |
| `--wait` | 页面加载后的等待时间（秒）。默认 3。 | `--wait 5` |
| `--headless` | 是否使用无头模式。默认 `True`。调试时可设为 `False`。 | `--headless False` |

### 2. 搜索 (Search)
**用法**: `python skills/browser/scripts/search.py --query "<关键词>" [选项]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `--query` | **必填**。搜索关键词。 | `Python 教程` |
| `--engine` | 搜索引擎：`baidu` (默认), `google`, `bing`。 | `--engine google` |
| `--limit` | 返回结果的数量。默认 10。 | `--limit 5` |

### 3. 获取/爬取内容 (Get Content)
**用法**: `python skills/browser/scripts/get_content.py --url "<URL>" [选项]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `--url` | **必填**。页面 URL。 | `https://news.ycombinator.com` |
| `--selector` | 可选。提取特定元素的 CSS 选择器。 | `--selector "h2.title"` |
| `--format` | 输出格式：`text` (默认), `html`, `json`。 | `--format json` |

### 4. 填写表单 (Fill Form)
**用法**: `python skills/browser/scripts/fill_form.py --url "<URL>" --data '<JSON_DATA>'`

| 参数 | 说明 | 示例 |
|---|---|---|
| `--url` | 包含表单的 URL。 | `https://example.com/login` |
| `--data` | **必填**。字段名和值的 JSON 对象。 | `'{"user":"admin","pass":"123"}'` |

### 5. 点击元素 (Click)
**用法**: `python skills/browser/scripts/click_element.py --url "<URL>" --selector "<CSS_SELECTOR>"`

---

## 最佳实践 (Best Practices)

1. **路径规范**: 始终使用从根目录开始的路径：`python skills/browser/scripts/...`。
2. **多步操作**: 如果需要登录后操作，应先运行 `fill_form.py`，然后运行 `click_element.py` 或 `get_content.py`。
3. **调试**: 如果操作失败，尝试设置 `--headless False`（如果环境支持显示器）或查看脚本输出的错误信息。
4. **等待**: 动态加载的网页请适当增加 `--wait` 时间。

## 示例场景 (Examples)

### 场景 A：搜索并提取第一个结果的内容
1. `python skills/browser/scripts/search.py --query "OpenAI news" --limit 1`
2. 获取结果中的 URL 后：`python skills/browser/scripts/get_content.py --url "https://..."`

### 场景 B：登录网站
1. `python skills/browser/scripts/fill_form.py --url "https://site.com/login" --data '{"username":"myuser","password":"mypassword"}'`