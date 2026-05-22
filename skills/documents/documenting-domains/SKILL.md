---
name: documenting-domains
description: >
  Generate domain documentation from codebase analysis - entities, glossary, relationships.
  Triggers: domain model, entity diagram, ドメインモデル, 用語集, glossary, ubiquitous language.
allowed-tools: [Read, Write, Grep, Glob, Bash, Task]
context: fork
user-invocable: false
---

# ドメイン理解生成

## 検出

| カテゴリ         | 対象                                          |
| ---------------- | --------------------------------------------- |
| エンティティ     | class, interface, dataclass, Prisma, ORM      |
| 不変条件         | バリデーションロジック、制約、必須フィールド  |
| ドメイン用語     | クラス/関数名、コメント、JSDoc                |
| 関係             | エンティティ参照、継承、インポート            |
| ビジネスルール   | バリデータ、ポリシー、ドメインサービス        |
| ドメインイベント | イベントクラス、EventEmitter、pub/subパターン |

## ORMパターン

| ORM/フレームワーク | パターン                   |
| ------------------ | -------------------------- |
| Prisma             | `model User {}`            |
| TypeORM            | `@Entity()`, `@Column()`   |
| Sequelize          | `Model.init()`             |
| Django             | `class User(models.Model)` |
| SQLAlchemy         | `class User(Base)`         |
