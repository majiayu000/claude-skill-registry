---
name: dotnet-fast-io
description: '.NET 고속 표준 입출력 및 파일 I/O 최적화'
---

# .NET 고속 입출력

대용량 데이터 입출력 최적화를 위한 API 가이드입니다.

## 1. 핵심 API

| API | 용도 |
|-----|------|
| `Console.OpenStandardInput()` | 버퍼 스트림 입력 |
| `Console.OpenStandardOutput()` | 버퍼 스트림 출력 |
| `BufferedStream` | 스트림 버퍼링 |
| `FileOptions.Asynchronous` | 비동기 파일 I/O |

---

## 2. 고속 표준 입출력

### 2.1 기본 패턴

```csharp
// 대용량 입출력 시 버퍼 스트림 직접 사용
using var inputStream = Console.OpenStandardInput();
using var outputStream = Console.OpenStandardOutput();
using var reader = new StreamReader(inputStream, bufferSize: 65536);
using var writer = new StreamWriter(outputStream, bufferSize: 65536);

// 버퍼 플러시 비활성화로 성능 향상
writer.AutoFlush = false;

string? line;
while ((line = reader.ReadLine()) is not null)
{
    writer.WriteLine(ProcessLine(line));
}

// 마지막에 수동 플러시
writer.Flush();
```

### 2.2 알고리즘 문제 풀이용

```csharp
using System.Text;

// 고속 입력
using var reader = new StreamReader(
    Console.OpenStandardInput(),
    Encoding.ASCII,
    bufferSize: 65536);

// 고속 출력
using var writer = new StreamWriter(
    Console.OpenStandardOutput(),
    Encoding.ASCII,
    bufferSize: 65536);

var sb = new StringBuilder();

// 대량 출력은 StringBuilder로 모은 후 한 번에 출력
for (int i = 0; i < 100000; i++)
{
    sb.AppendLine(i.ToString());
}

writer.Write(sb);
writer.Flush();
```

---

## 3. 파일 I/O 최적화

### 3.1 버퍼 크기 최적화

```csharp
// 기본 버퍼 크기 (4KB)보다 큰 버퍼 사용
const int bufferSize = 64 * 1024; // 64KB

using var fileStream = new FileStream(
    path,
    FileMode.Open,
    FileAccess.Read,
    FileShare.Read,
    bufferSize: bufferSize);
```

### 3.2 비동기 파일 I/O

```csharp
// 비동기 옵션으로 파일 열기
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

### 3.3 SequentialScan 힌트

```csharp
// 순차 읽기 시 OS에 힌트 제공
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
// 파일 위치 지정 없이 직접 오프셋 접근
using var handle = File.OpenHandle(path, FileMode.Open, FileAccess.Read);

var buffer = new byte[4096];
long offset = 1000;

int bytesRead = RandomAccess.Read(handle, buffer, offset);

// 비동기 버전
bytesRead = await RandomAccess.ReadAsync(handle, buffer, offset);
```

---

## 4. 대용량 파일 처리

### 4.1 청크 단위 읽기

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

### 4.2 메모리 매핑 파일

```csharp
using System.IO.MemoryMappedFiles;

// 대용량 파일을 메모리에 매핑
using var mmf = MemoryMappedFile.CreateFromFile(path, FileMode.Open);
using var accessor = mmf.CreateViewAccessor();

// 직접 메모리 접근
byte value = accessor.ReadByte(position);
accessor.Write(position, newValue);
```

---

## 5. 성능 비교

| 방식 | 상대 성능 | 용도 |
|------|----------|------|
| Console.ReadLine() | 1x (기준) | 일반 |
| StreamReader (기본 버퍼) | 2x | 대용량 |
| StreamReader (64KB 버퍼) | 3-5x | 대용량 |
| MemoryMappedFile | 5-10x | 초대용량 |

---

## 6. 주의사항

### ⚠️ 버퍼 크기

- 너무 작으면 시스템 콜 증가
- 너무 크면 메모리 낭비
- 권장: 4KB ~ 64KB

### ⚠️ Encoding 지정

```csharp
// UTF-8 BOM 없이 읽기
using var reader = new StreamReader(
    stream,
    new UTF8Encoding(encoderShouldEmitUTF8Identifier: false));
```

### ⚠️ Flush 타이밍

```csharp
// AutoFlush = false로 성능 향상
writer.AutoFlush = false;

// 중요 데이터 후 수동 Flush
writer.Flush();
```

---

## 7. 참고 문서

- [File and Stream I/O](https://learn.microsoft.com/en-us/dotnet/standard/io/)
- [Memory-Mapped Files](https://learn.microsoft.com/en-us/dotnet/standard/io/memory-mapped-files)

