---
name: reviewing-security
description: >
  OWASP Top 10ベースのセキュリティレビューと脆弱性検出。
  セキュリティ問題のコードレビュー、脆弱性分析、または
  security, OWASP, XSS, SQL injection, セキュリティ, 脆弱性,
  cloud security, AWS, IAM, Terraform, クラウドセキュリティ, インフラ に言及した時に使用。
allowed-tools: [Read, Grep, Glob, Task]
agent: security-reviewer
context: fork
user-invocable: false
---

# セキュリティレビュー

## 検出 (OWASP Top 10)

| ID  | カテゴリ             | パターン                               | 修正                                 |
| --- | -------------------- | -------------------------------------- | ------------------------------------ |
| A01 | アクセス制御不備     | 認証欠如、IDOR、パストラバーサル       | 認証ミドルウェア、所有権チェック     |
| A02 | 暗号化の失敗         | `password: 'plaintext'`                | bcrypt/argon2ハッシュ                |
| A03 | インジェクション     | `db.query(\`SELECT...${id}\`)`         | パラメータ化クエリ、ORM              |
| A03 | インジェクション     | `exec(\`ping ${host}\`)`               | 入力検証、ライブラリ使用             |
| A03 | XSS                  | `dangerouslySetInnerHTML={{ __html }}` | デフォルトエスケープ、DOMPurify      |
| A05 | セキュリティ設定ミス | `cors({ origin: '*' })`                | 明示的オリジン許可リスト             |
| A05 | セキュリティ設定ミス | `cookie: {}` (オプションなし)          | secure, httpOnly, sameSite: 'strict' |
| A09 | ログ記録の失敗       | `logger.info({ password })`            | 機密フィールド除外                   |
| A10 | SSRF                 | `fetch(userInputUrl)`                  | URL検証、許可リスト                  |

## 信頼度閾値

信頼度 >80% の場合のみ報告。含める: file:line、悪用シナリオ、修正推奨。

## 参照

| トピック         | スコープ         | ファイル                             |
| ---------------- | ---------------- | ------------------------------------ |
| 基本             | A01, A02, A07    | `references/owasp-basic.md`          |
| インジェクション | A03              | `references/owasp-injection.md`      |
| 上級             | A04-A06, A08-A10 | `references/owasp-advanced.md`       |
| クラウド         | IAM, IaC, CI/CD  | `references/cloud-infrastructure.md` |
