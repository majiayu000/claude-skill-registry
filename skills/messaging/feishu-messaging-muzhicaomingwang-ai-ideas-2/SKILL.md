---
name: feishu-messaging
description: |
  飞书消息发送与文档创建工作流。
  触发场景：用户提到"发飞书消息"、"飞书文档"、"通知某人"、"发送到飞书"、"飞书通知"。
  适用于：发送飞书消息、创建飞书文档、操作多维表格、管理知识库。
---

# 飞书消息与文档 Skill

## 概述

此 Skill 通过飞书开放平台 API 帮助用户发送消息、创建文档和管理飞书资源。

## 核心能力

| 功能 | 状态 | 所需权限 |
|------|------|---------|
| 发送文本消息 | ✅ 可用 | `im:message:send_as_bot` |
| 发送富文本消息 | ✅ 可用 | `im:message:send_as_bot` |
| 发送卡片消息 | ✅ 可用 | `im:message:send_as_bot` |
| 获取群聊列表 | ✅ 可用 | `im:chat:readonly` |
| 获取群成员 | ⏳ 待授权 | `im:chat.members:read` |
| 创建飞书文档 | ⏳ 待授权 | `docx:document` |
| 创建多维表格 | ⏳ 待授权 | `bitable:app` |
| 创建知识库页面 | ⏳ 待授权 | `wiki:wiki` |

## 使用方法

### 发送消息给指定用户

```
给 [姓名] 发一条飞书消息，告诉他 [内容]
```

**前置条件**：需要获取用户的 open_id

### 获取用户 open_id 的方法

1. **方法一：通过邮箱/手机号查询**（需要 `contact:user.id:readonly` 权限）
   ```
   用户邮箱：xxx@company.com
   ```

2. **方法二：让用户主动发消息**
   - 用户在飞书中搜索机器人名称
   - 发送任意消息
   - 机器人获取到用户的 open_id

3. **方法三：用户自行查看**
   - 用户在机器人对话中发送 `/myid`
   - 或从飞书开放平台后台查看

### 已知用户 ID 记录

| 姓名 | open_id | 备注 |
|------|---------|------|
| 王植萌 | `ou_18b8063b232cbdec73ea1541dfb74890` | zhimeng.wang@qunar.com |

## 消息类型

### 1. 文本消息

```python
mcp__feishu__im_v1_message_create(
    params={"receive_id_type": "open_id"},
    data={
        "receive_id": "ou_xxx",
        "msg_type": "text",
        "content": '{"text": "Hello World"}'
    }
)
```

### 2. 富文本消息（Post）

支持标题、粗体、链接、@用户等格式。

```python
mcp__feishu__im_v1_message_create(
    params={"receive_id_type": "open_id"},
    data={
        "receive_id": "ou_xxx",
        "msg_type": "post",
        "content": json.dumps({
            "zh_cn": {
                "title": "消息标题",
                "content": [
                    [{"tag": "text", "text": "正文内容"}],
                    [{"tag": "text", "text": "粗体", "style": ["bold"]}],
                    [{"tag": "a", "text": "链接", "href": "https://example.com"}]
                ]
            }
        })
    }
)
```

### 3. 卡片消息（Interactive）

最丰富的消息格式，支持分栏、按钮、图片等。

```python
mcp__feishu__im_v1_message_create(
    params={"receive_id_type": "open_id"},
    data={
        "receive_id": "ou_xxx",
        "msg_type": "interactive",
        "content": json.dumps({
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "卡片标题"},
                "template": "blue"  # blue/green/orange/red/purple
            },
            "elements": [
                {"tag": "markdown", "content": "**支持 Markdown**\n- 列表项1\n- 列表项2"},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": "分栏内容"}}
            ]
        })
    }
)
```

## 标准操作流程

### 发送消息 SOP

```
1. 确认收件人
   ↓ 有 open_id → 直接发送
   ↓ 无 open_id → 获取 open_id（见上述方法）

2. 确认消息类型
   ↓ 简单文本 → text
   ↓ 需要格式 → post
   ↓ 丰富卡片 → interactive

3. 构造消息内容
   ↓ 根据类型构造 JSON

4. 发送消息
   ↓ 调用 im_v1_message_create

5. 确认送达
   ↓ 检查返回的 message_id
```

### 创建文档 SOP（待权限开通）

