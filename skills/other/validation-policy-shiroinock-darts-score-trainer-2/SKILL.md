---
name: validation-policy
description: 数値の入出力バリデーション方針。関数の引数・戻り値の妥当性チェック規約を定義。test-writer, implement, reviewerの各観点で参照。
allowed-tools: Read
---

# 数値バリデーション方針

このプロジェクトにおける数値の入出力バリデーションの統一方針を定義します。

## 基本原則

### 1. すべての公開関数は入力を検証する

- **外部からの入力は信頼しない**
- 関数の最初で引数の妥当性をチェック
- 不正な入力には早期にエラーをスロー

### 2. 一貫したエラーハンドリング

- 同じ種類の不正入力には同じエラーメッセージを使用
- エラーメッセージは日本語で明確に
- `throw new Error()`を使用（カスタムエラーは現時点では不要）

### 3. 型だけでは不十分

- TypeScriptの型チェックは実行時には働かない
- 数値の範囲、整数性、有限性を実行時に検証

## バリデーションチェック項目

### 必須チェック（すべての数値引数）

#### 1. 有限値チェック
```typescript
if (!Number.isFinite(value)) {
  throw new Error('適切なエラーメッセージ');
}
```

**検出する値**: `Infinity`, `-Infinity`, `NaN`

**理由**:
- `NaN`は比較演算が予期しない結果になる（`NaN === NaN`は`false`）
- `Infinity`は算術演算で予期しない振る舞いをする

#### 2. 整数チェック（整数値を期待する引数）
```typescript
if (!Number.isInteger(value)) {
  throw new Error('適切なエラーメッセージ');
}
```

**検出する値**: `1.5`, `3.14`, `0.1`など

**理由**: ダーツの点数は整数のみ有効

### 条件付きチェック（要件に応じて）

#### 3. 範囲チェック
```typescript
if (value < min || value > max) {
  throw new Error('適切なエラーメッセージ');
}
```

**例**:
- 残り点数: `> 0`（正の整数）
- 投擲点数: `0 <= value <= 60`
- 座標値: プロジェクト固有の範囲

#### 4. ドメイン固有のチェック
```typescript
if (!VALID_SCORES.has(value)) {
  throw new Error('適切なエラーメッセージ');
}
```

**例**: 有効なダーツスコア（23, 29などは無効）

## チェック順序の原則

**必ず以下の順序で実行**:

1. **有限値チェック** (`Number.isFinite()`)
2. **整数チェック** (`Number.isInteger()`)
3. **範囲チェック** (最小値・最大値)
4. **ドメイン固有チェック** (業務ルール)

**理由**: 早い段階で基本的な不正入力を排除し、より複雑なチェックに進む

## 実装パターン

### パターン1: 整数 + 正の値

```typescript
export function exampleFunction(score: number): void {
  // 入力値の妥当性チェック
  if (!Number.isFinite(score) || !Number.isInteger(score)) {
    throw new Error('点数は整数である必要があります');
  }

  if (score <= 0) {
    throw new Error('点数は正の整数である必要があります');
  }

  // ビジネスロジック...
}
```

### パターン2: 整数 + 範囲指定

```typescript
export function exampleFunction(throwScore: number): void {
  // 入力値の妥当性チェック
  if (!Number.isFinite(throwScore) || !Number.isInteger(throwScore)) {
    throw new Error('投擲点数は整数である必要があります');
  }

  if (throwScore < 0 || throwScore > 60) {
    throw new Error('投擲点数は0以上60以下である必要があります');
  }

  // ビジネスロジック...
}
```

### パターン3: 有限値のみ（整数制約なし）

```typescript
export function exampleFunction(coordinate: number): void {
  // 入力値の妥当性チェック
  if (!Number.isFinite(coordinate)) {
    throw new Error('座標は有限の数値である必要があります');
  }

  // ビジネスロジック...
}
```

## エラーメッセージの統一

### 標準メッセージテンプレート

| チェック内容 | メッセージ例 |
|------------|-------------|
| 有限値チェック（整数期待） | `{パラメータ名}は整数である必要があります` |
| 有限値チェック（実数可） | `{パラメータ名}は有限の数値である必要があります` |
| 正の整数 | `{パラメータ名}は正の整数である必要があります` |
| 範囲指定 | `{パラメータ名}は{最小値}以上{最大値}以下である必要があります` |

**注意**: 有限値と整数を同時にチェックする場合、エラーメッセージは「整数である必要があります」とする（`NaN`や`Infinity`も整数ではないため）

## test-writerの観点

### テストケース作成時の必須項目

#### 1. 異常系テスト - 入力検証

各関数に対して以下のテストケースを作成：

```typescript
describe('入力検証', () => {
  test('NaNはエラーをスローする', () => {
    expect(() => targetFunction(NaN)).toThrow('適切なエラーメッセージ');
  });

  test('Infinityはエラーをスローする', () => {
    expect(() => targetFunction(Infinity)).toThrow('適切なエラーメッセージ');
  });

  test('-Infinityはエラーをスローする', () => {
    expect(() => targetFunction(-Infinity)).toThrow('適切なエラーメッセージ');
  });

  test('小数値（整数期待の場合）はエラーをスローする', () => {
    expect(() => targetFunction(2.5)).toThrow('適切なエラーメッセージ');
  });

  test('範囲外の値はエラーをスローする', () => {
    expect(() => targetFunction(-1)).toThrow('適切なエラーメッセージ');
    expect(() => targetFunction(999)).toThrow('適切なエラーメッセージ');
  });
});
```

