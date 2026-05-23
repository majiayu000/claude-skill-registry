---
name: alamofire-patterns
description: "Expert Alamofire decisions for iOS/tvOS: when Alamofire adds value vs URLSession suffices, interceptor chain design trade-offs, retry strategy selection, and certificate pinning considerations. Use when designing network layer, implementing auth token refresh, or choosing between networking approaches. Trigger keywords: Alamofire, URLSession, interceptor, RequestAdapter, RequestRetrier, certificate pinning, Session, network layer, token refresh, retry"
version: "3.0.0"
---

# Alamofire Patterns — Expert Decisions

Expert decision frameworks for Alamofire choices. Claude knows Alamofire syntax — this skill provides judgment calls for when Alamofire adds value and how to design interceptor chains.

---

## Decision Trees

### Alamofire vs URLSession

```
What networking features do you need?
├─ Basic REST calls with JSON
│  └─ Modern URLSession is sufficient
│     async/await + Codable works well
│
├─ Complex authentication (token refresh, retry)
│  └─ Alamofire's RequestInterceptor shines
│     Built-in retry coordination
│
├─ Request/Response inspection and modification
│  └─ Does app need centralized logging/metrics?
│     ├─ YES → Alamofire EventMonitor
│     └─ NO → URLSession delegate suffices
│
├─ Certificate pinning
│  └─ Alamofire ServerTrustManager simplifies this
│     But URLSession can do it with delegates
│
└─ Multipart uploads with progress
   └─ Alamofire upload API is cleaner
      URLSession works but more boilerplate
```

**The trap**: Adding Alamofire for simple apps. If you just need basic GET/POST with JSON, URLSession's async/await API is clean enough and avoids a dependency.

### Interceptor Chain Design

```
What cross-cutting concerns exist?
├─ Just auth token injection
│  └─ Single RequestAdapter
│
├─ Auth + retry on 401
│  └─ Authenticator pattern (Alamofire's built-in)
│     Handles refresh token race conditions
│
├─ Multiple concerns (auth, logging, caching headers)
│  └─ Compositor pattern
│     Interceptor(adapters: [...], retriers: [...])
│
└─ Request modification varies by endpoint
   └─ Per-router interceptors
      Different Session instances or conditional logic
```

### Retry Strategy Selection

```
What kind of failure?
├─ Auth failure (401)
│  └─ Refresh token and retry once
│     Use Authenticator, not generic retry
│
├─ Transient network error
│  └─ Is request idempotent?
│     ├─ YES → Retry with exponential backoff (3 attempts)
│     └─ NO → Don't retry (may cause duplicates)
│
├─ Server error (5xx)
│  └─ Retry for 503 (Service Unavailable) only
│     Other 5xx usually won't recover
│
└─ Client error (4xx except 401)
   └─ Never retry
      Request is malformed, retry won't help
```

---

## NEVER Do

### Interceptor Design

**NEVER** refresh tokens in generic retry logic:
```swift
// ❌ Race condition — multiple requests refresh simultaneously
final class BadInterceptor: RequestRetrier {
    func retry(_ request: Request, for session: Session, dueTo error: Error, completion: @escaping (RetryResult) -> Void) {
        if response.statusCode == 401 {
            Task {
                try await refreshToken()  // 5 requests = 5 refresh calls!
                completion(.retry)
            }
        }
    }
}

// ✅ Use Alamofire's Authenticator — coordinates refresh across requests
final class TokenAuthenticator: Authenticator {
    func refresh(_ credential: OAuthCredential, for session: Session, completion: @escaping (Result<OAuthCredential, Error>) -> Void) {
        // Single refresh, all waiting requests resume
    }
}
```

**NEVER** create new Session instances per request:
```swift
// ❌ Loses connection pooling, memory inefficient
func fetchUser() async throws -> User {
    let session = Session()  // New session per call!
    return try await session.request(endpoint).serializingDecodable(User.self).value
}

// ✅ Reuse session — connection pooling, shared interceptors
final class NetworkManager {
    private let session: Session  // Single instance

    func fetchUser() async throws -> User {
        try await session.request(endpoint).serializingDecodable(User.self).value
    }
}
```

**NEVER** use Interceptor for endpoint-specific logic:
```swift
// ❌ Interceptor has complex conditionals
func adapt(_ urlRequest: URLRequest, ...) {
    if urlRequest.url?.path.contains("/admin") {
        // Add admin header
    } else if urlRequest.url?.path.contains("/public") {
        // Skip auth
    }
}

// ✅ Use Router pattern — endpoint defines its own needs
enum APIRouter: URLRequestConvertible {
    case adminEndpoint
    case publicEndpoint

    var requiresAuth: Bool {
        switch self {
        case .adminEndpoint: return true
        case .publicEndpoint: return false
        }
    }
}
```

### Session Configuration

