---
name: feature-pilot
description: |
  プロジェクト プロジェクトのAI主導機能開発を統合するオーケストレーター。
  すべての開発要求の単一進入点として、作業タイプを自動判別し、適切な下位スキルを調整する。
  **Readiness Gate 機能が内蔵されており、Go/No-Go 検証を直接実行する。**

  「新機能追加」「バグ修正」「機能修正」「開発要求」「実装して」等の要求でトリガーされる。

  <example>
  user: "ユーザーが提出したコードを分析する機能が必要"
  assistant: "feature-pilotを使用して作業タイプを判別し、パイプラインを開始します"
  </example>

  <example>
  user: "Diff表示画面でシンタックスハイライトが動かないバグを修正して"
  assistant: "feature-pilotを使用してバグ修正ワークフローを開始します"
  </example>
doc_contract:
  review_interval_days: 30
---

# Feature Pilot (AI主導機能開発オーケストレーター)

> **核心コンセプト**: 「単一進入点、自動調整、内蔵検証」 (One Entry, Auto Orchestration, Built-in Validation)

AI主導開発環境ですべての開発要求を受け付け、適切なワークフローを自動調整する統合オーケストレーター。

---

## EXECUTION PROTOCOL (MANDATORY) - v9.0

> **CRITICAL**: このセクションは**スキップできません**。
> feature-pilot 実行時は以下のプロトコルを**必ず**遵守してください。
> 違反時は**即座に中断**し、最初から再開する必要があります。

### Pre-flight Checklist (スキル開始前の必須出力)

> **⚡ CHECKLIST UPDATE RULE (MANDATORY)**:
> 各チェック項目の確認完了時に、チェックリスト全体を再出力し、該当項目の状態を更新すること。
> `---` → `✅` (通過) または `❌` (失敗)。全項目確認まで毎回最新状態を反映。
> **未更新のまま次段階に進行 = Violation Protocol 違反 (severity: HIGH)**

```markdown
## Pre-flight Checklist (feature-pilot)

|   ID   | 項目                                        | 状態 |
| :----: | ------------------------------------------- | :--: |
| PF-001 | 作業タイプ判別完了                          | ---  |
| PF-002 | CONTEXT.json アクセス可能または新規作成可能 | ---  |
| PF-003 | CLAUDE.md ルール確認                        | ---  |
| PF-004 | Tier 判定完了                               | ---  |
| PF-005 | Evidence キャッシュ確認                     | ---  |
| PF-006 | 下位スキル ESP 互換性確認                   | ---  |
| PF-007 | 作業 ID 確定                                | ---  |

**作業タイプ**: [NEW_FEATURE | MODIFY_FEATURE | BUG_FIX | DOCS_ONLY]
**Tier 判定**: [1 | 2 | 3]
**パイプライン**: [該当パイプライン一覧]

---

→ 各項目確認後に本テーブルを再出力 (状態列を ✅/❌ に更新)
→ 全項目 ✅: 実行進行 / 1つでも ❌: 即時中断 + 理由報告
```

### Model Routing Policy (必須遵守)

| 作業                          | モデル | コスト |
| ----------------------------- | :----: | :----: |
| 作業タイプ分類                | Haiku  |   $    |
| コンテキスト収集 (turbo-mode) | Haiku  |   $    |
| Readiness Gate 検証           | Sonnet |   $$   |
| 実装 (feature-implementer)    | Sonnet |   $$   |
| アーキテクチャ決定            |  Opus  |  $$$   |

**下位スキル ESP 継承ルール**:

- ESP v2.0+ スキル呼出時 → 当該スキルの Pre/Post-flight 出力確認必須
- ESP 未適用スキル呼出時 → feature-pilot が代行検証
- **フォールバックチェーン**: Haiku → Sonnet → Opus (失敗時自動昇格)

### Evidence Caching Policy

| 検証タイプ     | 有効時間 | 無効化条件                                      |
| -------------- | :------: | ----------------------------------------------- |
| npm run lint   |   30分   | `src/**/*.{ts,tsx}` 変更                        |
| npm test       |   30分   | `tests/**/*.{ts,tsx}`, `src/**/*.{ts,tsx}` 変更 |
| Readiness Gate |   60分   | SPEC-_.md, screens/_.md 変更                    |
| Security Scan  |   60分   | `.env*` 変更                                    |

**キャッシュ活用**:

- 有効時間内の同一検証 → 再実行省略、キャッシュ結果使用
- 無効化条件充足 → 強制再実行
- `--force` フラグ → キャッシュ無視、強制再実行

### Post-flight Checklist (スキル終了前の必須出力)

> **⚡ CHECKLIST UPDATE RULE (MANDATORY)**:
> 各チェック項目の確認完了時に、チェックリスト全体を再出力し、該当項目の状態を更新すること。
> `---` → `✅` (通過) または `❌` (失敗)。全項目確認まで毎回最新状態を反映。
> **未更新のまま次段階に進行 = Violation Protocol 違反 (severity: HIGH)**

```markdown
## Post-flight Checklist (feature-pilot)

|   ID    | 項目                                                | 状態 |
| :-----: | --------------------------------------------------- | :--: |
| POF-001 | パイプライン完了または明示的中断                    | ---  |
| POF-002 | CONTEXT.json 最終状態更新                           | ---  |
| POF-003 | QA 検証通過 (pre-quality-gate)                      | ---  |
| POF-004 | 下位スキル Post-flight すべて完了                   | ---  |
| POF-005 | Evidence キャッシュ完了                             | ---  |
| POF-006 | DoD 検証完了 (completion_contract verdict = passed) | ---  |

**最終状態**: [Done | Blocked | AwaitingUser | Failed]
**Evidence キャッシュ**:

- npm_lint: [CACHED until HH:MM | NOT_CACHED]
- npm_test: [CACHED until HH:MM | NOT_CACHED]
- readiness_gate: [CACHED until HH:MM | NOT_CACHED]

---

→ 各項目確認後に本テーブルを再出力 (状態列を ✅/❌ に更新)
→ 全項目 ✅: 完了報告 / 1つでも ❌: 修正後再検証
```

### Violation Protocol

| 違反タイプ                                       |  重大度  | 処理                                         |
| ------------------------------------------------ | :------: | -------------------------------------------- |
| Pre-flight 未出力                                | CRITICAL | 即座に中断、最初から再開                     |
| Post-flight 未検証                               |   HIGH   | 完了報告前に検証実行                         |
| Model パラメータ欠落 (Task 呼出)                 |   HIGH   | 当該 Task 再呼出                             |
| 下位スキル ESP 違反                              |   HIGH   | 当該スキル再実行                             |
| 検証なしの完了主張                               | CRITICAL | 即座に中断、検証実行                         |
| Evidence キャッシュ無視 (不要な再実行)           |   LOW    | 警告後続行                                   |
| チェックリスト状態未更新 (---/[ ]/⬜ のまま進行) |   HIGH   | 即座にチェックリスト再出力、状態更新後に進行 |

---

## 核心原則

1. **Single Entry Point**: ユーザーはどのスキルを使うか知る必要がない
2. **Auto Classification**: 要求を分析して作業タイプを自動判別
3. **Pipeline Orchestration**: 適切な下位スキルを順次/並列呼出
4. **Built-in Validation**: Readiness Gate が内蔵されており別途スキル呼出不要
5. **Context Continuity**: 全パイプラインでコンテキスト維持
6. **Context Preservation via CONTEXT.json**: 統合コンテキストファイルによる状態追跡でコンテキスト喪失防止

---

## 作業タイプ (Work Types)

