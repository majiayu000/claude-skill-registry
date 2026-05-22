---
name: auth
description: "Implements authentication and payment features using Clerk, Supabase Auth, or Stripe. Use when user mentions ログイン, 認証, auth, authentication, Clerk, Supabase, 決済, payment, Stripe, 課金, サブスクリプション. Do NOT load for: 一般的なUI作成, データベース設計, 非認証機能."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
metadata:
  skillport:
    category: auth
    tags: [auth, authentication, payments, clerk, supabase, stripe]
    alwaysApply: false
---

# Auth Skills

認証と決済機能の実装を担当するスキル群です。

## 含まれる小スキル

| スキル | 用途 |
|--------|------|
| auth-impl | Clerk/Supabase Auth による認証実装 |
| payments | Stripe による決済実装 |

## ルーティング

- 認証機能: auth-impl/doc.md
- 決済機能: payments/doc.md

## 実行手順

1. **品質判定ゲート**（Step 0）
2. ユーザーのリクエストを分類(認証 or 決済)
3. 適切な小スキルの doc.md を読む
4. その内容に従って実装

### Step 0: 品質判定ゲート（セキュリティチェックリスト）

認証・決済機能は常にセキュリティリスクが高いため、作業開始前に必ず以下を表示:

```markdown
🔐 セキュリティチェックリスト

この作業はセキュリティ上重要です。以下を確認してください：

### 認証関連
- [ ] パスワードはハッシュ化（bcrypt/argon2）
- [ ] セッション管理は安全か（HTTPOnly Cookie）
- [ ] CSRF 対策は実装されているか
- [ ] レート制限（ブルートフォース対策）

### 決済関連
- [ ] 機密情報（カード番号等）をサーバーに保存しない
- [ ] Stripe/決済プロバイダの SDK を正しく使用
- [ ] Webhook の署名検証
- [ ] 金額改ざん防止（サーバー側で金額を確定）

### 共通
- [ ] エラーメッセージが詳細すぎないか（情報漏洩防止）
- [ ] ログに機密情報を出力していないか
```

### セキュリティ重要度表示

```markdown
⚠️ 注意レベル: 🔴 高

この機能は以下のリスクがあります：
- 認証情報の漏洩
- 不正アクセス
- 決済の不正操作

専門家によるレビューを推奨します。
```

### VibeCoder 向け

```markdown
🔐 安全にログイン・決済機能を作るために

1. **パスワードは「ハッシュ化」する**
   - 元のパスワードを復元できない形で保存
   - 万が一データが漏れても安全

2. **カード情報はサーバーに保存しない**
   - Stripe などの専用サービスに任せる
   - 自分のサーバーには一切保存しない

3. **エラーメッセージは曖昧に**
   - 「パスワードが違います」ではなく「認証に失敗しました」
   - 悪意ある人にヒントを与えない
```
