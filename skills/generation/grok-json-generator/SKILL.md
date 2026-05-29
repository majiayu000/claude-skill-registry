---
name: grok-json-generator
description: 将 Twitter 链接列表转换为 Grok 生成的结构化 JSON 数据。
---

# Grok JSON 生成器

将 Twitter 链接列表转换为 Grok 生成的结构化 JSON 数据。

## 使用场景

当你完成 Twitter 筛选后，有一批选中的链接需要转换为结构化数据录入数据库时使用。

## 工作流程

1. **输入链接列表**：通过命令行参数或文件输入
2. **打开 Grok 对话**：自动访问固定的 Grok 聊天界面
3. **自动填写内容**：将链接填入 Grok 聊天
4. **触发结构化提取**：使用固定提示词让 Grok 生成结构化 JSON
5. **保存输出**：将生成的 JSON 保存到文件

## 快速开始

### 前置要求

1. Grok 账号已登录
2. 浏览器已打开 Grok 聊天界面
3. 固定的 Grok 聊天 URL（需要你提供）

### 运行方式

```bash
# 基础使用
node scripts/grok-generator.js --links "https://x.com/link1 https://x.com/link2"

# 从文件读取链接
node scripts/grok-generator.js --input-file /Users/douba/twitter-output/twitter-links-2026-01-13.txt

# 指定输出目录
node scripts/grok-generator.js --links "https://x.com/link1 https://x.com/link2" --output-dir /Users/douba/twitter-output
```

## 可用参数

- `--links`: 链接列表（空格分隔）
- `--input-file`: 从文件读取链接
- `--grok-url`: Grok 聊天 URL（固定对话）
- `--prompt`: 自定义提示词（可选，有默认）
- `--output-dir`: 输出目录（默认：/Users/douba/twitter-output）
- `--browser`: 连接的浏览器（default: http://localhost:9222）

## 输出格式

### JSON 结构

```json
{
  "generated_at": "2026-01-13T10:00:00Z",
  "total_links": 10,
  "data": [
    {
      "url": "https://x.com/user/status/123456789",
      "title": "推文标题",
      "content": "推文内容",
      "author": "用户名",
      "tags": ["标签1", "标签2"],
      "metadata": {
        "likes": 100,
        "retweets": 50,
        "images": ["图片URL1", "图片URL2"]
      }
    }
  ]
}
```

## 实现方式

1. 使用 Playwright 连接到已打开的浏览器
2. 访问 Grok 聊天 URL
3. 等待页面加载
4. 将链接以文本形式粘贴到 Grok 输入框
5. 等待生成完成
6. 解析页面获取 JSON 输出
7. 保存到文件

## 配置

```javascript
const CONFIG = {
  grokUrl: 'https://x.com/i/grok', // 需要你提供固定对话 URL
  defaultPrompt: '请将以下 Twitter 链接转换为结构化 JSON 格式，包括标题、内容、作者、标签、互动数据等。',
  timeout: 30000, // 30秒超时
  waitTime: 2000 // 每次检查间隔 2 秒
};
```

## 注意事项

- 需要你提供固定的 Grok 聊天 URL
- 支持断点续跑（从上次处理位置继续）
- 失败重试机制
- 详细的日志输出

## 示例输出

```
✅ Grok JSON 生成器启动...

🔗 输入链接: 10 条
🌐 连接到浏览器...
💬 访问 Grok 聊天...

⏳ 等待生成...
✅ 生成完成

📊 总计: 10 条
💾 保存到: /Users/douba/twitter-output/grok-data-2026-01-13.json
📁 文件路径: /Users/douba/twitter-output/grok-data-2026-01-13.json
```

## 下一步

生成 JSON 后，可以使用 `db-importer` 技能将数据录入数据库。
