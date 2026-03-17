---
name: code-conventions
description: Defines project-wide code conventions for magic number elimination, constant usage, performance optimization, and coordinate system separation. Use when implementing, testing, or reviewing code to ensure consistency across the codebase.
allowed-tools: Read
---

# コード規約スキル

このスキルは、プロジェクトの共通コード規約を定義し、エージェント定義ファイルから参照されます。

## 基本原則

### 1. マジックナンバーの排除

**原則**: ドメイン知識としてみなせる数値は、必ず定数として定義し、コード中での直接記述を避ける。

**定義例**:
```typescript
// ❌ マジックナンバー（避けるべき）
const expectedInnerRadius = mockTransform.physicalDistanceToScreen(7.95);
const expectedOuterRadius = mockTransform.physicalDistanceToScreen(225);

// ✅ 定数インポート（推奨）
import { BOARD_PHYSICAL } from '../../utils/constants';
const expectedInnerRadius = mockTransform.physicalDistanceToScreen(BOARD_PHYSICAL.rings.outerBull);
const expectedOuterRadius = mockTransform.physicalDistanceToScreen(BOARD_PHYSICAL.rings.boardEdge);
```

**ドメイン知識として扱う数値の例**:
- ダーツボード物理サイズ（mm）: 3.175, 7.95, 99, 107, 162, 170, 225など
- セグメント角度: π/10（18度）
- セグメント番号: 1-20
- 有効な得点: 0-60点の特定値
- ゲーム設定: 501, 701, 301点

### 2. 定数参照の原則

**実装ファイルでの定義**:
```typescript
// src/utils/constants.ts
export const BOARD_PHYSICAL = {
  rings: {
    innerBull: 3.175,      // mm
    outerBull: 7.95,       // mm
    tripleInner: 99,       // mm
    tripleOuter: 107,      // mm
    doubleInner: 162,      // mm
    doubleOuter: 170,      // mm
    boardEdge: 225         // mm
  }
} as const;
```

**テストファイルでの使用**:
```typescript
// src/__tests__/integration/dartboard-rendering.test.ts
import { BOARD_PHYSICAL } from '../../utils/constants';

test('期待される半径でテストする', () => {
  const expectedInnerRadius = mockTransform.physicalDistanceToScreen(BOARD_PHYSICAL.rings.outerBull);
  // ...
});
```

**メリット**:
1. 定数値の変更時にテストが自動的に追従する
2. コメントで値の意味を説明する必要がなくなる
3. タイポや値の誤りを防げる
4. ドメイン知識の一元管理が実現される

### 3. パフォーマンス最適化

**原則**: 描画関数などで繰り返し使われる共通処理は、ループ外に抽出する。

**例**:
```typescript
// ❌ 非効率（20回呼び出し）
SEGMENTS.forEach((_, index) => {
  p5.fill(fillColor);
  p5.noStroke();  // ← 毎回呼び出し
  // ...
});

// ✅ 効率的（1回呼び出し）
p5.noStroke();  // ← ループ外で一度だけ
SEGMENTS.forEach((_, index) => {
  p5.fill(fillColor);
  // ...
});
```

### 4. 座標系の分離

**原則**: 物理座標（mm）と画面座標（pixel）を厳密に分離する。

**実装例**:
```typescript
// ✅ 物理座標で計算してから画面座標に変換
const innerRadius = transform.physicalDistanceToScreen(BOARD_PHYSICAL.rings.outerBull);
const outerRadius = transform.physicalDistanceToScreen(BOARD_PHYSICAL.rings.boardEdge);

// ❌ 避けるべき：物理座標と画面座標の混在
const radius = 225 * scale;  // マジックナンバー + スケール計算の混在
```

### 5. コメント規約

**物理座標定数のコメント例**:
```typescript
export const BOARD_PHYSICAL = {
  rings: {
    innerBull: 3.175,      // mm: インナーブル半径（50点エリア）
    outerBull: 7.95,       // mm: アウターブル半径（25点エリア）
    tripleInner: 99,       // mm: トリプルリング内側
    tripleOuter: 107,      // mm: トリプルリング外側
    // ...
  }
} as const;
```

**テストコメント例**:
```typescript
// 期待される半径（画面座標）
// BOARD_PHYSICAL.rings.outerBullを画面座標に変換
const expectedInnerRadius = mockTransform.physicalDistanceToScreen(BOARD_PHYSICAL.rings.outerBull);
```

### 6. 型安全性の原則

**原則**: 型アサーション（`as`）は可能な限り避け、型ガードを使用する。

**型アサーションは避ける（非推奨）**:
```typescript
// ❌ 型アサーション（避けるべき）
const typedPersistedState = persistedState as { config?: Partial<PracticeConfig> };
if (typedPersistedState.config) {
  // 実行時エラーのリスクがある
}
```

**型ガードを使用（推奨）**:
```typescript
// ✅ 型ガード（推奨）
if (
  typeof persistedState === 'object' &&
  persistedState !== null &&
  'config' in persistedState
) {
  const config = persistedState.config;
  if (config && typeof config === 'object') {
    // 型安全に処理できる
  }
}
```

**ヘルパー関数で型ガードを抽出（より推奨）**:
```typescript
// ✅ 再利用可能な型ガード
const isPersistFormat = (
  data: unknown
): data is { state: { config: unknown }; version: number } => {
  return (
    data !== null &&
    typeof data === 'object' &&
    'state' in data &&
    data.state !== null &&
    typeof data.state === 'object' &&
    'config' in data.state
  );
};

// 使用例
if (isPersistFormat(parsed)) {
  return parsed; // 型安全
}
```

