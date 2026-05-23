---
name: fapi
description: FAPI（Financial-grade API）機能の開発・修正を行う際に使用。FAPI 1.0 Baseline/Advanced, FAPI CIBA, mTLS, PAR, JARM実装時に役立つ。
---

# FAPI（Financial-grade API）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/04-implementation-guides/oauth-oidc/fapi.md` - FAPI実装ガイド
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-06-fapi.md` - FAPI概念
- `documentation/docs/content_10_ai_developer/ai-32-extension-fapi.md` - AI開発者向けFAPIガイド
- `documentation/docs/content_06_developer-guide/03-application-plane/02-01-authorization-request-verification.md` - 認可リクエスト検証フロー詳細（プロファイル決定、検証チェーン、エラーハンドリング）
- `documentation/requirements/fapi-1.0-gap-analysis.yaml` - FAPI 1.0 Gap分析（OIDF適合性テスト結果と修正記録）
- `documentation/docs/content_05_how-to/phase-2-security/05-fapi-setup.md` - FAPIセットアップガイド（プロファイル決定、認可サーバー/クライアント設定、OIDF認定チェックリスト）
- `documentation/requirements/fapi-1.0-advanced-op-test-mapping.md` - FAPI 1.0 Advanced OPテスト63件とRFC/仕様要件のマッピング表

## 機能概要

FAPIは、金融グレードのセキュリティを実現するOIDC/OAuth 2.0プロファイル。
- **FAPI 1.0 Baseline Profile**: 基本的なセキュリティ要件
- **FAPI 1.0 Advanced Profile**: 高度なセキュリティ要件（PAR, JARM, mTLS必須）
- **FAPI CIBA Profile**: CIBAとFAPIの組み合わせ
- **Sender-constrained Access Token**: mTLSバインディング

## プロファイル適用条件

FAPIプロファイルは**リクエストのスコープ**と**テナントの`extension`設定**で自動決定される。

| 優先度 | 条件 | プロファイル |
|--------|------|-------------|
| 1 | テナント`extension.fapi_advance_scopes`に該当するスコープあり | FAPI_ADVANCE |
| 2 | テナント`extension.fapi_baseline_scopes`に該当するスコープあり | FAPI_BASELINE |
| 3 | `openid`スコープを含む | OIDC |
| 4 | 上記以外 | OAUTH2 |

CIBAフローではbaseline/advanceどちらのスコープでも `FAPI_CIBA` になる。

**詳細**: `content_06_developer-guide/03-application-plane/02-01-authorization-request-verification.md` セクション2.3〜3（プロファイル決定、検証チェーン、エラーハンドリング）

## モジュール構成

```
libs/
├── idp-server-core-extension-fapi/          # FAPI拡張モジュール
│   └── .../extension/fapi/
│       ├── FapiBaselineVerifier.java       # FAPI Baseline検証
│       ├── FapiAdvanceVerifier.java        # FAPI Advanced検証
│       ├── FapiProfileValidator.java       # FAPIプロファイル検証
│       ├── TlsClientAuthAuthenticator.java # mTLSクライアント認証
│       └── SelfSignedTlsClientAuthAuthenticator.java
│
├── idp-server-core-extension-fapi-ciba/     # FAPI-CIBA拡張
│   └── .../extension/fapi/ciba/
│       └── FapiCibaVerifier.java
│
├── idp-server-core/                         # コア（PAR, JARM実装）
│   └── .../oauth/
│       ├── request/
│       │   └── OAuthPushedRequestParameters.java  # PAR
│       ├── response/
│       │   └── JarmCreatable.java                 # JARM
│       ├── io/
│       │   ├── OAuthPushedRequest.java
│       │   └── OAuthPushedRequestResponse.java
│       └── verifier/extension/
│           └── JarmVerifier.java
│
└── idp-server-control-plane/               # 管理API
    └── .../management/fapi/
        └── FapiConfigManagementApi.java
