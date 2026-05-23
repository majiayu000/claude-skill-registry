---
name: optimizing-memory-allocation
description: "Implements Zero Allocation patterns using Span, ArrayPool, and ObjectPool for memory efficiency in .NET. Use when reducing GC pressure or optimizing high-performance memory operations."
---

# .NET Memory Efficiency, Zero Allocation

A guide for APIs that minimize GC pressure and enable high-performance memory management.

**Quick Reference:** See [QUICKREF.md](QUICKREF.md) for essential patterns at a glance.

## 1. Core Concepts

- .NET CLR GC Heap Memory Optimization
- Understanding Stack allocation vs Heap allocation
- Stack-only types through ref struct

## 2. Key APIs

| API | Purpose | NuGet |
|-----|---------|-------|
| `Span<T>`, `Memory<T>` | Stack-based memory slicing | BCL |
| `ArrayPool<T>.Shared` | Reduce GC pressure through array reuse | BCL |
| `DefaultObjectPool<T>` | Object pooling | Microsoft.Extensions.ObjectPool |
| `MemoryCache` | In-memory caching | System.Runtime.Caching |

---

## 3. Span<T>, ReadOnlySpan<T>

### 3.1 Basic Usage

```csharp
// Zero Allocation when parsing strings
public void ParseData(ReadOnlySpan<char> input)
{
    // String manipulation without Heap allocation
    var firstPart = input.Slice(0, 10);
    var secondPart = input.Slice(10);
}

// Array slicing
public void ProcessArray(int[] data)
{
    Span<int> span = data.AsSpan();
    Span<int> firstHalf = span[..^(span.Length / 2)];
    Span<int> secondHalf = span[(span.Length / 2)..];
}
```

### 3.2 String Processing Optimization

```csharp
// ❌ Bad example: Substring allocates new string
string part = text.Substring(0, 10);

// ✅ Good example: AsSpan has no allocation
ReadOnlySpan<char> part = text.AsSpan(0, 10);
```

### 3.3 Using with stackalloc

```csharp
public void ProcessSmallBuffer()
{
    // Allocate small buffer on Stack (no Heap allocation)
    Span<byte> buffer = stackalloc byte[256];
    FillBuffer(buffer);
}
```

---

## 4. ArrayPool<T>

Reduces GC pressure by reusing large arrays.

### 4.1 Basic Usage

```csharp
namespace MyApp.Services;

public sealed class DataProcessor
{
    public void ProcessLargeData(int size)
    {
        // Rent array (minimize Heap allocation)
        var buffer = ArrayPool<byte>.Shared.Rent(size);

        try
        {
            // Use buffer (only use up to requested size)
            ProcessBuffer(buffer.AsSpan(0, size));
        }
        finally
        {
            // Must return
            ArrayPool<byte>.Shared.Return(buffer);
        }
    }
}
```

### 4.2 clearArray Option

```csharp
// Initialize before returning when handling sensitive data
ArrayPool<byte>.Shared.Return(buffer, clearArray: true);
```

---

## 5. ObjectPool<T>

Reuses expensive objects.

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

Unlike Span<T>, can be stored in fields or used in async methods.

```csharp
public sealed class AsyncProcessor
{
    private Memory<byte> _buffer;

    public AsyncProcessor(int size)
    {
        _buffer = new byte[size];
    }

    // Memory<T> can be used in async methods
    public async Task ProcessAsync()
    {
        await FillBufferAsync(_buffer);
        ProcessData(_buffer.Span);
    }
}
```

---

## 7. Required NuGet Package

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Extensions.ObjectPool" Version="9.0.*" />
</ItemGroup>
```

---

## 8. Important Notes

### ⚠️ Span<T> Constraints

- `Span<T>`, `ReadOnlySpan<T>` **cannot be used with async-await**
- Cannot be boxed (ref struct)
- Cannot be stored as class field (use Memory<T>)
- Cannot be captured in lambdas/closures

### ⚠️ ArrayPool Return Required

- Arrays rented with `Rent()` must be returned with `Return()`
- Use try-finally pattern
- Memory leak occurs if not returned

### ⚠️ Rented Size vs Actual Size

```csharp
// Array larger than requested may be returned
var buffer = ArrayPool<byte>.Shared.Rent(100);
// buffer.Length >= 100 (not exactly 100)

// Use only requested size when actually using
ProcessBuffer(buffer.AsSpan(0, 100));
```

---

## 9. References

- [Span<T> - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.span-1)
- [ArrayPool<T> - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1)

