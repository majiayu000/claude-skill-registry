---
name: Git Workflow with Conventional Commits
description: Automated Git workflow including staging, committing with Conventional Commits format, PR creation, and merging. Use when committing changes, creating PRs, or managing Git branches.
allowed-tools: Bash, Read, Grep, Glob
---

# 📝 Git Workflow with Conventional Commits

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐⭐⭐ (P0 Level)
**Purpose**: Conventional Commits準拠のGitワークフロー自動化

---

## 📋 概要

Conventional Commits仕様とMiyabiのPRガイドラインに従った
完全なGitワークフロー自動化を提供します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| コミット | "commit these changes" |
| PR作成 | "create a PR" |
| マージ | "merge this branch" |
| 機能完了後 | "after completing feature" |
| レビュー対応後 | "after review feedback" |

---

## 🔧 P1: Conventional Commits形式

### コミットメッセージ構造

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type一覧（優先順位順）

| Type | 用途 | 頻度 | 例 |
|------|------|------|-----|
| `feat` | 新機能 | 高 | `feat(auth): add OAuth2 login` |
| `fix` | バグ修正 | 高 | `fix(api): resolve null pointer` |
| `docs` | ドキュメント | 中 | `docs(readme): update install guide` |
| `refactor` | リファクタリング | 中 | `refactor(parser): simplify logic` |
| `test` | テスト | 中 | `test(unit): add auth tests` |
| `chore` | メンテナンス | 低 | `chore(deps): update tokio` |
| `style` | フォーマット | 低 | `style(lint): fix clippy warnings` |
| `perf` | パフォーマンス | 低 | `perf(db): add index` |
| `ci` | CI/CD | 低 | `ci(workflow): add clippy check` |
| `build` | ビルド | 低 | `build(cargo): update Cargo.lock` |
| `revert` | リバート | 稀 | `revert: feat(auth)` |

### Scope一覧

| Scope | 対象 |
|-------|------|
| `auth` | 認証・認可 |
| `api` | APIエンドポイント |
| `db` | データベース |
| `ui` | ユーザーインターフェース |
| `cli` | コマンドライン |
| `agent` | Agentシステム |
| `worktree` | Worktree管理 |
| `deps` | 依存関係 |

---

## 🚀 P2: ワークフロー別パターン

### Pattern 1: 標準コミット

```bash
# Step 1: 状態確認
git status && git diff --name-status

# Step 2: ステージング
git add <files>

# Step 3: コミット（HEREDOC必須）
git commit -m "$(cat <<'EOF'
feat(agent): add CodeGenAgent implementation

Implement CodeGenAgent for AI-driven code generation:
- Add BaseAgent trait implementation
- Support for Rust, TypeScript, Python
- Automatic test generation

Closes #270

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Step 4: プッシュ
git push -u origin feature/270-codegen-agent
```

### Pattern 2: PR作成

```bash
# GitHub CLI使用
gh pr create \
  --title "feat(agent): Issue #270 - Add CodeGenAgent" \
  --body "$(cat <<'EOF'
## Summary
Implements CodeGenAgent for AI-driven code generation.

## Changes
- ✅ Add `crates/miyabi-agents/src/codegen.rs`
- ✅ Implement BaseAgent trait
- ✅ Add unit tests (85% coverage)

## Test Plan
- [x] Unit tests pass
- [x] Clippy warnings resolved
- [x] Format check passed

## Related Issues
Closes #270

## Quality Report
- **Score**: 85/100 ✅
- **Coverage**: 85%

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" \
  --draft
```

### Pattern 3: マージ戦略

| 戦略 | コマンド | 用途 |
|------|---------|------|
| Squash（推奨） | `gh pr merge --squash --delete-branch` | 大半のPR |
| Merge | `gh pr merge --merge --delete-branch` | 大規模機能 |
| Rebase | `gh pr merge --rebase --delete-branch` | 単一コミットPR |

---

## ⚡ P3: ブランチ命名規則

### 形式

```
<type>/<issue-number>-<brief-description>
```

### 例

| Type | 例 |
|------|-----|
| feature | `feature/270-codegen-agent` |
| fix | `fix/271-worktree-race-condition` |
| docs | `docs/272-update-skills` |
| refactor | `refactor/273-cleanup-types` |
| test | `test/274-add-integration-tests` |
| chore | `chore/275-update-deps` |

---

## 📊 Worktree固有ワークフロー

### Worktree作成からマージまで

```bash
# Step 1: Worktree作成
git worktree add .worktrees/issue-270 -b feature/270-codegen-agent

# Step 2: Worktree内で作業
cd .worktrees/issue-270
# ... 変更 ...
git add .
git commit -m "feat(agent): add CodeGenAgent"

# Step 3: プッシュ
git push -u origin feature/270-codegen-agent

# Step 4: PR作成
gh pr create --title "feat(agent): Issue #270" --draft

# Step 5: クリーンアップ（マージ後）
cd ../..
git worktree remove .worktrees/issue-270
git push origin --delete feature/270-codegen-agent
git branch -d feature/270-codegen-agent
```

---

## 🛡️ エラーハンドリング

### Pre-commit Hook対応

```bash
# Hook変更確認
git status

# Hook変更をamend
git add .
git commit --amend --no-edit
git push --force-with-lease
```

### マージコンフリクト

```bash
# コンフリクト確認
git status
git diff

# 解決後
git add <resolved-files>
git merge --continue
# または
git rebase --continue
```

### 誤ったブランチへのコミット

```bash
# 最後のコミット取り消し（変更は保持）
git reset --soft HEAD~1

# 正しいブランチへ移動
git checkout correct-branch

# 再コミット
git add .
git commit -m "Your message"
```

### シークレットの誤コミット

```bash
# ファイルをコミットから削除
git rm --cached path/to/secret-file
git commit --amend --no-edit
git push --force-with-lease

# 古いコミットの場合: git-filter-repo使用
```

---

## ✅ チェックリスト

### コミット前

- [ ] テスト合格 (`cargo test`)
- [ ] Clippy警告なし (`cargo clippy`)
- [ ] フォーマット済み (`cargo fmt`)
- [ ] シークレットなし
- [ ] Conventional Commits準拠
- [ ] 変更がIssue要件に一致
- [ ] ドキュメント更新（必要時）

### PR作成前

- [ ] タイトルが規約に準拠
- [ ] 説明が完全
- [ ] CI合格
- [ ] コンフリクトなし
- [ ] レビュアー割り当て
- [ ] ラベル付与
- [ ] Issue紐付け (`Closes #XXX`)

---

## 🔗 関連ドキュメント

| ドキュメント | 用途 |
|-------------|------|
| `agents/specs/coding/pr-agent.md` | PRAgent仕様 |
| `docs/WORKTREE_PROTOCOL.md` | Worktreeプロトコル |
| `docs/LABEL_SYSTEM_GUIDE.md` | ラベルシステム |
| `.gitignore` | 除外ファイル |

---

## 📝 関連Skills

- **Agent Execution**: Worktree経由のブランチ作成
- **Rust Development**: コミット前テスト
- **Issue Analysis**: コミットtype/scope決定
