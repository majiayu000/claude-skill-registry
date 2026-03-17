---
name: system-io-pipelines
description: >
  Guidance for System.IO.Pipelines high-performance I/O in .NET.
  USE FOR: high-throughput stream parsing, zero-copy buffer management, PipeReader/PipeWriter patterns, network protocol parsing, ReadOnlySequence processing, replacing Stream-based I/O bottlenecks.
  DO NOT USE FOR: simple file reads (use Stream or File APIs), HTTP request handling (use ASP.NET Core), gRPC communication (use grpc-dotnet), email (use mimekit).
license: MIT
metadata:
  displayName: "System.IO.Pipelines"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "System.IO.Pipelines Documentation"
    url: "https://learn.microsoft.com/en-us/dotnet/standard/io/pipelines"
  - title: "System.IO.Pipelines NuGet Package"
    url: "https://www.nuget.org/packages/System.IO.Pipelines"
  - title: ".NET Runtime GitHub Repository"
    url: "https://github.com/dotnet/runtime"
---

# System.IO.Pipelines

## Overview

`System.IO.Pipelines` is a high-performance I/O library introduced in .NET Core that solves the classic problems of stream-based parsing: managing buffers, handling partial reads, and avoiding excessive memory copies. It provides `PipeReader` and `PipeWriter` as the core abstractions, connected by a `Pipe` that manages an internal buffer pool. The reader consumes data from the pipe, and the writer produces data into it. Unlike `Stream`, Pipelines separates the concerns of buffering, backpressure, and parsing, making it easier to write correct and efficient protocol parsers.

