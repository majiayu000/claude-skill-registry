---
name: wechat-article-reader
description: >
  微信公众号文章抓取与阅读助手。当用户分享微信公众号链接（mp.weixin.qq.com）
  并希望阅读、总结、翻译或讨论文章内容时触发。
  触发词：读公众号文章、抓取微信文章、read wechat article
allowed-tools: Read, Bash, Write, Glob, Grep, WebFetch, Agent
model: sonnet
---

# 微信公众号文章抓取与阅读助手

通过 Playwright 无头浏览器抓取微信公众号文章全文，支持后续阅读、总结、翻译等操作。

## 触发条件

用户消息中包含 `mp.weixin.qq.com` 链接，且意图为阅读/总结/讨论文章内容。

## 工作流程

### 第 1 步：环境检查与依赖安装

在执行抓取前，确保 Playwright 可用：

```bash
# 检查 node_modules 中是否有 playwright
ls node_modules/playwright 2>/dev/null || npm install playwright
```

> 注意：Playwright 需要 Chromium 浏览器内核。首次使用时可能需要运行 `npx playwright install chromium`。

### 第 2 步：执行抓取

调用抓取脚本，脚本位于本 skill 目录下：

```bash
node <skill-dir>/scripts/fetch.mjs "<微信文章URL>"
```

脚本输出格式：

```
---META---
{"title":"...","author":"...","date":"...","imageCount":N}
---TEXT---
文章正文内容...
---IMAGES---
[1] alt: url
[2] alt: url
```

### 第 3 步：内容处理

根据用户意图处理抓取到的内容：

| 用户意图 | 处理方式 |
|---------|---------|
| 阅读/查看 | 直接展示标题、作者、正文摘要 |
| 总结 | 提取核心观点，生成结构化摘要 |
| 翻译 | 将中文内容翻译为目标语言 |
| 讨论/分析 | 基于文章内容进行深度分析 |
| 保存 | 将内容保存为本地 markdown 文件 |

## 核心规则

1. **URL 识别**：仅处理 `mp.weixin.qq.com` 域名的链接
2. **失败处理**：如果脚本返回 `ERROR: 被微信反爬拦截`，告知用户稍后重试或手动复制内容
3. **内容展示**：默认展示标题、作者、发布日期和正文摘要，不要一次性输出全部正文（除非用户要求）
4. **超时控制**：给 Bash 命令设置 60 秒超时
5. **临时依赖**：如果当前目录没有 playwright，在临时目录安装后执行

## 错误处理

| 错误 | 原因 | 应对 |
|------|------|------|
| 环境异常 | 被微信反爬检测拦截 | 建议用户稍后重试，或手动复制文章内容 |
| 超时 | 网络问题或页面加载慢 | 重试一次，仍失败则告知用户 |
| playwright 未安装 | 缺少依赖 | 自动安装 `npm install playwright` |
| 空内容 | 文章可能已删除或需要登录 | 告知用户文章不可访问 |

## 注意事项

- 此工具仅用于个人阅读用途，不用于批量爬取
- 微信反爬策略可能变化，无法保证 100% 成功
- 抓取的图片为微信 CDN 链接，可能有防盗链，直接访问可能失败
