---
name: dotnet-async
description: '.NET 비동기 프로그래밍 패턴 (Task, ValueTask, ConfigureAwait)'
---

# .NET 비동기 프로그래밍

효율적인 비동기 프로그래밍을 위한 API 및 패턴 가이드입니다.

## 1. 핵심 API

| API | 용도 |
|-----|------|
| `Task` | 비동기 작업 (반환값 없음) |
| `Task<T>` | 비동기 작업 (반환값 있음) |
| `ValueTask<T>` | 고빈도 호출 최적화 |
| `IAsyncEnumerable<T>` | 비동기 스트림 |

---

## 2. Task vs ValueTask

### 2.1 Task<T> 사용 시점

- 대부분의 비동기 작업
- 항상 실제 비동기 작업이 발생하는 경우

### 2.2 ValueTask<T> 사용 시점

- 동기적 완료가 빈번한 경우 (캐시 히트)
- 고빈도 호출 메서드

```csharp
// 캐시 히트가 빈번한 경우 ValueTask 사용
public ValueTask<Data> GetDataAsync(string key)
{
    if (_cache.TryGetValue(key, out var cached))
    {
        // 동기적 반환 (Heap 할당 없음)
        return new ValueTask<Data>(cached);
    }

    // 비동기 작업 필요 시
    return new ValueTask<Data>(LoadFromDbAsync(key));
}
```

### 2.3 ValueTask 주의사항

```csharp
// ❌ 나쁜 예: ValueTask를 여러 번 await
var task = GetDataAsync("key");
var result1 = await task;
var result2 = await task; // 오류 발생 가능!

// ✅ 좋은 예: 한 번만 await
var result = await GetDataAsync("key");
```

---

## 3. ConfigureAwait

```csharp
// 라이브러리에서는 ConfigureAwait(false) 사용
public async Task<string> FetchDataAsync()
{
    var response = await _httpClient.GetAsync(url)
        .ConfigureAwait(false);
    return await response.Content.ReadAsStringAsync()
        .ConfigureAwait(false);
}
```

---

## 4. 비동기 스트림 (IAsyncEnumerable)

```csharp
public async IAsyncEnumerable<Data> GetDataStreamAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var item in _source.ReadAllAsync(ct))
    {
        yield return await ProcessAsync(item);
    }
}

// 소비
await foreach (var data in GetDataStreamAsync(ct))
{
    Console.WriteLine(data);
}
```

---

## 5. 취소 토큰 (CancellationToken)

```csharp
public async Task<Data> LoadDataAsync(CancellationToken ct = default)
{
    ct.ThrowIfCancellationRequested();
    return await _httpClient.GetFromJsonAsync<Data>(url, ct);
}

// 타임아웃 설정
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
await LongRunningOperationAsync(cts.Token);
```

---

## 6. 동시성 제어

```csharp
private readonly SemaphoreSlim _semaphore = new(maxCount: 10);

public async Task ProcessWithThrottlingAsync(Data data)
{
    await _semaphore.WaitAsync();
    try
    {
        await ProcessAsync(data);
    }
    finally
    {
        _semaphore.Release();
    }
}
```

---

## 7. 안티패턴

```csharp
// ❌ async void 금지 (예외 처리 불가)
public async void BadMethod() { }

// ✅ async Task
public async Task GoodMethod() { }

// ❌ .Result, .Wait() 금지 (데드락 위험)
var result = GetDataAsync().Result;

// ✅ await 사용
var result = await GetDataAsync();

// ❌ 불필요한 async/await
public async Task<Data> GetDataAsync()
{
    return await _repository.GetAsync();
}

// ✅ 직접 반환
public Task<Data> GetDataAsync()
{
    return _repository.GetAsync();
}
```

---

## 8. 참고 문서

- [Task-based Asynchronous Pattern](https://learn.microsoft.com/en-us/dotnet/standard/asynchronous-programming-patterns/task-based-asynchronous-pattern-tap)
- [ValueTask](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask-1)
