# 76-webgl-ws-polling-bridge

Status: ACTIVE
AppliesTo: v10
Type: Policy / Contract

---

## Purpose

WebGL에서 WebSocket 이벤트를 **폴링(Polling) 기반**으로 전달하는 `.jslib` ↔ C# 간 계약을 정의한다.

이 문서는 **인터페이스 계약**이 핵심이며, 구현 코드가 정답이다.

---

## Hard Rules

1. **SendMessage/콜백 기반 설계 금지**
   - WebGL에서 WebSocket 이벤트를 C#으로 전달할 때 `SendMessage` 콜백을 사용하지 않는다.
   - 모든 이벤트는 `WS_PollEvent`로만 소비한다.

2. **이벤트 소비는 Tick()에서만 수행**
   - `Tick()` 호출 시에만 이벤트 큐를 drain한다.
   - 메인 스레드 보장.

3. **이벤트 처리량 제한 필수**
   - 한 `Tick()`에서 최대 N개의 이벤트만 처리한다.
   - 무한 루프/폭주 방지.

---

## Function Contract (C# → JS)

아래 함수들은 `.jslib`에서 구현하고, C#에서 `[DllImport("__Internal")]`로 호출한다.

### WS_Connect

```csharp
[DllImport("__Internal")]
private static extern int WS_Connect(string url, string subProtocolsJson);
```

- **설명**: WebSocket 연결 시작
- **파라미터**:
  - `url`: WebSocket URL (wss:// 필수, WebGL에서 ws:// 금지)
  - `subProtocolsJson`: sub-protocol 배열의 JSON 문자열 (nullable, 예: `["devian.v1"]`)
- **리턴**: `socketId` (0 이상), 실패 시 음수

### WS_GetState

```csharp
[DllImport("__Internal")]
private static extern int WS_GetState(int socketId);
```

- **설명**: WebSocket 연결 상태 조회
- **리턴**: `0=CONNECTING`, `1=OPEN`, `2=CLOSING`, `3=CLOSED`, `-1=INVALID`

### WS_SendBinary

```csharp
[DllImport("__Internal")]
private static extern int WS_SendBinary(int socketId, IntPtr ptr, int len);
```

- **설명**: 바이너리 메시지 전송
- **파라미터**:
  - `ptr`: WASM heap 상의 버퍼 포인터 (`GCHandle.Alloc(Pinned)`)
  - `len`: 버퍼 길이
- **리턴**: `0=성공`, 음수=실패

### WS_Close

```csharp
[DllImport("__Internal")]
private static extern void WS_Close(int socketId, int code, string reason);
```

- **설명**: WebSocket 종료 요청
- **파라미터**:
  - `code`: 종료 코드 (예: 1000)
  - `reason`: 종료 사유 (nullable)

### WS_PollEvent

```csharp
[DllImport("__Internal")]
private static extern int WS_PollEvent(
    int socketId,
    out int eventType,
    out int code,
    out IntPtr dataPtr,
    out int dataLen,
    out IntPtr messagePtr);
```

- **설명**: 이벤트 큐에서 다음 이벤트를 가져온다
- **리턴**:
  - `0` = 이벤트 없음
  - `1` = 이벤트 있음 (출력값 유효)
- **출력 파라미터**:
  - `eventType`: 이벤트 타입 (아래 참조)
  - `code`: CLOSE 이벤트의 종료 코드, ERROR/MESSAGE에서는 0
  - `dataPtr`: MESSAGE 이벤트의 바이너리 데이터 포인터 (_malloc 할당)
  - `dataLen`: MESSAGE 이벤트의 데이터 길이
  - `messagePtr`: ERROR/CLOSE 이벤트의 UTF8 문자열 포인터 (_malloc 할당, nullable)

### WS_FreeBuffer

```csharp
[DllImport("__Internal")]
private static extern void WS_FreeBuffer(IntPtr ptr);
```

- **설명**: MESSAGE 이벤트의 `dataPtr` 해제
- **필수**: MESSAGE 수신 후 반드시 호출

### WS_FreeString

```csharp
[DllImport("__Internal")]
private static extern void WS_FreeString(IntPtr ptr);
```

- **설명**: ERROR/CLOSE 이벤트의 `messagePtr` 해제
- **필수**: messagePtr이 non-null이면 반드시 호출

---

## EventType Enum

| 값 | 이름 | 설명 |
|----|------|------|
| 0 | NONE | 이벤트 없음 (리턴값 0과 동일) |
| 1 | OPEN | 연결 성공 |
| 2 | CLOSE | 연결 종료 (code, messagePtr 유효) |
| 3 | ERROR | 오류 발생 (messagePtr 유효) |
| 4 | MESSAGE | 바이너리 메시지 수신 (dataPtr, dataLen 유효) |

---

## WS_PollEvent 사용 패턴

```csharp
// Tick() 내부
const int MaxEventsPerTick = 64;

for (int i = 0; i < MaxEventsPerTick; i++)
{
    int result = WS_PollEvent(_socketId, out int eventType, out int code,
                              out IntPtr dataPtr, out int dataLen, out IntPtr messagePtr);
    if (result == 0)
        break; // 이벤트 없음

    switch (eventType)
    {
        case 1: // OPEN
            EnqueueDispatch(() => OnOpen?.Invoke());
            break;

        case 2: // CLOSE
            string reason = messagePtr != IntPtr.Zero
                ? Marshal.PtrToStringUTF8(messagePtr)
                : "";
            EnqueueDispatch(() => OnClose?.Invoke((ushort)code, reason));
            if (messagePtr != IntPtr.Zero) WS_FreeString(messagePtr);
            break;

        case 3: // ERROR
            string errorMsg = messagePtr != IntPtr.Zero
                ? Marshal.PtrToStringUTF8(messagePtr)
                : "Unknown error";
            EnqueueDispatch(() => OnError?.Invoke(new Exception(errorMsg)));
            if (messagePtr != IntPtr.Zero) WS_FreeString(messagePtr);
            break;

        case 4: // MESSAGE
            // ArrayPool로 복사 후 core.OnFrame 호출
            var buffer = ArrayPool<byte>.Shared.Rent(dataLen);
            Marshal.Copy(dataPtr, buffer, 0, dataLen);
            _core.OnFrame(_sessionId, buffer.AsSpan(0, dataLen));
            ArrayPool<byte>.Shared.Return(buffer);
            WS_FreeBuffer(dataPtr);
            break;
    }
}
```

---

## DoD (Hard Gate)

- [ ] `WS_PollEvent`가 유일한 이벤트 소비 경로이다 (SendMessage 없음)
- [ ] MESSAGE 수신 후 `WS_FreeBuffer(dataPtr)` 호출됨
- [ ] ERROR/CLOSE 수신 후 messagePtr이 non-null이면 `WS_FreeString(messagePtr)` 호출됨
- [ ] 한 Tick에서 처리하는 이벤트 개수에 상한이 있음

---

## Reference

- 메모리 규칙: [77-webgl-jslib-memory-rules](../77-webgl-jslib-memory-rules/SKILL.md)
- WebSocket 클라이언트: [72-network-ws-client](../72-network-ws-client/SKILL.md)
- Transport Adapter: [70-ws-transport-adapter](../70-ws-transport-adapter/SKILL.md)