```

## FAPI Baseline検証

`idp-server-core-extension-fapi/` モジュール内:

```java
public class FapiBaselineVerifier {
    public void verify(
        AuthorizationRequest request,
        Client client
    ) {
        // 1. response_type=code only
        if (!request.responseType().isCode()) {
            throw new InvalidRequestException(
                "fapi_baseline_requires_code_flow"
            );
        }

        // 2. PKCE必須（S256のみ）
        if (!request.hasCodeChallenge()) {
            throw new InvalidRequestException(
                "code_challenge_required"
            );
        }

        if (request.codeChallengeMethod() != CodeChallengeMethod.S256) {
            throw new InvalidRequestException(
                "code_challenge_method_must_be_s256"
            );
        }

        // 3. state必須
        if (!request.hasState()) {
            throw new InvalidRequestException("state_required");
        }

        // 4. nonce必須（OpenID Connect時）
        if (request.scope().contains("openid") &&
            !request.hasNonce()) {
            throw new InvalidRequestException("nonce_required");
        }
    }
}
```

## FAPI Advanced検証

```java
public class FapiAdvanceVerifier {
    public void verify(
        AuthorizationRequest request,
        Client client
    ) {
        // Baseline要件チェック
        fapiBaselineVerifier.verify(request, client);

        // 1. PAR必須
        if (!request.isPushedAuthorizationRequest()) {
            throw new InvalidRequestException(
                "par_required_for_fapi_advanced"
            );
        }

        // 2. JARM必須
        if (!request.hasResponseMode() ||
            !request.responseMode().isJwt()) {
            throw new InvalidRequestException(
                "jarm_required_for_fapi_advanced"
            );
        }

        // 3. mTLS必須
        if (!request.hasMtlsCertificate()) {
            throw new InvalidRequestException(
                "mtls_required_for_fapi_advanced"
            );
        }
    }
}
```

## PAR（Pushed Authorization Requests）

`idp-server-core/oauth/request/` および `oauth/io/` 内:

PAR実装は以下のクラスで構成:
- `OAuthPushedRequestParameters` - PAR処理
- `OAuthPushedRequest` - リクエスト表現
- `OAuthPushedRequestResponse` - レスポンス表現

### PARレスポンスのHTTPステータスコード

RFC 9126 Section 2.2 に従い、PAR成功レスポンスは **HTTP 201 Created** を返す。

- `OAuthPushedRequestStatus.CREATED(201)` - 成功ステータス
- `OAuthV1Api` のPARエンドポイントは `response.statusCode()` でステータスを動的に決定

### PAR + FAPI Advanced の検証アーキテクチャ

FAPI Advanced では認可リクエストに JWS 署名付き Request Object が必須（Section 5.2.2 clause 1）。
PAR 経由のリクエストでは、以下の2段階で検証が分離される:

**1. PARエンドポイント（`OAuthRequestHandler.handlePushedRequest`）**
- クライアントは plain パラメータ または Request Object（JWT）を PAR エンドポイントに POST
- `OAuthRequestPattern` が `NORMAL` または `REQUEST_OBJECT` として解析される
- `OAuthRequestVerifier.verify()` で FAPI Advanced の全検証を実行（署名、exp、nbf、aud 含む）
- 検証通過後、`AuthorizationRequest` をリポジトリに保存
- `request_uri`（`urn:ietf:params:oauth:request_uri:...`）を発行

**2. 認可エンドポイント（`OAuthRequestHandler.handleRequest`）**
- クライアントは `client_id` + `request_uri` で認可エンドポイントにアクセス
- `OAuthRequestPattern` が `PUSHED_REQUEST_URI` として解析される
- `PushedRequestUriPatternContextCreator` が保存済みパラメータを復元
- **JoseContext は空**（保存時に JoseContext 情報は保持されない）
- `FapiAdvanceVerifier` は PAR 経由の場合、以下の検証をスキップ:
  - Request Object 署名検証（`isUnsignedRequestObject`）
  - JWT クレーム検証（exp、nbf、aud）
- 以下の検証は PAR 経由でも実行:
  - JARM 設定チェック
  - response_type / response_mode 検証
  - sender-constrained access token 検証
  - クライアント認証方式検証
  - public client 拒否

```
PARエンドポイント                    認可エンドポイント
┌─────────────────────┐            ┌─────────────────────┐
│ パラメータ受信        │            │ request_uri 受信      │
│ ↓                   │            │ ↓                   │
│ パターン解析          │            │ PUSHED_REQUEST_URI   │
│ (NORMAL/REQUEST_OBJ) │            │ ↓                   │
│ ↓                   │            │ 保存済みパラメータ復元  │
│ FAPI Advanced 全検証  │            │ (JoseContext は空)    │
│ (署名,exp,nbf,aud)   │            │ ↓                   │
│ ↓                   │            │ FAPI Advanced 検証    │
│ クライアント認証       │            │ (JWT検証はスキップ)   │
│ ↓                   │            │ ↓                   │
│ AuthzRequest 保存     │            │ 認可処理続行          │
│ ↓                   │            └─────────────────────┘
│ request_uri 発行      │
└─────────────────────┘
```

**関連ファイル:**
- `FapiAdvanceVerifier.java` - PAR判定とスキップロジック
- `OAuthRequestHandler.java` - PAR/認可の2段階ハンドリング
- `PushedRequestUriPatternContextCreator.java` - PAR復元時の空JoseContext生成
- `OAuthRequestPattern.java` - NORMAL / REQUEST_OBJECT / REQUEST_URI / PUSHED_REQUEST_URI の4パターン
- `OAuthPushedRequestStatus.java` - CREATED(201) / BAD_REQUEST(400) / UNAUTHORIZED(401) / SERVER_ERROR(500)

## JARM（JWT-secured Authorization Response Mode）

`idp-server-core/oauth/response/` 内:

JARM実装は以下のクラスで構成:
- `JarmCreatable` - JARM生成インターフェース
- `JarmVerifier` - JARM検証

## mTLS（Mutual TLS）

`idp-server-core-extension-fapi/` 内:

mTLS実装は以下のクラスで構成:
- `TlsClientAuthAuthenticator` - tls_client_auth方式
- `SelfSignedTlsClientAuthAuthenticator` - self_signed_tls_client_auth方式

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   ├── fapi_baseline.test.js                # FAPI Baseline仕様
│   ├── fapi_advance.test.js                 # FAPI Advanced仕様
│   ├── fapi_ciba.test.js                    # FAPI CIBA仕様
│   ├── rfc9126_par.test.js                  # PAR (RFC 9126)
│   └── jarm.test.js                         # JARM仕様
│
├── usecase/financial-grade/
│   ├── financial-grade-01-transfer-flow.test.js
│   └── financial-grade-02-authentication-device-rule.test.js
│
└── security/
    └── (FAPI関連セキュリティテスト)
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core-extension-fapi:compileJava
./gradlew :libs:idp-server-core-extension-fapi-ciba:compileJava

# テスト
cd e2e && npm test -- spec/fapi_baseline.test.js
cd e2e && npm test -- spec/fapi_advance.test.js
cd e2e && npm test -- spec/rfc9126_par.test.js
cd e2e && npm test -- usecase/financial-grade/
```

