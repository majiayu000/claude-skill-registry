---
name: translator
description: Translate code comments, documentation, and UI strings between multiple languages. Use when internationalizing applications or translating technical documentation.
---

# Translator Skill

技術文書やコードコメントを多言語翻訳するスキルです。

## 概要

プログラミング文脈を理解した高精度な翻訳を提供します。技術用語、変数名、コードブロックを適切に保持します。

## 主な機能

- **技術文書翻訳**: README、ドキュメント、API仕様
- **コードコメント翻訳**: インラインコメント、JSDoc、Docstring
- **UI/UX テキスト**: ボタン、ラベル、エラーメッセージ
- **技術用語保持**: 専門用語は原語維持または注釈付き
- **コードブロック保護**: コード部分は翻訳しない
- **一貫性維持**: 用語集による統一翻訳
- **多言語対応**: 50以上の言語

## サポート言語

- 日本語 ↔ 英語
- 中国語（簡体字・繁体字）
- 韓国語
- スペイン語、フランス語、ドイツ語
- その他50以上の言語

## 使用方法

### 基本的な翻訳

```
以下のREADMEを日本語に翻訳：
[英語のREADME]

注意:
- コードブロックは保持
- 技術用語は適切に処理
```

### コードコメント翻訳

```
このファイルのコメントを英語に翻訳：
[日本語コメント付きコード]

要件:
- コードは変更しない
- コメントのみ翻訳
- JSDoc形式を維持
```

### UI テキスト

```
以下のUIテキストを5言語に翻訳：
言語: 英語、日本語、中国語、韓国語、スペイン語

元テキスト:
- "Sign Up"
- "Password must be at least 8 characters"
- "Email already exists"
```

## 翻訳例

### README翻訳

**英語 → 日本語**:

```markdown
# Project Name

A powerful tool for developers.

## Installation

```bash
npm install project-name
```

## Features

- Fast performance
- Easy to use
- Well documented
```

↓

```markdown
# プロジェクト名

開発者のための強力なツールです。

## インストール

```bash
npm install project-name
```

## 機能

- 高速なパフォーマンス
- 使いやすさ
- 充実したドキュメント
```

### コードコメント翻訳

**日本語 → 英語**:

```javascript
/**
 * ユーザーを作成する
 * @param {string} email - メールアドレス
 * @param {string} password - パスワード（8文字以上）
 * @returns {User} 作成されたユーザー
 * @throws {ValidationError} 入力値が不正な場合
 */
function createUser(email, password) {
  // メールアドレスの形式をチェック
  if (!isValidEmail(email)) {
    throw new ValidationError('無効なメールアドレスです');
  }

  // パスワードの長さをチェック
  if (password.length < 8) {
    throw new ValidationError('パスワードは8文字以上必要です');
  }

  // ユーザーをデータベースに保存
  return db.users.create({ email, password });
}
```

↓

```javascript
/**
 * Create a user
 * @param {string} email - Email address
 * @param {string} password - Password (minimum 8 characters)
 * @returns {User} Created user
 * @throws {ValidationError} If input is invalid
 */
function createUser(email, password) {
  // Check email format
  if (!isValidEmail(email)) {
    throw new ValidationError('Invalid email address');
  }

  // Check password length
  if (password.length < 8) {
    throw new ValidationError('Password must be at least 8 characters');
  }

  // Save user to database
  return db.users.create({ email, password });
}
```

### UI テキスト多言語化

```json
{
  "en": {
    "signup": "Sign Up",
    "login": "Log In",
    "password_error": "Password must be at least 8 characters",
    "email_exists": "Email already exists"
  },
  "ja": {
    "signup": "サインアップ",
    "login": "ログイン",
    "password_error": "パスワードは8文字以上である必要があります",
    "email_exists": "このメールアドレスは既に登録されています"
  },
  "zh": {
    "signup": "注册",
    "login": "登录",
    "password_error": "密码必须至少8个字符",
    "email_exists": "电子邮件已存在"
  },
  "ko": {
    "signup": "가입하기",
    "login": "로그인",
    "password_error": "비밀번호는 최소 8자 이상이어야 합니다",
    "email_exists": "이메일이 이미 존재합니다"
  }
}
```

## 技術用語の扱い

### 保持する用語

- API, HTTP, REST, GraphQL
- JSON, XML, YAML
- Git, GitHub, commit, pull request
- Docker, Kubernetes
- React, Vue, Angular

### 翻訳する用語

- function → 関数
- variable → 変数
- array → 配列
- object → オブジェクト

### 両方を併記

```
配列 (array)
オブジェクト (object)
非同期 (asynchronous)
```

## ベストプラクティス

1. **コンテキスト提供**: 翻訳対象の用途を明記
2. **用語集活用**: プロジェクト固有用語を統一
3. **レビュー**: ネイティブスピーカーによる確認
4. **段階的翻訳**: README → コメント → UI の順

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
このREADMEを英語から日本語に翻訳：
- コードブロックは保持
- 技術用語は適切に処理（必要に応じて併記）
- Markdown形式を維持

[英語のREADME内容]
```

高品質な翻訳が生成されます！
