---
name: deep-research
description: OpenAIまたはGoogle Gemini Deep Research APIを使用して深層リサーチを実行する統合スキル。Subcommandアーキテクチャ（start/status/poll/result/list）で長時間リサーチを安定的に管理する。
metadata:
  short-description: Deep Research
doc_contract:
  review_interval_days: 90
---

# Deep Research v2.0

## Overview

OpenAIまたはGoogle Gemini Deep Research APIを活用して、複雑なテーマについて深層的なリサーチを実行する統合スキルである。

### v2.0 核心変更（Subcommand Architecture）

v1.0は単一プロセスブロッキング方式であったが、v2.0で**Subcommandアーキテクチャ**に全面再設計された:

| 問題（v1.0）                          | 解決（v2.0）                        |
| ------------------------------------- | ----------------------------------- |
| Bash 10分タイムアウト vs リサーチ60分 | `start`（即時返却）+ `poll`（分離） |
| クラッシュ時の結果消失                | Stateファイル基盤の永続管理         |
| 単一プロセスall-or-nothing            | 6つのサブコマンドに分離             |

## 事前要件

### APIキー設定

使用するプロバイダに応じてAPIキーを設定する必要がある:

#### OpenAI

1. [OpenAI Platform](https://platform.openai.com/)でAPIキーを発行
2. 環境変数設定: `export OPENAI_API_KEY="your-api-key"`

#### Google

1. [Google AI Studio](https://aistudio.google.com/)でAPIキーを発行
2. 環境変数設定: `export GEMINI_API_KEY="your-api-key"`

### Pythonパッケージインストール

```bash
# OpenAI用
pip install openai

# Google用
pip install google-genai

# または両方
pip install openai google-genai
```

## プロバイダ比較

| 特徴               | OpenAI                                  | Google                            |
| ------------------ | --------------------------------------- | --------------------------------- |
| **モデル**         | o3-deep-research, o4-mini-deep-research | deep-research-pro-preview-12-2025 |
| **実行方式**       | `background=True`（非同期）             | `background=True`（非同期）       |
| **ポーリング間隔** | 15秒                                    | 30秒                              |
| **Zombie Guard**   | 120回（30分）                           | 60回（30分）                      |
| **モデル選択**     | o3/mini                                 | 単一                              |
| **コスト**         | 相対的に高い                            | 相対的に低い                      |
| **用途**           | 高速応答、高品質合成                    | 長時間リサーチ、包括的分析        |

## サブコマンド

### アーキテクチャ概要

```
start ──→ [Stateファイル生成] ──→ poll ──→ [完了検知] ──→ result
  │                                │
  │ (即時返却、session_id出力)      │ (反復ポーリング、バックグラウンド可能)
  │                                │
  └── status (1回照会) ────────────┘

list: 全セッション一覧照会
run:  start + poll (レガシー互換)
```

### 1. `start` - リサーチ開始（即時返却）

```bash
# OpenAIでリサーチ開始
python scripts/deep_research.py start "リサーチテーマ" --provider openai

# Googleでリサーチ開始
python scripts/deep_research.py start "リサーチテーマ" --provider google

# 自動Provider選択
python scripts/deep_research.py start "リサーチテーマ" --auto

# OpenAI + 高速モデル
python scripts/deep_research.py start "リサーチテーマ" --provider openai --model mini

# 日本語結果要求
python scripts/deep_research.py start "リサーチテーマ" --language japanese

# カスタム出力パス
python scripts/deep_research.py start "リサーチテーマ" --output docs/research/custom.md
```

**出力**: `session_id`を返却する。以後 `status`、`poll`、`result` コマンドで使用。

### 2. `status` - 状態確認（1回）

```bash
python scripts/deep_research.py status <session_id>
```

**出力**: `queued`、`in_progress`、`completed`、`failed`、`cancelled` のいずれか。

### 3. `poll` - 完了までポーリング

```bash
# 完了まで待機（バックグラウンド実行推奨）
python scripts/deep_research.py poll <session_id>
```

- OpenAI: 15秒間隔、最大120回（30分）
- Google: 30秒間隔、最大60回（30分）
- **Zombie Guard**: 最大反復回数到達時に自動中断（無限ループ防止）

### 4. `result` - 完了した結果照会

```bash
python scripts/deep_research.py result <session_id>
```

完了したリサーチ結果を出力しファイルに保存する。

### 5. `list` - セッション一覧

```bash
python scripts/deep_research.py list
```

全リサーチセッションの状態を表で表示する。

### 6. `run` - レガシー互換（start + poll）

```bash
# v1.0互換: start後に自動poll
python scripts/deep_research.py run "リサーチテーマ" --provider openai

# レガシー構文もサポート（サブコマンドなし）
python scripts/deep_research.py "リサーチテーマ" --provider openai
```

## ワークフロー

### 基本ワークフロー（推奨）

```bash
# 1. リサーチ開始（即時返却）
python scripts/deep_research.py start "プログラミング学習アプリ市場分析" --auto
# → session_id: mkt-analysis-openai-20260208

# 2. (任意) 状態確認
python scripts/deep_research.py status mkt-analysis-openai-20260208

# 3. 完了までポーリング（バックグラウンド実行可能）
python scripts/deep_research.py poll mkt-analysis-openai-20260208

# 4. 結果確認
python scripts/deep_research.py result mkt-analysis-openai-20260208
```

### Claude Codeでの実行パターン

```bash
# start (Bashツール、即時返却)
python scripts/deep_research.py start "テーマ" --auto

# poll (Bashツール、run_in_background=true)
python scripts/deep_research.py poll <session_id>

# 完了確認後に結果照会
python scripts/deep_research.py result <session_id>
```

### クラッシュ復旧

プロセスが中断されてもStateファイルが残っているため:

```bash
# セッション一覧でin_progressを確認
python scripts/deep_research.py list

# 再度ポーリング開始
python scripts/deep_research.py poll <session_id>
```

## 出力ファイル

### デフォルト保存パス

`--output`を指定しなければ `docs/research/` ディレクトリに自動保存される。

### ファイル名形式

```
{slug}-{provider}-{date}.md
```

例:

- `mkt-analysis-openai-20260208.md`
- `ai-trend-2026-google-20260208.md`
- `nextjs-vs-remix-openai-20260208.md`

### Slug生成規則

- クエリから主要キーワードを抽出し最大5単語で組み合わせ
- 日本語はローマ字変換せず主要英語キーワードを抽出
- 特殊文字を除去、ハイフンで接続

## Stateファイル管理

Stateファイルは `.claude/skills/deep-research/state/` ディレクトリにJSON形式で保存される。

### Stateファイル構造

```json
{
  "session_id": "mkt-analysis-openai-20260208",
  "provider": "openai",
  "query": "プログラミング学習アプリ市場分析",
  "status": "in_progress",
  "api_id": "resp_xxx",
  "output_path": "docs/research/mkt-analysis-openai-20260208.md",
  "created_at": "2026-02-08T15:30:00",
  "updated_at": "2026-02-08T15:35:00"
}
```

### 自動クリーンアップ

`config.yaml`の `state.cleanup_after_hours` 設定に従い、完了/失敗状態のStateファイルは72時間後に自動削除される。

## Smart Provider Selection

クエリ内容を自動分析して最適なProviderを選択するインテリジェントルーティング機能である。

### 使い方

```bash
# 自動選択モード（キーワード分析 + 学習ベース）
python scripts/deep_research.py start "プログラミング学習アプリの最新トレンド" --auto

# 戦略指定 - 品質優先（OpenAI優先）
python scripts/deep_research.py start "深層分析が必要なテーマ" --strategy quality

# 戦略指定 - コスト優先（Google優先）
python scripts/deep_research.py start "幅広い市場調査" --strategy cost
```

### キーワードルール

**OpenAIが選択されるキーワード**:

- 深層、deep、分析、analysis、学術、academic、研究、research、レポート、report、論文、paper、構造化、structured

**Googleが選択されるキーワード**:

- 最新、latest、トレンド、trend、ニュース、news、市場、market、競合、competitor、高速、quick、スキャン、scan、現況、current

### 戦略モード

| モード    | 動作                                    | 使用ケース               |
| --------- | --------------------------------------- | ------------------------ |
| `auto`    | キーワードスコア + 学習パターン基盤選択 | 一般的な場合（推奨）     |
| `quality` | OpenAI優先（高品質レポート）            | 重要な意思決定用リサーチ |
| `cost`    | Google優先（コスト削減）                | 予算が限られている場合   |
| `manual`  | ユーザー指定Providerのみ使用            | 特定Provider強制使用     |

### 学習データ

使用履歴は `logs/usage_patterns.json` に保存され、直近100件の履歴のみ保持される。
最低10件以上のデータが蓄積されると学習が開始される。

## プロンプト作成のコツ

APIを通じたDeep ResearchはChatGPTと異なり明確化質問を行わないため、プロンプトに以下を含めると良い:

1. **具体的な範囲**: 「直近2年間」、「日本市場中心」
2. **求める比較点**: 「価格、性能、使いやすさの比較」
3. **求める指標**: 「市場規模、成長率、MAUを含む」
4. **好ましい出典**: 「学術論文中心」、「産業レポート参照」
5. **出力形式**: 「表形式で整理」、「長所短所リストで」

## 制限事項

### 共通

- **APIアクセス**: 各プロバイダのAPIキーが必要
- **コスト**: Deep Researchモデルは一般モデルよりコストが高い
- **用途**: 単純な質問や短い対話には不適切（一般モデル使用推奨）
- **Zombie Guard**: 最大ポーリング回数超過時に自動中断

### OpenAI専用

- **モデルサポート**: o3-deep-research、o4-mini-deep-researchのみサポート

### Google専用

- **実行時間**: 最大60分（大部分は20分以内に完了）
- **オーディオ入力**: サポートされない
- **ストリーミング**: サポートされない（ポーリングベース）

## エラー処理

| エラー                   | 原因                   | 解決策                               |
| ------------------------ | ---------------------- | ------------------------------------ |
| `OPENAI_API_KEY not set` | OpenAI APIキー未設定   | `export OPENAI_API_KEY="..."` を実行 |
| `GEMINI_API_KEY not set` | Google APIキー未設定   | `export GEMINI_API_KEY="..."` を実行 |
| `AuthenticationError`    | 不正なAPIキー          | APIキーを確認し再設定                |
| `RateLimitError`         | APIリクエスト上限超過  | しばらく待ってから再試行             |
| `Zombie guard triggered` | 最大ポーリング回数超過 | `list`で状態確認後 `poll` を再開     |
| `State file not found`   | 存在しないセッションID | `list`で有効なセッションを確認       |

## 設定 (config.yaml)

```yaml
# ポーリング設定
polling:
  openai:
    interval: 15 # 秒
    max_iterations: 120 # 15s x 120 = 30分
  google:
    interval: 30
    max_iterations: 60 # 30s x 60 = 30分

# 出力設定
output:
  default_dir: 'docs/research'
  filename_format: '{slug}-{provider}-{date}'

# State設定
state:
  dir: 'state'
  cleanup_after_hours: 72
```

## Resources

### scripts/

- `deep_research.py` - Deep Research CLI v2.0 (Subcommand Architecture)

### references/

- `openai_api_reference.md` - OpenAI Deep Research API参照ドキュメント
- `google_api_reference.md` - Google Deep Research API参照ドキュメント

### state/

- リサーチセッションStateファイル保存ディレクトリ

### logs/

- `usage_patterns.json` - Smart Provider Selection 学習データ
