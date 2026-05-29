---
name: plugin-marketplace-creator
description: Plugin Marketplace構造を対話的に生成し、marketplace.json、plugin.json、ディレクトリ構造を自動作成するスキル。Use when users mention "plugin marketplace", "marketplace作成", "プラグインカタログ", "複数のプラグインを管理", "チーム向けプラグイン配布", or need to create marketplace.json/plugin.json files. Also use when users want to organize multiple Claude Code plugins for distribution.
---

# Plugin Marketplace Creator

## Overview

このスキルは、Claude Code Plugin Marketplaceの完全な構造を対話的に生成します。marketplace.json、個別のplugin.json、推奨ディレクトリ構造、テンプレートファイルを自動作成し、`claude plugin validate`での検証までサポートします。

## Workflow Decision Tree

ユーザーの要求に応じて適切なワークフローを選択します：

```
ユーザーの要求
├─ 新規Marketplace作成 → Full Workflow (Step 1-5)
├─ 既存Marketplaceにプラグイン追加 → Step 3-5
├─ 既存ツールとの連携 → Integration Workflow
└─ 設定ファイルのみ生成 → Step 4-5
```

## Step 1: Initialize Marketplace Structure

### 1-1. 基本情報の収集

AskUserQuestionツールを使用して、以下の情報を対話的に収集します：

**質問1: Marketplace名**
- Header: "Marketplace名"
- Question: "Marketplaceの名前を指定してください（kebab-case形式）"
- Options:
  - Label: "company-tools", Description: "企業ツール向け（推奨）"
  - Label: "team-plugins", Description: "チーム向けプラグイン"
  - Label: "project-marketplace", Description: "プロジェクト固有"

**質問2: 配置ディレクトリ**
- Header: "配置先"
- Question: "Marketplaceを作成するディレクトリを指定してください"
- Options:
  - Label: "./my-marketplace", Description: "カレントディレクトリ配下（推奨）"
  - Label: "../claude-marketplace", Description: "親ディレクトリ"
  - Label: "~/.claude/marketplaces/", Description: "グローバルmarketplace"

### 1-2. ディレクトリ構造の作成

`scripts/init_marketplace.py`を実行してディレクトリ構造を作成します：

```bash
python3 ${CLAUDE_SKILL_ROOT}/scripts/init_marketplace.py <marketplace-name> --path <output-directory>
```

生成される構造：
```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── .gitkeep
├── README.md
└── .gitignore
```

## Step 2: Configure Marketplace Metadata

### 2-1. オーナー情報の収集

AskUserQuestionツールで収集：

**質問1: オーナー名**
- Header: "Owner"
- Question: "Marketplaceのメンテナー名を入力してください"
- Options:
  - Label: "DevTools Team", Description: "開発チーム名"
  - Label: "Engineering", Description: "エンジニアリング部門"
  - Label: "個人名", Description: "個人メンテナー"

**質問2: メールアドレス（オプション）**
- Header: "Email"
- Question: "メンテナーのメールアドレスを入力しますか？"
- Options:
  - Label: "入力する", Description: "team@example.com形式"
  - Label: "スキップ", Description: "メールアドレスなし"

### 2-2. メタデータ設定（オプション）

**質問: メタデータ追加**
- Header: "Metadata"
- Question: "追加のメタデータを設定しますか？"
- Options:
  - Label: "はい", Description: "description, version, pluginRoot等を設定"
  - Label: "いいえ", Description: "最小限の設定のみ"

メタデータを追加する場合：
- **description**: Marketplaceの説明（1-2文）
- **version**: セマンティックバージョン（例: 1.0.0）
- **pluginRoot**: プラグインのルートディレクトリ（推奨: `./plugins`）

## Step 3: Add Plugins

### 3-1. プラグイン追加方法の選択

**質問: プラグイン追加方法**
- Header: "プラグイン追加"
- Question: "プラグインをどのように追加しますか？"
- MultiSelect: true
- Options:
  - Label: "対話的に追加", Description: "1つずつ情報を入力"
  - Label: "既存プラグインをインポート", Description: "既存のplugin.jsonから読み込み"
  - Label: "新規作成と連携", Description: "/claude-code:create-*コマンドを使用"

### 3-2. プラグイン情報の収集

各プラグインについて以下を収集：

**必須フィールド**:
- `name`: プラグイン名（kebab-case）
- `source`: ソースタイプ
  - 相対パス: `"./plugins/plugin-name"`
  - GitHub: `{"source": "github", "repo": "owner/repo"}`
  - Git URL: `{"source": "url", "url": "https://..."}`

**オプションフィールド**:
- `description`: プラグインの説明
- `version`: バージョン番号
- `author`: 作成者情報
- `homepage`: ドキュメントURL
- `repository`: リポジトリURL
- `license`: ライセンス（例: MIT, Apache-2.0）
- `keywords`: 検索キーワード配列
- `category`: カテゴリー（例: productivity, devops）
- `tags`: タグ配列
- `strict`: `true`（デフォルト）または `false`

