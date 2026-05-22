---
name: dev:developing
description: |
  TODO.mdのタスクを実行。TDD/E2E/TASKラベルに応じたワークフローで実装。
  Worktree内での独立した開発を支援。

  Trigger:
  実装, 開発, /dev:impl, implementing, develop
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - mcp__claude-in-chrome__tabs_context_mcp
  - mcp__claude-in-chrome__tabs_create_mcp
  - mcp__claude-in-chrome__navigate
  - mcp__claude-in-chrome__find
  - mcp__claude-in-chrome__computer
  - mcp__claude-in-chrome__form_input
  - mcp__claude-in-chrome__read_page
  - mcp__claude-in-chrome__resize_window
---

# 実装（dev:developing）

## 概要

TODO.mdのタスクを実行する。タスクのラベルに応じてTDDまたはE2Eワークフローを適用。

## 入力

- `docs/features/{feature-slug}/stories/{story-slug}/TODO.md`
- feature-slug, story-slug

## 出力

- 実装コード
- テストコード（TDDタスク）
- コミット

---

## ワークフロー分岐

```
TODO.mdを読み込み
    ↓
タスクのラベルを確認
    ├─ [TASK] → TASKワークフロー
    ├─ [TDD] → TDDワークフロー
    └─ [E2E] → E2Eワークフロー
```

**実行順序**: TASKタスクは通常、最初に実行（環境構築が必要なため）

---

## TASKワークフロー

`[TASK]` ラベル付きタスクに適用。設定/セットアップ/インフラ構築を実行。

```
[1/3] 実行（EXEC）
    → agents/task-execute.md [sonnet]
    → 設定ファイル作成、コマンド実行
        ↓
[2/3] 検証（VERIFY）
    → ファイル存在確認、ビルド確認
        ↓
[3/3] コミット
```

→ 詳細: [references/task-flow.md]

### TASKタスク実行

```javascript
// [EXEC] タスク実行
Task({
  description: "TASKタスク実行",
  prompt: `以下のTASKタスクを実行してください。
タスク: {task_name}
説明: {task_description}

1. 必要な設定ファイルを作成/編集
2. 必要なコマンドを実行
3. 結果を報告`,
  subagent_type: "general-purpose",
  model: "sonnet"
})
```

```javascript
// [VERIFY] 検証
Task({
  description: "TASK検証",
  prompt: `以下のTASKタスクの検証を行ってください。
タスク: {task_name}

検証内容:
- ファイル存在確認
- ビルド/コンパイル確認
- サービス起動確認（該当する場合）`,
  subagent_type: "general-purpose",
  model: "haiku"
})
```

---

## TDDワークフロー

`[TDD]` ラベル付きタスクに適用。RED→GREEN→REFACTORサイクルを厳格に遵守。

```
[1/6] テスト作成（RED）
    → agents/tdd-write-test.md [sonnet]
    → テスト実行して失敗を確認
    → コミット（テストのみ）
        ↓
[2/6] 実装（GREEN）
    → agents/tdd-implement.md [sonnet]
    → テスト実行して成功を確認
    → テストは変更しない
        ↓
[3/6] リファクタリング
    → agents/tdd-refactor.md [opus]
    → テスト実行して成功を確認
        ↓
[4/6] セルフレビュー
    → コード品質チェック
    → 問題あれば修正→テスト
        ↓
[5/6] 品質チェック
    → lint/format/build
        ↓
[6/6] コミット
```

→ 詳細: [references/tdd-flow.md]

### TDDタスク実行

```javascript
// [RED] テスト作成
Task({
  description: "テスト作成",
  prompt: `以下のタスクのテストを作成してください。
タスク: {task_name}
説明: {task_description}
入力: {input}
出力: {output}

テストのみ作成し、実装は書かないでください。
テストを実行して失敗することを確認してください。`,
  subagent_type: "general-purpose",
  model: "sonnet"
})
```

```javascript
// [GREEN] 実装
Task({
  description: "実装",
  prompt: `テストを通す最小限の実装を行ってください。
タスク: {task_name}

重要:
- テストは変更しない
- 最小限の実装のみ
- 将来の要件を先取りしない`,
  subagent_type: "general-purpose",
  model: "sonnet"
})
```

```javascript
// [REFACTOR] リファクタリング
Task({
  description: "リファクタリング",
  prompt: `コード品質を改善してください。
対象: {task_name}

