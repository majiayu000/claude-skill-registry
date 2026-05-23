---
name: dotnet-pipelines
description: '.NET Streaming 패턴 (System.IO.Pipelines)'
---

# .NET Streaming (System.IO.Pipelines)

고성능 I/O 파이프라인을 위한 System.IO.Pipelines API 가이드입니다.

## 1. 핵심 개념

| 개념 | 설명 |
|------|------|
| `Pipe` | 메모리 버퍼 기반 읽기/쓰기 파이프 |
| `PipeReader` | 파이프에서 데이터 읽기 |
| `PipeWriter` | 파이프에 데이터 쓰기 |
| `ReadOnlySequence<T>` | 비연속 메모리 시퀀스 |

## 2. 장점

- **Zero-copy**: 불필요한 메모리 복사 최소화
- **배압 제어**: 생산자-소비자 간 속도 조절
- **메모리 풀링**: 자동 버퍼 재사용
- **비동기 I/O**: 효율적인 비동기 처리

---

## 3. 기본 사용법

```csharp
using System.IO.Pipelines;

public sealed class PipelineProcessor
{
    public async Task ProcessAsync(Stream stream)
    {
        var pipe = new Pipe();

        // Writer와 Reader 동시 실행
        var writing = FillPipeAsync(stream, pipe.Writer);
        var reading = ReadPipeAsync(pipe.Reader);

        await Task.WhenAll(writing, reading);
    }

    private async Task FillPipeAsync(Stream stream, PipeWriter writer)
    {
        const int minimumBufferSize = 512;

        while (true)
        {
            // 메모리 풀에서 버퍼 획득
            Memory<byte> memory = writer.GetMemory(minimumBufferSize);

            int bytesRead = await stream.ReadAsync(memory);

            if (bytesRead == 0)
                break;

            // 쓴 바이트 수 알림
            writer.Advance(bytesRead);

            // 데이터 플러시 및 Reader에게 알림
            FlushResult result = await writer.FlushAsync();

            if (result.IsCompleted)
                break;
        }

        // 쓰기 완료 신호
        await writer.CompleteAsync();
    }

    private async Task ReadPipeAsync(PipeReader reader)
    {
        while (true)
        {
            ReadResult result = await reader.ReadAsync();
            ReadOnlySequence<byte> buffer = result.Buffer;

            // 버퍼 처리
            ProcessBuffer(buffer);

            // 처리한 위치까지 소비 완료 알림
            reader.AdvanceTo(buffer.End);

            if (result.IsCompleted)
                break;
        }

        // 읽기 완료 신호
        await reader.CompleteAsync();
    }
}
```

---

## 4. 라인 단위 파싱

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

        // 처리되지 않은 데이터 위치 알림
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
    // 줄바꿈 찾기
    SequencePosition? position = buffer.PositionOf((byte)'\n');

    if (position is null)
    {
        line = default;
        return false;
    }

    // 줄바꿈 전까지 슬라이스
    line = buffer.Slice(0, position.Value);

    // 줄바꿈 이후로 버퍼 이동
    buffer = buffer.Slice(buffer.GetPosition(1, position.Value));

    return true;
}
```

---

## 5. ReadOnlySequence<T> 처리

```csharp
private void ProcessBuffer(ReadOnlySequence<byte> buffer)
{
    if (buffer.IsSingleSegment)
    {
        // 단일 세그먼트 - 직접 접근
        ProcessSpan(buffer.FirstSpan);
    }
    else
    {
        // 다중 세그먼트 - 순회 필요
        foreach (var segment in buffer)
        {
            ProcessSpan(segment.Span);
        }
    }
}
```

---

## 6. 네트워크 I/O 통합

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

## 7. PipeOptions 설정

```csharp
var pipeOptions = new PipeOptions(
    pool: MemoryPool<byte>.Shared,           // 메모리 풀
    readerScheduler: PipeScheduler.ThreadPool, // Reader 스케줄러
    writerScheduler: PipeScheduler.ThreadPool, // Writer 스케줄러
    pauseWriterThreshold: 64 * 1024,         // Writer 일시정지 임계값
    resumeWriterThreshold: 32 * 1024,        // Writer 재개 임계값
    minimumSegmentSize: 4096,                // 최소 세그먼트 크기
    useSynchronizationContext: false
);

var pipe = new Pipe(pipeOptions);
```

---

## 8. 필수 NuGet 패키지

```xml
<ItemGroup>
  <!-- .NET Core 3.0+ 에서는 BCL에 포함 -->
  <PackageReference Include="System.IO.Pipelines" Version="9.0.*" />
</ItemGroup>
```

---

## 9. 주의사항

### ⚠️ AdvanceTo 호출 필수

```csharp
// ReadAsync 후 반드시 AdvanceTo 호출
ReadResult result = await reader.ReadAsync();
// ... 처리 ...
reader.AdvanceTo(consumed, examined);
```

### ⚠️ 버퍼 수명

```csharp
// ❌ 나쁜 예: ReadAsync 후 버퍼 저장
ReadOnlySequence<byte> saved;
var result = await reader.ReadAsync();
saved = result.Buffer; // 위험! AdvanceTo 후 무효화됨

// ✅ 좋은 예: 필요한 데이터 복사
var copy = result.Buffer.ToArray();
reader.AdvanceTo(result.Buffer.End);
```

### ⚠️ 완료 호출

```csharp
// Writer와 Reader 모두 CompleteAsync 호출 필수
await writer.CompleteAsync();
await reader.CompleteAsync();
```

---

## 10. 참고 문서

- [System.IO.Pipelines](https://learn.microsoft.com/en-us/dotnet/standard/io/pipelines)
- [High-performance I/O](https://devblogs.microsoft.com/dotnet/system-io-pipelines-high-performance-io-in-net/)

