---
name: wechat-channel
description: 微信 (WeChat) 与 OpenClaw 的双向集成通道。基于 Wechaty + PadLocal 实现微信消息的接收和发送，支持私聊、群聊、@提及检测、图片/文件传输。当需要通过微信与 AI 助手交互、接收微信消息触发 AI 响应、或从 OpenClaw 发送消息到微信时使用此技能。
allowed-tools: Bash, Read, Write, Edit
---

# 微信 Channel 集成

将微信接入 OpenClaw，实现双向消息通道。

## 架构概述

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   微信用户   │ ←→  │  Wechaty Bridge  │ ←→  │  OpenClaw   │
│  (私聊/群聊) │     │  (PadLocal协议)   │     │   Gateway   │
└─────────────┘     └──────────────────┘     └─────────────┘
                           ↓
                    ┌──────────────────┐
                    │   消息格式转换    │
                    │   - 文本/图片/文件 │
                    │   - @提及检测     │
                    │   - 群聊/私聊路由  │
                    └──────────────────┘
```

## 核心组件

### 1. Wechaty Bridge (消息桥接服务)

独立运行的 Node.js 服务，负责：
- 微信登录（扫码）
- 消息收发
- 联系人/群组管理
- 与 OpenClaw Gateway 通信

### 2. OpenClaw Webhook 接收器

接收来自 Wechaty Bridge 的消息，转发给 AI Agent。

### 3. 消息发送 API

OpenClaw Agent 通过 HTTP API 发送消息到微信。

## 快速开始

### 前置条件

- Node.js >= 18
- PadLocal Token（付费服务，约 ¥200/月）
- OpenClaw Gateway 运行中

### 1. 安装依赖

```bash
cd /home/aa/clawd/skills/wechat-channel
npm init -y
npm install wechaty wechaty-puppet-padlocal axios dotenv
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入配置
```

### 3. 启动服务

```bash
node scripts/wechat-bridge.js
# 扫描终端显示的二维码登录
```

## 配置说明

### 环境变量 (.env)

```env
# PadLocal Token (必需)
# 获取方式: https://pad-local.com
PADLOCAL_TOKEN=YOUR_PADLOCAL_TOKEN

# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789
OPENCLAW_WEBHOOK_SECRET=your_webhook_secret

# 微信 Bot 配置
WECHAT_BOT_NAME=OpenClaw助手

# 安全配置
# 允许的用户微信ID (逗号分隔，留空允许所有)
ALLOWED_USERS=wxid_xxx,wxid_yyy
# 允许的群聊ID (逗号分隔，留空允许所有)
ALLOWED_GROUPS=xxx@chatroom,yyy@chatroom

# 群聊行为
# 是否需要@才响应群消息
REQUIRE_MENTION_IN_GROUP=true

# 日志级别
LOG_LEVEL=info
```

### OpenClaw 配置 (openclaw.json)

```json
{
  "channels": {
    "wechat": {
      "enabled": true,
      "webhookUrl": "http://localhost:3001/webhook",
      "webhookSecret": "your_webhook_secret",
      "dmPolicy": "allowlist",
      "allowFrom": ["wxid_xxx", "wxid_yyy"],
      "groups": {
        "xxx@chatroom": {
          "name": "工作群",
          "requireMention": true
        }
      }
    }
  }
}
```

## 消息格式

### 接收消息 (Webhook Payload)

```json
{
  "type": "message",
  "channel": "wechat",
  "messageId": "msg_123456",
  "from": {
    "id": "wxid_sender",
    "name": "张三",
    "alias": "zhangsan"
  },
  "chat": {
    "id": "wxid_sender",
    "type": "private"
  },
  "text": "你好，帮我查一下天气",
  "timestamp": 1706745600000,
  "mentions": [],
  "replyTo": null
}
```

### 群聊消息

```json
{
  "type": "message",
  "channel": "wechat",
  "messageId": "msg_789012",
  "from": {
    "id": "wxid_sender",
    "name": "张三"
  },
  "chat": {
    "id": "xxx@chatroom",
    "type": "group",
    "name": "工作群"
  },
  "text": "@OpenClaw助手 帮我总结一下今天的会议",
  "mentions": ["bot_wxid"],
  "isMentioned": true
}
```

### 发送消息 (API)

```bash
# 发送文本
curl -X POST http://localhost:3001/api/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SECRET" \
  -d '{
    "to": "wxid_receiver",
    "type": "text",
    "content": "收到，正在处理..."
  }'

# 发送图片
curl -X POST http://localhost:3001/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "to": "wxid_receiver",
    "type": "image",
    "url": "https://example.com/image.png"
  }'

# 发送文件
curl -X POST http://localhost:3001/api/send \
  -d '{
    "to": "wxid_receiver",
    "type": "file",
    "path": "/path/to/file.pdf",
    "filename": "report.pdf"
  }'
```

## 安全策略

### 私聊策略 (dmPolicy)

| 策略 | 说明 |
|------|------|
| `open` | 允许所有人私聊（危险） |
| `allowlist` | 仅允许 allowFrom 列表中的用户 |
| `pairing` | 需要配对审批 |

### 群聊策略

| 配置 | 说明 |
|------|------|
| `requireMention: true` | 必须@机器人才响应 |
| `allowFrom` | 群内允许触发的用户列表 |

## 使用场景

### 1. 个人助手

```
用户: 帮我查一下明天北京的天气
Bot: 明天北京天气：晴，温度 -5°C ~ 5°C，建议穿羽绒服。
```

### 2. 群聊助手

```
用户: @OpenClaw助手 总结一下刚才的讨论
Bot: 刚才讨论的要点：
1. 项目进度需要加快
2. 下周三前完成设计稿
3. 周五进行代码评审
```

### 3. 自动化通知

```javascript
// 从 OpenClaw Agent 发送通知
await sendWechatMessage({
  to: 'xxx@chatroom',
  text: '⚠️ 服务器 CPU 使用率超过 90%，请检查！'
});
```

## 故障排查

### 登录问题

**问题**: 扫码后无法登录
**解决**: 
1. 检查 PadLocal Token 是否有效
2. 确认微信账号未被限制
3. 尝试重新获取 Token

### 消息收发问题

**问题**: 消息发送失败
**解决**:
1. 检查网络连接
2. 确认目标用户/群组 ID 正确
3. 查看日志中的错误信息

### 连接断开

**问题**: 服务运行一段时间后断开
**解决**:
1. 使用 PM2 管理进程，自动重启
2. 检查 PadLocal 服务状态
3. 实现心跳检测和重连机制

## 限制说明

### PadLocal 限制

- 需要付费 Token（约 ¥200/月）
- 单 Token 只能登录一个微信号
- 可能受微信风控影响

### 微信平台限制

- 发送频率限制（建议间隔 1-2 秒）
- 群聊人数限制
- 文件大小限制（约 100MB）
- 不支持小程序消息

### 功能限制

- 不支持语音消息转文字（需额外集成）
- 不支持视频号内容
- 红包、转账等敏感功能不可用

## 相关文件

- `scripts/wechat-bridge.js` - 主服务代码
- `scripts/message-handler.js` - 消息处理逻辑
- `.env.example` - 环境变量模板
- `references/wechaty-api.md` - Wechaty API 参考

## TODO

- [ ] 获取 PadLocal Token
- [ ] 配置 OpenClaw Webhook 接收
- [ ] 测试私聊消息收发
- [ ] 测试群聊 @提及
- [ ] 配置安全策略
- [ ] 部署为系统服务
- [ ] 实现断线重连
- [ ] 添加消息队列（高并发场景）
