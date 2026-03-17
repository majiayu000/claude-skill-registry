---
name: Creating Atomic PRs
description: Create small, focused Pull Requests by splitting implementations into atomic steps. Prevents direct work on main/master branches and enforces safe Git workflows. Use when the user asks to commit changes, create PRs, or mentions git operations. Keywords: commit, PR, pull request, git, branch, main, master, コミット, プルリクエスト.
---

# Creating Atomic PRs

このSkillは、mainブランチでの直接作業を防止し、小さく分割された「アトミック」なPRを作成するための包括的なワークフローを提供します。

## 概要

**問題**:
- mainブランチのままブランチを切らずに`git add .`で一括コミット
- PRが大きすぎてレビューが困難
- 機能全体を1つのPRにまとめてしまう

**解決策**:
- ブランチ保護（main/master/developでの作業を防止）
- PR分割提案（AIが小さなステップに分割）
- 段階的なコミット・PR作成

## いつ使うか

このSkillは以下の場合に自動的に発動します：
- ユーザーが「コミットして」「PRを作成して」と依頼した時
- `git commit`、`git add`、`git push`を実行しようとした時
- ブランチ管理、PR作成に関する質問があった時

## ワークフロー

### Phase 0: Branch Protection Check ⚠️

**最初に必ず実行**：現在のブランチをチェック

```bash
git branch --show-current
```

**判定**：
- `main`、`master`、`develop`の場合
  → **即座に処理を中断**
  → featureブランチ作成を促す（Phase 2へ）

- featureブランチの場合
  → Phase 1へ進む

**重要**: この保護チェックをスキップしてはいけません。

---

### Phase 1: PR Planning - 分割戦略の立案 📋

**目的**: 実装を小さなステップに分割し、レビュー可能なPRを計画する

#### 1-1. ユーザーに実装内容をヒアリング

以下を確認：
- どんな機能を実装するのか
- どのファイルを変更するのか
- 既存の機能への影響はあるか

#### 1-2. AI による分割案の提案

**プロンプト例**：
```
「既存のコードを壊さないように、小さなステップでPRを分けて実装したい。
この機能を段階的に実装するための最適な分割案を提案してください。」
```

**分割の原則**（重要）：
- ✅ 1つの機能を完結させるのではなく、「その機能を実現するための1つのパーツ」レベルで分割
- ✅ レビューが超簡単になるくらい小さく
- ✅ 既存のコードを壊さない安全な変更から始める

#### 1-3. 分割案の例

**良い分割の例**：
```markdown
## 機能: ユーザー認証システム追加

### ステップ1（PR#1）
- ドメインオブジェクト（User型）に認証項目を追加するだけ
- 変更ファイル: `types/user.ts`
- リスク: 低（既存機能に影響なし）

### ステップ2（PR#2）
- 新しい認証プロバイダを作成するだけ
- 変更ファイル: `providers/auth-provider.ts`
- リスク: 低（誰も使っていない）

### ステップ3（PR#3）
- 認証UIコンポーネントを作成
- 変更ファイル: `components/Login.tsx`
- リスク: 中（既存機能と統合）

### ステップ4（PR#4）
- 既存のルーティングと統合
- 変更ファイル: `routes.ts`, `App.tsx`
- リスク: 中（既存フローに影響）
```

**悪い分割の例**：
```markdown
❌ ステップ1: ユーザー認証システム全体を実装
- 変更ファイル: 10個以上
- リスク: 高（レビューが困難）
```

#### 1-4. ユーザーと分割案を確認

提案した分割案をユーザーに提示し、調整：
- 各ステップの内容が明確か
- 依存関係は正しいか
- 優先順位は適切か

---

### Phase 2: Branch Creation 🌿

**前提**: Phase 0で保護ブランチを検出した場合、またはPR分割の各ステップで新しいブランチを作成

#### 2-1. ブランチ命名規則の確認

**フォーマット**：
```
(feature|bugfix|hotfix)/<ticket-id>-<description>
```

**例**：
```bash
feature/TASK-123-add-user-domain
feature/TASK-123-add-auth-provider
bugfix/BUG-456-fix-login-error
hotfix/HOTFIX-789-security-patch
```

#### 2-2. ブランチ作成

```bash
# ベースブランチから作成
git checkout main
git pull origin main
git checkout -b feature/TASK-123-add-user-domain
```

#### 2-3. 作成確認

```bash
git branch --show-current
# => feature/TASK-123-add-user-domain
```

---

### Phase 3: Implementation & Staging 📝

**前提**: Phase 1で計画したステップに従って実装

#### 3-1. 実装作業

現在のステップ（例: ステップ1）の内容だけを実装：
- ドメインオブジェクトに項目追加
- **他のステップには手を出さない**

#### 3-2. 変更ファイルの確認

```bash
git status
```

#### 3-3. ファイルの分類と個別ステージング

**重要**: `git add -A` は絶対に使用しない

変更ファイルを以下のカテゴリに分類：
1. **機能実装**: ビジネスロジック、コンポーネント
2. **テスト**: テストファイル
3. **ドキュメント**: README、コメント

**個別にステージング**：
```bash
# 機能実装
git add src/types/user.ts

# テスト
git add tests/user.test.ts

# ドキュメント
git add docs/user-model.md
```

