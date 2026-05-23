---
name: calendar-events
description: Google Calendar の予定を取得する。「今日の予定」「今週の予定」「今月の予定」「カレンダー予定」「スケジュール確認」などで起動。期間を指定可能。
allowed-tools: [Read, Bash]
---

# Calendar Events

Google Calendar の予定を今日/週/月で取得します。

## 実行方法

### 今日の予定

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py --range today
```

### 今週の予定

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py --range week
```

### 今月の予定

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py --range month
```

### JSON 形式で出力

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py --format json --range today
```

### カレンダー一覧を取得

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py calendars
```

### 色一覧を表示

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py colors
```

## 期間の解釈

ユーザーの発言から期間を解釈:

- 「今日の予定」→ `--range today`
- 「今週の予定」「週の予定」→ `--range week`
- 「今月の予定」「月の予定」→ `--range month`
- 指定なしの場合 → `--range today`

## 出力項目

- start: 開始日時
- end: 終了日時
- summary: 予定名
- location: 場所