| タイプ             | トリガー信号                   | パイプライン                                                                                |
| ------------------ | ------------------------------ | ------------------------------------------------------------------------------------------- |
| **NEW_FEATURE**    | "新機能", "追加", SPEC 未存在  | architect → spec → ui-approval → **gate** → impl → wiring → qa → status-sync → quality-gate |
| **MODIFY_FEATURE** | "修正", "変更", 既存 SPEC あり | spec-update → ui-approval → **gate** → impl → wiring → status-sync → quality-gate           |
| **BUG_FIX**        | "バグ", "エラー", "修正"       | analyze → impl → test                                                                       |
| **DOCS_ONLY**      | "文書のみ", "SPECのみ"         | 該当スキルのみ呼出                                                                          |

---

## CONTEXT.json 管理プロトコル (Context Preservation)

> **核心目的**: 「コンテキスト喪失防止」 - セッション中断/再開、スキル切替時にも作業状態を完全保存

### 概要

CONTEXT.json は機能開発の全ライフサイクルの状態を追跡する**統合コンテキストファイル**です。

| 項目             | 内容                                    |
| ---------------- | --------------------------------------- |
| **場所**         | `docs/features/<id>/CONTEXT.json`       |
| **スキーマ**     | `docs/_templates/context_schema.json`   |
| **テンプレート** | `docs/_templates/context_template.json` |
| **Git 追跡**     | はい (状態履歴保存)                     |

### 核心セクション

| セクション       | 目的               | 活用時点                     |
| ---------------- | ------------------ | ---------------------------- |
| **quick_resume** | 3秒以内に状況把握  | セッション再開時に最初に読む |
| **progress**     | FR 基準の進捗率    | 実装段階で継続更新           |
| **references**   | 参照文書の優先順位 | 現在の作業に応じて動的変更   |
| **decisions**    | 決定履歴           | コンテキスト復元時に参照     |
| **history**      | 状態遷移履歴       | デバッグおよび監査追跡       |

### 状態マシン (State Machine)

```
                          +----------+
                          |   Idle   |
                          +----+-----+
                               | start
                               v
                          +----------+
              +---------->| Briefing |
              |           +----+-----+
              |                | brief_done
              |                v
              |         +--------------+
              |         | SpecDrafting |<--------------+
              |         +------+-------+               |
              |                | spec_done             |
              |                v                       |
              |         +--------------+         +-----+-------+
              |         | UiApproval   |         | SpecUpdating |
              |         +------+-------+         +-----+-------+
              |                | ui_approved           |
              |                v                       | update_done
              |         +--------------+               |
              |         | Implementing |<--------------+
              |         +------+-------+
              |                | impl_done
              |                v
              |         +--------------+
              |         | SyncingStatus|
              |         +------+-------+
              |                | sync_done
              |                v
              |         +-----------+
              |         | Reviewing |
              |         +-----+-----+
              |               | review_pass
              |               v
              |         +----------+
              |         |   Done   |
              |         +----------+
              |
              |  +-----------+
              +--| BugFixing | (from any state)
                 +-----------+

---------- 例外状態 ----------

+-----------------+     +--------------+     +----------+     +----------+
| AwaitingUser    |     |   Blocked    |     |  Failed  |     | Archived |
| (7問上限到達    |     | (質問未解決) |     |(復旧不可)|     |(終了)    |
|  ユーザー待機)  |     |              |     |          |     |          |
+-----------------+     +--------------+     +----------+     +----------+
       ^                      ^
       |                      |
       +----------------------+--- (from any state)
```

### 状態説明

| 状態             | トリガー条件                                                      | 脱出条件                  |
| ---------------- | ----------------------------------------------------------------- | ------------------------- |
| **AwaitingUser** | 7問質問上限到達、Tier 1 セキュリティ作業                          | ユーザー応答受信          |
| **Failed**       | 復旧不可エラー、3回連続 No-Go                                     | 手動介入必要              |
| **Archived**     | ユーザー明示要求 (merged/superseded/deferred/abandoned/duplicate) | 復元不可 (新規作成で対応) |

### 状態遷移ルール

| 現在状態       | トリガー                    | 次状態           | 条件                        |
| -------------- | --------------------------- | ---------------- | --------------------------- |
| Idle           | 作業開始                    | Briefing         | -                           |
| Briefing       | CONTEXT.json 完了           | SpecDrafting     | CONTEXT.json 存在           |
| SpecDrafting   | SPEC.md 完了                | **UiApproval**   | SPEC.md, screens/\*.md 存在 |
| **UiApproval** | UI 承認                     | Implementing     | Readiness Gate Go           |
| **UiApproval** | UI 却下                     | Blocked          | 却下理由記録                |
| SpecUpdating   | SPEC 修正完了               | **UiApproval**   | SPEC 修正完了               |
| Implementing   | 実装完了                    | SyncingStatus    | テスト通過                  |
| BugFixing      | バグ修正完了                | SyncingStatus    | 回帰テスト通過              |
| SyncingStatus  | 同期完了                    | Reviewing        | index.md 更新               |
| Reviewing      | DoD 検証通過                | Done             | DoD verdict = passed        |
| _Any_          | 未解決質問発生              | Blocked          | open_questions に追加       |
| Blocked        | 質問解決                    | previous_state   | 質問 resolved               |
| _Any_          | **7問上限到達**             | **AwaitingUser** | question_count >= 7         |
| _Any_          | **Tier 1 セキュリティ作業** | **AwaitingUser** | 認証/権限/PII/決済関連      |
| AwaitingUser   | ユーザー応答受信            | previous_state   | -                           |
| _Any_          | **3回連続 No-Go**           | **Failed**       | 連続失敗カウント >= 3       |
| _Any_          | **復旧不可エラー**          | **Failed**       | 致命的エラー発生            |
| Failed         | 手動介入                    | Idle             | 管理者リセット              |
| Done           | アーカイブ要求              | **Archived**     | ユーザー明示要求            |
| Blocked        | アーカイブ要求              | **Archived**     | ユーザー明示要求            |
| Failed         | アーカイブ要求              | **Archived**     | ユーザー明示要求            |

### CONTEXT.json ライフサイクル

#### 1. 作業開始時 (Load or Create)

```markdown
## CONTEXT.json チェック

1. `docs/features/<id>/CONTEXT.json` 存在確認
2. 存在:
   - quick_resume セクションを読み現在状態を即時把握
   - lock.locked 確認 → locked なら警告
   - references.current_focus 確認 → 参照すべき文書を把握
3. 未存在:
   - `docs/_templates/context_template.json` をコピーして新規作成
   - feature_id, title, why, success_criteria を初期化
```

#### 2. ロック取得 (Lock Acquisition)

```json
{
  "execution": {
    "lock": {
      "locked": true,
      "locked_by": "claude-session-20260211-1430",
      "locked_at": "2026-02-11T14:30:00+09:00",
      "lock_expires_at": "2026-02-11T15:00:00+09:00"
    }
  }
}
```

**ロックルール**:

- 作業開始時にロック取得 (`lock_expires_at` = `locked_at` + 30分)
- lock があるが `lock_expires_at` < 現在時刻 → **stale lock と見なし**、強制解除後に新 lock 取得
- 作業完了/中断時に明示的解除

#### 3. 状態遷移 (State Transition)

各状態変更時に `history` に記録:

```json
{
  "history": [
    {
      "at": "2026-02-11T14:35:00+09:00",
      "from_state": "Briefing",
      "to_state": "SpecDrafting",
      "triggered_by": "feature-spec-generator",
      "note": "SPEC-029.md 作成完了"
    }
  ]
}
```

#### 4. 決定記録 (Decision Logging)

重要な決定発生時に `decisions` に追加:

```json
{
  "decisions": [
    {
      "at": "2026-02-11T15:00:00+09:00",
      "summary": "状態管理にReact Hooksを選択（Zustandの代わり）",
      "rationale": "プロジェクト規模に対して適切な軽量性 + 既存パターンとの一貫性"
    }
  ]
}
```

