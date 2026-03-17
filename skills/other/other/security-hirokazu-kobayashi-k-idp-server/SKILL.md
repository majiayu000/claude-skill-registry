---
name: security
description: セキュリティ・脆弱性対策の開発・テストを行う際に使用。OAuth/OIDC攻撃対策、認証識別子切り替え攻撃、Session Fixation、マルチテナント分離、セキュリティテスト実装時に役立つ。
---

# セキュリティ・脆弱性対策ガイド

## ドキュメント

- `e2e/src/tests/security/README.md` - セキュリティテスト詳細
- `documentation/docs/content_11_learning/06-security/` - セキュリティ学習リソース

---

## 対策済み脆弱性一覧

| 脆弱性 | CWE | 重大度 | 対策 |
|--------|-----|--------|------|
| 認証識別子切り替え攻撃 | CWE-287 | Critical | DB検索優先化 |
| Redirect URI切り替え攻撃 | CWE-601 | Critical | 完全一致検証 |
| Session Fixation | CWE-384 | High | 認証後Session再生成 |
| 認可コード再利用 | CWE-294 | High | 使用後即時削除 |
| マルチテナント分離違反 | CWE-284 | Critical | Tenant第一引数パターン |
| SSRF | CWE-918 | High | プライベートIP/メタデータブロック |
| パスワードブルートフォース | CWE-307 | High | Redisカウンター（INCR+TTL） |

---

## 認証識別子切り替え攻撃（CWE-287）

### 攻撃シナリオ

```
1. 被害者のメールアドレスAで認証開始
2. チャレンジ送信後、攻撃者メールアドレスBに変更
3. Bの検証コードで認証
4. 【脆弱】: メールアドレスAとしてログイン ❌
5. 【正常】: メールアドレスBとしてログイン ✅
```

### 対策コード

`EmailAuthenticationInteractor.java:257-306`:

```java
private User resolveUser(
    Tenant tenant,
    AuthenticationTransaction transaction,
    String email,
    String providerId,
    UserQueryRepository userQueryRepository) {

  // === 1st factor user identification ===

  // 1. Database search FIRST (Issue #800 fix)
  User existingUser = userQueryRepository.findByEmail(tenant, email, providerId);
  if (existingUser.exists()) {
    log.debug("User found in database. email={}, sub={}", email, existingUser.sub());
    return existingUser;
  }

  // 2. Reuse transaction user if same identity (Challenge resend scenario)
  if (transaction.hasUser()) {
    User transactionUser = transaction.user();
    if (email.equals(transactionUser.email())) {
      return transactionUser; // Same identity -> reuse
    }
    // Different identity -> create new user (identifier switching)
  }

  // 3. New user creation...
}
```

### セキュリティテスト

```
e2e/src/tests/security/identifier_switching_attack.test.js
```

---

## Redirect URI切り替え攻撃（CWE-601）

### 攻撃シナリオ

| 攻撃パターン | 説明 | 対策 |
|-------------|------|------|
| Token Endpoint不一致 | 認可時と異なるredirect_uriでトークン取得 | 完全一致検証 |
| 未登録URI | 登録されていないredirect_uriを使用 | 登録URI必須 |
| 部分一致攻撃 | `example.com/callback.evil.com` | 厳密一致（substring禁止） |
| URIエンコーディング | `%2e%2e/` でパストラバーサル | 正規化後検証 |

### RFC 6749 準拠検証

```java
// redirect_uri検証（RFC 6749 Section 4.1.3）
// "values MUST be identical"

// NG: 部分一致
if (registeredUri.startsWith(requestUri)) // ❌

// OK: 完全一致
if (registeredUri.equals(requestUri)) // ✅
```

### セキュリティテスト

```
e2e/src/tests/security/redirect_uri_switching_attack.test.js
```

**テストケース（21件）**:
- Token Endpoint redirect_uri検証
- 未登録URI拒否
- 部分一致攻撃防止
- HTTP/HTTPS スキーム違い検証
- ポート省略/明示検証
- クエリパラメータ追加検証
- 認可コード再利用防止

---

## Session Fixation（CWE-384）

### 攻撃シナリオ

```
1. 攻撃者がSession IDを取得
2. 被害者に固定Session IDでアクセスさせる
3. 被害者が認証完了
4. 【脆弱】: 攻撃者が同じSession IDで被害者としてアクセス ❌
5. 【正常】: 認証後にSession ID再生成 ✅
```

### 対策

認証成功後にセッションを再生成し、旧セッションIDを無効化。

### セキュリティテスト

```
e2e/src/tests/security/session_fixation_password_auth.test.js
```

---

## 認可コード再利用攻撃（CWE-294）

### RFC 6749 Section 10.5

> "The authorization server MUST ensure that authorization codes cannot be used more than once."

### 対策コード

`AuthorizationCodeGrantService.java:131-134, 202`:

