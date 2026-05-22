---
name: implementing-io-pipelines-lite
description: "Provides essential System.IO.Pipelines patterns. Use when quickly referencing core pipeline streaming techniques without detailed explanations."
---

# Pipelines Essentials

## 1. Basic Pattern

```csharp
using System.IO.Pipelines;

var pipe = new Pipe();

// Run Writer and Reader concurrently
await Task.WhenAll(
    FillPipeAsync(stream, pipe.Writer),
    ReadPipeAsync(pipe.Reader)
);
```

## 2. Writer

```csharp
private async Task FillPipeAsync(Stream stream, PipeWriter writer)
{
    while (true)
    {
        Memory<byte> memory = writer.GetMemory(512);
        int bytesRead = await stream.ReadAsync(memory);

        if (bytesRead == 0) break;

        writer.Advance(bytesRead);
        await writer.FlushAsync();
    }

    await writer.CompleteAsync();
}
```

## 3. Reader

```csharp
private async Task ReadPipeAsync(PipeReader reader)
{
    while (true)
    {
        ReadResult result = await reader.ReadAsync();
        ProcessBuffer(result.Buffer);
        reader.AdvanceTo(result.Buffer.End);

        if (result.IsCompleted) break;
    }

    await reader.CompleteAsync();
}
```

## 4. Important Notes

- Must call AdvanceTo after ReadAsync
- Must call CompleteAsync for both Writer and Reader

> For details: See `/dotnet-pipelines` skill