#### 5. 未解決質問 (Open Questions)

Blocked 状態遷移条件:

```json
{
  "open_questions": [
    {
      "id": "Q1",
      "question": "コード分析結果のキャッシュ期間は?",
      "status": "open",
      "impact": "API設計 + ストレージ設計",
      "resolution": null
    }
  ]
}
```

#### 6. 作業完了時 (Completion)

> **⚡ CHECKLIST UPDATE RULE (MANDATORY)**:
> 各項目の確認完了時に、チェックリスト全体を再出力し `[ ]` を `[x]` に更新すること。
> 全項目 `[x]` 確認後に次段階へ進行。未更新のまま進行 = Violation Protocol 違反 (severity: HIGH)

```markdown
## 完了チェックリスト

- [ ] current_state → Done
- [ ] lock.locked → false
- [ ] touched_files リスト最終確認
- [ ] history に完了記録追加
```

### 下位スキルからの CONTEXT.json 直接更新

各下位スキルは作業完了時に **CONTEXT.json を直接更新** します:

```
// 各スキルが直接 CONTEXT.json 読取 → 修正 → 保存
Read docs/features/<id>/CONTEXT.json
Edit:
  - quick_resume.current_state → 新状態
  - quick_resume.current_task → 次の作業
  - quick_resume.next_actions → 次のアクション
  - quick_resume.last_updated_at → 現在時刻
  - progress.details.FR-XXXNN → 進行状態更新
  - history[] → 状態遷移記録追加
```

**例: feature-spec-generator 完了時**

```json
{
  "quick_resume": {
    "current_state": "SpecDrafting",
    "current_task": "Readiness Gate 検証待ち",
    "next_actions": ["Readiness Gate 実行", "Go 判定時に実装開始"],
    "last_updated_at": "2026-02-11T14:35:00+09:00"
  },
  "progress": {
    "percentage": 10,
    "fr_total": 5,
    "fr_completed": 0,
    "fr_in_progress": 0
  },
  "history": [
    {
      "at": "2026-02-11T14:35:00+09:00",
      "from_state": "Briefing",
      "to_state": "SpecDrafting",
      "triggered_by": "feature-spec-generator",
      "note": "SPEC-029.md 作成完了"
    }
  ]
}
```

**例: Discovery Gate (Phase 0) 完了後の architecture 更新**

```json
{
  "architecture": {
    "domain_model": {
      "path": "docs/features/029-vocabulary-book/DOMAIN-MODEL.md",
      "bounded_contexts": ["VocabularyManagement"],
      "ubiquitous_language_count": 12,
      "generated_at": "2026-02-11T10:00:00+09:00"
    },
    "adr": null,
    "system_design": null,
    "discovery_gate": {
      "verdict": "Go",
      "verified_at": "2026-02-11T10:30:00+09:00",
      "blocking_count": 0,
      "warning_count": 0
    },
    "tier_applied": "M"
  }
}
```

> **スキーマ契約**: architecture は feature-architect が null 初期化し、Discovery Gate 通過後に feature-pilot が実際の成果物パスで更新。Tier S (Phase 0 スキップ) の場合は全体 null を維持。

**例: Archived への遷移時**

```json
{
  "quick_resume": {
    "current_state": "Archived",
    "current_task": "",
    "next_actions": [],
    "last_updated_at": "2026-02-11T16:00:00+09:00"
  },
  "archived_reason": "superseded",
  "archived_ref": "046-vocabulary-book-v2"
}
```

> **スキーマ契約**: `archived_reason` は enum ["merged", "superseded", "deferred", "abandoned", "duplicate"]。`archived_ref` は `archived_reason` が "merged" または "superseded" の場合のみ必須。

**利点**: ブロックパース不要、各スキルが自律的に状態管理

### Blocked 状態復旧プロトコル

```markdown
## Blocked 状態からの復旧

1. `open_questions` 中 status="open" 項目確認
2. ユーザーに質問一覧を提示
3. 回答受信後:
   - status → "resolved"
   - resolution フィールドに回答記録
4. すべての質問が resolved の場合:
   - current_state → previous_state
   - previous_state → null
```

### Reviewing 段階 (DoD 検証 + 品質検証)

> **SSOT 原則**:
>
> - 品質検証ルール → `Makefile`
> - 完了条件定義 → `BRIEF §7`
> - 完了条件追跡 → `CONTEXT.json completion_contract`
> - 共通 Base DoD → `.claude/pipelines/*.yaml base_dod`

**実行手順**:

1. **completion_contract 初期化** (未初期化の場合):
   - `completion_contract.work_type` → Phase 0 で判別した作業タイプ ("NEW_FEATURE" | "MODIFY_FEATURE" | "BUG_FIX")
   - パイプライン YAML の `base_dod` から work_type 対応の Base DoD をロード
   - BRIEF §7 を読取、Feature-Specific 項目 (§7.1) を追加
   - CONTEXT.json に `completion_contract` セクションを書込
   - フォールバック: §7 未存在 → success_criteria → Base DoD のみ

2. **Machine-Verifiable 項目の自動検証**:

   ```bash
   Bash: make q.check
   ```

   - 既存 Evidence Cache 活用（30分 TTL）
   - 各項目の status を passed/failed に更新
   - evidence にコマンド結果を記録

3. **AI-Verifiable 項目の検証**:
   - SPEC §0 vs 実装コードの準拠チェック
   - JSDoc コメント存在チェック (export 関数)
   - evidence に検証根拠を記録

4. **Human-Verifiable 項目の確認** (存在する場合):
   - ユーザーに確認依頼 → AwaitingUser 遷移

5. **verdict 判定**:
   - 全 passed → verdict = "passed" → Done 遷移
   - machine/ai failed あり → verdict = "failed" → implement へ revert
   - human pending のみ → verdict = "partial" → AwaitingUser

6. **summary 再計算 + CONTEXT.json 更新**:
   - `completion_contract.summary` の total/passed/failed/skipped/pass_rate を再計算
   - `completion_contract.last_verified_at` を現在時刻に更新
   - `current_state` → Done (verdict = passed の場合)
   - `history` に完了記録追加

---

## 効率性・品質スキル

> **核心コンセプト**: 検証済みパターンを Next.js / TypeScript に特化

### 統合スキル一覧

| スキル               | 役割                                     | 活性化条件                 | 連携段階               |
| -------------------- | ---------------------------------------- | -------------------------- | ---------------------- |
| **turbo-mode**       | 並列実行 + 3-Tier モデルルーティング     | コンテキスト収集、並列実装 | Phase 1, Step 4        |
| **persistent-mode**  | 検証完了まで自動継続                     | Tier 1 作業、明示的要求    | 全パイプライン         |
| **pre-quality-gate** | lint + test + アーキテクチャ検査サイクル | 実装完了後                 | Step 4.6 → Step 5 の間 |

### turbo-mode v2.0 (実際の並列実行エンジン) - CRITICAL

> **v2.0 更新**: ガイドライン → 実際の実行エンジンに強化

**自動活性化時点**:

- **Phase 1**: コンテキスト収集 (並列読取) - NEW_FEATURE, MODIFY_FEATURE
- **Step 4**: 実装段階 (独立ファイル並列作成)

#### turbo-mode 呼出プロトコル (MUST FOLLOW)

**Phase 1 コンテキスト収集時**:

