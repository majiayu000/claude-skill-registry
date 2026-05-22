---
name: ios-security
description: "iOSアプリのセキュリティレビュー。OWASP Mobile Top 10、App Transport Security、Keychain使用をチェック。Use when: セキュリティ、脆弱性、認証、Keychain、ATS を依頼された時。"
---

# iOS セキュリティレビュー

## OWASP Mobile Top 10 チェック項目

| ID | リスク | チェック内容 |
|----|-------|-------------|
| M1 | Improper Platform Usage | Info.plist の ATS設定、権限の最小化 |
| M2 | Insecure Data Storage | Keychain使用、UserDefaults に機密情報なし |
| M3 | Insecure Communication | HTTPS強制、証明書ピンニング |
| M4 | Insecure Authentication | BiometricなしのKeychain保護、Token管理 |

## Swift セキュリティパターン

### 機密情報の保存
- [ ] パスワード・トークンはKeychainに保存
- [ ] UserDefaultsに機密情報を保存していない
- [ ] ハードコードされたAPIキー・シークレットがない

### 通信セキュリティ
- [ ] Info.plistでATSが無効化されていない
- [ ] URLSessionでカスタム証明書検証を適切に実装
- [ ] デバッグ用のログに機密情報を出力していない

### コード検査パターン
```bash
# ハードコード検索
grep -rn "password\|secret\|apiKey\|api_key" Sources/

# print/NSLogの確認（本番では削除推奨）
grep -rn "print(\|NSLog(" Sources/
```