---
name: user-management
description: ユーザー管理（User Management）機能の開発・修正を行う際に使用。ユーザー登録、ID Policy、preferred_username、ユーザーステータス、パスワードポリシー実装時に役立つ。
---

# ユーザー管理（User Management）開発ガイド

## ドキュメント

- `documentation/docs/content_03_concepts/02-identity-management/concept-01-id-management.md` - ID管理概念
- `documentation/docs/content_03_concepts/02-identity-management/concept-02-password-policy.md` - パスワードポリシー概念

## 機能概要

ユーザー管理は、ユーザーのライフサイクルとアイデンティティを管理する層。
- **ユーザー登録**: 直接登録、Federation経由登録
- **ID Policy**: USERNAME, EMAIL, PHONE, EXTERNAL_USER_ID
- **preferred_username自動割り当て**: ID Policyに基づく自動設定
- **ユーザーステータス管理**: UNREGISTERED → REGISTERED → VERIFIED → LOCKED/DISABLED/DELETED
- **パスワードポリシー**: NIST SP 800-63B準拠

## モジュール構成

```
libs/
├── idp-server-core/                         # ユーザー管理コア
│   └── .../openid/identity/
│       ├── User.java                       # ユーザーエンティティ
│       ├── UserRegistrator.java            # ユーザー登録
│       ├── UserLifecycleManager.java       # ライフサイクル管理
│       ├── UserVerifier.java               # ユーザー検証
│       ├── UserStatus.java                 # ユーザーステータス
│       ├── UserIdentifier.java             # ユーザーID
│       ├── authentication/
│       │   ├── PasswordPolicyValidator.java
│       │   └── PasswordChangeService.java
│       └── repository/
│           ├── UserCommandRepository.java
│           └── UserQueryRepository.java
│
└── idp-server-control-plane/               # 管理API
    └── .../management/identity/
        └── UserManagementApi.java
```

## UserRegistrator

`idp-server-core/openid/identity/UserRegistrator.java` 内の実際の実装:

```java
public class UserRegistrator {

    UserQueryRepository userQueryRepository;
    UserCommandRepository userCommandRepository;
    UserVerifier userVerifier;

    public User registerOrUpdate(Tenant tenant, User user) {

        User existingUser = userQueryRepository.findById(
            tenant,
            user.userIdentifier()
        );

        if (existingUser.exists()) {
            User updatedUser = existingUser.updateWith(user);
            applyIdentityPolicyIfNeeded(tenant, updatedUser);
            userCommandRepository.update(tenant, updatedUser);
            return updatedUser;
        }

        // Identity Policy適用（preferred_username設定）
        applyIdentityPolicyIfNeeded(tenant, user);

        // ビジネスルール検証
        userVerifier.verify(tenant, user);

        // ステータス設定
        if (user.status().isInitialized()) {
            user.setStatus(UserStatus.REGISTERED);
        }

        userCommandRepository.register(tenant, user);

        return user;
    }

    /**
     * Identity Policyを適用してpreferred_usernameを再計算
     *
     * OIDC Core仕様: preferred_usernameはmutableで変更可能
     * テナントのIdentity Policy（username, email, phone, external_user_id）
     * に基づいて自動割り当て
     */
    private void applyIdentityPolicyIfNeeded(Tenant tenant, User user) {
        user.applyIdentityPolicy(tenant.identityPolicyConfig());
    }
}
```

## UserStatus（ユーザーステータスライフサイクル）

```java
public enum UserStatus {
    UNREGISTERED,   // 未登録
    REGISTERED,     // 登録済み
    VERIFIED,       // 本人確認済み
    LOCKED,         // ロック中
    DISABLED,       // 無効化
    DELETED;        // 削除済み

    public boolean isInitialized() { ... }
    public boolean isActive() { ... }
}
```

## ID Policy種類

| Policy | 説明 | preferred_username割り当て |
|--------|------|---------------------------|
| `USERNAME` | ユーザー名ベース | username |
| `EMAIL` | メールアドレスベース | email |
| `PHONE` | 電話番号ベース | phone_number |
| `EXTERNAL_USER_ID` | 外部IdPベース | external_user_id |

**注意**: preferred_usernameは、ID Policyに基づいて**自動設定**されます（Issue #729対応）。

## パスワードポリシー

`idp-server-core/openid/identity/authentication/` 内:

```java
public class PasswordPolicyValidator {
    // NIST SP 800-63B準拠
    // - 最小8文字（デフォルト）
    // - 複雑性要件（大文字、小文字、数字、特殊文字）
    // - カスタム正規表現パターン
}
```

## パスワード変更

```java
public class PasswordChangeService {
    public void changePassword(
        Tenant tenant,
        UserId userId,
        String oldPassword,
        String newPassword
    ) {
        // 既存パスワード検証
        // パスワードポリシー検証
        // パスワードハッシュ更新
    }
}
```

## E2Eテスト

```
e2e/src/tests/
├── scenario/application/
│   └── scenario-01-user-registration.test.js  # ユーザー登録シナリオ
│
└── usecase/standard/
    └── standard-01-onboarding-and-audit.test.js
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava

# テスト
cd e2e && npm test -- scenario/application/scenario-01-user-registration.test.js
```

## トラブルシューティング

### ユーザー登録失敗
- UserVerifierのビジネスルール検証を確認
- ID Policyが正しく設定されているか確認

### preferred_usernameが設定されない
- Tenant.identityPolicyConfig()を確認
- User.applyIdentityPolicy()が呼ばれているか確認

### パスワードポリシー違反
- PasswordPolicyValidatorの設定を確認
- 最小文字数、複雑性要件を確認

### ユーザーステータスが更新されない
- UserStatus遷移ルールを確認
- UserLifecycleManagerが正しく動作しているか確認
