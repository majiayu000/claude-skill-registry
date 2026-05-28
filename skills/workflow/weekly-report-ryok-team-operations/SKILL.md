---
name: weekly-report
description: "MLシステム開発共同研究プロジェクトの週報を自動作成するスキル。先週の週報をベースにNotionから今週の更新情報を収集し、差分を反映して新しい週報をNotionに発行する。Use when: (1) 週報を作成したい、(2) weekly reportを作りたい、(3) 週次報告を作成したい、(4) create weekly report"
---

# Weekly Report Creation

MLシステム開発共同研究プロジェクトの週報を自動作成する。

## Workflow

```
1. 先週版の取得 → 2. 今週の情報収集 → 3. 内容の更新 → 4. Notion発行 → 5. 検証
```

### Step 1: Baseline Retrieval（先週版の取得）

タイトルパターン `【週次報告】<monday-of-week>週 共同研究 MLシステム開発` に合致する直近の先週版を検索。

```
Notion検索 → 本文（Markdown）と MailBody を取得 → 今週版のベースとして使用
```

先週版が存在しない場合のみ、テンプレートから新規作成。

### Step 2: Information Collection（今週の素材収集）

指定週範囲で以下を検索：
- **Engineering Meeting Management** DB
- **AI Coding** project-task DB
- 追加ページ：
  - https://www.notion.so/AI-PJ-Task-14d4bc176b2b804696e5e9ecb171db55?pvs=9
  - https://www.notion.so/2424bc176b2b80f4a3a9c33c7b6d481f?v=2424bc176b2b80aa94d8000ce20fc39f

### Step 3: Content Updating（内容の更新）

先週版をベースに今週の収集結果を照合して更新：

| 変化の種類 | 対応 |
|-----------|------|
| 新規発生 | 追記 |
| 状況変化 | 本文を直接更新（上書き） |
| 中止/撤回/完了 | 本文から削除 or 「完了」と記載変更 |

**確証が薄い項目には末尾に `<確認してください>` を付与**（情報ソースが曖昧／未確定な予定／相互矛盾など）

**出典タグを付ける**: `[src: MeetingNote <yyyy-mm-dd>]`, `[src: AI Coding DB#<task-id>]` 等

### Step 4: Report Publication（Notion発行）

**Page name**: `【週次報告】<monday-of-week>週 共同研究 MLシステム開発`
- `<monday-of-week>` はその週の月曜日（例: `2025-06-30`）

**Database**: Engineering Meeting Management (`12d4bc17-6b2b-80be-907d-e7a2f457658e`)

**Properties**:
| Property | Value |
|----------|-------|
| `date` | `<week-ending-date>` |
| `type` | `週報` |
| `email recipient` | `松尾先生` |
| `MailBody` | 更新済み本文 |

### Step 5: Final Recording（最終確認）

- 新規ページの存在、プロパティ、本文/`MailBody` の整合を検証
- 更新件数（新規 / 更新 / 完了）と `<確認してください>` 件数をログに記録

## Template

週報のテンプレートと記載ルールは [template.md](template.md) を参照。

先週版が存在しない場合のみ、このテンプレートから新規作成する。

## Arguments

| Parameter | Type | Description |
|-----------|------|-------------|
| `week-date` | string | Week ending date in `YYYY-MM-DD` format. If omitted, uses current week. |
