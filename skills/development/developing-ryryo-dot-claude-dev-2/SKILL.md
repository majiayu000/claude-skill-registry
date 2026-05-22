---
name: dev:developing
description: |
  TODO.mdのタスクを実行。TDD/E2E/TASKラベルに応じたワークフローで実装。
  Worktree内での独立した開発を支援。

  Trigger:
  dev:developing, /dev:developing, 実装, 開発, implementing, develop
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
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

## Phase 0: Worktree移動 & ブランチチェック

実装開始前に、作業環境を正しく設定する。

```
引数が指定されているか確認
    ├─ 引数あり（docs/features/...） → Worktree存在チェック
    │   ├─ Worktree存在 → 移動
    │   └─ Worktree不在 → カレントで継続（通常ありえない）
    └─ 引数なし → ブランチ確認
        ├─ master/main → Worktree作成を促す
        └─ feature/* 等 → そのまま続行
```

### 0.0 Worktree存在チェック・移動（引数指定時）

**引数が `docs/features/{feature-slug}/stories/{story-slug}` 形式の場合:**

```bash
# 1. Worktree一覧を取得
git worktree list

# 2. story-slugに対応するWorktreeを探す
# 例: docs/features/tarot-demo/stories/init-project
#  → .worktrees/feature-init-project を探す

# 3. 存在すれば移動
WORKTREE_DIR=$(git worktree list | grep "feature-{story-slug}" | awk '{print $1}')
if [ -n "$WORKTREE_DIR" ]; then
  cd "$WORKTREE_DIR"
  pwd  # 移動先を確認
  echo "Worktreeに移動しました: $WORKTREE_DIR"
else
  echo "対応するWorktreeが見つかりません。カレントディレクトリで継続します。"
fi
```

**重要**: 引数が指定された場合、まずこの手順を実行してからPhase 0.1以降に進む。

### 0.1 ブランチ確認

```bash
git branch --show-current
```

### 0.2 master/main の場合: Worktree作成

```javascript
AskUserQuestion({
  questions: [
    {
      question: "現在 master/main ブランチです。Worktreeを作成しますか？",
      header: "Worktree",
      options: [
        {
          label: "作成する（推奨）",
          description: "Worktree（別ディレクトリ）で独立した開発環境を作成",
        },
        {
          label: "このまま続行",
          description: "master/main で直接作業（非推奨）",
        },
      ],
      multiSelect: false,
    },
  ],
});
```

**「作成する」を選択された場合**:

```javascript
// Worktreeのブランチ名をユーザーに確認
AskUserQuestion({
  questions: [{
    question: "Worktreeのブランチ名を入力してください（例: feature/user-auth）",
    header: "Worktree名",
    options: [
      { label: "feature/{story-slug}", description: "ストーリー名から機能ブランチを作成" },
      { label: "fix/{story-slug}", description: "ストーリー名から修正ブランチを作成" }
    ],
    multiSelect: false
  }]
})

// Worktree作成
// 配置: .worktrees/{branch}（リポジトリ内）
// 例: .worktrees/feature-user-auth
Bash({
  command: `
BRANCH_NAME="{branch-name}"
WORKTREE_DIR=".worktrees/${BRANCH_NAME//\//-}"
mkdir -p .worktrees
git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR"
`,
  description: "Worktreeを作成"
})
```

**作成後**:

- エージェント自身が新しいWorktreeディレクトリに移動する
- 作業ディレクトリを変更してからタスクを継続

```bash
cd "$WORKTREE_DIR"
pwd  # 移動先を確認
```

---

## Phase 0.5: タスク登録

TODO.mdからタスクを読み込み、タスク管理システムに登録する。
これによりリアルタイムの進捗追跡が可能になる。

### 0.5.1 TODO.md読み込み

```javascript
Read({
  file_path: "docs/features/{feature-slug}/stories/{story-slug}/TODO.md",
});
```

### 0.5.2 タスク登録

未完了タスク（`- [ ]`）を抽出し、TaskCreateで登録:

```javascript
// 例: TODO.mdに以下のタスクがある場合
// - [ ] [TDD][RED] validateEmail テスト作成
// - [ ] [TDD][GREEN] validateEmail 実装

TaskCreate({
  subject: "[TDD][RED] validateEmail テスト作成",
  description: "validateEmail関数のテストを作成する",
  activeForm: "validateEmailテストを作成中...",
});

TaskCreate({
  subject: "[TDD][GREEN] validateEmail 実装",
  description: "validateEmail関数を実装する",
  activeForm: "validateEmailを実装中...",
});
```

### 0.5.3 依存関係の判断

依存関係はエージェントが文脈で判断する。必要に応じて:

```javascript
TaskUpdate({
  taskId: "2",
  addBlockedBy: ["1"], // GREENはREDの後
});
```

**注意**: 固定ルールは設けない。エージェントがタスク内容を見て判断。

### 0.5.4 現在の状態確認

```javascript
TaskList(); // 登録されたタスク一覧を確認
```

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

**シンプルに直接実行**（サブエージェント呼び出しなし）

