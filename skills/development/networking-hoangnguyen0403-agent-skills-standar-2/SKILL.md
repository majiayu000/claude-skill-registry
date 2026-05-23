---
name: iOS Networking
description: Standards for URLSession, Alamofire, and API communication.
metadata:
  labels: [ios, networking, urlsession, alamofire, codable]
  triggers:
    files: ['**/*Service.swift', '**/*API.swift', '**/*Client.swift']
    keywords: [URLSession, Alamofire, Moya, URLRequest, URLComponents, Codable]
---

# iOS Networking Standards

## **Priority: P0**

## Implementation Guidelines

### URLSession (Native)

- **Tasks**: Use `dataTaskPublisher` (Combine) or `data(for:delegate:)` (async/await).
- **Configuration**: Use `URLSessionConfiguration.default` for standard tasks and `ephemeral` for private browsing/clearing cache.
- **Request Building**: Use `URLComponents` and `URLQueryItem` to build URLs safely. Never use string interpolation for parameters.

### Alamofire (Standard Third-Party)

- **Session**: Maintain a singleton or DI-injected `Session` instance.
- **Request**: Use `.validate()` to automatically check for 200..299 status codes.
- **Encoding**: Use `JSONParameterEncoder.default` for body parameters.

### Best Practices

- **Codable**: Use `Codable` for JSON mapping. Prefer `snake_case` to `camelCase` decoding strategies if the API follows snake_case.
- **Retriers & Adapters**: Use `RequestInterceptor` for adding Auth headers (Bearer) and handling token refresh (401).
- **SSL Pinning**: Implement using `ServerTrustManager` for production security.

## Anti-Patterns

- **Main Thread completion**: `**No UI updates in background task**: Always jump to Main thread/MainActor.`
- **Raw Mapping**: `**No manual JSONSerialization**: Use Codable.`
- **Missing Timeout**: `**No indefinite wait**: Always set a reasonable timeoutInterval (e.g., 30s).`

## References

- [Native & Alamofire Implementation](references/implementation.md)