## OIDF適合性テスト（OIDF Conformance Test Suite）

### 概要

OpenID Foundation (OIDF) が提供する適合性テストスイートで、FAPI仕様への準拠を自動検証する。
テストスイートURL: `https://www.certification.openid.net/`

本プロジェクトでは以下の2つのテストプランを実行:

| テストプラン | 内容 | テスト数 |
|-------------|------|---------|
| **FAPI 1.0 Advanced Final** (`fapi1-advanced-final-test-plan`) | 認可フロー、Request Object検証、JARM、mTLS、エラーハンドリング | ~30テスト |
| **FAPI-CIBA ID1** (`fapi-ciba-id1-test-plan`) | CIBAフロー、poll/pingモード、Request Object検証、Refresh Token | ~30テスト |

### テスト環境の構成

```
OIDF Conformance Suite (https://www.certification.openid.net/)
    ↕ HTTPS
ローカル idp-server (api.local.dev / mtls.api.local.dev)
    ↕
Financial-grade テナント (tenant_id: c3d4e5f6-a7b8-c9d0-e1f2-a3b4c5d6e7f8)
```

OIDFテストスイートがローカルサーバーにHTTPSでアクセスするため、ローカル環境が外部からアクセス可能である必要がある（ngrok等のトンネリングまたはDNS設定）。

### financial-gradeテナントのセットアップ

```bash
# 1. ローカル環境起動
docker compose up -d

# 2. financial-gradeテナント作成（管理APIで組織・テナント・クライアント一括作成）
cd config/examples/financial-grade
./setup.sh

# 3. テナント設定の更新（既存テナントの設定変更時）
./update.sh

# 4. テナント削除（クリーンアップ）
./delete.sh
```

