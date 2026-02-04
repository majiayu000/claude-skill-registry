# 77-webgl-jslib-memory-rules

Status: ACTIVE
AppliesTo: v10
Type: Policy / Hard Rules

---

## Purpose

WebGL `.jslib` ↔ C# 간 ptr/len/문자열 메모리 수명 규칙을 **Hard Rule**로 고정한다.

이 규칙을 위반하면 **메모리 누수 또는 크래시**가 발생한다.

---

## Hard Rules

### 1. `.jslib`가 `_malloc`한 모든 버퍼는 C#이 반드시 Free 호출로 반환해야 함

| 이벤트 | 포인터 | Free 함수 |
|--------|--------|-----------|
| MESSAGE | `dataPtr` | `WS_FreeBuffer(dataPtr)` |
| ERROR/CLOSE | `messagePtr` | `WS_FreeString(messagePtr)` |

**위반 시**: WASM heap 메모리 누수 → 장기 실행 시 OOM 크래시

### 2. C#은 `WS_PollEvent`로 받은 ptr을 즉시 managed(ArrayPool)로 복사하고 ptr을 보존하지 않는다

```csharp
// CORRECT
var buffer = ArrayPool<byte>.Shared.Rent(dataLen);
Marshal.Copy(dataPtr, buffer, 0, dataLen);
// ... 사용 ...
ArrayPool<byte>.Shared.Return(buffer);
WS_FreeBuffer(dataPtr);

// WRONG - ptr 보존 금지
_savedPtr = dataPtr; // 이후 Free 시점 불명확 → 누수/UAF
```

**위반 시**: Use-After-Free 또는 메모리 누수

### 3. 한 Tick에서 처리 가능한 이벤트 개수 상한이 있어야 한다

```csharp
const int MaxEventsPerTick = 64; // 권장값

for (int i = 0; i < MaxEventsPerTick; i++)
{
    if (WS_PollEvent(...) == 0)
        break;
    // 처리
}
```

**위반 시**: 대량 수신 시 프레임 드롭, 메인 스레드 블로킹

### 4. `ToArray()` 금지, `ArrayPool<byte>` 사용 강제

```csharp
// CORRECT
var buffer = ArrayPool<byte>.Shared.Rent(dataLen);
Marshal.Copy(dataPtr, buffer, 0, dataLen);
// ... 사용 후 ...
ArrayPool<byte>.Shared.Return(buffer);

// WRONG
byte[] buffer = new byte[dataLen]; // GC 압박
Marshal.Copy(dataPtr, buffer, 0, dataLen);
```

**위반 시**: GC 압박으로 프레임 스파이크, 핫 경로 allocation

---

## 권장 구현 패턴

### MESSAGE 처리

```csharp
case EventType.MESSAGE:
    // 1. ArrayPool에서 버퍼 임대
    var buffer = ArrayPool<byte>.Shared.Rent(dataLen);
    try
    {
        // 2. Marshal.Copy로 복사
        Marshal.Copy(dataPtr, buffer, 0, dataLen);

        // 3. core로 전달
        _core.OnFrame(_sessionId, buffer.AsSpan(0, dataLen));
    }
    finally
    {
        // 4. ArrayPool 반환
        ArrayPool<byte>.Shared.Return(buffer);
    }
    // 5. Free 호출 (반드시)
    WS_FreeBuffer(dataPtr);
    break;
```

### ERROR/CLOSE 처리

```csharp
case EventType.CLOSE:
    string reason = "";
    if (messagePtr != IntPtr.Zero)
    {
        reason = Marshal.PtrToStringUTF8(messagePtr);
        WS_FreeString(messagePtr); // 반드시
    }
    EnqueueDispatch(() => OnClose?.Invoke((ushort)code, reason));
    break;
```

---

## FAIL 조건

아래 패턴이 문서/코드에 등장하면 **FAIL**:

1. **Free 누락 가능성이 있는 설계**
   - 예: `dataPtr`를 필드에 저장하고 나중에 Free하는 구조
   - 예: 예외 발생 시 Free가 호출되지 않는 코드 경로

2. **`ToArray()` 또는 `new byte[]` 사용**
   - 핫 경로(수신 루프)에서 allocation

3. **이벤트 처리량 상한 없음**
   - 무한 루프로 PollEvent 호출

4. **ptr 보존**
   - `WS_PollEvent`에서 받은 ptr을 복사 없이 보관

---

## Verification Checklist

- [ ] MESSAGE 수신 후 `WS_FreeBuffer(dataPtr)` 호출됨
- [ ] ERROR/CLOSE 수신 후 messagePtr이 non-null이면 `WS_FreeString(messagePtr)` 호출됨
- [ ] 예외 발생 시에도 Free가 호출되도록 try-finally 또는 동등한 구조 사용
- [ ] `ArrayPool<byte>.Shared.Rent()`/`.Return()` 사용
- [ ] `ToArray()` 또는 `new byte[]` 미사용
- [ ] Tick당 이벤트 처리 상한 존재 (권장: 64)

---

## Reference

- 폴링 계약: [76-webgl-ws-polling-bridge](../76-webgl-ws-polling-bridge/SKILL.md)
- WebSocket 클라이언트: [72-network-ws-client](../72-network-ws-client/SKILL.md)
