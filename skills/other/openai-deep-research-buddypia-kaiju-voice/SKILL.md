---
name: openai-deep-research
description: OpenAI Deep Research APIを使用して深層リサーチを実行するスキル。ユーザーが特定のテーマについて深層調査、市場分析、技術リサーチ等を要求する場合に使用する。
metadata:
  short-description: Deep Research
doc_contract:
  review_interval_days: 90
---

> ⚠️ **DEPRECATED** - このスキルは `deep-research` スキルに統合されました。`deep-research --provider openai` を使用してください。

# OpenAI Deep Research

## Overview

OpenAI Deep Research APIを活用して、複雑なテーマについて深層的なリサーチを実行するスキルである。Deep Researchエージェントはウェブを探索して情報を収集・分析し、総合的なリサーチレポートを生成する。

## 事前要件

### APIキー設定

OpenAI APIキーが必要である:

1. [OpenAI Platform](https://platform.openai.com/)でAPIキーを発行
2. 環境変数設定: `export OPENAI_API_KEY="your-api-key"`

### Pythonパッケージインストール

```bash
pip install openai
```

## 使用可能なモデル

| モデル                  | 用途                           |
| ----------------------- | ------------------------------ |
| `o3-deep-research`      | 深層合成・高品質出力に最適化   |
| `o4-mini-deep-research` | 軽量化、高速な応答が必要な場合 |

## ワークフロー

### 1. リサーチ要求分析

ユーザーのリサーチ要求を分析して明確なリサーチクエリを構成する:

- リサーチテーマの明確化
- 求める情報の範囲と深さの把握
- 言語設定（デフォルト: ユーザー要求言語）

### 2. Deep Research実行

`scripts/deep_research.py` スクリプトを使用してリサーチを実行する:

```bash
# 基本的な使い方 (o3-deep-researchモデル)
python scripts/deep_research.py "リサーチテーマ"

# 高速リサーチ (o4-mini-deep-researchモデル)
python scripts/deep_research.py "リサーチテーマ" --model mini

# 韓国語結果要求
python scripts/deep_research.py "リサーチテーマ" --language korean

# 英語結果要求
python scripts/deep_research.py "リサーチテーマ" --language english

# 日本語結果要求
python scripts/deep_research.py "リサーチテーマ" --language japanese

# 結果をファイルに保存
python scripts/deep_research.py "リサーチテーマ" --output result.md

# ストリーミングモード（リアルタイム進捗確認）
python scripts/deep_research.py "リサーチテーマ" --stream
```

### 3. リサーチモニタリング

- `--stream` オプション使用時はリアルタイムで進捗確認可能
- デフォルトモードでは完了まで待機後に結果出力

### 4. 結果処理

リサーチ完了後:

- 結果はマークダウン形式で出力される
- `--output` オプション使用時はファイルに保存される
- 推論要約（reasoning summary）も併せて提供される

## 使用例

### 技術リサーチ

```bash
python scripts/deep_research.py "2025年生成型AI技術トレンドと主要企業動向分析" --language japanese
```

### 市場分析

```bash
python scripts/deep_research.py "AIゲームアプリ市場分析と競合状況。主要プレイヤー、市場規模、成長率を含む" --language japanese
```

### 学術調査

```bash
python scripts/deep_research.py "Large Language Modelの最新研究動向と主要論文レビュー" --language english --model mini
```

### 比較分析

```bash
python scripts/deep_research.py "Next.js vs Remix: 2025年基準の性能、エコシステム、採用市場の比較" --output nextjs_vs_remix.md
```

## プロンプト作成のコツ

APIを通じたDeep ResearchはChatGPTと異なり明確化質問を行わないため、プロンプトに以下を含めると良い:

1. **具体的な範囲**: 「直近2年間」、「日本市場中心」
2. **求める比較点**: 「価格、性能、使いやすさの比較」
3. **求める指標**: 「市場規模、成長率、MAUを含む」
4. **好ましい出典**: 「学術論文中心」、「産業レポート参照」
5. **出力形式**: 「表形式で整理」、「長所短所リストで」

## 制限事項

- **APIアクセス**: OpenAI APIキーが必要
- **コスト**: Deep Researchモデルは一般モデルよりコストが高い
- **用途**: 単純な質問や短い対話には不適切（一般モデル使用推奨）

## エラー処理

| エラー                   | 原因                     | 解決策                               |
| ------------------------ | ------------------------ | ------------------------------------ |
| `OPENAI_API_KEY not set` | 環境変数未設定           | `export OPENAI_API_KEY="..."` を実行 |
| `AuthenticationError`    | 不正なAPIキー            | APIキーを確認し再設定                |
| `RateLimitError`         | APIリクエスト上限超過    | しばらく待ってから再試行             |
| `ModuleNotFoundError`    | パッケージ未インストール | `pip install openai` を実行          |

## Resources

### scripts/

- `deep_research.py` - Deep Research APIを呼び出すメインスクリプト

### references/

- `api_reference.md` - OpenAI Deep Research API参照ドキュメント