```markdown
## Turbo Mode 活性化 (Phase 1)

### 作業一覧

| ID  | 作業                                 | タイプ | ティア |
| --- | ------------------------------------ | ------ | ------ |
| T1  | 既存 Custom Hook パターン検索        | Read   | Haiku  |
| T2  | 関連 API Route 確認                  | Read   | Haiku  |
| T3  | 類似機能テストパターン調査           | Read   | Haiku  |
| T4  | 再利用候補探索 (類似 Component/Hook) | Read   | Haiku  |

### 依存性分析

T1, T2, T3, T4: すべて Read → 独立 → 並列可能

### バッチ構成

バッチ 1 (並列): T1, T2, T3, T4

### 実行

→ 4つの Task を **単一応答で同時呼出**
```

**実際の並列呼出例**:

feature-pilot は Phase 1 で以下のように **一つの応答で複数 Task を同時呼出** します:

```
Task 1: subagent_type="Explore", model="haiku", prompt="src/features/ で Custom Hook パターン検索"
Task 2: subagent_type="Explore", model="haiku", prompt="src/app/api/ で関連 API Route 確認"
Task 3: subagent_type="Explore", model="haiku", prompt="tests/ で類似テストパターン調査"
Task 4: subagent_type="Explore", model="haiku", prompt="src/features/ + src/shared/ で再利用可能な類似 Component/Hook 探索"

→ 4つの結果同時返却 (待機時間 1/4)
```

**Step 4 実装段階時**:

```markdown
## Turbo Mode 活性化 (Step 4)

### 依存性分析 (レイヤー基準)

- TypeScript Type + Zod Schema, API Layer: 独立 → 並列可能
- Custom Hook: Type 必要 → Type 後に実行
- Component: Hook 必要 → Hook 後に実行

### バッチ構成

バッチ 1 (並列): TypeScript Type + Zod Schema, API Layer
バッチ 2 (順次): Custom Hook
バッチ 3 (順次): Component
バッチ 4 (順次): Test (API Test, Hook Test, Component Test)

### 実行

→ バッチ 1: 2つの Sonnet Task 同時呼出
→ バッチ 2-4: 順次実行
```

**3-Tier モデルルーティング**:
| 複雑度 | モデル | 例 |
|--------|--------|-----|
| 簡単 | Haiku | ファイル位置検索、package.json 確認、パターン検索 |
| 標準 | Sonnet | Component/Hook 実装、テスト作成 |
| 複雑 | Opus | アーキテクチャ分析、セキュリティレビュー、バグ根本原因 |

### persistent-mode (完了まで自動継続)

**活性化条件**:

```python
if tier == 1 and work_type in ["NEW_FEATURE", "MODIFY_FEATURE"]:
    activate_persistent_mode()

if "最後まで" in user_request or "止めないで" in user_request:
    activate_persistent_mode()
```

**検証チェックリスト (すべて通過で終了)**:

> **⚡ CHECKLIST UPDATE RULE (MANDATORY)**:
> 各チェック項目の確認完了時に、チェックリスト全体を再出力し、該当項目の状態を更新すること。
> `[ ]` → `[x]` (通過) または `[FAIL]` (失敗)。全項目確認まで毎回最新状態を反映。
> **未更新のまま次段階に進行 = Violation Protocol 違反 (severity: HIGH)**

- [ ] `npm run lint` → エラー 0件
- [ ] `npm test` → すべてのテスト通過
- [ ] TaskList → pending 0件
- [ ] CONTEXT.json → current_state = Done

### pre-quality-gate (QA サイクル)

**実行時点**: Step 4.5 (feature-wiring) 完了後

**サイクルフロー**:

```
Skill ツール:
- skill: "pre-quality-gate"

→ make q.check 実行 (lint + test + architecture check)
→ 失敗時は修正 → 再実行 (最大 5回)
→ 同一エラー 3回 → 停止
```

---

## プロトコル (Protocol)

### Phase 0: 要求受付と分類 (Request Classification)

1. **要求分析**:
   - キーワード抽出 (新機能、修正、バグ、リサーチ等)
   - 機能 ID 言及有無確認
   - 具体的なファイル/画面言及有無確認

2. **既存文書確認**:

   ```bash
   # 言及された機能 ID の文書存在確認
   ls docs/features/<mentioned-id>/ 2>/dev/null
   ```

3. **作業タイプ判別**:
   ```
   IF バグ/エラー/動かない 言及 → BUG_FIX
   ELSE IF SPEC なし AND 新機能要求 → NEW_FEATURE
   ELSE IF SPEC あり AND 変更要求 → MODIFY_FEATURE
   ELSE → ユーザーに明確化質問
   ```

### Phase 1: 計画提示 (Plan Presentation)

判別された作業タイプに応じて実行計画を提示:

> **⚡ PIPELINE PROGRESS UPDATE RULE (MANDATORY)**:
> 各ステップ完了時に、本テーブルを再出力し状態列を `✅`/`❌`/`⏭️` に更新すること。
> `---` のまま次ステップに進行 = Violation Protocol 違反 (severity: HIGH)

```markdown
## 作業分類完了

**要求**: [ユーザー要求要約]
**作業タイプ**: NEW_FEATURE
**関連機能**: なし (新規)

### 実行計画

| Step | 状態 | スキル/アクション         | 説明                                                    |
| :--: | :--: | ------------------------- | ------------------------------------------------------- |
|  0   | ---  | `/research-pilot`         | Product Discovery (条件付: リサーチ/妥当性キーワード時) |
|  1   | ---  | `/feature-architect`      | CONTEXT.json 作成                                       |
|  2   | ---  | `/feature-spec-generator` | SPEC.md + Screen 作成                                   |
|  3   | ---  | **Readiness Gate**        | Go/No-Go 検証 (内蔵)                                    |
|  4   | ---  | 実装進行                  | SPEC 基準                                               |
|  5   | ---  | テスト + 品質検証         | lint + test + architecture check                        |

→ 各ステップ完了時に本テーブルを再出力し状態列を ✅/❌/⏭️ に更新
→ 全ステップ ✅/⏭️: 完了 / 1つでも ❌: 中断 + 理由報告

進行しますか?
```

### Phase 2: パイプライン実行 (Pipeline Execution)

各作業タイプ別パイプライン:

#### NEW_FEATURE パイプライン

**重要**: 新機能は必ず **architect (CONTEXT 作成)** → SPEC → Gate → 実装の順序に従います。
**Option B 原則**: feature-architect が CONTEXT.json を作成して初めて feature-spec-generator が実行可能です。