**setup.sh が行うこと:**
1. `.env`から管理者認証情報を読み込み、アクセストークンを取得
2. `onboarding-request.json`を使って組織+テナント+クライアント群を一括作成
3. 認証ポリシー、認証設定（FIDO2等）を個別APIで設定
4. テストユーザーを作成

**主要設定ファイル:**

| ファイル | 内容 |
|---------|------|
| `onboarding-request.json` | テナント定義 + 全クライアント定義（一括オンボーディング） |
| `financial-tenant.json` | テナント設定のリファレンス（discovery応答に反映される値） |
| `tls-client-auth-client.json` | tls_client_auth方式クライアント |
| `tls-client-auth-client-2.json` | tls_client_auth方式クライアント（2nd client for OIDF） |
| `private-key-jwt-client.json` | private_key_jwt方式クライアント |
| `financial-client.json` | self_signed_tls_client_auth方式クライアント |
| `authentication-policy/oauth.json` | FAPI用認証ポリシー |
| `certs/` | mTLSクライアント証明書・CA証明書 |

### OIDF テスト設定ファイル

OIDFテストスイートにインポートするJSON設定:

```
config/examples/financial-grade/oidc-test/
├── fapi/
│   └── tls_client_auth.json          # FAPI 1.0 Advanced Final (tls_client_auth)
└── fapi-ciba/
    ├── tls_client_auth_poll.json      # FAPI-CIBA (tls_client_auth + poll)
    ├── private_key_jwt_poll.json      # FAPI-CIBA (private_key_jwt + poll)
    └── FAPI-CIBA-test-cases.md        # テストケース詳細ドキュメント
```

**設定ファイルの構造:**
```json
{
  "alias": "テスト計画の識別名",
  "server": {
    "discoveryUrl": "https://api.local.dev/{tenant_id}/.well-known/openid-configuration"
  },
  "client": { "client_id": "...", "scope": "...", "jwks": {...} },
  "client2": { "client_id": "...", "scope": "...", "jwks": {...} },
  "mtls": { "key": "...", "cert": "..." },
  "mtls2": { "key": "...", "cert": "..." },
  "resource": {
    "resourceUrl": "https://mtls.api.local.dev/{tenant_id}/v1/me/identity-verification/applications"
  }
}
```

**注意:**
- `discoveryUrl`は通常エンドポイント (`api.local.dev`)
- `resourceUrl`はmTLSエンドポイント (`mtls.api.local.dev`) — sender-constrainedトークン検証にクライアント証明書が必要
- `client`と`client2`は2クライアントテスト用（証明書バインドアクセストークンの交差検証等）
- `mtls`/`mtls2`はそれぞれのクライアントのTLSクライアント証明書

### FAPI-CIBAテスト時の追加要件

CIBAテストではユーザーがデバイスで認証を承認する必要がある:

```bash
# CIBAデバイス認証シミュレーション（テスト中に手動実行）
cd config/examples/financial-grade
./ciba-device-auth.sh
```

このスクリプトはCIBAバックチャネル認証リクエストに対して、ユーザーの認証承認をシミュレートする。

### Gap分析ドキュメント

`documentation/requirements/fapi-1.0-gap-analysis.yaml` にOIDF適合性テスト結果と修正記録を管理:
- 各GAP項目のID、仕様参照、修正状態、修正内容を記録
- テナント設定・クライアント設定の要件充足分析も含む
- 新しいGAPが見つかった場合はこのファイルに追記する

## トラブルシューティング

### PKCE S256エラー
- `code_challenge_method=S256`のみ許可（plainは不可）
- FAPI Baselineでは必須

### PAR request_uri無効
- request_uriの有効期限（90秒）を確認
- 使用済みrequest_uriは再利用不可

### mTLS証明書検証失敗
- クライアント証明書が正しく送信されているか確認
- `TlsClientAuthAuthenticator` の設定を確認

### JARM署名検証失敗
- Authorization Serverの署名鍵（JWK）を確認
- `response`パラメータのJWT形式を確認

### OIDFテスト discoveryUrl エラー
- `discoveryUrl`が`api.local.dev`(通常エンドポイント)を指しているか確認
- `resourceUrl`が`mtls.api.local.dev`(mTLSエンドポイント)を指しているか確認
- `host.docker.internal:8445`等の旧URL形式が残っていないか確認
