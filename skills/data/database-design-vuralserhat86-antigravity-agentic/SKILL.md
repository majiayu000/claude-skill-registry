---
name: database-design-vuralserhat86-antigravity-agentic
description: '> Schema tasarımı, migration ve query optimization rehberi.'
---

---
name: database_design
router_kit: FullStackKit
description: Schema tasarımı, migration stratejileri, indexing, query optimization ve database best practices.
metadata:
  skillport:
    category: development
    tags: [accessibility, api integration, backend, browser apis, client-side, components, css3, database design, debugging, deployment, frameworks, frontend, fullstack, html5, javascript, libraries, node.js, npm, performance optimization, responsive design, seo, state management, testing, typescript, ui/ux, web development]      - optimization
---

# 🗄️ Database Design

> Schema tasarımı, migration ve query optimization rehberi.

---

## 📋 İçindekiler

1. [Schema Tasarım Prensipleri](#1-schema-tasarım-prensipleri)
2. [Normalization](#2-normalization)
3. [Indexing Stratejileri](#3-indexing-stratejileri)
4. [Query Optimization](#4-query-optimization)
5. [Migration Best Practices](#5-migration-best-practices)
6. [NoSQL Patterns](#6-nosql-patterns)

---

## 1. Schema Tasarım Prensipleri

### Naming Conventions
```sql
-- Tablolar: snake_case, çoğul
CREATE TABLE users (...);
CREATE TABLE order_items (...);

-- Kolonlar: snake_case
user_id, created_at, is_active

-- Primary Key: id veya table_id
id SERIAL PRIMARY KEY
-- veya
user_id UUID PRIMARY KEY

-- Foreign Key: referenced_table_id
user_id INTEGER REFERENCES users(id)
```

### Temel Kolon Tipleri
| Veri | PostgreSQL | MySQL |
|------|------------|-------|
| ID | `UUID` / `SERIAL` | `CHAR(36)` / `INT AUTO_INCREMENT` |
| Text (kısa) | `VARCHAR(255)` | `VARCHAR(255)` |
| Text (uzun) | `TEXT` | `TEXT` |
| Tarih | `TIMESTAMP WITH TIME ZONE` | `DATETIME` |
| Boolean | `BOOLEAN` | `TINYINT(1)` |
| JSON | `JSONB` | `JSON` |
| Para | `DECIMAL(19,4)` | `DECIMAL(19,4)` |

---

## 2. Normalization

### Normal Formlar
| Form | Kural | Örnek |
|------|-------|-------|
| 1NF | Atomik değerler | `address` → `street`, `city`, `zip` |
| 2NF | Tam bağımlılık | Composite key parçalama |
| 3NF | Transitif bağımlılık yok | `user.department_name` → ayrı tablo |

### Denormalization Durumları
- Read-heavy workload
- Reporting/analytics tabloları
- Cache tabloları
- Aggregation sonuçları

---

## 3. Indexing Stratejileri

### Index Tipleri
```sql
-- B-Tree (varsayılan, genel amaçlı)
CREATE INDEX idx_users_email ON users(email);

-- Composite Index (sıra önemli!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Partial Index (koşullu)
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- Unique Index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- GIN/GiST (full-text, JSON, array)
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);
```

### Index Seçim Kuralları
```
✅ Index Ekle:
- WHERE clause'da sık kullanılan kolonlar
- JOIN kolonları (foreign keys)
- ORDER BY kolonları
- Unique constraint gereken kolonlar

❌ Index Ekleme:
- Düşük cardinality (boolean, enum)
- Sık güncellenen kolonlar
- Küçük tablolar (<1000 row)
```

---

## 4. Query Optimization

### EXPLAIN Analizi
```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 123
AND created_at > '2025-01-01';
```

### Optimization Teknikleri
```sql
-- ❌ YANLIŞ: SELECT *
SELECT * FROM users;

-- ✅ DOĞRU: Sadece gerekli kolonlar
SELECT id, name, email FROM users;

-- ❌ YANLIŞ: N+1 query
FOR user IN users:
    SELECT * FROM orders WHERE user_id = user.id

-- ✅ DOĞRU: JOIN veya IN
SELECT * FROM orders WHERE user_id IN (1, 2, 3);

-- ❌ YANLIŞ: Function on indexed column
SELECT * FROM users WHERE YEAR(created_at) = 2025;

-- ✅ DOĞRU: Range query
SELECT * FROM users
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
```

### Pagination
```sql
-- Offset-based (küçük veri setleri)
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;

-- Cursor-based (büyük veri setleri, önerilen)
SELECT * FROM users
WHERE id > :last_id
ORDER BY id
LIMIT 20;
```

---

## 5. Migration Best Practices

### Dosya Yapısı
```
migrations/
├── 001_create_users_table.sql
├── 002_add_email_to_users.sql
├── 003_create_orders_table.sql
└── 004_add_index_orders_user_id.sql
```

### Güvenli Migration Kuralları
```sql
-- ✅ Backward compatible
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- ⚠️ Dikkatli ol (default value gerekli)
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- ❌ Tehlikeli (prodda direkt yapma)
ALTER TABLE users DROP COLUMN old_field;
DROP TABLE deprecated_table;
```

### Zero-Downtime Migration
1. Yeni kolon ekle (nullable)
2. Dual-write başlat
3. Data migration yap
4. Yeni kolonu NOT NULL yap
5. Eski kolonu kaldır

---

## 6. NoSQL Patterns

### MongoDB Schema Design
```javascript
// Embedded (1:few, read-heavy)
{
  _id: ObjectId("..."),
  name: "John",
  addresses: [
    { street: "123 Main", city: "NYC" },
    { street: "456 Oak", city: "LA" }
  ]
}

// Referenced (1:many, write-heavy)
// users collection
{ _id: ObjectId("..."), name: "John" }

// orders collection
{ _id: ObjectId("..."), user_id: ObjectId("..."), total: 100 }
```

### Redis Data Structures
```
STRING  → Cache, session
HASH    → Object storage
LIST    → Queue, timeline
SET     → Tags, unique items
ZSET    → Leaderboard, ranking
```

---

*Database Design v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [System Design Primer - Database](https://github.com/donnemartin/system-design-primer#database)

### Aşama 1: Requirements & Modeling
- [ ] **Access Patterns**: Veri nasıl okunacak? (Read-heavy vs Write-heavy).
- [ ] **Conceptual**: Varlıkları (Entities) ve ilişkileri (ER Diagram) çiz.
- [ ] **Engine**: İlişkisel (Postgres) mi NoSQL (Mongo/Redis) mi karar ver.

### Aşama 2: Logical Design
- [ ] **Normalization**: 3NF'e kadar normalize et. (Performans için denormalize edilecek alanları belirle).
- [ ] **Constraints**: Foreign Key, Unique, Not Null kısıtlarını tanımla.
- [ ] **Indices**: Sorgu desenlerine göre index planı yap.

### Aşama 3: Physical Implementation
- [ ] **Migration**: SQL dosyalarını oluştur (V1__init.sql).
- [ ] **Capacity**: veri tiplerini (INT vs BIGINT, VARCHAR vs TEXT) optimize et.
- [ ] **Security**: Rol tabanlı erişim (RLS) ve şifreleme ayarlarını yap.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | ER diyagramı tüm use-case'leri kapsıyor mu? |
| 2 | Her tablo için Primary Key var mı? |
| 3 | EXPLAIN ile sorgu maliyetleri kontrol edildi mi? |
