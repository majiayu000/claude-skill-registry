---
name: markdown-table-generator
description: Generate well-formatted markdown tables from data. Use when creating documentation tables or formatting tabular data.
---

# Markdown Table Generator Skill

Markdownテーブルを生成・整形するスキルです。

## 概要

データから美しく整列されたMarkdownテーブルを生成します。

## 主な機能

- **自動整列**: 列幅を自動調整
- **データソース**: CSV、JSON、配列から変換
- **配置指定**: 左寄せ、中央、右寄せ
- **ソート**: 列でのソート
- **フィルタリング**: 条件に合う行のみ
- **スタイル**: GitHub、GitLab、標準Markdown

## 使用方法

```
以下のデータからMarkdownテーブルを生成：

名前: 田中, 年齢: 30, 職業: エンジニア
名前: 佐藤, 年齢: 25, 職業: デザイナー
名前: 鈴木, 年齢: 28, 職業: マネージャー
```

## 生成例

### 基本テーブル

**入力データ**:
```
Product, Price, Stock
iPhone 15, 128000, 50
MacBook Pro, 298000, 20
AirPods Pro, 39800, 100
```

**生成テーブル**:
```markdown
| Product      | Price  | Stock |
|--------------|--------|-------|
| iPhone 15    | 128000 | 50    |
| MacBook Pro  | 298000 | 20    |
| AirPods Pro  | 39800  | 100   |
```

### 配置指定

**左寄せ・中央・右寄せ**:
```markdown
| 商品         | カテゴリ | 価格   |
|:-------------|:--------:|-------:|
| iPhone 15    | スマホ   | 128000 |
| MacBook Pro  | PC       | 298000 |
| AirPods Pro  | オーディオ | 39800  |
```

- `:---` = 左寄せ
- `:---:` = 中央揃え
- `---:` = 右寄せ

### JSONからテーブル

**入力JSON**:
```json
[
  {"name": "John", "age": 30, "city": "Tokyo"},
  {"name": "Jane", "age": 25, "city": "Osaka"}
]
```

**生成テーブル**:
```markdown
| name | age | city  |
|------|-----|-------|
| John | 30  | Tokyo |
| Jane | 25  | Osaka |
```

### CSVからテーブル

**入力CSV**:
```
Name,Email,Role
Alice,alice@example.com,Admin
Bob,bob@example.com,User
Carol,carol@example.com,Editor
```

**生成テーブル**:
```markdown
| Name  | Email               | Role   |
|-------|---------------------|--------|
| Alice | alice@example.com   | Admin  |
| Bob   | bob@example.com     | User   |
| Carol | carol@example.com   | Editor |
```

### 複雑なテーブル

**統計データ**:
```markdown
| メトリクス          | 1月      | 2月      | 3月      | 平均     |
|:-------------------|--------:|--------:|--------:|---------:|
| ページビュー        | 125,430 | 138,920 | 152,100 | 138,817  |
| ユニークユーザー    | 45,230  | 52,100  | 58,920  | 52,083   |
| コンバージョン率    | 2.3%    | 2.8%    | 3.1%    | 2.7%     |
| 平均滞在時間（秒）  | 145     | 158     | 172     | 158      |
```

### チェックリストテーブル

```markdown
| タスク                   | 担当者 | ステータス | 期限       |
|-------------------------|--------|-----------|-----------|
| デザインレビュー         | 鈴木   | ✅ 完了    | 2024-06-15 |
| 実装                     | 田中   | 🔄 進行中  | 2024-06-20 |
| テスト                   | 山田   | ⏳ 待機中  | 2024-06-25 |
| リリース                 | 佐藤   | ⏳ 待機中  | 2024-06-30 |
```

### 比較表

```markdown
| 機能           | 無料プラン | プロ      | エンタープライズ |
|---------------|:---------:|:--------:|:---------------:|
| ユーザー数     | 5人まで   | 無制限    | 無制限           |
| ストレージ     | 5GB       | 100GB    | 無制限           |
| サポート       | コミュニティ | メール   | 24/7 電話       |
| 価格（月額）   | ¥0        | ¥1,200   | お問い合わせ     |
```

## 整形機能

### 未整列テーブルの整形

**入力（未整列）**:
```markdown
|Name|Age|City|
|-|-|-|
|John Doe|30|Tokyo|
|Jane|25|San Francisco|
```

**整形後**:
```markdown
| Name     | Age | City          |
|----------|-----|---------------|
| John Doe | 30  | Tokyo         |
| Jane     | 25  | San Francisco |
```

### ソート機能

```
以下のテーブルを価格の高い順にソート：
[テーブル]
```

### フィルタリング

```
以下のテーブルから在庫50以上の商品のみ抽出：
[テーブル]
```

## HTMLテーブルへの変換

**Markdown**:
```markdown
| Name | Age |
|------|-----|
| John | 30  |
```

**HTML**:
```html
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Age</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John</td>
      <td>30</td>
    </tr>
  </tbody>
</table>
```

## ベストプラクティス

1. **適切な列幅**: 内容に応じて調整
2. **配置**: 数値は右寄せ、テキストは左寄せ
3. **ヘッダー**: 明確で簡潔に
4. **改行**: 長いテキストは適度に分割
5. **記号**: 絵文字で視認性向上（✅ ❌ ⚠️）

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
以下のデータからMarkdownテーブルを生成：

製品名, 価格, 在庫
iPhone 15, 128000, 50
MacBook Pro, 298000, 20

要件:
- 価格は右寄せ
- 在庫は中央揃え
- 価格でソート（降順）
```

美しく整形されたテーブルが生成されます！
