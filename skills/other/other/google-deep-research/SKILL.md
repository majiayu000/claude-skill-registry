---
name: google-deep-research
description: Google Gemini Deep Research APIを使用して包括的なディープリサーチを実行するスキル。ユーザーが特定のテーマについて深層的な調査、市場分析、技術リサーチ、文献調査等を要求する場合に使用する。
metadata:
  short-description: Deep Research
doc_contract:
  review_interval_days: 90
---

> ⚠️ **DEPRECATED** - このスキルは `deep-research` スキルに統合されました。`deep-research --provider google` を使用してください。

# Google Deep Research

## Overview

Google Gemini Deep Research APIを活用して、複雑なテーマについて包括的なリサーチを実行するスキルである。Deep Researchエージェントは最大60分間ウェブを探索して情報を収集・分析し、総合的なリサーチレポートを生成する。

## 事前要件

### APIキー設定

Google AI StudioでGemini APIキーが必要である:

1. [Google AI Studio](https://aistudio.google.com/)でAPIキーを発行
2. 環境変数設定: `export GEMINI_API_KEY="your-api-key"`

### Pythonパッケージインストール

```bash
pip install google-genai
```

## ワークフロー

### 1. リサーチ要求分析

ユーザーのリサーチ要求を分析して明確なリサーチクエリを構成する:

- リサーチテーマの明確化
- 求める情報の範囲と深さの把握
- 言語設定（デフォルト: ユーザー要求言語）

### 2. Deep Research実行

`scripts/deep_research.py` スクリプトを使用してリサーチを実行する:

```bash
# 基本的な使い方
python scripts/deep_research.py "リサーチテーマ"

# 韓国語結果要求
python scripts/deep_research.py "リサーチテーマ" --language korean

# 英語結果要求
python scripts/deep_research.py "リサーチテーマ" --language english

# 日本語結果要求
python scripts/deep_research.py "リサーチテーマ" --language japanese

# 結果をファイルに保存
python scripts/deep_research.py "リサーチテーマ" --output result.md
```

### 3. リサーチ状態モニタリング

Deep Researchはバックグラウンドで実行され、大部分の作業は20分以内に完了する（最大60分）。

スクリプトは10秒ごとに進捗状態をポーリングし、以下を表示する:

- 進捗率と予想残り時間
- 現在検索中のトピック
- 完了時は全体レポート

### 4. 結果処理

リサーチ完了後:

- 結果はマークダウン形式で出力される
- `--output` オプション使用時はファイルに保存される
- エラー発生時は詳細メッセージを表示

## 使用例

### 技術リサーチ

```bash
python scripts/deep_research.py "2025年生成型AI技術トレンドと主要企業動向" --language japanese
```

### 市場分析

```bash
python scripts/deep_research.py "AIゲームアプリ市場分析と競合状況" --language japanese
```

### 学術調査

```bash
python scripts/deep_research.py "Large Language Modelの最新研究動向と主要論文" --language english
```

## 制限事項

- **実行時間**: 最大60分（大部分は20分以内に完了）
- **オーディオ入力**: サポートされない
- **APIアクセス**: Allowlist登録が必要（一部機能）
- **ツール**: google_searchとurl_contextツールがデフォルトで提供

## エラー処理

| エラー                   | 原因                        | 解決策                               |
| ------------------------ | --------------------------- | ------------------------------------ |
| `GEMINI_API_KEY not set` | 環境変数未設定              | `export GEMINI_API_KEY="..."` を実行 |
| `Research failed`        | APIエラーまたはタイムアウト | クエリを簡略化するか再試行           |
| `ModuleNotFoundError`    | パッケージ未インストール    | `pip install google-genai` を実行    |

## Resources

### scripts/

- `deep_research.py` - Deep Research APIを呼び出すメインスクリプト

### references/

- `api_reference.md` - Google Deep Research API参照ドキュメント
