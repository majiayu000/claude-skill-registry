---
name: implementation-planning
description: 複雑なタスク（3ステップ以上・複数ファイル変更）の実装前に使用。計画ファイルを作成し進捗を追跡。
---

## Overview

複雑なタスクを計画的に実装するためのスキルです。計画ファイルを作成し、進捗を追跡しながら実装を進めます。

## Files in This Skill

- **SKILL.md** (this file) - プロセス概要
- **templates/plan-template.md** - 計画ファイルのテンプレート

## When to Use

以下の場合に使用:

1. **複雑な実装タスク** - 3つ以上のステップや複数のファイル変更が必要
2. **新機能の追加** - 新しいコンポーネント、API、機能を追加
3. **リファクタリング** - 複数のファイルにまたがる変更
4. **バグ修正** - 調査と修正が複数ステップにわたる場合

## When NOT to Use

以下の場合は計画ファイルを作成せず直接実装:

1. 単一ファイルの小さな変更（数行の修正）
2. タイポ修正やコメント追加
3. 既存のパターンを使った簡単な追加
4. 明らかに1ステップで完了するタスク

## Process

### Step 1: Create Plan File

`.implementation-plan-{session-id-suffix}.md` を作成

- `session-id-suffix`: セッションIDの最後の8文字
- 例: `.implementation-plan-n2CmeYid.md`

テンプレートは `templates/plan-template.md` を参照

### Step 2: User Confirmation

計画作成後、**必ずユーザーに確認を求める**:

```
実装計画を作成しました: `.implementation-plan-{suffix}.md`

この計画で実装を進めてよろしいでしょうか？

計画の概要:
- [ゴール1]
- [ゴール2]
- [ゴール3]

実装ステップ数: X

承認いただけましたら、実装を開始します。
```

**ユーザーからの承認を得るまで実装を開始しない**

### Step 3: Execute with Progress Tracking

1. **ステップ開始時**: ステータスを `PENDING` → `IN_PROGRESS` に更新
2. **実装中**: ファイルを作成・編集
3. **ステップ完了時**: ステータスを `IN_PROGRESS` → `COMPLETED` に更新
4. **問題発生時**: Progress Logに記録

### Step 4: Testing & Validation

Testing Planに従ってテストを実行:

```bash
bun run build:dev  # ビルド確認
bun run lint       # Lint確認
bun run type       # 型チェック
```

### Step 5: Completion

1. 計画ファイルのステータスを `COMPLETED` に更新
2. Goals セクションの全チェックボックスを完了に
3. ユーザーに完了報告

```
実装が完了しました！

✅ 全ての目標を達成
✅ ビルド成功
✅ Lint通過
✅ テスト完了

変更されたファイル:
- src/component/atoms/Button.tsx (作成)
- src/component/atoms/Button.stories.tsx (作成)
```

## Best Practices

### Planning Phase

1. **Be Specific**: 曖昧な表現を避け、具体的なアクションを記載
2. **Be Comprehensive**: 途中でユーザーに質問しなくて済むように
3. **Be Realistic**: 各ステップの作業量を現実的に見積もる

### Implementation Phase

1. **Follow the Plan**: 計画に従って実装
2. **Document Changes**: 計画からの逸脱は記録
3. **Update Progress**: 各ステップ完了時に更新
4. **Test Regularly**: 各ステップ完了後に動作確認

### Communication

1. **Initial Confirmation**: 計画作成後、必ずユーザー確認
2. **Progress Updates**: 長時間の場合、途中経過を報告
3. **Completion Report**: 完了時に明確なサマリー
4. **Be Transparent**: 問題や変更があれば正直に報告

## Example

```markdown
# Implementation Plan: Add User Profile Edit Feature

## Goals
- [ ] ユーザーがプロフィール情報を編集できる
- [ ] 編集内容がAPIに保存される
- [ ] バリデーションエラーが適切に表示される

## Implementation Steps

### 1. Create Profile Edit Form Component
**Status**: PENDING
**What to do**:
- ProfileEditFormコンポーネントを作成
- LabeledInput, TextArea, Button を使用

**Files to modify**:
- `src/component/organisms/ProfileEditForm.tsx` (create)

**Completion criteria**:
- フォームが表示される
- 各フィールドに入力できる
```

## Summary

1. **計画的な実装**: 事前に詳細な計画を立てる
2. **進捗の可視化**: 計画ファイルで進捗を追跡
3. **ユーザーとの協調**: 計画段階でユーザー確認
4. **問題の記録**: 実装中の問題や解決策を記録
5. **完了の明確化**: 何が完了し、何が残っているか明確に