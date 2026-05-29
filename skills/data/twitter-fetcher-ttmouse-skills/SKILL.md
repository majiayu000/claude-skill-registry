---
name: twitter-fetcher
description: 统一的推文内容获取技能。支持单条/批量推文提取，输出结构化数据。当用户提供 Twitter/X 链接并希望获取内容时自动触发。
---

# Twitter Fetcher

统一的推文内容获取基础技能，供其他技能调用或直接使用。

## 触发条件

- 用户提供 x.com 或 twitter.com 链接
- 用户说"获取推文"、"提取推文内容"、"抓取这条推文"
- 其他技能需要获取推文内容时

## 使用方式

### 命令行

```bash
cd /Users/douba/.claude/skills/twitter-fetcher

# 单条推文
node scripts/fetch.js "https://x.com/user/status/123456"

# 批量推文（从文件读取）
node scripts/fetch.js --file urls.txt

# 指定输出格式
node scripts/fetch.js "https://x.com/..." --format json
node scripts/fetch.js "https://x.com/..." --format markdown
node scripts/fetch.js "https://x.com/..." --format text

# 保存到文件
node scripts/fetch.js "https://x.com/..." --output /tmp/tweet.json
```

### 作为模块调用

```javascript
const { fetchTweet, fetchTweets } = require('/Users/douba/.claude/skills/twitter-fetcher/scripts/fetch.js');

// 单条
const tweet = await fetchTweet('https://x.com/user/status/123');

// 批量
const tweets = await fetchTweets(['url1', 'url2', 'url3']);
```

## 输出格式

### JSON（默认）

```json
{
  "success": true,
  "data": {
    "url": "https://x.com/dotey/status/2007197068394164613",
    "author": {
      "name": "宝玉",
      "handle": "dotey"
    },
    "content": "推文正文内容...",
    "timestamp": "2026-01-03T05:07:00Z",
    "metrics": {
      "views": "288K",
      "likes": "1.3K",
      "retweets": "216",
      "replies": "49"
    },
    "images": [],
    "quotedTweet": null,
    "extractedAt": "2026-01-20T10:30:00Z"
  }
}
```

### Markdown

```markdown
# @dotey - 宝玉

> 2026-01-03 05:07

推文正文内容...

---
Views: 288K | Likes: 1.3K | Retweets: 216 | Replies: 49
Source: https://x.com/dotey/status/2007197068394164613
```

### Text

纯文本，只包含推文正文。

## 技术实现

- 使用 Playwright headless 浏览器
- 无需登录即可获取公开推文
- 自动等待内容渲染（5-8秒）
- 多选择器策略，提高提取成功率

## 登录态（可选）

对于需要登录才能查看的推文：

### 方式 1：连接已登录的 Chrome

```bash
# 先启动 Chrome 调试端口
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# 使用 --cdp 参数
node scripts/fetch.js "https://x.com/..." --cdp
```

### 方式 2：使用保存的登录态

```bash
# 首次：保存登录态
node scripts/fetch.js --save-auth

# 后续：使用保存的登录态
node scripts/fetch.js "https://x.com/..." --use-auth
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Timeout | 网络慢或页面加载失败 | 重试或增加 --timeout |
| Empty content | 推文被删除或需要登录 | 使用 --cdp 或 --use-auth |
| Rate limited | 请求过于频繁 | 等待后重试 |

## 与其他技能的关系

本技能是基础能力，供以下技能调用：

- `twitter-collector` - 批量采集时调用
- `twitter-cleaner` - 清洗时获取完整内容
- `twitter-to-obsidian` - 保存笔记时获取内容
- `notebooklm` - 添加 Twitter 源时获取内容

## 依赖

```bash
cd /Users/douba/.claude/skills/twitter-fetcher
npm install
```

需要 Playwright 和 Chromium：
```bash
npm install playwright
npx playwright install chromium
```
