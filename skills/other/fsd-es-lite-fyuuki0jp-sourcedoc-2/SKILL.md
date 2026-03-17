---
name: fsd-es-lite
description: FSD + ES-lite アーキテクチャに基づく機能開発スキル。新しいfeature/entity/widgetを追加する時、CQRS + Event Sourcingパターンで実装する時、scaffoldスクリプトを使う時に使用。AI-nativeアプリケーション開発向け。
---

# FSD + ES-lite 開発スキル

Feature-Sliced Design (FSD) と Event Sourcing Lite (ES-lite) を組み合わせた開発プロセス。
PoC・小規模開発向けに最適化された軽量アーキテクチャ。

## 設計原則

### 1. 関数ベース実装（クラス禁止）

クラスを使わず、関数とvelonaのDIで実装する。

**理由**:
- クラスはインスタンス内での状態管理が複雑になりがち
- 関数は純粋で、テストしやすく、合成しやすい
- velonaで依存注入すれば、テスト時のモック差し替えも容易

```typescript
// ✅ 関数ベース + velona DI
import { depend } from "velona";

export const executeCommand = depend(
  { eventStore, projector, clock: () => new Date().toISOString(), idGen: () => crypto.randomUUID() },
  async (deps, command: Command, correlationId: string) => {
    // 実装
  }
);

// テスト時
executeCommand.inject({ eventStore: mockStore })(command, correlationId);

// ❌ クラスベース（使わない）
class CommandHandler {
  constructor(private eventStore: IEventStore) {}
  async execute(command: Command) { /* ... */ }
}
```

### 2. ES-lite統一

全featureでEvent Sourcing Lite（軽量版ES）に統一。

**特徴**:
- 全状態変更をイベントとして記録
- イベントリプレイで状態再構築
- AIエージェント + ユーザー操作を同じイベント系列で追跡
- CRUDとの混在を避け、学習コストを削減

### 3. 厳格なFSD構造

```
src/
  shared/          # 共有インフラ・ユーティリティ
  entities/        # ドメインモデル・スキーマ・表示UI（オプション）
  features/        # ユースケース・API・状態管理
  widgets/         # 複合UIブロック
  pages/           # ルートコンポーネント
  app/             # アプリ初期化
```

### 4. decide/apply パターン（純粋関数）

```typescript
// decide: 状態 + コマンド → イベント（純粋関数）
function decide(
  state: Aggregate | null,
  command: Command,
  meta: EventMeta
): Result<Event[], DecisionError>

// apply: 状態 + イベント → 新状態（純粋関数）
function apply(
  state: Aggregate | null,
  event: Event
): Aggregate
```

## Scaffoldスクリプト

新しい機能を追加する際は、scaffoldスクリプトを使用して最小限のボイラープレートを生成する。
生成後、ドメインに合わせてカスタマイズする。

### Feature全体を生成

```bash
npx tsx .claude/skills/fsd-es-lite/scripts/scaffold-feature.ts <feature-name>
```

生成されるファイル（最小構成）:
- `entities/<name>/model/schema.ts` - Zodドメインスキーマ
- `entities/<name>/model/events.ts` - イベント型定義
- `features/<name>/model/decide.ts` - 決定ロジック
- `features/<name>/model/apply.ts` - 適用ロジック
- `features/<name>/model/commands.ts` - コマンド実行
- `features/<name>/model/queries.ts` - クエリ
- `features/<name>/model/projector.ts` - Projection更新
- `features/<name>/api/routes.ts` - Hono APIルート
- `features/<name>/api/contracts.ts` - RPC型定義
- `features/<name>/api/schemas.ts` - バリデーションスキーマ

**UIやhooksは必要に応じて追加する**（scaffoldでは生成しない）

### Entityのみを生成

```bash
npx tsx .claude/skills/fsd-es-lite/scripts/scaffold-entity.ts <entity-name>
```

