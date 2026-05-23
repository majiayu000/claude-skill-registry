---
name: csharp-code-style
description: C# code style and naming conventions based on POCU standards. Covers naming rules (mPascalCase for private, bBoolean prefix, EEnum prefix), code organization, C# 9.0 patterns. Use PROACTIVELY for C# code reviews, refactoring, or establishing project standards.
---

# C# Code Style Guide

## Overview

C# 코딩 표준 (POCU 기반, C# 9.0 기준)

**Core Topics**:
- 명명 규칙 (m접두어, b접두어, E/S접두어)
- 코드 작성 규칙
- 클래스 구조 순서
- C# 9.0 패턴

## Naming Conventions

### Quick Reference

| Element | Convention | Example |
|---------|-----------|---------|
| Class | PascalCase | `PlayerManager`, `OrderService` |
| Struct | SPascalCase | `SUserID`, `SPlayerData` |
| Interface | IPascalCase | `IDisposable`, `IOrderService` |
| Enum | EPascalCase | `EDirection`, `EOrderStatus` |
| Method (public) | PascalCase (동사+명사) | `GetAge()`, `ProcessOrder()` |
| Method (private) | camelCase | `getAge()`, `processOrder()` |
| Property | PascalCase | `Name`, `OrderID` |
| Private Field | mPascalCase | `mAge`, `mOrderRepository` |
| Local Variable | camelCase | `totalAmount`, `isValid` |
| Parameter | camelCase | `customerId`, `orderDate` |
| Constant | ALL_CAPS | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| Static readonly | ALL_CAPS | `MY_CONST_OBJECT` |
| Boolean Variable | bCamelCase / mbPascalCase | `bFired`, `mbIsEnabled` |
| Boolean Property | Is/Has/Can/Should | `IsFired`, `HasChildren` |

### Private Member Pattern

```csharp
public class OrderService
{
    // Private fields: m + PascalCase
    private readonly IOrderRepository mOrderRepository;
    private readonly ILogger mLogger;
    private int mRetryCount;
    private bool mbIsProcessing;  // boolean: mb prefix

    // Constructor parameter: camelCase (no prefix)
    public OrderService(IOrderRepository orderRepository, ILogger logger)
    {
        mOrderRepository = orderRepository;
        mLogger = logger;
    }

    // Public method: PascalCase
    public Order GetOrder(int orderId)
    {
        return getOrderInternal(orderId);
    }

    // Private method: camelCase
    private Order getOrderInternal(int orderId)
    {
        return mOrderRepository.Find(orderId);
    }
}
```

### Enum and Struct Prefixes

```csharp
// Enum: E prefix
public enum EDirection
{
    None,
    North,
    South,
    East,
    West
}

// Bit flags enum: Flags suffix
[Flags]
public enum EVisibilityFlags
{
    None = 0,
    Visible = 1,
    Hidden = 2,
    Collapsed = 4
}

// Struct: S prefix (readonly struct는 제외 가능)
public struct SUserID
{
    public int Value { get; }
}

// readonly record struct: S prefix 불필요
public readonly record struct UserID(int Value);
```

### Nullable Naming

```csharp
// Nullable parameter: OrNull suffix
public Animation GetAnimation(string nameOrNull)
{
    if (nameOrNull == null)
    {
        return DefaultAnimation;
    }
    return mAnimations[nameOrNull];
}

// Nullable return: OrNull suffix
public string GetNameOrNull()
{
    return mbHasName ? mName : null;
}

// Recursive function: Recursive suffix
public int FibonacciRecursive(int n)
{
    if (n <= 1)
    {
        return n;
    }
    return FibonacciRecursive(n - 1) + FibonacciRecursive(n - 2);
}
```

## Code Writing Rules

### Prohibited Patterns

```csharp
// [WRONG] var keyword
var order = GetOrder(1);
var items = new List<Item>();

// [CORRECT] Explicit type
Order order = GetOrder(1);
List<Item> items = new List<Item>();

// [WRONG] Null coalescing operator (??)
string name = inputName ?? "Default";

// [CORRECT] Explicit null check
string name;
if (inputName != null)
{
    name = inputName;
}
else
{
    name = "Default";
}

// [WRONG] using declaration (C# 8.0)
using FileStream stream = new FileStream(path, FileMode.Open);

// [CORRECT] using statement
using (FileStream stream = new FileStream(path, FileMode.Open))
{
    // ...
}

// [WRONG] target-typed new()
List<Order> orders = new();

// [CORRECT] Explicit type
List<Order> orders = new List<Order>();

// [WRONG] Async suffix
public async Task<Order> GetOrderAsync(int id);

// [CORRECT] No Async suffix
public async Task<Order> GetOrder(int id);

// [WRONG] inline out declaration
if (int.TryParse(input, out int result))

// [CORRECT] separate out declaration
int result;
if (int.TryParse(input, out result))
```

