---
name: dotnet-async-lite
description: '비동기 프로그래밍 핵심 패턴'
---

# 비동기 프로그래밍 핵심

## 1. Task vs ValueTask

```csharp
// 일반 비동기: Task 사용
public async Task<Data> LoadAsync() { }

// 캐시 히트 빈번: ValueTask 사용
public ValueTask<Data> GetAsync(string key)
{
    if (_cache.TryGetValue(key, out var cached))
        return new ValueTask<Data>(cached);

    return new ValueTask<Data>(LoadFromDbAsync(key));
}
```

## 2. CancellationToken

```csharp
public async Task<Data> LoadAsync(CancellationToken ct = default)
{
    ct.ThrowIfCancellationRequested();
    return await _httpClient.GetFromJsonAsync<Data>(url, ct);
}

// 타임아웃
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
await LongOperationAsync(cts.Token);
```

## 3. 안티패턴

```csharp
// ❌ async void 금지
public async void BadMethod() { }

// ❌ .Result, .Wait() 금지 (데드락)
var result = GetDataAsync().Result;

// ✅ await 사용
var result = await GetDataAsync();
```

> 상세 내용: `/dotnet-async` skill 참조
