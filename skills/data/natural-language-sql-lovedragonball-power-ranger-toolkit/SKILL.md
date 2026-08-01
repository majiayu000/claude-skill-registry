---
name: natural-language-sql
description: แปลง natural language เป็น SQL queries และอธิบาย SQL ด้วยภาษาธรรมดา
---

# 🗄️ Natural Language SQL Skill

---
name: natural-language-sql
description: Convert natural language queries to SQL and explain SQL in plain language
---

## 🎯 Purpose

แปลง natural language เป็น SQL queries และอธิบาย SQL ด้วยภาษาธรรมดา

## 📋 When to Use

- Write SQL from descriptions
- Explain existing queries
- Learn SQL syntax
- Quick data exploration
- Non-technical stakeholders

## 🔧 Translation Examples

### Simple Queries
```
"แสดงรายชื่อลูกค้าทั้งหมด"
↓
SELECT * FROM customers;

"หาลูกค้าที่ชื่อ John"
↓
SELECT * FROM customers WHERE name = 'John';
```

### Aggregations
```
"นับจำนวนออเดอร์ทั้งหมด"
↓
SELECT COUNT(*) FROM orders;

"ยอดขายรวมต่อเดือน"
↓
SELECT
  DATE_TRUNC('month', created_at) AS month,
  SUM(total) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;
```

### Joins
```
"ออเดอร์พร้อมชื่อลูกค้า"
↓
SELECT o.*, c.name AS customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.id;
```

### Complex Queries
```
"Top 10 ลูกค้าที่ซื้อมากที่สุดในปี 2024"
↓
SELECT
  c.name,
  SUM(o.total) AS total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.created_at >= '2024-01-01'
GROUP BY c.id, c.name
ORDER BY total_spent DESC
LIMIT 10;
```

## 📊 SQL Patterns

| Natural Language | SQL Pattern |
|-----------------|-------------|
| ทั้งหมด | `SELECT *` |
| กรอง/ที่มี | `WHERE` |
| เรียงตาม | `ORDER BY` |
| จำนวน/รวม | `COUNT/SUM` |
| เฉลี่ย | `AVG` |
| กลุ่ม | `GROUP BY` |
| เชื่อม | `JOIN` |
| ไม่ซ้ำ | `DISTINCT` |
| จำกัด | `LIMIT` |

## 📝 Explain SQL

```sql
-- Input SQL
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.created_at >= '2024-01-01'
GROUP BY c.id, c.name
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC;
```

**Explanation:**
1. ดึงชื่อลูกค้าและนับจำนวนออเดอร์
2. เชื่อมตาราง customers กับ orders (รวมลูกค้าที่ไม่มีออเดอร์)
3. กรองเฉพาะออเดอร์ตั้งแต่ปี 2024
4. จัดกลุ่มตามลูกค้า
5. แสดงเฉพาะลูกค้าที่มีมากกว่า 5 ออเดอร์
6. เรียงจากมากไปน้อย

## ✅ Best Practices

- [ ] Use parameterized queries
- [ ] Avoid SELECT *
- [ ] Index frequently filtered columns
- [ ] Limit results
- [ ] Test on small dataset first

## 🔗 Related Skills

- `database-management` - DB operations
- `data-analysis` - Analyze results
- `api-design` - SQL in APIs
