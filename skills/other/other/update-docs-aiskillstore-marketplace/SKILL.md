---
name: update-docs
description: ドキュメント更新スキル（仕様書、設計書、README等の更新）
---

# Update Docs Skill - ドキュメント更新スキル

## 役割

プロジェクトドキュメントの更新を支援するスキルです。機能仕様書、DB設計書、エラーコード一覧、README等の更新を行います。

## 実行フロー

### Phase 1: ドキュメントタイプ判定

#### document_type="feature"
- 対象: `documents/features/[機能名]/specification.md`
- 更新内容: 機能仕様書の更新

#### document_type="database"
- 対象: `documents/architecture/database-design.md`
- 更新内容: データベース設計の更新

#### document_type="errors"
- 対象: `documents/development/error-codes.md`
- 更新内容: エラーコード一覧の更新

#### document_type="readme"
- 対象: `README.md` または各ディレクトリのREADME.md
- 更新内容: README の更新

### Phase 2: ドキュメント読み込み
```bash
# ドキュメントファイルを読み込み
cat [document_path]
```

### Phase 3: 更新内容の適用
- update_content に基づいて更新
- 既存の構造を維持
- Markdown形式を保持

### Phase 4: 更新確認
- 更新後のドキュメント内容を確認
- Markdown構文エラーがないか確認

### Phase 5: 完了報告
```markdown
## Update Docs 完了報告

### 更新ドキュメント
- **タイプ**: [document_type]
- **パス**: [document_path]

### 更新内容
- [update_content]

### 次のステップ
変更内容を確認し、必要に応じてコミットしてください。
```
