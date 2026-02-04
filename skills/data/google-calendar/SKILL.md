---
name: google-calendar
description: |
  gogcli (gog) を使用してGoogle Calendarを操作するスキル。予定の一覧表示、検索、作成、更新、削除、招待への応答などをCLI経由で実行。
  Use when: (1) 今日の予定を確認したい、(2) 予定を作成したい、(3) カレンダーを確認したい、(4) ミーティングを設定したい、(5) 空き時間を確認したい、(6) 予定を検索したい
  Trigger: calendar, カレンダー, 予定, スケジュール, ミーティング, 会議, meeting, schedule, 空き時間
---

# Google Calendar Operations with gogcli

`gog` CLIを使用してGoogle Calendarを操作する。

## Prerequisites

```bash
# Installation
brew install gogcli

# Authentication (初回のみ)
gog auth login
```

## Commands Reference

### List Events

```bash
# 今日の予定
gog calendar events --today

# 明日の予定
gog calendar events --tomorrow

# 今週の予定
gog calendar events --week

# 今後N日間の予定
gog calendar events --days=7

# 日付範囲を指定
gog calendar events --from="2024-02-01" --to="2024-02-28"

# 相対的な指定
gog calendar events --from="today" --to="friday"

# 全カレンダーの予定
gog calendar events --all

# 特定カレンダーの予定
gog calendar events <calendarId>

# 最大件数指定
gog calendar events --max=20
```

### Search Events

```bash
# イベント検索
gog calendar search "ミーティング"

# 日付範囲付き検索
gog calendar search "定例" --from="today" --days=30

# 今週の検索
gog calendar search "報告" --week
```

### Create Events

```bash
# 基本的なイベント作成
gog calendar create primary \
  --summary="ミーティング" \
  --from="2024-02-10T14:00:00+09:00" \
  --to="2024-02-10T15:00:00+09:00"

# 詳細付きイベント
gog calendar create primary \
  --summary="プロジェクト定例" \
  --from="2024-02-10T14:00:00+09:00" \
  --to="2024-02-10T15:00:00+09:00" \
  --description="議題: 進捗確認" \
  --location="会議室A"

# 参加者を追加
gog calendar create primary \
  --summary="チームMTG" \
  --from="2024-02-10T14:00:00+09:00" \
  --to="2024-02-10T15:00:00+09:00" \
  --attendees="user1@example.com,user2@example.com"

# Google Meetを自動作成
gog calendar create primary \
  --summary="オンラインMTG" \
  --from="2024-02-10T14:00:00+09:00" \
  --to="2024-02-10T15:00:00+09:00" \
  --with-meet

# 終日イベント
gog calendar create primary \
  --summary="休暇" \
  --from="2024-02-10" \
  --to="2024-02-11" \
  --all-day

# 繰り返しイベント
gog calendar create primary \
  --summary="週次定例" \
  --from="2024-02-10T10:00:00+09:00" \
  --to="2024-02-10T11:00:00+09:00" \
  --rrule="RRULE:FREQ=WEEKLY;BYDAY=MO"

# リマインダー付き
gog calendar create primary \
  --summary="重要MTG" \
  --from="2024-02-10T14:00:00+09:00" \
  --to="2024-02-10T15:00:00+09:00" \
  --reminder="popup:30m" \
  --reminder="email:1d"
```

### Update Events

```bash
# イベントを更新
gog calendar update primary <eventId> \
  --summary="新しいタイトル"

# 時間を変更
gog calendar update primary <eventId> \
  --from="2024-02-10T15:00:00+09:00" \
  --to="2024-02-10T16:00:00+09:00"
```

### Delete Events

```bash
# イベントを削除
gog calendar delete primary <eventId>

# 確認なしで削除
gog calendar delete primary <eventId> --force
```

### Respond to Invitations

```bash
# 承諾
gog calendar respond primary <eventId> --status="accepted"

# 辞退
gog calendar respond primary <eventId> --status="declined"

# 仮承諾
gog calendar respond primary <eventId> --status="tentative"

# コメント付き
gog calendar respond primary <eventId> \
  --status="accepted" \
  --comment="参加します"
```

### Free/Busy Check

```bash
# 空き時間を確認
gog calendar freebusy "primary" \
  --from="2024-02-10T09:00:00+09:00" \
  --to="2024-02-10T18:00:00+09:00"

# 複数カレンダーの空き確認
gog calendar freebusy "user1@example.com,user2@example.com" \
  --from="2024-02-10T09:00:00+09:00" \
  --to="2024-02-10T18:00:00+09:00"
```

### Calendar Management

```bash
# カレンダー一覧
gog calendar calendars

# カレンダーの色一覧
gog calendar colors

# 予定の競合を確認
gog calendar conflicts --from="today" --days=7
```

### Special Events

```bash
# フォーカスタイム（集中時間）
gog calendar focus-time \
  --from="2024-02-10T09:00:00+09:00" \
  --to="2024-02-10T12:00:00+09:00"

# 不在（Out of Office）
gog calendar out-of-office \
  --from="2024-02-10" \
  --to="2024-02-12"

# 勤務場所の設定
gog calendar working-location \
  --from="2024-02-10" \
  --to="2024-02-10" \
  --type="home"
```

## Common Workflows

### 今日の予定を確認

```bash
gog calendar events --today
```

### 来週の予定を確認

```bash
gog calendar events --from="monday" --to="friday"
```

### 会議を設定（Meet付き）

```bash
gog calendar create primary \
  --summary="打ち合わせ" \
  --from="2024-02-10T14:00:00+09:00" \
  --to="2024-02-10T15:00:00+09:00" \
  --attendees="participant@example.com" \
  --with-meet \
  --send-updates="all"
```

## Output Formats

| Flag | Description |
|------|-------------|
| `--json` | JSON形式で出力（スクリプト向け） |
| `--plain` | TSV形式で出力（パース容易） |
| (default) | 人間が読みやすい形式 |

## Tips

- `primary` は自分のメインカレンダー
- `--account=email@example.com` で複数アカウントを切り替え
- 時刻はRFC3339形式（例: `2024-02-10T14:00:00+09:00`）
- 相対指定が便利: `today`, `tomorrow`, `monday`, etc.
- `--send-updates="all"` で参加者に通知を送信
