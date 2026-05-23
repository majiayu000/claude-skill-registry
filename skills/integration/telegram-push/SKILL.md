# Telegram Push Skill

通过独立的 Telegram Bot 推送消息到群聊或私聊，不依赖 OpenClaw 的 telegram channel 配置。

## 使用场景

- 推送新闻/通知到 Telegram 群
- 定时任务推送
- 独立于主 bot 的消息发送

## 配置

Bot 信息存储在 `pass` 中：
- Token: `pass tokens/telegram-newsrobot`
- Bot: @fkkanfnnfbot (NewsRobot)

### 已配置的群组

| 群名 | Chat ID | 说明 |
|------|---------|------|
| DailyNews | -1003824568687 | 新闻推送群 |

## 使用方法

### 1. 发送文本消息

```bash
curl -s -X POST "https://api.telegram.org/bot$(pass tokens/telegram-newsrobot)/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": -1003824568687,
    "text": "消息内容",
    "parse_mode": "HTML"
  }'
```

### 2. 发送 Markdown 消息

```bash
curl -s -X POST "https://api.telegram.org/bot$(pass tokens/telegram-newsrobot)/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": -1003824568687,
    "text": "*标题*\n\n内容",
    "parse_mode": "MarkdownV2"
  }'
```

### 3. 发送带按钮的消息

```bash
curl -s -X POST "https://api.telegram.org/bot$(pass tokens/telegram-newsrobot)/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": -1003824568687,
    "text": "消息内容",
    "reply_markup": {
      "inline_keyboard": [[
        {"text": "按钮1", "url": "https://example.com"},
        {"text": "按钮2", "callback_data": "action1"}
      ]]
    }
  }'
```

### 4. 发送图片

```bash
curl -s -X POST "https://api.telegram.org/bot$(pass tokens/telegram-newsrobot)/sendPhoto" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": -1003824568687,
    "photo": "https://example.com/image.jpg",
    "caption": "图片说明"
  }'
```

## 辅助脚本

### telegram-push.sh

```bash
#!/bin/bash
# 快速推送消息到 DailyNews 群
# 用法: telegram-push.sh "消息内容"

TOKEN=$(pass tokens/telegram-newsrobot)
CHAT_ID="-1003824568687"
MESSAGE="$1"

curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": ${CHAT_ID}, \"text\": \"${MESSAGE}\"}"
```

## 添加新群组

1. 把 @fkkanfnnfbot 加入目标群
2. 在群里发一条消息
3. 获取 chat_id:
   ```bash
   curl -s "https://api.telegram.org/bot$(pass tokens/telegram-newsrobot)/getUpdates" | jq '.result[-1].message.chat'
   ```
4. 更新本文档的群组列表

## 注意事项

- 超级群的 chat_id 以 `-100` 开头
- 普通群升级为超级群后 chat_id 会变化，API 会返回 `migrate_to_chat_id`
- 发送频率限制：同一群每分钟约 20 条
- HTML 模式支持: `<b>`, `<i>`, `<code>`, `<pre>`, `<a href="">`

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| chat not found | Bot 未加入群 | 把 bot 加入群 |
| migrate_to_chat_id | 群升级为超级群 | 使用返回的新 chat_id |
| bot was blocked | 用户屏蔽了 bot | 无法发送，需用户解除屏蔽 |
