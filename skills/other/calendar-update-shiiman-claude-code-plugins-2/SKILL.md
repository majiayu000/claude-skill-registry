---
name: calendar-update
description: Google Calendar の予定を更新する。「予定を変更」「イベント編集」「予定を修正」「日程変更」「時間を変える」「場所を変更」などで起動。
allowed-tools: [Read, Bash]
---

# Calendar Update

Google Calendar の予定を更新します。

## 引数

- イベントID (必須): 更新する予定のID

## オプション

- `--calendar <id>`: カレンダーID（デフォルト: primary）
- `--summary <title>`: 新しいタイトル
- `--start <datetime>`: 新しい開始日時 (ISO 8601形式)
- `--end <datetime>`: 新しい終了日時 (ISO 8601形式)
- `--location <place>`: 新しい場所
- `--description <text>`: 新しい説明
- `--color <1-11>`: 新しい色ID

## 実行方法

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_calendar.py update --event-id <event-id> --summary "新しいタイトル"
```

### 日時を変更

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_calendar.py update --event-id <event-id> --start 2025-01-08T15:00:00 --end 2025-01-08T16:00:00
```
