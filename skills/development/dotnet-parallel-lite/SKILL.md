---
name: dotnet-parallel-lite
description: '병렬 처리 핵심 패턴'
---

# 병렬 처리 핵심

## 1. Parallel.ForEach

```csharp
var options = new ParallelOptions
{
    MaxDegreeOfParallelism = Environment.ProcessorCount
};

Parallel.ForEach(items, options, item =>
{
    ProcessItem(item);
});
```

## 2. PLINQ

```csharp
var results = data
    .AsParallel()
    .Where(d => d.IsValid)
    .Select(d => Transform(d))
    .ToList();
```

## 3. Thread-Safe 컬렉션

```csharp
// 병렬 처리 중 결과 수집
var results = new ConcurrentBag<Result>();

Parallel.ForEach(data, item =>
{
    results.Add(Process(item));
});
```

## 4. 주의사항

- ⚠️ CPU 바운드: Parallel 사용
- ⚠️ I/O 바운드: async-await 사용

```csharp
// ❌ I/O에 Parallel 사용
Parallel.ForEach(urls, url => httpClient.GetAsync(url).Result);

// ✅ I/O에 async-await 사용
await Task.WhenAll(urls.Select(url => httpClient.GetAsync(url)));
```

> 상세 내용: `/dotnet-parallel` skill 참조
