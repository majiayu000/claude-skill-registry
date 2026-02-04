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

## エージェント委譲ルール

**⚠️ 各ステップの実行は必ずTaskエージェントに委譲する。自分で実装・テスト・レビューしない。**

呼び出しパターン（全ステップ共通）:
```
agentContent = Read(".claude/skills/dev/developing/agents/{agent}.md")
Task({ prompt: agentContent + 追加コンテキスト, subagent_type: {type}, model: {指定モデル} })
```

## ワークフロー別ステップ・委譲先

### TDDワークフロー（[TDD]ラベル）

| Step | agent | model | type | 備考 |
|------|-------|-------|------|------|
| 1 RED | tdd-write-test.md | sonnet | general-purpose | テストのみ作成。テスト失敗を確認 |
| 1b COMMIT | simple-add-dev.md | haiku | simple-add | テストのみ先行コミット |
| 2 GREEN | tdd-implement.md | sonnet | general-purpose | テスト固定。通常2-4周で収束 |
| 3 REFACTOR | tdd-refactor.md | opus | general-purpose | 機能追加なし、品質改善のみ |
| 4 SIMPLIFY | (code-simplifier) | opus | code-simplifier | 明瞭性・一貫性・保守性向上 |
| 5 REVIEW | tdd-review.md | opus | general-purpose | 過剰適合・抜け道チェック。問題→Step 2へ |
| 6 CHECK | quality-check.md | haiku | general-purpose | lint/format/build |
| 7 MANAGE | test-asset-management.md | sonnet | general-purpose | テスト保持/簡素化/削除判断 |
| 8 COMMIT | simple-add-dev.md | haiku | simple-add | 実装+テスト資産管理結果をコミット |

→ 詳細: [references/tdd-flow.md]

### E2Eワークフロー（[E2E]ラベル）

| Step | agent | model | type | 備考 |
|------|-------|-------|------|------|
| 1 IMPL | e2e-implement.md | sonnet | general-purpose | UIコンポーネント実装 |
| 2 AUTO | e2e-verify.md | haiku | general-purpose | agent-browser検証。問題→Step 1へ |
| 3 CHECK | quality-check.md | haiku | general-purpose | lint/format/build |
| 4 COMMIT | simple-add-dev.md | haiku | simple-add | コミット |

→ 詳細: [references/e2e-flow.md]

### TASKワークフロー（[TASK]ラベル）

**サブエージェント呼び出しなし。エージェントが直接実行。**

```
1. TaskUpdate(in_progress)
2. 実行（設定ファイル作成、コマンド実行など）
3. 検証（ファイル存在確認、ビルド確認など）
4. TaskUpdate(completed) + TODO.md更新（- [ ] → - [x]）
5. /simple-add でコミット
```

→ 詳細: [references/task-flow.md]

---

## ★ 実行手順（必ずこの順序で実行）

### Phase 1: Worktree移動 & ブランチチェック

1. 引数が `docs/features/{feature-slug}/stories/{story-slug}` 形式 → `git worktree list` で対応Worktreeを探し移動
2. 引数なし → `git branch --show-current` でブランチ確認
3. master/main → **AskUserQuestion** でWorktree作成を確認。作成する場合は `.worktrees/{branch}` に配置

**ゲート**: 作業ディレクトリが確定しなければ次に進まない。

### Phase 2: タスク登録

1. TODO.mdを読み込み、未完了タスク（`- [ ]`）を **TaskCreate** で登録
2. 依存関係があれば **TaskUpdate(addBlockedBy)** で設定
3. **TaskList** で登録確認

**ゲート**: タスクが登録されなければ次に進まない。

### Phase 3: タスク実行（ラベル別ワークフロー）

1. **実行順序**: TASKタスクを最初に実行（環境構築が必要なため）
2. 各タスクのラベルに応じて上記ワークフローを適用
3. 各タスク完了時に **TaskUpdate(completed)** + TODO.md更新（`- [ ]` → `- [x]`）

**ゲート**: 全タスクが完了しなければ次に進まない。

---

## 完了条件

- [ ] すべてのTASKタスクが完了
- [ ] すべてのTDDタスクが完了（RED→GREEN→REFACTOR→SIMPLIFY→REVIEW→CHECK→MANAGE→COMMIT）
- [ ] すべてのE2Eタスクが完了（IMPL→AUTO→CHECK→COMMIT）
- [ ] 全テストが成功
- [ ] 品質チェックが通過
- [ ] TODO.mdが全て完了マーク

## 参照

- agents/: tdd-write-test.md, tdd-implement.md, tdd-refactor.md, tdd-review.md, e2e-implement.md, e2e-verify.md, quality-check.md, simple-add-dev.md, task-execute.md, test-asset-management.md, test-runner.md
- references/: tdd-flow.md, e2e-flow.md, task-flow.md, test-conventions.md
- rules/: workflow/tdd-workflow.md, workflow/e2e-cycle.md, workflow/workflow-branching.md
