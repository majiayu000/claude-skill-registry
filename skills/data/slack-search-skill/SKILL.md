---
name: slack-search
description: |
  Slackチャンネルやメッセージをセマンティック検索する。
  BookRAGに基づく階層的インデックスを活用した検索機能を提供。
  以下のようなリクエストで使用:
  - 「Slackで〜を検索」「〜のチャンネルを探して」
  - 「〜さんの発言を探して」「〜に関連するチャンネル」
  - 「DX展示会のチャンネル」「プロジェクトの状況」
  - 「最近のイベント」「12月のアクティビティ」
---

# Slack Search Skill

BookRAGに基づく階層的インデックスを活用したSlackセマンティック検索。

## クイックスタート

```python
import sys
sys.path.insert(0, '/Users/kou1904/githubactions_fordata/cursor_tools')
from slack_search import SlackSearch

search = SlackSearch()

# ワークスペース概要
overview = search.get_workspace_overview()

# チャンネル検索（セマンティック検索）
results = search.find_channels("DX展示会")

# チャンネル詳細
detail = search.get_channel_detail("infobox/buyingshift")

# 関連チャンネル探索
related = search.find_related_channels("infobox/buyingshift")

# 人物検索
persons = search.find_person("清水")

# イベント検索
events = search.find_events("DX")

# タイムライン検索
timeline = search.get_timeline("2025-12-01", "2025-12-31")
```

## 利用可能な検索機能

### 1. ワークスペース概要 (`get_workspace_overview`)

全体の統計情報とカテゴリ構造を取得。

```python
# 全ワークスペース
overview = search.get_workspace_overview()

# 特定のワークスペース
overview = search.get_workspace_overview("infobox")
```

**対応ワークスペース**: infobox, yoake, tokenpocket, fungiblex

### 2. チャンネル検索 (`find_channels`)

チャンネル名、トピック、概要からセマンティック検索。

```python
# 基本検索
results = search.find_channels("展示会")

# フィルタ付き検索
results = search.find_channels(
    query="プロジェクト",
    workspace="infobox",
    category="project",
    limit=20
)
```

**チャンネルカテゴリ**:
- `cafe`: 個人チャンネル（cafe_*）
- `project`: プロジェクト（pj_*）
- `product`: プロダクト開発（product_*）
- `sales`: 営業（sales_*）
- `notify`: 通知（notify_*）
- `partner`: 外部パートナー（*_infobox）
- `event`: イベント（日付パターン）
- `external`: 外部連携（ex-*, ext-*）

### 3. チャンネル詳細 (`get_channel_detail`)

特定チャンネルの詳細情報を取得。

```python
# フルID指定
detail = search.get_channel_detail("infobox/buyingshift")

# チャンネル名のみでも可
detail = search.get_channel_detail("buyingshift")
```

**返却情報**:
- 概要（overview）
- トピック（topics）
- 参加者（participants）
- 活動期間（first_activity, last_activity）
- ファイルパス（data, summary, archive）
- 関連チャンネル（related_channels）

### 4. 関連チャンネル探索 (`find_related_channels`)

グラフ構造に基づいて関連チャンネルを探索。

```python
# 直接関連
related = search.find_related_channels("buyingshift")

# 間接関連まで（depth=2）
related = search.find_related_channels("buyingshift", depth=2)
```

### 5. 人物検索 (`find_person`)

発言者やメンションから人物を検索。

```python
results = search.find_person("清水")
# 返却: 名前、エイリアス、参加チャンネル数、チャンネルリスト
```

### 6. イベント検索 (`find_events`)

展示会、会議などのイベントを検索。

```python
# 全イベント
events = search.find_events()

# キーワード検索
events = search.find_events("DX")
```

### 7. カテゴリ別一覧 (`list_channels_by_category`)

特定カテゴリのチャンネルを一覧。

```python
# 全ワークスペースのcafeチャンネル
cafes = search.list_channels_by_category("cafe")

# infoboxのprojectチャンネルのみ
projects = search.list_channels_by_category("project", workspace="infobox")
```

### 8. タイムライン検索 (`get_timeline`)

期間指定でアクティビティを検索。

```python
timeline = search.get_timeline(
    start_date="2025-12-01",
    end_date="2025-12-31",
    workspace="infobox"  # オプション
)
```

### 9. 出力ソース情報 (`get_output_sources`)

calendar, gmail, drive, voicememoの統計情報。

```python
sources = search.get_output_sources()
```

## データ構造

### インデックスパス
- メインインデックス: `slack-sync/index/book_index.json`
- スキーマ定義: `slack-sync/index/schema.md`

### データソース
- 現在データ: `slack-sync/data/{workspace}/`
- サマリー: `slack-sync/data/summary/{workspace}/`
- アーカイブ: `slack-sync/data/archive/{workspace}/`
- 出力: `output/` (calendar, gmail, drive, voicememo)

## CLIコマンド

```bash
# ワークスペース概要
python3 cursor_tools/slack_search.py overview [workspace]

# チャンネル検索
python3 cursor_tools/slack_search.py find "クエリ"

# チャンネル詳細
python3 cursor_tools/slack_search.py detail "channel_id"

# 関連チャンネル
python3 cursor_tools/slack_search.py related "channel_id"

# 人物検索
python3 cursor_tools/slack_search.py person "名前"

# イベント検索
python3 cursor_tools/slack_search.py events [クエリ]

# カテゴリ別
python3 cursor_tools/slack_search.py category "カテゴリ名"

# タイムライン
python3 cursor_tools/slack_search.py timeline "開始日" "終了日"
```

## インデックス更新

インデックスはGitHub Actionsで毎日自動更新されます。
手動更新:

```bash
python3 slack-sync/scripts/build_book_index.py
```

## ユースケース例

### 「清水さんが参加しているプロジェクトを教えて」

```python
person = search.find_person("清水")[0]
project_channels = [
    ch for ch in person["channels"]
    if search.get_channel_detail(ch).get("category") == "project"
]
```

### 「最近のDX展示会イベントの成果を確認」

```python
events = search.find_events("DX")
for event in events:
    detail = search.get_channel_detail(event["channel"])
    print(f"{event['name']}: {detail['overview']}")
```

### 「buyingshiftに関連する活動を調べる」

```python
detail = search.get_channel_detail("buyingshift")
related = search.find_related_channels("buyingshift", depth=2)
print(f"関連チャンネル数: {related['total_related']}")
```
