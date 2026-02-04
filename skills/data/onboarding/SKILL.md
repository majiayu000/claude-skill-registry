---
name: onboarding
description: idp-serverプロジェクト初心者向けのオンボーディングガイド。プロジェクト全体像、学習ロードマップ、開発環境構築、最初のコントリビューションまでをサポート。
---

# idp-server オンボーディングガイド

## クイックスタート

詳細なセットアップ手順は以下を参照:
- `documentation/docs/content_02_quickstart/quickstart-01-getting-started.md`

---

## このプロジェクトとは

**idp-server**は、身元確認特化のエンタープライズ・アイデンティティプラットフォームです。

---

## 何ができるか

### ユーザー認証
| 機能 | 説明 |
|------|------|
| **パスワード認証** | 従来型のID/パスワード認証 |
| **多要素認証（MFA）** | SMS OTP、Email OTP |
| **パスワードレス認証** | FIDO2/WebAuthn、Passkey |
| **FIDO-UAF** | モバイルデバイス生体認証 |
| **外部IdP連携（SSO）** | Google、Azure AD、カスタムOIDC |

### 認可・トークン
| 機能 | 説明 |
|------|------|
| **OAuth 2.0** | Authorization Code、Client Credentials、Refresh Token |
| **OpenID Connect** | ID Token発行、UserInfo、Discovery |
| **CIBA** | バックチャネル認証（Poll/Push/Ping） |
| **FAPI** | 金融グレードAPI（Baseline/Advanced） |

### 身元確認（eKYC）
| 機能 | 説明 |
|------|------|
| **本人確認フロー** | 外部eKYCサービス連携 |
| **Verified Claims** | OpenID Connect for IDA準拠 |
| **確認結果管理** | 身元確認結果の保存・参照 |

### エンタープライズ機能
| 機能 | 説明 |
|------|------|
| **マルチテナント** | 組織・テナント単位の完全分離 |
| **管理API** | テナント/クライアント/ユーザー管理 |
| **セキュリティイベント** | Slack/Email/Webhook通知、SSF対応 |
| **監査ログ** | 全操作の記録・検索 |
| **Verifiable Credentials** | デジタル証明書発行 |

### 設定・カスタマイズ
| 機能 | 説明 |
|------|------|
| **認証ポリシー** | クライアント/スコープ別の認証要件 |
| **パスワードポリシー** | 複雑性・有効期限・履歴管理 |
| **セッション管理** | SSO、RP-Initiated Logout、Back-Channel Logout |
| **カスタムクレーム** | 任意の属性をトークンに追加 |

---

## 技術スタック

- Java 21+ / Spring Boot 3.x
- Gradle / PostgreSQL & MySQL
- Hexagonal Architecture + DDD

```
┌─────────────────────────────────────────────────────────────┐
│                      idp-server                              │
├─────────────────────────────────────────────────────────────┤
│  OAuth 2.0 / OpenID Connect / CIBA / FAPI 準拠              │
│  マルチテナント対応 / eKYC連携 / Enterprise Ready           │
└─────────────────────────────────────────────────────────────┘
```

---

## 学習ロードマップ

### Phase 1: 基礎理解（1-2日）

#### Step 1.1: プロジェクト概要を読む
```
CLAUDE.md                           # 必読: プロジェクト概要
documentation/docs/content_01_intro/ # イントロダクション
```

#### Step 1.2: コンセプトを理解する
```
documentation/docs/content_03_concepts/
├── 01-foundation/                  # 基盤
│   ├── concept-01-multi-tenant.md  # マルチテナント
│   ├── concept-02-control-plane.md # 管理API
│   └── concept-03-client.md        # クライアント
├── 02-identity-management/         # ID管理
├── 03-authentication-authorization/ # 認証・認可
│   ├── concept-01-authentication-policy.md
│   └── concept-04-authorization.md
└── 04-tokens-claims/               # トークン・クレーム
```

#### Step 1.3: OAuth 2.0/OIDC基礎（未経験の場合）
```
documentation/docs/content_04_protocols/
├── protocol-01-authorization-code-flow.md  # 認可コードフロー
├── protocol-02-ciba-flow.md                # CIBAフロー
├── protocol-03-introspection.md            # トークンイントロスペクション
└── protocol-06-client-authentication.md    # クライアント認証
```

---

### Phase 2: アーキテクチャ理解（2-3日）

#### Step 2.1: レイヤー構造を理解する

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  idp-server-springboot-adapter (Controller, Filter)         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  idp-server-use-cases (EntryService)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                            │
│  idp-server-core (Handler, Service, Repository IF)          │
│  idp-server-core-extension-* (CIBA, FAPI, IDA等)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                       │
│  idp-server-core-adapter (Repository実装, SQL)              │
│  idp-server-platform (共通基盤)                              │
└─────────────────────────────────────────────────────────────┘
```

#### Step 2.2: モジュール一覧

| モジュール | 役割 | 依存関係 |
|-----------|------|----------|
| `idp-server-core` | OIDCコアエンジン | platform |
| `idp-server-platform` | 共通基盤（JSON, HTTP, Mapper等） | なし |
| `idp-server-use-cases` | EntryService（ユースケース実装） | core, control-plane |
| `idp-server-control-plane` | 管理API契約定義 | core |
| `idp-server-core-adapter` | 永続化実装（PostgreSQL/MySQL） | core |
| `idp-server-springboot-adapter` | Spring Boot統合 | use-cases |
| `idp-server-core-extension-ciba` | CIBA拡張 | core |
| `idp-server-core-extension-fapi` | FAPI拡張 | core |
| `idp-server-core-extension-ida` | 身元確認拡張 | core |
| `idp-server-authentication-interactors` | 認証方式実装 | core |
| `idp-server-federation-oidc` | 外部IdP連携 | core |

#### Step 2.3: 開発者ガイドを読む
```
documentation/docs/content_06_developer-guide/
├── 01-getting-started/             # 入門（サービス概要、アーキテクチャ、設計原則）
├── 02-control-plane/               # 管理API
├── 03-application-plane/           # OAuth/OIDCエンドポイント
├── 04-implementation-guides/       # 実装ガイド
├── 05-configuration/               # 設定
├── 06-patterns/                    # 共通パターン
├── 07-troubleshooting/             # トラブルシューティング
└── 08-reference/                   # リファレンス
```

---

### Phase 3: 開発環境構築（半日）

**詳細ガイド**: `documentation/docs/content_02_quickstart/quickstart-01-getting-started.md`

#### Step 3.1: 必要なツール
```bash
# Java 21+
java -version

