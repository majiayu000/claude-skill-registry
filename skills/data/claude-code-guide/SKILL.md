---
name: claude-code-guide
description: "Claude Code 拡張機能（サブエージェント、プラグイン、スキル）の作成・設定方法。トリガー: 拡張機能, agent作成, skill作成, plugin作成, CLI自動承認, headless, エージェント, プラグイン, スキル"
user-invocable: true
allowed-tools: Read
model: haiku
---

# Claude Code 拡張機能ガイド

Claude Code の拡張機能を作成・設定するためのリファレンス。

## 概要

| 拡張機能 | 用途 | 詳細 |
|---------|------|------|
| サブエージェント | 特定タスクを委譲するカスタムエージェント | sub-agents.md |
| プラグイン | 複数プロジェクト間で共有する拡張パッケージ | plugins.md |
| スキル | 自動選択・実行される条件付き処理 | skills.md |
| CLI自動承認 | CI/CD向け非対話モード | cli-automation.md |

## クイックリファレンス

### ファイル配置

```
~/.claude/                    # ユーザーレベル（全プロジェクト）
├── agents/agent-name.md
├── skills/skill-name/SKILL.md
└── plugins/...

.claude/                      # プロジェクトレベル（version control推奨）
├── agents/agent-name.md
└── skills/skill-name/SKILL.md
```

### 組み込みサブエージェント

- `Explore`: 読み取り専用、コードベース探索用
- `Plan`: 計画立案用
- `general-purpose`: 複雑なマルチステップタスク

## 詳細ドキュメント

各拡張機能の詳細は以下を参照:

- `sub-agents.md` - サブエージェントの作成方法
- `plugins.md` - プラグインの構造と設定
- `skills.md` - スキルの定義とメタデータ
- `cli-automation.md` - CLI自動承認とヘッドレスモード

## 公式ドキュメント

- [Sub-agents](https://code.claude.com/docs/ja/sub-agents)
- [Plugins](https://code.claude.com/docs/ja/plugins)
- [Skills](https://code.claude.com/docs/ja/skills)
- [Headless/CLI](https://code.claude.com/docs/ja/headless)
- [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) - **最新機能の調査時は必ず確認**

## 調査時の注意

Claude Code の機能や設定について調査する際は、必ず以下を確認すること:

1. **CHANGELOG.md** - 最新バージョンで追加・変更された機能を把握
2. **公式ドキュメント** - 上記リンク先で詳細仕様を確認
3. **既存設定との整合性** - このリポジトリの設定と矛盾がないか確認
