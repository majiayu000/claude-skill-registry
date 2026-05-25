# 73-network-http-rpc-client

Status: ACTIVE  
AppliesTo: v10  
Type: Policy / Requirements

---

## Purpose

Devian 런타임 모듈(단일 모듈)의 Network 기능에 **binary→base64 단일 파라미터 POST RPC 클라이언트**를 추가한다.

이 SKILL은 정책/요구사항/설계 의도를 정의한다. 구현 및 공개 API는 코드가 정답이며, 예시는 참고용이다.

> **Namespace 정책:** 모든 타입은 `namespace Devian` 단일을 사용한다.
> 네트워크 계열 public API는 `Net` 접두사로 명확화한다.

---

## Scope

### 목표 (In Scope)

- `NetHttpRpcClient`: sync API HTTP RPC 클라이언트
- base64 single-param POST RPC 규약
- `application/x-www-form-urlencoded` 전송

### 비목표 (Out of Scope)

- REST 규격 지원 X
- TypeScript 변경 X
- WebSocket과의 통합/공유 큐는 다음 단계
- JSON 응답 파싱 (기본 미지원)

---

## Module Structure

> Devian C# 런타임은 단일 모듈(`Devian.csproj`)로 통합되어 있다.
> **모든 타입은 `namespace Devian`에 위치한다.** (분리된 하위 네임스페이스 금지)

```
framework-cs/module/Devian/
└── src/
    └── Net/
        └── Transports/
            └── NetHttpRpcClient.cs
```

---

## RPC Wire Protocol

### Request

| 항목 | 값 |
|------|-----|
| Method | `POST` |
| Content-Type | `application/x-www-form-urlencoded; charset=utf-8` |
| Body | `{paramName}={urlEncoded(base64(requestBinary))}` |
| Default paramName | `"p"` |

**Flow:**
```
requestBinary (byte[])
    ↓ Convert.ToBase64String()
base64 string
    ↓ Uri.EscapeDataString()
urlEncoded string
    ↓ "{paramName}={value}"
form-urlencoded body
```

### Response

| 항목 | 값 |
|------|-----|
| Expected | Plain text base64 (no JSON wrapper) |
| Decoding | `Convert.FromBase64String(text.Trim())` |

**Flow:**
```
HTTP Response Body (text)
    ↓ Trim()
trimmed base64 string
    ↓ Convert.FromBase64String()
responseBinary (byte[])
```

> **Note:** JSON 응답 `{"p":"..."}` 형태는 기본 미지원. 필요시 옵션 확장 가능.

---

## API Signatures (Reference)

> **Note:** 아래는 이해를 돕기 위한 참고 예시이며, 최종 시그니처/공개 API는 코드가 정답이다.  
> 코드 변경 시 이 문서를 'SSOT'로 맞추지 않는다. 필요하면 문서를 참고 수준으로 갱신한다.

```csharp
namespace Devian
{
    /// <summary>
    /// HTTP RPC client with binary→base64 single-param POST protocol.
    /// All public APIs are synchronous.
    /// </summary>
    public sealed class NetHttpRpcClient : IDisposable
    {
        /// <summary>
        /// Creates a new NetHttpRpcClient.
        /// </summary>
        /// <param name="endpoint">RPC endpoint URI.</param>
        /// <param name="paramName">Form parameter name (default: "p").</param>
        /// <param name="http">Optional HttpClient (if null, creates internal one).</param>
        public NetHttpRpcClient(Uri endpoint, string paramName = "p", HttpClient? http = null);

        /// <summary>
        /// Synchronously call the RPC endpoint.
        /// Throws on HTTP error or decode failure.
        /// </summary>
        /// <param name="requestBinary">Request payload.</param>
        /// <returns>Response payload (decoded from base64).</returns>
        public byte[] Call(ReadOnlySpan<byte> requestBinary);

        /// <summary>
        /// Try to call the RPC endpoint without throwing.
        /// </summary>
        /// <param name="requestBinary">Request payload.</param>
        /// <param name="responseBinary">Response payload if successful.</param>
        /// <returns>True if successful, false otherwise.</returns>
        public bool TryCall(ReadOnlySpan<byte> requestBinary, out byte[] responseBinary);

        /// <summary>
        /// Dispose the client (releases HttpClient if owned).
        /// </summary>
        public void Dispose();
    }
}
```

---

## Hard Rules

### MUST

1. **Public API는 sync만 제공**: `Call()`, `TryCall()`, `Dispose()`
2. **async 노출 금지**: `Task`, `ValueTask`, `async` 키워드 금지 (public API)
3. **내부에서만 async 사용**: `SendAsync(...).GetAwaiter().GetResult()` 패턴
4. **HttpClient 주입 지원**: 외부 주입 시 Dispose하지 않음

### MUST NOT

1. public API에 `async` 도입
2. REST 규격이나 JSON 파싱 기본 구현
3. WebSocket 코드와 결합

---

## Error Policy

| 메서드 | 실패 시 |
|--------|---------|
| `Call()` | 예외 throw (`HttpRequestException`, `FormatException` 등) |
| `TryCall()` | `false` 반환, `responseBinary = Array.Empty<byte>()` |

---

## Usage Example

```csharp
using Devian;

// Create client
using var rpc = new NetHttpRpcClient(new Uri("https://api.example.com/rpc"));

// Prepare request
byte[] request = /* serialized protobuf or other binary */;

// Call (throws on error)
byte[] response = rpc.Call(request);

// Or try-call (no throw)
if (rpc.TryCall(request, out var resp))
{
    // handle resp
}
```

---

## Build Target

- `netstandard2.1` 유지
- 추가 NuGet 패키지 불필요 (`System.Net.Http`는 기본 포함)

---

## Reference

- Parent Module: `Devian` (단일 런타임 모듈, `namespace Devian`)
- Related: `skills/devian-core/72-network-ws-client/SKILL.md`
