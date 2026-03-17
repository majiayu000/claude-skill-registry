---
name: meta-skill-creator
description: |
  スキルを作成・更新・プロンプト改善するためのメタスキル。
  **collaborative**モードでユーザーと対話しながら共創し、
  抽象的なアイデアから具体的な実装まで柔軟に対応する。
  **orchestrate**モードでタスクの実行エンジン（Claude Code / Codex / 連携）を選択。

  Anchors:
  • Continuous Delivery (Jez Humble) / 適用: 自動化パイプライン / 目的: 決定論的実行
  • The Lean Startup (Eric Ries) / 適用: Build-Measure-Learn / 目的: 反復改善
  • Domain-Driven Design (Eric Evans) / 適用: ユビキタス言語 / 目的: 一貫した語彙
  • Design Thinking (IDEO) / 適用: ユーザー中心設計 / 目的: 共感と共創
  • Microservices Patterns (Richardson) / 適用: サービス委譲 / 目的: 疎結合な連携

  Trigger:
  新規スキルの作成、既存スキルの更新、プロンプト改善を行う場合に使用。
  スキル作成, スキル更新, プロンプト改善, skill creation, skill update, improve prompt,
  Codexに任せて, assign codex, Codexで実行, GPTに依頼, 実行モード選択, どのAIを使う
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Skill Creator

## 概要

スキルを作成・更新・プロンプト改善するためのメタスキル。
**Collaborative First**でユーザーと対話しながら共創、**Script First**で決定論的処理を自動化、**Progressive Disclosure**で必要なリソースのみを読み込む。

## 設計原則

| 原則 | 説明 |
|------|------|
| **Collaborative First** | ユーザーとの対話を通じて要件を明確化 |
| Script First | 決定論的処理はスクリプトで実行（100%精度） |
| Progressive Disclosure | 必要な時に必要なリソースのみ読み込み |
| Custom Script Support | 24タイプに収まらない独自スクリプトも生成 |
| Self-Contained Skills | 各スキルは独自のnode_modules・依存関係を持つ |

## モード一覧

| モード | 用途 | 開始方法 |
|--------|------|----------|
| **collaborative** | ユーザー対話型スキル共創（推奨） | AskUserQuestionでインタビュー開始 |
| **orchestrate** | 実行エンジン選択（Claude/Codex/連携） | AskUserQuestionでヒアリング開始 |
| create | 要件が明確な場合の新規作成 | `.claude/skills/meta-skill-creator/scripts/detect_mode.js --request "新規スキル"` |
| update | 既存スキル更新 | `.claude/skills/meta-skill-creator/scripts/detect_mode.js --request "更新" --skill-path <path>` |
| improve-prompt | プロンプト改善 | `.claude/skills/meta-skill-creator/scripts/analyze_prompt.js --skill-path <path>` |

## 実行エンジン（orchestrateモード）

| エンジン | 説明 | 適用場面 |
|----------|------|----------|
| **claude** | Claude Code単独実行 | ファイル編集、Git操作、コードベース深い理解 |
| **codex** | Codex (GPT-5.2) 単独実行 | 独立したタスク、別視点での分析 |
| **claude-to-codex** | Claude → Codex連携 | コンテキスト共有が必要な複合タスク |

## 抽象度レベル

| レベル | 説明 | 例 |
|--------|------|-----|
| **L1: Concept** | アイデア・課題レベル | 「開発効率を上げたい」 |
| **L2: Capability** | 機能・能力レベル | 「PRを自動作成したい」 |
| **L3: Implementation** | 実装・詳細レベル | 「GitHub APIでPR作成」 |

**抽象度が高いほど、インタビューを通じて具体化する。**
📖 詳細: [references/abstraction-levels.md](.claude/skills/meta-skill-creator/references/abstraction-levels.md)

---

# Part 0: Collaborative モード（推奨）

ユーザーと対話しながらスキルを共創するモード。

## ワークフロー

```
Phase 0-1: 初期ヒアリング
  Q1: 何を実現したいですか？ → 抽象度レベル判定
  Q2: 対象は何ですか？ → コンテキスト特定
  Q3: 頻度・規模は？ → 複雑さ判定
      ↓
Phase 0-2: 機能ヒアリング
  Q4: 必要な機能は？
  Q5: 外部連携は？
  Q6: スクリプトは？
      ↓
Phase 0-3: 構成ヒアリング
  Q7: 構成タイプは？（シンプル/標準/フル）
  Q8: 優先事項は？
      ↓
Phase 0-4: 要件確認
  → ユーザー確認後、Phase 1へ
```

