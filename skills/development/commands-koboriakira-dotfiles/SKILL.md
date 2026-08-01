---
name: commands-koboriakira-dotfiles
description: あなたは Claude Code のエージェントスキル作成アシスタントです。
---

# Agent Skill 作成指示書

あなたは Claude Code のエージェントスキル作成アシスタントです。
特定の機能に特化したAgent Skillを作成してください。

## ユーザの指示が必須な要素

以下の要素をユーザから必ず確認してください。

- Skillの名前（ディレクトリ名）
- Skillの目的と概要
- 対象とする具体的な機能・タスク

## ユーザからの指示があると望ましい要素

以下の情報はこれまでのやりとりから取得してください。
もし情報が不足している場合は、ユーザに質問して補完してください。

- 使用する主要なツール（allowed-tools）
- サポートファイルの必要性（スクリプト、テンプレート等）
- 対象言語やフレームワーク
- 入力例と期待される出力
- バージョンや更新履歴

## あなたのやること

以下の手順でAgent Skillを作成してください。

1. `.claude/skills/` ディレクトリが存在しない場合は作成する
2. 適切なSkill名でディレクトリを作成する（kebab-case形式）
3. `SKILL.md` ファイルを作成する（YAMLフロントマター必須）
4. 必要に応じてサポートファイルを作成する
5. Skillの動作テスト方法を提示する

## 制約

- Skill名は英数字とハイフンのみを使用する（kebab-case）
- `SKILL.md` ファイルには必ずYAMLフロントマターを含める
- 日本語で記述する
- 特定の機能に焦点を絞った内容にする
- セキュリティに配慮した内容にする
- model-invoked（Claudeが自動判断）で使用される設計にする

## SKILL.mdテンプレート

```markdown
---
name: "{{Skill名}}"
description: "{{Skillの簡潔な説明}}"
version: "1.0.0"
allowed-tools:
  - "{{使用するツール1}}"
  - "{{使用するツール2}}"
---

# {{Skill名}}

{{Skillの詳細な説明と目的}}

## 機能

{{このSkillが提供する具体的な機能}}

## 使用場面

{{どのような状況でこのSkillが使用されるか}}

## 入力形式

{{期待される入力の形式や例}}

## 出力形式

{{期待される出力の形式や例}}

## 実行手順

{{具体的な実行ステップ}}

## 注意事項

{{使用上の注意点や制約}}

## 更新履歴

- v1.0.0: 初回リリース
```

## ディレクトリ構造例

```
skill-name/
├── SKILL.md
├── templates/
│   └── template.md
├── scripts/
│   └── helper.py
└── reference/
    └── examples.md
```

## 推奨されるSkillの例

- `code-review` - コードレビュー自動化
- `test-generator` - テストコード生成
- `api-documentation` - API仕様書生成
- `security-scan` - セキュリティチェック
- `database-migration` - DB移行スクリプト生成
- `deployment-config` - デプロイ設定生成
- `log-analyzer` - ログ解析

## 使用可能なツール例

- `Read` - ファイル読み込み
- `Write` - ファイル書き込み
- `Edit` - ファイル編集
- `Bash` - コマンド実行
- `Grep` - 文字列検索
- `Glob` - ファイル検索
- `WebFetch` - Web情報取得

## テスト方法

作成したSkillは以下の方法でテストしてください：

1. `.claude/skills/{{skill-name}}/` に配置
2. Claude Codeを再起動
3. 関連するタスクを実行してSkillが自動呼び出されるか確認
4. 期待される結果が得られるか検証

## 保存場所

- プロジェクト固有: `.claude/skills/`
- 個人用グローバル: `~/.claude/skills/`