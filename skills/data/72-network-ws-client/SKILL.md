# 72-network-ws-client

Status: ACTIVE  
AppliesTo: v10  
Type: Policy / Requirements

---

## Purpose

Devian 런타임에 **WebSocket 기반 클라이언트 런타임**을 추가한다.

이 SKILL은 정책/요구사항/설계 의도를 정의한다. 구현 및 공개 API는 코드가 정답이며, 여기의 시그니처/예시는 참고용이다.

> **Namespace 정책:** 모든 타입은 `namespace Devian` 단일을 사용한다.
> 네트워크 계열 public API는 `Net` 접두사로 명확화한다.

---

## Scope

### 목표 (In Scope)

- `NetWsClient`: WebSocket 클라이언트 (sync public API)
  - **Non-WebGL**: background threads 기반
  - **WebGL**: thread 없음, `Tick()` 기반 폴링
- `NetClient`: 프레임 수신 → 디스패치 라우팅
- `INetRuntime`: opcode 기반 디스패치 인터페이스 (이미 Net 포함, 유지)
- `NetFrameV1`: 프레임 포맷 파서 (`[opcode:int32LE][payload...]`)

### 비목표 (Out of Scope)

- TypeScript 변경 없음
- HTTP/RPC는 별도 SKILL에서 다룸
- 기존 `INetPacketSender`, `NetPacketEnvelope` API 변경 없음

---

## Relationship with Devian

이 SKILL은 `namespace Devian`에 **네트워크 기능**을 제공한다.

| 기존 | 추가 (이 SKILL) |
|------|----------------|
| `INetPacketSender` | 변경 없음 |
| `NetPacketEnvelope` | 변경 없음 |
| - | `NetFrameV1` |
| - | `INetRuntime` |
| - | `NetClient` |
| - | `NetWsClient` |

---

## File Paths (Reference)

```
framework-cs/module/Devian/src/Net/
├── NetFrameV1.cs
├── INetRuntime.cs
├── NetClient.cs
└── Transports/
    └── NetWsClient.cs
```

---

## API Signatures (Reference)

> **Note:** 아래는 이해를 돕기 위한 참고 예시이며, 최종 시그니처/공개 API는 코드가 정답이다.  
> 코드 변경 시 이 문서를 'SSOT'로 맞추지 않는다. 필요하면 문서를 참고 수준으로 갱신한다.

### NetFrameV1

```csharp
namespace Devian
{
    public static class NetFrameV1
    {
        /// <summary>
        /// Frame format: [opcode:int32LE][payload...]
        /// </summary>
        public static bool TryParse(
            ReadOnlySpan<byte> frame,
            out int opcode,
            out ReadOnlySpan<byte> payload);

        /// <summary>
        /// Build frame into destination buffer.
        /// Returns bytes written.
        /// </summary>
        public static int Build(
            Span<byte> destination,
            int opcode,
            ReadOnlySpan<byte> payload);

        /// <summary>
        /// Calculate total frame size.
        /// </summary>
        public static int CalculateSize(int payloadLength);
    }
}
```

### INetRuntime

```csharp
namespace Devian
{
    public interface INetRuntime
    {
        /// <summary>
        /// Dispatch inbound message by opcode.
        /// Returns true if handled, false otherwise.
        /// </summary>
        bool TryDispatchInbound(int sessionId, int opcode, ReadOnlySpan<byte> payload);
    }
}
```

### NetClient

```csharp
namespace Devian
{
    public sealed class NetClient
    {
        public NetClient(INetRuntime runtime);

        /// <summary>
        /// Called by transport when a complete frame is received.
        /// Parses frame and dispatches to runtime.
        /// </summary>
        public void OnFrame(int sessionId, ReadOnlySpan<byte> frame);
    }
}
```

### NetWsClient

```csharp
namespace Devian
{
    public sealed class NetWsClient : IDisposable
    {
        public NetWsClient(NetClient core, int sessionId = 0);

        public bool IsOpen { get; }

        public event Action? OnOpen;
        public event Action<ushort, string>? OnClose;
        public event Action<Exception>? OnError;

        /// <summary>
        /// Synchronously connect and start background recv/send threads.
        /// </summary>
        public void Connect(string url, string[]? subProtocols = null);

        /// <summary>
        /// Synchronously enqueue frame for sending.
        /// </summary>
        public void SendFrame(ReadOnlySpan<byte> frame);

        /// <summary>
        /// Request graceful close.
        /// </summary>
        public void Close();

        /// <summary>
        /// Process dispatch queue on calling thread (Unity main thread).
        /// WebGL에서는 WS_PollEvent drain도 수행한다.
        ///
        /// 문서 표준 호출명: Tick()
        /// Update()는 alias로 유지 (레거시, Unity MonoBehaviour.Update 혼동 방지)
        /// </summary>
        public void Tick();

        /// <summary>
        /// Alias for Tick(). 레거시 호환용, 사용 비권장.
        /// Unity MonoBehaviour.Update()와 혼동 금지.
        /// </summary>
        [Obsolete("Use Tick() instead")]
        public void Update();

        public void Dispose();
    }
}
```

---

## Frame Format (NetFrameV1)

```
+------------------+------------------+
| opcode (4 bytes) | payload (N bytes)|
| int32 LE         | raw bytes        |
+------------------+------------------+
```

- **opcode**: 32-bit signed integer, little-endian
- **payload**: 0 or more bytes

