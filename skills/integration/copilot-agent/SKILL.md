---
name: copilot-agent
description: |
  GitHub Copilot CLIをサブエージェントとして活用し、コードベースの解析・調査を行う。
  以下の場面で使用:
  (1) /copilot コマンドで明示的に呼び出された場合
  (2) コードベースの広範な調査が必要で、別視点からの分析が有用な場合
  (3) 特定の実装パターンや設計についてセカンドオピニオンが欲しい場合
---

# Copilot Agent

GitHub Copilot CLIを非対話モードで実行し、コードベースの解析結果を取得する。

## 基本コマンド

```bash
copilot -p "<プロンプト>" --allow-all-tools -s
```

### オプション説明
- `-p "<プロンプト>"`: 非対話モードでプロンプトを実行（完了後に終了）
- `--allow-all-tools`: 全ツールの自動実行を許可（確認なし）
- `-s, --silent`: エージェントの応答のみを出力（統計情報なし）

## 使用パターン

### コードベース調査
```bash
copilot -p "このプロジェクトの全体構造を調査し、主要なコンポーネントとその役割を説明してください" --allow-all-tools -s
```

### 特定機能の分析
```bash
copilot -p "認証機能の実装を調査し、セキュリティ上の懸念点があれば報告してください" --allow-all-tools -s
```

### 実装提案
```bash
copilot -p "新機能Xを実装する場合、既存のコードベースに基づいて最適なアプローチを提案してください" --allow-all-tools -s
```

## モデル選択

特定のモデルを使用する場合は `--model` オプションを追加:

```bash
copilot -p "<プロンプト>" --allow-all-tools -s --model claude-sonnet-4
```

利用可能なモデル:
- `claude-sonnet-4.5`, `claude-haiku-4.5`, `claude-opus-4.5`,
- `gpt-5.2`, `gpt-5-mini`, `gpt-5.1-codex-mini`, `gpt-5.1-codex-max`
- `gemini-3-pro-preview`

## 注意事項

- 長時間の調査は避け、具体的で焦点を絞ったプロンプトを使用する
- 出力が大きい場合はタイムアウトする可能性がある
- `--allow-all-paths` を追加すると全パスへのアクセスが可能になる
