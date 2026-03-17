---
name: control-plane
description: 管理API（Control Plane）の開発・修正を行う際に使用。システムレベル・組織レベルAPI、リソース管理、権限モデル実装時に役立つ。
---

# Control Plane（管理API）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/02-control-plane/00-resource-overview.md` - リソース一覧
- `documentation/docs/content_06_developer-guide/02-control-plane/01-overview.md` - Control Plane概要
- `documentation/docs/content_06_developer-guide/02-control-plane/03-system-level-api.md` - システムレベルAPI
- `documentation/docs/content_06_developer-guide/02-control-plane/04-organization-level-api.md` - 組織レベルAPI

## 機能概要

Control Planeは、idp-serverの管理API層。システム全体の設定管理、組織・テナント管理、リソース構成を行う。
- **2層構造**: System Level（プラットフォーム全体）、Organization Level（組織別）
- **Dry-runモード**: 全変更操作でサポート
- **権限モデル**: 40+のデフォルト管理者権限

## モジュール構成

```
libs/
├── idp-server-control-plane/                # 管理API契約定義
│   └── .../control_plane/management/
│       ├── organization/                    # 組織管理API
│       │   └── OrganizationManagementApi.java
│       ├── tenant/                          # テナント管理API
│       │   └── TenantManagementApi.java
│       ├── oidc/client/                     # クライアント管理API
│       │   └── ClientManagementApi.java
│       ├── authentication/                  # 認証ポリシー管理API
│       │   └── AuthenticationPolicyManagementApi.java
│       ├── identity/user/                   # ユーザー管理API
│       │   └── UserManagementApi.java
│       └── ... (各ドメイン別)
│
├── idp-server-use-cases/                    # EntryService実装
│   └── .../management/
│       ├── system/
│       │   └── OrganizationManagementEntryService.java
│       └── organization/
│           └── TenantManagementEntryService.java
│
└── idp-server-core/                         # ドメインロジック
    └── .../handler/
        ├── OrganizationHandler.java
        └── TenantHandler.java
```

## API設計パターン

### システムレベルAPI

```java
// 1. ManagementApi (契約定義)
public interface OrganizationManagementApi {
    ResponseEntity<?> create(OrganizationCreateRequest request);
    ResponseEntity<?> update(
        String orgId,
        OrganizationUpdateRequest request
    );
}

// 2. EntryService (use-casesモジュール)
public class OrganizationManagementEntryService {
    public void create(OrganizationCreateRequest request) {
        // Handler呼び出し
        handler.create(request.toEntity());
    }
}

// 3. Handler (coreモジュール)
public class OrganizationHandler {
    public void create(Organization org) {
        // Validator で検証
        validator.validate(org);

        // Repository呼び出し
        repository.register(org);
    }
}
```

### 組織レベルAPI（Tenant第一引数パターン）

```java
// Handler: Tenant第一引数
public class ClientHandler {
    public void create(Tenant tenant, Client client) {
        validator.validate(tenant, client);
        repository.register(tenant, client);
    }
}

// Repository: Tenant第一引数必須（OrganizationRepository除く）
public interface ClientRepository {
    void register(Tenant tenant, Client client);
    Client find(Tenant tenant, ClientId clientId);
}
```

## E2Eテスト

```
e2e/src/tests/
└── scenario/control_plane/
    ├── organization/
    │   ├── organization_tenant_management.test.js
    │   ├── organization_client_management.test.js
    │   ├── organization_scope_management.test.js
    │   ├── organization_authentication_policy_management*.test.js
    │   ├── organization_federation_configuration_management.test.js
    │   └── organization_identity_verification_config_management*.test.js
    └── resource_server/
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-control-plane:compileJava
./gradlew :libs:idp-server-use-cases:compileJava

# テスト
cd e2e && npm test -- scenario/control_plane/organization/
```

## トラブルシューティング

### Tenant第一引数エラー
- 全Repository操作で`Tenant`を第一引数に渡す（`OrganizationRepository`除く）
- `repository.find(tenant, clientId)` ✓
- `repository.find(clientId)` ✗

### Dry-runが動作しない
- Handler層で`dryRun`パラメータを受け取る
- `if (dryRun) return;`の前にValidatorを実行
- AuditLogには記録（実データ変更のみスキップ）
