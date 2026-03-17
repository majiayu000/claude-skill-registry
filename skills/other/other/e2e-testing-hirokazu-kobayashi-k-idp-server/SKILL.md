---
name: e2e-testing
description: E2Eテストの作成・実行を行う際に使用。spec/scenario/monkey/usecaseの4層テスト構造、テストパターン、実行方法に役立つ。
---

# E2Eテスト開発ガイド

## ドキュメント

- `e2e/README.md` - E2Eテスト概要
- `e2e/src/tests/testConfig.js` - テスト設定

---

## テスト構造

```
e2e/src/tests/
├── spec/           # 仕様準拠テスト（RFC/OIDC仕様への準拠確認）
├── scenario/       # シナリオテスト（ユーザーフロー・ユースケース）
├── usecase/        # ユースケーステスト（機能別詳細テスト）
├── monkey/         # ファジングテスト（異常系・エッジケース）
├── security/       # セキュリティテスト
└── integration/    # 統合テスト
```

---

## テストカテゴリ詳細

### spec/ - 仕様準拠テスト

RFC/OIDC仕様への準拠を検証。プロトコルレベルの動作確認。

```
spec/
├── oauth/                              # OAuth 2.0
│   ├── rfc6749_*.test.js              # RFC 6749 (OAuth 2.0)
│   ├── rfc7009_*.test.js              # RFC 7009 (Token Revocation)
│   ├── rfc7662_*.test.js              # RFC 7662 (Token Introspection)
│   └── rfc9126_*.test.js              # RFC 9126 (PAR)
├── oidc_core_*.test.js                # OIDC Core
├── oidc_discovery.test.js             # OIDC Discovery
├── ciba_*.test.js                     # CIBA
├── fapi_*.test.js                     # FAPI Baseline/Advanced
├── jarm.test.js                       # JARM
└── openid_for_verifiable_credential_*.test.js  # OID4VCI
```

### scenario/ - シナリオテスト

実際のユーザーフローを検証。E2Eでの動作確認。

```
scenario/
├── application/                        # アプリケーションシナリオ
│   ├── scenario-01-user-registration.test.js    # ユーザー登録
│   ├── scenario-02-sso-oidc.test.js             # SSOログイン
│   ├── scenario-03-mfa-registration.test.js     # MFA登録
│   ├── scenario-04-ciba-mfa.test.js             # CIBA MFA
│   ├── scenario-05-identity_verification-*.test.js  # 身元確認
│   └── scenario-11-password-policy-full-flow.test.js # パスワードポリシー
├── control_plane/                      # 管理APIシナリオ
│   └── organization/                   # 組織管理
└── resource_server/                    # リソースサーバー
```

### usecase/ - ユースケーステスト

機能別の詳細テスト。特定機能の網羅的検証。

```
usecase/
├── standard/       # 標準機能（brute-force-protection等）
├── advance/        # 高度な機能
├── ciba/           # CIBA詳細テスト
├── mfa/            # MFA詳細テスト
└── financial-grade/  # 金融グレード
```

### monkey/ - ファジングテスト

異常系・エッジケースを検証。意図的な無効入力・プロトコル違反。

```
monkey/
├── authorization-monkey.test.js
├── token-monkey.test.js
├── ciba-monkey.test.js
└── ...
```

---

## テスト設定

### testConfig.js

```javascript
// e2e/src/tests/testConfig.js
module.exports = {
  baseUrl: 'https://api.local.dev',
  authUrl: 'https://auth.local.dev',
  tenantId: '...',
  clientId: '...',
  // ...
};
```

---

## テスト実行

### 全テスト実行

```bash
cd e2e
npm install
npm test
```

### カテゴリ別実行

```bash
# 仕様準拠テスト
npm test -- spec/

# シナリオテスト
npm test -- scenario/

# 特定ファイル
npm test -- spec/oidc_core_3_1_code.test.js

# パターンマッチ
npm test -- --grep "authorization code"
```

### テスト名指定

```bash
npm test -- --testNamePattern="token parameter REQUIRED"
```

---

## テスト作成パターン

### 基本構造

```javascript
const { describe, it, before } = require('mocha');
const { expect } = require('chai');
const config = require('../testConfig');

describe('機能名', () => {
  before(async () => {
    // セットアップ
  });

  describe('正常系', () => {
    it('should return valid response', async () => {
      // テスト実装
      const response = await fetch(`${config.baseUrl}/endpoint`);
      expect(response.status).to.equal(200);
    });
  });

  describe('異常系', () => {
    it('should return error for invalid input', async () => {
      // エラーケース
    });
  });
});
```

### OAuth/OIDC テストパターン

```javascript
// Authorization Request
const authUrl = new URL(`${config.baseUrl}/authorize`);
authUrl.searchParams.set('client_id', config.clientId);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('redirect_uri', config.redirectUri);
authUrl.searchParams.set('scope', 'openid');
authUrl.searchParams.set('state', 'random-state');

// Token Request
const tokenResponse = await fetch(`${config.baseUrl}/token`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authCode,
    redirect_uri: config.redirectUri,
    client_id: config.clientId,
    client_secret: config.clientSecret
  })
});
```

---

## テストデータ設定

### 初期セットアップ

```bash
# admin-tenant 初期化
./init-admin-tenant-config.sh
./setup.sh

# E2Eテスト用データ
./config/scripts/e2e-test-data.sh

# テナント別データ
./config/scripts/e2e-test-tenant-data.sh -t <tenant-id>
```

### テスト用設定ファイル

```
config/examples/
├── standard-oidc-web-app/      # 標準OIDCクライアント
├── fapi-baseline/              # FAPI Baseline
├── fapi-advance/               # FAPI Advanced
├── ciba/                       # CIBA
└── verifiable-credentials/     # VC
```

---

## CI/CD

```bash
# GitHub Actions等での実行
cd e2e
npm ci
npm test -- --reporter json > test-results.json
```

---

## トラブルシューティング

### テスト失敗時

| 問題 | 原因 | 解決策 |
|------|------|--------|
| 接続エラー | サーバー未起動 | `docker compose up -d` 確認 |
| 401 Unauthorized | テストデータ未設定 | `e2e-test-data.sh` 実行 |
| タイムアウト | 処理遅延 | `--timeout 10000` オプション追加 |
| DNS解決失敗 | サブドメイン未設定 | `/local-environment` スキル参照 |

### デバッグ

```bash
# 詳細ログ出力
DEBUG=* npm test -- spec/oidc_core_3_1_code.test.js

# 単一テスト実行
npm test -- --grep "specific test name"
```

---

## 命名規則

| カテゴリ | 命名パターン | 例 |
|---------|-------------|-----|
| spec | `{rfc番号}_{セクション}_{機能}.test.js` | `rfc6749_4_1_authorization_code.test.js` |
| scenario | `scenario-{番号}-{説明}.test.js` | `scenario-01-user-registration.test.js` |
| usecase | `{機能}-{番号}-{説明}.test.js` | `ciba-01-require-rar.test.js` |
| monkey | `{対象}-monkey.test.js` | `authorization-monkey.test.js` |

---

## 関連スキル

| スキル | 用途 |
|--------|------|
| `/local-environment` | ローカル環境構築・トラブルシューティング |
| `/authorization-endpoint` | 認可エンドポイント仕様 |
| `/token-management` | トークンエンドポイント仕様 |
| `/ciba` | CIBA仕様 |
| `/fapi` | FAPI仕様 |
