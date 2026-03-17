---
name: dto-implementation
description: >
  DTO implementation guidelines for the HMIS project. Use when creating or modifying DTOs,
  writing JPQL constructor queries, implementing DTO-based reports, converting entity code
  to DTO patterns, or troubleshooting DTO query issues. Covers constructor rules, facade
  methods, null relationship handling, and navigation patterns.
user-invocable: true
---

# DTO Implementation Guidelines

## Critical Rules

1. **NEVER modify existing constructors** - only add new ones
2. **Use direct DTO queries** - avoid entity-to-DTO conversion loops
3. **JPQL PERSISTED FIELDS ONLY**: NEVER use derived properties like `nameWithTitle`, `age`, `displayName` in JPQL

## Direct DTO Query Pattern

```java
// CORRECT - Direct DTO query from database
String jpql = "SELECT new com.divudi.core.data.dto.StockDTO("
    + "s.id, s.itemBatch.item.name, s.itemBatch.item.code, "
    + "s.itemBatch.retailsaleRate, s.stock, "
    + "s.itemBatch.dateOfExpire, s.itemBatch.batchNo) "
    + "FROM Stock s WHERE ...";

// MUST use findLightsByJpql() with cast
List<StockDTO> dtos = (List<StockDTO>) facade.findLightsByJpql(jpql, params, TemporalType.TIMESTAMP);
```

```java
// WRONG - Never do entity-to-DTO loops
List<Stock> stocks = stockFacade.findByJpql(sql, params);
List<StockDTO> dtos = new ArrayList<>();
for (Stock stock : stocks) { dtos.add(new StockDTO(stock.getField1(), ...)); }
```

## Navigation Pattern: Use IDs, Not Entities

```java
// CORRECT - IDs and names for navigation
public class OpdSaleSummaryDTO {
    private Long categoryId;      // For navigation
    private String categoryName;  // For display
    private Long itemId;          // For navigation
    private String itemName;      // For display
    private Double total;
}
```

## Null Relationship Handling

Accessing properties through nullable relationships causes **silent query failures** (0 results, no exception):

```java
// WRONG - Fails silently if cancelledBill is null
"b.cancelledBill.createdAt"

// CORRECT - Use LEFT JOIN
"FROM Bill b LEFT JOIN b.cancelledBill cb "
// Then use cb.createdAt with COALESCE
```

## Constructor Rules

- Always use **wrapper types** (`Boolean`, `Integer`, `Long`) for null safety
- Parameter count and order must match JPQL SELECT exactly
- Keep existing constructors intact; add new ones

## Common Non-Persisted Properties (Cannot Use in JPQL)

| Entity | Non-Persisted | Use Instead |
|--------|--------------|-------------|
| Person | nameWithTitle | name (or title, name separately) |
| Person | age | dob (calculate in Java) |
| Item | displayName | name |

For complete reference, read [developer_docs/dto/implementation-guidelines.md](../../developer_docs/dto/implementation-guidelines.md).
