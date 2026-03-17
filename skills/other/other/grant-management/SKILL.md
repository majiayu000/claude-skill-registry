---
name: grant-management
description: Grant管理（Grant Management）機能の開発・修正を行う際に使用。AuthorizationGrant、ConsentClaims、同意管理、Grant管理API実装時に役立つ。
---

# Grant管理（Grant Management）開発ガイド

## ドキュメント

- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-05-grant-management.md` - Grant管理概念
- `documentation/openapi/swagger-grant-management-ja.yaml` - Grant管理API仕様（OpenAPI）

## 機能概要

Grant管理は、認可コンテキストを管理する層。
- **AuthorizationGrant**: ユーザー、認証、クライアント、スコープの複合構造
- **AuthorizationGranted**: 永続化されたGrant（created_at/updated_at含む）
- **ConsentClaims**: 同意情報の管理
- **Scopeベース同意**: クライアント別にscopeを記録
- **Grant管理API**: 管理者向けのGrant一覧取得・詳細取得・取り消しAPI

## モジュール構成

```
libs/
├── idp-server-core/                         # Grantコア
│   └── .../grant_management/
│       ├── AuthorizationGranted.java        # 永続化Grant（created_at/updated_at含む）
│       ├── AuthorizationGrantedIdentifier.java
│       ├── AuthorizationGrantedQueries.java # クエリパラメータ（limit上限1000）
│       ├── AuthorizationGrantedRepository.java
│       ├── AuthorizationGrantedQueryRepository.java
│       ├── grant/
│       │   ├── AuthorizationGrant.java      # 認可Grant
│       │   ├── GrantIdTokenClaims.java
│       │   └── GrantUserinfoClaims.java
│       └── consent/
│           └── ConsentClaims.java           # 同意情報
│
├── idp-server-core-adapter/                 # DB実装
│   └── .../grant_management/
│       ├── AuthorizationGrantedDataSource.java
│       ├── AuthorizationGrantedQueryDataSource.java
│       ├── ModelConverter.java              # DB→モデル変換
│       ├── PostgresqlExecutor.java
│       └── MysqlExecutor.java
│
├── idp-server-control-plane/                # Grant管理API定義
│   └── .../management/oidc/grant/
│       ├── OrgGrantManagementApi.java       # APIインターフェース
│       ├── GrantManagementContext.java
│       ├── GrantManagementContextBuilder.java
│       ├── handler/
│       │   ├── OrgGrantManagementHandler.java
│       │   ├── GrantManagementService.java
│       │   ├── GrantFindListService.java
│       │   ├── GrantFindService.java
│       │   └── GrantRevocationService.java  # Grant取り消し+トークン削除
│       └── io/
│           ├── GrantManagementRequest.java
│           ├── GrantManagementResponse.java
│           ├── GrantManagementResult.java
│           └── GrantManagementStatus.java
│
├── idp-server-use-cases/                    # EntryService
│   └── .../control_plane/organization_manager/
│       └── OrgGrantManagementEntryService.java
│
└── idp-server-springboot-adapter/           # REST API
    └── .../control_plane/restapi/organization/
        └── OrganizationGrantManagementV1Api.java
```

## Grant管理API（Organization Level）

### エンドポイント

| メソッド | パス | 説明 | 権限 |
|---------|------|------|------|
| GET | `/v1/management/organizations/{org-id}/tenants/{tenant-id}/grants` | Grant一覧取得 | `GRANT_READ` |
| GET | `/v1/management/organizations/{org-id}/tenants/{tenant-id}/grants/{grant-id}` | Grant詳細取得 | `GRANT_READ` |
| DELETE | `/v1/management/organizations/{org-id}/tenants/{tenant-id}/grants/{grant-id}` | Grant取り消し | `GRANT_DELETE` |

### クエリパラメータ（一覧取得）

| パラメータ | 説明 |
|-----------|------|
| `user_id` | ユーザーIDでフィルタ |
| `client_id` | クライアントIDでフィルタ |
| `from` | 作成日時の開始範囲（ISO 8601） |
| `to` | 作成日時の終了範囲（ISO 8601） |
| `limit` | 最大件数（デフォルト20、上限1000） |
| `offset` | スキップ件数 |

### dry_runモード

DELETE時に `?dry_run=true` を指定すると、実際の削除を行わずシミュレーション結果を返す。

### Grant取り消し時の動作

Grant削除時に、同じuser+clientの**全トークン**（アクセストークン、リフレッシュトークン）も削除される（Auth0スタイル）。

## AuthorizationGranted構造

```java
public class AuthorizationGranted {
    AuthorizationGrantedIdentifier identifier;
    AuthorizationGrant authorizationGrant;
    LocalDateTime createdAt;
    LocalDateTime updatedAt;

    public Map<String, Object> toMap() {
        // id, user, client, scopes, created_at, updated_at を返す
    }
}
```

## AuthorizationGrant構造

```java
public class AuthorizationGrant {
    TenantIdentifier tenantIdentifier;
    User user;
    Authentication authentication;
    RequestedClientId requestedClientId;
    ClientAttributes clientAttributes;
    GrantType grantType;
    Scopes scopes;
    GrantIdTokenClaims idTokenClaims;
    GrantUserinfoClaims userinfoClaims;
    CustomProperties customProperties;
    AuthorizationDetails authorizationDetails;
    ConsentClaims consentClaims;
}
```

## Grantが作成されるタイミング

- Authorization Code Flowでの同意時
- Password Grantでのトークン発行時（スコープはマージされる）
- その他のGrant Typeでのトークン発行時

## E2Eテスト

```
e2e/src/tests/
├── usecase/standard/
│   └── standard-05-grant-revocation.test.js   # Grant取り消しE2E
└── scenario/control_plane/organization/
    └── organization_grant_management.test.js  # Grant管理APIテスト
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava
./gradlew :libs:idp-server-control-plane:compileJava

# E2Eテスト
cd e2e && npm test -- src/tests/usecase/standard/standard-05-grant-revocation.test.js
cd e2e && npm test -- src/tests/scenario/control_plane/organization/organization_grant_management.test.js
```

## トラブルシューティング

### Grantが見つからない
- AuthorizationGrantedが正しく生成されているか確認
- ユーザー、認証、クライアント情報が揃っているか確認
- Password Grantの場合、`ResourceOwnerPasswordCredentialsGrantService`でGrant作成ロジックを確認

### Grant取り消し後もトークンが有効
- `GrantRevocationService`で`deleteByUserAndClient`が呼ばれているか確認
- トランザクションが正しくコミットされているか確認

### created_at/updated_atがレスポンスに含まれない
- `ModelConverter.parseLocalDateTime()`が正しくパースしているか確認
- DBからのtimestamp形式を確認（`LocalDateTimeParser`で対応）
