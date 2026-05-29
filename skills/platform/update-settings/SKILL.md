---
name: update-settings
description: プロジェクトの .claude/settings.json を更新する。「設定を更新して」「settings を変更」「permissions を追加」「設定を変えて」「Claude の設定」「設定ファイルを編集」「allowedTools を追加」などで起動。Claude Code のプロジェクト設定を管理。
allowed-tools: [Read, Write, Bash, Glob]
---

# Update Settings

プロジェクトの `.claude/settings.json` を更新します。

## ワークフロー

### 1. 現在の設定を確認

`.claude/settings.json` が存在するか確認:

**ファイルが存在する場合:**

- 内容を読み込む
- 既存の設定を確認

**ファイルが存在しない場合:**

- `.claude` ディレクトリが存在しない場合は作成
- テンプレートから新規作成するか確認

### 2. 変更内容を確認

ユーザーに何を変更したいか確認:

- permissions の追加/削除
- allowedTools の追加/削除
- env 環境変数の設定
- hooks の追加/削除
- その他の設定

### 3. 設定を更新

`.claude/settings.json` を更新または作成。

### 4. 結果を報告

変更内容をユーザーに報告。

## 設定項目

### permissions

Claude に許可する操作:

```json
{
  "permissions": {
    "allow": ["Bash(*)", "Read(*)", "Write(*)"],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

### allowedTools

使用を許可するツール:

```json
{
  "allowedTools": ["Read", "Write", "Bash", "Glob", "Grep"]
}
```

### env

環境変数の設定:

```json
{
  "env": {
    "NODE_ENV": "development"
  }
}
```

### hooks

イベントフック（詳細は `/shiiman-claude:create-hook` を参照）

## テンプレートからの新規作成

ファイルが存在しない場合、以下のテンプレートを使用して作成できます。

### 基本テンプレート

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  },
  "allowedTools": []
}
```

### 推奨テンプレート（開発プロジェクト向け）

```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(git:*)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(git push --force)"
    ]
  },
  "allowedTools": [
    "Read",
    "Write",
    "Edit",
    "Bash",
    "Glob",
    "Grep"
  ],
  "env": {}
}
```

### ディレクトリ作成

`.claude` ディレクトリが存在しない場合:

```bash
mkdir -p .claude
```

## 重要な注意事項

- ✅ 既存の設定を保持しながら更新
- ✅ JSON の形式を正しく維持
- ✅ 変更前にバックアップを推奨
- ✅ ファイルが存在しない場合はテンプレートから作成可能
- ✅ `.claude` ディレクトリがない場合は自動作成
- ❌ 設定ファイル全体を上書きしない（マージする）
