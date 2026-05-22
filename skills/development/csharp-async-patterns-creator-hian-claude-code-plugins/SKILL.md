---
name: csharp-async-patterns
description: Modern C# asynchronous programming patterns using async/await, proper CancellationToken usage, and error handling in async code. Use when guidance needed on async/await best practices, Task composition and coordination, ConfigureAwait usage, ValueTask optimization, or async operation cancellation patterns. Pure .NET framework patterns applicable to any C# application.
requires:
  - csharp-plugin:csharp-code-style
---

# C# Async/Await Patterns

## Overview

C# 비동기 프로그래밍 패턴 (POCU 표준 적용)

**Foundation Required**: `csharp-code-style` (mPascalCase, Async 접미사 금지, var 금지)

**Core Topics**:
- async/await 기본
- CancellationToken 패턴
- ConfigureAwait 사용법
- 비동기 에러 처리
- Task 조합 및 조율
- ValueTask 최적화

## Quick Start

```csharp
public class DataService
{
    private readonly IDataRepository mRepository;
    private readonly ILogger mLogger;

    public DataService(IDataRepository repository, ILogger logger)
    {
        mRepository = repository;
        mLogger = logger;
    }

    // ✅ POCU: Async 접미사 없음
    public async Task<Data> LoadData(CancellationToken ct = default)
    {
        try
        {
            Data data = await mRepository.Fetch(ct);
            return processData(data);
        }
        catch (OperationCanceledException)
        {
            mLogger.Info("Operation cancelled");
            throw;
        }
    }

    private Data processData(Data data)
    {
        Debug.Assert(data != null);
        // Processing logic
        return data;
    }
}
```

## Key Rules (POCU)

### Async 메서드 명명

```csharp
// ❌ WRONG: Async 접미사 사용
public async Task<Order> GetOrderAsync(int id);
public async Task SaveOrderAsync(Order order);

// ✅ CORRECT: Async 접미사 없음
public async Task<Order> GetOrder(int id);
public async Task SaveOrder(Order order);
```

### async void 금지

```csharp
// ❌ WRONG: async void
public async void LoadData()
{
    await mRepository.Fetch();
}

// ✅ CORRECT: async Task
public async Task LoadData()
{
    await mRepository.Fetch();
}

// ⚠️ EXCEPTION: 이벤트 핸들러만 async void 허용
private async void OnButtonClick(object sender, EventArgs e)
{
    try
    {
        await ProcessClick();
    }
    catch (Exception ex)
    {
        mLogger.Error(ex, "Click handler failed");
    }
}
```

### 명시적 타입 사용

```csharp
// ❌ WRONG: var 사용
var result = await GetOrder(1);
var tasks = new List<Task>();

// ✅ CORRECT: 명시적 타입
Order result = await GetOrder(1);
List<Task> tasks = new List<Task>();
```

### using 문 사용

```csharp
// ❌ WRONG: using 선언
using CancellationTokenSource cts = new CancellationTokenSource(timeout);

// ✅ CORRECT: using 문
using (CancellationTokenSource cts = new CancellationTokenSource(timeout))
{
    return await LoadData(cts.Token);
}
```

## CancellationToken 패턴

```csharp
public class OrderProcessor
{
    private readonly IOrderRepository mRepository;

    // 항상 CancellationToken 지원
    public async Task<Order> ProcessOrder(int orderId, CancellationToken ct = default)
    {
        ct.ThrowIfCancellationRequested();

        Order order = await mRepository.GetOrder(orderId, ct);
        Debug.Assert(order != null);

        await validateOrder(order, ct);
        await calculateTotal(order, ct);
        await mRepository.SaveOrder(order, ct);

        return order;
    }

    private async Task validateOrder(Order order, CancellationToken ct)
    {
        Debug.Assert(order != null);
        await mRepository.ValidateInventory(order.Items, ct);
    }

    private async Task calculateTotal(Order order, CancellationToken ct)
    {
        Debug.Assert(order != null);
        decimal total = 0;
        foreach (OrderItem item in order.Items)
        {
            ct.ThrowIfCancellationRequested();
            total += item.Price * item.Quantity;
        }
        order.Total = total;
    }
}
```

## Reference Documentation

### [Best Practices](references/best-practices.md)
Essential patterns for async/await:
- CancellationToken 사용 패턴
- ConfigureAwait 가이드라인
- async void 회피
- 예외 처리

### [Code Examples](references/code-examples.md)
Comprehensive code examples:
- 기본 비동기 작업
- 병렬 실행 패턴
- 타임아웃 및 재시도
- 고급 패턴

### [Anti-Patterns](references/anti-patterns.md)
Common mistakes to avoid:
- .Result, .Wait() 차단
- Fire-and-forget 오류 처리 누락
- CancellationToken 미전파

## Key Principles

1. **Async All the Way**: 비동기 호출 체인 유지
2. **Always Support Cancellation**: 장기 실행 작업은 CancellationToken 필수
3. **ConfigureAwait in Libraries**: 라이브러리 코드에서 ConfigureAwait(false) 사용
4. **No Async Suffix**: POCU 표준 - Async 접미사 금지
5. **No async void**: 이벤트 핸들러 외 async void 금지
6. **Explicit Types**: var 대신 명시적 타입 사용
