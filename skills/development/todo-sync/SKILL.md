---
name: todo-sync
description: 'description: docs/TODOS.mdとコード内TODOコメントを抽出・照合し同期する。ripgrep/scantodos.shで現況を収集し、ドキュメント追記と不要TODO削除に使う。'
---

name: todo-sync
description: docs/TODOS.mdとコード内TODOコメントを抽出・照合し同期する。ripgrep/scan_todos.shで現況を収集し、ドキュメント追記と不要TODO削除に使う。

# Todo Sync

## Overview
- docs/TODOS.mdとコード/テンプレート/テストのTODOを集約し、差分を解消する手順。
- フロー: スキャン → 照合 → docs更新 → コード側リンク追記 → 再確認。

## Quick start
- 既存TODO確認: `docs/TODOS.md` の見出しごとの粒度とチェックボックス使用方針を把握（実行タスクは `- [ ] 説明`）。
- スキャン: `bash skills/todo-sync/scripts/scan_todos.sh tmp/todo-scan.txt`（出力先省略可、`.venv`/`skills`/`node_modules`除外）
- 確認: `cat tmp/todo-scan.txt` で位置と内容をチェック。

## 同期ワークフロー
1. バケット分け: スキャン結果を「既存TODO対応」「新規追加」「不要/完了」に分類。
2. docs反映:
   - 実行タスクはチェックボックス形式で追記: `- [ ] 命令形・簡潔`。完了時は `[x]`。
   - 完了/不要は行削除し、対応するコードTODOも除去/更新。
3. コード側メモ:
   - TODOコメントに対応先: `# TODO[docs/TODOS.md:L12] 説明` / `// TODO[docs/TODOS.md:L12] 説明`
   - ドキュメントのみのTODOは可能なら参照ファイルを付記: `- ... (src/...)`
4. 再スキャン: 変更後に再度 `scan_todos.sh` を実行し残存TODOを確認。

## scripts/
- `scripts/scan_todos.sh`: ripgrepでTODOを走査し指定ファイルへ保存。`.venv`/`skills`/`node_modules`を除外。出力空でもファイルは生成。

## references/
- なし。必要になったら追加。
