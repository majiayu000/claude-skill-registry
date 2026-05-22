---
name: typescript-rules
description: 型安全性とエラーハンドリングルールを適用。any禁止、型ガード必須。TypeScript実装、型定義レビュー時に使用。
---

# TypeScript 開発ルール

## Backend実装における型安全性

**データフローでの型安全性**
入力層（`unknown`） → 型ガード → ビジネス層（型保証） → 出力層（シリアライズ）

**Backend固有の型シナリオ**:
- **API通信**: レスポンスは必ず`unknown`で受け、型ガードで検証
- **フォーム入力**: 外部入力は`unknown`、バリデーション後に型確定
- **レガシー統合**: `window as unknown as LegacyWindow`のように段階的アサーション
- **テストコード**: モックも必ず型定義、`Partial<T>`や`vi.fn<[Args], Return>()`活用

## コーディング規約

**クラス使用の判断基準**
- **推奨：関数とinterfaceでの実装**
  - 背景: テスタビリティと関数合成の柔軟性が向上
- **クラス使用を許可**:
  - フレームワーク要求時（NestJSのController/Service、TypeORMのEntity等）
  - カスタムエラークラス定義時
  - 状態とビジネスロジックが密結合している場合（例: ShoppingCart、Session、StateMachine）
- **判断基準**: 「このデータは振る舞いを持つか？」がYesならクラス検討
  ```typescript
  // 関数とinterface
  interface UserService { create(data: UserData): User }
  const userService: UserService = { create: (data) => {...} }
  ```

**関数設計**
- **引数は0-2個まで**: 3個以上はオブジェクト化
  ```typescript
  // オブジェクト引数
  function createUser({ name, email, role }: CreateUserParams) {}
  ```

**依存性注入**
- **外部依存は引数で注入**: テスト可能性とモジュール性確保
  ```typescript
  // 依存性を引数で受け取る
  function createService(repository: Repository) { return {...} }
  ```

**非同期処理**
- Promise処理: 必ず`async/await`を使用
- エラーハンドリング: 必ず`try-catch`でハンドリング
- 型定義: 戻り値の型は明示的に定義（例: `Promise<Result>`）

**フォーマット規則**
- セミコロン省略（Biomeの設定に従う）
- 型は`PascalCase`、変数・関数は`camelCase`
- インポートは絶対パス（`src/`）

**クリーンコード原則**
- 使用されていないコードは即座に削除
- デバッグ用`console.log()`は削除
- コメントアウトされたコード禁止（バージョン管理で履歴管理）
- コメントは「なぜ」を説明（「何」ではなく）

## エラーハンドリング

**絶対ルール**: エラーの握りつぶし禁止。すべてのエラーは必ずログ出力と適切な処理を行う。

**Fail-Fast原則**: エラー時は速やかに失敗させ、不正な状態での処理継続を防ぐ
```typescript
// 禁止: 無条件フォールバック
catch (error) {
  return defaultValue // エラーを隠蔽
}

// 必須: 明示的な失敗
catch (error) {
  logger.error('処理失敗', error)
  throw error // 上位層で適切に処理
}
```

**Result型パターン**: エラーを型で表現し、明示的に処理
```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }

// 使用例：エラーの可能性を型で表現
function parseUser(data: unknown): Result<User, ValidationError> {
  if (!isValid(data)) return { ok: false, error: new ValidationError() }
  return { ok: true, value: data as User }
}
```

**カスタムエラークラス**
```typescript
export class AppError extends Error {
  constructor(message: string, public readonly code: string, public readonly statusCode = 500) {
    super(message)
    this.name = this.constructor.name
  }
}
// 用途別: ValidationError(400), BusinessRuleError(400), DatabaseError(500), ExternalServiceError(502)
```

**層別エラー処理**
- API層: HTTPレスポンスに変換、機密情報を除外してログ出力
- サービス層: ビジネスルール違反を検出、AppErrorはそのまま伝播
- リポジトリ層: 技術的エラーをドメインエラーに変換

**構造化ログと機密情報保護**
機密情報（password, token, apiKey, secret, creditCard）は絶対にログに含めない

**非同期エラーハンドリング**
- グローバルハンドラー設定必須: `unhandledRejection`, `uncaughtException`
- すべてのasync/awaitでtry-catch使用
- エラーは必ずログと再スロー

## パフォーマンス最適化

- ストリーミング処理: 大きなデータセットはストリームで処理
- メモリリーク防止: 不要なオブジェクトは明示的に解放