Pipelines is the foundation of Kestrel (ASP.NET Core's web server) and is designed for scenarios where `Stream` APIs become a bottleneck: custom protocol servers, high-throughput message parsing, and any I/O-bound code that processes large volumes of data with minimal allocation.

## Basic PipeReader Pattern

The standard pattern for reading from a `PipeReader`: read, examine the buffer, advance, and repeat.

```csharp
using System;
using System.Buffers;
using System.IO.Pipelines;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

public class LineReader
{
    public async Task ReadLinesAsync(
        PipeReader reader, CancellationToken ct)
    {
        while (true)
        {
            ReadResult result = await reader.ReadAsync(ct);
            ReadOnlySequence<byte> buffer = result.Buffer;

            while (TryReadLine(ref buffer, out ReadOnlySequence<byte> line))
            {
                ProcessLine(line);
            }

            // Tell the pipe how much was consumed and examined
            reader.AdvanceTo(buffer.Start, buffer.End);

            if (result.IsCompleted)
                break;
        }

        await reader.CompleteAsync();
    }

    private static bool TryReadLine(
        ref ReadOnlySequence<byte> buffer,
        out ReadOnlySequence<byte> line)
    {
        var position = buffer.PositionOf((byte)'\n');
        if (position is null)
        {
            line = default;
            return false;
        }

        line = buffer.Slice(0, position.Value);
        buffer = buffer.Slice(
            buffer.GetPosition(1, position.Value));
        return true;
    }

    private static void ProcessLine(ReadOnlySequence<byte> line)
    {
        var text = Encoding.UTF8.GetString(line);
        Console.WriteLine($"Line: {text}");
    }
}
```

## PipeWriter Pattern

Write data into a pipe using `PipeWriter`, which manages buffer allocation from the memory pool.

```csharp
using System;
using System.Buffers;
using System.IO.Pipelines;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

public class MessageWriter
{
    public async Task WriteMessagesAsync(
        PipeWriter writer,
        IAsyncEnumerable<string> messages,
        CancellationToken ct)
    {
        foreach await (var message in messages.WithCancellation(ct))
        {
            var bytes = Encoding.UTF8.GetBytes(message + "\n");

            // Get memory from the writer's pool
            var memory = writer.GetMemory(bytes.Length);
            bytes.CopyTo(memory);
            writer.Advance(bytes.Length);

            // Flush to make data available to the reader
            FlushResult flushResult = await writer.FlushAsync(ct);
            if (flushResult.IsCompleted)
                break;
        }

        await writer.CompleteAsync();
    }

    public async Task WriteWithSpanAsync(
        PipeWriter writer, ReadOnlyMemory<byte> data,
        CancellationToken ct)
    {
        // Efficient: write directly to the pipe's buffer
        var span = writer.GetSpan(data.Length);
        data.Span.CopyTo(span);
        writer.Advance(data.Length);
        await writer.FlushAsync(ct);
    }
}
```

## Connecting Pipe to Stream

Bridge between `Stream` and `PipeReader`/`PipeWriter` using built-in adapters.

```csharp
using System.IO;
using System.IO.Pipelines;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;

public class StreamPipeAdapter
{
    public async Task ProcessNetworkStreamAsync(
        NetworkStream networkStream, CancellationToken ct)
    {
        // Create a PipeReader from an existing stream
        var reader = PipeReader.Create(networkStream,
            new StreamPipeReaderOptions(
                bufferSize: 4096,
                minimumReadSize: 1024));

        var lineReader = new LineReader();
        await lineReader.ReadLinesAsync(reader, ct);
    }

    public async Task ProcessWithPipeAsync(CancellationToken ct)
    {
        var pipe = new Pipe(new PipeOptions(
            pauseWriterThreshold: 64 * 1024,  // 64 KB
            resumeWriterThreshold: 32 * 1024,  // 32 KB
            minimumSegmentSize: 4096,
            useSynchronizationContext: false));

        // Writer and reader run concurrently
        var writing = FillPipeAsync(pipe.Writer, ct);
        var reading = new LineReader()
            .ReadLinesAsync(pipe.Reader, ct);

        await Task.WhenAll(reading, writing);
    }

    private async Task FillPipeAsync(
        PipeWriter writer, CancellationToken ct)
    {
        // Simulate incoming data
        var data = System.Text.Encoding.UTF8
            .GetBytes("Hello\nWorld\n");
        var memory = writer.GetMemory(data.Length);
        data.CopyTo(memory);
        writer.Advance(data.Length);
        await writer.FlushAsync(ct);
        await writer.CompleteAsync();
    }
}
```

## Parsing Binary Protocol with ReadOnlySequence

Parse a length-prefixed binary protocol using `SequenceReader<byte>` for efficient multi-segment buffer access.

```csharp
using System;
using System.Buffers;
using System.Buffers.Binary;
using System.IO.Pipelines;
using System.Threading;
using System.Threading.Tasks;

public class BinaryProtocolParser
{
    public async Task ParseAsync(
        PipeReader reader, CancellationToken ct)
    {
        while (true)
        {
            var result = await reader.ReadAsync(ct);
            var buffer = result.Buffer;

            while (TryParseMessage(
                ref buffer, out byte messageType,
                out ReadOnlySequence<byte> payload))
            {
                HandleMessage(messageType, payload);
            }

            reader.AdvanceTo(buffer.Start, buffer.End);

            if (result.IsCompleted)
                break;
        }

        await reader.CompleteAsync();
    }

    private static bool TryParseMessage(
        ref ReadOnlySequence<byte> buffer,
        out byte messageType,
        out ReadOnlySequence<byte> payload)
    {
        messageType = 0;
        payload = default;

        // Header: MessageType(1 byte) + PayloadLength(4 bytes)
        if (buffer.Length < 5) return false;

        var reader = new SequenceReader<byte>(buffer);

        if (!reader.TryRead(out messageType)) return false;
        if (!reader.TryReadBigEndian(out int payloadLength))
            return false;

        if (buffer.Length < 5 + payloadLength) return false;

        payload = buffer.Slice(5, payloadLength);
        buffer = buffer.Slice(5 + payloadLength);
        return true;
    }

    private void HandleMessage(
        byte type, ReadOnlySequence<byte> payload)
    {
        Console.WriteLine(
            $"Message type={type}, length={payload.Length}");
    }
}
```

## Backpressure Configuration

Configure the pipe's pause/resume thresholds to control memory usage when the writer outpaces the reader.

```csharp
using System.Buffers;
using System.IO.Pipelines;

var options = new PipeOptions(
    pool: MemoryPool<byte>.Shared,
    // Pause writing when buffer exceeds 1 MB
    pauseWriterThreshold: 1024 * 1024,
    // Resume writing when buffer drops below 512 KB
    resumeWriterThreshold: 512 * 1024,
    minimumSegmentSize: 4096,
    useSynchronizationContext: false);

var pipe = new Pipe(options);
```

## Stream vs Pipelines

| Aspect | `Stream` | `System.IO.Pipelines` |
|---|---|---|
| Buffer management | Caller allocates `byte[]` | Pipe manages pooled buffers |
| Partial reads | Caller handles loop + offset | `AdvanceTo` tracks unconsumed data |
| Backpressure | Not built-in | `pauseWriterThreshold` / `resumeWriterThreshold` |
| Multi-segment buffers | Not supported | `ReadOnlySequence<byte>` spans segments |
| Memory allocation | New `byte[]` per read | Pooled `Memory<byte>` segments |
| Concurrent read/write | Not safe | Designed for concurrent reader + writer |
| Cancellation | Per-operation | Per-operation with `CancellationToken` |

## Best Practices

1. **Use Pipelines when `Stream` APIs become a bottleneck** in protocol parsing or high-throughput I/O; for simple file reads or low-volume HTTP calls, `Stream` is sufficient.
2. **Always call `reader.AdvanceTo(consumed, examined)`** to tell the pipe how much data was consumed (can be freed) and examined (do not re-read), preventing unbounded buffer growth.
3. **Check `result.IsCompleted`** after processing the buffer to detect when the writer signals completion, and exit the read loop cleanly.
4. **Use `SequenceReader<byte>`** to parse multi-segment `ReadOnlySequence<byte>` buffers efficiently without copying them into a contiguous array.
5. **Configure `pauseWriterThreshold` and `resumeWriterThreshold`** to implement backpressure and prevent out-of-memory conditions when the writer produces data faster than the reader consumes it.
6. **Avoid slicing `ReadOnlySequence` into `byte[]`** (via `ToArray()`) except when absolutely necessary; work with the sequence directly or use `SequenceReader<byte>` to avoid copying.
7. **Run the writer and reader on separate tasks** (`Task.WhenAll(writingTask, readingTask)`) to maximize throughput by allowing concurrent I/O and parsing.
8. **Call `CompleteAsync` on both `PipeReader` and `PipeWriter`** when done, passing an exception if the operation failed, to signal the other side and release pooled buffers.
9. **Set `useSynchronizationContext: false`** in `PipeOptions` for server-side code to avoid posting continuations to the synchronization context, which can cause deadlocks.
10. **Use `PipeReader.Create(stream)` and `PipeWriter.Create(stream)`** to adapt existing `Stream`-based APIs to Pipelines incrementally, without rewriting the entire I/O stack at once.
