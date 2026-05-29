---
name: weekend-remote
description: スマホレビュー向き作業の洗い出しとIssue作成。土日リモート対応用のタスクストックを作成。
---

# Weekend Remote Skill

土日にClaude Codeリモート対応で処理できる作業を洗い出し、Issueとして作成するスキル。

## このスキルを使用するタイミング

以下のキーワードが含まれる場合:

- 「土日用のタスクを洗い出して」
- 「スマホでレビューできる作業をストックしたい」
- 「weekend-remote」
- 「リモート作業用のIssueを作成」

## ワークフロー

```
Phase 1: コードベース探索
  ├── 1.1 技術的負債（console.log, any型, 未使用import等）
  ├── 1.2 リファクタリング候補（命名統一, パターン統一等）
  ├── 1.3 パフォーマンス改善（useMemo不足等）
  └── 1.4 ドキュメント改善（JSDoc不足等）

Phase 2: 候補の分類
  ├── ◎: 差分小、判断不要、5-10分
  ├── ○: 少し判断必要、10-20分
  └── △: PCレビュー推奨

Phase 3: Issue作成
  ├── 3.1 weekend-remote ラベル確認（なければ作成）
  ├── 3.2 各候補をIssueとして作成
  └── 3.3 Claude Code依頼文を含める
```

## 探索対象

### 技術的負債

- `console.log`, `console.warn`, `console.error` の削除漏れ
- `any` 型の使用
- `as unknown as` の二重キャスト
- 未使用の `import`
- TODO/FIXME コメントの放置

### リファクタリング

- `export default` → named export
- `React.FC` の使用
- 直接カラー指定 → セマンティックトークン
- 命名の不統一
- 重複コード

### パフォーマンス

- `useMemo` / `useCallback` の不足
- 毎回新しいオブジェクト/配列を作成
- `new Date()` の重複生成

### ドキュメント

- JSDoc の不足
- `@deprecated` の移行ガイド不足
- テスト意図のコメント不足

## Issue作成テンプレート

```markdown
## 概要

[作業内容の説明]

## 対象ファイル

- `path/to/file.tsx`

## 確認方法

`npm run typecheck && npm run lint`

## 推定時間

X分

## スマホレビュー適性

◎ / ○ / △

## Claude Code依頼文

\`\`\`
[Issue番号]の作業を実施してください。

対象ファイル: [ファイルパス]
作業内容: [具体的な作業内容]

完了後は以下を実行:

- npm run typecheck
- npm run lint
- 変更内容をコミット
  \`\`\`
```

## コマンド

### ラベル作成（初回のみ）

```bash
gh label create "weekend-remote" --description "土日リモート作業用（スマホレビュー可能）" --color "7057FF"
```

### Issue一覧確認

```bash
gh issue list -l weekend-remote
```

### 残りIssue数確認

```bash
gh issue list -l weekend-remote --state open | wc -l
```

## スマホレビュー適性の判断基準

| 適性 | 条件                                           |
| ---- | ---------------------------------------------- |
| ◎    | 差分が10行以内、機械的な変更、判断不要         |
| ○    | 差分が20行程度、少し判断が必要                 |
| △    | 複数ファイル横断、視覚確認必要、PCレビュー推奨 |

## 土日おすすめセット

1回の作業で2-3個のIssueをセットにする:

- **クリーンアップセット**: 未使用ファイル削除 + 設定修正
- **パフォーマンスセット**: useMemo化 x 2-3
- **ドキュメントセット**: JSDoc追加 x 2-3