```
1. 确认文档类型
   ↓ 普通文档 → docx_builtin_import
   ↓ 多维表格 → bitable_v1_app_create
   ↓ 知识库页面 → wiki 相关 API

2. 准备内容
   ↓ Markdown 格式（会自动转换）

3. 创建文档

4. 分享权限（可选）
   ↓ 添加协作者
```

## 权限申请指南

### 飞书应用信息

- **App ID**: `cli_a8831f109ffc500e`
- **应用名称**: zhimeng's Agent
- **管理后台**: https://open.feishu.cn/app/cli_a8831f109ffc500e

### 权限申请链接

| 功能 | 权限 | 申请链接 |
|------|------|---------|
| 查询用户ID | `contact:user.id:readonly` | [申请](https://open.feishu.cn/app/cli_a8831f109ffc500e/auth?q=contact:user.id:readonly) |
| 读取群成员 | `im:chat.members:read` | [申请](https://open.feishu.cn/app/cli_a8831f109ffc500e/auth?q=im:chat.members:read) |
| 读取消息 | `im:message` | [申请](https://open.feishu.cn/app/cli_a8831f109ffc500e/auth?q=im:message) |
| 创建文档 | `docx:document` | [申请](https://open.feishu.cn/app/cli_a8831f109ffc500e/auth?q=docx:document) |
| 多维表格 | `bitable:app` | [申请](https://open.feishu.cn/app/cli_a8831f109ffc500e/auth?q=bitable:app) |
| 知识库 | `wiki:wiki` | [申请](https://open.feishu.cn/app/cli_a8831f109ffc500e/auth?q=wiki:wiki) |

### 一键申请全部

[申请所有常用权限](https://open.feishu.cn/app/cli_a8831f109ffc500e/auth?q=contact:user.id:readonly,im:chat.members:read,im:message,docx:document,bitable:app,wiki:wiki)

## 常见问题

### Q: 消息发送成功但用户没收到？

**可能原因**：
1. 用户未与机器人建立联系 → 让用户先给机器人发消息
2. open_id 不正确 → 确认 open_id 来源
3. 跨租户 → 机器人无法给其他企业用户发消息

### Q: 权限申请不了？

**可能原因**：
1. 机器人版本正在审核中 → 等待审核通过
2. 企业管理员限制 → 联系管理员开通
3. 权限需要特殊审批 → 走企业内部流程

### Q: 如何发送群消息？

使用 `chat_id` 代替 `open_id`：
```python
params={"receive_id_type": "chat_id"},
data={"receive_id": "oc_xxx", ...}
```

## 消息模板

### 能力介绍卡片

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "🤖 Claude Code 能力介绍"},
    "template": "blue"
  },
  "elements": [
    {"tag": "markdown", "content": "Hi，我是 **Claude Code**，一个 AI 编程助手。"},
    {"tag": "div", "text": {"tag": "lark_md", "content": "**💻 开发支持**\n• 代码编写、调试和重构\n• Bug 排查与修复"}},
    {"tag": "div", "text": {"tag": "lark_md", "content": "**📊 项目管理**\n• 飞书文档/多维表格操作\n• Git 提交、PR 创建"}},
    {"tag": "hr"},
    {"tag": "markdown", "content": "有任何需要，随时召唤我！"}
  ]
}
```

### 任务通知卡片

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "📋 任务通知"},
    "template": "green"
  },
  "elements": [
    {"tag": "div", "fields": [
      {"is_short": true, "text": {"tag": "lark_md", "content": "**任务**\n部署上线"}},
      {"is_short": true, "text": {"tag": "lark_md", "content": "**状态**\n✅ 已完成"}}
    ]},
    {"tag": "hr"},
    {"tag": "markdown", "content": "详情请查看 [链接](https://example.com)"}
  ]
}
```

## 注意事项

1. **消息频率限制** - 单用户每分钟最多 5 条消息
2. **内容长度限制** - 卡片消息 body 不超过 30KB
3. **图片需先上传** - 使用 `im/v1/images` 上传后获取 image_key
4. **敏感信息** - 不要在消息中包含密码、token 等敏感信息

## 相关资源

- [飞书开放平台文档](https://open.feishu.cn/document/)
- [消息卡片搭建工具](https://open.feishu.cn/tool/cardbuilder)
- [消息内容格式参考](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json)
