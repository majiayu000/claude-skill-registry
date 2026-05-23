---
name: dotnet-fast-io-lite
description: '고속 I/O 핵심 패턴'
---

# 고속 I/O 핵심

## 1. 고속 표준 입출력

```csharp
using var reader = new StreamReader(
    Console.OpenStandardInput(),
    bufferSize: 65536);

using var writer = new StreamWriter(
    Console.OpenStandardOutput(),
    bufferSize: 65536);

writer.AutoFlush = false;

// 처리 후 수동 플러시
writer.Flush();
```

## 2. 파일 I/O

```csharp
// 64KB 버퍼로 순차 읽기
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

## 4. 성능 비교

| 방식 | 상대 성능 |
|------|----------|
| Console.ReadLine() | 1x |
| StreamReader (64KB) | 3-5x |
| MemoryMappedFile | 5-10x |

> 상세 내용: `/dotnet-fast-io` skill 참조
