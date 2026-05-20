---
name: custom-claims
description: カスタムクレーム（Custom Claims）機能の開発・修正を行う際に使用。claims: scopeマッピング、verified_claims: マッピング実装時に役立つ。
---

# カスタムクレーム（Custom Claims）開発ガイド

## ドキュメント

- `documentation/docs/content_03_concepts/04-tokens-claims/concept-03-custom-claims.md` - カスタムクレーム概念
- `documentation/docs/content_03_concepts/04-tokens-claims/concept-01-id-token.md` - ID Token概念

## 機能概要

カスタムクレーム機能は、ID Tokenに任意の属性を含める層。
- **カスタムクレームscopeマッピング**: `claims:attribute_name` 構文
- **Verified claimマッピング**: `verified_claims:attribute_name` 構文（OIDC4IDA準拠）

## モジュール構成

```
libs/
└── idp-server-core/                         # クレームコア
    └── .../oauth/
        ├── response/
        │   ├── AuthorizationResponseIdTokenCreator.java
        │   ├── AuthorizationResponseCodeIdTokenCreator.java
        │   └── AuthorizationResponseCodeTokenIdTokenCreator.java
        └── token/
            └── (トークン生成関連クラス)
```

## ID Token生成

`idp-server-core/oauth/response/` 内:

ID Token生成は、response type別に複数のCreatorクラスが存在します:

| クラス | 用途 |
|--------|------|
| `AuthorizationResponseIdTokenCreator` | Implicit FlowでのID Token生成 |
| `AuthorizationResponseCodeIdTokenCreator` | Authorization Code Flowでのresponse ID Token生成 |
| `AuthorizationResponseCodeTokenIdTokenCreator` | Hybrid Flowでのresponse ID Token生成 |

## カスタムクレームscopeマッピング

### Scope構文

```
claims:attribute_name
```

カスタムクレームは、`claims:` プレフィックスでscopeを指定することで、
ID Tokenに任意の属性を含めることができます。

## Verified Claimマッピング（OIDC4IDA）

### Scope構文

```
verified_claims:attribute_name
```

Verified Claimは、`verified_claims:` プレフィックスでscopeを指定することで、
本人確認済みの属性をID Tokenに含めることができます。

**前提条件**: ユーザーが本人確認済み（`isIdentityVerified()`）であること

## E2Eテスト

```
e2e/src/tests/
└── spec/
    ├── oidc_core_2_id_token.test.js         # ID Token仕様テスト
    └── oidc_core_2_id_token_extension.test.js
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava

# テスト
cd e2e && npm test -- spec/oidc_core_2_id_token.test.js
cd e2e && npm test -- spec/oidc_core_2_id_token_extension.test.js
```

## トラブルシューティング

### カスタムクレームがID Tokenに含まれない
- Scope形式が正しいか確認（`claims:attribute_name`）
- ユーザーの`custom_properties`に属性が存在するか確認

### Verified Claimが含まれない
- ユーザーが本人確認済みか確認（`user.isIdentityVerified()`）
- 認証方式が要件を満たすか確認
