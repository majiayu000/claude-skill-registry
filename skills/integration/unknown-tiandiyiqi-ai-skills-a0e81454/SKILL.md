---
name: connect
description: Connect Claude to any app. Send emails, create issues, post messages, update databases - take real actions across Gmail, Slack, GitHub, Notion, and 1000+ services.
---

# 连接

将Claude连接到任何应用程序。停止生成关于你能做什么的文本——直接去做。

## 何时使用此技能

当您需要Claude执行以下操作时使用此技能：

- **发送邮件** 而非起草邮件
- **创建问题** 而非描述问题
- **发布消息** 而非建议消息
- **更新数据库** 而非解释如何更新

## 带来的变化

| 没有连接时 | 使用连接时 |
|------------|------------|
| "这是一封草拟邮件..." | 发送邮件 |
| "您应该创建一个问题..." | 创建问题 |
| "发布到Slack..." | 直接发布 |
| "添加到Notion..." | 直接添加 |

## 支持的应用

**1000+集成**，包括：

- **邮件：** Gmail、Outlook、SendGrid
- **聊天：** Slack、Discord、Teams、Telegram
- **开发：** GitHub、GitLab、Jira、Linear
- **文档：** Notion、Google Docs、Confluence
- **数据：** Sheets、Airtable、PostgreSQL
- **CRM：** HubSpot、Salesforce、Pipedrive
- **存储：** Drive、Dropbox、S3
- **社交：** Twitter、LinkedIn、Reddit

## 设置

### 1. 获取API密钥

在[platform.composio.dev](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills)获取您的免费密钥

### 2. 设置环境变量

```bash
export COMPOSIO_API_KEY="your-key"
```

### 3. 安装

```bash
pip install composio          # Python
npm install @composio/core    # TypeScript
```

完成。Claude现在可以连接到任何应用。

## 示例

### 发送邮件
```
Email sarah@acme.com - Subject: "已发货！" Body: "v2.0已上线，有问题请告诉我"
```

### 创建GitHub问题
```
在my-org/repo中创建问题："移动端超时bug"，标签：bug
```

### 发布到Slack
```
发布到#engineering："部署完成 - v2.4.0已上线"
```

### 链式操作
```
查找本周标记为"bug"的GitHub问题，总结后发布到Slack的#bugs频道
```

## 工作原理

使用Composio工具路由器：

1. **您要求**Claude执行某操作
2. **工具路由器查找**正确的工具（1000+选项）
3. **OAuth处理**自动完成
4. **操作执行**并返回结果

### 代码

```python
from composio import Composio
from claude_agent_sdk.client import ClaudeSDKClient
from claude_agent_sdk.types import ClaudeAgentOptions
import os

composio = Composio(api_key=os.environ["COMPOSIO_API_KEY"])
session = composio.create(user_id="user_123")

options = ClaudeAgentOptions(
    system_prompt="您可以在外部应用执行操作。",
    mcp_servers={
        "composio": {
            "type": "http",
            "url": session.mcp.url,
            "headers": {"x-api-key": os.environ["COMPOSIO_API_KEY"]},
        }
    },
)

async with ClaudeSDKClient(options) as client:
    await client.query("发送Slack消息到#general：您好！")
```

## 认证流程

首次使用某个应用时：
```
要发送邮件，我需要Gmail访问权限。
在此授权：https://...
授权完成后说"已连接"。
```

之后连接会保持。

## 框架支持

| 框架 | 安装命令 |
|------|----------|
| Claude Agent SDK | `pip install composio claude-agent-sdk` |
| OpenAI Agents | `pip install composio openai-agents` |
| Vercel AI | `npm install @composio/core @composio/vercel` |
| LangChain | `pip install composio-langchain` |
| 任何MCP客户端 | 使用 `session.mcp.url` |

## 故障排除

- **需要授权** → 点击链接，授权后说"已连接"
- **操作失败** → 检查目标应用中的权限
- **找不到工具** → 具体说明：如"Slack #general"而非"发送消息"

---

<p align="center">
  <b>加入20,000+开发者的行列，构建能够交付的代理</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="开始使用"/>
  </a>
</p>