**NEVER** disable SSL validation in production:
```swift
// ❌ Security vulnerability
let manager = ServerTrustManager(evaluators: [
    "api.production.com": DisabledTrustEvaluator()  // MITM vulnerable!
])

// ✅ Use DisabledTrustEvaluator only for development
#if DEBUG
let evaluator = DisabledTrustEvaluator()
#else
let evaluator = DefaultTrustEvaluator()
#endif
```

**NEVER** ignore response validation:
```swift
// ❌ Silently accepts 4xx/5xx as success
session.request(endpoint)
    .responseDecodable(of: User.self) { response in
        // May decode error response as User!
    }

// ✅ Always validate before decoding
session.request(endpoint)
    .validate(statusCode: 200..<300)
    .responseDecodable(of: User.self) { response in
        // Only called for 2xx responses
    }
```

### Retry Logic

**NEVER** retry non-idempotent requests:
```swift
// ❌ May create duplicate orders
func placeOrder() {
    session.request(APIRouter.createOrder)
        .validate()
        .response { response in
            if response.error != nil {
                self.placeOrder()  // Retry — may duplicate!
            }
        }
}

// ✅ Use idempotency keys for non-idempotent operations
func placeOrder(idempotencyKey: String) {
    session.request(APIRouter.createOrder(idempotencyKey: idempotencyKey))
    // Server uses key to prevent duplicates
}
```

**NEVER** retry immediately without backoff:
```swift
// ❌ Hammers server during outage
let retryPolicy = RetryPolicy(retryLimit: 5)  // Immediate retries

// ✅ Exponential backoff
let retryPolicy = RetryPolicy(
    retryLimit: 3,
    exponentialBackoffBase: 2,
    exponentialBackoffScale: 0.5
)
```

---

## Essential Patterns

### Authenticator with Refresh Coordination

```swift
final class OAuthAuthenticator: Authenticator {
    private let tokenStore: TokenStore
    private let refreshService: RefreshService

    func apply(_ credential: OAuthCredential, to urlRequest: inout URLRequest) {
        urlRequest.headers.add(.authorization(bearerToken: credential.accessToken))
    }

    func refresh(_ credential: OAuthCredential, for session: Session, completion: @escaping (Result<OAuthCredential, Error>) -> Void) {
        // Alamofire ensures only ONE refresh happens
        // Other 401 requests wait for this to complete
        refreshService.refresh(refreshToken: credential.refreshToken) { result in
            switch result {
            case .success(let tokens):
                let newCredential = OAuthCredential(
                    accessToken: tokens.accessToken,
                    refreshToken: tokens.refreshToken,
                    expiration: tokens.expiration
                )
                self.tokenStore.save(newCredential)
                completion(.success(newCredential))
            case .failure(let error):
                completion(.failure(error))
            }
        }
    }

    func didRequest(_ urlRequest: URLRequest, with response: HTTPURLResponse, failDueToAuthenticationError error: Error) -> Bool {
        response.statusCode == 401
    }

    func isRequest(_ urlRequest: URLRequest, authenticatedWith credential: OAuthCredential) -> Bool {
        urlRequest.headers["Authorization"] == "Bearer \(credential.accessToken)"
    }
}
```

### Compositor Interceptor

```swift
// Combine multiple adapters and retriers
let interceptor = Interceptor(
    adapters: [
        AuthAdapter(tokenStore: tokenStore),
        LoggingAdapter(),
        DeviceInfoAdapter()
    ],
    retriers: [
        AuthRetrier(authenticator: authenticator),
        NetworkRetrier(retryLimit: 3)
    ]
)

let session = Session(interceptor: interceptor)
```

### Certificate Pinning

```swift
let evaluators: [String: ServerTrustEvaluating] = [
    "api.yourapp.com": PinnedCertificatesTrustEvaluator(
        certificates: Bundle.main.af.certificates,
        acceptSelfSignedCertificates: false,
        performDefaultValidation: true,
        validateHost: true
    )
]

let session = Session(
    serverTrustManager: ServerTrustManager(evaluators: evaluators)
)
```

---

## Quick Reference

### When Alamofire Adds Value

| Feature | URLSession | Alamofire |
|---------|------------|-----------|
| Basic REST | ✅ Sufficient | Overkill |
| Token refresh with retry | Tricky | ✅ Authenticator |
| Certificate pinning | Possible | ✅ Cleaner API |
| Request/Response logging | Custom | ✅ EventMonitor |
| Multipart upload progress | Verbose | ✅ Clean API |
| Connection pooling | Automatic | Automatic |

### Interceptor Checklist

- [ ] Single Session instance shared across app
- [ ] Authenticator for token refresh (not generic retry)
- [ ] Exponential backoff for transient failures
- [ ] Only retry idempotent requests
- [ ] Validate responses before decoding
- [ ] Certificate pinning for production

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| New Session per request | Loses pooling | Share Session |
| DisabledTrustEvaluator in prod | Security hole | Proper pinning |
| Token refresh in RetryPolicy | Race condition | Use Authenticator |
| Retry without backoff | Server hammering | Exponential backoff |
| No .validate() call | Silent failures | Always validate |
| Complex conditionals in Interceptor | Wrong layer | Router pattern |
