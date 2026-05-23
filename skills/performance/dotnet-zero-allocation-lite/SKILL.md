---
name: dotnet-zero-allocation-lite
description: 'Zero Allocation 핵심 패턴 (Span, ArrayPool)'
---

# Zero Allocation 핵심

## 1. Span<T> 기본

```csharp
// 문자열 슬라이싱 (Heap 할당 없음)
ReadOnlySpan<char> part = text.AsSpan(0, 10);

// 배열 슬라이싱
Span<int> span = data.AsSpan();
Span<int> firstHalf = span[..^(span.Length / 2)];
```

## 2. ArrayPool<T>

```csharp
// 배열 대여
var buffer = ArrayPool<byte>.Shared.Rent(size);

try
{
    ProcessBuffer(buffer.AsSpan(0, size));
}
finally
{
    ArrayPool<byte>.Shared.Return(buffer);
}
```

## 3. stackalloc

```csharp
// Stack에 작은 버퍼 할당
Span<byte> buffer = stackalloc byte[256];
```

## 4. 주의사항

- ⚠️ Span<T>는 async-await 사용 불가
- ⚠️ ArrayPool: Rent 후 반드시 Return 호출

> 상세 내용: `/dotnet-zero-allocation` skill 참조
