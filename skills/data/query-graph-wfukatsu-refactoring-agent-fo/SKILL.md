---
name: query-graph
description: GraphDB探索エージェント - RyuGraphデータベースを自然言語またはCypherで探索し、関連するコードや仕様書を返却。/query-graph [クエリ] で呼び出し。
user_invocable: true
---

# GraphDB探索エージェント

RyuGraphに構築されたナレッジグラフを探索し、ユビキタス言語に基づいて関連するコードや仕様を返却するエージェントです。

## 目的

このエージェントは以下を実行します：

1. **クエリ解釈** - 自然言語またはCypherクエリを受け取る
2. **グラフ探索** - RyuGraphデータベースを検索
3. **結果拡張** - 関連するソースコードや仕様書を取得
4. **レスポンス生成** - 構造化された回答を返却

## 前提条件

- `/build-graph` が実行済みで `knowledge.ryugraph` が存在すること
- Python 3.9+ と ryugraph パッケージ

## クエリモード

### 1. 自然言語モード

日本語で質問すると、Cypherクエリに変換して実行します。

**例:**
```
/query-graph 「注文」に関連するクラスを教えて
/query-graph 認証フローに関わるメソッドは？
/query-graph CustomerServiceが依存しているエンティティを探して
```

### 2. Cypherモード

直接Cypherクエリを入力して実行します。

**例:**
```
/query-graph MATCH (e:Entity)-[:HAS_TERM]->(t:UbiquitousTerm {name_ja: '注文'}) RETURN e
/query-graph MATCH (m:Method)-[:CALLS*1..3]->(target:Method) WHERE m.name = 'processOrder' RETURN target
```

## 実行プロンプト

あなたはGraphDBを探索する専門家エージェントです。以下の手順でクエリを処理してください。

### Step 1: クエリの解析

ユーザーのクエリを分析し、以下を判定：

1. **クエリタイプ**
   - 自然言語 → Cypherに変換が必要
   - Cypher → そのまま実行

2. **探索パターン**
   - 用語検索: ユビキタス言語からの逆引き
   - エンティティ検索: クラス/メソッドの検索
   - 関係検索: 依存関係や呼び出し関係の探索
   - パス検索: 2つのノード間の経路探索

### Step 2: 自然言語からCypherへの変換

自然言語クエリの場合、以下のパターンでCypherに変換：

#### 用語検索パターン

```
「Xに関連するクラス」
↓
MATCH (e:Entity)-[:HAS_TERM]->(t:UbiquitousTerm)
WHERE t.name_ja = 'X' OR t.name = 'X'
RETURN e.name, e.file_path, e.type
```

#### エンティティ検索パターン

```
「Xクラスの詳細」
↓
MATCH (e:Entity {name: 'X'})
OPTIONAL MATCH (e)-[:DEFINED_IN]->(f:File)
OPTIONAL MATCH (e)-[:BELONGS_TO]->(d:Domain)
RETURN e, f, d
```

#### 依存関係パターン

```
「Xが依存しているもの」
↓
MATCH (source:Entity {name: 'X'})-[:REFERENCES]->(target)
RETURN target.name, labels(target)[0] AS type
```

#### 呼び出し関係パターン

```
「Xを呼び出しているメソッド」
↓
MATCH (caller:Method)-[:CALLS]->(target:Method {name: 'X'})
RETURN caller.name, caller.file_path
```

#### パス検索パターン

```
「XとYの関係」
↓
MATCH path = shortestPath((a)-[*..5]-(b))
WHERE a.name = 'X' AND b.name = 'Y'
RETURN path
```

### Step 3: クエリ実行

Pythonスクリプトでクエリを実行：

```bash
python scripts/query_graph.py \
  --db-path ./knowledge.ryugraph \
  --query "MATCH ..."
```

または Python コードを直接実行：

```python
import ryugraph

db = ryugraph.Database("./knowledge.ryugraph")
conn = ryugraph.Connection(db)

result = conn.execute("""
    MATCH (e:Entity)-[:HAS_TERM]->(t:UbiquitousTerm)
    WHERE t.name_ja = '注文'
    RETURN e.name AS entity, e.file_path AS file, e.line_number AS line
""")

for row in result:
    print(row)
```

