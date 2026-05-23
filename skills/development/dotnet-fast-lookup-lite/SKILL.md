---
name: dotnet-fast-lookup-lite
description: '고속 탐색 핵심 패턴'
---

# 고속 탐색 핵심

## 1. HashSet<T>

```csharp
// O(1) 존재 여부 확인
var allowedIds = new HashSet<int> { 1, 2, 3, 4, 5 };

if (allowedIds.Contains(userId))
{
    // 허용된 사용자
}
```

## 2. FrozenSet<T> (.NET 8+)

```csharp
using System.Collections.Frozen;

// 불변 고속 탐색
var allowedExtensions = new[] { ".jpg", ".png", ".gif" }
    .ToFrozenSet(StringComparer.OrdinalIgnoreCase);
```

## 3. Dictionary 최적화

```csharp
// ❌ 두 번 조회
if (dict.ContainsKey(key))
    var value = dict[key];

// ✅ 한 번 조회
if (dict.TryGetValue(key, out var value))
{
    // value 사용
}
```

## 4. 사용 시점

| 시나리오 | 권장 컬렉션 |
|----------|--------------|
| 자주 변경되는 집합 | `HashSet<T>` |
| 읽기 전용 설정 | `FrozenSet<T>` |
| Key-Value 캐시 | `Dictionary<K,V>` |

> 상세 내용: `/dotnet-fast-lookup` skill 참조
