---
name: dotnet-parallel
description: '.NET 병렬 처리 패턴 (Parallel, PLINQ, ConcurrentCollections)'
---

# .NET 병렬 처리

CPU 바운드 작업의 병렬 처리를 위한 API 및 패턴 가이드입니다.

## 1. 핵심 API

| API | 용도 |
|-----|------|
| `Parallel.For`, `Parallel.ForEach` | CPU 바운드 병렬 처리 |
| `PLINQ (.AsParallel())` | LINQ 쿼리 병렬화 |
| `Partitioner<T>` | 대용량 데이터 파티셔닝 |
| `ConcurrentDictionary<K,V>` | Thread-safe 딕셔너리 |

---

## 2. Parallel 클래스

### 2.1 Parallel.ForEach

```csharp
public sealed class ImageProcessor
{
    public void ProcessImages(IEnumerable<string> imagePaths)
    {
        var options = new ParallelOptions
        {
            MaxDegreeOfParallelism = Environment.ProcessorCount
        };

        Parallel.ForEach(imagePaths, options, path =>
        {
            ProcessImage(path);
        });
    }
}
```

### 2.2 조기 중단

```csharp
Parallel.For(0, data.Length, (i, state) =>
{
    if (data[i] == target)
    {
        state.Break();
    }
});
```

---

## 3. PLINQ

```csharp
var results = data
    .AsParallel()
    .WithDegreeOfParallelism(Environment.ProcessorCount)
    .Where(d => d.IsValid)
    .Select(d => Transform(d))
    .ToList();

// 순서 유지 필요 시
var results = data
    .AsParallel()
    .AsOrdered()
    .Select(d => Process(d))
    .ToList();
```

---

## 4. Thread-Safe 컬렉션

| 컬렉션 | 용도 |
|--------|------|
| `ConcurrentDictionary<K,V>` | Thread-safe 딕셔너리 |
| `ConcurrentQueue<T>` | Thread-safe FIFO 큐 |
| `ConcurrentBag<T>` | Thread-safe 순서 없는 컬렉션 |

```csharp
// 병렬 처리 중 결과 수집
var results = new ConcurrentBag<Result>();

Parallel.ForEach(data, item =>
{
    var result = Process(item);
    results.Add(result);
});
```

---

## 5. ThreadLocal<T>

스레드별 독립 변수로 경합 방지

```csharp
private readonly ThreadLocal<StringBuilder> _localBuilder =
    new(() => new StringBuilder());

public void ProcessInParallel()
{
    Parallel.For(0, 1000, i =>
    {
        var sb = _localBuilder.Value!;
        sb.Clear();
        sb.Append(i);
    });
}
```

---

## 6. 주의사항

### ⚠️ 병렬 처리 vs 비동기

- **CPU 바운드**: Parallel 사용
- **I/O 바운드**: async-await 사용

```csharp
// ❌ I/O 작업에 Parallel 사용
Parallel.ForEach(urls, url => httpClient.GetAsync(url).Result);

// ✅ I/O 작업에 async-await 사용
await Task.WhenAll(urls.Select(url => httpClient.GetAsync(url)));
```

### ⚠️ 공유 상태 동기화

```csharp
// ❌ 일반 컬렉션에 병렬 쓰기
var list = new List<int>();
Parallel.For(0, 1000, i => list.Add(i)); // Race condition!

// ✅ Thread-safe 컬렉션 사용
var bag = new ConcurrentBag<int>();
Parallel.For(0, 1000, i => bag.Add(i));
```

---

## 7. 참고 문서

- [Parallel Class](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel)
- [PLINQ](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/introduction-to-plinq)