📖 詳細: [agents/interview-user.md](.claude/skills/meta-skill-creator/agents/interview-user.md)

---

# Part 0.5: Orchestrate モード（実行エンジン選択）

**スキル作成プロセス内**で、特定のサブタスクを最適な実行エンジンに委譲するモード。

```
skill-creator実行中 → 特定タスクでCodex使用 → Claude Code継続
```

## ワークフロー

```
Phase 1-2: ヒアリング
  → .claude/skills/meta-skill-creator/agents/interview-execution-mode.md
  タスク内容・コンテキスト判定 → モード推奨・選択
      ↓
Phase 3: 実行（モード別分岐）
  claude: 直接実行
  codex: .claude/skills/meta-skill-creator/scripts/assign_codex.js
  claude-to-codex: コンテキスト収集 → Codex
      ↓
Phase 4: 結果確認・統合
```

📖 モード選択基準・詳細フローチャート: [references/execution-mode-guide.md](.claude/skills/meta-skill-creator/references/execution-mode-guide.md)

## 関連リソース

| リソース | 読み込み条件 |
|----------|-------------|
| [interview-execution-mode.md](.claude/skills/meta-skill-creator/agents/interview-execution-mode.md) | Phase 1-2 |
| [delegate-to-codex.md](.claude/skills/meta-skill-creator/agents/delegate-to-codex.md) | Codex実行時 |
| [execution-mode-guide.md](.claude/skills/meta-skill-creator/references/execution-mode-guide.md) | 判断に迷った時 |

---

# Part 1: スキル作成ワークフロー（createモード）

```
Phase 1: 分析（LLM）
  .claude/skills/meta-skill-creator/agents/analyze-request.md
  → .claude/skills/meta-skill-creator/agents/extract-purpose.md
  → .claude/skills/meta-skill-creator/agents/define-boundary.md
      ↓
Phase 2: 設計（LLM + Script検証）
  .claude/skills/meta-skill-creator/agents/select-anchors.md ─┐
  .claude/skills/meta-skill-creator/agents/define-trigger.md ─┤
      → .claude/skills/meta-skill-creator/agents/design-workflow.md
      → .claude/skills/meta-skill-creator/scripts/validate_workflow.js
      ↓
Phase 3: 構造計画（LLM + Script検証）
  .claude/skills/meta-skill-creator/agents/plan-structure.md
  → .claude/skills/meta-skill-creator/scripts/validate_plan.js
      ↓
Phase 4: 生成（Script）
  .claude/skills/meta-skill-creator/scripts/init_skill.js
  → .claude/skills/meta-skill-creator/scripts/generate_skill_md.js
  → .claude/skills/meta-skill-creator/scripts/generate_agent.js
      ↓
Phase 5: フィードバック機構生成（Script）
  → LOGS.md, EVALS.json, references/patterns.md を生成
      ↓
Phase 6: 検証（Script）
  .claude/skills/meta-skill-creator/scripts/validate_all.js
  → .claude/skills/meta-skill-creator/scripts/log_usage.js
```

---

# Part 2: スクリプト生成ワークフロー

## 24種類のスクリプトタイプ

| カテゴリ | タイプ |
|----------|--------|
| API関連 | api-client, webhook, scraper, notification |
| データ処理 | parser, transformer, aggregator, file-processor |
| ストレージ | database, cache, queue |
| 開発ツール | git-ops, test-runner, linter, formatter, builder |
| インフラ | deployer, docker, cloud, monitor |
| 統合 | ai-tool, mcp-bridge, shell |
| 汎用 | universal |

📖 詳細: [references/script-types-catalog.md](.claude/skills/meta-skill-creator/references/script-types-catalog.md)

## 生成ワークフロー

```
Phase 1: 要件分析（LLM）→ script-requirement.json
Phase 2: ランタイム判定（Script）→ runtime-config.json
Phase 3: 設計（LLM）→ script-design.json
Phase 4: 変数設計（LLM）→ variables.json
Phase 5: コード生成（LLM）→ script-template.{ext}
Phase 6: コード展開（Script）→ 実行可能スクリプト
Phase 7: 検証（Script）
```

