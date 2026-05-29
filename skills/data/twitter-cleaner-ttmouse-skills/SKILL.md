---
name: twitter-cleaner
description: 对 Twitter 采集产出进行二次清洗，自动获取完整推文内容并生成可筛选数据。
---

# Twitter 数据清洗器

在完成 twitter-collector 抓取之后，自动将链接导入筛选页面，生成完整推文文本与图片，供后续人工/自动规则筛选使用。

## 使用场景
- 采集阶段仅得到链接和简要文本，需要获取完整推文内容
- 希望在清洗页面里直接复制、再筛选、再导出
- 为 Grok 转换、数据库入库等后续环节准备干净、完整的数据输入

## 工作流程
1. 读取 twitter-collector 生成的链接（txt 或 preview HTML 中勾选项）
2. 打开 `https://twitterhot.vercel.app/tweet-filter.html`
3. 自动粘贴全部链接，触发第三方页面生成图片与完整文本
4. 等待解析完成并抓取页面返回的完整推文内容
5. 保存清洗结果（含全文、图片 URL、原始链接）到本地文件，为预览/筛选页面提供输入

## 使用方式

### 方式 A：MCP 驱动模式（推荐，免配置）
直接指令 AI 执行清洗。AI 会自动调用内置的 `browser` 技能，复用您的 Profile 并在 `twitterhot` 页面自动粘贴和提取数据。
- **优点**：无需手动启动 Chrome 调试端口，全自动化。
- **指令示例**：`@twitter-cleaner 执行清洗，输入文件为 twitter-links-2026-01-18.txt。`

### 方式 B：本地脚本模式（需开启调试端口）
如果您希望在本地终端手动运行：
1. **启动 Chrome 调试端口**：
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```
2. **运行脚本**：
   ```bash
   node scripts/cleaner.js --input /Users/douba/twitter-output/twitter-links-2026-01-18.txt
   ```

## 可用参数
- `--input`: 链接文本文件
- `--preview`: 预览 HTML（解析勾选状态）
- `--filter-url`: 筛选页地址（默认：twitterhot）
- `--output-dir`: 输出目录（默认 `/Users/douba/twitter-output`）
- `--output`: 输出格式（json/preview-html）
- `--browser`: 连接的浏览器调试端口（默认 9222）

## 输出格式
### JSON
```json
{
  "generated_at": "2026-01-14T10:30:00Z",
  "count": 25,
  "items": [
    {
      "url": "https://x.com/user/status/123",
      "text": "完整推文内容……",
      "author": "user",
      "images": ["https://pbs.twimg.com/media/..."],
      "source": "twitterhot",
      "tags": ["自动打标", "筛选用"]
    }
  ]
}
```

### 预览 HTML
生成新的 preview 页面，卡片中展示完整文本、所有图片、筛选标签，可以继续人工勾选。

## 技术实现
1. 通过 Playwright 复用已打开浏览器（绝不自行关闭）
2. 自动访问筛选页面并粘贴链接
3. 轮询页面 DOM，等待第三方解析结果
4. 解析 `data-url`、完整文本、图片等数据
5. 保存为 JSON 或新的 preview 页面，供下一环节使用

## 与现有流程的衔接
```
twitter-collector → twitter-cleaner → grok-json-generator → db-importer
```

- collector：抓取链接
- cleaner：生成完整内容、支持规则筛选
- grok-json-generator：结构化提炼
- db-importer：入库

这样你就能独立地控制“数据清洗”阶段，既保留第三方页面生成的完整文本，又能在预览页面里按规则进行筛选、打标和导出。