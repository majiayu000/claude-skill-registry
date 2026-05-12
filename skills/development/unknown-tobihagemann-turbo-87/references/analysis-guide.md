# Analysis Guide

Detailed guidance for analyzing different application types, platforms, and special concerns. Read the section relevant to your codebase.

## Contents
- Application type lenses
- Platform-specific considerations
- Protocol implementations
- Native code / FFI boundaries
- Implicit network behavior
- Cryptographic code
- Dependency boundary analysis
- STRIDE completeness check
- Severity calibration by context

## Application Type Lenses

The application type determines which attack surfaces to prioritize. Apply the relevant lens after identifying the codebase type.

### Web Service / API

Focus areas:
- **Authentication flow**: OIDC, sessions, API keys, token lifecycle, token storage
- **Authorization enforcement**: per-route, per-resource, role-based checks. Missing or incorrect annotations on new endpoints are critical.
- **Input validation**: every API boundary — path params, query params, JSON bodies, headers, file uploads
- **Injection**: SQL (parameterized queries?), NoSQL, command injection, template injection
- **Client-side security**: CSP, XSS prevention (template auto-escaping, no raw HTML rendering), CSRF resistance, cookie flags
- **SSRF**: any place where user input influences outbound requests (URLs, hostnames, redirect targets)
- **External integrations**: HTTP clients calling third-party services, secret management for API keys
- **Deployment security**: security headers, CORS, TLS termination, dev/prod separation, debug endpoints
- **Rate limiting and availability**: explicit rate limiting or reliance on infrastructure

XSS severity depends on what can be stolen: if browser-stored crypto keys or auth tokens are accessible, XSS is critical.

### Desktop Application

Focus areas:
- **File handling**: path validation, symlink following, temp file creation, permissions
- **Credential and key storage**: OS keychain usage, memory handling, zeroization
- **IPC**: named pipes, Unix domain sockets, shared memory, clipboard
- **Update mechanism**: signature verification, TLS, rollback protection
- **Mounting / filesystem exposure**: what is accessible when a vault/volume is mounted, interface binding (loopback vs all interfaces)
- **Plugin/extension loading**: ServiceLoader, dynamic imports, plugin directories with full app privileges
- **Local attack surface**: malicious files opened by the app, crafted configuration, environment variables

Severity adjustment: local attacker risks are typically lower than remote because local access often implies broader compromise.

### Library / SDK

Focus areas:
- **Public API surface**: what functions are exported, what inputs they accept, what invariants they maintain
- **Default security posture**: are defaults safe? Dangerous options should require explicit opt-in.
- **API misuse scenarios**: how can callers defeat the library's protections by using the API incorrectly? Rate misuse severity by how easy the mistake is AND how severe the consequences are. A footgun behind an explicit flag is less severe than a dangerous default.
- **Error handling**: do errors leak sensitive information? Are they distinguishable in ways that enable oracles?
- **Extension points**: ServiceLoader, plugin APIs, callback registration — what happens if an attacker controls these?
- **Dependency trust**: what does the library assume about its own dependencies?

Key principle: for libraries, the API surface IS the primary trust boundary. The three-tier input classification (attacker/operator/developer) is essential because the library cannot enforce how callers use it.

### CLI Tool

Focus areas:
- **Argument and stdin parsing**: injection risks, shell metacharacters
- **Filesystem interactions**: path traversal, race conditions (TOCTOU), symlink following
- **Environment variable handling**: secrets in env, PATH manipulation
- **Output handling**: secrets in stdout/stderr, piped to untrusted destinations
- **Privilege requirements**: does it need elevated privileges? How does it drop them?
- **Installer/setup**: privilege escalation during installation, fixed vs user-controlled paths

### Mobile Application