```
Phase -1: research-pilot (条件付実行)
        +------------------------------------+
        | 条件: 以下のいずれかに該当する場合     |
        |  - ユーザーが「リサーチ」「妥当性」   |
        |    「調査」「ゼロベース」と言及       |
        |  - ユーザーが /research-pilot 明示呼出|
        |  - Tier XL 判定時に実行提案          |
        |                                    |
        | Skill ツール使用:                    |
        | - skill: "research-pilot"          |
        | - args: "<機能説明>"               |
        |                                    |
        | BUILD 決定時:                       |
        |   → RESEARCH.md 作成               |
        |   → CONTEXT.json research 準備     |
        |   → Phase 0.5 へ進行               |
        |                                    |
        | SKIP/DEFER 決定時:                  |
        |   → RESEARCH.md 記録後パイプライン終了|
        |                                    |
        | キャッシュ: 既存 RESEARCH.md 30日以内 |
        |   → 再実行省略、キャッシュ使用       |
        +------------------------------------+
        v BUILD → Phase 0.5 / SKIP/DEFER → 終了

Phase 0.5: Turbo Mode コンテキスト収集 (自動活性化)
        +------------------------------------+
        | turbo-mode v2.0 自動活性化          |
        |                                    |
        | 作業一覧作成 → 依存性分析 → バッチ構成|
        |                                    |
        | 並列実行 (単一応答で複数 Task):       |
        | - Task 1: 既存パターン検索 [Haiku]   |
        | - Task 2: 関連 API 確認 [Haiku]     |
        | - Task 3: テストパターン調査 [Haiku]  |
        | - Task 4: 再利用候補探索 [Haiku]     |
        |                                    |
        | 予想時間短縮: 60-70%                 |
        +------------------------------------+
        v コンテキスト収集完了 (並列結果マージ)

Step 1: Skill ツールで feature-architect 呼出 - 必須ゲート
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "feature-architect"       |
        | - args: (なし) または "--quick" (Tier 3)|
        |                                    |
        | CONTEXT.json 作成の唯一の責任者     |
        | この段階はスキップ不可               |
        +------------------------------------+
        v CONTEXT.json 作成 (必須)

Step 2: Skill ツールで feature-spec-generator 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "feature-spec-generator"  |
        | - args: "<機能ID>"                 |
        |                                    |
        | 前提条件: CONTEXT.json 必須         |
        | (Step 1 で architect が作成)        |
        +------------------------------------+
        v SPEC.md, screens/*.md 作成

Step 2.5: Skill ツールで ui-approval-gate 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "ui-approval-gate"        |
        | - args: "<機能ID>"                 |
        |                                    |
        | ユーザー承認必須ゲート               |
        | ワイヤーフレーム作成 + レビュー + 承認 |
        | 承認なしでは次段階へ進行不可          |
        +------------------------------------+
        v 承認 → Step 3 / 却下 → Blocked

Step 3: [内蔵] Readiness Gate Protocol 実行
        +------------------------------------+
        | 別途スキル呼出なしで直接検証          |
        | - Phase 1: 上流契約検証              |
        | - Phase 2: 技術契約検証              |
        | - Phase 3: 実装安全性検証            |
        | → 下記「Readiness Gate Protocol」参照|
        +------------------------------------+
        v Go → Step 4 / No-Go → Step 2 へ復帰

Step 4: 実装開始 (Sequential Mode)
        +------------------------------------+
        | turbo-mode v2.0 バッチ並列           |
        | → バッチ 1: Type+Zod+API (並列)     |
        | → バッチ 2: Custom Hook (順次)       |
        | → バッチ 3: Component (順次)         |
        | → バッチ 4: Test (順次)              |
        +------------------------------------+
        v SPEC の FR 順にコード作成 + テスト

Step 4.5: Skill ツールで feature-wiring 呼出 - INTEGRATED
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "feature-wiring"          |
        | - args: "<機能ID>"                 |
        |                                    |
        | データソース連動 + ナビゲーション連結  |
        | 実装完了後に必ず実行                  |
        +------------------------------------+
        v 統合連動完了

Step 4.6: Skill ツールで pre-quality-gate 呼出 (QA サイクル)
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "pre-quality-gate"        |
        |                                    |
        | lint → test → アーキテクチャ検査      |
        | すべての検証通過まで最大 5回繰返し    |
        | 同一エラー 3回 → 停止               |
        | 通過後 Step 5 へ進行                 |
        +------------------------------------+
        v QA サイクル通過

Step 5: Skill ツールで feature-status-sync 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "feature-status-sync"     |
        | - args: "<機能ID>" (省略可)         |
        +------------------------------------+
        v index.md 状態同期

Step 6: Skill ツールで priority-analyzer 呼出 (選択的)
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "priority-analyzer"       |
        | - args: "<機能ID> --apply"         |
        |                                    |
        | 選択的実行条件:                      |
        | - progress 変化 >= 10%              |
        | - または priority.last_updated 14日+|
        +------------------------------------+
        v 優先順位再計算 (CONTEXT.json 更新)

Step 7: Skill ツールで pre-quality-gate 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "pre-quality-gate"        |
        +------------------------------------+
        v 最終品質検証
```

#### MODIFY_FEATURE パイプライン

**重要**: 既存 SPEC がある場合、必ず feature-spec-updater を先に実行する必要があります。SPEC 修正なしに実装を開始してはなりません。

```
Step 1: Skill ツールで feature-spec-updater 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "feature-spec-updater"    |
        | - args: "<機能ID>"                 |
        +------------------------------------+
        v 既存 SPEC ロード、変更範囲分析、diff 出力

Step 2: feature-spec-updater 結果確認
        - SPEC 変更事項レビュー
        - 変更履歴追加確認
        - 連鎖影響文書確認
        v

Step 2.5: Skill ツールで ui-approval-gate 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "ui-approval-gate"        |
        | - args: "<機能ID>"                 |
        |                                    |
        | 変更された UI のユーザー承認必須     |
        | ワイヤーフレーム更新 + レビュー       |
        +------------------------------------+
        v 承認 → Step 3 / 却下 → Blocked

Step 3: [内蔵] Readiness Gate Protocol 実行
        +------------------------------------+
        | 別途スキル呼出なしで直接検証          |
        | → 下記「Readiness Gate Protocol」参照|
        +------------------------------------+
        v Go → Step 4 / No-Go → Step 2.5 へ復帰

Step 4: 実装 + テスト (SPEC の修正された FR 基準)
        v

Step 4.5: Skill ツールで feature-wiring 呼出 (必要時) - INTEGRATED
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "feature-wiring"          |
        | - args: "<機能ID>"                 |
        |                                    |
        | 実行条件:                            |
        | - 新規 Hook/画面追加時               |
        | - データ/エントリポイント変更時       |
        +------------------------------------+
        v 統合連動

Step 5: Skill ツールで feature-status-sync 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "feature-status-sync"     |
        | - args: "<機能ID>"                 |
        +------------------------------------+
        v index.md 状態同期

Step 6: Skill ツールで priority-analyzer 呼出 (選択的)
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "priority-analyzer"       |
        | - args: "<機能ID> --apply"         |
        |                                    |
        | 選択的実行条件:                      |
        | - progress 変化 >= 10%              |
        | - または priority.last_updated 14日+|
        +------------------------------------+
        v 優先順位再計算

Step 7: Skill ツールで pre-quality-gate 呼出 (選択)
        v 品質検証
```

#### BUG_FIX パイプライン

**重要**: バグ修正も体系的なプロセスに従います。症状だけを見て修正するのではなく、根本原因を見つけて解決します。

```
Step 1: Skill ツールで bug-fix 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "bug-fix"                 |
        | - args: "<バグ症状説明>"            |
        +------------------------------------+
        v Phase 1: バグ分析 (症状整理、関連コード探索)
        v Phase 2: 根本原因分析 (仮説樹立、検証)
        v Phase 3: 修正実装 (回帰テスト → コード修正)
        v Phase 4: 検証完了 (全テスト、lint)

Step 2: 修正完了確認
        - 回帰テスト追加確認
        - 全テスト通過確認
        - npm run lint 通過確認
        v

Step 3: (選択) Skill ツールで pre-quality-gate 呼出
        +------------------------------------+
        | Skill ツール使用:                    |
        | - skill: "pre-quality-gate"        |
        +------------------------------------+
        v 最終品質検証 (コミット前)
```

### Phase 3: 進行状況追跡 (Progress Tracking)

各段階完了時に状態更新:

```markdown
## 進行状況

**作業**: 001-code-analysis (NEW_FEATURE)

| 段階           |   状態   | 成果物                    |
| -------------- | :------: | ------------------------- |
| CONTEXT 作成   |   Done   | `CONTEXT.json`            |
| SPEC 作成      |   Done   | `SPEC-001.md`, `screens/` |
| Readiness Gate |   Done   | Go 判定                   |
| 実装           |   Done   | FR-00101~00105 完了       |
| 状態同期       | Progress | index.md 更新中           |
| 品質検証       | Pending  | -                         |

### 現在の作業

feature-status-sync: index.md 状態同期中...
```

---

## Readiness Gate Protocol (内蔵)

