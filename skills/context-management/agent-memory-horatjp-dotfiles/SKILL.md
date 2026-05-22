---
name: agent-memory
description: ユーザーが「記憶して」「思い出して」などのメモリ操作を指示した時に使用。重要な調査結果、アーキテクチャの決定、問題の解決策を発見した時にも積極的に保存を提案する。
---

# Agent Memory

会話をまたいで知識を保存・復元するスキルです。記憶は `.claude/skills/agent-memory/memories/` に保存されます。

## 使用タイミング

### ユーザーからの指示
- 「記憶して」「保存して」「覚えておいて」
- 「思い出して」「○○について思い出して」
- 「メモを確認して」「記憶を整理して」

### プロアクティブ（積極的な使用）
以下の場合は、ユーザーに保存を提案してください：
- 重要な調査結果を発見した時
- 非自明なコードパターンを見つけた時
- 問題の解決策を導き出した時
- アーキテクチャ上の決定を行った時
- 既知の問題領域を調査する前に記憶を確認

## 保存方法

### 1. カテゴリフォルダを作成
```bash
mkdir -p memories/<category-name>
```

kebab-case形式で命名（例: `file-processing`, `react-patterns`, `api-design`）

### 2. マークダウンファイルを作成

必須front matterを含むファイルを作成：

```markdown
---
summary: "簡潔な1-2行の要約"
created: 2025-01-09
---

# タイトル

詳細な内容をここに記述...
```

### オプションのfront matterフィールド
- `updated`: 最終更新日（YYYY-MM-DD）
- `status`: `in-progress`, `resolved`, `blocked`, `abandoned`
- `tags`: 検索用タグの配列 `[tag1, tag2]`
- `related`: 関連ファイルのパス配列

### 3. ファイル例

```markdown
---
summary: "ReactのuseEffectでクリーンアップ関数を使う方法"
created: 2025-01-09
status: resolved
tags: [react, hooks, cleanup]
related:
  - src/components/Timer.tsx
---

# useEffect クリーンアップパターン

## 問題
タイマーが正しくクリアされず、メモリリークが発生。

## 解決策
useEffectからクリーンアップ関数を返す：

\`\`\`typescript
useEffect(() => {
  const timer = setTimeout(() => {
    // 処理
  }, 1000);

  return () => clearTimeout(timer);
}, []);
\`\`\`
```

## 復元方法（Summary-First アプローチ）

### 1. カテゴリ一覧を確認
```bash
ls -d memories/*/
```

### 2. サマリー一覧を表示（推奨）
```bash
rg --no-ignore --hidden '^summary:' memories/
```

`--no-ignore --hidden` フラグは必須（memories ディレクトリは .gitignore 対象のため）

### 3. キーワードでサマリー検索
```bash
rg --no-ignore --hidden '^summary:.*<キーワード>' memories/ -i
```

### 4. タグで検索
```bash
rg --no-ignore --hidden '^tags:.*\[.*<タグ>.*\]' memories/ -i
```

### 5. 全文検索（必要な場合のみ）
```bash
rg --no-ignore --hidden '<キーワード>' memories/ -i
```

### 6. ファイルを読み込み
サマリーから該当ファイルを特定したら、Read toolで内容を確認。

## メンテナンス操作

### 更新
1. ファイルを編集
2. `updated` フィールドを追加・更新
3. 必要に応じて `status` を変更

### 削除
```bash
trash memories/<category>/<file>.md
# または
rm memories/<category>/<file>.md
```

空になったカテゴリフォルダも削除：
```bash
rmdir memories/<category>
```

### 統合・再編成
関連する記憶が増えてきたら：
- 複数のメモを1つに統合
- カテゴリを再編成
- 重複を削除

## ベストプラクティス

### 記述のポイント
- **自己完結的に**: 前提知識なしで理解できるように記述
- **決定的なサマリー**: サマリーだけで重要度を判断できるように
- **最新性を保つ**: 古い情報は更新または削除
- **実用性重視**: 本当に役立つ内容に絞る

### 保存する内容
✅ 調査結果・発見したパターン
✅ 問題の解決方法・回避策
✅ アーキテクチャの決定と理由
✅ プロジェクト固有の知識・設定

### 保存しない内容
❌ 一時的な情報
❌ 頻繁に変更される情報
❌ 機密情報（パスワード、APIキーなど）

## フォルダ構成例

```
memories/
├── react/
│   ├── hooks-cleanup.md
│   └── state-management.md
├── typescript/
│   └── type-narrowing.md
├── api-design/
│   ├── rest-conventions.md
│   └── error-handling.md
└── project-context/
    └── architecture-decisions.md
```

## 注意事項

- `memories/` ディレクトリは `.gitignore` で除外される（個人用のメモのため）
- ファイル名・フォルダ名はkebab-case形式を使用
- ripgrep検索時は必ず `--no-ignore --hidden` フラグを使用
- Summary-Firstアプローチで効率的に検索（全文検索は最終手段）
