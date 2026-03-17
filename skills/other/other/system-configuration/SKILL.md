---
name: system-configuration
description: システム設定（System Configuration）機能の開発・修正を行う際に使用。SSRF保護、Trusted Proxies、HTTPセキュリティ実装時に役立つ。
---

# システム設定（System Configuration）開発ガイド

## ドキュメント

- `documentation/docs/content_03_concepts/06-security-extensions/concept-04-system-configuration.md` - システム設定概念
- `documentation/docs/content_06_developer-guide/05-configuration/system-configuration.md` - システム設定ガイド

## 機能概要

システム設定は、プラットフォーム全体のセキュリティ設定を管理する層。
- **SSRF保護**: Server-Side Request Forgery攻撃防止
- **Trusted Proxies**: X-Forwarded-Forヘッダー信頼設定
- **プライベートIPブロック**: 内部ネットワークへのアクセス防止
- **Allowlist検証**: OWASP推奨のホワイトリスト方式

## モジュール構成

```
libs/
├── idp-server-platform/                     # プラットフォーム基盤
│   └── .../platform/
│       ├── security/ssrf/
│       │   ├── SsrfProtectionValidator.java  # SSRF保護
│       │   └── PrivateIpRange.java           # プライベートIP定義
│       ├── system/
│       │   ├── SystemConfiguration.java
│       │   └── config/
│       │       ├── SsrfProtectionConfig.java
│       │       └── TrustedProxyConfig.java
│       └── http/
│           └── SsrfProtectedHttpClient.java
│
└── idp-server-springboot-adapter/           # Spring Boot統合
    └── .../adapters/springboot/
        └── TrustedProxyFilter.java          # Proxyフィルター
```

## SSRF保護

`idp-server-platform/security/ssrf/SsrfProtectionValidator.java` 内の実際の実装:

```java
/**
 * SSRF攻撃を防ぐURLとIPアドレスの検証
 *
 * OWASP推奨の防御施策:
 * - プライベート/内部IPレンジへのリクエストをブロック
 * - クラウドメタデータサービスへのアクセスをブロック
 * - HTTP/HTTPSスキームのみ許可
 * - DNS解決後のIPアドレスを検証
 */
public class SsrfProtectionValidator {

    private final Set<PrivateIpRange> blockedRanges;
    private final Set<String> bypassHosts;

    /** 全プライベートIPレンジをブロックするValidator */
    public SsrfProtectionValidator() {
        this.blockedRanges = EnumSet.allOf(PrivateIpRange.class);
        this.bypassHosts = Collections.emptySet();
    }

    /**
     * 開発用: バイパスホストを設定
     * localhost, mock-service等を許可
     */
    public static SsrfProtectionValidator withBypassHosts(
        Set<String> bypassHosts
    ) {
        return new SsrfProtectionValidator(
            EnumSet.allOf(PrivateIpRange.class),
            bypassHosts
        );
    }

    /**
     * URI検証
     */
    public void validate(URI targetUri) {
        // スキーム検証（HTTP/HTTPSのみ）
        // DNS解決
        // IPアドレス検証（プライベートIPブロック）
    }

    /**
     * Allowlist検証（OWASP推奨）
     */
    public void validateWithAllowlist(
        URI targetUri,
        Set<String> allowedHosts
    ) {
        // ホストがAllowlistに含まれるか確認
        // SSRF保護も併用
    }
}
```

## PrivateIpRange（ブロック対象）

```java
public enum PrivateIpRange {
    PRIVATE_10,      // 10.0.0.0/8
    PRIVATE_172,     // 172.16.0.0/12
    PRIVATE_192,     // 192.168.0.0/16
    LOOPBACK,        // 127.0.0.0/8
    LINK_LOCAL,      // 169.254.0.0/16
    CLOUD_METADATA;  // クラウドメタデータサービス
}
```

## Trusted Proxies

`idp-server-springboot-adapter/TrustedProxyFilter.java` 内の実際の実装:

```java
/**
 * Trusted Proxyからの実クライアントIP解決
 *
 * リバースプロキシ・ロードバランサー背後で動作する際、
 * X-Forwarded-Forヘッダーから実クライアントIPを抽出
 *
 * セキュリティ:
 * - X-Forwarded-Forは偽装可能
 * - Trusted Proxy設定が有効な場合のみ信頼
 * - リクエストのremote addressがTrusted Proxyと一致する場合のみ
 */
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class TrustedProxyFilter extends OncePerRequestFilter {

    public static final String RESOLVED_CLIENT_IP_ATTRIBUTE =
        "resolvedClientIp";

    @Override
    protected void doFilterInternal(
        HttpServletRequest request,
        HttpServletResponse response,
        FilterChain filterChain
    ) throws ServletException, IOException {

        String resolvedIp = resolveClientIp(request);
        request.setAttribute(RESOLVED_CLIENT_IP_ATTRIBUTE, resolvedIp);

        filterChain.doFilter(request, response);
    }

    /**
     * 実クライアントIP解決
     *
     * Trusted ProxyからのリクエストでX-Forwarded-Forヘッダーが
     * 存在する場合、最初のIPを抽出（元のクライアント）
     * それ以外はremote addressを返却
     */
    private String resolveClientIp(HttpServletRequest request) {
        String remoteAddr = request.getRemoteAddr();

        TrustedProxyConfig config = systemConfig.trustedProxies();

        if (!config.isEnabled()) {
            return remoteAddr;
        }

        if (!config.isTrustedProxy(remoteAddr)) {
            return remoteAddr;
        }

        // X-Forwarded-Forから実IPを抽出
        // ...
    }
}
```

## システム設定

`idp-server-platform/system/` 内:

```java
public class SystemConfiguration {
    SsrfProtectionConfig ssrfProtection;
    TrustedProxyConfig trustedProxies;

    public SsrfProtectionConfig ssrfProtection() {
        return ssrfProtection;
    }

    public TrustedProxyConfig trustedProxies() {
        return trustedProxies;
    }
}
```

### SSRF保護設定

```java
public class SsrfProtectionConfig {
    boolean enabled;
    Set<String> bypassHosts;      // 開発用バイパス
    Set<String> allowedHosts;     // Allowlist（OWASP推奨）
}
```

### Trusted Proxy設定

```java
public class TrustedProxyConfig {
    boolean enabled;
    List<String> trustedProxyCidrs;  // CIDR形式（例: 10.0.0.0/8）

    public boolean isTrustedProxy(String ipAddress) {
        // IPアドレスがTrusted Proxy CIDRに含まれるか確認
    }
}
```

## E2Eテスト

```
e2e/src/tests/
└── (システム設定関連テストは各機能のセキュリティテスト内で検証)
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-platform:compileJava

# テスト
cd e2e && npm test
```

## トラブルシューティング

### SSRF保護でブロックされる
- 開発環境: bypassHostsにlocalhost, mock-serviceを追加
- 本番環境: allowedHostsを設定（OWASP推奨）

### クラウドメタデータサービスへのアクセス
- 169.254.169.254はデフォルトでブロック
- AWS/GCP/Azureメタデータサービスへのアクセスは禁止

### Trusted Proxy設定が動作しない
- TrustedProxyConfig.enabledがtrueか確認
- リクエストのremote addressがtrustedProxyCidrsに含まれるか確認
- CIDR形式が正しいか確認（例: 10.0.0.0/8）

### X-Forwarded-Forが信頼されない
- Trusted Proxyからのリクエストか確認
- TrustedProxyFilterが動作しているか確認
- request.getAttribute("resolvedClientIp")でIPを取得
