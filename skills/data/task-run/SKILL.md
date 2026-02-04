---
user-invocable: true
description: "[タスク] 3. Issue実行 + 進捗同期"
---

# [タスク] 3. Issue実行 + 進捗同期

## 入力: $ARGUMENTS
- Issue番号（例: `#123` または `123`）
- 省略時: 実行可能なIssue（依存解決済み）を一覧表示して選択

---

## 🎯 目的
- 指定されたIssue（または選択したIssue）に従って実装を行う
- **組み込みTask** と **GitHub Issue** の進捗を同期する
- 完了時に両方を更新（Task: completed、Issue: close）

---

## 共通前提（参照）
- 実装規約・口調・TDD・Docコメント等は `CLAUDE.md` に従う
- `doc/input/rdd.md` を読み、該当する `.claude/skills/*` を適用
- 詳細運用は `doc/guide/ai_guidelines.md` を参照

---

## 実行手順

### 1. Issue選択（引数省略時）
```
📋 実行可能なIssue（依存解決済み）

┌────┬─────────────────────┬──────────┬─────────────┬─────────────┐
│ #  │ Title               │ Issue    │ Task Status │ blockedBy   │
├────┼─────────────────────┼──────────┼─────────────┼─────────────┤
│ 1  │ API設計             │ #126     │ pending     │ なし ✅     │
│ 2  │ ユーザー認証実装     │ #123     │ pending     │ なし ✅     │
│ -  │ ログイン画面作成     │ #124     │ pending     │ #123 ⏳     │
└────┴─────────────────────┴──────────┴─────────────┴─────────────┘

→ どのIssueを実行する？ [番号を入力]
```

### 2. プレチェック
```bash
# Issue内容を取得して確認
gh issue view {ISSUE_NUMBER}
```
- `ready-for-dev` ラベルがあるか
- RDD参照セクションの存在
- 変更要求がある場合は **承認済み** か確認
- 組み込みTaskの blockedBy が空か確認

### 2.5. 作業ブランチ作成（通常 or worktree）

**通常モード（単一タスク）:**
```bash
git checkout -b task/{ISSUE_NUMBER}-{short-description}
```

**並行モード（git worktree）:**
複数タスクを同時に進める場合は worktree を使用:
```bash
# 親ディレクトリにworktreeを作成
git worktree add ../$(basename $(pwd))-task-{ISSUE_NUMBER} -b task/{ISSUE_NUMBER}-{short-description}

# worktreeに移動して作業
cd ../$(basename $(pwd))-task-{ISSUE_NUMBER}
```

> **Tips**: 別ターミナルで別のClaude Codeセッションを起動し、異なるworktreeで並行作業が可能。
> 完了後は `git worktree remove ../project-task-{ISSUE_NUMBER}` で削除。

### 3. 着手（組み込みTask + Issue同期）

**組み込みTask更新:**
```
TaskUpdate:
  taskId: "{task-id}"  # metadata.issueNumber で特定
  status: "in_progress"
```

**Issueコメント（⚠️ 確認あり）:**
```bash
gh issue comment {ISSUE_NUMBER} --body "🚀 着手開始

## 実行計画
- [ ] {ステップ1}
- [ ] {ステップ2}
- [ ] {ステップ3}
"
```

### 4. 実装（TDD厳守）
- `CLAUDE.md` の規約に従い、RED → GREEN → REFACTOR で段階的に進める
- 要件をToDoに分解（最小ステップ）
- 既存パターン再利用と重複回避を最優先

### 5. 検証
```bash
pnpm lint --fix && pnpm type-check
pnpm test
```
- 失敗時の切り分け（最小サンプル運用等）は `CLAUDE.md` の方針に従う

**UI変更がある場合（Agent Browser利用可能時）:**
```bash
# 開発サーバーを起動後、Agent Browserでページを確認
agent-browser open http://localhost:3000/{対象パス}
agent-browser snapshot -i  # 要素一覧を取得
# 必要に応じてインタラクション確認
agent-browser click @{ref}
agent-browser fill @{ref} "テスト入力"
```
- 表示崩れ、状態遷移、レスポンシブを目視確認
- 問題発見時は修正後に再スナップショット

### 6. 進捗報告（適宜）
```bash
gh issue comment {ISSUE_NUMBER} --body "📝 進捗報告

## 完了
- [x] {完了したステップ}

## 次のステップ
- [ ] {残りのステップ}

## メモ
{気づいた点や注意点}
"
```

### 7. コミット + PR作成

**コミット（⚠️ 確認あり）:**
```bash
git add -A
git commit -m "feat: {変更概要} (#${ISSUE_NUMBER})

- {主要変更1}
- {主要変更2}

Refs #${ISSUE_NUMBER}"
```

**リモートにプッシュ:**
```bash
git push -u origin task/{ISSUE_NUMBER}-{short-description}
```

**PR作成（⚠️ 確認あり）:**
```bash
gh pr create \
  --title "feat: {変更概要}" \
  --body "## 概要
{このPRで何を実現するか}

## 変更内容
- {主要変更1}
- {主要変更2}

## RDD整合
- **準拠**: OK（根拠: doc/input/rdd.md §...）
- **変更要求**: 無し / 有（承認済み）

## 検証結果
- [x] lint/type-check PASS
- [x] test PASS

## テスト手順
1. {確認手順1}
2. {確認手順2}

Closes #${ISSUE_NUMBER}" \
  --base main
```

> **Note**: `Closes #${ISSUE_NUMBER}` により、PRマージ時にIssueが自動closeされるにゃ。

### 8. 完了（組み込みTask更新）

**組み込みTask更新:**
```
TaskUpdate:
  taskId: "{task-id}"
  status: "completed"
```

**完了報告:**
```
✅ TASK-{ISSUE_NUMBER} 完了

- PR: #{PR_NUMBER}
- マージ後に Issue #{ISSUE_NUMBER} が自動close
```

---

## 失敗時のガイド

### RDD違反
```bash
gh issue comment {ISSUE_NUMBER} --body "⚠️ RDD違反検出

## 内容
{違反内容}

## 変更要求(ADR-lite)
{変更提案}

## ステータス
承認待ち（ユーザー確認後に再開）
"
```

### 制約で実現不能
```bash
gh issue comment {ISSUE_NUMBER} --body "🚫 実現不能

## 理由
{制約の内容}

## 代替案
1. {代替案1}: {影響}
2. {代替案2}: {影響}

## ロールバック方法
{戻し方}
"
```

---

## 品質チェックリスト
- [ ] RDD準拠（スタック/制約に一致）
- [ ] Docコメント（JSDoc/Docstring）が全関数・クラスにある
- [ ] 重複コードを作らず既存パターンを再利用
- [ ] コメントで**ドメイン意図**と**決定理由**を明記
- [ ] 検証ゲート（lint/type/test）がPASS
- [ ] 必要なら最小サンプルで検証済み（削除可注記）
- [ ] 技術的負債が記録され、次スプリントに回されている
- [ ] **コミットメッセージに Issue番号を含めている**
- [ ] **PRを作成し、`Closes #Issue番号` を本文に含めている**
- [ ] **組み込みTask が completed に更新済み**

---

## 自己評価
- **成功自信度**: (1-10)
- **一言理由**: {短く理由を記載}
