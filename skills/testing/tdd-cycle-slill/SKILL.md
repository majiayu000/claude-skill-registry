---
name: tdd-cycle-skill
description: 明示的に呼び出されたときにのみ読み込みます。エージェントが自律的に呼び出す必要はありません。
---

1. Red - Green - Refactor のサイクルで実装します。ただし、「TDD が適さないタスクである」と判断した場合は、DIRECT に実装して OK です。
  - Red: 仕様に則り、落ちるテストを書いてください。
  - Green: テストを通すことだけを考えた最小限の実装をおこなってください。
  - Refactor: テストを通すことだけではなく、コード品質向上をおこなってください。
    - 将来の変更や機能変更が容易にするための保守性の確保
    - コードの重複を排除したり、複雑さを取り除いてシンプルさの確保

2. 実装を終えたら、test と lint, 型チェック, semgrep を実施します。問題があれば修正します。
  - `docker compose exec {コンテナサービス名} bunx tsc --noEmit`
  - `docker compose exec {コンテナサービス名} bun run fix`
  - `docker compose exec {コンテナサービス名} test`
  - `docker compose run --rm semgrep semgrep <args...>`

## 参考情報
必要な内容を取捨選択し Read して参考にしてください。

- [バックエンド開発ガイドライン](../common/references/backend.md)
- [フロントエンド開発ガイドライン](../common/references/frontend.md)
- [スキーマ駆動開発ガイドライン](../common/references/schema-db.md)
- [E2Eテストガイドライン](../common/references/e2e.md)
