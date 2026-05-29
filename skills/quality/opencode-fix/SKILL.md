# OpenCode バグ修正支援

mistakes.md参照・最小差分・大出力はmemory_add退避のバグ修正スキルです。

## 修正フロー

### 1. 再発防止チェックリスト作成（必須）

**最初に `.claude/hooks/mistakes.md` を参照**:

```bash
cat .claude/hooks/mistakes.md
```

過去の失敗パターンから「再発防止チェックリスト」を作成。

### 2. テストログの要約取得

**全文ログは貼らない**:

```bash
npm run test:summary
```

### 3. OpenCode 実行とログ保存

```bash
mkdir -p .opencode/runs
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
opencode run "Fix: <バグ詳細>" > .opencode/runs/fix_${TIMESTAMP}.log 2>&1
```

### 4. ログを memory_add に退避

**会話に貼らず、content_path で保存**:

```
memory_add で .opencode/runs/fix_${TIMESTAMP}.log を保存
→ referenceId を取得
```

### 5. Issue/会話に投稿する内容

```markdown
## OpenCode バグ修正実行結果

### 再発防止チェックリスト
- [x] エラーハンドリング実装済み
- [x] 境界値テスト追加
- [x] 型チェック通過

### 詳細ログ
参照ID: `${refId}`
`memory_search("${refId}")` で取得可能
```

### 6. 最小差分で適用

- 必要最小限の変更のみ
- 既存スタイルと一貫性を保つ
- 過剰なリファクタリングをしない

## 重要な注意事項

1. **mistakes.md は必ず最初に参照**
2. **大量ログは memory_add(content_path)**
3. **要約のみを投稿**
4. **最小差分**
5. **再発防止チェックリスト全項目を検証**
