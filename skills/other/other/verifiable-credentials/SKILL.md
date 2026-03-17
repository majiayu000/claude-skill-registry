---
name: verifiable-credentials
description: Verifiable Credentials（VC）機能の開発・修正を行う際に使用。OID4VCI準拠のCredential発行、Deferred発行、Batch発行実装時に役立つ。
---

# Verifiable Credentials 開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/03-application-plane/` - アプリケーション実装ガイド

---

## 機能概要

Verifiable Credentials（VC）は、デジタル証明書の発行・検証を行う機能。
- **OID4VCI準拠**: OpenID for Verifiable Credential Issuance
- **Credential発行**: 即時発行、Deferred（遅延）発行
- **Batch発行**: 複数Credentialの一括発行
- **フォーマット**: jwt_vc_json, ldp_vc 等

---

## モジュール構成

```
libs/
├── idp-server-core-extension-verifiable-credentials/   # VC拡張モジュール
│   └── .../core/extension/verifiable_credentials/
│       ├── handler/
│       │   ├── CredentialHandler.java              # Credential発行処理
│       │   ├── CredentialRequestErrorHandler.java
│       │   └── io/
│       │       ├── CredentialRequest.java
│       │       ├── CredentialResponse.java
│       │       ├── CredentialRequestStatus.java
│       │       ├── DeferredCredentialRequest.java
│       │       ├── DeferredCredentialResponse.java
│       │       ├── BatchCredentialRequest.java
│       │       └── BatchCredentialResponse.java
│       ├── verifier/
│       │   ├── VerifiableCredentialVerifier.java           # OAuthトークン検証
│       │   ├── VerifiableCredentialRequestVerifier.java
│       │   ├── VerifiableCredentialJwtProofVerifier.java   # JWT Proof検証
│       │   ├── VerifiableCredentialOAuthTokenVerifier.java
│       │   ├── OAuthVerifiableCredentialVerifier.java
│       │   ├── BatchVerifiableCredentialVerifier.java      # Batch検証
│       │   ├── DeferredVerifiableCredentialVerifier.java   # Deferred検証
│       │   └── DeferredVerifiableCredentialRequestVerifier.java
│       ├── request/
│       │   ├── CredentialRequestParameters.java
│       │   ├── DeferredCredentialRequestParameters.java
│       │   ├── BatchCredentialRequestParameters.java
│       │   ├── BatchCredentialRequests.java
│       │   ├── VerifiableCredentialRequest.java
│       │   ├── VerifiableCredentialProof.java
│       │   └── VerifiableCredentialRequestTransformable.java
│       ├── repository/
│       │   └── VerifiableCredentialTransactionRepository.java
│       ├── exception/
│       │   ├── VerifiableCredentialBadRequestException.java
│       │   ├── VerifiableCredentialTokenInvalidException.java
│       │   └── VerifiableCredentialRequestInvalidException.java
│       ├── VerifiableCredential.java
│       ├── VerifiableCredentials.java
│       ├── VerifiableCredentialTransaction.java
│       ├── VerifiableCredentialTransactionStatus.java    # pending, issued, expired
│       ├── VerifiableCredentialTransactionCreator.java
│       ├── VerifiableCredentialCreator.java
│       ├── VerifiableCredentialCreators.java
│       ├── VerifiableCredentialDelegate.java
│       ├── VerifiableCredentialResponse.java
│       ├── VerifiableCredentialResponseBuilder.java
│       ├── CredentialDelegateResponse.java
│       ├── CredentialProtocol.java
│       └── DefaultCredentialApi.java
│
├── idp-server-core/                                    # コア（VC型定義・設定）
│   └── .../openid/oauth/
│       ├── configuration/vc/
│       │   ├── VerifiableCredentialConfiguration.java
│       │   ├── VerifiableCredentialsSupportConfiguration.java
│       │   ├── VerifiableCredentialDefinitionConfiguration.java
│       │   ├── VerifiableCredentialSubjectConfiguration.java
│       │   └── VerifiableCredentialsDisplayConfiguration.java
│       ├── type/vc/
│       │   ├── Credential.java
│       │   ├── CredentialDefinition.java
│       │   ├── VerifiableCredentialFormat.java
│       │   ├── VerifiableCredentialBuilder.java
│       │   ├── VerifiableCredentialJsonCreator.java
│       │   ├── ProofType.java
│       │   ├── CNonceCreatable.java
│       │   ├── VcInvalidException.java
│       │   ├── VcInvalidKeyException.java
│       │   ├── VerifiableCredentialFormatInvalidException.java
│       │   └── VerifiableCredentialInvalidException.java
│       └── type/verifiablecredential/
│           ├── TransactionId.java
│           ├── CredentialIssuer.java
│           ├── CNonce.java
│           ├── CNonceExpiresIn.java
│           ├── CredentialDefinitionEntity.java
│           ├── DocType.java
│           ├── Format.java
│           ├── ProofEntity.java
│           ├── ProofType.java
│           └── VerifiableCredentialType.java
│
└── idp-server-core-adapter/                            # 永続化
    └── .../datasource/verifiable_credentials/
        ├── VerifiableCredentialTransactionDataSource.java
        ├── VerifiableCredentialTransactionDataSourceProvider.java
        ├── VerifiableCredentialTransactionSqlExecutor.java  # インターフェース
        ├── VerifiableCredentialTransactionSqlExecutors.java # ファクトリ
        ├── PostgresqlExecutor.java
        ├── MysqlExecutor.java
        └── ModelConverter.java
```

