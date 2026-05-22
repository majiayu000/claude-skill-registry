---
name: dev:story-to-tasks
description: |
  ストーリーからTDD/E2E/TASK分岐付きタスクリスト（TODO.md）を生成。
  ストーリー駆動開発の起点となるスキル。
  「タスクを作成」「/dev:story」で起動。

  Trigger:
  タスクを作成, ストーリーからタスク, /dev:story, story to tasks
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

# ストーリー → タスク生成（dev:story-to-tasks）

## 概要

ユーザーストーリーから実装可能なタスクリスト（TODO.md）を生成する。
各タスクにはTDD/E2E/TASKラベルを自動付与し、Worktree内での独立した開発を支援する。

## 3分類の定義

| カテゴリ | 対象 | ワークフロー | ステップ数 |
|----------|------|--------------|------------|
| **TDD** | ロジック、バリデーション、計算 | RED→GREEN→REFACTOR→REVIEW→CHECK→COMMIT | 6 |
| **E2E** | UIコンポーネント、レイアウト | IMPL→AUTO→CHECK→COMMIT | 4 |
| **TASK** | 設定、セットアップ、インフラ、ドキュメント | EXEC→VERIFY→COMMIT | 3 |

## 入力

- ユーザーからの会話（ストーリー説明）
- または docs/USER_STORIES.md
- feature-slug, story-slug（AskUserQuestionで確定）

## 出力

`docs/features/{feature-slug}/stories/{story-slug}/` に以下を保存:
- `story-analysis.json` - ストーリー分析結果
- `task-list.json` - タスクリスト
- `TODO.md` - TDD/E2E/TASKラベル付きタスク

---

## ワークフロー

```
Phase 0: Worktree判定・作成（条件付き）
    → ストーリーの粒度を判定
    → 大きい変更 → Worktree作成
    → 小さい変更 → スキップ
        ↓
Phase 1: ストーリー理解・slug確定
    → agents/analyze-story.md [opus]
    → AskUserQuestionでslug確定
    → story-analysis.json 出力
        ↓
Phase 2: タスク分解
    → agents/decompose-tasks.md [sonnet]
    → task-list.json 出力
        ↓
Phase 3: TDD/E2E/TASK分類
    → agents/assign-workflow.md [haiku]
    → TODO.md 出力
        ↓
Phase 4: ユーザー確認
    → AskUserQuestion で確認・承認
```

---

## Phase 0: Worktree判定・作成

### 0.1 粒度判定

ストーリーの粒度を判定し、Worktree作成の要否を決定する。

**Worktree作成が必要なケース**:
- 新機能開発（複数ファイル/ディレクトリにまたがる）
- リファクタリング（複数コンポーネント影響）
- アーキテクチャ変更

**スキップしてよいケース**:
- 単一バグ修正（1-2ファイル変更）
- ドキュメント更新
- 小さなスタイル調整
- 設定ファイルの微調整

### 0.2 ユーザー確認

```javascript
AskUserQuestion({
  questions: [{
    question: "Worktreeを作成しますか？",
    header: "Worktree",
    options: [
      { label: "作成する", description: "feature/xxx ブランチで独立した開発環境を作成" },
      { label: "スキップ", description: "現在のブランチで直接作業（小規模変更向け）" }
    ],
    multiSelect: false
  }]
})
```

### 0.3 Worktree作成（選択時）

```javascript
// ブランチ名をユーザーに確認
AskUserQuestion({
  questions: [{
    question: "ブランチ名を入力してください（例: feature/user-auth）",
    header: "ブランチ名",
    options: [
      { label: "feature/{story-slug}", description: "ストーリー名からブランチを自動生成" },
      { label: "fix/{story-slug}", description: "バグ修正用ブランチ" }
    ],
    multiSelect: false
  }]
})

// Worktree作成
Bash({
  command: "git worktree add -b {branch-name} ../{branch-name}",
  description: "Worktreeを作成"
})
```

**作成後**:
- 新しいWorktreeディレクトリに移動して作業を継続
- ユーザーに新しいパスを通知

---

## Phase 1: ストーリー理解・slug確定

### 1.1 ストーリー取得

ユーザーからストーリーを聞き取る、または既存ファイルを読み込む。

```javascript
// USER_STORIES.md が存在すれば読み込み
Read({ file_path: "docs/USER_STORIES.md" })
```

### 1.2 ストーリー分析

```javascript
Task({
  description: "ストーリー分析",
  prompt: `ストーリーを分析し、以下を抽出してください:
- 目的・ゴール
- スコープ（対象範囲）
- 受入条件
- feature-slug候補（3つ）
- story-slug候補（3つ）

出力形式: JSON
`,
  subagent_type: "general-purpose",
  model: "opus"
})
```

→ 詳細: [agents/analyze-story.md](.claude/skills/dev/story-to-tasks/agents/analyze-story.md)

### 1.3 slug確定

