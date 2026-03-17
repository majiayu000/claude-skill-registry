---
name: UI/UXデザインガイドライン
description: 共通UIコンポーネント、カラーパレット、タイポグラフィ、スペーシング、空状態デザイン。UI実装、コンポーネント作成、スタイリング時に使用。
---

# UI/UXデザインガイドライン

## テーマ・カラーシステム

### ダークモード対応

このアプリはライト/ダークモード対応。**ハードコード色は使用禁止**。

```tsx
// ❌ 禁止: ハードコード色
<div className="bg-white text-gray-800 border-gray-300">

// ✅ 推奨: セマンティックカラー
<div className="bg-card text-foreground border-input">
```

### セマンティックカラー対応表

| 用途 | セマンティック | 旧ハードコード |
|------|---------------|----------------|
| カード背景 | `bg-card` | `bg-white` |
| ページ背景 | `bg-background` | `bg-gray-50` |
| ミュート背景 | `bg-muted` | `bg-gray-50`, `bg-gray-100` |
| 主要テキスト | `text-foreground` | `text-gray-800`, `text-gray-900` |
| 副次テキスト | `text-muted-foreground` | `text-gray-500`, `text-gray-600` |
| ボーダー | `border` | `border-gray-200` |
| 入力ボーダー | `border-input` | `border-gray-300` |

### カラー背景にはdark:バリアントを追加

```tsx
// カラー背景は dark: バリアントを追加
<div className="bg-blue-50 dark:bg-blue-950">
<div className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
```

## shadcn/ui コンポーネント

### 必須インポート

```tsx
// ボタン
import { Button } from "@/components/ui/button";

// カード
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

// テーブル
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

// バッジ
import { Badge } from "@/components/ui/badge";

// ダイアログ（モーダル）
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

// スイッチ
import { Switch } from "@/components/ui/switch";

// 入力
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
```

### ボタンバリアント

```tsx
<Button variant="default">主要アクション</Button>
<Button variant="secondary">副次アクション</Button>
<Button variant="destructive">削除</Button>
<Button variant="outline">アウトライン</Button>
<Button variant="ghost">ゴースト</Button>
```

## レイアウトパターン

### ページコンテナ

```tsx
// 標準ページ
<div className="max-w-7xl mx-auto">
  <Card>
    <CardContent className="p-6">
      {/* コンテンツ */}
    </CardContent>
  </Card>
</div>

// タブ付きページ（ヘッダーにタブがある場合）
<div className="max-w-7xl mx-auto mt-8">
  {/* mt-8でタブとの間隔を確保 */}
</div>
```

### テーブルレイアウト

```tsx
<Card>
  <CardContent className="p-6">
    {/* ヘッダー：タイトル + アクション */}
    <div className="flex items-center justify-between mb-6">
      <div className="flex items-center gap-3">
        <Icon className="w-6 h-6 text-primary" />
        <h2 className="text-xl font-semibold text-foreground">タイトル</h2>
      </div>
      <Button>
        <Plus className="w-4 h-4 mr-2" />
        新規作成
      </Button>
    </div>

    {/* 検索・フィルター */}
    <div className="flex items-center gap-4 mb-4">
      <Input placeholder="検索..." className="max-w-sm" />
      <Select>...</Select>
    </div>

    {/* 合計表示 */}
    <div className="text-sm text-muted-foreground mb-4">
      合計: {total}
    </div>

    {/* テーブル */}
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>カラム</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {items.map((item) => (
          <TableRow key={item.id}>
            <TableCell>{item.value}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>

    {/* ページネーション */}
    <div className="flex items-center justify-end gap-2 mt-4">
      <Button variant="outline" size="sm" disabled={page === 1}>
        前へ
      </Button>
      <span className="text-sm text-muted-foreground">
        {page} / {totalPages}
      </span>
      <Button variant="outline" size="sm" disabled={page === totalPages}>
        次へ
      </Button>
    </div>
  </CardContent>
</Card>
```