Focus areas:
- **Data at rest**: is local storage encrypted? SharedPreferences vs Keystore (Android), UserDefaults vs Keychain (iOS)
- **IPC**: intents, URL schemes, deep links, content providers, broadcast receivers
- **Certificate pinning**: custom TLS validation, ATS exceptions
- **Exported components**: activities, services, receivers marked as exported (Android)
- **Biometric auth bypass**: can biometric checks be skipped by modifying local state?
- **Clipboard and screenshot exposure**: does the app expose sensitive data through clipboard or allow screenshots of sensitive screens?

## Platform-Specific Considerations

Detect the platform from build files and framework imports, then apply the relevant lens.

### macOS / iOS
- **Sandbox status**: check entitlements for `com.apple.security.app-sandbox`. An unsandboxed app has wider blast radius.
- **Keychain usage**: prefer Keychain over file-based credential storage
- **App Transport Security**: check for HTTP exceptions in Info.plist
- **Hardened Runtime / code signing**: check entitlements
- **XPC services**: trust boundaries between XPC components
- **Sparkle / update mechanisms**: update feed integrity, signature verification

### Android
- **Exported components**: check AndroidManifest.xml for `exported="true"` on activities, services, receivers, providers
- **Permission model**: runtime vs install-time permissions, dangerous permissions
- **Android Keystore vs SharedPreferences**: secrets should use Keystore
- **WebView**: JavaScript bridge exposure, loadUrl with untrusted input
- **Intent handling**: validate incoming intents, check for intent redirection

### Server / Linux
- **Privilege level**: running as root vs unprivileged user, Linux capabilities
- **Container isolation**: namespace boundaries, mounted volumes, network policies
- **Filesystem permissions**: sensitive files (credentials, keys) should be 0600/0640
- **Systemd socket activation**: exposed ports, binding addresses

### Web / Electron
- **Origin model**: same-origin policy, CSP configuration
- **Node integration** (Electron): is Node.js accessible from renderer? `nodeIntegration`, `contextIsolation` settings
- **Cookie security**: HttpOnly, Secure, SameSite flags
- **CORS policy**: overly permissive origins

## Protocol Implementations

When the codebase implements or speaks a network protocol:

1. **Map the protocol stack layer by layer**: transport → framing → authentication → application messages. Each layer that processes attacker-controlled input before higher layers validate it is a potential attack surface.

2. **Flag these patterns**:
   - Opportunistic encryption (STARTTLS-style "upgrade if available") — always a downgrade risk
   - Server-provided URLs or redirect targets used without validation
   - Peer-to-peer negotiation where either side's parameters control the connection
   - Any place where a remote party's response changes the security properties of the session
   - Protocol version negotiation with fallback to weaker versions

3. **State machines**: connection lifecycle management (handshake → upgrade → auth → steady-state). Look for states where security properties are not yet established, but data is already processed.

## Native Code / FFI Boundaries

Search for FFI boundaries. The blast radius of bugs in native code is higher (memory corruption, not just logic errors).

**How to find them:**
- Swift: `import` of C modules, bridging headers, `UnsafePointer`/`UnsafeBufferPointer`, `withUnsafe*` closures
- Kotlin/JVM: JNI, `System.loadLibrary`, native method declarations
- Python: `ctypes`, `cffi`, Cython `.pyx` files, C extension modules
- Rust: `unsafe` blocks wrapping FFI calls, `extern "C"` blocks
- Node.js: native addons (`.node`), `node-gyp` config, N-API

**For each FFI boundary, assess:**
- Is the native library processing untrusted input? (If yes, this is a significant attack surface)
- Are safety features configured? (Entity expansion limits, buffer size caps, sandboxing)
- Do callers validate inputs before passing them to native code?
- What is the native library's general CVE history? (Note as risk factor)

## Implicit Network Behavior

Trace every path from "remote data arrives" to "outbound network request is made." Any path without an explicit user consent gate is an attack surface.