```java
// 存在確認
if (!authorizationCodeGrant.exists()) {
  throw new TokenBadRequestException("invalid_grant", "not found authorization code.");
}

// ... トークン発行処理 ...

// 使用後は即時削除（再利用防止）
authorizationCodeGrantRepository.delete(tenant, authorizationCodeGrant);
```

---

## マルチテナント分離（CWE-284）

### 設計原則

```java
// ✅ 全Repository操作でTenant第一引数
public interface UserRepository {
    User find(Tenant tenant, UserId userId);
    void register(Tenant tenant, User user);
}

// ❌ Tenant指定なし（テナント間データ漏洩リスク）
public interface UserRepository {
    User find(UserId userId);  // 危険
}
```

### Row-Level Security（PostgreSQL）

```sql
-- RLSポリシーでテナント分離を強制
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

### セキュリティテスト

```
e2e/src/tests/security/multi_tenant_isolation.test.js
```

---

## SSRF保護（CWE-918）

### ブロック対象（16種）

`PrivateIpRange.java`:

| 種別 | IPレンジ | 説明 |
|------|---------|------|
| **IPv4 Loopback** | 127.0.0.0/8 | ループバック |
| **RFC1918 Private** | 10.0.0.0/8 | プライベート（Class A） |
| **RFC1918 Private** | 172.16.0.0/12 | プライベート（Class B） |
| **RFC1918 Private** | 192.168.0.0/16 | プライベート（Class C） |
| **Cloud Metadata** | 169.254.169.254/32 | AWS/GCP/Azure メタデータ |
| **Link-Local IPv4** | 169.254.0.0/16 | リンクローカル |
| **CGNAT** | 100.64.0.0/10 | Carrier-Grade NAT (RFC6598) |
| **Documentation** | 192.0.2.0/24 | TEST-NET-1 |
| **Documentation** | 198.51.100.0/24 | TEST-NET-2 |
| **Documentation** | 203.0.113.0/24 | TEST-NET-3 |
| **Broadcast** | 255.255.255.255/32 | ブロードキャスト |
| **Current Network** | 0.0.0.0/8 | 現在のネットワーク |
| **IPv6 Loopback** | ::1/128 | IPv6ループバック |
| **IPv6 Link-Local** | fe80::/10 | IPv6リンクローカル |
| **IPv6 ULA** | fc00::/7 | IPv6ユニークローカル |
| **IPv4-mapped IPv6** | ::ffff:0:0/96 | IPv4マップドIPv6 |

### 対策コード

`SsrfProtectionValidator.java:261-274`:

```java
private void validateIpAddress(String host, InetAddress address) {
  String ipString = address.getHostAddress();

  for (PrivateIpRange range : blockedRanges) {
    if (range.contains(address)) {
      throw new SsrfProtectionException(
          String.format(
              "Blocked: Host '%s' resolves to private/reserved IP %s (%s)",
              host, ipString, range.description()),
          host,
          ipString,
          range);
    }
  }
}
```

詳細は `/system-configuration` スキル参照。

---

## ユーザーステータス検証

### 無効ユーザーの認可防止

```
e2e/src/tests/security/invalid_user_status_authorization.test.js
```

---

## セキュリティテスト実行

### 全セキュリティテスト

```bash
cd e2e
npm test -- security/
```

### 個別実行

```bash
# 認証識別子切り替え
npm test -- security/identifier_switching_attack.test.js

# Redirect URI攻撃
npm test -- security/redirect_uri_switching_attack.test.js

# Session Fixation
npm test -- security/session_fixation_password_auth.test.js

# マルチテナント分離
npm test -- security/multi_tenant_isolation.test.js
```

---

## セキュリティテスト作成パターン

```javascript
describe("Security: [攻撃名]", () => {
  it("Should prevent [攻撃シナリオ]", async () => {
    // 1. 攻撃準備
    const victim = createVictimUser();
    const attacker = createAttackerUser();

    // 2. 攻撃実行
    const result = await executeAttack(victim, attacker);

    // 3. 脆弱性検証
    if (result.authenticatedAs === victim) {
      fail("CRITICAL: Attack succeeded - vulnerability exists");
    }

    // 4. 正常動作確認
    expect(result.authenticatedAs).toBe(attacker);
  });
});
```

---

## OWASP参照

| OWASP | 対策 |
|-------|------|
| A01 Broken Access Control | Tenant分離、認可検証 |
| A02 Cryptographic Failures | JWT署名検証、TLS必須 |
| A03 Injection | パラメータバインディング |
| A04 Insecure Design | 認証フロー設計レビュー |
| A05 Security Misconfiguration | SSRF保護、デフォルト拒否 |
| A07 Identification Failures | 識別子切り替え対策 |

---

## 関連スキル

| スキル | 用途 |
|--------|------|
| `/system-configuration` | SSRF保護、Trusted Proxies |
| `/security-events` | セキュリティイベント通知 |
| `/session-management` | セッション管理 |
| `/authentication` | 認証実装 |
| `/e2e-testing` | テスト実行方法 |