#### 2. テストの優先順位

1. **正常系**: 期待される入力での動作
2. **境界値**: 有効範囲の境界（最小値、最大値）
3. **異常系 - 型レベル**: `NaN`, `Infinity`, 非整数
4. **異常系 - 範囲**: 負の値、範囲外
5. **異常系 - ドメイン**: ドメイン固有の不正値

## implementの観点

### 実装時のチェックリスト

- [ ] すべての数値引数に対してバリデーションを実装
- [ ] バリデーションは関数の最初に配置
- [ ] チェック順序は「有限値 → 整数 → 範囲 → ドメイン」
- [ ] エラーメッセージは統一テンプレートに従う
- [ ] JSDocに`@throws`タグを追加
- [ ] JSDocの`@param`に「正の整数のみ」などの制約を明記

### JSDocの記載例

```typescript
/**
 * 残り点数がダブルでフィニッシュ可能かを判定する
 *
 * @param remainingScore 残り点数（正の整数のみ）
 * @returns ダブルでフィニッシュ可能ならtrue、不可能ならfalse
 * @throws {Error} 入力値が不正な場合
 */
export function canFinishWithDouble(remainingScore: number): boolean {
  // 入力値の妥当性チェック
  if (!Number.isFinite(remainingScore) || !Number.isInteger(remainingScore)) {
    throw new Error('残り点数は整数である必要があります');
  }

  // ...
}
```

## reviewerの観点

### レビュー時のチェックポイント

#### 1. 入力検証の完全性

- [ ] すべての数値引数にバリデーションがあるか
- [ ] `Number.isFinite()`チェックがあるか
- [ ] 整数が期待される場合、`Number.isInteger()`チェックがあるか
- [ ] 範囲チェックが適切か

#### 2. 一貫性

- [ ] 同じ種類のパラメータ（例: 残り点数）は同じバリデーションか
- [ ] エラーメッセージは統一テンプレートに従っているか
- [ ] チェック順序は「有限値 → 整数 → 範囲 → ドメイン」か

#### 3. テストカバレッジ

- [ ] `NaN`, `Infinity`, `-Infinity`のテストがあるか
- [ ] 小数値のテストがあるか（整数期待の場合）
- [ ] 範囲外のテストがあるか

#### 4. ドキュメント

- [ ] JSDocに`@throws`タグがあるか
- [ ] JSDocの`@param`に制約が明記されているか

### レビュー時の指摘例

**不十分な例**:
```typescript
export function example(score: number): void {
  if (score <= 0) {
    return false;
  }
  // ...
}
```

**指摘内容**:
- `NaN`, `Infinity`のチェックがない
- 整数チェックがない
- エラーをスローせずに`false`を返している（一貫性がない）

**改善例**:
```typescript
export function example(score: number): void {
  if (!Number.isFinite(score) || !Number.isInteger(score)) {
    throw new Error('点数は整数である必要があります');
  }

  if (score <= 0) {
    throw new Error('点数は正の整数である必要があります');
  }
  // ...
}
```

## よくある間違い

### ❌ 間違い1: `typeof`による型チェック

```typescript
if (typeof value !== 'number') {
  throw new Error('数値である必要があります');
}
```

**問題**: `NaN`や`Infinity`も`typeof`では`'number'`になる

**正しい方法**: `Number.isFinite()`を使用

### ❌ 間違い2: `value % 1 === 0`での整数チェック

```typescript
if (value % 1 !== 0) {
  throw new Error('整数である必要があります');
}
```

**問題**: `Infinity % 1`は`NaN`になり、`NaN !== 0`で一見動作するが意図が不明確

**正しい方法**: `Number.isInteger()`を使用

### ❌ 間違い3: エラーをスローせずに`false`を返す

```typescript
export function validate(value: number): boolean {
  if (value < 0) {
    return false; // ❌
  }
  return true;
}
```

**問題**:
- 不正な入力と正常な処理結果の区別がつかない
- 関数の使用者がエラーハンドリングを忘れる可能性

**正しい方法**: 不正な入力にはエラーをスロー

### ❌ 間違い4: チェック順序の誤り

```typescript
if (value <= 0) {
  throw new Error('正の整数である必要があります');
}

if (!Number.isInteger(value)) {
  throw new Error('整数である必要があります');
}
```

**問題**: `NaN`や`Infinity`が先の条件(`<= 0`)をすり抜ける可能性

**正しい方法**: 有限値・整数チェックを先に実行

## 既存コードとの一貫性

このプロジェクトの既存実装例（参照用）:

- `checkBust` (src/utils/gameLogic.ts:24-36): 残り点数と投擲点数の検証
- `canFinishWithDouble` (src/utils/gameLogic.ts:84-87): 残り点数の検証

新しい関数を追加する際は、これらと同じパターンに従ってください。

## まとめ

### 必ず守るべき3つのルール

1. **すべての数値引数を検証する** - `Number.isFinite()`と`Number.isInteger()`（必要に応じて）
2. **チェック順序を守る** - 有限値 → 整数 → 範囲 → ドメイン
3. **エラーメッセージを統一する** - 標準テンプレートを使用

これらのルールに従うことで、堅牢で保守性の高いコードベースを維持できます。