```
1. タスクをin_progressに更新
2. 普通に実行（設定ファイル作成、コマンド実行など）
3. 検証（ファイル存在確認、ビルド確認など）
4. タスクをcompletedに更新 + TODO.md更新
5. コミット（/simple-add）
```

### TASKタスク実行手順

```javascript
// 1. 開始
TaskUpdate({ taskId: currentTaskId, status: "in_progress" });

// 2. 実行（エージェントが直接行う）
// - 設定ファイル作成/編集
// - コマンド実行
// - 必要な作業を完了

// 3. 検証（エージェントが直接確認）
// - ファイル存在確認
// - ビルド/コンパイル確認

// 4. 完了
TaskUpdate({ taskId: currentTaskId, status: "completed" });
// TODO.mdを更新（チェックマーク付与）

// 5. コミット
// /simple-add を使用、または手動でコミット
```

---

## TDDワークフロー

`[TDD]` ラベル付きタスクに適用。RED→GREEN→REFACTOR→SIMPLIFY→REVIEWサイクルを厳格に遵守。

```
[1/8] テスト作成（RED）
    → agents/tdd-write-test.md [sonnet]
    → テスト実行して失敗を確認
    → コミット（テストのみ）
        ↓
[2/8] 実装（GREEN）
    → agents/tdd-implement.md [sonnet]
    → テスト実行して成功を確認
    → ⚠️ テストは絶対に変更しない（仕様のブレ防止）
    → 通常2〜4周で収束
        ↓
[3/8] リファクタリング（REFACTOR）
    → agents/tdd-refactor.md [opus]
    → 構造的改善（単一責任、重複排除、複雑度低減）
    → テスト実行して成功を確認
        ↓
[4/8] コード整理（SIMPLIFY）
    → code-simplifierエージェント [opus]
    → 明瞭性・一貫性・保守性の向上
    → テスト実行して成功を確認
        ↓
[5/8] セルフレビュー（REVIEW）【過剰適合・抜け道チェック】
    → 「この実装、テストに過剰適合してない？抜け道ない？」
    → 過剰適合: テストケースだけに最適化されていないか
    → 抜け道: テストをすり抜ける不具合・エッジケースがないか
    → 問題あれば[2/8]に戻って修正
        ↓
[6/8] 品質チェック（CHECK）
    → lint/format/build
        ↓
[7/8] テスト資産の管理
    → テストコードの長期的価値を評価
    → 長期保持 or 簡素化/削除を判断
    → メンテナンスコスト最小化
        ↓
[8/8] コミット（COMMIT）
    → agents/simple-add-dev.md [haiku]
    → 実装とテスト資産管理の結果をコミット
    → 軽量・高速なサブエージェントで実行
```

→ 詳細: [references/tdd-flow.md]

### TDDタスク実行

```javascript
// [RED] テスト作成
// 開始時: ステータスをin_progressに更新
TaskUpdate({ taskId: currentTaskId, status: "in_progress" });

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
  model: "sonnet",
});
```

```javascript
// [GREEN] 実装（t_wada式TDD: YAGNI・Baby steps）
Task({
  description: "実装",
  prompt: `【YAGNI・Baby steps】今あるテストを通すためだけのコードを書いてください。

タスク: {task_name}

## 実装戦略（順に検討）

1. **仮実装（Fake It）**: まずハードコードで通す
   - 例: return "expected_value" でテストを通す
   - 最速でグリーンにする

2. **三角測量**: テストが2つ以上あれば一般化を検討
   - 複数のテストを通すために必要な最小の一般化のみ

3. **明白な実装**: 自明な場合のみ直接実装
   - 迷ったら仮実装から始める

## 禁止事項（YAGNI）

- ❌ テストを変更しない
- ❌ 将来必要「かもしれない」コードを書かない
- ❌ 今のテストに関係ない機能を追加しない
- ❌ 「ついでに」のリファクタリング（REFACTORフェーズで行う）

## 合言葉

「今のテストを通す → 次のテストを追加 → また通す」
このサイクルを小さく回す。`,
  subagent_type: "general-purpose",
  model: "sonnet",
});
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
  model: "opus",
});
```

```javascript
// [SIMPLIFY] コード整理
Task({
  description: "コード整理",
  prompt: `code-simplifierエージェントを使ってコードを整理してください。
対象: {task_name}

明瞭性・一貫性・保守性を向上させます。
リファクタリング完了後のコード整理として実行。

重要: テストが成功し続けることを確認`,
  subagent_type: "code-simplifier",
  model: "opus",
});
```

```javascript
// [REVIEW] セルフレビュー（過剰適合・抜け道チェック）
Task({
  description: "セルフレビュー",
  prompt: `実装をレビューしてください。
対象: {task_name}

実装ファイル: {implementation_file}
テストファイル: {test_file}

過剰適合・抜け道チェックを実施してください。`,
  subagent_type: "tdd-review",
  model: "opus",
});
```

```javascript
// [CHECK] 品質チェック
Task({
  description: "品質チェック",
  prompt: `品質チェック（lint/format/build）を実行してください。

