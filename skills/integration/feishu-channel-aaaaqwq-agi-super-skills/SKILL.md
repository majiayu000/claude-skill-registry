---
name: feishu-channel
description: 飞书 (Lark/Feishu) 与 OpenClaw 的双向集成通道。通过飞书机器人实现消息的接收和发送，支持私聊、群聊、@提及检测、卡片消息、文件传输。当需要通过飞书与 AI 助手交互、接收飞书消息触发 AI 响应、或从 OpenClaw 发送消息到飞书时使用此技能。与 feishu-automation 的区别：本 skill 专注于消息通道集成，feishu-automation 专注于飞书平台自动化操作（多维表格、文档等）。
allowed-tools: mcp__lark-mcp_*, Bash, Read, Write, Edit
---

# 飞书 Channel 集成

将飞书接入 OpenClaw，实现双向消息通道。

## 与 feishu-automation 的区别

| 特性 | feishu-channel | feishu-automation |
|------|----------------|-------------------|
| **主要用途** | 消息通道集成 | 平台自动化操作 |
| **消息接收** | ✅ Webhook 事件订阅 | ❌ 不支持 |
| **消息发送** | ✅ 实时对话 | ✅ 通知推送 |
| **多维表格** | ❌ 不涉及 | ✅ 完整支持 |
| **文档管理** | ❌ 不涉及 | ✅ 完整支持 |
| **适用场景** | AI 对话机器人 | 数据同步、自动化工作流 |

## 架构概述

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   飞书用户   │ ←→  │   飞书开放平台    │ ←→  │  OpenClaw   │
│  (私聊/群聊) │     │   (Webhook)      │     │   Gateway   │
└─────────────┘     └──────────────────┘     └─────────────┘
                           ↓
                    ┌──────────────────┐
                    │   Webhook 服务    │
                    │   - 事件验证      │
                    │   - 消息解析      │
                    │   - 格式转换      │
                    └──────────────────┘
```

## 核心组件

### 1. 飞书机器人应用

在飞书开放平台创建的企业自建应用，负责：
- 接收用户消息（通过事件订阅）
- 发送消息（通过消息 API）
- 管理权限和安全

### 2. Webhook 服务

接收飞书事件推送，转发给 OpenClaw Gateway。

### 3. 消息发送 API

通过 lark-mcp 工具或直接调用飞书 API 发送消息。

## 快速开始

### 前置条件

- 飞书开放平台账号
- 企业自建应用（机器人能力）
- OpenClaw Gateway 运行中
- 公网可访问的 Webhook URL（或使用内网穿透）

### 1. 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 添加「机器人」能力
4. 配置权限（见下方权限列表）
5. 获取 App ID 和 App Secret

### 2. 配置事件订阅

1. 在应用管理页面，进入「事件订阅」
2. 配置请求地址：`https://your-domain.com/webhook/feishu`
3. 订阅事件：
   - `im.message.receive_v1` - 接收消息
   - `im.message.message_read_v1` - 消息已读（可选）

### 3. 部署 Webhook 服务

```bash
cd /home/aa/clawd/skills/feishu-channel
npm install
cp .env.example .env
# 编辑 .env 填入配置
npm start
```

### 4. 发布应用

1. 在飞书开放平台提交审核
2. 审核通过后发布
3. 在飞书中搜索并添加机器人

## 配置说明

### 环境变量 (.env)

```env
# 飞书应用配置 (必需)
FEISHU_APP_ID=cli_xxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx

# 事件订阅验证 Token
FEISHU_VERIFICATION_TOKEN=xxxxxxxxxxxxxxxx
# 事件加密 Key (可选，推荐启用)
FEISHU_ENCRYPT_KEY=xxxxxxxxxxxxxxxx

# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789
OPENCLAW_WEBHOOK_SECRET=your_webhook_secret

# 安全配置
# 允许的用户 open_id (逗号分隔，留空允许所有)
ALLOWED_USERS=ou_xxx,ou_yyy
# 允许的群聊 chat_id (逗号分隔，留空允许所有)
ALLOWED_GROUPS=oc_xxx,oc_yyy

# 群聊行为
REQUIRE_MENTION_IN_GROUP=true

# 服务端口
PORT=3002

# 日志级别
LOG_LEVEL=info
```

