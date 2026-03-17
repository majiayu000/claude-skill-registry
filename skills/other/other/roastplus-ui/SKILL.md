---
name: roastplus-ui
description: ローストプラスアプリのUIデザインシステム。Tailwind CSS v4ベースの配色、コンポーネントパターン、レイアウト、アニメーションを提供。新規ページ作成、コンポーネント実装、デザイン一貫性チェックに使用。通常モードとクリスマスモードの両方に対応。
---

# ローストプラス UIデザインシステム

## デザイン哲学

- **高級感**: コーヒーの焙煎という専門的で高級な活動を表現
- **親しみやすさ**: 温かみのあるオレンジと黒を基調とした色選び
- **使いやすさ**: 最小タッチサイズ44px、レスポンシブデザイン、アクセシビリティ対応

## クイックスタート

### 新規ページ作成（3ステップ）

**1. ページタイプを決める**
- フル画面レイアウト（タイマー、スケジュール系）
- スクロール可能レイアウト（リスト、記録系）
- フォームレイアウト（設定、入力系）

**2. テンプレートを使用**

```tsx
'use client';
import { useAuth } from '@/lib/auth';
import { useAppLifecycle } from '@/hooks/useAppLifecycle';

export default function YourPage() {
  const { user, loading } = useAuth();
  useAppLifecycle();

  if (loading) return <Loading />;
  if (!user) return <LoginPage />;

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#F7F7F5' }}>
      <div className="container mx-auto px-4 sm:px-6 py-4 sm:py-6 max-w-4xl">
        <header className="mb-6 sm:mb-8">
          {/* ヘッダー */}
        </header>
        <main className="bg-white rounded-lg shadow-md p-6">
          {/* コンテンツ */}
        </main>
      </div>
    </div>
  );
}
```

**3. コンポーネントを追加**

詳細なコンポーネントパターンは `references/components.md` を参照。

## ブランドカラー

| 名称 | 16進数 | 用途 | Tailwindクラス |
|------|--------|------|----------------|
| Primary Orange | `#EF8A00` | メインアクション | `amber-600` |
| Dark Brown | `#211714` | ヘッダー、濃い背景 | `dark` |
| Background | `#F7F7F5` | ページ背景 | - |

詳細は `references/color-schemes.md` を参照。

## 共通コンポーネント（必須）

**⚠️ UI作成時は必ず `@/components/ui` の共通コンポーネントを使用すること。生のTailwindでボタンやカードを作成しない。**

### ルール
1. **既存コンポーネントを優先使用** → 作成前に必ず確認
2. **既存で対応不可の場合** → `components/ui/` に新規共通コンポーネントを作成
3. **共通コンポーネントの重複禁止** → 類似機能のコンポーネントを作らない

### インポート
```tsx
import {
  Button, IconButton,           // ボタン系
  Input, NumberInput, InlineInput, Textarea, Select, Checkbox, Switch,  // フォーム系
  Card, Modal, Dialog,          // コンテナ系
  Badge, Tabs, Accordion, ProgressBar, EmptyState  // その他
} from '@/components/ui';
```

### 使用例

```tsx
// ❌ NG: 生のTailwindでボタンを作成
<button className="px-6 py-3 bg-amber-600 text-white rounded-lg">保存</button>

// ✅ OK: 共通コンポーネントを使用
<Button variant="primary" isChristmasMode={isChristmasMode}>保存</Button>
```

```tsx
// ❌ NG: 生のTailwindでカードを作成
<div className="bg-white rounded-2xl shadow-md p-5">...</div>

// ✅ OK: 共通コンポーネントを使用
<Card variant="hoverable" isChristmasMode={isChristmasMode}>...</Card>
```

```tsx
// ❌ NG: 生のTailwindで入力を作成
<input className="w-full rounded-lg border-2 border-gray-200 px-4 py-3.5" />

// ✅ OK: 共通コンポーネントを使用
<Input label="名前" placeholder="入力" isChristmasMode={isChristmasMode} />
```

### クリスマスモード対応
すべての共通コンポーネントは `isChristmasMode` propをサポート：
```tsx
const { isChristmasMode } = useChristmasMode();

<Button isChristmasMode={isChristmasMode}>...</Button>
<Card isChristmasMode={isChristmasMode}>...</Card>
<Input isChristmasMode={isChristmasMode} />
```

## リファレンスドキュメント

詳細な実装パターン、バリエーション、ベストプラクティスは以下を参照:

- **[components.md](references/components.md)** - 全コンポーネントパターン（ボタン、カード、モーダル、入力等）
- **[color-schemes.md](references/color-schemes.md)** - 配色スキーム、テーマ切り替え
- **[layouts.md](references/layouts.md)** - レイアウトパターン、スペーシング、レスポンシブ設計
- **[animations.md](references/animations.md)** - アニメーション、トランジション、Framer Motion
- **[christmas-mode.md](references/christmas-mode.md)** - クリスマスモード実装ガイド

## ベストプラクティス

### アクセシビリティ
- すべてのタッチターゲット: `min-h-[44px]`
- フォーカスリング: `focus-visible:ring-2`
- ARIA属性を適切に使用

### レスポンシブデザイン
- モバイルファースト設計
- ブレークポイント: `sm:` (640px), `md:` (768px), `lg:` (1024px)

### クリスマスモード対応
- `useChristmasMode()` フックを使用
- 詳細は `references/christmas-mode.md` を参照

## 使用時のワークフロー

1. **新規ページ作成**: テンプレートを使用 → `components.md` からパターン選択
2. **コンポーネント実装**: `components.md` で該当パターン検索 → コピー&調整
3. **デザイン一貫性チェック**: 配色、タッチサイズ、レスポンシブ確認
4. **クリスマスモード対応**: 必要な場合は `christmas-mode.md` を参照
