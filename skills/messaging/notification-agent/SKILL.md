---
name: notification-agent
description: Multi-channel notification dispatcher. Sends trading alerts, reports, and system notifications via Telegram, Slack, Email, and WebSocket. Supports urgency-based routing and custom formatting.
license: Proprietary
compatibility: Requires Telegram Bot API, Slack API, SMTP, WebSocket
metadata:
  author: ai-trading-system
  version: "1.0"
  category: system
  agent_role: notifier
---

# Notification Agent - 알림 발송 관리자

## Role
Trading Signal, 리포트, 시스템 알림을 Telegram, Slack, Email, WebSocket을 통해 적절한 채널로 전송합니다.

## Core Capabilities

### 1. Multi-Channel Support

#### Telegram
- **Use Case**: 실시간 거래 Signal, 긴급 알림
- **Format**: Markdown with buttons
- **Priority**: High urgency

#### Slack
- **Use Case**: 팀 협업, 일일 리포트
- **Format**: Rich formatting with attachments
- **Priority**: Medium urgency

#### Email
- **Use Case**: 주간/월간 리포트
- **Format**: HTML with charts
- **Priority**: Low urgency

#### WebSocket
- **Use Case**: Dashboard 실시간 업데이트
- **Format**: JSON
- **Priority**: Real-time

### 2. Urgency-Based Routing

```python
URGENCY_ROUTING = {
    'CRITICAL': ['Telegram', 'Slack', 'WebSocket'],  # 즉시 모든 채널
    'HIGH': ['Telegram', 'WebSocket'],                # 즉시 알림
    'MEDIUM': ['Slack', 'Email'],                     # 배치 발송
    'LOW': ['Email']                                  # 일일 요약에 포함
}
```

### 3. Message Templates

#### Trading Signal Template (Telegram)
```markdown
🎯 **New Trading Signal**

**Ticker**: {ticker}
**Action**: {action}
**Confidence**: {confidence:.0%}
**Source**: {source}

**Reasoning**: {reasoning}

**Target**: ${target_price}
**Stop Loss**: ${stop_loss}

[Approve] [Reject]
```

#### Daily Report Template (Email)
```html
<h1>Daily Trading Report - {date}</h1>

<h2>Performance</h2>
<table>
  <tr><td>Win Rate</td><td>{win_rate:.1%}</td></tr>
  <tr><td>Daily Return</td><td>{return:.2%}</td></tr>
</table>

<h2>Top Signals</h2>
...
```

### 4. Rate Limiting

```python
RATE_LIMITS = {
    'Telegram': 30 / 60,      # 30 messages per minute
    'Slack': 1 / 1,            # 1 message per second
    'Email': 100 / 3600,       # 100 emails per hour
    'WebSocket': None          # No limit
}
```

## Decision Framework

```
Step 1: Receive Notification Request
  - Type: signal, report, alert, error
  - Urgency: critical, high, medium, low
  - Content: message body
  - Recipients: list of users/channels

Step 2: Determine Channels
  Based on urgency:
    CRITICAL → All channels
    HIGH → Telegram + WebSocket
    MEDIUM → Slack + Email
    LOW → Email only

Step 3: Format Message
  For each channel:
    - Apply channel-specific template
    - Format content (Markdown, HTML, JSON)
    - Add buttons/actions if applicable

Step 4: Check Rate Limits
  IF rate limit exceeded:
    → Queue message
    → Send when available

Step 5: Send Notification
  Try:
    send_to_channel(channel, formatted_message)
  Except:
    log_error()
    retry_with_backoff()

Step 6: Track Delivery
  - Log sent time
  - Track delivery status
  - Record user interaction (if applicable)
```

## Output Format

```json
{
  "notification_id": "NOTIF-20251221-001",
  "type": "trading_signal",
  "urgency": "HIGH",
  "content": {
    "ticker": "AAPL",
    "action": "BUY",
    "confidence": 0.85,
    "source": "war_room",
    "reasoning": "Strong consensus...",
    "target_price": 205.00,
    "stop_loss": 195.00
  },
  "channels": ["telegram", "websocket"],
  "recipients": {
    "telegram": ["COMMANDER_CHAT_ID"],
    "websocket": ["active_connections"]
  },
  "sent_at": "2025-12-21T13:00:00Z",
  "delivery_status": {
    "telegram": {
      "status": "sent",
      "message_id": "12345",
      "sent_at": "2025-12-21T13:00:01Z"
    },
    "websocket": {
      "status": "broadcasted",
      "connections": 3,
      "sent_at": "2025-12-21T13:00:00Z"
    }
  }
}
```

## Examples

**Example 1**: 긴급 Trading Signal (CRITICAL)
```
Input:
- Type: trading_signal
- Urgency: CRITICAL
- Content: Emergency FDA approval for MRNA

Channels:
- Telegram: Immediate alert with [Approve] button
- Slack: Rich message with details
- WebSocket: Real-time dashboard update

Output:
- All channels notified within 5 seconds
```