> **核心質問**: 「AIがこの文書だけを見て、追加質問なしに安全に実装できるか?」

### 概要

別途の `ai-readiness-gate` スキルを feature-pilot に**統合**しました。

| 統合理由                           | 効果                           |
| ---------------------------------- | ------------------------------ |
| Skill ツール呼出オーバーヘッド除去 | パイプライン効率性向上         |
| コンテキスト切替なし               | 情報損失防止                   |
| スキル数削減                       | 小規模開発環境での認知負荷軽減 |
| 単一スキルで完結                   | 管理の単純化                   |

### 実行時点

- **NEW_FEATURE**: Step 3 (SPEC 作成後)
- **MODIFY_FEATURE**: Step 3 (SPEC 修正後)

### Phase 0: 機械検証 (MANDATORY - 最優先実行)

> **目的**: プレースホルダー、未完成セクションをスクリプトで 100% 遮断

**検証スクリプト実行** (Phase 1-3 の前に必ず実行):

```bash
cd .claude/skills/feature-pilot/scripts
python validate_spec.py <SPEC_PATH>

# 例
python validate_spec.py docs/features/001-code-analysis/SPEC-001-code-analysis.md
```

**Exit Code 解釈**:
| Exit Code | 意味 | 次のアクション |
|:---------:|------|---------------|
| `0` | すべての検証通過 | Phase 1-3 進行 |
| `1` | BLOCKING イシュー | **即座に No-Go**、SPEC 修正必要 |
| `2` | WARNING のみ存在 | Phase 1-3 進行、注意必要 |

**BLOCKING パターン (自動 No-Go)**:

- `{placeholder}` 形式の未完成テキスト
- `TODO:`, `FIXME:`, `XXX:` マーカー
- 空テーブルセル (`| ? |`, `| - |`)
- 未完成 AC (`AC1: {基準}`)
- パスプレースホルダー (`src/features/{feature}/components/{name}.tsx`)
- 番号未割当 (`FR-NNN`, `SCR-NNN`)
- チェックボックス AC 形式 (`- [ ] AC1:`) -- `--strict-bdd` モードで BLOCKING (新規 SPEC 対象)

**必須セクション検査**:

- セクション 0 (AI 実装契約): `## 0. AI 実装契約`
- セクション 0.1 (Target Files): `### 0.1 Target Files`
- セクション 0.2 (State/Hook): `### 0.2 State / Hook`
- セクション 0.3 (Error Handling): `### 0.3 Error Handling`
- セクション 1-3, 5: 概要、機能要件、依存性、変更履歴

### 5 Phase 検証構造

```
+-------------------------------------------------------------+
| Phase 0: 機械検証 (Automated Validation)                      |
| - validate_spec.py スクリプト実行                              |
| - BLOCKING パターン検査 (プレースホルダー、TODO 等)             |
| - 必須セクション存在検査 (セクション 0, 0.1~0.3, 1, 2, 3, 5)   |
| - FR 完全性検査 (AC、テストパス、実装パス)                      |
|     → Exit 1 なら即座に No-Go (Phase 1-3 進行せず)            |
+-------------------------------------------------------------+
| Phase 1: 上流契約検証 (Upstream Contract)                      |
| - CONTEXT <-> SPEC 整合性 (Why, Constraints, Success)         |
| - BRIEF <-> CONTEXT <-> SPEC Why/Scope/Constraints 整合性     |
| - Manifest 有効性                                             |
+-------------------------------------------------------------+
| Phase 1.5: BRIEF <-> SPEC 追跡性検証 (Traceability)           |
| - BRIEF.md 存在 + Section 0 保存確認                          |
| - User Story → FR マッピングカバレッジ検証                     |
| - BDD Scenario → FR マッピングカバレッジ検証                   |
| - マッピングされた FR の SPEC 内の実在確認                     |
+-------------------------------------------------------------+
| Phase 2: 技術契約検証 (Technical Contract)                     |
| - コア 5 完備チェック                                         |
|   - Target Files (予想パス)                                   |
|   - UI Mapping (画面-機能マッピング)                           |
|   - Verification Strategy (テスト方針)                        |
|   - Cross-Feature Dependencies (依存性)                       |
|   - Failure Handling (エラーシナリオ)                          |
| - SPEC 完全性 (必須セクション存在)                             |
+-------------------------------------------------------------+
| Phase 2.5: Product/UX Readiness                               |
| - 適用判定 (UI がある機能のみ、Backend-only 免除)              |
| - Engagement Design (Hook Model: Trigger→Reward→Investment)   |
| - JTBD Full (Functional + Emotional + Social Job)             |
| - Retention Design (AARRR: Activation, Retention Loop)        |
| - Conversion Design (BJ Fogg MAP + Soft Paywall)              |
| - Competitive Benchmark (競合の類似機能ベンチマーク)           |
|     → Blocking: Aha Moment 未定義, Functional Job 未定義,     |
|       Hard Paywall 検出                                       |
+-------------------------------------------------------------+
| Phase 3: 実装安全性検証 (Implementation Safety)                |
| - Tier 自動判定 (チェックリスト基準)                           |
| - 3 Gate (Breaking Change, Security, Testability)              |
| - 追加検証 (マイグレーション、オフライン)                      |
+-------------------------------------------------------------+
```

### 最終判定基準

| 判定               | 条件                                            | 次のアクション     |
| ------------------ | ----------------------------------------------- | ------------------ |
| **No-Go**          | Phase 1-3 (Phase 2.5 含む) で Blocking 項目失敗 | 文書補完後に再検証 |
| **Conditional Go** | Blocking なし、Warning 1件+                     | 注意しつつ実装進行 |
| **Go**             | すべて通過、Warning 0件                         | 実装開始           |

### Readiness Gate 出力形式

```markdown
# Readiness Gate 検証結果

> **検証日**: 2026-02-11 14:30
> **対象**: Feature 001 - コード分析機能
> **Tier**: 2 (外部 API 連携)

---

## 最終判定: Go

---

## Phase 1: 上流契約検証 - Pass

| 項目                                       | 状態 |
| ------------------------------------------ | :--: |
| Why 一致 (BRIEF -> CONTEXT.why -> SPEC)    | Pass |
| Scope 一致 (BRIEF -> SPEC Goals/Non-Goals) | Pass |
| Hard Constraints 遵守 (BRIEF -> SPEC)      | Pass |
| Success Contracts カバレッジ               | Pass |

## Phase 1.5: BRIEF <-> SPEC 追跡性検証 - Pass

| 項目                                             | 状態 |
| ------------------------------------------------ | :--: |
| BRIEF.md 存在                                    | Pass |
| Section 0 (Original Request) 保存                | Pass |
| US カバレッジ (全 US → 最低 1つ FR)              | Pass |
| BDD カバレッジ (全 AC → 最低 1つ FR)             | Pass |
| FR 存在確認 (マッピングされた FR が SPEC に存在) | Pass |

> **CONTEXT.json 更新 (Phase 1.5 完了時)**:
>
> - `traceability.validated_at` → 現在時刻 (ISO 8601)
> - `traceability.user_story_to_fr` → Phase 1.5 で検証された US→FR マッピング
> - `traceability.bdd_to_fr` → Phase 1.5 で検証された BDD→FR マッピング
> - `traceability.unmapped_user_stories` → マッピングされなかった US リスト
> - `traceability.unmapped_bdd_scenarios` → マッピングされなかった BDD リスト

---

## Phase 2: 技術契約検証 - Pass

### コア 5 状態

| 要素                 | 状態 |
| -------------------- | :--: |
| Target Files         | Pass |
| UI Mapping           | Pass |
| Verification & Test  | Pass |
| Cross-Feature Impact | Pass |
| Failure Handling     | Pass |

---

## Phase 2.5: Product/UX Readiness - Pass

| 領域                    | 状態 | 備考                                                                |
| ----------------------- | :--: | ------------------------------------------------------------------- |
| Engagement (Hook Model) | Pass | Aha Moment: "初回コード分析で改善提案を受信"                        |
| JTBD Full               | Pass | Functional: コード品質向上, Emotional: 成長実感, Social: スキル証明 |
| Retention (AARRR)       | Pass | 日次学習ループ設計済み                                              |
| Conversion (BJ Fogg)    | Pass | 無料 3回/日 → Soft Paywall                                          |
| Competitive             | Pass | 他サービス対比 AI 駆動インタラクティブ教育で差別化                  |

---

## Phase 3: 実装安全性検証 - Pass

### 3 Gate 結果

| Gate | 質問             | 結果 |
| :--: | ---------------- | :--: |
|  A   | Breaking Change? | Pass |
|  B   | Security Risk?   | Pass |
|  C   | Testable?        | Pass |

---

## 次のステップ

実装を開始します。SPEC の FR 順に進行します。

> **CONTEXT.json 更新 (Go 判定時)**:
>
> - `artifacts.spec_locked_at` → 現在時刻 (ISO 8601)
> - `artifacts.spec_validation.last_run_at` → 現在時刻
> - `artifacts.spec_validation.verdict` → "Go" | "Conditional Go"
> - `artifacts.spec_validation.blocking_count` → 検出された Blocking 件数
> - `artifacts.spec_validation.warning_count` → 検出された Warning 件数
```

