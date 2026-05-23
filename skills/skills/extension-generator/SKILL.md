---
name: extension-generator
description: Claude Codeの拡張機能（スキル、サブエージェント、プロジェクト設定）をユーザーの自然言語指示から自動生成するスキル。「○○を作るスキルを作って」「○○エージェントを作って」「CLAUDE.mdを設定して」などのリクエスト時に使用。v2.1.1以降、スラッシュコマンドとスキルは統合されたため、すべてスキルとして作成。
---

# Extension Generator

ユーザーの自然言語指示からClaude Codeの拡張機能を**提案・生成**するスキル。

## ワークフロー

### Step 1: 要件ヒアリング

ユーザーの指示から以下を確認（不明な場合は質問）:

1. **目的**: 何を解決したいか？
2. **トリガー**: いつ使いたいか？（明示的 or 自動検出）
3. **複雑さ**: 単純なプロンプト？複数ステップ？外部ツール連携？
4. **独立性**: メイン会話で実行？独立コンテキストが必要？
5. **再利用性**: 個人用？チーム共有？

### Step 2: 構成を提案

要件に基づいて**何を作るべきか提案**する:

```
【提案テンプレート】

ご要件を整理すると:
- 目的: ○○
- トリガー: ○○
- 複雑さ: ○○

以下の構成を提案します:

📁 .claude/skills/skill-name/
├── SKILL.md          ← [必須] メイン定義
├── references/       ← [任意] 参照ドキュメント
│   └── xxx.md
└── scripts/          ← [任意] 自動化スクリプト
    └── xxx.py

または

📁 .claude/agents/
└── agent-name.md     ← サブエージェント

理由: ○○

この構成でよろしいですか？
```

### Step 3: 生成実行

承認後、各ファイルを生成。

---

## 構成要素ガイド

### スキル構造 (.claude/skills/)

```
skill-name/
├── SKILL.md          # 必須
├── references/       # 任意: 参照ドキュメント
├── scripts/          # 任意: 自動化スクリプト
└── assets/           # 任意: テンプレート等
```

#### SKILL.md（必須）

スキルの**メイン定義ファイル**。

- フロントマター（name, description, allowed-tools等）
- ワークフロー/手順
- 使用例

**いつ作る**: 常に必須

#### references/（任意）

**補足情報・チェックリスト・詳細ガイド**を格納。

| 作るべき時 | 例 |
|------------|-----|
| チェックリストが必要 | `SECURITY.md`, `PERFORMANCE.md` |
| ドメイン知識が必要 | `API_SPEC.md`, `CODING_STYLE.md` |
| 複数パターンがある | `PATTERNS.md`, `EXAMPLES.md` |
| SKILL.mdが長くなりすぎる | 分割して参照 |

**参照方法**: `See [references/xxx.md](references/xxx.md)`

#### scripts/（任意）

**自動化スクリプト**を格納。

| 作るべき時 | 例 |
|------------|-----|
| 外部ツール実行が必要 | `run-linters.sh` |
| データ処理が必要 | `analyze.py` |
| ファイル生成が必要 | `generate.py` |
| 検証/バリデーションが必要 | `validate.sh` |

**実行方法**: `!./scripts/xxx.sh` または `allowed-tools: Bash(./scripts/*)`

---

### サブエージェント (.claude/agents/)

**独立コンテキスト**で動作する特化型AI。

```
agent-name.md         # 単一ファイル
```

| 作るべき時 | 理由 |
|------------|------|
| 独立したコンテキストが必要 | メイン会話を汚さない |
| 異なるモデルを使いたい | `model: haiku` で高速化 |
| 複雑なマルチステップタスク | 専門家として動作 |
| ツールセットを制限したい | `tools:` で明示指定 |

---

## 複雑さ別の推奨構成

### シンプル（単一プロンプト）

```
skill-name/
└── SKILL.md
```

例: コミットメッセージ生成、簡単な説明

### 中程度（チェックリスト・ガイド付き）

```
skill-name/
├── SKILL.md
└── references/
    ├── CHECKLIST.md
    └── EXAMPLES.md
```

例: コードレビュー、ドキュメント生成

### 複雑（外部ツール連携）

```
skill-name/
├── SKILL.md
├── references/
│   ├── SECURITY.md
│   └── PERFORMANCE.md
└── scripts/
    ├── run-linters.sh
    └── analyze.py
```

例: 包括的コードレビュー、CI/CD連携

### 独立実行が必要

```
.claude/agents/
└── specialist.md
```

例: デバッガー、データサイエンティスト、探索エージェント

---

## スキル vs サブエージェント 選択基準

| 要件 | → | 選択 |
|------|---|------|
| 知識・ガイドを追加したい | → | スキル |
| ワークフローを標準化したい | → | スキル |
| メイン会話で実行したい | → | スキル |
| 独立コンテキストが必要 | → | サブエージェント |
| 異なるモデルを使いたい | → | サブエージェント |
| 複雑な探索・調査タスク | → | サブエージェント |

---

## 参照ドキュメント

詳細なパターンとテンプレート:

- **スキル**: [references/skill-patterns.md](references/skill-patterns.md)
- **サブエージェント**: [references/subagent-patterns.md](references/subagent-patterns.md)
- **プロジェクト設定**: [references/project-config-patterns.md](references/project-config-patterns.md)
- **テンプレート集**: [references/templates.md](references/templates.md)

---

## 生成スクリプト

スケルトン生成用:

```bash
# スキル作成
python scripts/generate_extension.py skill <name> [--simple]

# サブエージェント作成
python scripts/generate_extension.py agent <name> [--scope user|project]

# プロジェクト設定作成
python scripts/generate_extension.py project
```

See [scripts/generate_extension.py](scripts/generate_extension.py)
