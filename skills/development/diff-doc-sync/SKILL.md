---
name: diff-doc-sync
description: 'description: git差分/未コミット変更を走査し、影響するdocs/やAGENTS.mdを更新する手順を案内する。コード変更とドキュメント同期が必要なときに使用。'
---

name: diff-doc-sync
description: git差分/未コミット変更を走査し、影響するdocs/やAGENTS.mdを更新する手順を案内する。コード変更とドキュメント同期が必要なときに使用。

# Diff Doc Sync

## Overview
- 変更差分を洗い出し、影響ドキュメントを特定して反映する手順を提供。
- トリガー: コード/設定/UI変更後に docs/ や AGENTS.md 更新が必要なとき。

## Quick start
- 差分取得: `bash skills/diff-doc-sync/scripts/list_changes.sh`（デフォルト: HEADとの差分）
- ステージ済みのみ: `bash skills/diff-doc-sync/scripts/list_changes.sh --cached`
- 未ステージのみ: `bash skills/diff-doc-sync/scripts/list_changes.sh --working`

## ワークフロー
1. 差分確認
   - コマンドで変更ファイル一覧を取得。大きい変更は領域ごとに整理。
2. マッピング
   - 下表と DOCUMENT_MANAGEMENT.md を参照し、更新対象ドキュメントを決定。
3. 反映
   - docsは箇条書きまたは `- [ ]` で短く追記。AGENTS.md/CLAUDE.mdは既存ルールに従う。
   - UI変更は docs/ui/*.html に構造/振る舞い差分をメモ。
4. 検証
   - 変更ドキュメントを読み直し矛盾がないか確認。
   - 必要なら TODOやテスト項目を追加。

## マッピング例（本プロジェクト）
| 変更 | 更新候補 |
| --- | --- |
| `demo_app/` 配下のAPI/サービス | docs/fastapi-htmx-spec.md, docs/TODOS.md |
| テンプレート/静的ファイル | docs/ui/*.html, docs/TODOS.md |
| 設定/依存 (`app_config.json`, `.env`, `requirements.txt`) | READMEまたは設定説明を置くdocs節、docs/TODOS.md |
| Azure関連 | CLAUDE.md（既存モジュール方針）、関連仕様md |
| 新規機能 | docs/<機能名>.md 追加検討＋docs/TODOS.md |

## 記述の型
- 新規仕様: 箇条書きで入出力/制約/エラーハンドリングを1行ずつ。
- TODO追加: `- [ ]` 命令形。完了は `[x]`。
- 差分メモ: 「変更理由」「主要な振る舞い」「依存ENV」の3点を短文で。

## scripts/
- `scripts/list_changes.sh`: git差分を取得し一覧化。`--cached`（ステージのみ）、`--working`（未ステージのみ）、`--base <rev>` で比較対象変更可。

## references/
- なし。必要なら追加。