### No-Go 時の処理

```markdown
# Readiness Gate 検証結果

> **最終判定**: No-Go

## 失敗事由

- **Phase 2 - Verification & Test**: FR-00103 に AC 欠落
- **Phase 2.5 - Engagement**: Aha Moment 未定義

## 修正指示

1. SPEC-001.md の FR-00103 に受入条件(AC) 追加必要
2. 予想テストシナリオ明示必要
3. BRIEF に Aha Moment 定義追加 → SPEC に反映

## 次のアクション

→ **Step 2 へ復帰**: feature-spec-generator 再実行して SPEC 補完
```

---

## 下位スキル呼出ルール

> **Option B 原則**: feature-architect は**必須ゲート**です。spec-generator は CONTEXT.json なしでは実行できません。

| スキル                   | 呼出条件                          | Skill ツール args                              | 役割                                       |  必須  |
| ------------------------ | --------------------------------- | ---------------------------------------------- | ------------------------------------------ | :----: |
| `research-pilot`         | **NEW_FEATURE Phase -1** (条件付) | `"<機能説明>"` または `"--tier <S\|M\|L\|XL>"` | **Product Discovery**                      | 条件付 |
| `feature-architect`      | NEW_FEATURE Step 1                | `(なし)` または `"--quick"`                    | **CONTEXT.json 作成 (唯一の責任者)**       |  必須  |
| `feature-spec-generator` | NEW_FEATURE Step 2                | `"<機能ID>"`                                   | CONTEXT 基準 SPEC 作成                     |  必須  |
| `feature-spec-updater`   | **MODIFY_FEATURE Step 1**         | `"<機能ID>"`                                   | **既存 SPEC 修正**                         |  必須  |
| `ui-approval-gate`       | **Step 2.5 (SPEC 作成/修正後)**   | `"<機能ID>"`                                   | **UI ワイヤーフレーム作成 + ユーザー承認** |  必須  |
| `bug-fix`                | **BUG_FIX Step 1**                | `"<バグ症状>"`                                 | **バグ分析および修正**                     |  必須  |
| `feature-wiring`         | **実装完了後 Step 4.5**           | `"<機能ID>"`                                   | **データ連動 + ナビゲーション連結**        |  必須  |
| `feature-status-sync`    | **wiring 完了後**                 | `"<機能ID>"` (省略可)                          | **index.md 状態同期**                      |  必須  |
| `feature-doctor`         | **CONTEXT.json 不整合/破損時**    | (なし)                                         | **状態診断 + 自動復旧**                    |  任意  |
| `priority-analyzer`      | **状態同期後** (選択的)           | `"<機能ID> --apply"`                           | **優先順位再計算**                         |  任意  |
| `pre-quality-gate`       | priority 更新後                   | (なし)                                         | 最終品質検証                               |  任意  |
| `turbo-mode`             | **Phase 1 コンテキスト収集**      | (なし)                                         | **並列実行 + 3-Tier モデルルーティング**   |  任意  |
| `persistent-mode`        | **Tier 1 作業または明示的要求**   | (なし)                                         | **検証完了まで自動継続**                   |  任意  |

**Tier 基準 architect モード自動選択**:

| Tier | architect モード  | 説明                                   |
| :--: | :---------------: | -------------------------------------- |
| 1-2  |     Standard      | 全コンテキスト収集、最大 7件の質問     |
|  3   | Quick (`--quick`) | 最小フィールドのみ収集、最大 2件の質問 |

> **参考**: Readiness Gate は**内蔵**されているため、別途スキル呼出なしで直接実行します。

---

## ユーザーインタラクションパターン

### 最小入力 (推奨)

```
ユーザー: "コード分析機能を追加して"
```

→ feature-pilot がすべてを自動調整

### 詳細入力

```
ユーザー: "001-code-analysis のコード改善提案ロジックを GPT ベースから Gemini に変更して"
```

→ MODIFY_FEATURE に判別、該当 SPEC ロード後に進行

### 中間介入

```
ユーザー: "SPEC まで作って、実装は後で"
```

→ DOCS_ONLY に切替、gate まで実行

---

## 例外処理

| 状況                            | 処理                                              |
| ------------------------------- | ------------------------------------------------- |
| **作業タイプ不明確**            | ユーザーに選択肢提示                              |
| **下位スキル失敗**              | エラー内容表示後にリトライまたは手動介入要求      |
| **CONTEXT.json 不整合/破損**    | `feature-doctor` 実行後にリトライ                 |
| **Readiness Gate No-Go (新規)** | 修正案内後 feature-spec-generator 再呼出          |
| **Readiness Gate No-Go (修正)** | 修正案内後 feature-spec-updater 再呼出            |
| **ユーザー中断要求**            | 現在の進行状況保存後に中断                        |
| **7問上限到達**                 | `AwaitingUser` 遷移、未回答項目は推奨案を自動選択 |
| **Tier 1 セキュリティ作業検知** | 即座に停止、`AwaitingUser` 遷移、ユーザー確認必須 |

---

## 自律性制御ルール (Autonomy Control Rules)

> **核心原則**: AI の過剰自律動作を防止し、重要な決定はユーザー確認を経るように強制

### 7問上限ルール (Question Limit)

セッション内のユーザー質問回数を 7回に制限し、過度な対話なしに進行します。

| 質問カウント | 状態         | 行動                             |
| :----------: | ------------ | -------------------------------- |
|     1-6      | 正常進行     | 質問後に応答待ち                 |
|      7       | 上限到達     | 最後の質問後に**自律停止**       |
|    7 超過    | AwaitingUser | 追加質問不可、デフォルト自動選択 |

**処理プロトコル**:

1. 各質問時に `CONTEXT.json` の `question_count` 増加
2. 7 到達時に `current_state` → `AwaitingUser`、`previous_state` 記録
3. 未回答項目は**推奨案自動選択**または**仮定 (Assumption) として記録**
4. SPEC/CONTEXT に仮定を明示

**通知メッセージ形式**:

```markdown
7問質問上限到達

未回答項目は推奨案で自動選択されました:

- Q4: オフライン動作 → 「ローカル保存後に同期」 (推奨案)
- Q5: エラー表示 → 「トースト通知」 (推奨案)

仮定事項として記録されました。変更が必要な場合は回答してください。
```

