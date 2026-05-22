---
name: ui-component
description: ReactコンポーネントとTailwind CSSスタイリングの実装パターン提供
version: 1.0.0
tools:
  - Read
  - Grep
  - Glob
skill_type: knowledge
auto_invoke: false
---

# フロントエンドUI実装パターン

## 概要

Reactコンポーネントの作成とTailwind CSSスタイリングの定型パターンを提供します。UI実装の標準化とデザインシステムの一貫性を確保します。

## 技術スタック

- **フレームワーク**: React 18 + TypeScript
- **スタイリング**: Tailwind CSS 3
- **状態管理**: Zustand
- **ルーティング**: React Router v6
- **ビルドツール**: Vite

## コンポーネント実装パターン

### 基本構造

**ファイル構成**:
```
main/frontend/src/
├── pages/          # ページコンポーネント
│   └── RaceDetailPage.tsx
├── components/     # 共通コンポーネント
│   └── RaceCard.tsx
├── stores/         # Zustand ストア
│   ├── appStore.ts
│   └── cartStore.ts
├── types/          # 型定義
│   └── index.ts
└── api/            # APIクライアント
    └── client.ts
```

### ページコンポーネントパターン

**テンプレート**:
```typescript
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppStore } from '../stores/appStore';
import type { <Type> } from '../types';
import { apiClient } from '../api/client';

export function <Page>Page() {
  const { <param> } = useParams<{ <param>: string }>();
  const navigate = useNavigate();
  const showToast = useAppStore((state) => state.showToast);

  const [data, setData] = useState<<Type> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!<param>) return;

    let isMounted = true;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      const response = await apiClient.get<Resource>(<param>);

      if (!isMounted) return;

      if (response.success && response.data) {
        setData(response.data);
      } else {
        setError(response.error || 'データ取得に失敗しました');
      }

      setLoading(false);
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [<param>]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!data) return <EmptyState />;

  return (
    <div className="container mx-auto p-4">
      {/* コンテンツ */}
    </div>
  );
}
```

**重要な原則**:
- `isMounted` フラグでメモリリーク防止
- ローディング・エラー・空状態を適切にハンドリング
- Zustand ストアでグローバル状態管理

### 馬券関連UIパターン

#### レースカード

```typescript
interface RaceCardProps {
  race: Race;
  onClick?: () => void;
}

export function RaceCard({ race, onClick }: RaceCardProps) {
  return (
    <div
      className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow cursor-pointer"
      onClick={onClick}
    >
      {/* レース番号・時刻 */}
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-bold text-gray-700">{race.number}</span>
        <span className="text-sm text-gray-500">{race.time}</span>
      </div>

      {/* レース名 */}
      <h3 className="text-lg font-bold mb-2">{race.name}</h3>

      {/* 距離・馬場状態 */}
      <div className="flex gap-2 flex-wrap">
        {race.distance && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
            {race.distance}m
          </span>
        )}
        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
          {race.condition}
        </span>
      </div>
    </div>
  );
}
```

#### 出走馬カード

```typescript
interface RunnerCardProps {
  runner: Horse;
  selected?: boolean;
  onToggle?: () => void;
}

export function RunnerCard({ runner, selected, onToggle }: RunnerCardProps) {
  return (
    <div
      className={`
        border-2 rounded-lg p-3 cursor-pointer transition-all
        ${selected ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-400'}
      `}
      onClick={onToggle}
    >
      {/* 枠番・馬番 */}
      <div className="flex items-center gap-2 mb-2">
        <span
          className="w-8 h-8 flex items-center justify-center rounded font-bold text-sm"
          style={{
            backgroundColor: runner.color,
            color: runner.textColor,
          }}
        >
          {runner.wakuBan}
        </span>
        <span className="text-lg font-bold">{runner.number}</span>
      </div>

      {/* 馬名 */}
      <h4 className="font-semibold mb-1">{runner.name}</h4>

      {/* 騎手 */}
      <p className="text-sm text-gray-600 mb-2">{runner.jockey}</p>

      {/* オッズ・人気 */}
      <div className="flex justify-between items-center">
        <span className="text-sm font-semibold text-orange-600">
          {runner.odds.toFixed(1)}倍
        </span>
        <span className="text-xs text-gray-500">{runner.popularity}人気</span>
      </div>

      {/* 馬体重（オプション） */}
      {runner.weight && (
        <div className="mt-2 text-xs text-gray-600">
          馬体重: {runner.weight}kg
          {runner.weightDiff !== undefined && (
            <span className={runner.weightDiff >= 0 ? 'text-red-600' : 'text-blue-600'}>
              {' '}({runner.weightDiff >= 0 ? '+' : ''}{runner.weightDiff})
            </span>
          )}
        </div>
      )}
    </div>
  );
}
```

### Tailwind CSSパターン

#### 色の使い方

**JRA公式カラー**:
```typescript
// 枠色（main/frontend/src/types/index.ts で定義）
export const WakuColors: Record<number, { background: string; text: string }> = {
  1: { background: '#FFFFFF', text: '#000000' }, // 白枠
  2: { background: '#000000', text: '#FFFFFF' }, // 黒枠
  3: { background: '#E8384F', text: '#FFFFFF' }, // 赤枠
  4: { background: '#1E90FF', text: '#FFFFFF' }, // 青枠
  5: { background: '#FFD700', text: '#000000' }, // 黄枠
  6: { background: '#2E8B57', text: '#FFFFFF' }, // 緑枠
  7: { background: '#FF8C00', text: '#FFFFFF' }, // 橙枠
  8: { background: '#FF69B4', text: '#FFFFFF' }, // 桃枠
};
```

**状態色**:
```css
/* 成功 */
.bg-green-100 .text-green-800

/* 警告 */
.bg-yellow-100 .text-yellow-800

/* エラー */
.bg-red-100 .text-red-800

/* 情報 */
.bg-blue-100 .text-blue-800

/* ニュートラル */
.bg-gray-100 .text-gray-800
```

#### レイアウトパターン

**コンテナ**:
```tsx
<div className="container mx-auto p-4 max-w-7xl">
  {/* コンテンツ */}
</div>
```

**カード**:
```tsx
<div className="bg-white rounded-lg shadow-md p-4">
  {/* カードコンテンツ */}
</div>
```

**グリッド（レスポンシブ）**:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* グリッドアイテム */}
</div>
```

**Flexbox**:
```tsx
{/* 横並び（両端揃え） */}
<div className="flex justify-between items-center">
  <span>左</span>
  <span>右</span>