### Required Patterns

```csharp
// Always use braces, even for single line
if (condition)
{
    DoSomething();
}

// Float literals with f suffix
float value = 0.5f;
float another = 1.0f;

// Switch must have default case
switch (status)
{
    case EStatus.Active:
        Process();
        break;
    case EStatus.Inactive:
        Skip();
        break;
    default:
        Debug.Fail("Unknown status");
        break;
}

// Debug.Assert for all assumptions
Debug.Assert(order != null, "Order should not be null");
Debug.Assert(count > 0, "Count must be positive");

// Properties instead of getter/setter methods
// [WRONG]
public int GetAge() { return mAge; }
public void SetAge(int age) { mAge = age; }

// [CORRECT] (.NET 5+ only - NOT available in Unity)
public int Age { get; private init; }

// [CORRECT] (Unity compatible)
public int Age { get; private set; }
```

### C# 9.0 Patterns

> **Unity Limitation**: `init` accessor is NOT available in Unity (requires .NET 5+ runtime).
> See [Modern Patterns Reference](references/modern-patterns.md#unity-runtime-limitations) for details and alternatives.

```csharp
// private init (C# 9.0) - .NET 5+ only, NOT available in Unity
public class Customer
{
    public string Name { get; private init; }  // Use 'private set' in Unity
    public string Email { get; private init; }
}

// Record for immutable data
public record OrderDto(int Id, string CustomerName, decimal TotalAmount);

// Pattern matching switch expression (available in Unity)
public string GetStatusMessage(EOrderStatus status)
{
    return status switch
    {
        EOrderStatus.Pending => "Order is pending",
        EOrderStatus.Completed => "Order completed",
        _ => throw new ArgumentOutOfRangeException(nameof(status))
    };
}
```

## Class Structure Order

```csharp
public class OrderService : IOrderService
{
    // 1. Constants
    private const int MAX_RETRY_COUNT = 3;
    public static readonly TimeSpan DEFAULT_TIMEOUT = TimeSpan.FromSeconds(30);

    // 2. Private member variables
    private readonly IOrderRepository mOrderRepository;
    private readonly ILogger mLogger;
    private int mProcessedCount;
    private bool mbIsInitialized;

    // 3. Properties (with private member above if needed)
    public int ProcessedCount => mProcessedCount;
    public bool IsInitialized => mbIsInitialized;

    // 4. Constructors
    public OrderService(IOrderRepository orderRepository, ILogger logger)
    {
        mOrderRepository = orderRepository;
        mLogger = logger;
    }

    // 5. Public methods
    public Order GetOrder(int id)
    {
        Debug.Assert(id > 0, "ID must be positive");
        return mOrderRepository.Find(id);
    }

    public void ProcessOrder(Order order)
    {
        validateOrder(order);
        processInternal(order);
    }

    // 6. Private methods
    private void validateOrder(Order order)
    {
        Debug.Assert(order != null);
    }

    private void processInternal(Order order)
    {
        // Implementation
    }
}
```

## File Organization

- 각 클래스는 독립된 파일에 작성
- 파일명 = 클래스명 (정확히 일치)
- Partial 클래스: `ClassName.SubName.cs`

## Reference Documentation

### [Naming Conventions](references/naming-conventions.md)
Complete naming rules:
- m/mb 접두어 상세
- E/S 접두어 규칙
- OrNull 접미어 패턴
- ALL_CAPS 상수 규칙

### [Modern Patterns](references/modern-patterns.md)
C# 9.0 language features:
- Records and init-only properties
- Pattern matching
- File-scoped namespaces (C# 10)
- 금지 패턴 상세

### [Error Handling](references/error-handling.md)
Error handling patterns:
- Debug.Assert 사용
- 경계에서만 예외 처리
- null 반환/매개변수 회피
- 유효성 검증 패턴

## Key Principles

1. **가독성 최우선**: 명확하고 이해하기 쉬운 코드 작성
2. **명시적 타입**: `var` 사용 금지, 타입 명시
3. **Null 안전**: OrNull 접미어로 nullable 명시
4. **Assertion**: 모든 가정에 Debug.Assert 사용
5. **경계 검증**: 외부 데이터는 경계에서만 검증
6. **Use init**: Prefer C# 9.0 private init (.NET 5+ only, NOT available in Unity)
7. **No Emoji**: 코드 예제 및 문서에서 이모지 사용 금지, 텍스트 태그 사용 ([WRONG], [CORRECT], [CAUTION])