**メリット**:
1. 実行時のデータ構造を正確にチェックできる
2. 型アサーションによる誤った型推論を防げる
3. リファクタリング時の安全性が向上する
4. コードの意図が明確になる

### 7. マジック文字列の定数化

**原則**: 繰り返し使用される文字列リテラルは定数として定義する。

**定数化すべき文字列の例**:
```typescript
// ❌ マジック文字列（避けるべき）
const PRESETS = {
  'preset-basic': {
    configId: 'preset-basic',  // 同じ文字列の重複
    // ...
  }
};

// ✅ 定数化（推奨）
const DEFAULT_PRESET_ID = 'preset-basic' as const;
const PRESETS = {
  [DEFAULT_PRESET_ID]: {
    configId: DEFAULT_PRESET_ID,
    // ...
  }
};
```

**メリット**:
1. タイポによるバグを防げる
2. リネーム時の変更箇所が減る
3. コードの意図が明確になる
4. IDEの補完が効く

### 8. エラーハンドリングとロギング

**原則**: サイレントに失敗する場合でも、デバッグ用にログを残す。

**ロギングなし（非推奨）**:
```typescript
// ❌ エラーを無視（デバッグが困難）
try {
  localStorage.setItem(name, JSON.stringify(value));
} catch {
  // エラーハンドリング: 保存失敗時は何もしない
}
```

**ロギングあり（推奨）**:
```typescript
// ✅ console.warnでエラーを記録（推奨）
try {
  localStorage.setItem(name, JSON.stringify(value));
} catch (error) {
  // localStorage容量制限やシリアライズエラーを無視
  // アプリケーションの動作には影響しないため、サイレントに失敗
  console.warn('Failed to persist config to localStorage:', error);
}
```

**メリット**:
1. 本番環境でのデバッグが容易になる
2. エラーの発生頻度を把握できる
3. ユーザー体験を損なわずに問題を追跡できる

**ガイドライン**:
- アプリケーション動作に影響しないエラー → `console.warn`
- ユーザーに通知すべきエラー → UIで表示 + `console.error`
- 開発中のみ必要な情報 → `console.log`（本番では削除）

### 9. 重複コードの排除

**原則**: 同じロジックが複数箇所に存在する場合は、関数として抽出する。

**重複あり（非推奨）**:
```typescript
// ❌ 重複したデフォルト設定ロジック
const loadInitialConfig = (): PracticeConfig => {
  // ...
  return { ...PRESETS['preset-basic'] };
};

const initialState = {
  config: loadInitialConfig(),  // 初期化用関数
};

const getDefaultConfig = (): PracticeConfig => {
  return { ...PRESETS['preset-basic'] };  // 同じロジック
};
```

**重複なし（推奨）**:
```typescript
// ✅ 単一の関数に統一
const getDefaultConfig = (): PracticeConfig => {
  return { ...PRESETS[DEFAULT_PRESET_ID] };
};

const initialState = {
  config: getDefaultConfig(),  // 同じ関数を再利用
};
```

**メリット**:
1. 修正時の変更箇所が減る
2. ロジックの一貫性が保たれる
3. テストが容易になる

### 10. ヘルパー関数の配置と命名

**原則**: ヘルパー関数は使用箇所の前に定義し、意図が明確な名前を付ける。

**配置の例**:
```typescript
// 1. 定数定義
const DEFAULT_PRESET_ID = 'preset-basic' as const;
const PERSIST_VERSION = 0 as const;

// 2. データ定義（定数を使用する可能性がある）
const PRESETS: Record<string, PracticeConfig> = {
  [DEFAULT_PRESET_ID]: { /* ... */ }
};

// 3. ヘルパー関数（データ定義後に配置）
const isPersistFormat = (data: unknown): data is PersistFormat => { /* ... */ };
const getDefaultConfig = (): PracticeConfig => { /* ... */ };

// 4. メインロジック（ヘルパー関数を使用）
export const useGameStore = create<GameStore>()(/* ... */);
```

**命名のガイドライン**:
- 型ガード関数: `is〜Format`（例: `isPersistFormat`, `isPracticeConfigFormat`）
- 取得関数: `get〜`（例: `getDefaultConfig`）
- 変換関数: `to〜`または`〜To〜`（例: `toScreenCoordinate`）
- チェック関数: `has〜`、`can〜`（例: `hasValidConfig`）

## チェックリスト

### 実装時の確認項目

- [ ] ドメイン知識としてみなせる数値が定数として定義されているか
- [ ] テストファイルでも定数をインポートして使用しているか
- [ ] ループ外で実行可能な処理がループ内に含まれていないか
- [ ] 物理座標と画面座標が混在していないか
- [ ] 定数値の変更時にテストが自動的に対応できるか
- [ ] 型アサーション（`as`）を避け、型ガードを使用しているか
- [ ] マジック文字列を定数化しているか
- [ ] サイレントエラーにログ出力を追加しているか
- [ ] 重複コードを関数として抽出しているか
- [ ] ヘルパー関数が適切に配置され、明確な名前が付けられているか

### レビュー時の確認項目

1. **型安全性**:
   - 型アサーション（`as`）が使用されている場合、型ガードに置き換え可能か？
   - `unknown`型のデータを適切に型ガードでチェックしているか？

2. **可読性**:
   - 複雑な型ガードロジックをヘルパー関数として抽出できるか？
   - 関数名が意図を明確に表しているか？

3. **保守性**:
   - マジック文字列/数値が定数化されているか？
   - 重複したロジックが存在しないか？

4. **デバッグ性**:
   - サイレントに失敗するエラーにログ出力があるか？
   - エラーメッセージが問題特定に役立つか？

5. **設計品質**:
   - ヘルパー関数の配置が依存関係を考慮しているか？
   - 単一責任の原則に従っているか？
