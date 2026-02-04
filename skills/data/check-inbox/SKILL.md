---
name: check-inbox
description: |
  メールとSlackから返信すべき項目・タスクを抽出する統合型スキル。
  Gemini 3.0 Flashで文脈判定し、優先度と返信ドラフトを生成。
  「受信箱チェック」「TODO確認」「返信すべきメッセージ」などのリクエストで使用。
---

# /check-inbox - Inbox タスク抽出

メール（Gmail）とSlackから返信が必要な項目を抽出し、優先度付きでリストアップします。

## クイックスタート

```bash
# 基本実行（過去3日間）
cd .claude/skills/check-inbox/scripts
python check_inbox.py

# 過去7日間を確認
python check_inbox.py --days 7

# メールのみ確認
python check_inbox.py --email-only

# Slackのみ確認
python check_inbox.py --slack-only
```

## 機能

- **メール分析**: `/output/gmail/` のMarkdownファイルからメールを抽出
  - マーケティング・自動通知メールを自動除外
  - 人からのメールのみをLLMで分析

- **Slack分析**: `slack-sync/data/` のメンションを抽出
  - @Kohei Nakamura, @Kohei(TokenPocket), @minicoohei, @kohei を検索
  - スレッド返信も考慮して判定

- **LLM判定** (Gemini 3.0 Flash)
  - 返信が必要かどうかを判定
  - 優先度（高/中/低）を設定
  - 返信ドラフトを生成

## オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--days, -d` | 過去何日分を確認 | 3 |
| `--email-only` | メールのみ確認 | - |
| `--slack-only` | Slackのみ確認 | - |
| `--output, -o` | 出力ファイルパス | `inbox-{date}.md` |
| `--gmail-dir` | Gmailデータディレクトリ | 自動検出 |
| `--slack-dir` | Slackデータディレクトリ | 自動検出 |
| `--workspace, -w` | Slackワークスペース | 全て |
| `--users, -u` | 検索対象ユーザー（カンマ区切り） | デフォルトリスト |
| `--no-llm` | LLM分析をスキップ | - |
| `--quiet, -q` | 進捗表示を抑制 | - |
| `--notify-line` | 結果をLINEに通知 | - |

## 出力例

```markdown
# Inbox Tasks - 2026-01-28

## 🔴 高優先度

### 📧 メール
- **[Re: プロジェクト進捗]** from: 田中太郎 (2026-01-27)
  - 理由: 期限付きの確認依頼
  - 返信案: 「ご連絡ありがとうございます。明日中に確認し、ご報告いたします。」

### 💬 Slack
- **[#pj_xxx]** @Kohei (2026-01-27 14:30)
  - 内容: APIの仕様について質問があります
  - 理由: 直接質問、要回答
  - 返信案: 「APIの仕様について確認しました。...」

## 🟡 中優先度
...

---
生成日時: 2026-01-28 10:00:00
対象期間: 過去3日間
メール件数: 15件 → 要対応: 3件
Slack件数: 42件 → 要対応: 8件
```

## 環境設定

### 必要な環境変数

`.env` ファイルに以下を設定:

```env
GEMINI_API_KEY=your_api_key_here
# または
GOOGLE_API_KEY=your_api_key_here

# LINE通知（--notify-line 使用時）
LINE_CHANNEL_ACCESS_TOKEN=your_line_access_token
LINE_USER_ID=your_line_user_id
```

### 依存パッケージ

```bash
pip install google-generativeai python-dateutil
```

## データディレクトリ

以下のパスを自動検出:

**メール**:
- `./output/gmail/`
- `~/output/gmail/`

**Slack**:
- `./slack-sync/data/`
- `~/githubactions_fordata/slack-sync/data/`

## 関連スキル

- `/email-tasks` - メール専用タスク抽出
- `/slack-tasks` - Slack専用タスク抽出
