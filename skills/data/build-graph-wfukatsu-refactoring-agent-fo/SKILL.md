---
name: build-graph
description: GraphDB構築エージェント - ユビキタス言語とコード解析結果からRyuGraphデータベースを構築。/build-graph [対象パス] で呼び出し。
user_invocable: true
---

# GraphDB構築エージェント

既存のシステム分析結果とソースコードを解析し、RyuGraph GraphDBにユビキタス言語ベースのナレッジグラフを構築するエージェントです。

## 目的

このエージェントは以下を実行します：

1. **分析結果の収集** - `/analyze-system` の出力（ユビキタス言語、ドメイン-コード対応表等）を収集
2. **コード解析** - Serenaツールでソースコードの構造を解析
3. **グラフ構築** - RyuGraphにノードとリレーションシップを登録
4. **メタデータ保存** - グラフのスキーマ情報と統計を保存

## 前提条件

- Python 3.9+
- ryugraph パッケージ (`pip install ryugraph`)
- `/analyze-system` が実行済み（推奨、なくてもコードから構築可能）

## グラフスキーマ

### ノードテーブル

| テーブル | 説明 | プロパティ |
|---------|------|-----------|
| `UbiquitousTerm` | ユビキタス言語の用語 | name (PK), name_ja, definition, domain |
| `Domain` | ビジネスドメイン | name (PK), type, description |
| `Entity` | クラス/インターフェース | name (PK), file_path, type, line_number |
| `Method` | メソッド/関数 | name (PK), signature, file_path, line_number |
| `File` | ソースファイル | path (PK), language, module |
| `Actor` | アクター（人/システム） | name (PK), type, description |
| `Role` | ロール/権限 | name (PK), permissions |

### リレーションテーブル

| テーブル | FROM → TO | 説明 |
|---------|-----------|------|
| `BELONGS_TO` | Entity → Domain | ドメインへの所属 |
| `DEFINED_IN` | Entity/Method → File | ファイルでの定義 |
| `REFERENCES` | Entity/Method → Entity | 参照関係 |
| `CALLS` | Method → Method | 呼び出し関係 |
| `IMPLEMENTS` | Entity → Entity | 実装/継承関係 |
| `HAS_TERM` | Entity/Method → UbiquitousTerm | 用語との関連 |
| `HAS_ROLE` | Actor → Role | ロールの保持 |

## 実行プロンプト

あなたはGraphDBを構築する専門家エージェントです。以下の手順でRyuGraphデータベースを構築してください。

### Step 1: 入力情報の確認

まず、対象ディレクトリと分析結果の有無を確認します。

```bash
# 引数から対象パスを取得
TARGET_PATH=$1  # 例: ./src

# 分析結果の存在確認
ls ${TARGET_PATH}/reports/01_analysis/
```

### Step 2: 分析結果の読み込み

分析結果が存在する場合、以下のファイルを読み込みます：

```
reports/01_analysis/
├── ubiquitous_language.md     # ユビキタス言語
├── domain_code_mapping.md     # ドメイン-コード対応
├── actors_roles_permissions.md # アクター・ロール
└── current_system_overview.md  # システム概要
```

**重要:** Markdownのテーブルをパースして構造化データに変換します。

### Step 3: コードベースの解析

Serenaツールを使用してコード構造を取得：

```
# シンボル概要を取得
mcp__serena__get_symbols_overview で主要ファイルを解析

# クラス/メソッドの詳細を取得
mcp__serena__find_symbol で重要なシンボルを検索

# 参照関係を取得
mcp__serena__find_referencing_symbols で依存関係を分析
```

### Step 4: グラフデータの生成

収集した情報からグラフデータを生成します。

**ノードデータ（CSVファイル）:**

```csv
# terms.csv
name,name_ja,definition,domain
Order,注文,顧客が商品を購入する単位,コアドメイン
Customer,顧客,システムの利用者,コアドメイン

# entities.csv
name,file_path,type,line_number
Order,src/domain/order.ts,class,10
Customer,src/domain/customer.ts,class,5

# methods.csv
name,signature,file_path,line_number
createOrder,createOrder(items: Item[]): Order,src/service/order.ts,25
```

**リレーションデータ（CSVファイル）:**

```csv
# belongs_to.csv
entity,domain
Order,OrderManagement
Customer,CustomerManagement

# has_term.csv
entity,term
Order,Order
CustomerService,Customer
```

### Step 5: RyuGraphデータベースの構築

Pythonスクリプトを実行してグラフを構築：

```bash
python scripts/build_graph.py \
  --data-dir ${TARGET_PATH}/reports/graph/data \
  --db-path ${TARGET_PATH}/knowledge.ryugraph
```

### Step 6: 検証クエリの実行

構築したグラフの整合性を確認：

```cypher
# ノード数の確認
MATCH (n) RETURN labels(n), count(*);

# リレーション数の確認
MATCH ()-[r]->() RETURN type(r), count(*);

# サンプルクエリ
MATCH (e:Entity)-[:HAS_TERM]->(t:UbiquitousTerm)
RETURN e.name, t.name_ja LIMIT 10;
```

## 出力

### ファイル構成

```
<対象プロジェクト>/
├── knowledge.ryugraph/          # RyuGraphデータベース
└── reports/
    └── graph/
        ├── data/                # 中間CSVファイル
        │   ├── terms.csv
        │   ├── domains.csv
        │   ├── entities.csv
        │   ├── methods.csv
        │   ├── files.csv
        │   ├── actors.csv
        │   ├── roles.csv
        │   ├── belongs_to.csv
        │   ├── defined_in.csv
        │   ├── references.csv
        │   ├── calls.csv
        │   ├── implements.csv
        │   ├── has_term.csv
        │   └── has_role.csv
        ├── schema.md            # グラフスキーマ説明
        └── statistics.md        # グラフ統計情報
```

### statistics.md の形式

```markdown
# GraphDB統計情報

## 生成日時
2024-XX-XX HH:MM:SS

## ノード統計

| ノードタイプ | 件数 |
|------------|------|
| UbiquitousTerm | 45 |
| Domain | 6 |
| Entity | 120 |
| Method | 350 |
| File | 80 |
| Actor | 5 |
| Role | 8 |

## リレーション統計

| リレーションタイプ | 件数 |
|------------------|------|
| BELONGS_TO | 120 |
| DEFINED_IN | 470 |
| REFERENCES | 890 |
| CALLS | 1200 |
| IMPLEMENTS | 45 |
| HAS_TERM | 280 |
| HAS_ROLE | 12 |

## データソース

- 分析結果: あり
- コード解析: あり
- 対象ファイル数: 80
```

## ツール使用ガイドライン

### 優先順位

1. **分析結果の読み込み** - Readツールでマークダウンを解析
2. **Serenaツール** - コードのシンボリック解析
3. **Bashツール** - Pythonスクリプトの実行

### 注意事項

- 大規模プロジェクトでは、主要なディレクトリのみを解析対象にする
- 外部ライブラリ（node_modules, vendor等）は除外する
- メソッド/関数の呼び出し関係は、静的解析の限界があることを警告する

## エラーハンドリング

- ryugraphがインストールされていない → `pip install ryugraph` を提案
- 分析結果がない → コードのみから構築（精度低下を警告）
- 対象言語非対応 → 手動でCSVを作成するよう案内
