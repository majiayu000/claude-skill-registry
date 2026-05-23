---
name: dotnet-fast-lookup
description: '.NET 고속 탐색 패턴 (HashSet, FrozenSet, Dictionary 최적화)'
---

# .NET 고속 탐색

O(1) 시간 복잡도를 활용한 고속 탐색 API 가이드입니다.

## 1. 핵심 API

| API | 시간 복잡도 | 특징 |
|-----|------------|------|
| `HashSet<T>` | O(1) | 가변, 중복 불가 |
| `FrozenSet<T>` | O(1) | 불변, .NET 8+ |
| `Dictionary<K,V>` | O(1) | 가변, Key-Value |
| `FrozenDictionary<K,V>` | O(1) | 불변, .NET 8+ |

---

## 2. HashSet<T>

```csharp
// O(1) 시간 복잡도로 존재 여부 확인
var allowedIds = new HashSet<int> { 1, 2, 3, 4, 5 };

if (allowedIds.Contains(userId))
{
    // 허용된 사용자
}

// 집합 연산
setA.IntersectWith(setB); // 교집합
setA.UnionWith(setB);     // 합집합
setA.ExceptWith(setB);    // 차집합
```

---

## 3. FrozenSet<T> (.NET 8+)

```csharp
using System.Collections.Frozen;

// 불변 고속 탐색 (읽기 전용 시나리오)
var allowedExtensions = new[] { ".jpg", ".png", ".gif" }
    .ToFrozenSet(StringComparer.OrdinalIgnoreCase);

if (allowedExtensions.Contains(fileExtension))
{
    // 허용된 확장자
}
```

---

## 4. Dictionary<K,V> 최적화

```csharp
// ❌ 두 번 조회
if (dict.ContainsKey(key))
{
    var value = dict[key];
}

// ✅ 한 번 조회
if (dict.TryGetValue(key, out var value))
{
    // value 사용
}

// 기본값과 함께 조회
var value = dict.GetValueOrDefault(key, defaultValue);
```

---

## 5. 비교자 (Comparer) 최적화

```csharp
// 문자열 대소문자 무시 비교
var set = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
set.Add("Hello");
set.Contains("HELLO"); // true
```

---

## 6. 사용 시점

| 시나리오 | 권장 컬렉션 |
|----------|------------|
| 자주 변경되는 집합 | `HashSet<T>` |
| 읽기 전용 설정 데이터 | `FrozenSet<T>` |
| 빈번한 존재 여부 확인 | `HashSet<T>` / `FrozenSet<T>` |
| Key-Value 캐시 | `Dictionary<K,V>` |
| 정적 매핑 테이블 | `FrozenDictionary<K,V>` |

---

## 7. 참고 문서

- [HashSet<T>](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.hashset-1)
- [FrozenSet<T>](https://learn.microsoft.com/en-us/dotnet/api/system.collections.frozen.frozenset-1)
