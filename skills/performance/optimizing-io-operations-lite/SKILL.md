---
name: optimizing-io-operations-lite
description: "Provides essential high-performance I/O patterns. Use when quickly referencing core I/O optimization techniques without detailed explanations."
---

# High-Performance I/O Essentials

## 1. High-Speed Standard I/O

```csharp
using var reader = new StreamReader(
    Console.OpenStandardInput(),
    bufferSize: 65536);

using var writer = new StreamWriter(
    Console.OpenStandardOutput(),
    bufferSize: 65536);

writer.AutoFlush = false;

// Manual flush after processing
writer.Flush();
```

## 2. File I/O

```csharp
// Sequential read with 64KB buffer
using var stream = new FileStream(
    path,
    FileMode.Open,
    FileAccess.Read,
    FileShare.Read,
    bufferSize: 64 * 1024,
    options: FileOptions.SequentialScan);
```

## 3. RandomAccess (.NET 6+)

```csharp
using var handle = File.OpenHandle(path, FileMode.Open, FileAccess.Read);
int bytesRead = await RandomAccess.ReadAsync(handle, buffer, offset);
```

## 4. Performance Comparison

| Method | Relative Performance |
|--------|---------------------|
| Console.ReadLine() | 1x |
| StreamReader (64KB) | 3-5x |
| MemoryMappedFile | 5-10x |

> For details: See `/dotnet-fast-io` skill