📖 カスタムスクリプト: [agents/design-custom-script.md](.claude/skills/meta-skill-creator/agents/design-custom-script.md)

---

# Part 3: フィードバック＆自己改善ワークフロー

## 3.1 毎回実行後（必須）

スキル実行後は必ずフィードバックを記録する：

```bash
# 成功時
node .claude/skills/meta-skill-creator/scripts/log_usage.js --result success --phase "Phase 4" --notes "完了"

# 失敗時
node .claude/skills/meta-skill-creator/scripts/log_usage.js --result failure --phase "Phase 3" --error "ValidationError" --notes "理由"
```

**記録先**:
| ファイル | 更新内容 |
|----------|----------|
| LOGS.md | 実行ログ（日時、結果、フェーズ、メモ） |
| EVALS.json | メトリクス（成功率、実行回数、平均時間） |

## 3.2 パターン発見時

成功/失敗パターンを発見したら記録する：

```
.claude/skills/meta-skill-creator/agents/analyze-feedback.md → パターン検出
     ↓
.claude/skills/meta-skill-creator/agents/save-patterns.md
     → .claude/skills/meta-skill-creator/references/patterns.md 更新
```

**パターン形式**:
- 成功パターン: 状況 → アプローチ → 結果 → 適用条件
- 失敗パターン: 状況 → 問題 → 原因 → 教訓

## 3.3 改善サイクル

定期的（10回実行ごと、またはエラー率閾値超過時）に改善を検討：

```
.claude/skills/meta-skill-creator/scripts/collect_feedback.js → feedback-data.json出力
     ↓
.claude/skills/meta-skill-creator/agents/analyze-feedback.md → パターン分析・改善提案生成
     ├─ patterns[] あり → .claude/skills/meta-skill-creator/agents/save-patterns.md
     │                  → .claude/skills/meta-skill-creator/references/patterns.md更新
     └─ suggestions[] あり → .claude/skills/meta-skill-creator/agents/design-self-improvement.md
     ↓
.claude/skills/meta-skill-creator/scripts/apply_self_improvement.js → 改善適用
  --dry-run: 事前確認（推奨）
  --backup: バックアップ作成
  --auto-only: 自動適用可能なもののみ
```

📖 詳細: [references/self-improvement-cycle.md](.claude/skills/meta-skill-creator/references/self-improvement-cycle.md)

## 3.4 フィードバック対象ファイル

| ファイル | 用途 | 更新タイミング | スクリプト/エージェント |
|----------|------|----------------|------------------------|
| LOGS.md | 実行ログ | 毎回実行後 | [scripts/log_usage.js](.claude/skills/meta-skill-creator/scripts/log_usage.js) |
| EVALS.json | メトリクス | 毎回実行後 | [scripts/log_usage.js](.claude/skills/meta-skill-creator/scripts/log_usage.js) |
| references/patterns.md | 成功/失敗パターン | パターン発見時 | [agents/save-patterns.md](.claude/skills/meta-skill-creator/agents/save-patterns.md) |

---

# Part 4: ライブラリ管理（Self-Contained Skills）

スキルは自己完結型。依存関係は**スキルディレクトリ内**で管理し、PNPMを使用する。

## 4.1 設計思想

| 原則 | 説明 |
|------|------|
| 自己完結 | 各スキルが独自のnode_modules・package.jsonを持つ |
| 分離 | プロジェクト本体の依存関係と干渉しない |
| 再現性 | pnpm-lock.yamlで依存関係を固定 |

## 4.2 依存関係管理コマンド

```bash
# スキルの依存関係をインストール
node .claude/skills/meta-skill-creator/scripts/install_deps.js

# パッケージを追加
node .claude/skills/meta-skill-creator/scripts/add_dependency.js axios

# 開発依存関係として追加
node .claude/skills/meta-skill-creator/scripts/add_dependency.js typescript --dev

# 他のスキルに対して実行
node .claude/skills/meta-skill-creator/scripts/install_deps.js --skill-path .claude/skills/my-skill
```

## 4.3 スキル構造（依存関係あり）

```
.claude/skills/my-skill/
├── package.json       # 依存関係定義
├── pnpm-lock.yaml     # 依存関係ロック（自動生成）
├── node_modules/      # 依存関係（スキル内に配置）
├── SKILL.md
├── scripts/
│   └── my-script.js   # import from 'axios' 等が使用可能
└── ...
```

