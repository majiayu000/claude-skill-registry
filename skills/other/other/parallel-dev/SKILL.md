---
name: parallel-dev
description: 残issueを分析し、PR単位でエージェントチームを並列起動する。各PRにarchitect→実装→レビューのパイプラインを自動適用。
user-invocable: true
argument-hint: "[issue番号をカンマ区切り | all] (デフォルト: all = Phase1残issueを自動検出)"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, SendMessage, TeamCreate, TaskCreate, TaskUpdate, TaskList, TaskGet, TaskOutput, AskUserQuestion, WebFetch
---

# 並列開発ワークフロースキル

issueをPR単位に分割し、エージェントチームで並列開発を実行する。

## 処理フロー

### Phase 0: 残issue分析（自動 or 指定）

引数が `all` または未指定の場合：
1. `gh issue list --state open` でOpenなissueを取得
2. `後回し/本審査対応` ラベルのissueを除外
3. Phase 1に必要なissueを優先度でソート
4. ユーザーにPR分割案を提示し、承認を得る

引数がissue番号の場合：
1. 指定されたissueの内容を取得
2. PR分割案を生成

### Phase 1: 環境準備

各PRごとに：
1. **git worktree作成**
   ```bash
   git worktree add ~/.claude-worktrees/inspirehub-mobile/<branch-name> -b <branch-name> main
   ```
2. **ブランチ命名**: `fix/issue-<番号>-<概要>` or `feat/issue-<番号>-<概要>`

### Phase 2: チーム作成 + タスク登録

1. `TeamCreate` でチームを作成（チーム名: `sprint-<日付>`）
2. 各PRをタスクとして登録（`TaskCreate`）
3. 依存関係があればblocks/blockedByを設定

### Phase 3: パイプライン起動（並列）

各PRに対して `task-planner` エージェントをspawn。
各task-plannerは以下のサブエージェントパイプラインを**順番に**実行する：

```
┌─────────────────────────────────────────────────────────────────┐
│ PR パイプライン（task-planner が管理）                             │
│                                                                 │
│  Step 1: architect（設計・調査）                                   │
│    └→ 設計判断・変更方針の決定                                      │
│                                                                 │
│  Step 2: kotlin-dev / ios-dev（実装）                              │
│    └→ shared層修正: kotlin-dev                                    │
│    └→ iOS UI修正: ios-dev                                        │
│    └→ 実装後にコミット                                             │
│                                                                 │
│  Step 3: design-reviewer（UI変更がある場合のみ）                     │
│    └→ HIG準拠・画面設計書との一致確認                                │
│    └→ 指摘があればStep 2に戻る                                     │
│                                                                 │
│  Step 4: code-reviewer（コードレビュー）                            │
│    └→ git diff main でレビュー                                    │
│    └→ KMP境界チェック                                             │
│    └→ 指摘があればStep 2に戻る                                     │
│                                                                 │
│  Step 5: qa-checker（ビルド確認）                                  │
│    └→ shared層テスト                                              │
│    └→ iOSビルド                                                  │
│    └→ Androidビルド                                              │
│    └→ ビルドエラーがあればStep 2に戻る                               │
│                                                                 │
│  Step 6: 完了報告 → team-leadに通知                                │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 4: PR作成

全パイプライン完了後：
1. 各worktreeのブランチをpush
2. `gh pr create` でPR作成
3. PR URLをユーザーに報告
4. Xcodeでworktreeを開くコマンドを表示：
   ```bash
   open ~/.claude-worktrees/inspirehub-mobile/<branch-name>/iosApp/iosApp.xcodeproj
   ```

### Phase 5: クリーンアップ

1. チームをシャットダウン（`SendMessage` type: shutdown_request）
2. `TeamDelete` でチームを削除
3. worktreeは残す（ユーザーが動作確認するため）

## サブエージェントへのpromptテンプレート

### architect

```
あなたは {PR名} の設計担当だ。
作業ディレクトリ: {worktree_path}
タスク: {設計タスクの詳細}
以下のファイルを読んで分析せよ：{対象ファイルリスト}
設計判断と変更方針を報告せよ。コードは書くな。
```

### kotlin-dev

```
あなたは {PR名} のKotlin実装担当だ。
作業ディレクトリ: {worktree_path}
ブランチ: {branch_name}
タスク: {実装タスクの詳細}
architectの設計方針: {architect_output}
KMPルール（.claude/rules/kotlin-kmp.md）に従え。
実装後、worktree内でコミットせよ。
```

### ios-dev

```
あなたは {PR名} のiOS実装担当だ。
作業ディレクトリ: {worktree_path}
ブランチ: {branch_name}
タスク: {実装タスクの詳細}
architectの設計方針: {architect_output}
iOSルール（.claude/rules/ios-swift.md）に従え。
実装後、worktree内でコミットせよ。
```

### design-reviewer

```
{worktree_path} のiOS UI変更をレビューせよ。
確認項目:
1. 画面設計書（docs/design/画面設計_ネイティブアプリ.md）との一致
2. SwiftUIデザインガイド準拠
3. iOS HIG準拠
4. アクセシビリティ対応
指摘事項をリスト形式で報告せよ。
```

### code-reviewer

```
{worktree_path} のコード変更をレビューせよ。
`git diff main` で差分を確認。
確認項目:
1. KMP境界の整合性（shared ↔ iOS）
2. 非推奨API使用チェック
3. セキュリティ（OWASP Top 10）
4. エラーハンドリング
指摘事項をリスト形式で報告せよ。
```

### qa-checker

```
{worktree_path} でビルド確認を実行せよ。
1. cd {worktree_path} && ./gradlew :shared:testDebugUnitTest
2. cd {worktree_path} && ./gradlew :composeApp:assembleDebug
3. cd {worktree_path}/iosApp && xcodebuild -project iosApp.xcodeproj -scheme iosApp -configuration Debug -destination 'generic/platform=iOS Simulator' -quiet
結果を報告せよ。
```

## コンフリクト防止ルール

- 各PRは独立したworktreeで作業する
- 同じファイルを複数PRで変更する場合はユーザーに確認
- shared層の変更がiOS層に影響する場合、shared側が先にマージされてからUI側を開始

## 出力フォーマット

```markdown
## 並列開発レポート

### チーム構成
- チーム名: {team_name}
- PR数: {pr_count}

### PR一覧
| PR | issue | ブランチ | ステータス | パイプライン進捗 |
|----|-------|---------|-----------|----------------|

### 各PRの詳細
#### PR-A: {タイトル}
- architect: {結果サマリ}
- 実装: {結果サマリ}
- design-review: {結果サマリ}
- code-review: {結果サマリ}
- build: {結果サマリ}

### 動作確認コマンド
{各worktreeのXcodeプロジェクトを開くコマンド}
```