AskUserQuestionでslug候補を提示し、ユーザーに選択してもらう:

```javascript
AskUserQuestion({
  questions: [
    {
      question: "feature-slugを選択してください",
      header: "Feature",
      options: [
        // analyze-story.mdの出力から動的に生成
        { label: "user-auth", description: "ユーザー認証機能" },
        { label: "dashboard", description: "ダッシュボード機能" },
        { label: "settings", description: "設定機能" }
      ],
      multiSelect: false
    },
    {
      question: "story-slugを選択してください",
      header: "Story",
      options: [
        // analyze-story.mdの出力から動的に生成
        { label: "login-form", description: "ログインフォーム実装" },
        { label: "validation", description: "バリデーション追加" },
        { label: "error-handling", description: "エラーハンドリング" }
      ],
      multiSelect: false
    }
  ]
})
```

**ポイント**:
- 既存のfeature-slugがあれば優先的に提示
- 「その他」で自由入力も可能

### 1.4 出力ディレクトリ作成

```bash
mkdir -p docs/features/{feature-slug}/stories/{story-slug}
```

### 1.5 story-analysis.json 保存

```javascript
Write({
  file_path: "docs/features/{feature-slug}/stories/{story-slug}/story-analysis.json",
  content: JSON.stringify(analysisResult, null, 2)
})
```

---

## Phase 2: タスク分解

```javascript
Task({
  description: "タスク分解",
  prompt: `story-analysis.jsonを読み込み、ストーリーを実装可能なタスクに分解してください。

各タスクには以下を含める:
- タスク名
- 説明
- 入出力（明確な場合）
- 依存関係

出力形式: JSON
`,
  subagent_type: "general-purpose",
  model: "sonnet"
})
```

→ 詳細: [agents/decompose-tasks.md](.claude/skills/dev/story-to-tasks/agents/decompose-tasks.md)

### 出力: task-list.json

```javascript
Write({
  file_path: "docs/features/{feature-slug}/stories/{story-slug}/task-list.json",
  content: JSON.stringify(taskList, null, 2)
})
```

---

## Phase 3: TDD/E2E/TASK分類

```javascript
Task({
  description: "TDD/E2E/TASK分類",
  prompt: `task-list.jsonを読み込み、各タスクをTDD/E2E/TASKに分類してください。

判定基準:
- TDD: 入出力が明確、アサーションで検証可能、ロジック層
- E2E: 視覚的確認が必要、UX判断、プレゼンテーション層
- TASK: テスト不要、UI検証不要、セットアップ/設定タスク

出力形式: Markdown（TODO.md形式）
`,
  subagent_type: "general-purpose",
  model: "haiku"
})
```

→ 詳細: [agents/assign-workflow.md](.claude/skills/dev/story-to-tasks/agents/assign-workflow.md)
→ 判定基準: [references/tdd-criteria.md](.claude/skills/dev/story-to-tasks/references/tdd-criteria.md) | [references/e2e-criteria.md](.claude/skills/dev/story-to-tasks/references/e2e-criteria.md) | [references/task-criteria.md](.claude/skills/dev/story-to-tasks/references/task-criteria.md)

### 出力: TODO.md

```markdown
# TODO

## フェーズ1: 環境セットアップ

### TASKタスク
- [ ] [TASK][EXEC] TypeScript環境構築
- [ ] [TASK][VERIFY] ビルド確認

## フェーズ2: ユーザー認証機能

### TDDタスク
- [ ] [TDD][RED] validateEmail のテスト作成
- [ ] [TDD][GREEN] validateEmail の実装
- [ ] [TDD][REFACTOR] リファクタリング

### E2Eタスク
- [ ] [E2E][IMPL] LoginForm UIコンポーネント
- [ ] [E2E][AUTO] agent-browser検証

### 共通
- [ ] [CHECK] lint/format/build
```

---

## Phase 4: ユーザー確認

```javascript
AskUserQuestion({
  questions: [{
    question: "タスクリストを確認してください。問題なければ実装を開始しますか？",
    header: "確認",
    options: [
      { label: "実装開始", description: "dev:developingで実装を開始" },
      { label: "修正が必要", description: "タスクを調整" }
    ],
    multiSelect: false
  }]
})
```

**「実装開始」を選択された場合**:
- dev:developingスキルを呼び出し

**「修正が必要」を選択された場合**:
- ユーザーの指示に従ってTODO.mdを修正
- 再度確認

---

## 完了条件

- [ ] story-analysis.jsonが生成された
- [ ] task-list.jsonが生成された
- [ ] TODO.mdが生成された
- [ ] 各タスクにTDD/E2E/TASKラベルが付与された
- [ ] ユーザーが承認した

## 関連スキル

- **dev:developing**: TDD/E2E/TASKタスクの実装
- **dev:feedback**: 実装後のフィードバック

## 参照ルール

実装時は `.claude/rules/workflow/workflow-branching.md` が自動適用される（TDD/E2E/TASK分岐判定）。