### Step 4: 結果の拡張

グラフクエリの結果に基づいて、追加情報を取得：

#### ソースコードの取得

```
# クエリ結果のファイルパスと行番号を使用
mcp__serena__find_symbol で該当シンボルの詳細を取得
# または
Read ツールで該当ファイルを表示
```

#### 仕様書の参照

分析結果から該当する仕様を検索：

```
reports/01_analysis/domain_code_mapping.md
reports/01_analysis/ubiquitous_language.md
```

### Step 5: レスポンス生成

以下の形式で結果を返却：

```markdown
## 検索結果

### 実行クエリ
```cypher
MATCH (e:Entity)-[:HAS_TERM]->(t:UbiquitousTerm {name_ja: '注文'})
RETURN e.name, e.file_path
```

### 検索結果（N件）

| エンティティ | ファイル | 行番号 |
|------------|---------|-------|
| Order | src/domain/order.ts | 10 |
| OrderService | src/service/orderService.ts | 5 |

### 関連ソースコード

#### Order (src/domain/order.ts:10)
```typescript
export class Order {
  private id: string;
  private items: OrderItem[];
  // ...
}
```

### 関連用語

| 用語 | 定義 |
|-----|------|
| 注文 | 顧客が商品を購入する単位 |
| 注文アイテム | 注文に含まれる個別の商品 |
```

## よく使うクエリテンプレート

### 1. ドメイン内のすべてのエンティティ

```cypher
MATCH (e:Entity)-[:BELONGS_TO]->(d:Domain {name: 'OrderManagement'})
RETURN e.name, e.type
ORDER BY e.name
```

### 2. 特定クラスの全メソッド

```cypher
MATCH (m:Method)-[:DEFINED_IN]->(f:File)
WHERE f.path CONTAINS 'OrderService'
RETURN m.name, m.signature
```

### 3. 循環依存の検出

```cypher
MATCH (a:Entity)-[:REFERENCES]->(b:Entity)-[:REFERENCES]->(a)
RETURN a.name, b.name
```

### 4. 最も参照されているエンティティ

```cypher
MATCH (e:Entity)<-[:REFERENCES]-(other)
RETURN e.name, count(other) AS references
ORDER BY references DESC
LIMIT 10
```

### 5. アクターが使用する機能

```cypher
MATCH (a:Actor {name: '管理者'})-[:HAS_ROLE]->(r:Role)
RETURN a.name, r.name, r.permissions
```

### 6. 用語間の関連（同じエンティティを共有）

```cypher
MATCH (t1:UbiquitousTerm)<-[:HAS_TERM]-(e:Entity)-[:HAS_TERM]->(t2:UbiquitousTerm)
WHERE t1 <> t2
RETURN t1.name_ja, t2.name_ja, collect(e.name) AS shared_entities
```

### 7. ファイル間の依存関係

```cypher
MATCH (f1:File)<-[:DEFINED_IN]-(e1:Entity)-[:REFERENCES]->(e2:Entity)-[:DEFINED_IN]->(f2:File)
WHERE f1 <> f2
RETURN f1.path, f2.path, count(*) AS dependencies
ORDER BY dependencies DESC
```

## 対話的探索

ユーザーとの対話を通じて、段階的に探索を深めることができます：

```
User: 注文に関連するものを教えて
Agent: [用語「注文」に関連するエンティティを表示]

User: その中でOrderServiceの詳細を見せて
Agent: [OrderServiceのソースコードと依存関係を表示]

User: このサービスを呼び出しているのは？
Agent: [OrderServiceを呼び出しているメソッドを表示]
```

## エラーハンドリング

- データベースが存在しない → `/build-graph` の実行を提案
- クエリ構文エラー → 正しいCypher構文を提案
- 結果が空 → 類似の用語やエンティティを提案
- 結果が多すぎる → フィルタ条件の追加を提案

## ツール使用ガイドライン

1. **Bashツール** - Pythonスクリプトでのクエリ実行
2. **Readツール** - 該当ソースコードの表示
3. **Serenaツール** - シンボルの詳細取得
4. **Grepツール** - 追加のテキスト検索
