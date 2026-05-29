---
name: format-ui-display
description: UI表示用の日付、enum値をフォーマットします。日本語形式の日付、相対日付が必要な場合に使用します。
---

# UI表示フォーマットスキル

データを適切な形式でUI表示するためのスキルです。日付フォーマットとenumラベル変換を提供します。

## いつ使うか

このスキルは以下の場合に使用してください：

- テーブル・詳細画面で日付を表示する
- 相対的な日付表示（「5分前」「3日前」など）を実装する
- enum値（権限、ステータス、カテゴリ）を日本語ラベルに変換する
- Badge やその他のUIコンポーネントでラベル表示する

## クイックスタート

### 日付フォーマット

```typescript
import { formatDate } from '@repo/utils/format-date'

// 一覧画面
export function UsersTable({ users }: { users: User[] }) {
  return (
    <TableRow>
      <TableCell>{formatDate(user.createdAt, 'YYYY年M月D日')}</TableCell>
    </TableRow>
  )
}

// 詳細画面
export function UserDetail({ user }: { user: User }) {
  return (
    <div>
      <Label>作成日</Label>
      <p>{formatDate(user.createdAt, 'YYYY年M月D日 HH:mm')}</p>
    </div>
  )
}
```

## 詳細パターン

詳細な実装パターンについては references を参照してください：

- [date-formatting.md](references/date-formatting.md) - 日付フォーマットの詳細オプション、相対表示、カスタムフォーマット
