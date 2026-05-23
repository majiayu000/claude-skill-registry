---
name: dotnet-pipelines-lite
description: 'System.IO.Pipelines 핵심 패턴'
---

# Pipelines 핵심

## 1. 기본 패턴

```csharp
using System.IO.Pipelines;

var pipe = new Pipe();

// Writer와 Reader 동시 실행
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

## 4. 주의사항

- ⚠️ ReadAsync 후 반드시 AdvanceTo 호출
- ⚠️ Writer/Reader 모두 CompleteAsync 호출 필수

> 상세 내용: `/dotnet-pipelines` skill 참조
