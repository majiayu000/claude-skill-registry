---
name: commit-message-generator
description: Generate conventional commit messages following best practices. Use when creating structured git commit messages.
---

# Commit Message Generator Skill

高品質なGitコミットメッセージを生成するスキルです。

## 概要

Conventional Commits形式で、明確で一貫性のあるコミットメッセージを自動生成します。

## 主な機能

- **Conventional Commits**: 標準形式
- **自動分類**: feat、fix、docs等
- **詳細説明**: 変更内容の説明
- **Breaking Changes**: 互換性のない変更
- **Issue参照**: 自動リンク

## 使用方法

```
以下の変更内容からコミットメッセージを生成：
- ユーザー認証機能を追加
- JWT トークンを実装
- パスワードハッシュ化
```

## フォーマット

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type（必須）

- **feat**: 新機能
- **fix**: バグ修正
- **docs**: ドキュメント
- **style**: コードスタイル（フォーマット等）
- **refactor**: リファクタリング
- **perf**: パフォーマンス改善
- **test**: テスト追加・修正
- **chore**: ビルド、ツール等
- **ci**: CI設定
- **build**: ビルドシステム
- **revert**: 変更の取り消し

### Scope（任意）

変更の範囲（コンポーネント名、モジュール名等）

## 生成例

### 新機能

```
feat(auth): add JWT authentication

Implement JWT-based authentication system with the following features:
- Token generation and validation
- Refresh token mechanism
- Password hashing with bcrypt

Closes #123
```

### バグ修正

```
fix(api): resolve CORS issues in production

Fixed CORS configuration to allow requests from production domain.
Added proper headers and origin validation.

Fixes #456
```

### Breaking Change

```
feat(api)!: change user API response format

BREAKING CHANGE: User API now returns JSON instead of XML.
Migration guide available in docs/migration.md

Before:
```xml
<user>
  <name>John</name>
</user>
```

After:
```json
{
  "user": {
    "name": "John"
  }
}
```

Closes #789
```

### 複数変更

```
feat(users): implement user profile features

- Add profile picture upload
- Add bio and social links fields
- Implement profile visibility settings
- Add email notification preferences

Related to #234, #235
```

### リファクタリング

```
refactor(database): optimize query performance

Refactored user queries to use eager loading instead of N+1 queries.
Reduced database calls from 101 to 2 per request.

Performance improvement: ~90% faster response time
```

### ドキュメント

```
docs(api): update authentication documentation

- Add JWT token usage examples
- Document refresh token flow
- Add error response codes
- Include cURL examples
```

### テスト

```
test(auth): add unit tests for JWT validation

Added comprehensive test coverage for:
- Token generation
- Token validation
- Expired token handling
- Invalid token handling

Coverage: 95%
```

## ベストプラクティス

### 良いコミットメッセージ

```
feat(search): add fuzzy search algorithm

Implemented fuzzy matching for product search using Levenshtein distance.
Users can now find products even with typos.

Closes #567
```

**特徴**:
- 明確なタイプとスコープ
- 簡潔な件名（50文字以内）
- 詳細な本文（なぜ変更したか）
- Issue参照

### 避けるべき例

```
❌ update files
❌ fix bug
❌ WIP
❌ changes
❌ asdf
```

## 自動生成フロー

```bash
# 変更内容を分析
git diff --cached

# AIがコミットメッセージを生成
# 1. 変更ファイルを確認
# 2. 変更タイプを判定（feat/fix/etc）
# 3. スコープを推定
# 4. 変更内容を要約
# 5. Conventional Commits形式で生成
```

## Git Hook統合

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash

# Staged changesから自動生成
DIFF=$(git diff --cached)

# Claude/AIに送信してメッセージ生成
MESSAGE=$(claude-generate-commit-message "$DIFF")

# コミットメッセージファイルに書き込み
echo "$MESSAGE" > "$1"
```

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
以下の変更からコミットメッセージを生成：

変更ファイル:
- src/auth/jwt.ts (新規)
- src/middleware/auth.ts (新規)
- package.json (jwt依存追加)

変更内容:
- JWT認証を実装
- 認証ミドルウェアを追加
```

**生成されるメッセージ**:
```
feat(auth): implement JWT authentication

Add JWT-based authentication with the following:
- Token generation and validation (jwt.ts)
- Authentication middleware (auth.ts)
- jsonwebtoken dependency

Provides secure stateless authentication for API endpoints.
```
