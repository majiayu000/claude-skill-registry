---
name: batch-notification
description: 批量向用户发送IM消息。用于通知特定用户群体、筛选表格数据后发送、全员通知等场景。当管理员请求批量通知、群发消息、表格筛选后通知时使用此
  Skill。触发词：通知/发送/群发 + 用户/批量/表格。
---

---
name: batch-notification
description: Send IM messages to users in batch. Used for notifying specific user groups, sending after table filtering, all-staff notifications, etc. Use this Skill when administrators request batch notifications, mass messaging, or notifications after table filtering. Trigger words: notify/send/mass + users/batch/table.
---

# Batch User Notification

Support administrators to send IM notification messages to users in batch.

## Typical Scenarios

1. **Upload table + filter conditions**: Notify all users with benefits points greater than 0
2. **Upload target list**: Notify specified user list
3. **All-staff notification**: Notify everyone

## Quick Start

### All-staff Notification
```python
mcp__{channel}__send_markdown_message(
    touser="@all",
    content="## Notification Title\n\nNotification content..."
)
```

### Filtered Notification
```bash
python3 -c "
import pandas as pd
mapping = pd.read_excel('knowledge_base/企业管理/人力资源/user_mapping.xlsx')
business = pd.read_excel('/tmp/data.xlsx')
filtered = business[business['积分'] > 0]
result = pd.merge(filtered, mapping, on='工号', how='inner')
print('|'.join(result['企业微信用户ID'].tolist()))
"
```

## Detailed Workflow

Complete 5-stage workflow, see [WORKFLOW.md](WORKFLOW.md)

## pandas Query Patterns

Common filtering, JOIN, date processing patterns, see [PANDAS_PATTERNS.md](PANDAS_PATTERNS.md)

## Example Scenarios

Complete end-to-end examples, see [EXAMPLES.md](EXAMPLES.md)

## Core Principles

1. **Privacy protection**: Notifications are one-on-one private chats, messages must not contain other people's information
2. **Must confirm**: Must wait for administrator reply "confirm send" after constructing message
3. **Python first**: All table processing uses pandas
4. **Result transparency**: Clearly report sending results (success/failure counts)

## Available Tools

- **Bash**: Execute pandas scripts
- **mcp__{channel}__send_markdown_message**: Send Markdown messages
- **mcp__{channel}__send_text_message**: Send plain text messages
