---
name: implementing-io-pipelines
description: "Implements high-performance streaming using System.IO.Pipelines in .NET. Use when building network protocols, parsing binary data, or processing large streams efficiently."
---

# .NET Streaming (System.IO.Pipelines)

A guide for System.IO.Pipelines API for high-performance I/O pipelines.

**Quick Reference:** See [QUICKREF.md](QUICKREF.md) for essential patterns at a glance.

## 1. Core Concepts

| Concept | Description |
|---------|-------------|
| `Pipe` | Memory buffer-based read/write pipe |
| `PipeReader` | Read data from pipe |
| `PipeWriter` | Write data to pipe |
| `ReadOnlySequence<T>` | Non-contiguous memory sequence |

## 2. Advantages

- **Zero-copy**: Minimizes unnecessary memory copying
- **Backpressure control**: Speed regulation between producer and consumer
- **Memory pooling**: Automatic buffer reuse
- **Async I/O**: Efficient asynchronous processing

---

## 3. Basic Usage

```csharp
using System.IO.Pipelines;

public sealed class PipelineProcessor
{
    public async Task ProcessAsync(Stream stream)
    {
        var pipe = new Pipe();

        // Run Writer and Reader concurrently
        var writing = FillPipeAsync(stream, pipe.Writer);
        var reading = ReadPipeAsync(pipe.Reader);

        await Task.WhenAll(writing, reading);
    }

    private async Task FillPipeAsync(Stream stream, PipeWriter writer)
    {
        const int minimumBufferSize = 512;

        while (true)
        {
            // Acquire buffer from memory pool
            Memory<byte> memory = writer.GetMemory(minimumBufferSize);

            int bytesRead = await stream.ReadAsync(memory);

            if (bytesRead == 0)
                break;

            // Notify bytes written
            writer.Advance(bytesRead);

            // Flush data and notify Reader
            FlushResult result = await writer.FlushAsync();

            if (result.IsCompleted)
                break;
        }

        // Signal write completion
        await writer.CompleteAsync();
    }

    private async Task ReadPipeAsync(PipeReader reader)
    {
        while (true)
        {
            ReadResult result = await reader.ReadAsync();
            ReadOnlySequence<byte> buffer = result.Buffer;

            // Process buffer
            ProcessBuffer(buffer);

            // Notify consumption up to processed position
            reader.AdvanceTo(buffer.End);

            if (result.IsCompleted)
                break;
        }

        // Signal read completion
        await reader.CompleteAsync();
    }
}
```

---

## 4. Line-by-Line Parsing

```csharp
private async Task ReadLinesAsync(PipeReader reader)
{
    while (true)
    {
        ReadResult result = await reader.ReadAsync();
        ReadOnlySequence<byte> buffer = result.Buffer;

        while (TryReadLine(ref buffer, out ReadOnlySequence<byte> line))
        {
            ProcessLine(line);
        }

        // Notify unprocessed data position
        reader.AdvanceTo(buffer.Start, buffer.End);

        if (result.IsCompleted)
            break;
    }

    await reader.CompleteAsync();
}

private bool TryReadLine(
    ref ReadOnlySequence<byte> buffer,
    out ReadOnlySequence<byte> line)
{
    // Find newline
    SequencePosition? position = buffer.PositionOf((byte)'\n');

    if (position is null)
    {
        line = default;
        return false;
    }

    // Slice up to newline
    line = buffer.Slice(0, position.Value);

    // Move buffer past newline
    buffer = buffer.Slice(buffer.GetPosition(1, position.Value));

    return true;
}
```

---

## 5. Processing ReadOnlySequence<T>

```csharp
private void ProcessBuffer(ReadOnlySequence<byte> buffer)
{
    if (buffer.IsSingleSegment)
    {
        // Single segment - direct access
        ProcessSpan(buffer.FirstSpan);
    }
    else
    {
        // Multiple segments - iteration required
        foreach (var segment in buffer)
        {
            ProcessSpan(segment.Span);
        }
    }
}
```

---

## 6. Network I/O Integration

```csharp
public async Task ProcessSocketAsync(Socket socket)
{
    var pipe = new Pipe();

    var writing = ReceiveAsync(socket, pipe.Writer);
    var reading = ProcessAsync(pipe.Reader);

    await Task.WhenAll(writing, reading);
}

private async Task ReceiveAsync(Socket socket, PipeWriter writer)
{
    while (true)
    {
        Memory<byte> memory = writer.GetMemory(4096);

        int bytesReceived = await socket.ReceiveAsync(
            memory,
            SocketFlags.None);

        if (bytesReceived == 0)
            break;

        writer.Advance(bytesReceived);

        FlushResult result = await writer.FlushAsync();

        if (result.IsCompleted)
            break;
    }

    await writer.CompleteAsync();
}
```

---

## 7. PipeOptions Configuration

```csharp
var pipeOptions = new PipeOptions(
    pool: MemoryPool<byte>.Shared,           // Memory pool
    readerScheduler: PipeScheduler.ThreadPool, // Reader scheduler
    writerScheduler: PipeScheduler.ThreadPool, // Writer scheduler
    pauseWriterThreshold: 64 * 1024,         // Writer pause threshold
    resumeWriterThreshold: 32 * 1024,        // Writer resume threshold
    minimumSegmentSize: 4096,                // Minimum segment size
    useSynchronizationContext: false
);

var pipe = new Pipe(pipeOptions);
```

---

## 8. Required NuGet Package

```xml
<ItemGroup>
  <!-- Included in BCL for .NET Core 3.0+ -->
  <PackageReference Include="System.IO.Pipelines" Version="9.0.*" />
</ItemGroup>
```

---

## 9. Important Notes

### AdvanceTo Call Required

```csharp
// Must call AdvanceTo after ReadAsync
ReadResult result = await reader.ReadAsync();
// ... processing ...
reader.AdvanceTo(consumed, examined);
```

### Buffer Lifetime

```csharp
// ❌ Bad example: Saving buffer after ReadAsync
ReadOnlySequence<byte> saved;
var result = await reader.ReadAsync();
saved = result.Buffer; // Dangerous! Invalidated after AdvanceTo

// ✅ Good example: Copy needed data
var copy = result.Buffer.ToArray();
reader.AdvanceTo(result.Buffer.End);
```

### Completion Calls

```csharp
// Must call CompleteAsync for both Writer and Reader
await writer.CompleteAsync();
await reader.CompleteAsync();
```

---

## 10. References

- [System.IO.Pipelines](https://learn.microsoft.com/en-us/dotnet/standard/io/pipelines)
- [High-performance I/O](https://devblogs.microsoft.com/dotnet/system-io-pipelines-high-performance-io-in-net/)

