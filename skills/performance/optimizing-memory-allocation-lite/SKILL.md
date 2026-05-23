---
name: optimizing-memory-allocation-lite
description: "Provides essential Zero Allocation patterns using Span and ArrayPool. Use when quickly referencing core memory optimization techniques without detailed explanations."
---

# Zero Allocation Essentials

## 1. Span<T> Basics

```csharp
// String slicing (no Heap allocation)
ReadOnlySpan<char> part = text.AsSpan(0, 10);

// Array slicing
Span<int> span = data.AsSpan();
Span<int> firstHalf = span[..^(span.Length / 2)];
```

## 2. ArrayPool<T>

```csharp
// Rent array
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
// Allocate small buffer on Stack
Span<byte> buffer = stackalloc byte[256];
```

## 4. Important Notes

- Span<T> cannot be used with async-await
- ArrayPool: Must call Return after Rent

> For details: See `/dotnet-zero-allocation` skill