# Gradle
./gradlew --version

# Node.js (E2Eテスト用)
node --version
npm --version

# Docker (DB用)
docker --version
```

#### Step 3.2: ビルド確認
```bash
# フォーマット適用
./gradlew spotlessApply

# ビルド
./gradlew build

# 単体テスト
./gradlew test
```

#### Step 3.3: ローカル起動
```bash
# Docker Compose でDB起動
docker-compose up -d

# アプリケーション起動
./gradlew :app:bootRun
```

#### Step 3.4: E2Eテスト実行
```bash
cd e2e
npm install
npm test
```

---

### Phase 4: コードリーディング（3-5日）

#### Step 4.1: 認可フローを追う（推奨開始点）

1. **エントリーポイント**: `OAuthV1Api`
2. **EntryService**: `OAuthFlowEntryService.authorize()`
3. **Handler**: `AuthorizationRequestHandler`
4. **レスポンス生成**: `AuthorizationResponse`

```
libs/idp-server-springboot-adapter/
└── .../restapi/oauth/OAuthV1Api.java

libs/idp-server-use-cases/
└── .../application/enduser/OAuthFlowEntryService.java

libs/idp-server-core/
└── .../openid/authorization/handler/AuthorizationRequestHandler.java
```

#### Step 4.2: トークン発行フローを追う

1. `TokenV1Api` → `TokenEndpointEntryService`
2. `TokenRequestHandler` → 各GrantService
3. `OAuthTokenCreationServices` → トークン生成

#### Step 4.3: 管理APIパターンを理解

```
ManagementApi (契約IF)
    ↓
ManagementEntryService (ユースケース)
    ↓
ManagementHandler (ドメインロジック)
    ↓
Repository (永続化)
```

---

### Phase 5: 最初のコントリビューション（1-2日）

#### Step 5.1: Good First Issue を探す
```bash
gh issue list --label "good first issue" --state open
```

#### Step 5.2: 開発フロー
```bash
# 1. ブランチ作成
git checkout -b feature/issue-番号-説明

# 2. 実装

# 3. フォーマット
./gradlew spotlessApply

# 4. テスト
./gradlew test
cd e2e && npm test -- --grep "関連テスト"

# 5. コミット
git add -A
git commit -m "feat: 説明"

# 6. PR作成
gh pr create
```

#### Step 5.3: コーディング規約

| ルール | 説明 |
|--------|------|
| Tenant第一引数 | Repository操作は常にTenantを第一引数に |
| 値オブジェクト優先 | String/Map濫用禁止 |
| Validator/Verifier | void + throw パターン |
| 両DB対応 | PostgreSQL + MySQL両方実装 |

---

## よく使うスキル

開発時に以下のスキルを活用してください：

| スキル | 用途 |
|--------|------|
| `/architecture` | アーキテクチャ・レイヤー構造 |
| `/authentication` | 認証機能実装 |
| `/authorization-endpoint` | 認可エンドポイント |
| `/token-management` | トークン発行・管理 |
| `/control-plane` | 管理API開発 |
| `/federation` | 外部IdP連携 |
| `/ciba` | CIBA実装 |
| `/identity-verification` | 身元確認機能 |

---

## 困ったときは

### ドキュメント検索
```bash
# キーワードでドキュメント検索
grep -r "キーワード" documentation/docs/
```

### コード検索
```bash
# クラス名・メソッド名で検索
grep -r "クラス名" libs/
```

### E2Eテストから学ぶ
```
e2e/src/tests/
├── spec/           # RFC/OIDC仕様テスト（プロトコル動作確認）
├── scenario/       # シナリオテスト（ユースケース確認）
├── usecase/        # ユースケーステスト（機能確認）
└── monkey/         # ファジングテスト（異常系確認）
```

### Issue一覧確認
```bash
gh issue list --state open
```

---

## 次のステップ

1. **Phase 1-3** を完了したら、実際にローカルで動かしてみる
2. **Phase 4** でコードを読みながら、デバッガで処理を追う
3. **Phase 5** で小さなIssueから始める
4. わからないことがあれば、関連するスキルを参照する

**目標**: 2週間で「認可フロー全体を説明できる」レベルに到達

---

## 関連ドキュメント

- `CLAUDE.md` - プロジェクト概要
- `documentation/docs/content_06_developer-guide/` - 開発者ガイド
- `documentation/docs/content_02_quickstart/` - クイックスタート
- `.claude/skills/` - 各機能のスキル