</div>

{/* 横並び（中央揃え） */}
<div className="flex justify-center items-center gap-2">
  <span>アイテム1</span>
  <span>アイテム2</span>
</div>
```

#### バッジパターン

**グレード・クラスバッジ**:
```tsx
function getGradeBadgeColor(grade: RaceGrade): string {
  switch (grade) {
    case 'G1': return 'bg-gradient-to-r from-yellow-400 to-yellow-600 text-white';
    case 'G2': return 'bg-gradient-to-r from-gray-300 to-gray-400 text-gray-800';
    case 'G3': return 'bg-gradient-to-r from-orange-300 to-orange-500 text-white';
    case 'L': return 'bg-black text-white';
    case 'OP': return 'bg-gray-700 text-white';
    default: return 'bg-gray-200 text-gray-700';
  }
}

<span className={`px-2 py-1 text-xs font-bold rounded ${getGradeBadgeColor(race.gradeClass)}`}>
  {race.gradeClass}
</span>
```

**コース種別バッジ**:
```tsx
<span className={`px-2 py-1 text-xs rounded ${
  race.trackType === '芝' ? 'bg-green-100 text-green-800' :
  race.trackType === 'ダ' ? 'bg-amber-100 text-amber-800' :
  'bg-gray-100 text-gray-800'
}`}>
  {race.trackType}
</span>
```

### 状態管理パターン（Zustand）

**ストア定義**:
```typescript
import { create } from 'zustand';

interface AppState {
  isLoading: boolean;
  toastMessage: string | null;
  setLoading: (loading: boolean) => void;
  showToast: (message: string) => void;
  hideToast: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  isLoading: false,
  toastMessage: null,
  setLoading: (loading) => set({ isLoading: loading }),
  showToast: (message) => set({ toastMessage: message }),
  hideToast: () => set({ toastMessage: null }),
}));
```

**使用例**:
```typescript
// コンポーネント内
const showToast = useAppStore((state) => state.showToast);
const toastMessage = useAppStore((state) => state.toastMessage);

// トースト表示
showToast('カートに追加しました');
```

### フォーム入力パターン

**数値入力（金額）**:
```tsx
<div className="mb-4">
  <label className="block text-sm font-medium text-gray-700 mb-2">
    掛け金
  </label>
  <div className="flex items-center gap-2">
    <input
      type="number"
      min="100"
      step="100"
      value={betAmount}
      onChange={(e) => setBetAmount(Number(e.target.value))}
      className="border border-gray-300 rounded px-3 py-2 w-32"
    />
    <span className="text-gray-600">円</span>
  </div>
</div>
```

**セレクトボックス（券種）**:
```tsx
<select
  value={betType}
  onChange={(e) => setBetType(e.target.value as BetType)}
  className="border border-gray-300 rounded px-3 py-2"
>
  {betTypes.map((type) => (
    <option key={type} value={type}>
      {BetTypeLabels[type]}
    </option>
  ))}
</select>
```

### ボタンパターン

**プライマリボタン**:
```tsx
<button
  onClick={handleSubmit}
  disabled={!isValid}
  className="
    bg-blue-600 hover:bg-blue-700
    disabled:bg-gray-300 disabled:cursor-not-allowed
    text-white font-semibold
    px-6 py-3 rounded-lg
    transition-colors
  "
>
  カートに追加
</button>
```

**セカンダリボタン**:
```tsx
<button
  onClick={handleCancel}
  className="
    bg-white border border-gray-300
    hover:bg-gray-50
    text-gray-700
    px-6 py-3 rounded-lg
    transition-colors
  "
>
  キャンセル
</button>
```

**危険なアクション**:
```tsx
<button
  onClick={handleDelete}
  className="
    bg-red-600 hover:bg-red-700
    text-white font-semibold
    px-4 py-2 rounded
    transition-colors
  "
>
  削除
</button>
```

## 参照ファイル

- **ページ例**: `main/frontend/src/pages/RaceDetailPage.tsx`
- **型定義**: `main/frontend/src/types/index.ts`
- **ストア**: `main/frontend/src/stores/`
- **Tailwind設定**: `main/frontend/tailwind.config.js`

## 注意事項

- **レスポンシブ**: モバイルファーストで実装
- **アクセシビリティ**: セマンティックHTMLを使用
- **パフォーマンス**: useMemo, useCallback で最適化
- **一貫性**: 既存コンポーネントのスタイルを踏襲
