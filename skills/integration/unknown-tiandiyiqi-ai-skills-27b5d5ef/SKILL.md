---
name: connect-apps
description: Connect Claude to external apps like Gmail, Slack, GitHub. Use this skill when the user wants to send emails, create issues, post messages, or take actions in external services.
---

# 连接应用

将Claude连接到1000+应用。真正发送邮件、创建问题、发布消息——而非仅仅生成文本。

## 快速开始

### 步骤1：安装插件

```
/plugin install composio-toolrouter
```

### 步骤2：运行设置

```
/composio-toolrouter:setup
```

这将：
- 询问您的免费API密钥（在[platform.composio.dev](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills)获取）
- 配置Claude与1000+应用的连接
- 耗时约60秒

### 步骤3：尝试一下！

设置完成后，重启Claude Code并尝试：

```
发送测试邮件到 YOUR_EMAIL@example.com
```

如果成功，说明已连接！

## 您可以做什么

| 要求Claude... | 结果 |
|---------------|------|
| "发送邮件给sarah@acme.com，关于发布" | 真正发送邮件 |
| "创建GitHub问题：修复登录bug" | 创建问题 |
| "发布到Slack #general：部署完成" | 发布消息 |
| "添加会议记录到Notion" | 添加到Notion |

## 支持的应用

**邮件：** Gmail、Outlook、SendGrid
**聊天：** Slack、Discord、Teams、Telegram
**开发：** GitHub、GitLab、Jira、Linear
**文档：** Notion、Google Docs、Confluence
**数据：** Sheets、Airtable、PostgreSQL
**还有1000+更多...**

## 工作原理

1. 您要求Claude执行某操作
2. Composio工具路由器找到正确的工具
3. 首次使用？您将通过OAuth授权（一次性）
4. 操作执行并返回结果

## 故障排除

- **"插件未找到"** → 确保您运行了 `/plugin install composio-toolrouter`
- **"需要授权"** → 点击Claude提供的OAuth链接，然后说"完成"
- **操作失败** → 检查您在目标应用中的权限

---

<p align="center">
  <b>加入20,000+开发者的行列，构建能够交付的代理</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="开始使用"/>
  </a>
</p>
