---
description: 同花顺经济数据库（EDB）接口，通过指标代码查询宏观经济、行业、国际等经济数据。当用户需要查询 GDP、CPI、PMI 等宏观指标的历史序列时使用。
---

# ths-edb-skill

同花顺 EDB（经济数据库）JS 封装。

## 核心能力

- 宏观经济指标查询（GDP、CPI、PMI、M2 等）
- 行业经济数据
- 国际经济数据
- 按指标代码 + 日期范围查询

## 依赖

- ths-skill（同花顺底层认证）

## 数据源

- 同花顺 iFinD EDB API（/api/v1/edb_service）

## 使用

```bash
node "$SKILLS_ROOT/ths-edb-skill/index.js" --indicator M001 --start 2024-01-01 --end 2026-03-17
```

## 注意

- 需要同花顺 iFinD 账号和 ACCESS_TOKEN
