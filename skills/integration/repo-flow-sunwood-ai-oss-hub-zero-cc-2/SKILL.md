---
name: repo-flow
description: |
  Git Flow ワークフローで開発からdevelopへのマージまでを実行。
  「フィーチャーブランチ作って」「PR出して」「コードレビューして」「マージして」などのリクエスト時に使用。
  開発中の差分がある状態からブランチを作成します。
  develop → main のリリースフローもサポート。
  ※ develop → main のマージは人間が実行します。
allowed-tools: Bash, Glob, Grep, Read, Write
user-invocable: true
---

# Repo Flow

Git Flow ワークフローでフィーチャーブランチの作成からdevelopへのマージまでを支援します。

**※ develop → main のマージは人間が実行します。このスキルではmainへマージしません。**

**前提: 開発で差分がある状態から開始します**

**重要: ユーザーからの明示的な指示がない場合は、ワークフローを最後（developへのマージとクリーンアップ）まで自動的に実行してください。各ステップ間でユーザーに確認を求めず、一気通貫で実行してください。**

## ワークフロー

### Step 1: 現状確認（差分チェック）

```bash
git status
git diff --stat
git branch --show-current
```

- カレントブランチの確認
- 未コミット変更の有無と内容
- 変更されたファイル一覧

### Step 2: フィーチャーブランチ作成（差分を含めて）

**重要: 開発中の差分がある状態でブランチを作成します**

```bash
# 現在のブランチを確認
git branch --show-current

# develop からブランチ作成（差分は新しいブランチに引き継がれる）
git checkout develop 2>/dev/null || git checkout main
git pull

# 変更を一時退避（必要な場合）
git stash push -m "WIP: <description>"

# フィーチャーブランチ作成
git checkout -b feature/<name>

# 変更を戻す（一時退避していた場合）
git stash pop
```

**ブランチ名の決定:**
```
feature/<description>

例:
feature/repo-create-refs
feature/add-auth-system
feature/fix-login-bug
```

### Step 3: 差分をコミット

**現在の差分を確認:**
```bash
git status
git diff
```

**重要: 差分は巻き戻しやすいように細かくコミットする**
- ファイル単位、機能単位で小さく分けてコミット
- 1コミットにつき1つの変更を原則とする

**コミットメッセージ形式:**
```
<emoji> <type>: <subject>

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**タイプと対応する絵文字:**
| タイプ | 絵文字 | 説明 |
|:------|:------|:------|
| `feat` | ✨ | 新機能 |
| `fix` | 🐛 | バグ修正 |
| `docs` | 📚 | ドキュメント |
| `style` | 💄 | フォーマット |
| `refactor` | ♻️ | リファクタリング |
| `test` | 🧪 | テスト |
| `chore` | 🔧 | その他 |
| `perf` | ⚡ | パフォーマンス |
| `ci` | 🤖 | CI/CD |

**コミット例:**
```bash
# 細かく分けてコミット
git add path/to/auth.py
git commit -m "✨ feat(auth): add JWT authentication module

- Implement JWT-based authentication
- Add token generation and validation

Co-Authored-By: Claude <noreply@anthropic.com>"

git add path/to/login.py
git commit -m "✨ feat(auth): add login endpoint

- Add /login POST endpoint
- Include password hashing with bcrypt

Co-Authored-By: Claude <noreply@anthropic.com>"

git add path/to/logout.py
git commit -m "✨ feat(auth): add logout endpoint

- Add /logout POST endpoint
- Invalidate session tokens

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 4: プッシュ

```bash
git push -u origin feature/<name>
```

### Step 5: プルリクエスト作成

**ビルド/テストの実行:**
プロジェクトにビルドコマンドやテストコマンドが存在する場合は、PR作成前に実行する

```bash
# ビルド（存在する場合）
npm run build     # Node.js
mvn compile       # Maven
gradle build      # Gradle
cargo build       # Rust
go build          # Go

# テスト（存在する場合）
npm test          # Node.js
mvn test          # Maven
gradle test       # Gradle
cargo test        # Rust
go test ./...     # Go

# 結果を保存（エビデンスとしてPRに添付）
npm run build > build.log 2>&1
npm test > test.log 2>&1
```

**タイトル形式:**
```
<emoji> <type>(<scope>): <subject>

例:
✨ feat(repo-create): add comprehensive reference templates
🐛 fix(auth): resolve JWT token expiration issue
📚 docs(readme): update installation instructions
```

**PR 作成:**
```bash
# develop に対してPRを作成
gh pr create --base develop \
  --title "✨ feat(scope): description" \
  --body "PR body here"
```

**PR ボディテンプレート:**

詳細なテンプレートは `references/PULL_REQUEST.md` を参照

```bash
# テンプレートを表示
cat .claude/skills/repo-flow/references/PULL_REQUEST.md
```

**主なセクション:**
- Summary
- Changes
- Test plan
- Build & Test Results（ビルド結果、テスト結果、実行エビデンス）
- Multifaceted Analysis（技術的観点、運用観点、ユーザー観点）

### Step 6: コードレビュー対応