### 3-3. プラグイン追加の繰り返し

**質問: 追加のプラグイン**
- Header: "追加"
- Question: "別のプラグインを追加しますか？"
- Options:
  - Label: "はい", Description: "さらにプラグインを追加"
  - Label: "いいえ", Description: "完了"

## Step 4: Generate Configuration Files

### 4-1. marketplace.jsonの生成

`scripts/generate_marketplace.py`を実行：

```bash
python3 ${CLAUDE_SKILL_ROOT}/scripts/generate_marketplace.py \
  --name <marketplace-name> \
  --owner-name "<owner-name>" \
  --owner-email "<owner-email>" \
  --plugins <plugins-json> \
  --output <output-path>
```

生成されるmarketplace.jsonは`references/marketplace-schema.md`のスキーマに準拠します。

### 4-2. 個別plugin.jsonの生成

各プラグインについて、`scripts/generate_plugin.py`を実行：

```bash
python3 ${CLAUDE_SKILL_ROOT}/scripts/generate_plugin.py \
  --name <plugin-name> \
  --description "<description>" \
  --version <version> \
  --output <plugin-directory>/.claude-plugin/plugin.json
```

### 4-3. テンプレートファイルの配置

以下のテンプレートを`assets/templates/`からコピー：
- `README.md` → プロジェクトルート
- `.gitignore` → プロジェクトルート

## Step 5: Validate Marketplace

### 5-1. 自動検証の実行

Bashツールを使用して検証：

```bash
cd <marketplace-directory>
claude plugin validate .
```

または：

```bash
cd <marketplace-directory>
/plugin validate
```

### 5-2. 検証結果の確認

検証で確認される項目：
- ✅ marketplace.jsonのJSON構文
- ✅ 必須フィールドの存在（name, owner, plugins）
- ✅ プラグインソースパスの存在確認
- ✅ plugin.jsonの構文（strict: trueの場合）
- ✅ 命名規則（kebab-case）

### 5-3. エラー修正

検証エラーが発生した場合：
1. エラーメッセージを分析
2. 該当箇所を修正
3. 再度検証を実行

## Integration with Existing Tools

### `/claude-code:create-skill`との連携

新しいスキルを作成してmarketplaceに追加：

```bash
# Step 1: スキル作成
/claude-code:create-skill <skill-description>

# Step 2: スキルをmarketplaceに追加
# このスキルを再度呼び出して、作成されたスキルをプラグインとして追加
```

### `/claude-code:create-command`との連携

新しいコマンドを作成してmarketplaceに追加：

```bash
# Step 1: コマンド作成
/claude-code:create-command <command-description>

# Step 2: コマンドをmarketplaceに追加
```

### `/claude-code:create-subagent`との連携

新しいsubagentを作成してmarketplaceに追加：

```bash
# Step 1: subagent作成
/claude-code:create-subagent <subagent-description>

# Step 2: subagentをmarketplaceに追加
```

詳細は`references/integration-guide.md`を参照してください。

## Best Practices

### 予約済み名を避ける

以下のmarketplace名は使用できません：
- `claude-code-marketplace`
- `claude-code-plugins`
- `claude-plugins-official`
- `anthropic-marketplace`
- `anthropic-plugins`
- `agent-skills`
- `life-sciences`

### プラグイン命名規則

- **kebab-case**のみ使用
- 小文字と数字、ハイフンのみ
- 最大64文字
- 例: `code-formatter`, `deploy-tools`, `security-scanner`

### `pluginRoot`の活用

多数のプラグインを管理する場合、`metadata.pluginRoot`を設定して相対パスを簡潔化：

```json
{
  "metadata": {
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "formatter",
      "source": "formatter"  // "./plugins/formatter"と解釈される
    }
  ]
}
```

### `${CLAUDE_PLUGIN_ROOT}`変数の使用

プラグイン内のパス指定には必ず`${CLAUDE_PLUGIN_ROOT}`を使用：

```json
{
  "mcpServers": {
    "db-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server"
    }
  }
}
```

## Resources

### scripts/

- **`init_marketplace.py`**: Marketplaceディレクトリ構造を初期化
- **`generate_marketplace.py`**: marketplace.jsonを生成
- **`generate_plugin.py`**: plugin.jsonを生成

### references/

- **`marketplace-schema.md`**: marketplace.jsonの完全なスキーマ仕様
- **`plugin-schema.md`**: plugin.jsonのスキーマ仕様
- **`integration-guide.md`**: 既存ツールとの連携方法

### assets/templates/

- **`marketplace.json`**: Marketplaceテンプレート
- **`plugin.json`**: Pluginテンプレート
- **`README.md`**: プロジェクトREADMEテンプレート
- **`.gitignore`**: .gitignoreテンプレート
