---
name: gemini
description: Gemini CLI を使用してテキストと画像を生成する際にこのスキルを使用します。ユーザーが Gemini を通じてコンテンツ生成、画像生成、コードレビュー等を要求した際にトリガーされます。
metadata:
  short-description: Generate image/text with Gemini
doc_contract:
  review_interval_days: 90
---

# Gemini CLI

GoogleのGemini AIモデルをターミナルから直接使用できるCLIツールです。テキスト生成、画像生成、コード分析等、様々なAI作業を実行できます。

## 前提要件

Gemini CLIがインストールされている必要があります。インストールされていない場合:

```bash
# npm グローバルインストール (推奨)
npm install -g @google/gemini-cli

# または Homebrew (macOS/Linux)
brew install gemini-cli

# または npx で即時実行
npx https://github.com/google-gemini/gemini-cli
```

## テキスト生成

### 対話モード

```bash
# 基本実行
gemini

# 特定モデル使用
gemini -m gemini-3-flash-preview
```

### 非対話モード (スクリプト用)

```bash
# 単一プロンプト実行
gemini -p "AIゲーム対戦プロジェクトの紹介文を作成して"

# ファイル内容を含めて分析
gemini -p "このコードをレビューして" < code.ts

# 結果をファイルに保存
gemini -p "README 草案を作成して" > README.md
```

### コンテキスト含有

```bash
# 特定ディレクトリを含む
gemini --include-directories ./lib,./docs

# プロジェクト全体コンテキスト
gemini --include-directories .
```

## 画像生成

Gemini CLIでの画像生成はImagen MCPサーバーを通じて可能です。

### MCPサーバー設定

`~/.gemini/settings.json` ファイルに以下を追加:

```json
{
  "mcpServers": {
    "imagen": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-imagen"]
    }
  }
}
```

### 画像生成コマンド

```bash
# 対話モードで画像生成
gemini
> かわいい猫キャラクターアイコンを生成して

# 非対話モード
gemini -p "ミニマルスタイルのAIゲーム対戦アプリロゴを生成して"
```

### Gemini 2.5 Flash Image モデル (ネイティブ画像生成)

```bash
# 画像生成専用モデル使用
gemini -m gemini-3-flash-preview-image -p "韓国の伝統文様が入ったバナー画像"
```

## 実行例

### マーケティング文生成

```bash
gemini -p "AIゲーム対戦プロジェクト 'プロジェクト' の紹介文を作成して。
Gemini API活用、リアルタイム対戦、インタラクティブなゲーム体験を強調して。"
```

### コードレビュー

```bash
gemini -p "このReactコンポーネントのパフォーマンス改善点を見つけて" < src/features/battle/components/BattleArena.tsx
```

### ドキュメント草案作成

```bash
gemini -p "次の機能に関する技術ドキュメントを作成して: ユーザー学習進捗同期" \
  --include-directories ./docs/DATABASE_SCHEMA > docs/SYNC_FEATURE.md
```

## 便利なオプション

| オプション              | 説明                                                             |
| ----------------------- | ---------------------------------------------------------------- |
| `-m, --model`           | 使用するモデルを指定 (gemini-2.5-pro, gemini-3-flash-preview 等) |
| `-p, --prompt`          | 非対話モードで単一プロンプト実行                                 |
| `--include-directories` | コンテキストに含むディレクトリ                                   |
| `--sandbox`             | サンドボックスモードで実行 (ファイル変更不可)                    |
| `-y, --yes`             | 全ての確認プロンプトを自動承認                                   |

## 認証

- **Google ログイン** (推奨): 無料で毎分60回、1日1,000回リクエスト
- **API キー**: [AI Studio](https://aistudio.google.com)で発行後 `GEMINI_API_KEY` 環境変数に設定
- **Vertex AI**: エンタープライズ環境用

```bash
# API キー設定
export GEMINI_API_KEY="your-api-key"
```

## 参考資料

- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Gemini API 画像生成ドキュメント](https://ai.google.dev/gemini-api/docs/image-generation)
- [Google AI Studio](https://aistudio.google.com)