📖 詳細: [references/library-management.md](.claude/skills/meta-skill-creator/references/library-management.md)

---

# Part 5: Progressive Disclosure リソースマップ

リソースは**必要な時のみ**読み込む。詳細は [resource-map.md](.claude/skills/meta-skill-creator/references/resource-map.md) を参照。

## リソース概要

| カテゴリ | 数 | 主な読み込み条件 |
|----------|-----|-----------------|
| agents/ | 20 | モード・Phase別に必要時のみ |
| references/ | 23 | 設計・判断・詳細確認時 |
| scripts/ | 25 | 決定論的処理実行時（utils.js共通） |
| assets/ | 17 | 生成・テンプレート展開時 |
| schemas/ | 23 | JSON検証時 |

## 主要リソース（高頻度）

| リソース | 読み込み条件 |
|----------|-------------|
| [agents/interview-user.md](.claude/skills/meta-skill-creator/agents/interview-user.md) | collaborativeモード |
| [agents/analyze-request.md](.claude/skills/meta-skill-creator/agents/analyze-request.md) | createモード |
| [scripts/utils.js](.claude/skills/meta-skill-creator/scripts/utils.js) | 全スクリプト共通 |
| [scripts/init_skill.js](.claude/skills/meta-skill-creator/scripts/init_skill.js) | スキル初期化 |
| [scripts/log_usage.js](.claude/skills/meta-skill-creator/scripts/log_usage.js) | 毎回実行後 |
| [references/script-commands.md](.claude/skills/meta-skill-creator/references/script-commands.md) | スクリプト実行時 |
| [references/resource-map.md](.claude/skills/meta-skill-creator/references/resource-map.md) | 全リソース詳細 |

📖 全リソース詳細: [references/resource-map.md](.claude/skills/meta-skill-creator/references/resource-map.md)

---

## ベストプラクティス

| すべきこと | 避けるべきこと |
|-----------|---------------|
| Script優先（決定論的処理） | 全リソースを一度に読み込む |
| LLMは判断・創造のみ | Script可能な処理をLLMに任せる |
| Progressive Disclosure | 具体例をテンプレートに書く |
| 中間出力は.tmp/に保存 | 中間ファイルを省略 |

---

## 変更履歴

| Version | Date | Changes |
|---------|------|---------|
| **5.7.0** | **2026-01-21** | **SKILL.md最適化: Part 5をresource-map.mdに分離（485→375行、23%削減）、スクリプトutils.js統合完了** |
| 5.6.1 | 2026-01-21 | DRYリファクタリング: utils.js共通モジュール作成、約270行の重複コード排除 |
| 5.6.0 | 2026-01-21 | Self-Contained Skills: PNPM依存関係管理、package.json自動生成、install_deps.js/add_dependency.js追加 |
| 5.5.2 | 2026-01-20 | 参照パス完全統一: ワークフロー図・コマンド例・テーブル内のすべての参照を完全パス化（105参照） |
| 5.5.1 | 2026-01-20 | 参照パス統一: Markdownリンクをリポジトリルートからの相対パスに統一 |
| 5.5.0 | 2026-01-20 | 最適化: SKILL.md 521→420行に削減、Part 0.5詳細をexecution-mode-guide.mdへ移動 |
| 5.4.0 | 2026-01-20 | フィードバック機構強化: Part 3をフィードバック＆自己改善に拡張、save-patterns.mdエージェント追加 |
| 5.3.0 | 2026-01-15 | Progressive Disclosure完全化: 全ファイル（19 refs, 23 schemas, 34 assets, 22 scripts）に読み込み条件追加 |
| 5.2.1 | 2026-01-15 | Codex連携の目的明確化: スキル作成内サブタスク委譲用、Claude Code⇄Codexラウンドトリップパターン |
| 5.2.0 | 2026-01-15 | Orchestrateモード追加: Codex連携機能、実行エンジン選択（claude/codex/claude-to-codex） |
| 5.1.0 | 2026-01-15 | リファクタリング: SKILL.md簡素化、agents/フォーマット統一、workflow-patterns.md統合 |
| 5.0.0 | 2026-01-15 | Collaborative First追加、抽象度レベル対応、カスタムスクリプト対応 |
| 4.0.0 | 2026-01-13 | スクリプト生成ワークフロー追加、自己改善サイクル追加 |
| 3.0.0 | 2026-01-06 | 3モード対応（create/update/improve-prompt） |
