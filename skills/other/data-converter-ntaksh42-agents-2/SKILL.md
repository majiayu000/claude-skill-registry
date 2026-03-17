---
name: data-converter
description: Convert data between formats (JSON, XML, CSV, YAML, TOML). Use when transforming data structures or migrating between data formats.
---

# Data Converter Skill

データ形式を変換するスキルです。

## 概要

JSON、YAML、XML、CSV、TOML等の各種データ形式を相互変換します。

## 主な機能

- **多様な形式**: JSON ↔ YAML ↔ XML ↔ CSV ↔ TOML ↔ INI
- **データ検証**: スキーマバリデーション
- **整形**: インデント、ソート、圧縮
- **フィルタリング**: 特定フィールドの抽出
- **変換**: キャメルケース ↔ スネークケース
- **マージ**: 複数ファイルの統合

## 使用方法

```
以下のJSONをYAMLに変換：

{
  "name": "John",
  "age": 30
}
```

## 変換例

### JSON → YAML

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "credentials": {
      "username": "admin",
      "password": "secret"
    }
  }
}
```

↓

```yaml
database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secret
```

### CSV → JSON

```csv
name,age,city
John,30,Tokyo
Jane,25,Osaka
```

↓

```json
[
  {"name": "John", "age": 30, "city": "Tokyo"},
  {"name": "Jane", "age": 25, "city": "Osaka"}
]
```

### XML → JSON

```xml
<user>
  <name>John</name>
  <age>30</age>
  <email>john@example.com</email>
</user>
```

↓

```json
{
  "user": {
    "name": "John",
    "age": 30,
    "email": "john@example.com"
  }
}
```

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
