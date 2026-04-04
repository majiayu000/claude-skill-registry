---
name: codex-skill-generator
description: Codex CLI用のスキル作成ガイド。YAML frontmatter、ディレクトリ構造、ベストプラクティスを解説。Use when creating new Codex skills, updating existing skills, or learning about Codex skill development.
---

# Codex Skill Generator

Codex CLI用の効果的なスキルを作成するためのガイドです。

## When to Use This Skill

- 新しいCodexスキルを作成する時
- 既存のスキルを更新する時
- スキルの構造やベストプラクティスを学びたい時
- スキルが正しく動作しない時のトラブルシューティング

---

## スキルとは？

スキルはCodex CLIの機能を拡張するための組織化されたフォルダです。指示、リファレンス、スクリプトを含むことができます。

**特徴:**
- モデル呼び出し型（ユーザーのリクエストに基づいて自動的に起動）
- プロジェクト固有またはグローバルに配置可能
- 再利用可能なワークフロー・知識を定義

---

## ディレクトリ構造

### 配置場所

```
# グローバルスキル（全プロジェクトで使用可能）
~/.codex/skills/skill-name/SKILL.md

# プロジェクトスキル（リポジトリ内で使用）
.codex/skills/skill-name/SKILL.md
```

### 基本構造

```
skill-name/
├── SKILL.md              # メインスキルファイル（必須）
├── scripts/              # ユーティリティスクリプト（オプション）
│   ├── setup.sh
│   └── analyze.py
├── templates/            # テンプレートファイル（オプション）
│   └── template.md
└── reference.md          # 追加リファレンス（オプション）
```

---

## スキルの作成手順

### Step 1: ディレクトリ作成

```bash
# プロジェクトスキル
mkdir -p .codex/skills/my-skill-name

# グローバルスキル
mkdir -p ~/.codex/skills/my-skill-name
```

### Step 2: SKILL.md の作成

```yaml
---
name: skill-identifier
description: スキルの説明と使用タイミング。Use when [トリガーシナリオ].
---

# スキル名

スキルの概要説明

## When to Use This Skill

- 使用シナリオ1
- 使用シナリオ2

## Instructions

1. ステップ1
2. ステップ2

## Examples

### 例1
[具体例]
```

### Step 3: 有効化確認

```toml
# ~/.codex/config.toml
[features]
skills = true
```

---

## YAML Frontmatter 仕様

### 必須フィールド

| フィールド | 説明 | 制約 |
|-----------|------|------|
| `name` | スキル識別子 | 小文字、数字、ハイフンのみ。最大64文字 |
| `description` | スキルの説明 | 最大1024文字。トリガーキーワードを含める |

### name の命名規則

```yaml
# ✅ 良い例
name: error-analyzer
name: api-docs-writer
name: db-migration-helper

# ❌ 悪い例
name: Error_Analyzer      # 大文字・アンダースコアNG
name: my skill            # スペースNG
name: スキル名             # 日本語NG
```

### description のベストプラクティス

```yaml
# ✅ 良い例: 具体的でトリガーキーワードが豊富
description: エラー/スタックトレース/ログを解析し、原因の切り分けと最小修正案、確認手順を提示する。Use when debugging errors, analyzing stack traces, or troubleshooting issues.

# ✅ 良い例: 何をするか＋いつ使うかが明確
description: CSV/TSV/JSONを要約して洞察を返すスキル。Use when analyzing data, summarizing CSV files, or working with tabular data.

# ❌ 悪い例: 抽象的すぎる
description: データ処理を手伝う

# ❌ 悪い例: いつ使うかが不明
description: このスキルはデータベースマイグレーションとスキーマ変更を処理します
```

---

## 推奨スキル構成

```markdown
---
name: my-skill-name
description: [機能説明]。Use when [使用シナリオ].
---

# スキル名

簡潔な概要説明

## When to Use This Skill

- シナリオ1
- シナリオ2
- シナリオ3

## 手順 / Instructions

### Step 1: [ステップ名]
[説明]

### Step 2: [ステップ名]
[説明]

## Examples

### 例1: [シナリオ]
```[言語]
[コード例]
```

## Context / 補足情報

- 前提条件
- 制約事項

## AI Assistant Instructions

このスキルが起動されたら:

1. まず〇〇を確認
2. 次に〇〇を実行
3. 最後に〇〇を提示

Always:
- 〇〇する
- 〇〇する

Never:
- 〇〇しない
- 〇〇しない
```

---

## スクリプトの活用

### シェルスクリプト（単純な操作向け）

```bash
# scripts/setup.sh
#!/bin/bash
echo "Setting up environment..."
npm install
```

### Pythonスクリプト（複雑なロジック向け）

```python
# scripts/analyze.py
#!/usr/bin/env python3
import json
import sys

def main():
    # 分析ロジック
    result = {"status": "ok"}
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

### SKILL.mdからの参照

```markdown
## 使用方法

セットアップを実行:
```bash
bash scripts/setup.sh
```

