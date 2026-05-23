---
name: calendar-add
description: Google Calendar に予定を追加する。「予定追加」「カレンダーに追加」「予定を入れて」「スケジュール登録」「予定作成」などで起動。
allowed-tools: [Bash]
---

# Calendar Add

Google Calendar に新しい予定を追加します。

## 実行方法

### 予定を追加

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py add --summary "会議" --start "2025-01-08T14:00:00" --end "2025-01-08T15:00:00"
```

### カレンダーと色を指定して追加

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py add --summary "ランチ" --start "2025-01-08T12:00:00" --end "2025-01-08T13:00:00" --calendar "primary" --color 6 --location "レストラン"
```

### 終日イベント

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py add --summary "休暇" --start "2025-01-10" --end "2025-01-11" --all-day
```

### カレンダー一覧取得

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py calendars
```

### 色一覧表示

```bash
python plugins/shiiman-google/skills/calendar-events/scripts/google_calendar.py colors
```

## 色ID対応表

| ID | 色 |
|----|-----|
| 1 | ラベンダー |
| 2 | セージ |
| 3 | ぶどう |
| 4 | フラミンゴ |
| 5 | バナナ |
| 6 | みかん |
| 7 | ピーコック |
| 8 | グラファイト |
| 9 | ブルーベリー |
| 10 | バジル |
| 11 | トマト |

## ユーザー入力の解釈

ユーザーが自然言語で日時を指定した場合、ISO 8601 形式に変換してスクリプトを呼び出す:

| ユーザー入力 | 変換結果（例: 今日が 2025-01-07 の場合） |
|------------|----------------------------------------|
| 明日 14:00-15:00 | --start 2025-01-08T14:00:00 --end 2025-01-08T15:00:00 |
| 来週月曜 10:00 から 1時間 | --start 2025-01-13T10:00:00 --end 2025-01-13T11:00:00 |
| 今週金曜 終日 | --start 2025-01-10 --end 2025-01-11 --all-day |

## 必要な情報

- **予定タイトル** (必須): 予定の名前
- **開始日時** (必須): いつから
- **終了日時** (必須): いつまで
- カレンダー: どのカレンダーに追加するか（省略時: primary）
- 色: 予定の色（1-11）
- 場所: 場所
- 説明: 詳細な説明

## 出力項目

- id: イベントID
- summary: 予定タイトル
- start: 開始日時
- end: 終了日時
- calendar: カレンダー名
- color: 色（指定時）
- location: 場所（指定時）
- url: カレンダーで開くURL