生成されるファイル:
- `entities/<name>/model/schema.ts` - Zodドメインスキーマ
- `entities/<name>/model/events.ts` - イベント型定義
- `entities/<name>/model/index.ts` - エクスポート
- `entities/<name>/ui/<Name>.tsx` - UIコンポーネント（実装必須）
- `entities/<name>/ui/index.ts` - UIエクスポート

**生成後、TODOコメントを参照してドメインに合わせて実装する**

### Widgetを生成

```bash
npx tsx .claude/skills/fsd-es-lite/scripts/scaffold-widget.ts <widget-name>
```

生成されるファイル:
- `widgets/<name>/ui/<Name>.tsx` - メインコンポーネント（実装必須）
- `widgets/<name>/ui/index.ts` - UIエクスポート
- `widgets/<name>/model/index.ts` - モデルエクスポート
- `widgets/<name>/index.ts` - パブリックAPI

**生成後、TODOコメントを参照してentities/featuresを組み合わせて実装する**

## 開発フロー

### 新機能追加時

1. **scaffoldで雛形生成**
   ```bash
   npx tsx .claude/skills/fsd-es-lite/scripts/scaffold-feature.ts order
   ```

2. **ドメインスキーマ定義** (`entities/order/model/schema.ts`)
   - Zodでドメイン型を定義
   - ステータス enum、集約、投影を定義
   - ドメインに必要なフィールドを追加

3. **イベント定義** (`entities/order/model/events.ts`)
   - ドメインイベントを定義（Created, Updated, etc.）
   - イベントファクトリ関数を追加

4. **decide/apply実装** (`features/order/model/`)
   - `decide.ts`: ビジネスルールを純粋関数で実装
   - `apply.ts`: イベント適用を純粋関数で実装
   - in-source testingでテスト追加

5. **commands.ts実装**
   - velonaでDI
   - EventStore.load → decide → EventStore.append → Projector.save

6. **APIルート定義** (`features/order/api/routes.ts`)
   - Honoでエンドポイント定義
   - zValidatorでバリデーション

7. **必要に応じてUI/hooksを追加**
   - `features/order/hooks/` - TanStack Query hooks
   - `features/order/ui/` - UIコンポーネント
   - `entities/order/ui/` - 表示専用コンポーネント

## 参照ドキュメント

詳細な実装パターンは以下を参照:

- [ARCHITECTURE.md](ARCHITECTURE.md) - アーキテクチャ詳細
- [PATTERNS.md](PATTERNS.md) - コードパターン集

## 重要な設計判断

### Result型と例外の使い分け

| 種類 | エラー例 | 対応 |
|------|----------|------|
| Result型 | バリデーションエラー、バージョン競合 | 復帰可能 |
| 例外 | DBアクセスエラー | 復帰不能 |

### 楽観的ロック

```typescript
// コマンドにexpectedVersionを含める
type UpdateCommand = {
  type: "Update";
  aggregateId: string;
  expectedVersion: number;
  // ...
};

// appendでバージョンチェック
await eventStore.append(aggregateId, events, expectedVersion);
// → ConflictErrorならリトライを促す
```

### 日時型の統一

全ての日時はISO 8601文字列（`string`）で統一。

```typescript
// ✅ ISO 8601文字列
createdAt: z.string().datetime()

// ❌ Dateオブジェクト（使わない）
createdAt: z.date()
```

### Projector失敗時の方針

イベントは保存済みなので、投影失敗はログのみ。後からリプレイで再構築可能。

```typescript
try {
  await deps.projector.save(next);
} catch (error) {
  console.warn("Projection save failed:", error);
}
```

## AI操作追跡

CommandLogでAI操作を追跡:

```typescript
interface CommandLog {
  actor: { type: 'user' | 'ai' | 'system'; id?: string };
  aiInfo?: {
    modelId: string;
    runId: string;
    promptHash?: string;
  };
  // ...
}
```