---

## Close → OnClose 보장 (Hard Rule)

**로컬 Close() 호출 시 OnClose 이벤트가 반드시 발생해야 한다.**

- 서버 응답 여부와 무관하게 OnClose 발생 필수
- RecvLoop blocking 중이어도 OnClose 발생 필수
- CancellationToken.None으로 무한 대기 금지

**위반 시 FAIL:**
- Close() 후 OnClose 안 오면 FAIL
- 서버가 응답 안 해도 일정 시간 내 OnClose 와야 함

---

## Performance / GC Rules (Hard Rules)

### MUST

1. **ToArray() 금지**: 수신/송신 경로에서 `ToArray()` 호출 금지
2. **ArrayPool 기반 버퍼 재사용**:
   - 수신: `ArrayPool<byte>.Shared.Rent()` → 누적 → 처리 후 재사용
   - 송신: caller span을 rented buffer에 복사 → 전송 후 `Return()`
3. **Send는 sync enqueue (Non-WebGL)**: `SendFrame()`은 즉시 반환, 실제 전송은 send thread
4. **Receive는 pool buffer 누적 (Non-WebGL)**: `EndOfMessage`에서만 core로 전달

> **WebGL Note:** 이 문서에서 "send/recv thread"는 **Non-WebGL**을 의미한다. WebGL에서는 스레드가 없으며, 수신은 **콜백 전달이 아니라 폴링 전달**로 수행된다. **ToArray 금지, ArrayPool 재사용, 핫 경로 alloc 금지**는 동일하게 적용된다. ptr/len free 규칙은 [77-webgl-jslib-memory-rules](../77-webgl-jslib-memory-rules/SKILL.md)에 위임한다.

### MUST NOT

1. public API에 `async` 노출 금지 (`Connect`, `SendFrame`, `Close`는 sync)
2. 핫 경로에서 allocation 금지

---

## Threading Model

```
┌─────────────────┐
│   Main Thread   │
│  (Unity Update) │
│                 │
│  Tick() ────────┼──→ dispatch queue drain + (WebGL: WS_PollEvent drain)
│  SendFrame() ───┼──→ send queue enqueue
│  Connect()      │
│  Close()        │
└─────────────────┘
         │
         ▼ (Non-WebGL only)
┌─────────────────┐     ┌─────────────────┐
│   Send Thread   │     │   Recv Thread   │
│                 │     │                 │
│  dequeue ───────┼──→  │  ReceiveAsync   │
│  SendAsync      │     │  ──→ OnFrame()  │
└─────────────────┘     └─────────────────┘
```

> **Tick() vs Update() 표준화:**
> - `Tick()` = dispatch queue drain + (WebGL이면 WS_PollEvent drain)
> - `Update()` = `Tick()` alias (레거시, Unity MonoBehaviour.Update 혼동 방지 목적상 사용 비권장)

### WebGL Exception (`UNITY_WEBGL && !UNITY_EDITOR`)

WebGL에서는 브라우저 제약으로 **스레드 기반 send/recv 루프를 사용하지 않는다**.

**폴링 기반 모델 (콜백/SendMessage 금지):**

- `.jslib`가 이벤트 큐를 유지
- `Tick()`에서 `WS_PollEvent`를 최대 N개까지 drain하여:
  - `OPEN/CLOSE/ERROR` → 내부 dispatch queue에 enqueue
  - `MESSAGE(ptr, len)` → `Marshal.Copy` → `core.OnFrame(sessionId, frame)`
- **송신**: `ArrayPool<byte>` + `GCHandle.Alloc(Pinned)` → `WS_SendBinary(ptr,len)` (ToArray 없음)
- **수신**: `.jslib`가 `_malloc`으로 WASM heap에 복사 → C#이 `Marshal.Copy`로 `ArrayPool<byte>`에 복사 후 처리 → `WS_FreeBuffer(ptr)`로 해제

**메모리 규칙:**
- ptr/len/문자열 Free 규칙은 [77-webgl-jslib-memory-rules](../77-webgl-jslib-memory-rules/SKILL.md) 참조

**계약 정본:**
- [76-webgl-ws-polling-bridge](../76-webgl-ws-polling-bridge/SKILL.md)

---

## Event Dispatch

| Event | Parameters | 설명 |
|-------|------------|------|
| `OnOpen` | - | 연결 성공 |
| `OnClose` | `ushort code, string reason` | 연결 종료 |
| `OnError` | `Exception ex` | 오류 발생 |

- 이벤트는 **dispatch queue**를 통해 `Tick()`에서 실행 (Unity 호환)
- `Update()`는 `Tick()` alias (레거시 호환)
- Unity가 아닌 환경에서는 즉시 호출로 변경 가능

---

## Build Target

- `netstandard2.1` 유지
- `ClientWebSocket`이 누락되면 `System.Net.WebSockets.Client` 패키지 조건부 추가 가능
- 기본은 패키지 추가 없이 시도

---

## Reference

- Parent Module: `Devian` (단일 런타임 모듈, `namespace Devian`)
- Related: `skills/devian-core/10-core-runtime/SKILL.md`
- WebGL 폴링 계약: [76-webgl-ws-polling-bridge](../76-webgl-ws-polling-bridge/SKILL.md)
- WebGL 메모리 규칙: [77-webgl-jslib-memory-rules](../77-webgl-jslib-memory-rules/SKILL.md)