**gemini-code-assist などのレビュー確認:**
```bash
# レビューコメントを確認
gh pr view <number> --json comments

# gemini-code-assist のレビューを抽出
gh api repos/:owner/:repo/pulls/:number/comments --jq '.[] | select(.user.login == "gemini-code-assist[bot]")'
```

**修正コミット:**
```bash
# 修正をコミット（同じブランチにプッシュ）
git add <files>
git commit -m "🐛 fix: resolve review feedback

- Address comment about XXX
- Fix issue YYY pointed out in review

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

### Step 7: develop へのマージ

**Git Flow の正しい順序:**
```
feature → develop → (人が確認して) → main
```

```bash
# develop に切り替え
git checkout develop
git pull

# feature ブランチをマージ
git merge feature/<name> --no-ff
git push origin develop
```

### Step 8: クリーンアップ

```bash
# ローカルブランチ削除
git branch -d feature/<name>

# リモートブランチ削除
git push origin --delete feature/<name>

# リモートの追跡ブランチをクリーンアップ
git fetch --prune
```

## ブランチ構造

```
main           ← 本番環境（リリース時のみ更新）
  ↑
develop        ← 開発統合ブランチ
  ↑
feature/*      ← フィーチャーブランチ（各機能開発）
```

## 開発ワークフロー図

```
1. 開発（ファイル修正）
   ↓
2. feature/<name> ブランチ作成
   ↓ (差分を引き継ぐ)
3. コミット & プッシュ
   ↓
4. PR 作成 (feature → develop)
   ↓
5. レビュー & 修正
   ↓
6. develop にマージ
   ↓ (リリース時)
7. main にマージ (人間が実行)
   ↓
8. ブランチ削除
```

## クイックリファレンス

### コマンド一覧

| 操作 | コマンド |
|:--|:--|
| 差分確認 | `git status`, `git diff` |
| ブランチ作成 | `git checkout -b feature/<name>` |
| 一時退避 | `git stash push -m "message"` |
| 復元 | `git stash pop` |
| コミット | `git add . && git commit` |
| プッシュ | `git push -u origin feature/<name>` |
| PR 作成 | `gh pr create --base develop` |
| develop へマージ | `git merge feature/<name> --no-ff` |
| ブランチ削除 | `git branch -d feature/<name>` |

### develop が存在しない場合

```bash
# main から develop を作成
git checkout main
git pull
git checkout -b develop
git push -u origin develop
```

## ベストプラクティス

✅ **やるべきこと:**
- develop から feature ブランチを作成
- Conventional Commits 形式 + 絵文字でコミット
- **変更はファイル単位・機能単位で細かくコミット**（巻き戻しやすくするため）
- PR ボディに詳細な説明を記載
- **PR には多角的分析を含める**
- **ビルド/テストを実行し、エビデンスをPRに記載**
- PR は develop に対して作成
- コードレビューを受けてから develop にマージ
- **develop → main のマージは人間が実行**
- マージ済みブランチは削除

❌ **やるべきでないこと:**
- feature ブランチを直接 main にマージ
- リモートの main に直接プッシュ
- **develop → main のマージを自動化しない（人間が確認の上実行）**
- `git push --force` を使用（緊急時のみ）
- **大量の変更を1つのコミットにまとめる**

## 使用例

```bash
# 開発中の差分から最後まで一気に実行
/repo-flow フィーチャーブランチ作って
↓
1. 差分を確認します
2. ブランチ名を決定します
3. feature/<name> を作成して差分を移動
4. **ビルド/テストを実行**（プロジェクトに応じて）
5. 変更を**ファイル単位・機能単位で細かくコミット**（絵文字付き）
6. プッシュ
7. develop への PR を作成（多角的分析、ビルド/テスト結果を記載）
8. develop にマージ
9. ブランチをクリーンアップ

# ユーザーが明示的にステップを指定した場合は、そのステップのみ実行
/repo-flow PRだけ出して
↓
- プッシュ & PR 作成のみ実行（既にコミット済みの場合）

/repo-flow マージだけして
↓
- develop へのマージのみ実行

# main へのマージは人間が実行
# ↓
# リリース時、人間が develop → main をマージ
```

## コミット例（細かく分ける場合）

```bash
# 悪い例: 全部1つのコミット
git add .
git commit -m "✨ feat: add authentication system"

# 良い例: 細かく分ける
git add src/auth/jwt.py
git commit -m "✨ feat(auth): add JWT module

Co-Authored-By: Claude <noreply@anthropic.com>"

git add src/auth/login.py
git commit -m "✨ feat(auth): add login endpoint

Co-Authored-By: Claude <noreply@anthropic.com>"

git add src/auth/logout.py
git commit -m "✨ feat(auth): add logout endpoint

Co-Authored-By: Claude <noreply@anthropic.com>"

git add tests/auth_test.py
git commit -m "🧪 test(auth): add authentication tests

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## 関連スキル

| スキル | 用途 |
|:------|:------|
| **repo-maintain** | リリース、変更履歴、Issue |
| **repo-create** | 新規リポジトリ作成 |
