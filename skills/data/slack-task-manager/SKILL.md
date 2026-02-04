---
name: slack-task-manager
description: |
  Slack検索・TODO抽出・タスク管理を行うサブエージェント。
  複数データソースからタスクを抽出し、優先順位付けを行う。
  「Slackを検索」「タスクを抽出」「TODO確認」「メンション確認」等のリクエストで発動。
triggers:
  - Slackを検索
  - Slack検索
  - チャンネルを探して
  - メンションを確認
  - TODO抽出
  - タスク抽出
  - タスク一覧
  - 未対応タスク
  - 依頼事項
---

# Slack/Task Manager サブエージェント

Slack検索・TODO抽出・タスク管理を専用コンテキストで実行するサブエージェント。

## 目的

Slackデータとタスク管理をメインエージェントのコンテキストから分離し：
- 大量のSlackメッセージ検索を効率化
- 複数データソースからのタスク抽出を統合
- 検索結果のサマリーのみを返却

## 機能一覧

| 機能 | スクリプト | 説明 |
|-----|----------|------|
| Slack検索 | `slack_search.py` | BookRAGベースのセマンティック検索 |
| TODO抽出 | `extract_todos.py` | メンションからTODO抽出・ステータス判定 |
| タスク抽出 | `extract_tasks.py` | 複数ソースからタスク抽出 |

## 1. Slack検索 (`cursor_tools/slack_search.py`)

BookRAGに基づく階層的インデックスを活用したセマンティック検索。

### 機能

| メソッド | 説明 |
|---------|------|
| `get_workspace_overview()` | ワークスペース全体の概要 |
| `find_channels(query)` | チャンネル検索 |
| `get_channel_detail(channel_id)` | チャンネル詳細 |
| `find_related_channels(channel_id)` | 関連チャンネル検索 |
| `find_person(name)` | 人物検索 |

### 使用方法（Python）

```python
from cursor_tools.slack_search import SlackSearch

search = SlackSearch()

# ワークスペース概要
overview = search.get_workspace_overview()

# チャンネル検索
results = search.find_channels("DX展示会")

# チャンネル詳細
detail = search.get_channel_detail("infobox/buyingshift")

# 関連チャンネル
related = search.find_related_channels("infobox/buyingshift")

# 人物検索
person = search.find_person("清水")
```

### 検索例

```python
# プロジェクト関連のチャンネルを探す
results = search.find_channels("AIチュートリアル")

# 特定の人物が関わるチャンネル
person = search.find_person("田中")
```

## 2. TODO抽出 (`.claude/skills/slack-todo-extractor/scripts/extract_todos.py`)

Slackのメンションからタスクを抽出し、ステータス判定を行う。

### 使用方法

```bash
# 基本（キーワードベース）
python .claude/skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "Kohei,minicoohei" \
  --period "2026-01-06:2026-01-08"

# LLMベース（高精度、要GEMINI_API_KEY）
python .claude/skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "Kohei,minicoohei" \
  --period "1/6:8" \
  --use-llm

# JSON出力
python .claude/skills/slack-todo-extractor/scripts/extract_todos.py \
  -u "Kohei" -p "1/6:8" --use-llm -o json
```

### パラメータ

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| `--users`, `-u` | ✅ | 対象ユーザー名（カンマ区切り） | `Kohei, minicoohei` |
| `--period`, `-p` | ✅ | 検索期間 | `2026-01-06:2026-01-08` or `1/6:8` |
| `--workspace`, `-w` | ❌ | ワークスペース | `yoake`, `fungiblex` |
| `--use-llm` | ❌ | LLM（Gemini）で判定 | - |
| `--output`, `-o` | ❌ | 出力形式 | `markdown` or `json` |

### ステータス判定

| ステータス | 条件 |
|-----------|------|
| ✅ 完了 | 対象ユーザーが「完了」等 / 依頼者が「ありがとう」等 |
| 🟡 対応中 | 対象ユーザーが「承知」「やります」等 |
| 🔴 未対応 | 返信なし |

## 3. タスク抽出 (`cursor_tools/extract_tasks.py`)

複数のデータソースから自動的にタスクを抽出・優先順位付け。

### データソース

| ソース | 説明 |
|--------|------|
| Git | 変更ファイル、未コミット作業 |
| Activity Logger | 最近のアクティビティ |
| SpecStory | 仕掛かりタスク |
| Slack-sync | 依頼事項、メンション |
| Output | カレンダー、Gmail、ボイスメモ |
| Notion | データベース/ページ |

### 使用方法

```bash
# 全ソースからタスク抽出
python cursor_tools/extract_tasks.py

# 特定ソースのみ
python cursor_tools/extract_tasks.py --sources git,slack

# HowToDo生成付き
python cursor_tools/extract_tasks.py --with-howtodo

# HTML出力
python cursor_tools/extract_tasks.py --format html --output tasks.html
```

### 出力形式

```yaml
tasks:
  - id: task_001
    source: slack
    title: "EASソリューションの調査"
    priority: high
    status: pending
    due_date: "2026-01-10"
    assignee: "Kohei"
    channel: "yoake/team-core"
```

## サブエージェント呼び出しパターン

メインエージェントは以下のパターンでこのサブエージェントを呼び出す：

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Slack search",
    prompt="""
    このスキルを読んで実行してください: .claude/skills/slack-task-manager/SKILL.md
    
    タスク: {ユーザーの指示}
    検索クエリ: {検索ワード}
    期間: {期間指定}
    
    検索結果のサマリーを返却してください。
    """
)
```

## 返却フォーマット

### Slack検索結果

```yaml
status: success
query: "DX展示会"
results:
  - channel: "infobox/dx-event-2026"
    description: "2026年DX展示会の準備チャンネル"
    relevance: 0.95
    recent_activity: "2026-01-25"
  - channel: "yoake/dx-project"
    description: "DXプロジェクト全般"
    relevance: 0.82
total_matches: 5
```

### TODO抽出結果

```yaml
status: success
period: "2026-01-06 ~ 2026-01-08"
summary:
  total: 12
  pending: 3
  in_progress: 5
  completed: 4
high_priority:
  - title: "EASソリューションの調査"
    from: "Sota Moriyama"
    channel: "yoake/team-core"
    status: pending
```

## 前提条件

- `slack-sync/` のSlack同期が完了していること
- スレッド返信が必要な場合は事前に同期

```bash
# Slack同期
cd slack-sync
python scripts/fetch_slack.py --workspace yoake

# スレッド返信も取得
python scripts/fetch_slack.py --workspace yoake --refresh-threads
```

## 依存関係

```txt
python-dotenv>=1.0.0
google-generativeai>=0.3.0  # LLMモード使用時
```

## 環境変数

```bash
# LLMモード使用時
GEMINI_API_KEY=your_api_key

# Notion連携時
NOTION_TOKEN=your_token
```

## ユースケース

1. **チャンネル検索**: プロジェクト関連のチャンネルを探す
2. **TODO確認**: 自分宛のメンションからタスクを抽出
3. **タスク統合**: 複数ソースからタスクを一覧化
4. **優先順位付け**: 期限・重要度でタスクを整理