## モーダル（Dialog）

### 作成・編集フォーム用

```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent className="sm:max-w-[500px]">
    <DialogHeader>
      <DialogTitle>新規作成</DialogTitle>
    </DialogHeader>
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">名前</Label>
        <Input id="name" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div className="flex justify-end gap-3">
        <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>
          キャンセル
        </Button>
        <Button type="submit">作成</Button>
      </div>
    </form>
  </DialogContent>
</Dialog>
```

### FormModalコンポーネント（複雑なフォーム用）

```tsx
import { FormModal } from "@/components/modals/FormModal";

<FormModal
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  onSubmit={handleSubmit}
  title="新規作成"
  submitLabel="作成"
  cancelLabel="キャンセル"
  language="ja"
  maxWidth="2xl"
>
  {/* フォームフィールド */}
</FormModal>
```

## 空状態（Empty State）

```tsx
{data.length === 0 && (
  <div className="text-center py-12 text-muted-foreground">
    <Icon className="w-12 h-12 mx-auto mb-4 opacity-50" />
    <p>データがありません</p>
  </div>
)}
```

## フォーム要素

### 標準入力

```tsx
<div className="space-y-2">
  <Label htmlFor="field">
    フィールド名 <span className="text-red-500">*</span>
  </Label>
  <Input
    id="field"
    value={value}
    onChange={(e) => setValue(e.target.value)}
    placeholder="入力してください"
  />
</div>
```

### セレクト

```tsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

<Select value={value} onValueChange={setValue}>
  <SelectTrigger className="w-[200px]">
    <SelectValue placeholder="選択してください" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="option1">オプション1</SelectItem>
    <SelectItem value="option2">オプション2</SelectItem>
  </SelectContent>
</Select>
```

## バッジ

### ロールバッジ（ダークモード対応）

```tsx
const roleColors = {
  ADMIN: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200",
  MANAGER: "bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-200",
  USER: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  GUEST: "bg-muted text-muted-foreground",
};

<Badge className={roleColors[role]}>{role}</Badge>
```

### ステータスバッジ

```tsx
// 有効
<Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
  有効
</Badge>

// 無効
<Badge className="bg-muted text-muted-foreground">
  無効
</Badge>

// 警告
<Badge className="bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200">
  未登録
</Badge>
```

## タイポグラフィ

```tsx
// ページタイトル（Headerで表示）
<h1 className="text-xl font-bold text-foreground">

// セクションタイトル
<h2 className="text-xl font-semibold text-foreground">

// カードタイトル
<h3 className="text-lg font-semibold text-foreground">

// ラベル
<Label className="text-sm font-medium text-foreground">

// 本文
<p className="text-sm text-muted-foreground">

// 小さいテキスト
<span className="text-xs text-muted-foreground">
```

## スペーシング

| 用途 | クラス |
|------|--------|
| カード内パディング | `p-6` または `p-8` |
| セクション間 | `space-y-6` |
| フォーム要素間 | `space-y-4` |
| ボタン間 | `gap-3` |
| アイコンとテキスト間 | `gap-2` または `gap-3` |
| ページとヘッダータブ間 | `mt-8` |

## 戻るボタン（BackButton）

```tsx
import { BackButton } from "@/components/ui/BackButton";

// アイコンのみ（推奨）
<BackButton href="/parent-page" />

// ラベル付き
<BackButton href="/parent-page" label="一覧に戻る" />

// onClick対応
<BackButton onClick={() => setSelectedItem(null)} />
```

## チェックリスト

新しいUIを作成する際:

- [ ] ハードコード色を使用していない（`bg-white`, `text-gray-*` など禁止）
- [ ] セマンティックカラーを使用（`bg-card`, `text-foreground` など）
- [ ] カラー背景には `dark:` バリアントを追加
- [ ] shadcn/ui コンポーネントを使用
- [ ] 適切なスペーシングを適用
- [ ] 空状態を実装
- [ ] モバイル対応を考慮
