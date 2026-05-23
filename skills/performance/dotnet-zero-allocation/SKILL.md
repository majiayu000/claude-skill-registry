---
name: dotnet-zero-allocation
description: '.NET 메모리 효율화 및 Zero Allocation 패턴 (Span, ArrayPool, ObjectPool)'
---

# .NET 메모리 효율화, Zero Allocation

GC 압박을 최소화하고 고성능 메모리 관리를 위한 API 사용 가이드입니다.

## 1. 핵심 개념

- .NET CLR GC Heap Memory Optimization
- Stack 할당 vs Heap 할당 이해
- ref struct를 통한 Stack-only 타입

## 2. 주요 API

| API | 용도 | NuGet |
|-----|------|-------|
| `Span<T>`, `Memory<T>` | Stack 기반 메모리 슬라이싱 | BCL |
| `ArrayPool<T>.Shared` | 배열 재사용으로 GC 압박 감소 | BCL |
| `DefaultObjectPool<T>` | 객체 풀링 | Microsoft.Extensions.ObjectPool |
| `MemoryCache` | 인메모리 캐싱 | System.Runtime.Caching |

---

## 3. Span<T>, ReadOnlySpan<T>

### 3.1 기본 사용법

```csharp
// 문자열 파싱 시 Zero Allocation
public void ParseData(ReadOnlySpan<char> input)
{
    // Heap 할당 없이 문자열 조작
    var firstPart = input.Slice(0, 10);
    var secondPart = input.Slice(10);
}

// 배열 슬라이싱
public void ProcessArray(int[] data)
{
    Span<int> span = data.AsSpan();
    Span<int> firstHalf = span[..^(span.Length / 2)];
    Span<int> secondHalf = span[(span.Length / 2)..];
}
```

### 3.2 문자열 처리 최적화

```csharp
// ❌ 나쁜 예: Substring은 새 문자열 할당
string part = text.Substring(0, 10);

// ✅ 좋은 예: AsSpan은 할당 없음
ReadOnlySpan<char> part = text.AsSpan(0, 10);
```

### 3.3 stackalloc과 함께 사용

```csharp
public void ProcessSmallBuffer()
{
    // Stack에 작은 버퍼 할당 (Heap 할당 없음)
    Span<byte> buffer = stackalloc byte[256];
    FillBuffer(buffer);
}
```

---

## 4. ArrayPool<T>

대용량 배열을 재사용하여 GC 압박을 줄입니다.

### 4.1 기본 사용법

```csharp
namespace MyApp.Services;

public sealed class DataProcessor
{
    public void ProcessLargeData(int size)
    {
        // 배열 대여 (Heap 할당 최소화)
        var buffer = ArrayPool<byte>.Shared.Rent(size);

        try
        {
            // 버퍼 사용 (요청 크기만큼만 사용)
            ProcessBuffer(buffer.AsSpan(0, size));
        }
        finally
        {
            // 반드시 반환
            ArrayPool<byte>.Shared.Return(buffer);
        }
    }
}
```

### 4.2 clearArray 옵션

```csharp
// 민감한 데이터 처리 시 반환 전 초기화
ArrayPool<byte>.Shared.Return(buffer, clearArray: true);
```

---

## 5. ObjectPool<T>

비용이 큰 객체를 재사용합니다.

```csharp
namespace MyApp.Services;

using Microsoft.Extensions.ObjectPool;

public sealed class HeavyObjectProcessor
{
    private readonly ObjectPool<HeavyObject> _pool;

    public HeavyObjectProcessor()
    {
        var policy = new DefaultPooledObjectPolicy<HeavyObject>();
        _pool = new DefaultObjectPool<HeavyObject>(policy, maximumRetained: 100);
    }

    public void Process()
    {
        var obj = _pool.Get();

        try
        {
            obj.DoWork();
        }
        finally
        {
            _pool.Return(obj);
        }
    }
}
```

---

## 6. Memory<T>

Span<T>와 달리 필드에 저장하거나 async 메서드에서 사용 가능합니다.

```csharp
public sealed class AsyncProcessor
{
    private Memory<byte> _buffer;

    public AsyncProcessor(int size)
    {
        _buffer = new byte[size];
    }

    // Memory<T>는 async 메서드에서 사용 가능
    public async Task ProcessAsync()
    {
        await FillBufferAsync(_buffer);
        ProcessData(_buffer.Span);
    }
}
```

---

## 7. 필수 NuGet 패키지

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Extensions.ObjectPool" Version="9.0.*" />
</ItemGroup>
```

---

## 8. 주의사항

### ⚠️ Span<T> 제약

- `Span<T>`, `ReadOnlySpan<T>`는 **async-await와 함께 사용 불가**
- ref struct이므로 Boxing 불가
- 클래스 필드로 저장 불가 (Memory<T> 사용)
- 람다/클로저에서 캡처 불가

### ⚠️ ArrayPool 반환 필수

- `Rent()`로 대여한 배열은 반드시 `Return()` 호출
- try-finally 패턴 사용 권장
- 반환하지 않으면 메모리 누수 발생

### ⚠️ 대여 크기 vs 실제 크기

```csharp
// 요청한 크기보다 큰 배열이 반환될 수 있음
var buffer = ArrayPool<byte>.Shared.Rent(100);
// buffer.Length >= 100 (정확히 100이 아님)

// 실제 사용 시 요청 크기만 사용
ProcessBuffer(buffer.AsSpan(0, 100));
```

---

## 9. 참고 문서

- [Span<T> - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.span-1)
- [ArrayPool<T> - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1)
