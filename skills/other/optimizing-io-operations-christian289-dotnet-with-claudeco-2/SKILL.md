---
name: optimizing-io-operations
description: "Optimizes standard I/O and file operations for high-performance data processing in .NET. Use when building high-throughput file processing or competitive programming solutions."
---

# .NET High-Performance I/O

A guide for APIs optimizing large-scale data input/output.

**Quick Reference:** See [QUICKREF.md](QUICKREF.md) for essential patterns at a glance.

## 1. Core APIs

| API | Purpose |
|-----|---------|
| `Console.OpenStandardInput()` | Buffered stream input |
| `Console.OpenStandardOutput()` | Buffered stream output |
| `BufferedStream` | Stream buffering |
| `FileOptions.Asynchronous` | Async file I/O |

---

## 2. High-Speed Standard I/O

### 2.1 Basic Pattern

```csharp
// Use buffer stream directly for large I/O
using var inputStream = Console.OpenStandardInput();
using var outputStream = Console.OpenStandardOutput();
using var reader = new StreamReader(inputStream, bufferSize: 65536);
using var writer = new StreamWriter(outputStream, bufferSize: 65536);

// Disable buffer flush for performance improvement
writer.AutoFlush = false;

string? line;
while ((line = reader.ReadLine()) is not null)
{
    writer.WriteLine(ProcessLine(line));
}

// Manual flush at the end
writer.Flush();
```

### 2.2 For Algorithm Problem Solving

```csharp
using System.Text;

// High-speed input
using var reader = new StreamReader(
    Console.OpenStandardInput(),
    Encoding.ASCII,
    bufferSize: 65536);

// High-speed output
using var writer = new StreamWriter(
    Console.OpenStandardOutput(),
    Encoding.ASCII,
    bufferSize: 65536);

var sb = new StringBuilder();

// Collect large output in StringBuilder and write at once
for (int i = 0; i < 100000; i++)
{
    sb.AppendLine(i.ToString());
}

writer.Write(sb);
writer.Flush();
```

---

## 3. File I/O Optimization

### 3.1 Buffer Size Optimization

```csharp
// Use larger buffer than default (4KB)
const int bufferSize = 64 * 1024; // 64KB

using var fileStream = new FileStream(
    path,
    FileMode.Open,
    FileAccess.Read,
    FileShare.Read,
    bufferSize: bufferSize);
```

### 3.2 Async File I/O

```csharp
// Open file with async option
using var fileStream = new FileStream(
    path,
    FileMode.Open,
    FileAccess.Read,
    FileShare.Read,
    bufferSize: 4096,
    options: FileOptions.Asynchronous);

var buffer = new byte[4096];
int bytesRead = await fileStream.ReadAsync(buffer);
```

### 3.3 SequentialScan Hint

```csharp
// Provide hint to OS for sequential reading
using var fileStream = new FileStream(
    path,
    FileMode.Open,
    FileAccess.Read,
    FileShare.Read,
    bufferSize: 64 * 1024,
    options: FileOptions.SequentialScan);
```

### 3.4 RandomAccess (.NET 6+)

```csharp
// Direct offset access without file position management
using var handle = File.OpenHandle(path, FileMode.Open, FileAccess.Read);

var buffer = new byte[4096];
long offset = 1000;

int bytesRead = RandomAccess.Read(handle, buffer, offset);

// Async version
bytesRead = await RandomAccess.ReadAsync(handle, buffer, offset);
```

---

## 4. Large File Processing

### 4.1 Chunk-Based Reading

```csharp
public async IAsyncEnumerable<byte[]> ReadChunksAsync(
    string path,
    int chunkSize = 64 * 1024,
    [EnumeratorCancellation] CancellationToken ct = default)
{
    using var stream = new FileStream(
        path,
        FileMode.Open,
        FileAccess.Read,
        FileShare.Read,
        bufferSize: chunkSize,
        options: FileOptions.Asynchronous | FileOptions.SequentialScan);

    var buffer = new byte[chunkSize];
    int bytesRead;

    while ((bytesRead = await stream.ReadAsync(buffer, ct)) > 0)
    {
        if (bytesRead == chunkSize)
        {
            yield return buffer;
            buffer = new byte[chunkSize];
        }
        else
        {
            yield return buffer[..bytesRead];
        }
    }
}
```

### 4.2 Memory-Mapped Files

```csharp
using System.IO.MemoryMappedFiles;

// Map large file to memory
using var mmf = MemoryMappedFile.CreateFromFile(path, FileMode.Open);
using var accessor = mmf.CreateViewAccessor();

// Direct memory access
byte value = accessor.ReadByte(position);
accessor.Write(position, newValue);
```

---

## 5. Performance Comparison

| Method | Relative Performance | Use Case |
|--------|---------------------|----------|
| Console.ReadLine() | 1x (baseline) | General |
| StreamReader (default buffer) | 2x | Large data |
| StreamReader (64KB buffer) | 3-5x | Large data |
| MemoryMappedFile | 5-10x | Very large data |

---

## 6. Important Notes

### Buffer Size

- Too small increases system calls
- Too large wastes memory
- Recommended: 4KB ~ 64KB

### Encoding Specification

```csharp
// Read UTF-8 without BOM
using var reader = new StreamReader(
    stream,
    new UTF8Encoding(encoderShouldEmitUTF8Identifier: false));
```

### Flush Timing

```csharp
// Improve performance with AutoFlush = false
writer.AutoFlush = false;

// Manual flush after important data
writer.Flush();
```

---

## 7. References

- [File and Stream I/O](https://learn.microsoft.com/en-us/dotnet/standard/io/)
- [Memory-Mapped Files](https://learn.microsoft.com/en-us/dotnet/standard/io/memory-mapped-files)

