---
name: documenting-domains
description: コードベース分析からドメインドキュメントを生成
allowed-tools: Read, Write, Grep, Glob, Task
context: fork
user-invocable: false
---

# ドメインドキュメント生成

## アプローチ: スキーマファースト

エンティティ/モデルファイルを信頼の源として Read する。

| 優先度 | ソース                | 方法                                |
| ------ | --------------------- | ----------------------------------- |
| 1      | ORMスキーマファイル   | ファイル全文 Read、エンティティ解析 |
| 2      | 型/クラスファイル     | ファイル全文 Read、フィールド抽出   |
| 3      | Grep（フォールバック）| 発見のみ、フィールド値の取得は不可  |

## 検出

| カテゴリ           | 対象                                             |
| ------------------ | ------------------------------------------------ |
| エンティティ       | class, interface, dataclass, Prisma, ORM         |
| Value Objects      | 内部構造を持つ埋め込み型、独立ライフサイクルなし |
| ポリモーフィック型 | 判別共用体、サブタイプ階層、バリアント           |
| 不変条件           | バリデーションロジック、制約、必須フィールド     |
| ドメイン用語       | クラス/関数名、コメント、JSDoc                   |
| 関連               | エンティティ参照、継承、import（直接 + 間接）    |
| ビジネスルール     | バリデータ、ポリシー、ドメインサービス           |
| ドメインイベント   | イベントクラス、EventEmitter、pub/subパターン    |
| コード問題         | typo、命名不整合、null処理のギャップ             |

## 発見ルール

読み取り前にモデルルート配下の全ディレクトリを列挙する。全ディレクトリ = エンティティまたはVOの候補。未調査のディレクトリを残さない。

## ORM抽出ルール

| ORM/フレームワーク | エンティティ検出             | フィールド抽出               | 不変条件検出                          |
| ------------------ | ---------------------------- | ---------------------------- | ------------------------------------- |
| Prisma             | `model EntityName {`         | `fieldName Type @annotation` | `@unique`, `@default`, `@@index`      |
| TypeORM            | `@Entity()` class            | `@Column()` property         | `@Check()`, クラスバリデータ          |
| Sequelize          | `Model.init({...})`          | init config 内のプロパティ   | `validate:` オプション                |
| Drizzle            | `pgTable()`, `sqliteTable()` | カラム定義                   | `.notNull()`, `.unique()`             |
| Django             | `class X(models.Model)`      | `models.CharField(...)` 等   | `validators=`, `unique=True`          |
| SQLAlchemy         | `class X(Base)`              | `Column(Type, ...)` 宣言     | `CheckConstraint`, `UniqueConstraint` |
| 汎用               | `class X` / `interface X`    | プロパティ宣言 + 型          | メソッド内の throw/assert/validate    |

## スキーマ読み取り

| ルール           | 詳細                                                                   |
| ---------------- | ---------------------------------------------------------------------- |
| ファイル全文読み | フィールド値の grep 取得は不可                                         |
| 全フィールド取得 | 「重要な」ものだけでなく全フィールド                                   |
| 正確な型名保持   | 定義通りの型名を使用、`\| null` を含む場合はそのまま記録               |
| nullable 検出    | `?? null` → nullable; `?? null` なし → non-nullable; `?: T` → optional |
| enum 実装形式    | 形式を記録: named_enum, object_literal, class_wrapped                  |
| enum 値          | 宣言順で全値; コード上の実際のキーのみ使用                             |
| 制約の保持       | NOT NULL, required, @IsNotEmpty, バリデータ                            |
| ソース位置       | プロジェクト相対パス + 行番号を一貫して使用                            |
| 命名の不一致     | ディレクトリ名 ≠ 型名を記録                                            |
| コード問題       | 読み取り中に発見したtypo、不整合パターンを記録                         |

反ハルシネーション: 出力の全フィールドは Read 呼び出しに基づく `source_file` が必須。Read 証拠なし = 出力禁止。

### Prisma スキーマ

`model X { ... }` ブロックをエンティティの信頼源としてパース。`Type?` = nullable、`@relation` = リレーション、`enum X { ... }` = enum 値。

## 信頼度

| 証拠                   | レベル   |
| ---------------------- | -------- |
| スキーマ + バリデータ  | verified |
| スキーマファイルのみ   | verified |
| 型/クラス定義          | inferred |
| Grepマッチのみ         | unknown  |

## 検証ゲート

出力前に検証:

| チェック項目     | ルール                                                |
| ---------------- | ----------------------------------------------------- |
| 幻フィールド禁止 | 全出力フィールドは Read の file:line に紐づく必要あり |
| ディレクトリ網羅 | 全モデルディレクトリ → 出力にエンティティまたはVO     |
| nullable 正確性  | 全フィールドの nullable 状態がコードパターンと一致    |
| enum 正確性      | enumキー/値がコードと完全一致、実装形式を記録         |
| パス一貫性       | 全ソースパスが同一のプロジェクト相対形式              |
| 関連の深さ       | 間接関連（A → B → C）もERに含める                     |
| 命名の整合       | ディレクトリ ≠ 型名の不一致を記録                     |