**Common patterns:**
- URL extraction from messages that triggers automatic metadata/preview fetches
- Framework auto-fetch behavior (LPMetadataProvider, AsyncImage, OEmbed, OpenGraph resolvers)
- Avatar/profile picture loading from user-provided URLs
- DNS lookups triggered by untrusted hostnames (SRV records, MX lookups)
- Webhook/callback URLs where a remote party specifies where the app sends data

**Assess for each:**
- IP disclosure to attacker-controlled servers
- SSRF potential (can it hit localhost or internal services?)
- Volume/DoS (can one message trigger many fetches?)
- Scheme restriction (limited to HTTPS, or can `file://`, `ftp://` be triggered?)

## Cryptographic Code

When the codebase performs cryptographic operations:

1. **Map the key hierarchy**: master key → derived keys → per-operation keys. Note how key material flows and where blast radius is limited.

2. **Trace nonce/IV management**: nonce reuse in AES-GCM or AES-CTR is catastrophic. Verify nonces come from a strong source and are never reused.

3. **Check authentication**: is authenticated encryption used (AES-GCM, ChaCha20-Poly1305)? Are MAC comparisons constant-time? Can authentication be skipped via API flags?

4. **Assess key protection**: how are keys stored at rest? Scrypt/Argon2 parameters for password-derived keys? Key zeroization after use?

5. **Identify designed leakage**: deterministic encryption leaks equality. Chunked encryption leaks file size. Note these as inherent properties, not bugs.

6. **Side-channel awareness**: constant-time comparisons for secrets, memory zeroization attempts, RNG quality.

Do not perform deep novel cryptanalysis. Identify which primitives are used, verify they are applied correctly for their guarantees, and flag known dangerous patterns.

## Dependency Boundary Analysis

When the codebase delegates security-critical operations to an external library:

1. **State the trust assumption**: name the dependency and what it is trusted to do. Example: "cryptolib implements authenticated encryption and key handling correctly."

2. **Analyze the integration boundary**: does this codebase pass correct inputs? Handle error returns? Avoid misuse patterns (nonce reuse, ignoring auth failures)?

3. **Do not audit the dependency's internals**. Focus on how this codebase uses it.

4. **Flag unverified assumptions**: when the assumption is hard to verify (e.g., "SecureRandom is strong and available"), note conditions under which it could fail.

## STRIDE Completeness Check

After drafting the threat model, verify coverage against STRIDE. You do not need to organize by STRIDE, but every applicable category should appear somewhere:

- **Spoofing**: Can an attacker impersonate a user, service, or component?
- **Tampering**: Can an attacker modify data in transit or at rest?
- **Repudiation**: Can actions be performed without accountability?
- **Information disclosure**: Can secrets, data, or metadata leak?
- **Denial of service**: Can availability be degraded?
- **Elevation of privilege**: Can an attacker gain capabilities beyond their trust level?

If a category is not represented in the threat model, either add coverage or note it in the "less relevant" paragraph with a reason.

## Severity Calibration by Context

Severity depends on the intersection of attacker position and impact:

| Impact | Remote Unauth | Remote Auth | Local Unpriv | Local Admin |
|---|---|---|---|---|
| Key/secret compromise | Critical | Critical | High | Medium |
| Code execution | Critical | Critical | High | Medium |
| Bulk data exposure | Critical | High | Medium | Low |
| Limited data exposure | High | Medium | Low | Low |
| Denial of service | Medium | Medium | Low | Low |
| Metadata leakage | Medium | Low | Low | Low |

**Adjustments by application type:**
- **Web services**: remote unauthenticated attacks weight highest. XSS is critical when it can steal crypto keys or auth tokens.
- **Desktop apps**: account for the local attacker model (lower baseline). Issues requiring OS-level compromise are medium at most.
- **Libraries**: rate severity relative to the worst realistic caller context. Unsafe defaults affect every consumer.
- **Mobile apps**: consider the device theft model. Data at rest severity depends on encryption status.

Always explain the calibration rationale in section 4. Generic CVSS-style scoring without context is not useful.