---

### Phase 4: Commit 💾

**前提**: Phase 3でステージングが完了

#### 4-1. Conventional Commits に基づくprefix選択

| Prefix | 用途 | 例 |
|--------|------|-----|
| `feat:` | 新機能追加 | `feat: add User domain model` |
| `fix:` | バグ修正 | `fix: resolve login error` |
| `add:` | ファイル・パッケージ追加 | `add: install auth library` |
| `test:` | テスト追加・修正 | `test: add user model tests` |
| `docs:` | ドキュメント変更 | `docs: update auth README` |
| `refactor:` | リファクタリング | `refactor: simplify auth logic` |
| `style:` | コードスタイル変更 | `style: format auth files` |
| `chore:` | その他の変更 | `chore: update dependencies` |

#### 4-2. コミットメッセージ生成

**フォーマット**：
```
<prefix>: <subject>

<body>

Co-Authored-By: Claude <noreply@anthropic.com>
```

**例**：
```bash
git commit -m "feat: add authentication fields to User domain model

Added email, passwordHash, and role fields to support authentication.
This is the first step in implementing the user authentication system.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Phase 5: PR Creation 🚀

**前提**: Phase 4でコミットが完了

#### 5-1. リモートにpush

```bash
git push -u origin feature/TASK-123-add-user-domain
```

#### 5-2. PR description生成

**フォーマット**：
```markdown
## Summary
このPRは[機能名]の実装における[ステップ番号]です。

## このPRでやること
- [変更内容1]
- [変更内容2]

## このPRでやらないこと（意図的に分割）
- [次のステップでやること1]
- [次のステップでやること2]

## なぜ小さく分割したか
- [理由1: 既存コードへの影響を最小化]
- [理由2: レビュー負荷を軽減]
- [理由3: リスクの高い変更を別PRで慎重に扱う]

## 次のステップ
- [ ] PR#[次のPR番号]: [次のステップの内容]

## Test plan
- [ ] [テスト項目1]
- [ ] [テスト項目2]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

#### 5-3. PRの作成

```bash
gh pr create --title "feat: add User domain model (Step 1/4)" --body "$(cat <<'EOF'
## Summary
このPRはユーザー認証システムの実装におけるステップ1です。

## このPRでやること
- User型に認証フィールド（email、passwordHash、role）を追加

## このPRでやらないこと（意図的に分割）
- 認証プロバイダの実装（Step 2）
- 認証UIの実装（Step 3）
- 既存ルーティングとの統合（Step 4）

## なぜ小さく分割したか
- 既存のUser型を使用しているコードへの影響を最小化
- 型定義だけなので安全で、レビューが超簡単
- 次のステップで認証プロバイダを安全に実装できる基盤を作る

## 次のステップ
- [ ] PR#2: 認証プロバイダの作成
- [ ] PR#3: 認証UIコンポーネントの作成
- [ ] PR#4: 既存ルーティングとの統合

## Test plan
- [ ] TypeScriptのコンパイルが通ることを確認
- [ ] 既存のUserを使用しているテストが通ることを確認

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## 既存Skillとの連携

### `enforcing-git-commit-workflow` との連携
- コミットメッセージのフォーマット
- 個別ファイルステージングのルール

### `executing-ai-development-workflow` との連携
- PR作成後のレビューフロー
- 多層レビューの実施

### `git-workflow` コマンドとの違い
- `git-workflow`: 包括的なGitワークフロー全体を管理
- `creating-atomic-prs`: PR分割とブランチ保護に特化

---

## トラブルシューティング

### Q: Phase 0で保護ブランチを検出したのに、そのまま作業を続けてしまう

**A**: 以下を必ず実行してください：
1. `git stash` で変更を一時退避
2. Phase 2でfeatureブランチを作成
3. `git stash pop` で変更を復元
4. Phase 3から作業を再開

### Q: PR分割案が提示されない

**A**: Phase 1-2で明示的にAIに相談してください：
```
「この実装を、既存のコードを壊さないように、
小さなステップでPRを分けて実装したいです。
どのように分割すればよいか提案してください。」
```

### Q: 1つのPRにすべての変更を含めたい

**A**: このSkillの目的は「小さく分割」することです。
以下の場合のみ、分割せずに1つのPRで進めることを検討：
- 変更が極めて小さい（1-2ファイル、10行以内）
- 緊急のhotfix
- 分割すると機能が壊れる（非常に稀）

---

## ベストプラクティス

### ✅ DO
- Phase 0のブランチチェックを**必ず**実行
- PR分割案をAIに相談し、レビュー負荷を最小化
- 各PRに「なぜ小さく分割したか」の理由を明記
- `git add`は個別ファイルのみ

### ❌ DON'T
- main/master/developブランチで直接作業
- `git add -A` や `git add .` を使用
- 機能全体を1つのPRにまとめる
- レビュワーに「でかい」「リスキー」なPRを送る

---

## まとめ

このSkillを使用することで：
- ✅ mainブランチでの事故を防止
- ✅ レビュワーの負担を大幅に軽減
- ✅ PRのマージ速度が向上
- ✅ 安全で段階的な機能追加が可能

**思い出してください**:
「PRは1つの機能を完結させるレベルではなく、その機能を実現するための1つのパーツレベルで分割」