**Example 2**: 일일 리포트 (MEDIUM)
```
Input:
- Type: daily_report
- Urgency: MEDIUM
- Content: Daily performance summary

Channels:
- Slack: Summary card
- Email: Full HTML report

Output:
- Slack: Posted to #trading channel
- Email: Sent to commander@example.com
```

**Example 3**: Circuit Breaker 발동 (CRITICAL)
```
Input:
- Type: emergency_alert
- Urgency: CRITICAL
- Content: Circuit Breaker triggered (Daily Loss > -2%)

Channels:
- Telegram: URGENT alert
- Slack: @channel mention
- Email: High priority

Output:
- Immediate notification to all channels
- Telegram bot calls Commander
```

**Example 4**: WebSocket 실시간 업데이트 (HIGH)
```
Input:
- Type: new_signal
- Urgency: HIGH
- Content: New signal from Deep Reasoning

Channels:
- WebSocket: Broadcast to /trading page

Output:
- Dashboard updates instantly
- No Telegram/Email (not urgent enough for push)
```

## Guidelines

### Do's ✅
- **적절한 채널 선택**: 긴급도에 맞게
- **Rate Limit 준수**: 스팸 방지
- **Clear Formatting**: 읽기 쉽게
- **Action Buttons**: 즉시 조치 가능하게

### Don'ts ❌
- 과도한 알림 금지 (Notification fatigue)
- 중요하지 않은 것을 CRITICAL로 표시 금지
- 에러 메시지를 사용자에게 직접 노출 금지
- Rate limit 초과 금지

## Integration

### Telegram Bot

```python
from backend.notifications.telegram_commander_bot import TelegramCommanderBot

telegram = TelegramCommanderBot(
    bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
    commander_chat_id=os.getenv('TELEGRAM_COMMANDER_CHAT_ID')
)

async def send_telegram_signal(signal: Dict):
    """Send trading signal via Telegram"""
    
    message = f"""
🎯 **New Trading Signal**

**Ticker**: {signal['ticker']}
**Action**: {signal['action']}
**Confidence**: {signal['confidence']:.0%}

**Reasoning**: {signal['reasoning']}

**Target**: ${signal['target_price']}
**Stop Loss**: ${signal['stop_loss']}
"""
    
    # Add approval buttons
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Approve", "callback_data": f"approve_{signal['signal_id']}"},
            {"text": "❌ Reject", "callback_data": f"reject_{signal['signal_id']}"}
        ]]
    }
    
    await telegram.send_message(
        text=message,
        parse_mode='Markdown',
        reply_markup=keyboard
    )
```

### WebSocket Broadcast

```python
from fastapi import WebSocket

active_connections: List[WebSocket] = []

async def broadcast_signal(signal: Dict):
    """Broadcast signal to all connected clients"""
    
    message = {
        "type": "new_signal",
        "data": signal
    }
    
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            active_connections.remove(connection)
```

### Email Report

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_report(report_html: str, recipient: str):
    """Send HTML email report"""
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Daily Trading Report - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = os.getenv('SMTP_FROM')
    msg['To'] = recipient
    
    html_part = MIMEText(report_html, 'html')
    msg.attach(html_part)
    
    with smtplib.SMTP(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
        server.send_message(msg)
```

### Slack Integration

```python
from slack_sdk.webhook import WebhookClient

slack = WebhookClient(os.getenv('SLACK_WEBHOOK_URL'))

def send_slack_report(report: Dict):
    """Send report to Slack"""
    
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"📊 Daily Report - {report['date']}"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Win Rate:*\n{report['win_rate']:.1%}"},
                {"type": "mrkdwn", "text": f"*Return:*\n{report['return']:.2%}"}
            ]
        }
    ]
    
    slack.send(blocks=blocks)
```

## Rate Limiting Implementation

```python
from collections import deque
from time import time

class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
    
    def allow(self) -> bool:
        """Check if call is allowed"""
        now = time()
        
        # Remove old calls
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()
        
        # Check limit
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        
        return False

# Usage
telegram_limiter = RateLimiter(max_calls=30, period=60)

if telegram_limiter.allow():
    await send_telegram_message(msg)
else:
    queue_message(msg)  # Send later
```

## Performance Metrics

- **Delivery Success Rate**: > 99%
- **Latency (CRITICAL)**: < 5 seconds
- **Latency (HIGH)**: < 30 seconds
- **Rate Limit Violations**: 0

## Notification Queue

```python
from queue import PriorityQueue

notification_queue = PriorityQueue()

# Priority: CRITICAL=1, HIGH=2, MEDIUM=3, LOW=4
notification_queue.put((1, critical_notification))
notification_queue.put((3, medium_notification))

# Worker processes queue
while True:
    priority, notification = notification_queue.get()
    send_notification(notification)
```

## Version History

- **v1.0** (2025-12-21): Initial release with Telegram, Slack, Email, WebSocket support