### 飞书应用权限

| 权限 | 说明 | 必需 |
|------|------|------|
| `im:message` | 获取与发送单聊、群组消息 | ✅ |
| `im:message.group_at_msg` | 接收群聊中@机器人消息 | ✅ |
| `im:message.p2p_msg` | 接收用户发给机器人的单聊消息 | ✅ |
| `im:chat` | 获取群组信息 | 推荐 |
| `contact:user.base` | 获取用户基本信息 | 推荐 |
| `im:resource` | 获取与上传图片或文件资源 | 可选 |

### OpenClaw 配置 (openclaw.json)

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxxxxxxxxx",
      "appSecret": "env:FEISHU_APP_SECRET",
      "webhookUrl": "https://your-domain.com/webhook/feishu",
      "dmPolicy": "allowlist",
      "allowFrom": ["ou_xxx", "ou_yyy"],
      "groups": {
        "oc_xxx": {
          "name": "工作群",
          "requireMention": true
        }
      }
    }
  }
}
```

## 消息格式

### 接收消息 (Webhook Event)

飞书原始事件格式：

```json
{
  "schema": "2.0",
  "header": {
    "event_id": "xxx",
    "event_type": "im.message.receive_v1",
    "create_time": "1706745600000",
    "token": "verification_token",
    "app_id": "cli_xxx"
  },
  "event": {
    "sender": {
      "sender_id": {
        "open_id": "ou_xxx",
        "user_id": "xxx",
        "union_id": "on_xxx"
      },
      "sender_type": "user"
    },
    "message": {
      "message_id": "om_xxx",
      "root_id": "",
      "parent_id": "",
      "create_time": "1706745600000",
      "chat_id": "oc_xxx",
      "chat_type": "group",
      "message_type": "text",
      "content": "{\"text\":\"@_user_1 你好\"}",
      "mentions": [
        {
          "key": "@_user_1",
          "id": {
            "open_id": "ou_bot"
          },
          "name": "OpenClaw助手"
        }
      ]
    }
  }
}
```

转换后的 OpenClaw 格式：

```json
{
  "type": "message",
  "channel": "feishu",
  "messageId": "om_xxx",
  "from": {
    "id": "ou_xxx",
    "name": "张三"
  },
  "chat": {
    "id": "oc_xxx",
    "type": "group",
    "name": "工作群"
  },
  "text": "你好",
  "mentions": ["ou_bot"],
  "isMentioned": true,
  "timestamp": 1706745600000
}
```

### 发送消息

#### 使用 lark-mcp 工具

```javascript
// 发送文本消息
await mcp__lark-mcp_sendMessage({
  receive_id: "ou_xxx",  // 或 oc_xxx (群聊)
  receive_id_type: "open_id",  // 或 chat_id
  msg_type: "text",
  content: JSON.stringify({
    text: "收到，正在处理..."
  })
});

// 发送富文本消息
await mcp__lark-mcp_sendMessage({
  receive_id: "oc_xxx",
  receive_id_type: "chat_id",
  msg_type: "post",
  content: JSON.stringify({
    zh_cn: {
      title: "任务完成",
      content: [
        [
          { tag: "text", text: "已完成 " },
          { tag: "a", text: "查看详情", href: "https://example.com" }
        ]
      ]
    }
  })
});