結果を簡潔に報告してください。`,
  subagent_type: "quality-check",
  model: "haiku",
});

// 完了時: ステータスをcompletedに更新 + TODO.md更新
TaskUpdate({ taskId: currentTaskId, status: "completed" });
```

```javascript
// [MANAGE] テスト資産の管理
Task({
  description: "テスト資産の管理",
  prompt: `以下のテストファイルを評価してください。

対象テストファイル: {test_file}
実装ファイル: {implementation_file}

長期的価値を評価し、保持/簡素化/削除を判断してください。`,
  subagent_type: "test-asset-management",
  model: "sonnet",
});
```

```javascript
// [COMMIT] コミット
Task({
  description: "コミット",
  prompt: `変更をコミットしてください。
対象: {task_name}

変更内容:
- 実装コード
- リファクタリング結果
- コード整理結果
- テスト資産管理の結果

重要: simple-add-dev.mdで定義されているコミットメッセージフォーマットに従ってください：
- <emoji> <type>: <description>
- 変更点をリスト形式で記載。日本語。

simple-add-devエージェントを使用してコミットしてください。`,
  subagent_type: "simple-add-dev",
  model: "haiku",
});
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
[4/4] コミット（COMMIT）
    → agents/simple-add-dev.md [haiku]
    → 軽量・高速なサブエージェントで実行
    → <emoji> <type>: <description>
    → 変更点をリスト形式で記載。日本語。
```

→ 詳細: [references/e2e-flow.md]

### E2Eタスク実行

```javascript
// [IMPL] UI実装
// 開始時: ステータスをin_progressに更新
TaskUpdate({ taskId: currentTaskId, status: "in_progress" });

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
  model: "sonnet",
});
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
  model: "haiku",
});

// 完了時: ステータスをcompletedに更新 + TODO.md更新
TaskUpdate({ taskId: currentTaskId, status: "completed" });
```

```javascript
// [COMMIT] コミット
Task({
  description: "コミット",
  prompt: `変更をコミットしてください。
対象: {task_name}

変更内容:
- UIコンポーネント実装
- agent-browser検証結果

重要: simple-add-dev.mdで定義されているコミットメッセージフォーマットに従ってください：
- <emoji> <type>: <description>
- 変更点をリスト形式で記載。日本語。

simple-add-devエージェントを使用してコミットしてください。`,
  subagent_type: "simple-add-dev",
  model: "haiku",
});
```

---

## 共通サブエージェント

TDD/E2Eワークフローで使用するサブエージェント（TASKは直接実行のため不要）：

### test-runner (haiku)

- **用途**: テスト実行と結果報告
- **使用場面**: RED/GREEN/REFACTOR/SIMPLIFYの各ステップ
- **効果**: トークン消費を抑え、高速にテスト結果を取得

### quality-check (haiku)

- **用途**: lint/format/build実行
- **使用場面**: TDD/E2Eの品質チェックステップ
- **効果**: 自動修正と簡潔な報告で効率化

### test-asset-management (sonnet)

- **用途**: テスト資産の長期価値評価
- **使用場面**: TDDのMANAGEステップ
- **効果**: メンテナンスコスト最小化

### tdd-review (opus)

- **用途**: 過剰適合・抜け道チェック
- **使用場面**: TDDのREVIEWステップ
- **効果**: 高品質な実装を保証

### simple-add-dev (haiku)

- **用途**: Git commit自動化
- **使用場面**: TDD/E2EのCOMMITステップ（TASKは任意）
- **効果**: 軽量・高速なコミット処理

---

## TODO.md更新

タスク完了時にTODO.mdを更新:

```javascript
Edit({
  file_path: "docs/features/{feature-slug}/stories/{story-slug}/TODO.md",
  old_string: "- [ ] [TDD][GREEN] validateEmail の実装",
  new_string: "- [x] [TDD][GREEN] validateEmail の実装",
});
```

---

## フェーズ完了確認

```javascript
AskUserQuestion({
  questions: [
    {
      question: "フェーズが完了しました。次のフェーズに進みますか？",
      header: "フェーズ完了",
      options: [{ label: "承認", description: "次のフェーズに進む" }],
      multiSelect: false,
    },
  ],
});
```

---

## 完了条件

- [ ] すべてのTASKタスクが完了
- [ ] すべてのTDDタスクが完了（RED→GREEN→REFACTOR）
- [ ] すべてのE2Eタスクが完了（IMPL→AUTO）
- [ ] 全テストが成功
- [ ] 品質チェックが通過
- [ ] TODO.mdが全て完了マーク

## 関連スキル

- **dev:story**: タスクリスト生成（TDD/E2E/TASK分類）
- **dev:feedback**: 実装後のフィードバック

## 参照ルール

- TDD/E2E/TASK分岐: `.claude/rules/workflow/workflow-branching.md`
- TDDワークフロー: `.claude/rules/workflow/tdd-workflow.md`
- E2Eサイクル: `.claude/rules/workflow/e2e-cycle.md`