### 自動停止条件 (Auto-Stop Conditions)

以下の条件検知時に**即座に作業中断**後、ユーザー確認要求:

#### Tier 1 (High Risk) - 即座に停止

| 検知条件                    | 状態遷移       | 必要措置                 |
| --------------------------- | -------------- | ------------------------ |
| 認証/権限関連コード修正     | `AwaitingUser` | ユーザー承認必須         |
| 決済/課金ロジック           | `AwaitingUser` | ユーザー承認必須         |
| 個人情報(PII) 処理          | `AwaitingUser` | セキュリティレビュー必須 |
| DB スキーママイグレーション | `Blocked`      | Migration Plan 必須      |
| 学習進度データ影響          | `AwaitingUser` | 影響分析後に承認         |

#### Tier 2 (Medium Risk) - 注意して進行

| 検知条件                   | 処理                                           |
| -------------------------- | ---------------------------------------------- |
| 外部 API 連携              | 契約確認後に進行、失敗時フォールバック定義必須 |
| 複数画面にまたがる状態管理 | 既存パターン遵守確認                           |
| API Route 新規/修正        | デプロイ前テスト必須                           |

#### Tier 3 (Low Risk) - 自律進行

| 作業タイプ          | 説明                     |
| ------------------- | ------------------------ |
| 単一画面 UI 変更    | レイアウト、スタイル調整 |
| テキスト/翻訳修正   | messages.ts 編集         |
| スタイル/テーマ調整 | 色、フォント、間隔等     |

### CONTEXT.json autonomy_control 更新

各スキルは作業開始/完了時に `autonomy_control` セクションを更新します:

```json
{
  "autonomy_control": {
    "max_questions_per_session": 7,
    "auto_stop_conditions": [
      "7問質問上限到達",
      "BLOCKING パターン発見",
      "Tier 1 セキュリティ関連作業",
      "DB マイグレーション必要"
    ],
    "current_autonomy_level": "supervised",
    "tier": 2,
    "claude_md_checked": true,
    "claude_md_version": "2026-02-11"
  }
}
```

### 自律性レベル (Autonomy Levels)

| レベル       | 説明             | 適用状況                      |
| ------------ | ---------------- | ----------------------------- |
| `full`       | 完全自律動作     | Tier 3 作業、明確な SPEC 存在 |
| `supervised` | 主要決定時に確認 | デフォルト、大部分の作業      |
| `paused`     | ユーザー入力待ち | AwaitingUser, Blocked 状態    |

### CLAUDE.md 強制参照

Phase 0 で CLAUDE.md 確認を強制します:

```markdown
## CLAUDE.md チェック (Phase 0 必須)

1. CLAUDE.md ファイル読取
2. autonomy_control.claude_md_checked → true
3. autonomy_control.claude_md_version → `git log -1 --format='%ai' -- CLAUDE.md` の出力 (YYYY-MM-DD 形式)
   - git 未使用環境: ファイル冒頭の `# currentDate` 値、または読取時の現在日付
4. 遵守事項 (Rules to Follow) セクション確認
5. 禁止事項 (MUST NOT) 違反時 → 即座に No-Go
```

---

## AI 行動指針

### DO (やるべきこと)

- 要求を受けたらまず作業タイプを分類
- **Skill ツールを使用して下位スキルを呼出** (feature-architect, feature-spec-generator, bug-fix 等)
- **SPEC 作成/修正後は必ず `ui-approval-gate` を呼出** (ワイヤーフレーム作成 + ユーザー承認必須)
- **Readiness Gate は UI 承認後に直接実行** (別途スキル呼出なし)
- 各段階の結果を明確に報告
- 進行状況を継続的に更新
- 下位スキルの出力を要約して伝達
- 予想される次段階を案内
- **実装完了後 `feature-wiring` を呼出** (データソース連動 + ナビゲーション連結必須)
- **wiring 完了後 `pre-quality-gate` を呼出** (QA サイクル通過必須)
- **QA 通過後 `feature-status-sync` を呼出** (index.md 状態同期必須)
- **BUG_FIX 時は必ず `bug-fix` スキルを呼出** (体系的バグ分析および修正)
- **progress 変化 >= 10% または priority 14日+ 経過時に `priority-analyzer` を呼出** (優先順位最新化)
- **コンテキスト収集時に `turbo-mode` を活用** (並列読取で効率性向上)
- **Tier 1 作業または「最後まで」要求時に `persistent-mode` を活性化** (検証完了まで自動継続)

### DON'T (やってはいけないこと)

- ユーザーにどのスキルを使うべきか質問
- 作業タイプ判別なしに直接実装開始
- **下位スキル呼出なしで直接作業実行** (例: SPEC 修正時に feature-spec-updater なしで直接修正、バグ修正時に bug-fix なしで直接修正)
- **UI 承認なしに Readiness Gate へ進行** (ui-approval-gate スキップ禁止)
- Readiness Gate 検証なしに実装進行 (NEW_FEATURE/MODIFY_FEATURE)
- 中間段階をスキップ
- **wiring スキルなしに feature-status-sync 進行** (空データ/孤児ページ問題発生)
- **状態同期 (feature-status-sync) なしに品質検証 (pre-quality-gate) 進行**
- **バグ修正時に回帰テストなしで修正完了** (bug-fix スキルが強制)
- **NEW_FEATURE で feature-architect をスキップ** (Option B 原則 - CONTEXT.json 作成は architect のみ可能)
- **CONTEXT.json なしで feature-spec-generator を直接呼出** (必須前提条件違反)

---

## 使用例

```bash
# 自然言語で要求 (推奨)
"ユーザーが提出したコードを分析して教育的な説明を生成する機能が必要"

# 具体的な修正要求
"001-code-analysis でコード分析後の説明テキストの品質を改善"

# バグ修正要求
"Diff表示画面でシンタックスハイライトが動かない問題を修正して"

# リサーチ要求
"競合サービスのコード教育機能を分析して"
```

---

## 参照文書

### 核心パイプラインスキル

- [Readiness Gate 詳細チェックリスト](references/readiness-checklist.md)
- [feature-architect スキル](../feature-architect/SKILL.md)
- [feature-spec-generator スキル](../feature-spec-generator/SKILL.md) - 新 SPEC 作成
- [feature-spec-updater スキル](../feature-spec-updater/SKILL.md) - 既存 SPEC 修正
- [ui-approval-gate スキル](../ui-approval-gate/SKILL.md) - UI ワイヤーフレーム承認ゲート
- [bug-fix スキル](../bug-fix/SKILL.md) - バグ分析および修正
- [feature-wiring スキル](../feature-wiring/SKILL.md) - データ連動 + ナビゲーション連結
- [feature-status-sync スキル](../feature-status-sync/SKILL.md) - index.md 状態同期

### 効率性・品質スキル

- [turbo-mode スキル](../turbo-mode/SKILL.md) - 並列実行 + 3-Tier モデルルーティング
- [persistent-mode スキル](../persistent-mode/SKILL.md) - 検証完了まで自動継続
- [pre-quality-gate スキル](../pre-quality-gate/SKILL.md) - lint/test/アーキテクチャ QA サイクル

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                                                                                                                                                                                                                                                                                                                                    |
| ---------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-02-11 | v1.0.0     | **プロジェクト 向け新規作成**: 旧プロジェクトから Next.js/Japanese に全面移行。CONVERT_CANDIDATE/REVERT_CANDIDATE パイプライン削除。Team Mode 削除。品質ゲート更新。security-scan 独立スキル参照削除。Evidence Cache を npm run lint / npm test に更新。turbo-mode バッチ順序を Type+API → Hook → Component → Test に変更。全テキスト日本語化。 |