チェックリスト:
- 単一責任原則
- 重複排除
- 命名改善
- 複雑度低減

重要: テストが成功し続けることを確認`,
  subagent_type: "general-purpose",
  model: "opus"
})
```

---

## E2Eワークフロー

`[E2E]` ラベル付きタスクに適用。agent-browserで操作フロー検証。

```
[1/4] UI実装
    → agents/e2e-implement.md [sonnet]
    → コンポーネント作成
        ↓
[2/4] agent-browser検証（ループ）
    → agents/e2e-verify.md [haiku]
    → 操作フロー検証
    → 問題あれば修正→再検証
        ↓
[3/4] 品質チェック
    → lint/format/build
        ↓
[4/4] コミット
```

→ 詳細: [references/e2e-flow.md]

### E2Eタスク実行

```javascript
// [IMPL] UI実装
Task({
  description: "UI実装",
  prompt: `UIコンポーネントを実装してください。
タスク: {task_name}
説明: {task_description}

コンポーネント設計:
- Props定義
- イベントハンドラ
- スタイリング`,
  subagent_type: "general-purpose",
  model: "sonnet"
})
```

```javascript
// [AUTO] agent-browser検証
Task({
  description: "agent-browser検証",
  prompt: `MCP agent-browserで操作フローを検証してください。

検証手順:
1. tabs_context_mcp でタブ情報取得
2. tabs_create_mcp で新規タブ作成
3. navigate で開発サーバーに遷移
4. find で要素検索
5. computer/form_input で操作実行
6. read_page で結果確認
7. スクリーンショット取得

期待する動作:
{expected_behavior}`,
  subagent_type: "general-purpose",
  model: "haiku"
})
```

---

## テスト実行（サブエージェント）

トークン消費を抑えるため、テスト実行はサブエージェントに委譲。

```javascript
Task({
  description: "テスト実行",
  prompt: `プロジェクトのテストを実行し、結果を報告してください。

テストコマンド: npm test / cargo test / pytest など

報告形式:
- 全テスト成功: "SUCCESS: X tests passed"
- 失敗あり: "FAILED:" + 失敗したテスト名とエラーのみ`,
  subagent_type: "general-purpose",
  model: "haiku"
})
```

---

## セルフレビュー

フェーズ完了時にコード品質をチェック。

```javascript
Task({
  description: "セルフレビュー",
  prompt: `変更されたファイルをレビューしてください。

レビュー観点:
1. TDD/テスト品質
2. コード品質（可読性、命名、複雑度）
3. セキュリティ
4. 設計原則

報告形式:
- 問題なし: "PASSED"
- 問題あり: "ISSUES:" + Critical/Warningのみ`,
  subagent_type: "Explore",
  model: "opus"
})
```

---

## 品質チェック

```bash
npm run lint && npm run format && npm run build
# または
cargo clippy && cargo fmt && cargo build
# または
flake8 && black . && pytest
```

---

## TODO.md更新

タスク完了時にTODO.mdを更新:

```javascript
Edit({
  file_path: "docs/features/{feature-slug}/stories/{story-slug}/TODO.md",
  old_string: "- [ ] [TDD][GREEN] validateEmail の実装",
  new_string: "- [x] [TDD][GREEN] validateEmail の実装"
})
```

---

## フェーズ完了確認

```javascript
AskUserQuestion({
  questions: [{
    question: "フェーズが完了しました。次のフェーズに進みますか？",
    header: "フェーズ完了",
    options: [
      { label: "承認", description: "次のフェーズに進む" }
    ],
    multiSelect: false
  }]
})
```

---

## 完了条件

- [ ] すべてのTASKタスクが完了（EXEC→VERIFY）
- [ ] すべてのTDDタスクが完了（RED→GREEN→REFACTOR）
- [ ] すべてのE2Eタスクが完了（IMPL→AUTO）
- [ ] 全テストが成功
- [ ] 品質チェックが通過
- [ ] TODO.mdが全て完了マーク

## 関連スキル

- **dev:story-to-tasks**: タスクリスト生成（TDD/E2E/TASK分類）
- **dev:feedback**: 実装後のフィードバック

## 参照ルール

- TDD/E2E/TASK分岐: `.claude/rules/workflow/workflow-branching.md`
- TDDワークフロー: `.claude/rules/workflow/tdd-workflow.md`
- E2Eサイクル: `.claude/rules/workflow/e2e-cycle.md`
