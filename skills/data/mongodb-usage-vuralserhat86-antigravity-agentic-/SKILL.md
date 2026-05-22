---
name: mongodb_usage
router_kit: FullStackKit
description: This skill should be used when user asks to "query MongoDB", "show database collections", "get collection schema", "list MongoDB databases", "search records in MongoDB", or "check database indexes".
metadata:
  skillport:
    category: auto-healed
    tags: [aggregation, big data, cleaning, csv, data analysis, data engineering, data science, database, documents, etl pipelines, export, import, json, machine learning basics, migration, mongodb usage, mongoose, nosql, numpy, pandas, python data stack, query optimization, reporting, schema design, sharding, sql, statistics, transformation, visualization]
---

# MongoDB MCP Usage

Use the MongoDB MCP server to integrate database queries into workflows.

## Read-Only Access

MongoDB MCP is configured in read-only mode. Only queries and data retrieval are supported. No write, update, or delete operations.

## Database Queries

Use `mcp__mongodb__*` tools for:

- Listing databases
- Viewing collection schemas
- Querying collection data
- Analyzing indexes

## Integration Pattern

1. List available databases with `mcp__mongodb__list_databases`
2. Explore collections with `mcp__mongodb__list_collections`
3. Get schema information with `mcp__mongodb__get_collection_schema`
4. Query data as needed for analysis
5. Format results for user consumption

## Environment Variables

MongoDB MCP requires:

- `MONGODB_URI` - Connection string (mongodb://...)

Configure in shell before using the plugin.

## Cost Considerations

- Minimize database calls when possible
- Use schema queries before running analysis queries
- Cache results locally if multiple calls needed
*MongoDB Usage v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [MongoDB Performance Best Practices](https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/)

### Aşama 1: Discovery & Inspection
- [ ] **Connection**: `mcp__mongodb__list_databases` ile erişimi doğrula.
- [ ] **Schema Analysis**: `mcp__mongodb__get_collection_schema` ile veri tiplerini ve yapıyı anla.
- [ ] **Index Check**: Mevcut indeksleri listele (`list_indexes` veya benzeri sorgu ile).

### Aşama 2: Query Construction
- [ ] **Filter**: Sorguları indeksli alanlar (Prefix) üzerinden filtrele.
- [ ] **Projection**: Sadece gerekli alanları (`{ field: 1 }`) seç (Network ve RAM tasarrufu).
- [ ] **Aggregation**: Karmaşık analizler için `$match`, `$group`, `$project` pipeline'ını kur.

### Aşama 3: Performance Check (Explain Plan)
- [ ] **Explain**: Sorgunun `COLLSCAN` (Tam tarama) mı `IXSCAN` (Index tarama) mı yaptığını kontrol et.
- [ ] **Optimization**: Yavaş sorgular için bileşik indeks (Compound Index) öner.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Sorgu 100ms'in altında cevap veriyor mu? |
| 2 | "In-memory sort" limiti aşılıyor mu (disk kullanımı var mı)? |
| 3 | Regex sorguları indeksin başlangıcını (anchor `^...`) kullanıyor mu? |
