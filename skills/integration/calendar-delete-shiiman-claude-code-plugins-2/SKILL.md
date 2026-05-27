---
name: calendar-delete
description: Google Calendar の予定を削除する。「予定を削除」「イベント削除」「予定をキャンセル」「予定を消して」「イベントを消して」などで起動。
allowed-tools: [Read, Bash]
---

# Calendar Delete

Google Calendar の予定を削除します。

## 引数

- イベントID (必須): 削除する予定のID

## オプション

- `--calendar <id>`: カレンダーID（デフォルト: primary）

## 実行方法

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_calendar.py delete --event-id <event-id>
```

### 特定のカレンダーから削除

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_calendar.py delete --event-id <event-id> --calendar work@group.calendar.google.com
```