---

## Credential発行フロー

### 即時発行

```
1. クライアント → Authorization Request (scope: openid, authorization_details含む)
2. ユーザー認証・同意
3. クライアント → Token Request
4. クライアント → Credential Request (access_token + proof)
5. サーバー → Credential Response (credential含む)
```

### Deferred（遅延）発行

```
1. Credential Request
2. Credential Response (transaction_id含む、credential未発行)
3. ... 非同期処理 ...
4. Deferred Credential Request (transaction_id)
5. Deferred Credential Response (credential含む)
```

---

## 主要クラス

### CredentialHandler

```java
public class CredentialHandler {
    // Credential発行リクエストを処理
    public CredentialResponse handleRequest(
            CredentialRequest request,
            VerifiableCredentialDelegate delegate) {
        // 1. OAuthトークン検証
        OAuthToken oAuthToken = oAuthTokenQueryRepository.find(tenant, accessTokenEntity);
        VerifiableCredentialVerifier verifier = new VerifiableCredentialVerifier(...);
        verifier.verify();

        // 2. Delegateを通じてCredential取得
        CredentialDelegateResponse credentialDelegateResponse =
            delegate.getCredential(tenant, subject, credentialDefinitions);

        // 3. トランザクション作成・保存
        VerifiableCredentialTransaction transaction =
            verifiableCredentialTransactionCreator.create();
        verifiableCredentialTransactionRepository.register(tenant, transaction);

        // 4. 即時発行 or Deferred
        if (credentialDelegateResponse.isIssued()) {
            VerifiableCredential vc = creator.create(credential, ...);
            builder.add(vc);
        }
        if (credentialDelegateResponse.isPending()) {
            builder.add(transaction.transactionId());  // Deferred用
        }

        return new CredentialResponse(CredentialRequestStatus.OK, response);
    }

    // Batch発行
    public BatchCredentialResponse handleBatchRequest(
            BatchCredentialRequest request,
            VerifiableCredentialDelegate delegate) { ... }

    // Deferred発行
    public DeferredCredentialResponse handleDeferredRequest(
            DeferredCredentialRequest request,
            VerifiableCredentialDelegate delegate) { ... }
}
```

### VerifiableCredentialTransaction

```java
// Deferred発行時のトランザクション管理
public class VerifiableCredentialTransaction {
    TransactionId transactionId;           // トランザクションID
    CredentialIssuer credentialIssuer;     // Credential発行者
    RequestedClientId requestedClientId;   // リクエスト元クライアント
    Subject subject;                       // ユーザーsubject
    Credential credential;                 // Credential（発行済みの場合）
    VerifiableCredentialTransactionStatus status;  // pending, issued, expired
}
```

### VerifiableCredentialTransactionStatus

```java
public enum VerifiableCredentialTransactionStatus {
    pending,   // 発行待ち
    issued,    // 発行済み
    expired;   // 期限切れ
}
```

### VerifiableCredentialDelegate

```java
// Credential取得のデリゲートインターフェース
// アプリケーション側で実装し、CredentialHandlerに渡す
public interface VerifiableCredentialDelegate {
    CredentialDelegateResponse getCredential(
        Tenant tenant,
        Subject subject,
        List<CredentialDefinition> credentialDefinitions);
}
```

---

## Authorization Details (RAR)

VCリクエストでは`authorization_details`を使用:

```json
{
  "type": "openid_credential",
  "format": "jwt_vc_json",
  "credential_definition": {
    "type": ["VerifiableCredential", "UniversityDegreeCredential"]
  }
}
```

---

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   └── openid_for_verifiable_credential_rar.test.js  # OID4VCI RAR テスト
│
└── scenario/application/
    └── (VC関連シナリオテスト)
```

---

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core-extension-verifiable-credentials:compileJava

# テスト
cd e2e && npm test -- spec/openid_for_verifiable_credential_rar.test.js
```

---

## トラブルシューティング

### Credential発行失敗

| 問題 | 原因 | 解決策 |
|------|------|--------|
| invalid_token | Access Token無効 | トークンが有効か、scope正しいか確認 |
| invalid_proof | JWT Proof検証失敗 | Proof形式、署名、nonce確認 |
| unsupported_credential_format | 未対応フォーマット | テナント設定でフォーマット有効化 |

### Deferred発行失敗

| 問題 | 原因 | 解決策 |
|------|------|--------|
| issuance_pending | まだ発行処理中 | 一定時間後に再リクエスト |
| invalid_transaction_id | トランザクションID無効 | IDが正しいか、期限切れでないか確認 |

---

## 関連スキル

| スキル | 用途 |
|--------|------|
| `/authorization-endpoint` | 認可リクエスト（authorization_details含む） |
| `/token-management` | トークン発行 |
| `/grant-management` | Grant管理 |