// 发送卡片消息
await mcp__lark-mcp_sendMessage({
  receive_id: "oc_xxx",
  receive_id_type: "chat_id",
  msg_type: "interactive",
  content: JSON.stringify({
    config: { wide_screen_mode: true },
    header: {
      template: "turquoise",
      title: { content: "通知", tag: "plain_text" }
    },
    elements: [
      {
        tag: "div",
        text: { content: "**重要通知**", tag: "lark_md" }
      },
      {
        tag: "action",
        actions: [
          {
            tag: "button",
            text: { content: "确认", tag: "plain_text" },
            type: "primary"
          }
        ]
      }
    ]
  })
});
```

#### 使用 HTTP API

```bash
# 发送文本消息
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxx",
    "msg_type": "text",
    "content": "{\"text\":\"Hello!\"}"
  }'
```

## 安全策略

### 事件验证

飞书事件订阅支持两种验证方式：

1. **Verification Token**: 简单的 Token 验证
2. **Encrypt Key**: AES 加密（推荐）

```javascript
// 验证示例
function verifyEvent(body, token) {
  if (body.token !== token) {
    throw new Error('Invalid verification token');
  }
}

// 解密示例
function decryptEvent(encrypt, key) {
  const crypto = require('crypto');
  const decipher = crypto.createDecipheriv(
    'aes-256-cbc',
    crypto.createHash('sha256').update(key).digest(),
    Buffer.alloc(16, 0)
  );
  return JSON.parse(
    decipher.update(encrypt, 'base64', 'utf8') + decipher.final('utf8')
  );
}
```

### 私聊策略

| 策略 | 说明 |
|------|------|
| `open` | 允许所有人私聊（危险） |
| `allowlist` | 仅允许 allowFrom 列表中的用户 |

### 群聊策略

| 配置 | 说明 |
|------|------|
| `requireMention: true` | 必须@机器人才响应 |
| `allowFrom` | 群内允许触发的用户列表 |

## 使用场景

### 1. 智能问答机器人

```
用户: @OpenClaw助手 帮我查一下今天的会议安排
Bot: 今天的会议安排：
- 10:00 产品评审会 (会议室A)
- 14:00 技术分享会 (线上)
- 16:00 周例会 (会议室B)
```

### 2. 工作流通知

```javascript
// 当任务完成时发送通知
await mcp__lark-mcp_sendMessage({
  receive_id: "oc_work_group",
  receive_id_type: "chat_id",
  msg_type: "interactive",
  content: JSON.stringify({
    header: {
      template: "green",
      title: { content: "✅ 任务完成", tag: "plain_text" }
    },
    elements: [
      {
        tag: "div",
        text: { content: "数据同步任务已完成\n处理记录: 1,234 条", tag: "lark_md" }
      }
    ]
  })
});
```

### 3. 审批流程

```
用户: @OpenClaw助手 提交请假申请，明天休息一天
Bot: 已收到请假申请，正在提交审批...
     [卡片消息: 请假申请详情 + 审批按钮]
```

## 故障排查

### Webhook 无法接收消息

1. 检查 Webhook URL 是否公网可访问
2. 检查 Verification Token 是否正确
3. 查看飞书开放平台的事件推送日志
4. 确认应用已发布且用户已添加机器人

### 消息发送失败

1. 检查 App ID 和 App Secret
2. 确认应用权限已开启
3. 检查 access_token 是否过期
4. 查看 API 返回的错误码

### 权限不足

1. 在飞书开放平台检查应用权限
2. 确认权限已审核通过
3. 重新获取 access_token

## 限制说明

### 飞书平台限制

- API 调用频率限制（参考官方文档）
- 消息长度限制
- 文件大小限制

### 功能限制

- 不支持语音消息
- 卡片消息交互需要额外配置回调
- 部分高级功能需要企业认证

## 相关文件

- `scripts/feishu-webhook.js` - Webhook 服务代码
- `.env.example` - 环境变量模板
- `references/feishu-api.md` - 飞书 API 参考
- `references/message-types.md` - 消息类型说明

## TODO

- [ ] 创建飞书应用并获取凭证
- [ ] 配置事件订阅
- [ ] 部署 Webhook 服务
- [ ] 测试私聊消息收发
- [ ] 测试群聊 @提及
- [ ] 配置安全策略
- [ ] 实现卡片消息交互