分析を実行:
```bash
python3 scripts/analyze.py <path>
```
```

---

## スキルパターン

### パターン1: 分析スキル

```yaml
---
name: code-analyzer
description: コードを分析し、問題点と改善案を提示する。Use when reviewing code, finding bugs, or improving code quality.
---

# Code Analyzer

## Instructions

1. 対象ファイル/ディレクトリを確認
2. 分析観点を明確化
3. 問題点を優先度順にリスト化
4. 具体的な修正案を提示
```

### パターン2: 生成スキル

```yaml
---
name: doc-generator
description: コードからドキュメントを自動生成する。Use when creating API docs, README files, or code comments.
---

# Document Generator

## Instructions

1. 対象コードを読み込む
2. 構造を分析
3. テンプレートに沿ってドキュメント生成
4. 出力形式を確認
```

### パターン3: ワークフロースキル

```yaml
---
name: deploy-helper
description: デプロイ手順をガイドする。Use when deploying to production, staging, or running release processes.
---

# Deploy Helper

## Instructions

1. 現在のブランチ・状態を確認
2. チェックリストを提示
3. 各ステップを順番に実行
4. 結果を確認
```

---

## トラブルシューティング

### スキルが起動しない

**原因1: features.skills が無効**
```toml
# ~/.codex/config.toml
[features]
skills = true  # ← 確認
```

**原因2: ファイル名が間違っている**
```
✅ SKILL.md（大文字）
❌ skill.md
❌ Skill.md
```

**原因3: YAML frontmatter の構文エラー**
```yaml
# ✅ 正しい形式
---
name: my-skill
description: 説明文
---

# ❌ デリミタがない
name: my-skill
description: 説明文

# ❌ タブを使用（スペースを使う）
---
name:	my-skill  # タブNG
---
```

**原因4: description にトリガーキーワードがない**
- ユーザーが使う言葉をdescriptionに含める
- 「Use when」で使用シナリオを明示

### スキルが意図しないタイミングで起動する

**対策:**
- descriptionをより具体的にする
- 他のスキルとキーワードが重複していないか確認

---

## ベストプラクティス

### 1. 1スキル = 1機能

```
✅ error-analyzer: エラー解析専用
✅ doc-generator: ドキュメント生成専用

❌ dev-helper: 何でもやる（曖昧）
```

### 2. 具体例を含める

```markdown
## Examples

### 例: TypeScriptの型エラー

入力:
```
error TS2339: Property 'foo' does not exist on type 'Bar'
```

出力:
```
## 原因
`Bar` 型に `foo` プロパティが定義されていません

## 修正案
1. interface Bar に foo を追加
2. または foo へのアクセスを削除
```
```

### 3. コンテキストを節約

- 基本的な説明は省略（Codexは既に知っている）
- 500行以下を目安に
- 詳細情報は別ファイルに分離

### 4. 明確な指示を書く

```markdown
## AI Assistant Instructions

1. **最初に**: 入力を確認し、不足があれば質問
2. **次に**: 分析を実行
3. **最後に**: 結果を構造化して出力

Always:
- ファイルパスと行番号を明示
- 実行可能なコードを提供

Never:
- 推測だけで回答しない
- 機密情報をログに出力しない
```

---

## クイックリファレンス: チェックリスト

新しいスキルを作成したら確認:

- [ ] ディレクトリ: `.codex/skills/skill-name/` または `~/.codex/skills/skill-name/`
- [ ] ファイル名: `SKILL.md`（大文字）
- [ ] YAML frontmatter: `---` で囲まれている
- [ ] `name`: 小文字・ハイフンのみ、64文字以内
- [ ] `description`: 機能＋使用シナリオ、トリガーキーワード含む
- [ ] 「When to Use」セクションがある
- [ ] 具体的な手順・例がある
- [ ] AI Assistant Instructions がある
- [ ] `features.skills = true` が有効

---

## テンプレート

### 最小構成

```markdown
---
name: my-skill
description: [何をするか]。Use when [いつ使うか].
---

# スキル名

## When to Use This Skill
- シナリオ1

## Instructions
1. ステップ1
2. ステップ2

## AI Assistant Instructions
このスキルが起動されたら:
1. [指示]
```

### フル構成

```markdown
---
name: my-skill
description: [詳細な説明]。Use when [シナリオ1], [シナリオ2], or [キーワード].
---

# スキル名

概要説明

## When to Use This Skill
- シナリオ1
- シナリオ2
- シナリオ3

## 前提条件
- 必要な環境
- 依存関係

## Instructions

### Step 1: [ステップ名]
[説明]

### Step 2: [ステップ名]
[説明]

## Examples

### 例1: [シナリオ]
```[言語]
[コード]
```

## Output Format
```
[出力フォーマット]
```

## Context
- 補足情報
- 制約事項

## AI Assistant Instructions

このスキルが起動されたら:
1. [指示1]
2. [指示2]
3. [指示3]

Always:
- [必須事項]

Never:
- [禁止事項]

## 関連リソース
- [リンク]
```
